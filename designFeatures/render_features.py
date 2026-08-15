#!/usr/bin/env python3
"""Render monitoring_features.json into the deliverable Markdown document.

Also cross-checks each feature's claimed case count against the deterministic
regex probes in evidence.json. The probes undercount (the summaries are
compressed prose), so a higher claim is not automatically wrong - but the
difference is surfaced rather than hidden.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Which deterministic probe is the closest lower bound for each feature.
PROBE_FOR = {
    "telehealth": "telehealth_signoff", "sign_off": "telehealth_signoff",
    "sign-off": "telehealth_signoff", "order": "telehealth_signoff",
    "impossible": "not_delivered", "service-day": "not_delivered",
    "death": "deceased_or_inpatient", "inpatient": "deceased_or_inpatient",
    "conflict": "deceased_or_inpatient",
    "enrol": "nominee_shell", "nominee": "nominee_shell", "excluded": "excluded_or_unlicensed",
    "dispens": "not_delivered", "wholesale": "not_delivered",
    "panel": "urine_drug_testing", "presumptive": "urine_drug_testing",
    "hospice": "medically_unnecessary",
    "evv": "impossible_volume", "double-booking": "impossible_volume",
    "upcod": "upcode_level", "substitution": "medically_unnecessary",
}


def probe_for(feature: dict, probes: dict) -> tuple[str | None, int | None]:
    hay = f"{feature['id']} {feature['name']}".lower()
    for key, probe in PROBE_FOR.items():
        if key in hay:
            return probe, probes.get(probe, {}).get("cases")
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--features", type=Path, default=Path("designFeatures/monitoring_features.json"))
    ap.add_argument("--evidence", type=Path, default=Path("designFeatures/evidence.json"))
    ap.add_argument("--out", type=Path, default=Path("designFeatures/monitoring_features.md"))
    a = ap.parse_args()

    fs = json.loads(a.features.read_text())
    ev = json.loads(a.evidence.read_text())
    probes = ev.get("mechanics", {})
    feats = fs["features"]

    L: list[str] = []
    A = L.append

    A("# Fraud Monitoring Features")
    A("")
    A("| | |")
    A("|---|---|")
    A(f"| **Source** | `{ev['source']}` — {ev['cases']} prosecuted cases (DOJ, 2025) |")
    A(f"| **Features** | {len(feats)} |")
    A(f"| **Generated** | {datetime.now().astimezone().strftime('%Y-%m-%d')} |")
    A("| **Specification** | [`instruction_designFeatures.md`](../instruction_designFeatures.md) |")
    A("| **Reproduce** | `designFeatures/analyze.py` → `design_features.py` → `render_features.py` |")
    A("")
    A("Each feature is a signal a payer could compute against claims, enrolment or "
      "credentialing data, derived from mechanics that recur across the case corpus.")
    A("")

    # ---------------------------------------------------------------- index
    A("## Index")
    A("")
    A("| # | Feature | Service groups | Cases | Priority |")
    A("|---:|---|---|---:|---|")
    for i, f in enumerate(feats, 1):
        A(f"| {i} | [{f['name']}](#{i}-{f['id'].replace('_', '-')}) "
          f"| {', '.join(f['service_groups'][:4])}{'…' if len(f['service_groups']) > 4 else ''} "
          f"| {f['evidence_cases']} | {f['priority']} |")
    A("")

    # ------------------------------------------------------- the features
    A("---")
    A("")
    for i, f in enumerate(feats, 1):
        A(f"## {i}. {f['name']}")
        A("")
        A(f"**Service groups** — {', '.join(f'`{s}`' for s in f['service_groups'])}")
        A("")
        A(f"**Mechanic.** {f['mechanic']}")
        A("")
        A("### Feature to be created")
        A("")
        A(f["feature_definition"])
        A("")
        A("### Alert logic")
        A("")
        A(f["alert_logic"])
        A("")
        A("### Data required")
        A("")
        for d in f["data_required"]:
            A(f"- {d}")
        A("")
        A("### Evidence")
        A("")
        probe, lower = probe_for(f, probes)
        line = f"**{f['evidence_cases']}** of {ev['cases']} cases support this feature."
        if lower is not None:
            if f["evidence_cases"] > lower:
                line += (f" The nearest keyword probe (`{probe}`) finds **{lower}**; the "
                         f"higher figure comes from reading the summaries in full, and is "
                         f"an estimate rather than a verified count.")
            else:
                line += f" Keyword probe `{probe}` independently finds {lower}."
        A(line)
        A("")
        A("Example cases:")
        A("")
        for d in f["example_documents"]:
            A(f"- `{d}`")
        A("")
        A("### False positives")
        A("")
        A(f["false_positives"])
        A("")
        A("---")
        A("")

    # --------------------------------------------------------- appendices
    A("## Appendix A — Mechanics found in the corpus")
    A("")
    A("Deterministic keyword probes over all 679 `SchemeSummary` values. These are "
      "**lower bounds**: the summaries are compressed prose, so a mechanic present in "
      "a case is not always phrased in a way a regex catches.")
    A("")
    A("| Mechanic | Cases | % | Top service groups |")
    A("|---|---:|---:|---|")
    for name, m in probes.items():
        svc = ", ".join(f"{s} ({n})" for s, n in m["top_services"][:4])
        A(f"| `{name}` | {m['cases']} | {m['pct']} | {svc} |")
    A("")

    A("## Appendix B — Corpus composition")
    A("")
    A("| Service group | Cases |")
    A("|---|---:|")
    for s, n in ev["service_counts"][:15]:
        A(f"| {s} | {n} |")
    A("")
    A("| Fraud type | Cases |")
    A("|---|---:|")
    for t, n in ev["fraudtype_counts"]:
        A(f"| {t} | {n} |")
    A("")

    A("## Appendix C — Limitations")
    A("")
    A(fs["corpus_notes"])
    A("")
    A("Additionally:")
    A("")
    A("- **No thresholds are supplied.** The corpus describes what schemes look like, "
      "not how often benign providers look similar. Every threshold above is a "
      "starting point to calibrate against a control population.")
    A("- **Selection bias runs one way.** Every case here was detected and prosecuted, "
      "so these are features for schemes that *got caught* — they may over-represent "
      "clumsy mechanics and under-represent successful fraud.")
    A("- **Case counts are evidence of a mechanic recurring, not of its prevalence** "
      "in the provider population.")

    a.out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{len(feats)} features -> {a.out}  ({len('\n'.join(L)):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
