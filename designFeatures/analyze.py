#!/usr/bin/env python3
"""Mine the extracted case summaries for recurring, *detectable* mechanics.

Counting is deterministic here on purpose: these numbers are the evidence base
for the monitoring features, so they must be reproducible rather than recalled.
Each probe is a mechanic that would leave a trace in claims, enrolment or
credentialing data - not a legal theory.
"""
from __future__ import annotations
import argparse, csv, json, re, sys
from collections import Counter
from pathlib import Path

# mechanic -> regex over SchemeSummary. Deliberately broad: these are for
# sizing a pattern, not for classifying a case.
PROBES = {
  "impossible_volume":      r"impossible|more hours than|24 hours|physically impossible|exceed(ed|ing)? .{0,20}(capacity|hours)|thousands of claims|hundreds of (claims|patients) (a|per) day",
  "no_records":             r"no (medical )?record|without (any )?documentation|lacked documentation|no supporting|never examined|no proof of delivery|undocumented",
  "not_delivered":          r"never (were )?(provided|delivered|dispensed|performed|rendered|shipped)|not (provided|delivered|dispensed|performed|rendered)|goods never",
  "excluded_or_unlicensed": r"exclud(ed|sion)|unlicensed|suspended licen|revoked licen|expired licen|not licensed|without a licen|barred from",
  "deceased_or_inpatient":  r"deceased|dead patient|after .{0,15}died|while .{0,20}(hospitali[sz]ed|inpatient|incarcerated)|nursing home resident",
  "telemarketing_leads":    r"telemarket|call cent|lead generat|marketing compan|patient recruit|recruiter|cold call",
  "telehealth_signoff":     r"telemedicine|telehealth|brief telephon|never spoke|without (ever )?(speaking|seeing|examining)|sight-unseen|cursory",
  "beneficiary_bribes":     r"paid (cash |gift |)?(kickback|bribe)s? to (patient|beneficiar)|gift card|cash payments to (patient|beneficiar)|paid beneficiaries",
  "sham_consulting":        r"consulting fee|medical director(ship)? (fee|agreement)|management service|MSO|sham (contract|agreement|lease)|speaker fee|marketing fee",
  "identity_misuse":        r"stolen (identit|Medicare number|beneficiar)|identity theft|misappropriat(ed|ing) .{0,20}(identit|number)|without .{0,20}knowledge or consent|compromised",
  "nominee_shell":          r"nominee|straw owner|shell (compan|corporation)|concealed (his|her|their|the) ownership|hidden owner|figurehead",
  "rapid_enrollment_spike": r"newly enrolled|shortly after (enrolling|enrollment)|recently acquired|bought .{0,30}(compan|suppli|pharmac)|dormant (compan|suppli)",
  "genetic_cancer_screen":  r"genetic test|cancer screening|CGx|pharmacogenetic|PGx|hereditary",
  "medically_unnecessary":  r"medically unnecessary|not medically necessary|regardless of (medical )?necessity|without regard to",
  "upcode_level":           r"upcod|higher(-| )(level|paying) code|billed .{0,20}as if|more expensive (code|procedure|service)|level (4|5|four|five)",
  "compound_or_expensive_rx": r"compound(ed|ing)? (cream|drug|medication)|expensive .{0,15}(drug|medication|cream)|high-reimburs",
  "covid_addon":            r"COVID|coronavirus|respiratory panel|add-?on test",
  "urine_drug_testing":     r"urine drug test|urinalysis|UDT|toxicology",
  "proof_of_delivery":      r"proof of delivery|never shipped|delivery record|signature (on|of) delivery",
  "unqualified_staff":      r"unqualified|unlicensed (staff|aide|technician)|not (a )?(licensed|qualified)|outside .{0,20}scope of practice|student|assistant performed",
}

def split(v): return [x.strip() for x in (v or "").split(";") if x.strip()]

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--out", type=Path, default=Path("designFeatures/evidence.json"))
    a = ap.parse_args()

    rows = list(csv.DictReader(a.csv_path.open(encoding="utf-8-sig")))
    text = {r["DocumentName"]: (r.get("SchemeSummary") or "") for r in rows}

    hits: dict[str, list[str]] = {}
    for name, pat in PROBES.items():
        rx = re.compile(pat, re.I)
        hits[name] = [d for d, t in text.items() if rx.search(t)]

    # which service groups each mechanic shows up in
    svc_of = {r["DocumentName"]: split(r.get("Service")) for r in rows}
    by_service = {
        name: Counter(s for d in docs for s in svc_of.get(d, [])).most_common(8)
        for name, docs in hits.items()
    }

    ev = {
        "source": str(a.csv_path),
        "cases": len(rows),
        "mechanics": {
            name: {"cases": len(docs), "pct": round(100 * len(docs) / len(rows), 1),
                   "top_services": by_service[name], "examples": docs[:4]}
            for name, docs in sorted(hits.items(), key=lambda kv: -len(kv[1]))
        },
        "service_counts": Counter(s for r in rows for s in split(r.get("Service"))).most_common(),
        "fraudtype_counts": Counter(t for r in rows for t in split(r.get("FraudTypeAll"))).most_common(),
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(ev, indent=2), encoding="utf-8")

    print(f"{len(rows)} cases from {a.csv_path.name}\n")
    print(f"{'mechanic':<26}{'cases':>7}{'  %':>6}   top service groups")
    for name, m in ev["mechanics"].items():
        svc = ", ".join(f"{s}({n})" for s, n in m["top_services"][:4])
        print(f"{name:<26}{m['cases']:>7}{m['pct']:>6}   {svc}")
    print(f"\n-> {a.out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
