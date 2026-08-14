#!/usr/bin/env python3
"""Extract case features and fraud patterns from a folder of case PDFs.

Implements instruction_findpattern.txt: one PDF per fraud case in, one row per
case out, plus an analysis of the recurring schemes.

    python extract_patterns.py                          # ./downloaded/testdata_DOJ_2026
    python extract_patterns.py --input-dir some/folder
    python extract_patterns.py --limit 3                # smoke test
    python extract_patterns.py --effort high            # deeper reading per document
    python extract_patterns.py --no-analysis            # fields only, skip the narrative

Outputs to ./extracted/:
    cases.csv      one row per case, the fields from the brief
    cases.json     the same, plus the computed counts
    patterns.md    counts + the pattern analysis
    errors.json    written only if some document failed
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from fraudextract import config, extract, patterns, pdftext

log = logging.getLogger("extract_patterns")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--input-dir", type=Path, default=config.DEFAULT_INPUT_DIR,
                    help=f"folder of case PDFs (default: {config.DEFAULT_INPUT_DIR})")
    ap.add_argument("--output-dir", type=Path, default=None,
                    help="where to write cases.csv / cases.json / patterns.md "
                         "(default: ./extracted/)")
    ap.add_argument("--limit", type=int, default=None, help="process only the first N PDFs")
    ap.add_argument("--effort", default=config.EFFORT,
                    choices=["low", "medium", "high", "xhigh", "max"],
                    help=f"reasoning effort per document (default: {config.EFFORT})")
    ap.add_argument("--workers", type=int, default=4, help="parallel extractions")
    ap.add_argument("--force", action="store_true",
                    help="re-extract documents already in the cache")
    ap.add_argument("--no-analysis", action="store_true",
                    help="skip the narrative pattern analysis")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)

    if not args.input_dir.is_dir():
        log.error("input directory not found: %s", args.input_dir)
        return 2

    if args.output_dir:
        config.set_output_dir(args.output_dir)

    pdfs = pdftext.find_pdfs(args.input_dir)
    if args.limit:
        pdfs = pdfs[: args.limit]
    if not pdfs:
        log.error("no PDFs in %s", args.input_dir)
        return 2

    log.info("extracting %s case documents from %s (effort=%s)",
             len(pdfs), args.input_dir, args.effort)
    log.info("output -> %s", config.OUTPUT_DIR)
    rows = extract.extract_all(pdfs, effort=args.effort, workers=args.workers,
                               force=args.force)

    computed = patterns.stats(rows)
    analysis = ("_Pattern analysis skipped (--no-analysis)._\n" if args.no_analysis
                else patterns.narrative(rows, computed))
    patterns.write_outputs(rows, computed, analysis)

    log.info("-" * 60)
    log.info("%s/%s documents extracted", computed["extracted"], computed["documents"])
    if computed["failed"]:
        log.warning("%s failed - see %s", computed["failed"], config.ERRORS_JSON)
    for name in (config.CASES_CSV, config.CASES_JSON, config.PATTERNS_MD):
        log.info("-> %s", name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
