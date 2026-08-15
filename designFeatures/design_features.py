#!/usr/bin/env python3
"""Design monitoring features from the extracted case summaries.

Reads every SchemeSummary in the input CSV plus the deterministic evidence from
analyze.py, and produces a set of monitoring features that could be computed
against claims, enrolment and credentialing data.

    python designFeatures/design_features.py downloaded/webtool/extractedSummary_2025_DOJ.csv

Writes designFeatures/monitoring_features.{json,md}.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List

import anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-5"
# Ten features with this many fields runs well past 16k output tokens, and the
# SDK requires streaming above that - so stream and take the final message.
MAX_TOKENS = 48000
TIMEOUT_S = 1800


class Feature(BaseModel):
    id: str = Field(description="Short stable id, snake_case, e.g. 'weekly_service_hours_per_npi'.")
    name: str = Field(description="Human-readable feature name, under 60 characters.")
    service_groups: List[str] = Field(
        description="Service groups this monitors, using the vocabulary in the data "
                    "(HomeHealth, Telehealth, DME, Laboratory, Pharmacy, "
                    "PhysicianPractice, BehavioralHealth, GeneticTesting, Hospice, "
                    "NursingHome, PersonalCare, SubstanceUseTreatment, Hospital, "
                    "Transportation, Chiropractic, Optometry, Dental, All)."
    )
    mechanic: str = Field(
        description="The fraud mechanic this catches, in one sentence, as seen in the cases."
    )
    feature_definition: str = Field(
        description="What the feature computes, precisely enough to implement: the "
                    "unit of observation, the numerator/denominator or aggregation, "
                    "and the time window. No vague verbs."
    )
    alert_logic: str = Field(
        description="A concrete starting rule - a threshold, percentile, ratio or "
                    "change-point - and what it does when it fires (flag for review, "
                    "prepay edit, records request). State that thresholds need "
                    "calibration against a control population."
    )
    data_required: List[str] = Field(
        description="The data elements needed, e.g. 'claim line rendering NPI', "
                    "'state licence status by date', 'Part A inpatient dates'."
    )
    evidence_cases: int = Field(
        description="How many of the 679 cases support this feature, from the corpus."
    )
    example_documents: List[str] = Field(
        description="2-4 DocumentName values from the corpus that motivate this feature. "
                    "Must be exact filenames that appear in the input."
    )
    false_positives: str = Field(
        description="The main benign explanation that would trip this feature, and how "
                    "to damp it. Be specific."
    )
    priority: str = Field(description="high, medium or low, by case volume x implementability.")


class FeatureSet(BaseModel):
    features: List[Feature] = Field(description="Exactly 10 monitoring features, highest priority first.")
    corpus_notes: str = Field(
        description="2-4 sentences on what the corpus can and cannot support for "
                    "feature design - what is under-represented, and what these "
                    "documents do not contain."
    )


SYSTEM = """
You design fraud-monitoring features for a health care payer. Your input is a
corpus of summaries of real prosecuted medical fraud cases (DOJ, 2025) plus
deterministic counts of recurring mechanics.

Design features that a payer could actually compute against claims, enrolment
and credentialing data. Rules:

- Ground every feature in the corpus. Cite real DocumentName values and a real
  case count. Never invent a case or inflate a count.
- A feature must be COMPUTABLE. "Monitor for suspicious billing" is not a
  feature. "Ratio of level-4/5 E&M codes to all E&M for a rendering NPI,
  monthly, versus specialty peers" is.
- Prefer features that catch a mechanic appearing across MANY cases over ones
  that fit a single spectacular case.
- Prefer signals visible BEFORE payment where possible, and say when a feature
  can only work retrospectively.
- The corpus is press-release prose, not claims data. It tells you what schemes
  look like, not what thresholds to use. Say so rather than inventing numbers
  that sound authoritative.
- Every feature will generate false positives. Name the benign explanation.

Cover a spread of service groups rather than clustering on one, and include at
least one enrolment/credentialing feature and one that needs no claims history
(so it works for a brand-new provider).
""".strip()


def build_corpus(rows: list[dict]) -> str:
    parts = []
    for r in rows:
        s = (r.get("SchemeSummary") or "").strip()
        if not s:
            continue
        parts.append(
            f"[{r['DocumentName']}]\n"
            f"service={r.get('Service') or '-'} | types={r.get('FraudTypeAll') or '-'} | "
            f"payer={r.get('PayerName') or '-'} | amount={r.get('FraudAmt') or '-'}\n{s}"
        )
    return "\n\n".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--evidence", type=Path, default=Path("designFeatures/evidence.json"))
    ap.add_argument("--out", type=Path, default=Path("designFeatures/monitoring_features.json"))
    ap.add_argument("--effort", default="high")
    a = ap.parse_args()

    rows = list(csv.DictReader(a.csv_path.open(encoding="utf-8-sig")))
    corpus = build_corpus(rows)
    evidence = json.loads(a.evidence.read_text()) if a.evidence.exists() else {}

    print(f"{len(rows)} cases, {len(corpus):,} chars of summary text")

    client = anthropic.Anthropic(max_retries=4, timeout=TIMEOUT_S)
    user = (
        "Deterministic mechanic counts over the same corpus (regex probes, so these "
        "are lower bounds - the prose is compressed):\n"
        f"{json.dumps(evidence.get('mechanics', {}), indent=2)[:6000]}\n\n"
        f"Service group counts:\n{json.dumps(evidence.get('service_counts', []))}\n\n"
        "=== CASE SUMMARIES ===\n" + corpus
    )

    # Structured outputs require additionalProperties:false on EVERY object,
    # including the nested Feature schema pydantic puts under $defs.
    def close(node):
        if isinstance(node, dict):
            if node.get("type") == "object":
                node["additionalProperties"] = False
            for v in node.values():
                close(v)
        elif isinstance(node, list):
            for v in node:
                close(v)
        return node

    schema = close(FeatureSet.model_json_schema())

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        output_config={"effort": a.effort,
                       "format": {"type": "json_schema", "schema": schema}},
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
    ) as stream:
        response = stream.get_final_message()

    if response.stop_reason == "refusal":
        print("request was declined", file=sys.stderr)
        return 1
    if response.stop_reason == "max_tokens":
        print("output hit max_tokens - raise MAX_TOKENS and retry", file=sys.stderr)
        return 1

    text = "".join(b.text for b in response.content if b.type == "text")
    fs = FeatureSet.model_validate_json(text)
    u = response.usage
    print(f"designed {len(fs.features)} features  "
          f"(in {u.input_tokens:,} / out {u.output_tokens:,} tokens)")

    # Verify every cited document actually exists - a fabricated citation would
    # make the whole document untrustworthy.
    known = {r["DocumentName"] for r in rows}
    bad = [(f.id, d) for f in fs.features for d in f.example_documents if d not in known]
    if bad:
        print(f"WARNING: {len(bad)} cited documents are not in the corpus:", file=sys.stderr)
        for fid, d in bad[:10]:
            print(f"  {fid}: {d}", file=sys.stderr)
    else:
        print("all cited example documents exist in the corpus")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(fs.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
