#!/usr/bin/env python3
"""webtool2 - case review with the prevention design shown under the summary.

Built to instruction_APIAnalisys.md, reading the designFeatures_v2 output: the
raw PDF on the left, and on the right the title, SchemeSummary, then the four
prevention columns, then everything else.

    python webtool2/app.py                        # ./downloaded/webtool2
    python webtool2/app.py --input-dir SOME/DIR
    python webtool2/app.py --port 9000 --no-browser

Binds to localhost only; PDFs are served from the dataset folder and nowhere else.
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
DEFAULT_INPUT = HERE.parent / "downloaded" / "webtool2"
DEFAULT_PORT = 8001          # webtool v1 owns 8000, so both can run at once

app = FastAPI(title="Fraud case review v2")
DATASETS: dict[str, ds.Dataset] = {}


def load(input_dir: Path) -> None:
    found = ds.discover(input_dir)
    if not found:
        raise SystemExit(ds.describe_problem(input_dir))
    DATASETS.clear()
    for d in found:
        DATASETS[d.key] = d
        print(f"  {d.key:<16} {len(d.rows):>5} cases  <-  {d.csv_path.name}")
        print(f"  {'':16} highlight columns: {', '.join(d.highlight_columns()) or '(none)'}")
        if d.missing_pdf:
            print(f"  {'':16} {len(d.missing_pdf):>5} rows have no PDF")
        if d.orphan_pdfs:
            print(f"  {'':16} {len(d.orphan_pdfs):>5} PDFs have no CSV row")


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
    tab_column: str | None = Query(None, description="column driving the tab strip"),
    tab_value: str | None = Query(None, description="selected tab"),
) -> JSONResponse:
    d = _get(dataset)
    doc, title_cols = d.doc_column, d.title_columns()
    tabs = d.tab_columns()
    tcol = tab_column if tab_column in d.columns else (tabs[0] if tabs else None)

    rows = d.rows
    if q:
        needle = q.lower()
        rows = [r for r in rows
                if any(needle in str(v).lower() for k, v in r.items() if not k.startswith("_"))]

    # Tab counts come after the search but before the tab filter, so the strip
    # shows how the current search splits, and picking a tab does not blank the
    # other counts.
    counts: dict[str, int] = {}
    if tcol:
        for r in rows:
            v = (r.get(tcol) or "").strip()
            if v:
                counts[v] = counts.get(v, 0) + 1
    searched_total = len(rows)

    if tcol and tab_value:
        rows = [r for r in rows if (r.get(tcol) or "") == tab_value]

    out = [{
        "index": r["_index"],
        "doc": r.get(doc, ""),
        "has_pdf": r["_has_pdf"],
        "tab": r.get(tcol, "") if tcol else "",
        **{c: r.get(c, "") for c in title_cols},
    } for r in rows]

    return JSONResponse({
        "total": len(d.rows), "count": len(out), "searched_total": searched_total,
        "tab_column": tcol, "tab_columns": tabs,
        "tabs": [{"value": v, "count": n}
                 for v, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))],
        "cases": out,
    })


@app.get("/api/case/{index}")
def api_case(index: int, dataset: str | None = None) -> JSONResponse:
    d = _get(dataset)
    if not 0 <= index < len(d.rows):
        raise HTTPException(404, f"case {index} out of range (0-{len(d.rows) - 1})")
    row = d.rows[index]
    highlight = d.highlight_columns()
    title = d.title_columns()
    shown = set(title) | set(highlight) | {d.summary_column}

    return JSONResponse({
        "index": index,
        "dataset": d.key,
        "doc": row.get(d.doc_column, ""),
        "has_pdf": row["_has_pdf"],
        "title": [{"name": c, "value": row.get(c, "")} for c in title],
        "summary_column": d.summary_column,
        "summary_text": row.get(d.summary_column, "") if d.summary_column else "",
        # The prevention design, rendered directly under the summary.
        "highlight": [{"name": c, "value": row.get(c, "")} for c in highlight],
        # Everything else, at the bottom.
        "fields": [{"name": c, "value": row.get(c, "")} for c in d.columns if c not in shown],
        "pdf_url": f"/pdf/{d.key}/{row.get(d.doc_column, '')}" if row["_has_pdf"] else None,
    })


@app.get("/pdf/{dataset}/{filename}")
def pdf(dataset: str, filename: str) -> FileResponse:
    d = _get(dataset)
    path = d.pdf_for(filename)
    if path is None:
        raise HTTPException(404, f"no such PDF in {dataset}: {filename}")
    return FileResponse(path, media_type="application/pdf",
                        headers={"Content-Disposition": f'inline; filename="{filename}"'})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--no-browser", action="store_true")
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
