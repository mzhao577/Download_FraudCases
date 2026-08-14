#!/usr/bin/env python3
"""Step 4 (optional) - check the corpus for gaps.

Reports, per source: documents missing their HTML, missing the PDF rendering of
that HTML, or suspiciously small (a bot wall or an error page rather than a
document). Nothing is re-fetched here - `download.py` is resumable, so rerun it
(add --force for the entries flagged as too small) to fill the gaps.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict

from fraudscrape import config
from fraudscrape.models import read_manifest

MIN_HTML_BYTES = 3_000
MIN_PDF_BYTES = 2_000
BINARY_TYPES = {"pdf", "csv", "zip", "xlsx", "xls", "doc", "docx", "txt"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sources", nargs="*", default=None)
    ap.add_argument("--list", type=int, default=10,
                    help="how many example URLs to print per problem class")
    args = ap.parse_args()

    docs = read_manifest()
    if args.sources:
        docs = [d for d in docs if d.source in args.sources]
    if not docs:
        print("manifest is empty - run discover.py first")
        return 2

    problems: dict[str, list[str]] = defaultdict(list)
    per_source = defaultdict(Counter)

    for d in docs:
        base = d.dest_base()
        per_source[d.source]["manifest"] += 1
        if d.doc_type.lower() in BINARY_TYPES:
            f = base.with_suffix(f".{d.doc_type.lower()}")
            if not f.exists() or f.stat().st_size == 0:
                problems["missing data file"].append(d.url)
            else:
                per_source[d.source]["ok"] += 1
            continue

        html, pdf = base.with_suffix(".html"), base.with_suffix(".pdf")
        if not html.exists():
            problems["missing html"].append(d.url)
            continue
        if html.stat().st_size < MIN_HTML_BYTES:
            problems["html suspiciously small"].append(d.url)
        if not pdf.exists():
            problems["missing pdf"].append(d.url)
            continue
        if pdf.stat().st_size < MIN_PDF_BYTES:
            problems["pdf suspiciously small"].append(d.url)
        per_source[d.source]["ok"] += 1

    print(f"{'source':<10} {'manifest':>9} {'complete':>9} {'gap':>6}")
    total_m = total_ok = 0
    for src in sorted(per_source):
        m, ok = per_source[src]["manifest"], per_source[src]["ok"]
        total_m, total_ok = total_m + m, total_ok + ok
        print(f"{src:<10} {m:>9,} {ok:>9,} {m - ok:>6,}")
    print(f"{'TOTAL':<10} {total_m:>9,} {total_ok:>9,} {total_m - total_ok:>6,}")

    if problems:
        print()
        for kind, urls in sorted(problems.items(), key=lambda kv: -len(kv[1])):
            print(f"{kind}: {len(urls):,}")
            for u in urls[: args.list]:
                print(f"   {u}")
    else:
        print("\nno gaps found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
