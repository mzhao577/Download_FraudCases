#!/usr/bin/env python3
"""Build the web tool's input folder from an existing corpus + extraction run.

The brief specifies this layout:

    ./downloaded/webtools/
        DOJ_2025/                          raw case PDFs
        extractedSummary_2025_DOJ.csv      one row per PDF

This wires that up from what the other pipelines already produced, without
copying gigabytes: the PDF folder is symlinked by default.

    python webtool/setup_input.py --key DOJ_2025
    python webtool/setup_input.py --key DOJ_2026 --copy
    python webtool/setup_input.py --key DOJ_2025 \\
        --pdf-dir downloaded/DOJ_2025 --csv extracted/DOJ_2025/cases.csv
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "downloaded" / "webtools"


def summary_csv_name(key: str) -> str:
    """DOJ_2025 -> extractedSummary_2025_DOJ.csv (the brief's example spelling)."""
    parts = key.split("_")
    return f"extractedSummary_{'_'.join(reversed(parts))}.csv" if len(parts) == 2 \
        else f"extractedSummary_{key}.csv"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default="DOJ_2025", help="dataset key, e.g. DOJ_2025")
    ap.add_argument("--pdf-dir", type=Path, default=None,
                    help="source PDFs (default: ./downloaded/<key>)")
    ap.add_argument("--csv", type=Path, default=None,
                    help="source summary CSV (default: ./extracted/<key>/cases.csv)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--copy", action="store_true",
                    help="copy the PDFs instead of symlinking (uses real disk)")
    args = ap.parse_args()

    pdf_src = (args.pdf_dir or ROOT / "downloaded" / args.key).resolve()
    csv_src = (args.csv or ROOT / "extracted" / args.key / "cases.csv").resolve()

    if not pdf_src.is_dir():
        print(f"error: PDF folder not found: {pdf_src}", file=sys.stderr); return 2
    if not csv_src.is_file():
        print(f"error: summary CSV not found: {csv_src}", file=sys.stderr)
        print("       run the extractor first: ./ExtractedAll_in1InputFolder.sh "
              f"{args.key}", file=sys.stderr)
        return 2

    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    dest_pdfs = out / args.key
    dest_csv = out / summary_csv_name(args.key)

    # --- PDFs -------------------------------------------------------------
    if dest_pdfs.is_symlink() or dest_pdfs.exists():
        if dest_pdfs.is_symlink():
            dest_pdfs.unlink()
        elif args.copy:
            shutil.rmtree(dest_pdfs)
    if args.copy:
        shutil.copytree(pdf_src, dest_pdfs, dirs_exist_ok=True)
        how = "copied"
    else:
        dest_pdfs.symlink_to(pdf_src, target_is_directory=True)
        how = "symlinked"

    # --- CSV --------------------------------------------------------------
    shutil.copy2(csv_src, dest_csv)

    # --- verify the join --------------------------------------------------
    with dest_csv.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    doc_col = next((c for c in (rows[0] if rows else {}) if c.lower() == "documentname"), None)
    pdfs = {p.name for p in dest_pdfs.glob("*.pdf")}
    names = {(r.get(doc_col) or "").strip() for r in rows} if doc_col else set()

    print(f"input folder : {out}")
    print(f"  {args.key}/  -> {how} from {pdf_src}  ({len(pdfs)} PDFs)")
    print(f"  {dest_csv.name}  ({len(rows)} rows)")
    if not doc_col:
        print("  WARNING: no DocumentName column - the tool cannot join rows to PDFs")
        return 1
    matched = len(names & pdfs)
    print(f"  join on {doc_col}: {matched} matched, "
          f"{len(names - pdfs)} rows without a PDF, {len(pdfs - names)} PDFs without a row")
    print(f"\nstart the tool:  python webtool/app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
