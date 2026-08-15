#!/usr/bin/env python3
"""Add a MonitoringFeature column to the case summary CSV.

For every case, decide which of the 10 monitoring features would have been the
one most likely to catch it. The output is the input CSV unchanged plus one
extra column.

    python designFeatures/label_cases.py downloaded/webtool/extractedSummary_2025_DOJ.csv

Two methods:

  --method llm    (default) Claude reads each summary and picks the feature most
                  likely to catch it, in batches, with the label constrained to
                  the 10 feature ids by a closed enum.
  --method rules  offline keyword scoring, no API key needed. Recall is much
                  lower (~38% vs ~95%) because the summaries are free prose, so
                  it is a fallback rather than the default.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

import anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-5"
BATCH = 40

NEW_COLUMN = "MonitoringFeature"
UNASSIGNED = "none - no feature clearly applies"

# feature id -> (signature regexes over SchemeSummary, service groups it targets)
# The regexes restate the mechanic each feature was designed to catch; the
# service groups come from the feature definitions themselves.
SIGNATURES: dict[str, tuple[str, set[str]]] = {
    "signoff_velocity_orders_per_signing_npi": (
        r"telemedicine|telehealth|sign(ed|ing)? .{0,30}(order|prescription)|never (spoke|examin|saw)|"
        r"sight-unseen|brief telephon|without .{0,25}(examin|seeing|speaking)|telemarket|call cent|"
        r"lead generat|doctor.{0,20}(paid|bribed) to (sign|order)",
        {"Telehealth", "DME", "GeneticTesting", "Laboratory", "Pharmacy"}),

    "impossible_service_day_hours": (
        r"impossible|more (hours|time) than|24 hours|hours .{0,20}(never|not) (worked|provided)|"
        r"exceed(ed|ing)? .{0,25}(capacity|hours|day)|timesheet|billed .{0,20}hours|"
        r"same time|overlapping (visit|session|service)|more than .{0,15}(could|possible)",
        {"BehavioralHealth", "SubstanceUseTreatment", "PhysicianPractice", "HomeHealth",
         "PersonalCare", "Chiropractic"}),

    "service_date_vs_beneficiary_status": (
        r"deceased|dead patient|after .{0,20}died|while .{0,25}(hospitali[sz]ed|inpatient|incarcerated|in jail|in prison)|"
        r"patients who were (dead|deceased|hospitali)",
        set()),  # "All" - no service restriction

    "new_supplier_ramp_no_history": (
        r"newly (enrolled|acquired|formed)|shortly after (enrolling|enrollment|acquiring)|"
        r"(bought|purchased|acquired) .{0,40}(compan|suppli|pharmac|lab)|dormant|"
        r"rapidly (billed|submitted)|within (weeks|days|months) of",
        {"DME", "Laboratory", "GeneticTesting", "Hospice", "HomeHealth", "BehavioralHealth"}),

    "enrolment_exclusion_and_hidden_ownership": (
        r"nominee|straw (owner|buyer)|shell (compan|corporation)|conceal(ed|ing) .{0,30}ownership|"
        r"hidden owner|figurehead|exclud(ed|sion)|unlicensed|suspended licen|revoked licen|"
        r"expired licen|barred from|prior conviction|not licensed",
        {"DME", "Hospice", "Laboratory", "BehavioralHealth", "HomeHealth", "Pharmacy",
         "SubstanceUseTreatment"}),

    "pharmacy_dispense_vs_wholesale_purchase": (
        r"never (dispensed|filled|shipped)|not dispensed|drugs? .{0,25}never|"
        r"prescriptions? .{0,20}never (filled|dispensed)|billed for (drug|medication|prescription)|"
        r"compound(ed|ing)|inventory|wholesal",
        {"Pharmacy"}),

    "lab_panel_stacking_and_reflex_without_review": (
        r"urine drug test|urinalysis|toxicolog|confirmatory test|presumptive|panel|"
        r"unnecessary .{0,20}test|respiratory panel|COVID .{0,20}(test|add-?on)|bundl",
        {"Laboratory", "SubstanceUseTreatment", "PhysicianPractice"}),

    "hospice_nonterminal_and_live_discharge": (
        r"hospice|terminal(ly)? ill|six months? to live|end.of.life|live discharge|"
        r"not (terminally )?ill|certif(ied|ying) .{0,25}(terminal|hospice)",
        {"Hospice", "NursingHome", "HomeHealth"}),

    "evv_geolocation_and_attendant_overlap": (
        r"electronic visit verification|EVV|home (visit|health aide|care aide)|attendant|caregiver|"
        r"personal care (aide|service|attendant)|visits? (that )?(never|did not) (occur|happen|take place)|"
        r"aide .{0,20}(never|not)",
        {"PersonalCare", "HomeHealth", "BehavioralHealth", "AdultDayCare"}),

    "procedure_substitution_upcode_pairs": (
        r"upcod|higher(-| )(level|paying|reimburs)|billed .{0,25}as if|more expensive (code|procedure)|"
        r"level (4|5|four|five)|substitut(ed|ing)|different (code|procedure) than|"
        r"cheaper .{0,20}(device|product|version)|misrepresent(ed|ing) .{0,25}(procedure|service|code)",
        {"PhysicianPractice", "DME", "Chiropractic", "Optometry", "NursingHome", "WoundCare"}),
}

SERVICE_WEIGHT = 2   # the case is in a service group the feature targets
PROBE_WEIGHT = 3     # the summary shows the mechanic the feature detects
MIN_SCORE = 3        # below this, no feature is claimed


def split(v: str | None) -> list[str]:
    return [x.strip() for x in (v or "").split(";") if x.strip()]


def score_case(summary: str, services: set[str], order: list[str]) -> tuple[str, dict[str, int]]:
    scores: dict[str, int] = {}
    for fid, (pattern, groups) in SIGNATURES.items():
        s = 0
        if re.search(pattern, summary, re.I):
            s += PROBE_WEIGHT
        if groups and services & groups:
            s += SERVICE_WEIGHT
        elif not groups:                       # the "All" feature
            s += 1
        if s:
            scores[fid] = s
    if not scores:
        return UNASSIGNED, {}
    best = max(scores.values())
    if best < MIN_SCORE:
        return UNASSIGNED, scores
    # Tie-break by the feature ordering in monitoring_features.json, which is
    # priority order - so a tie resolves to the higher-priority feature.
    winners = [f for f in order if scores.get(f) == best]
    return winners[0], scores


# --------------------------------------------------------------------------
# LLM assignment
# --------------------------------------------------------------------------

LLM_SYSTEM = """
You assign fraud cases to monitoring features. For each case you are given a
short summary of what the fraudsters actually did; pick the ONE feature from the
list that would most likely have caught that case in claims, enrolment or
credentialing data.

- Judge by the detection mechanism, not by the service line. A pharmacy case
  whose mechanic is a hidden owner belongs to the enrolment feature, not the
  pharmacy one.
- Pick the feature that would fire EARLIEST and most reliably on this case.
- Use "none" only when no feature plausibly applies - a case whose mechanic is
  outside every feature (pure tax fraud, arson, grant embezzlement, a loan
  scheme with no claims component). Do not use "none" merely because the fit is
  imperfect.
- Return one row per case, using the index given. Do not skip any.
""".strip()


def build_llm_types(order: list[str]):
    """Build the enum-constrained response schema for this feature set."""
    from typing import Literal
    Label = Literal[tuple(order + ["none"])]  # type: ignore[valid-type]

    class Assignment(BaseModel):
        index: int = Field(description="The case index exactly as given in the input.")
        feature_id: Label = Field(description="The feature that would catch this case, or 'none'.")

    class Batch(BaseModel):
        assignments: List[Assignment] = Field(description="One entry per case in the batch.")

    return Batch


def describe_features(feats: list[dict]) -> str:
    out = []
    for f in feats:
        out.append(f"{f['id']}\n  name: {f['name']}\n  catches: {f['mechanic']}\n"
                   f"  services: {', '.join(f['service_groups'])}")
    return "\n".join(out)


def label_batch(client, Batch, feature_text: str, chunk: list[tuple[int, dict]]) -> dict[int, str]:
    body = "\n\n".join(
        f"[{i}] service={r.get('Service') or '-'} | types={r.get('FraudTypeAll') or '-'}\n"
        f"{(r.get('SchemeSummary') or '').strip()}"
        for i, r in chunk)
    try:
        resp = client.messages.parse(
            model=MODEL, max_tokens=8000,
            output_format=Batch,
            output_config={"effort": "low"},
            system=[{"type": "text",
                     "text": LLM_SYSTEM + "\n\nFEATURES:\n" + feature_text,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": body}],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  batch starting at {chunk[0][0]} failed: {exc!r}"[:160], file=sys.stderr)
        return {}
    if resp.stop_reason == "refusal" or resp.parsed_output is None:
        return {}
    return {a.index: a.feature_id for a in resp.parsed_output.assignments}


def assign_llm(rows: list[dict], feats: list[dict], workers: int) -> dict[int, str]:
    order = [f["id"] for f in feats]
    Batch = build_llm_types(order)
    feature_text = describe_features(feats)
    client = anthropic.Anthropic(max_retries=4, timeout=600)

    indexed = list(enumerate(rows))
    chunks = [indexed[i:i + BATCH] for i in range(0, len(indexed), BATCH)]
    result: dict[int, str] = {}

    # First batch alone so the rest read its cached system prompt.
    result.update(label_batch(client, Batch, feature_text, chunks[0]))
    print(f"  1/{len(chunks)} batches")
    if len(chunks) > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = [pool.submit(label_batch, client, Batch, feature_text, c) for c in chunks[1:]]
            for n, f in enumerate(futs, start=2):
                result.update(f.result())
                if n % 5 == 0 or n == len(chunks):
                    print(f"  {n}/{len(chunks)} batches")
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--features", type=Path, default=Path("designFeatures/monitoring_features.json"))
    ap.add_argument("--out", type=Path, default=None,
                    help="output CSV (default: designFeatures/<input stem>_withFeature.csv)")
    ap.add_argument("--use-name", action="store_true",
                    help="write the human-readable feature name instead of the id")
    ap.add_argument("--method", choices=["llm", "rules"], default="llm",
                    help="llm reads each summary (default); rules is an offline fallback")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    feats = json.loads(a.features.read_text())["features"]
    order = [f["id"] for f in feats]
    name_of = {f["id"]: f["name"] for f in feats}
    unknown = set(SIGNATURES) - set(order)
    if unknown:
        print(f"error: signatures reference unknown feature ids: {unknown}", file=sys.stderr)
        return 2

    with a.csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    if NEW_COLUMN in cols:
        print(f"error: input already has a {NEW_COLUMN} column", file=sys.stderr)
        return 2

    counts: Counter = Counter()
    if a.method == "llm":
        print(f"labelling {len(rows)} cases with {MODEL} in batches of {BATCH}")
        assigned = assign_llm(rows, feats, a.workers)
        for i, r in enumerate(rows):
            fid = assigned.get(i, UNASSIGNED)
            if fid == "none":
                fid = UNASSIGNED
            r[NEW_COLUMN] = name_of.get(fid, fid) if a.use_name else fid
            counts[fid] += 1
    else:
        for r in rows:
            fid, _ = score_case(r.get("SchemeSummary") or "", set(split(r.get("Service"))), order)
            r[NEW_COLUMN] = name_of.get(fid, fid) if a.use_name else fid
            counts[fid] += 1

    out = a.out or Path("designFeatures") / f"{a.csv_path.stem}_withFeature.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols + [NEW_COLUMN])
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} rows, {len(cols)} columns + {NEW_COLUMN}\n")
    print(f"{'feature':<52}{'cases':>7}{'  %':>7}")
    for fid, n in counts.most_common():
        print(f"{fid:<52}{n:>7}{100 * n / len(rows):>7.1f}")
    assigned = len(rows) - counts[UNASSIGNED]
    print(f"\nassigned {assigned}/{len(rows)} ({100 * assigned / len(rows):.1f}%)")
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
