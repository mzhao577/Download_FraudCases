---
title: Fraud Case Review (webtool2)
emoji: 📄
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
pinned: false
short_description: Case PDFs beside the prevention design, 679 DOJ cases
---

# Fraud Case Review — webtool2

The local `webtool2` tool, hosted: the source PDF on the left, and on the right
the case summary followed immediately by the prevention design from
`designFeatures_v2`.

This is the **same UI as the local tool** — `index.html` is copied verbatim from
`webtool2/static/index.html`, so the layout, the tab strip, the navigation and
the keyboard shortcuts all behave exactly as they do on `127.0.0.1:8001`.

| Key | Action |
|---|---|
| `j` / `k` | ±1 case |
| `J` / `K` | ±10 |
| `shift`+`PageDown` / `PageUp` | ±50 |
| `Home` / `End` | first / last |
| `g` / `/` | go-to box / search |

## What replaces the server

The local tool is a FastAPI app serving four endpoints. Hugging Face retired
the server-side Streamlit SDK and its Docker replacement needs a paid plan, so
this is a **static Space**: `static-api.js` intercepts `fetch()` and answers
those same four endpoints from the CSV in the browser.

| Endpoint | Served by |
|---|---|
| `/api/datasets` | `static-api.js`, from the CSV header |
| `/api/cases?q&tab_column&tab_value` | `static-api.js` — search, tab counts, filter |
| `/api/case/{index}` | `static-api.js` — title / summary / prevention / fields |
| `pdf/<DocumentName>` | plain static files, listed in `pdf/manifest.json` |

The response shapes match `webtool2/app.py`, including the rule that tab counts
are taken **after** the search but **before** the tab filter, so picking one tab
does not blank the others.

Everything runs in the browser. No server, no API key, nothing uploaded.

## Contents

```
index.html          the webtool2 UI, with one <script> tag added
static-api.js       the four endpoints, answered client-side
build.py            rebuilds this folder from the live tool
data/               extractedSummary_2025_DOJ_withFeatures.csv, 679 x 19
pdf/                679 DOJ press-release PDFs + manifest.json
```

Rebuild after a change to the local tool or the CSV:

```bash
python webtool2/setup_input.py --key DOJ_2025   # refresh the input folder
python hfspace_webtool2/build.py --pdfs         # re-assemble this folder
```

## Caveats

The PDFs are public DOJ press releases. The prevention designs are
model-generated reconstructions of what *would* have been visible in claims
data — none has been tested against real claim lines, and every threshold needs
calibration against a control population before use.
