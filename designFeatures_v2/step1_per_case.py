#!/usr/bin/env python3
"""Step 1 - for every case, work out how it could have been caught BEFORE payment.

For each row of the summary CSV, produce the three elements the brief asks for:

    DesiredServiceGroups   the provider types this applies to
    WaysToIdentify         how this case could have been spotted pre-payment
    FeaturesToCreate       the concrete, computable feature(s) to build

    python designFeatures_v2/step1_per_case.py <summary.csv>

Resumable: each batch is cached under designFeatures_v2/.cache/<prompt-id>/, so
a rerun only does the batches that are missing. The prompt id is a hash of the
system prompt, so editing the prompt below starts a fresh cache rather than
serving answers written to the old spec.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2lib as L  # noqa: E402

BATCH = 20

# Marker for cases with no claims-payment component. Written verbatim so the
# shape check, step 2's categoriser and a human reader all recognise them.
NO_CONTROL = "No payer-side control applies."

SYSTEM = f"""
You are a payment-integrity analyst. For each prosecuted fraud case you are
given, work out how that case could have been caught BY THE PAYER BEFORE THE
CLAIMS WERE PAID, and what to build so it is caught automatically next time.

For every case produce three things.

1. service_groups - the provider/service types this applies to. Use this
   vocabulary where it fits: HomeHealth, PersonalCare, NursingHome, Hospice,
   AdultDayCare, BehavioralHealth, SubstanceUseTreatment, PhysicalTherapy,
   SpeechTherapy, Pharmacy, Laboratory, GeneticTesting, DME, Telehealth,
   PhysicianPractice, Hospital, Dental, Ambulance, Transportation, Optometry,
   Chiropractic, Podiatry, WoundCare, Imaging, All. 1-4 entries. Give the groups
   the CONTROL should cover, not only the one this defendant happened to be in.

2. ways_to_identify - EXACTLY 4 or 5 sentences, one signal per sentence, the
   most decisive signal first. Each sentence names the observable signal AND the
   named data that carries it - a claim field, a form, a registry, a file.
   Name real things: the HCPCS/CPT/NDC billed, units and place of service, the
   ordering or referring NPI, the rendering NPI, dates of service, the CMS-855
   enrolment and ownership fields, PECOS, NPPES, the state licence board file,
   OIG LEIE, prior-auth records, EVV visit records, timesheets, OASIS/MDS
   assessments, ARCOS or wholesaler pedigree data, the beneficiary's other
   claims, the Death Master File, the payer's own remittance history.
   Say where in the lifecycle each signal is visible - enrolment, credentialing,
   prior authorisation, or claim adjudication.
   Hard limits: at most 25 words per sentence, one signal per sentence, no
   semicolon lists, no stacking clauses with "and"/"or" to smuggle in a second
   signal. Do not restate the case narrative and do not name the defendant.

3. features_to_create - 2 or 3 numbered checks, each written in EXACTLY this
   shape, one sentence each:

   1) <feature name>: on <unit of observation>, compute <the exact quantity,
   over named fields>; fires when <the comparison that trips it>; action
   <prepay edit | claim suspension | payment suspension | documentation request
   (ADR) | prior-authorisation requirement | site visit | postpay audit>.

   The unit of observation must be a real key an engineer can group by -
   provider NPI, provider NPI x week, beneficiary x supplier NPI, ordering NPI x
   HCPCS, claim line, rendering NPI x date of service, TIN, bank account.
   The computed quantity must be arithmetic over named data - a count, a sum, a
   rate, a ratio, a gap in days, overlapping minutes, a distinct-value count, a
   graph degree - never "review", "monitor", "assess", "analyse" or "flag".
   The trigger must be a stated comparison: above the calibrated percentile
   versus same-specialty peers, above the provider's own trailing baseline, a
   physical impossibility such as hours per day, or an exact registry mismatch.

Rules:
- Be specific to THIS case's mechanic. Do not restate a generic anti-fraud
  platitude. If two cases share a mechanic, they should get similar answers -
  that is expected and useful.
- Never invent a numeric cut-point. Write "above the calibrated percentile
  versus same-specialty peers" rather than a number you cannot support.
  Numbers that come from physics or the rule book are fine: 24 hours in a day,
  overlapping visit minutes, a licence expiry date, one device per lifetime.
- If the case has no claims-payment component at all (pure tax fraud, a loan
  scheme, street drug distribution, public corruption, or an annual round-up
  press release rather than a single case), use 2 or 3 sentences in
  ways_to_identify saying plainly that there is no claim and no adjudication
  point, then give the nearest non-claims detection route. Start
  features_to_create with the exact words "{NO_CONTROL}" and then, if one
  exists, one sentence on the nearest control outside the claims system.
- Return one entry per case, using the index given. Do not skip any.

WORKED EXAMPLE of the required style, for a telemarketed DME brace scheme:

ways_to_identify: "At adjudication, the ordering NPI on the L-code brace claims
has no prior evaluation-and-management encounter with that beneficiary. One
telehealth ordering NPI writes orders for beneficiaries in dozens of states in a
single week. Beneficiary residence ZIPs fall far outside the supplier's service
area on its CMS-855S enrolment record. The same beneficiary receives the same
L-code brace from several unrelated supplier NPIs within a month. Supplier
volume jumps from near-zero to peer-top-decile weeks after a PECOS ownership
change."

features_to_create: "1) Order-encounter gap: on claim line x ordering NPI,
compute the days between the date of service and the most recent E/M claim
between that ordering NPI and the beneficiary; fires when no such encounter
exists in the lookback window; action prepay edit. 2) Orderer dispersion: on
ordering NPI x week, compute the count of distinct beneficiary states and
distinct supplier NPIs on ordered DMEPOS claims; fires when above the calibrated
percentile versus same-specialty peers; action documentation request (ADR), then
payment suspension. 3) Duplicate device saturation: on beneficiary x HCPCS,
compute the count of distinct supplier NPIs paid in a rolling 30 days; fires
when that count exceeds one without a documented replacement reason; action
prepay edit."
""".strip()

# Cache is keyed on the prompt, so an edit above invalidates old answers.
PROMPT_ID = hashlib.sha1(SYSTEM.encode("utf-8")).hexdigest()[:8]
CACHE = L.HERE / ".cache" / PROMPT_ID


class CaseDesign(BaseModel):
    index: int = Field(description="The case index exactly as given.")
    service_groups: List[str] = Field(description="1-4 service groups from the vocabulary.")
    ways_to_identify: str = Field(
        description="4 or 5 sentences, one signal each, at most 25 words per sentence.")
    features_to_create: str = Field(
        description="2 or 3 numbered checks: 'N) name: on <unit>, compute <quantity>; "
                    "fires when <comparison>; action <action>.'")


class BatchOut(BaseModel):
    designs: List[CaseDesign] = Field(description="One entry per case in the batch.")


def ask(client, chunk: list[tuple[int, dict]], nudge: str = "",
        max_tokens: int = 32000) -> dict[int, dict]:
    """One model call for a chunk of cases. Empty dict on any failure.

    The nudge goes in a second system block so the long spec above stays a
    stable, cacheable prefix across the main pass and the re-asks.
    """
    system = [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}]
    if nudge:
        system.append({"type": "text", "text": nudge})
    body = "\n\n".join(L.case_block(i, r) for i, r in chunk)
    try:
        resp = client.messages.parse(
            model=L.MODEL,
            max_tokens=max_tokens,
            output_format=BatchOut,
            output_config={"effort": "medium"},
            system=system,
            messages=[{"role": "user", "content": body}],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  batch @{chunk[0][0]} failed: {exc!r}"[:170], file=sys.stderr)
        return {}
    if resp.stop_reason in ("refusal", "max_tokens") or resp.parsed_output is None:
        print(f"  batch @{chunk[0][0]} unusable: {resp.stop_reason}", file=sys.stderr)
        return {}
    return {d.index: {"service_groups": d.service_groups,
                      "ways_to_identify": d.ways_to_identify.strip(),
                      "features_to_create": d.features_to_create.strip()}
            for d in resp.parsed_output.designs}


def run_batch(client, chunk: list[tuple[int, dict]]) -> dict[int, dict]:
    key = CACHE / f"batch_{chunk[0][0]:05d}.json"
    cached = L.load_json(key, None)
    if cached:
        return {int(k): v for k, v in cached.items()}
    out = ask(client, chunk)
    if out:
        L.save_json(key, out)
    return out


# Sentence boundary: a full stop followed by a capital or end of text. The
# lookbehind only skips single-letter initials ("U.S."); these answers end
# sentences on acronyms - NPI, PECOS, LEIE, EVV - all the time.
_SENT = re.compile(r"(?<!\b[A-Z])[.!?](?=\s+[A-Z(\"']|\s*$)")


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT.split(text or "") if s.strip()]


def defects(d: dict) -> tuple[list[str], int, int]:
    """Every way this design misses the spec, plus a defect count and word overage.

    The model occasionally answers a field with a placeholder such as "x", so
    length is checked too, not only structure.
    """
    ways = (d.get("ways_to_identify") or "").strip()
    feats = (d.get("features_to_create") or "").strip()
    sents = sentences(ways)
    no_control = feats.startswith(NO_CONTROL)
    lo = 1 if no_control else 4  # non-payer cases have little to say; let them be brief
    bad: list[str] = []
    over = 0

    if len(ways) < 60:
        bad.append("ways is empty or a stub")
    else:
        if not lo <= len(sents) <= 5:
            bad.append(f"ways has {len(sents)} sentences")
        longest = max(len(s.split()) for s in sents)
        if longest > 30:
            bad.append(f"ways has a {longest}-word sentence")
            over = longest - 25

    if no_control:
        return (bad, len(bad), over)  # non-payer cases need no numbered checks
    if len(feats) < 80:
        bad.append("features are empty or a stub")
    else:
        if not feats.startswith("1)"):
            bad.append("features are not numbered")
        if "fires when" not in feats.lower():
            bad.append("features have no trigger")
        if "action" not in feats.lower():
            bad.append("features have no action")
    return (bad, len(bad), over)


def shape_problem(d: dict) -> str | None:
    """The first way this design misses the required shape, or None if it is fine."""
    bad, _, _ = defects(d)
    return bad[0] if bad else None


def penalty(d: dict) -> tuple[int, int]:
    """How far this design is from the required shape. Lower is better."""
    _, n, over = defects(d)
    return (n, over)


def reask(client, rows: list[dict], idxs: list[int], nudge: str, tag: str,
          have: dict[int, dict] | None = None) -> dict[int, dict]:
    """Re-request a set of indices in small batches, caching each answer.

    Used twice: for indices the model silently dropped, and for answers that
    came back off-shape. When `have` is given, a rewrite is only taken if it is
    strictly closer to the required shape - a re-ask must never lose ground.
    """
    got: dict[int, dict] = {}
    nid = hashlib.sha1(nudge.encode("utf-8")).hexdigest()[:6]  # edit the nudge, re-ask
    for start in range(0, len(idxs), 5):
        want = idxs[start:start + 5]
        key = CACHE / f"{tag}_{nid}_{want[0]:05d}.json"
        cached = L.load_json(key, None)
        fresh = ({int(k): v for k, v in cached.items()} if cached
                 else ask(client, [(i, rows[i]) for i in want], nudge, max_tokens=16000))
        if not fresh:
            # A chunk can die on one long answer overrunning max_tokens. Asking
            # case by case costs more calls but never loses the whole chunk.
            print(f"  chunk @{want[0]} returned nothing - asking case by case", file=sys.stderr)
            for i in want:
                fresh.update(ask(client, [(i, rows[i])], nudge, max_tokens=16000))
        if fresh and not cached:
            L.save_json(key, fresh)
        for i, d in fresh.items():
            if have is not None and i in have and penalty(d) >= penalty(have[i]):
                continue
            got[i] = d
    return got


MISSING_NUDGE = (
    "EVERY case below must appear in your answer, including any that are not payer "
    f"fraud at all. For those, say so in ways_to_identify and start features_to_create "
    f"with '{NO_CONTROL}'")

SHAPE_NUDGE = (
    "The previous answers for these cases broke the required shape. Keep the content just "
    "as specific - only the shape needs fixing, and do not shorten by dropping signals.\n"
    "ways_to_identify must contain FOUR or FIVE complete sentences, never fewer and never "
    "more. Count the full stops before you answer. Each sentence carries exactly one "
    "signal, runs to at most 25 words, and names the data field, form or file the signal "
    "comes from. If a sentence is too long, split it into two signals rather than deleting "
    "it.\n"
    "features_to_create must be 2 or 3 checks numbered '1)', '2)', '3)', each reading "
    "'<name>: on <unit of observation>, compute <quantity over named fields>; fires when "
    "<comparison>; action <action>.'")


def report(designs: dict[int, dict]) -> None:
    """Print how well the corpus holds the required shape."""
    if not designs:
        return
    vals = list(designs.values())
    payer = [d for d in vals if not (d["features_to_create"] or "").startswith(NO_CONTROL)]
    problems = Counter()
    for d in vals:
        p = shape_problem(d)
        if p:
            problems[re.sub(r"\d+", "N", p)] += 1
    if payer:
        sents = [len(sentences(d["ways_to_identify"])) for d in payer]
        words = [len(d["ways_to_identify"].split()) for d in payer]
        checks = [len(re.findall(r"\b\d\)", d["features_to_create"])) for d in payer]
        print(f"  ways: {sum(sents)/len(sents):.1f} sentences, {sum(words)/len(words):.0f} words "
              f"on average; features: {sum(checks)/len(checks):.1f} numbered checks")
    print(f"  {len(vals) - len(payer)} cases with no payer-side control")
    for p, n in problems.most_common():
        print(f"  still off-shape: {n} x {p}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--out", type=Path, default=L.HERE / "per_case_designs.json")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=None, help="first N cases only (smoke test)")
    ap.add_argument("--no-shape-pass", action="store_true",
                    help="skip re-asking for answers that came back off-shape")
    a = ap.parse_args()

    rows, _ = L.load_rows(a.csv_path)
    if a.limit:
        rows = rows[: a.limit]
    indexed = list(enumerate(rows))
    chunks = [indexed[i:i + BATCH] for i in range(0, len(indexed), BATCH)]
    print(f"{len(rows)} cases in {len(chunks)} batches of {BATCH}")

    client = L.client()
    designs: dict[int, dict] = {}

    # First batch alone so the rest read the cached system prompt.
    designs.update(run_batch(client, chunks[0]))
    print(f"  1/{len(chunks)}")
    if len(chunks) > 1:
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            futs = [pool.submit(run_batch, client, c) for c in chunks[1:]]
            for n, f in enumerate(futs, start=2):
                designs.update(f.result())
                if n % 5 == 0 or n == len(chunks):
                    print(f"  {n}/{len(chunks)}")

    missing = [i for i in range(len(rows)) if i not in designs]
    if missing:
        print(f"\n{len(missing)} cases were skipped by the model - repairing individually")
        designs.update(reask(client, rows, missing, MISSING_NUDGE, "missing"))
        missing = [i for i in range(len(rows)) if i not in designs]

    # Second pass: anything that came back off-shape gets rewritten to spec.
    # Two rounds, because one rewrite does not always land.
    if not a.no_shape_pass:
        for rnd in (1, 2):
            off = [i for i in sorted(designs) if shape_problem(designs[i])]
            if not off:
                break
            print(f"\n{len(off)} answers are off-shape - rewriting to spec (round {rnd})")
            designs.update(reask(client, rows, off, SHAPE_NUDGE, f"shape{rnd}", have=designs))

    print(f"\ndesigned {len(designs)}/{len(rows)} cases"
          + (f"  ({len(missing)} still missing: {missing[:10]})" if missing else ""))
    report(designs)
    L.save_json(a.out, {str(k): v for k, v in sorted(designs.items())})
    print(f"-> {a.out}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
