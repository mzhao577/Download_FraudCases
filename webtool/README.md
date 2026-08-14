# Case Review Web Tool

A two-panel reader for going through reported fraud cases one at a time: the raw
source document on the left, its extracted summary on the right. Built to support
the workflow in `instruction_APIAnalisys.txt` — read enough real cases to spot the
recurring mechanics, then turn each mechanic into a concrete claims check.

## Run it

```bash
python webtool/setup_input.py --key DOJ_2025    # build the input folder (once)
python webtool/app.py                           # http://127.0.0.1:8000
```

Options:

| Flag | Effect |
|---|---|
| `--input-dir DIR` | where to look for datasets (default `./downloaded/webtools`) |
| `--port N` | serve on another port (default 8000) |
| `--no-browser` | don't open a browser automatically |

Binds to `127.0.0.1` only — nothing is exposed off the machine.

## Input layout

```
downloaded/webtools/
    DOJ_2025/                          raw case PDFs, one per case
    extractedSummary_2025_DOJ.csv      one row per PDF
```

The folder and the CSV must refer to the same dataset. Matching is on **tokens,
not the literal string**: every token of the folder name (`DOJ`, `2025`) has to
appear somewhere in the CSV name, in any order. So `DOJ_2025/` pairs with
`extractedSummary_2025_DOJ.csv`, and it would also pair with
`DOJ_2025_summary.csv`.

Rows are joined to PDFs through the **`DocumentName`** column, which holds the
filename inside the subfolder.

Drop several datasets in the same input folder and a picker appears in the
toolbar.

`setup_input.py` **symlinks** the PDF folder rather than copying it, so pointing
the tool at a 226 MB corpus costs nothing. Use `--copy` for a standalone folder
you can move elsewhere.

## What's on screen

**Left panel** — the PDF, in the browser's own viewer: scrolling, zoom,
thumbnails and Ctrl-F search inside the document come free.

**Right panel**
- **Title**: `DocumentName`, with `FraudType` as a chip beside it
- **Top**: `SchemeSummary`, set large and readable — the thing you actually read
- **Bottom**: every remaining column, dollar amounts formatted

**Toolbar** — search, fraud-type filter, case counter, prev/next.

| Key | Action |
|---|---|
| `j` / `→` / `↓` | next case |
| `k` / `←` / `↑` | previous case |
| `/` | jump to the search box |
| `Esc` | leave the search box |

The case list on the far left toggles with the **☰ Cases** button, so you can
have the two panels alone when reading.

## Search is the point

The search box scans **every column of every row**, including `SchemeSummary`,
and highlights hits. That is what turns a pile of cases into a hypothesis:

- `upcod` → 80 cases in DOJ 2025, of which 33 are classified `Upcoding`
- `hospice`, `overtime`, `unlicensed`, `hours` → the over-capacity pattern
- a CPT code such as `99215` → cases naming a specific procedure

Read the hits, find the shared mechanic, and write the check. The
fraud-type filter narrows the same way when you want one scheme at a time.

## Layout

```
webtool/
  app.py            FastAPI server + JSON API
  dataset.py        dataset discovery, CSV/PDF join, path safety
  setup_input.py    builds the input folder from an existing corpus
  static/
    index.html      the whole UI (no build step, no CDN)
```

### API

| Endpoint | Returns |
|---|---|
| `GET /api/datasets` | datasets found, with row/PDF counts and column names |
| `GET /api/cases?q=&fraud_type=&dataset=` | filtered case list for the navigator |
| `GET /api/case/{index}?dataset=` | one full row, split into title / summary / fields |
| `GET /pdf/{dataset}/{filename}` | the PDF, served inline |

PDFs are served only when the filename appears in that dataset's CSV, and the
resolved path is checked to be inside the dataset folder — traversal attempts
(`../`, percent-encoded) return 404.

## Notes

- The tool reads the CSV at startup. Re-run the extractor and restart to pick up
  changes.
- Rows whose PDF is missing still appear, flagged in the list and with a banner
  on the right, rather than being hidden.
- Requires `fastapi` and `uvicorn` (already in `requirements.txt`).
