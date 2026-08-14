#!/usr/bin/env python3
"""Case review web tool - raw PDF on the left, extracted summary on the right.

    python webtool/app.py                         # ./downloaded/webtools
    python webtool/app.py --input-dir SOME/DIR
    python webtool/app.py --port 8080 --no-browser

Open http://127.0.0.1:8000 . Binds to localhost only; the PDFs are served from
the dataset folder and nowhere else.
"""

from __future__ import annotations

import argparse
import sys
import threading
import webbrowser
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dataset as ds  # noqa: E402

HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE.parent / "downloaded" / "webtools"

app = FastAPI(title="Fraud case review")
DATASETS: dict[str, ds.Dataset] = {}


def load(input_dir: Path) -> None:
    found = ds.discover(input_dir)
    if not found:
        raise SystemExit(ds.describe_problem(input_dir))
    DATASETS.clear()
    for d in found:
        DATASETS[d.key] = d
        print(f"  {d.key:<18} {len(d.rows):>5} cases  <-  {d.csv_path.name}")
        if d.missing_pdf:
            print(f"  {'':18} {len(d.missing_pdf):>5} rows have no PDF")
        if d.orphan_pdfs:
            print(f"  {'':18} {len(d.orphan_pdfs):>5} PDFs have no CSV row")


def _get(key: str | None) -> ds.Dataset:
    if not DATASETS:
        raise HTTPException(503, "no dataset loaded")
    if key is None:
        return next(iter(DATASETS.values()))
    if key not in DATASETS:
        raise HTTPException(404, f"unknown dataset '{key}'")
    return DATASETS[key]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (HERE / "static" / "index.html").read_text(encoding="utf-8")


@app.get("/api/datasets")
def api_datasets() -> JSONResponse:
    return JSONResponse([d.summary() for d in DATASETS.values()])


@app.get("/api/cases")
def api_cases(
    dataset: str | None = None,
    q: str | None = Query(None, description="free text, searched across every column"),
    fraud_type: str | None = None,
) -> JSONResponse:
    """The case list for the navigator: enough to show and filter, not the full row."""
    d = _get(dataset)
    doc, title_cols = d.doc_column, d.title_columns()
    ftype = ds._resolve(d.columns, "FraudType")

    rows = d.rows
    if q:
        needle = q.lower()
        # Search every column: the point of the tool is to spot a pattern such
        # as "99215" or "overtime" wherever it happens to be recorded.
        rows = [r for r in rows
                if any(needle in str(v).lower() for k, v in r.items() if not k.startswith("_"))]

    # Tab counts are taken after the search but before the type filter, so the
    # tabs show how the current search splits across fraud types - and picking a
    # tab does not make the other tabs' counts vanish.
    counts: dict[str, int] = {}
    if ftype:
        for r in rows:
            v = (r.get(ftype) or "").strip()
            if v:
                counts[v] = counts.get(v, 0) + 1
    searched_total = len(rows)

    if fraud_type:
        rows = [r for r in rows if (r.get(ftype) or "") == fraud_type]

    out = [{
        "index": r["_index"],
        "doc": r.get(doc, ""),
        "has_pdf": r["_has_pdf"],
        **{c: r.get(c, "") for c in title_cols},
    } for r in rows]
    # Most common first - that ordering is itself a finding when you are
    # looking for which schemes dominate.
    types = [{"value": v, "count": n}
             for v, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    return JSONResponse({"total": len(d.rows), "count": len(out),
                         "searched_total": searched_total,
                         "fraud_type_column": ftype,
                         "fraud_types": types, "cases": out})


@app.get("/api/case/{index}")
def api_case(index: int, dataset: str | None = None) -> JSONResponse:
    d = _get(dataset)
    if not 0 <= index < len(d.rows):
        raise HTTPException(404, f"case {index} out of range (0-{len(d.rows) - 1})")
    row = d.rows[index]
    fields = [{"name": c, "value": row.get(c, "")} for c in d.columns]
    return JSONResponse({
        "index": index,
        "dataset": d.key,
        "doc": row.get(d.doc_column, ""),
        "has_pdf": row["_has_pdf"],
        "title": [{"name": c, "value": row.get(c, "")} for c in d.title_columns()],
        "summary_column": d.summary_column,
        "summary_text": row.get(d.summary_column, "") if d.summary_column else "",
        "fields": fields,
        "pdf_url": f"/pdf/{d.key}/{row.get(d.doc_column, '')}" if row["_has_pdf"] else None,
    })


@app.get("/pdf/{dataset}/{filename}")
def pdf(dataset: str, filename: str) -> FileResponse:
    d = _get(dataset)
    path = d.pdf_for(filename)
    if path is None:
        raise HTTPException(404, f"no such PDF in {dataset}: {filename}")
    # inline so the browser renders it (scrollable and Ctrl-F searchable)
    return FileResponse(path, media_type="application/pdf",
                        headers={"Content-Disposition": f'inline; filename="{filename}"'})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT,
                    help=f"folder holding <KEY>/ and its summary CSV (default: {DEFAULT_INPUT})")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true", help="do not open a browser")
    args = ap.parse_args()

    print(f"loading from {args.input_dir}")
    load(args.input_dir)

    url = f"http://{args.host}:{args.port}"
    print(f"\n  ready -> {url}   (ctrl-c to stop)\n")
    if not args.no_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
