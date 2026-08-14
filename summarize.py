#!/usr/bin/env python3
"""Step 3 - count what was downloaded, per year and per source.

Writes summary/summary.md, summary/summary.csv, summary/summary.json and a copy
of the report at ./SUMMARY.md.
"""

from __future__ import annotations

import argparse
import sys

from fraudscrape import config, summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--print", dest="show", action="store_true",
                    help="also print the report to stdout")
    args = ap.parse_args()

    config.ensure_dirs()
    result = summary.build(write=True)
    print(f"documents: {result['documents_total']:,}")
    for src, n in sorted(result["documents_by_source"].items()):
        print(f"  {src:<10} {n:>7,}")
    print(f"-> {config.SUMMARY_DIR / 'summary.md'}")
    if args.show:
        print()
        print((config.SUMMARY_DIR / "summary.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
