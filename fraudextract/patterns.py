"""Aggregate the extracted cases: deterministic counts, then a narrative
pattern analysis, then the output files.

Counting is done in code, not by the model. The model is asked only for the
judgement layer - what the recurring schemes are and what they have in common.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import logging
import re
from collections import Counter
from pathlib import Path

import anthropic

from . import config
from .schema import CSV_COLUMNS

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# deterministic statistics
# --------------------------------------------------------------------------

def _split(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [p.strip() for p in re.split(r";|/(?![^()]*\))", str(value)) if p.strip()]


def _payer_bucket(payer: str) -> str:
    p = payer.lower()
    if "medicare" in p:
        return "Medicare"
    if "medicaid" in p or "medi-cal" in p:
        return "Medicaid"
    if "tricare" in p or "champva" in p:
        return "TRICARE/CHAMPVA"
    if any(k in p for k in ("blue cross", "aetna", "cigna", "united", "humana",
                            "commercial", "private")):
        return "Commercial payer"
    return payer.strip() or "unspecified"


def _state(value: str) -> str:
    return _split(value)[0].split("-")[0].strip() if value else ""


def _entity_key(value: str) -> str:
    """Normalised key for the lead defendant, used to spot repeat coverage."""
    lead = _split(value)[0] if value else ""
    lead = re.sub(r"\([^)]*\)", " ", lead)                       # drop "(owner)"
    lead = re.sub(r"\b(llc|inc|l\.l\.c|corp|co|ltd|agency|services|jr|sr|ii|iii)\b",
                  " ", lead, flags=re.IGNORECASE)
    return " ".join(sorted(re.findall(r"[a-z]{3,}", lead.lower())))


def duplicate_groups(rows: list[dict]) -> list[dict]:
    """Documents that appear to cover the same underlying case.

    A case is usually announced more than once - charge, plea, then sentencing -
    so "one PDF = one case" overcounts. Grouping on the lead defendant keeps the
    rows intact while making the double-count visible.
    """
    groups: dict[str, list[dict]] = {}
    for r in rows:
        key = _entity_key(r.get("FraudEntity") or "")
        if key:
            groups.setdefault(key, []).append(r)
    return [
        {
            "entity": members[0].get("FraudEntity"),
            "documents": [m.get("DocumentName") for m in members],
            "statuses": [m.get("CaseStatus") for m in members],
        }
        for members in groups.values()
        if len(members) > 1
    ]


def stats(rows: list[dict]) -> dict:
    good = [r for r in rows if "error" not in r]

    fraud_types = Counter()
    for r in good:
        for t in _split(r.get("FraudTypeAll")) or _split(r.get("FraudType")):
            fraud_types[t] += 1

    payers = Counter()
    for r in good:
        for p in _split(r.get("PayerName")):
            payers[_payer_bucket(p)] += 1

    states = Counter(s for r in good if (s := _state(r.get("State_County") or "")))
    statuses = Counter(r.get("CaseStatus") or "unspecified" for r in good)

    amounts = [r["FraudAmt"] for r in good if isinstance(r.get("FraudAmt"), (int, float))]
    settlements = [r["SettlementAmt"] for r in good
                   if isinstance(r.get("SettlementAmt"), (int, float))]
    sentences = [r["JailTime"] for r in good if isinstance(r.get("JailTime"), int)]

    combos = Counter()
    for r in good:
        types = _split(r.get("FraudTypeAll"))
        if len(types) > 1:
            combos[" + ".join(sorted(types))] += 1

    dupes = duplicate_groups(good)
    return {
        "documents": len(rows),
        "extracted": len(good),
        "failed": len(rows) - len(good),
        "distinct_cases": len(good) - sum(len(g["documents"]) - 1 for g in dupes),
        "repeat_coverage": dupes,
        "fraud_types": fraud_types.most_common(),
        "fraud_type_combinations": combos.most_common(),
        "payers": payers.most_common(),
        "states": states.most_common(),
        "case_status": statuses.most_common(),
        "fraud_amount": {
            "cases_with_amount": len(amounts),
            "total": sum(amounts),
            "median": sorted(amounts)[len(amounts) // 2] if amounts else None,
            "min": min(amounts) if amounts else None,
            "max": max(amounts) if amounts else None,
        },
        "settlement_amount": {
            "cases_with_amount": len(settlements),
            "total": sum(settlements),
        },
        "jail_months": {
            "cases_sentenced": len(sentences),
            "median": sorted(sentences)[len(sentences) // 2] if sentences else None,
            "min": min(sentences) if sentences else None,
            "max": max(sentences) if sentences else None,
        },
    }


# --------------------------------------------------------------------------
# narrative pattern analysis
# --------------------------------------------------------------------------

NARRATIVE_SYSTEM = """
You are a health care fraud analyst. You are given structured records extracted
from U.S. medical fraud cases, plus counts computed from them.

Write an analysis of the patterns: the recurring mechanics fraudsters used, what
the schemes have in common, which payers and provider types are hit, and which
signals would be visible in claims data. Ground every claim in the records - cite
the specific cases (by FraudEntity or DocumentName) that support each pattern.

Do not restate the counts you were given; interpret them. Say plainly when the
sample is too small to support a claim. Do not invent cases, amounts or facts
that are not in the records.

Output GitHub-flavoured markdown, starting at heading level 2. Cover:
## Recurring scheme patterns   - the mechanics, most common first
## What the schemes have in common
## Detection signals for a predictive model  - what would be visible in claims
## Caveats and sample limits
""".strip()


def narrative(rows: list[dict], computed: dict, *, effort: str = "high") -> str:
    """Ask Claude to interpret the extracted records. Returns markdown."""
    good = [{k: v for k, v in r.items() if k != "_meta"} for r in rows if "error" not in r]
    if not good:
        return "_No cases were extracted, so there is nothing to analyse._\n"

    payload = json.dumps({"cases": good, "computed_counts": computed},
                         indent=2, ensure_ascii=False)
    client = anthropic.Anthropic(max_retries=4)
    try:
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            output_config={"effort": effort},
            system=NARRATIVE_SYSTEM,
            messages=[{"role": "user", "content": payload}],
        )
    except anthropic.APIStatusError as exc:
        log.error("pattern analysis failed: %r", exc)
        return f"_Pattern analysis unavailable: {type(exc).__name__}._\n"

    if response.stop_reason == "refusal":
        return "_Pattern analysis unavailable: the request was declined._\n"
    return "".join(b.text for b in response.content if b.type == "text").strip() + "\n"


# --------------------------------------------------------------------------
# output files
# --------------------------------------------------------------------------

def _csv_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def write_outputs(rows: list[dict], computed: dict, analysis: str) -> None:
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    good = [r for r in rows if "error" not in r]
    errors = [r for r in rows if "error" in r]

    with config.CASES_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(CSV_COLUMNS)
        for r in sorted(good, key=lambda x: x.get("DocumentName", "")):
            writer.writerow([_csv_value(r.get(c)) for c in CSV_COLUMNS])

    config.CASES_JSON.write_text(
        json.dumps({"generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                    "model": config.MODEL,
                    "counts": computed,
                    "cases": [{k: v for k, v in r.items() if k != "_meta"} for r in good]},
                   indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    if errors:
        config.ERRORS_JSON.write_text(json.dumps(errors, indent=2), encoding="utf-8")
    elif config.ERRORS_JSON.exists():
        config.ERRORS_JSON.unlink()

    config.PATTERNS_MD.write_text(_markdown(good, computed, analysis), encoding="utf-8")


def _money(n) -> str:
    return f"${n:,.0f}" if isinstance(n, (int, float)) else "-"


def _markdown(good: list[dict], c: dict, analysis: str) -> str:
    L = []
    A = L.append
    A("# Medical Fraud Cases - Extracted Features and Patterns")
    A("")
    A(f"*Generated {dt.datetime.now().astimezone().isoformat(timespec='seconds')} "
      f"with `{config.MODEL}`*")
    A("")
    A(f"- Documents processed: **{c['documents']}** "
      f"(extracted {c['extracted']}, failed {c['failed']})")
    if c.get("repeat_coverage"):
        A(f"- Distinct cases: **{c['distinct_cases']}** - "
          f"{len(c['repeat_coverage'])} case(s) are covered by more than one document "
          f"(charge, plea and sentencing are announced separately), so per-document "
          f"counts overstate case counts")
    fa = c["fraud_amount"]
    A(f"- Fraud amounts stated in **{fa['cases_with_amount']}** cases, "
      f"totalling **{_money(fa['total'])}** "
      f"(median {_money(fa['median'])}, range {_money(fa['min'])} - {_money(fa['max'])})")
    sa = c["settlement_amount"]
    A(f"- Settlements/judgments stated in **{sa['cases_with_amount']}** cases, "
      f"totalling **{_money(sa['total'])}**")
    jt = c["jail_months"]
    A(f"- Custodial sentences imposed in **{jt['cases_sentenced']}** cases "
      f"(median {jt['median']} months, range {jt['min']}-{jt['max']})"
      if jt["cases_sentenced"] else "- No custodial sentences imposed in this sample")
    A("")

    A("## Cases")
    A("")
    A("| Document | Date | Entity | Payer | Fraud $ | Settlement $ | Jail (mo) | Type |")
    A("|---|---|---|---|---|---|---|---|")
    for r in sorted(good, key=lambda x: (x.get("ReportDT") or "")):
        A("| {doc} | {dt} | {ent} | {pay} | {amt} | {stl} | {jail} | {typ} |".format(
            doc=(r.get("DocumentName") or "")[:44],
            dt=r.get("ReportDT") or "-",
            ent=(r.get("FraudEntity") or "-")[:52],
            pay=(r.get("PayerName") or "-")[:28],
            amt=_money(r.get("FraudAmt")),
            stl=_money(r.get("SettlementAmt")),
            jail=r.get("JailTime") if r.get("JailTime") is not None else "-",
            typ=(r.get("FraudType") or "-")[:30],
        ))
    A("")

    def table(title: str, pairs, head: tuple[str, str]) -> None:
        if not pairs:
            return
        A(f"## {title}")
        A("")
        A(f"| {head[0]} | {head[1]} |")
        A("|---|---|")
        for key, n in pairs:
            A(f"| {key} | {n} |")
        A("")

    table("Fraud types (cases may carry several)", c["fraud_types"], ("Type", "Cases"))
    table("Scheme combinations", c["fraud_type_combinations"], ("Combination", "Cases"))
    table("Payers defrauded", c["payers"], ("Payer", "Cases"))
    table("States", c["states"], ("State", "Cases"))
    table("Case status", c["case_status"], ("Status", "Cases"))

    if c.get("repeat_coverage"):
        A("## Documents covering the same case")
        A("")
        A("| Entity | Documents | Stages |")
        A("|---|---|---|")
        for g in c["repeat_coverage"]:
            A("| {e} | {d} | {s} |".format(
                e=(g["entity"] or "-")[:60],
                d="<br>".join((n or "")[:50] for n in g["documents"]),
                s=", ".join(str(s) for s in g["statuses"]),
            ))
        A("")

    A("# Pattern analysis")
    A("")
    A(analysis)
    return "\n".join(L) + "\n"
