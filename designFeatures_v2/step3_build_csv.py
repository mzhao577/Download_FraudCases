#!/usr/bin/env python3
"""Step 3 - write the output CSV and the category catalogue.

    python designFeatures_v2/step3_build_csv.py <summary.csv>

Output: every input column, plus

    DesiredServiceGroups   the provider types the control should cover
    WaysToIdentify         how the case could have been caught pre-payment
    FeaturesToCreate       the automated check(s) to build
    FeatureCategory        which of the ~20 categories that check belongs to

The brief asks for three new columns and, separately, for the features to be
grouped into categories. FeatureCategory is the fourth column that grouping
needs in order to be usable from the CSV.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2lib as L  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path", type=Path)
    ap.add_argument("--designs", type=Path, default=L.HERE / "per_case_designs.json")
    ap.add_argument("--categories", type=Path, default=L.HERE / "categories.json")
    ap.add_argument("--assignments", type=Path, default=L.HERE / "case_categories.json")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()

    rows, cols = L.load_rows(a.csv_path)
    designs = L.load_json(a.designs, {})
    cats = L.load_json(a.categories, [])
    assign = L.load_json(a.assignments, {})
    if not designs:
        print("no per-case designs - run step1 first", file=sys.stderr)
        return 2

    name_of = {c["id"]: c["name"] for c in cats}
    point_of = {c["id"]: c["control_point"] for c in cats}

    new_cols = [L.COL_SERVICE, L.COL_WAYS, L.COL_FEATURES, L.COL_CATEGORY]
    for c in new_cols:
        if c in cols:
            print(f"error: input already has a {c} column", file=sys.stderr)
            return 2

    missing_design = 0
    cat_counts: Counter = Counter()
    for i, r in enumerate(rows):
        d = designs.get(str(i))
        if not d:
            missing_design += 1
            r[L.COL_SERVICE] = r[L.COL_WAYS] = r[L.COL_FEATURES] = ""
            r[L.COL_CATEGORY] = ""
            continue
        r[L.COL_SERVICE] = "; ".join(d["service_groups"])
        r[L.COL_WAYS] = d["ways_to_identify"]
        r[L.COL_FEATURES] = d["features_to_create"]
        cid = assign.get(str(i), "")
        r[L.COL_CATEGORY] = name_of.get(cid, cid)
        cat_counts[name_of.get(cid, cid) or "(unassigned)"] += 1

    out = a.out or L.HERE / f"{a.csv_path.stem}_withFeatures.csv"
    L.write_rows(out, rows, cols + new_cols)

    # Category catalogue, so the ~20 groups are readable without the JSON.
    md = ["# Feature Categories", "",
          f"{len(cats)} categories covering {len(rows)} cases from `{a.csv_path.name}`.", "",
          "| Category | Control point | Cases | Definition |", "|---|---|---:|---|"]
    for c in sorted(cats, key=lambda c: -cat_counts.get(c["name"], 0)):
        md.append(f"| **{c['name']}** | `{c['control_point']}` | "
                  f"{cat_counts.get(c['name'], 0)} | {c['definition']} |")
    md += ["", "## By control point", "", "| Control point | Categories | Cases |", "|---|---:|---:|"]
    by_point: Counter = Counter()
    cats_per_point: Counter = Counter()
    for c in cats:
        by_point[c["control_point"]] += cat_counts.get(c["name"], 0)
        cats_per_point[c["control_point"]] += 1
    for p, n in by_point.most_common():
        md.append(f"| `{p}` | {cats_per_point[p]} | {n} |")
    md.append("")
    (L.HERE / "categories.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{len(rows)} rows, {len(cols)} + {len(new_cols)} columns")
    if missing_design:
        print(f"WARNING: {missing_design} rows have no design")
    print(f"\n{'category':<46}{'cases':>7}")
    for name, n in cat_counts.most_common():
        print(f"{name:<46}{n:>7}")
    print(f"\n-> {out}")
    print(f"-> {L.HERE / 'categories.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
