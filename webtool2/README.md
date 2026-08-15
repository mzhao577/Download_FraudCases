# webtool2 — Case Review with the Prevention Design

Built to [`../instruction_APIAnalisys.md`](../instruction_APIAnalisys.md), reading the
[`designFeatures_v2`](../designFeatures_v2) output instead of the plain summary:
the raw PDF on the left, and on the right the case summary followed **immediately
by the four prevention columns**.

Runs alongside [`webtool/`](../webtool) (v1) — v1 owns port 8000, v2 owns 8001.

## Run it

```bash
python webtool2/setup_input.py --key DOJ_2025    # build the input folder (once)
python webtool2/app.py                           # → http://127.0.0.1:8001
```

| Flag | Effect |
|---|---|
| `--input-dir DIR` | where to look for datasets (default `./downloaded/webtool2`) |
| `--port N` | serve on another port (default `8001`) |
| `--no-browser` | do not open a browser |

## Input

```
downloaded/webtool2/
    DOJ_2025/                                     679 PDFs (symlinked)
    extractedSummary_2025_DOJ_withFeatures.csv    679 rows x 19 columns
```

Same token-matching rule as v1: every token of the folder name must appear in the
CSV name, in any order. When several CSVs match, the one with the most tokens
wins — so `..._withFeatures.csv` is preferred over the plain summary.

## Right panel order

| Position | Content |
|---|---|
| **Title** | `DocumentName`, with `FraudType` as a chip |
| **Top** | `SchemeSummary` |
| **Directly below** | **Prevention design** — `DesiredServiceGroups`, `WaysToIdentify`, `FeaturesToCreate`, `FeatureCategory`, on a tinted panel |
| **Bottom** | The remaining 12 columns |

The prevention block is **data-driven, not hard-coded**: any column positioned
*after* the summary column in the CSV is treated as a highlight column. Add a
fifth analysis column to the CSV and it appears there too, with no code change.
Short list-like values (service groups, category) render as pills; prose renders
as a block.

## Tabs

The tab strip is driven by a **selectable column** — `FeatureCategory` by
default, or `FraudType`, `Service`, `CaseStatus` from the *tabs by* dropdown.
Counts follow the current search but precede the tab filter, so a search
re-labels the tabs with how its hits split and selecting one tab does not blank
the others.

## Navigation

`⇤ First │ −50 │ −10 │ ← Previous │ Next → │ +10 │ +50 │ Last ⇥`, a go-to box and
a progress bar. Steps clamp rather than refuse.

| Key | Action |
|---|---|
| `j` / `k` | ±1 |
| `J` / `K` | ±10 |
| `shift`+`PageDown` / `PageUp` | ±50 |
| `Home` / `End` | first / last |
| `g` / `/` | go-to box / search |

## Layout

```
webtool2/
├── app.py            FastAPI server, JSON API, PDF serving
├── dataset.py        discovery, CSV/PDF join, highlight-column rule, path safety
├── setup_input.py    builds the input folder from designFeatures_v2 output
└── static/index.html the whole UI — no build step, no CDN
```

Binds to `127.0.0.1` only. PDFs are served only when the filename appears in the
dataset's CSV and the resolved path is inside the dataset folder; traversal
attempts return 404.
