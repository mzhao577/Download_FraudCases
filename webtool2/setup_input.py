#!/usr/bin/env python3
"""Build webtool2's input folder: ./downloaded/webtool2/<KEY>/ + the summary CSV.

    python webtool2/setup_input.py --key DOJ_2025

Symlinks the PDF folder rather than copying it, so pointing at a 226 MB corpus
costs no disk. --copy makes a standalone folder.
"""
from __future__ import annotations
import argparse, csv, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "designFeatures_v2" / "extractedSummary_2025_DOJ_withFeatures.csv"

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", default="DOJ_2025")
    ap.add_argument("--pdf-dir", type=Path, default=None)
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--out", type=Path, default=ROOT / "downloaded" / "webtool2")
    ap.add_argument("--copy", action="store_true")
    a = ap.parse_args()

    pdf_src = (a.pdf_dir or ROOT / "downloaded" / a.key).resolve()
    if not pdf_src.is_dir():
        print(f"error: PDF folder not found: {pdf_src}", file=sys.stderr); return 2
    if not a.csv.is_file():
        print(f"error: CSV not found: {a.csv}", file=sys.stderr); return 2

    out = a.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    dest_pdfs = out / a.key
    if dest_pdfs.is_symlink(): dest_pdfs.unlink()
    elif dest_pdfs.exists() and a.copy: shutil.rmtree(dest_pdfs)
    if a.copy:
        shutil.copytree(pdf_src, dest_pdfs, dirs_exist_ok=True); how = "copied"
    else:
        dest_pdfs.symlink_to(pdf_src, target_is_directory=True); how = "symlinked"

    dest_csv = out / a.csv.name
    shutil.copy2(a.csv, dest_csv)

    rows = list(csv.DictReader(dest_csv.open(encoding="utf-8-sig")))
    cols = list(rows[0]) if rows else []
    pdfs = {p.name for p in dest_pdfs.glob("*.pdf")}
    names = {(r.get("DocumentName") or "").strip() for r in rows}
    si = cols.index("SchemeSummary") if "SchemeSummary" in cols else -1

    print(f"input folder : {out}")
    print(f"  {a.key}/  -> {how} from {pdf_src}  ({len(pdfs)} PDFs)")
    print(f"  {dest_csv.name}  ({len(rows)} rows, {len(cols)} columns)")
    print(f"  join on DocumentName: {len(names & pdfs)} matched, "
          f"{len(names - pdfs)} rows without a PDF, {len(pdfs - names)} PDFs without a row")
    if si >= 0:
        print(f"  shown under SchemeSummary: {', '.join(cols[si+1:]) or '(none)'}")
    print("\nstart the tool:  python webtool2/app.py")
    return 0

if __name__ == "__main__":
    sys.exit(main())
