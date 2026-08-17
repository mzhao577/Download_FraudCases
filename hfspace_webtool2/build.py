#!/usr/bin/env python3
"""Assemble the static build of webtool2 for a Hugging Face Space.

Takes the live tool's own UI and turns it into files a static host can serve:

    index.html   webtool2/static/index.html, with one <script> tag added so the
                 API calls are answered in the browser by static-api.js
    data/        the summary CSV
    pdf/         the case PDFs, plus manifest.json listing what is there
                 (a static host cannot stat a folder, so has_pdf needs the list)

    python hfspace_webtool2/build.py                 # CSV only
    python hfspace_webtool2/build.py --pdfs          # with all 679 PDFs
    python hfspace_webtool2/build.py --pdfs --limit 5

The UI is copied, never edited by hand, so a change to the local tool reaches
the Space by rerunning this.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC_HTML = ROOT / "webtool2" / "static" / "index.html"
SRC_INPUT = ROOT / "downloaded" / "webtool2"

INJECT = '<script src="static-api.js"></script>\n<script>\n'


def build_html() -> str:
    html = SRC_HTML.read_text(encoding="utf-8")
    # The UI's own code is one inline <script> at the end; the shim has to be
    # installed before it runs, so it goes immediately in front.
    marker = "<script>\n"
    if marker not in html:
        raise SystemExit(f"could not find the inline script tag in {SRC_HTML}")
    if "static-api.js" in html:
        raise SystemExit("index.html already references static-api.js")
    return html.replace(marker, INJECT, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", type=Path, default=SRC_INPUT)
    ap.add_argument("--pdfs", action="store_true", help="copy the PDFs as well")
    ap.add_argument("--limit", type=int, default=None, help="first N PDFs only (smoke test)")
    a = ap.parse_args()

    csvs = sorted(a.input_dir.glob("*.csv"))
    if not csvs:
        print(f"no CSV in {a.input_dir}", file=sys.stderr)
        return 2
    src_csv = max(csvs, key=lambda p: len(p.stem))
    pdf_src = next((p for p in a.input_dir.iterdir() if p.is_dir()), None)

    (HERE / "data").mkdir(exist_ok=True)
    shutil.copy2(src_csv, HERE / "data" / src_csv.name)
    (HERE / "index.html").write_text(build_html(), encoding="utf-8")

    with (HERE / "data" / src_csv.name).open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    wanted = [(r.get("DocumentName") or "").strip() for r in rows]

    out_pdf = HERE / "pdf"
    copied, missing = 0, []
    if a.pdfs and pdf_src:
        out_pdf.mkdir(exist_ok=True)
        for name in (wanted[: a.limit] if a.limit else wanted):
            src = (pdf_src / name).resolve()      # the input folder holds symlinks
            if not src.is_file():
                missing.append(name)
                continue
            dst = out_pdf / name
            if not dst.exists() or dst.stat().st_size != src.stat().st_size:
                shutil.copy2(src, dst)
            copied += 1
    have = sorted(p.name for p in out_pdf.glob("*.pdf")) if out_pdf.is_dir() else []
    if have:
        (out_pdf / "manifest.json").write_text(json.dumps(have), encoding="utf-8")

    size = sum(p.stat().st_size for p in HERE.rglob("*") if p.is_file()) / 1e6
    print(f"index.html   <- {SRC_HTML.relative_to(ROOT)} (+ static-api.js)")
    print(f"data/{src_csv.name}  {len(rows)} rows")
    print(f"pdf/         {len(have)} files" + (f", {copied} copied" if a.pdfs else " (skipped)"))
    if missing:
        print(f"             {len(missing)} rows have no PDF, e.g. {missing[:2]}")
    print(f"total        {size:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
