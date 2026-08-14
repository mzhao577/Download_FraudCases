# Case Review Web Tool — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (part 3 of 3) |
| **Status** | Final — consolidates the original brief and the tool as built |
| **Last updated** | 2026-08-14 |
| **Implementation** | [`webtool/`](webtool/) |
| **Earlier drafts** | `instruction_APIAnalisys_v0.txt` |
| **Related** | [`instruction_download.txt`](instruction_download.txt) (part 1) · [`instruction_extractInfo.md`](instruction_extractInfo.md) (part 2) |

---

## 1. Goal

Build a web tool for looking at reported fraud cases **one at a time**, to find
insight into how fraud can be identified. Reading a case means holding two things
side by side — the source document and the extracted summary — so the tool puts
them in two panels and makes moving between cases fast.

This is part 3 of a chain: part 1 downloads the case documents, part 2 extracts a
structured summary from each, and this tool reads the result.

---

## 2. Input

### 2.1 Folder layout

One input folder holding a subfolder of PDFs and a matching summary CSV:

```
downloaded/webtools/
├── DOJ_2025/                          # raw PDFs, one per case
│   ├── 11-defendants-indicted-…_ec7a233deffb.pdf
│   └── …
└── extractedSummary_2025_DOJ.csv      # one row per PDF
```

### 2.2 Name matching

The subfolder and the CSV must refer to the same dataset. The shared part in the
example above is `DOJ_2025`, but the CSV spells it `2025_DOJ` — so matching is on
**tokens, in any order**, not on the literal string:

> Every token of the folder name must appear somewhere in the CSV name.

| Folder | CSV | Match |
|---|---|---|
| `DOJ_2025/` | `extractedSummary_2025_DOJ.csv` | ✅ |
| `DOJ_2025/` | `DOJ_2025_summary.csv` | ✅ |
| `DOJ_2025/` | `extractedSummary_2026_DOJ.csv` | ❌ |

### 2.3 Row-to-file join

Each PDF corresponds to one CSV row. The **`DocumentName`** column carries the
filename inside the subfolder. Column lookups are case-insensitive.

### 2.4 Multiple datasets

More than one pair may live in the same input folder; each is discovered
independently and a picker appears in the toolbar. With a single dataset the
picker is hidden.

---

## 3. Display

### 3.1 Two panels

| Panel | Content |
|---|---|
| **Left** | The raw document, in a format that is easy to scroll and search |
| **Right** | The summary of that case |

The left panel embeds the PDF in the browser's own viewer, so scrolling, zoom,
page thumbnails and in-document `Ctrl-F` search come for free.

### 3.2 Right panel

| Position | Content |
|---|---|
| **Title** | `DocumentName`, with `FraudType` beside it as a chip |
| **Top** | `SchemeSummary` — set large, the text you actually read |
| **Bottom** | Every remaining summary column, in a table |

Dollar columns are formatted with thousands separators; empty values show as `—`
rather than blank.

### 3.3 FraudType tabs

One tab per value of the `FraudType` column, **ordered most common first**, each
with a count:

```
All 679 │ Phantom Claims 134 │ kickback_Bribery For Referral 105 │ Drug_Prescriptions 90 │ …
```

Clicking a tab filters the case list; **All** clears the filter. Counts are
computed **after the search filter but before the type filter**, which has two
consequences worth stating:

- a search re-labels the tabs with how its hits split across schemes, so the
  strip doubles as a distribution readout;
- selecting one tab does not zero out the other tabs' counts.

### 3.4 Navigation

```
⇤ First │ −50 │ −10 │ ← Previous │ Next → │ +10 │ +50 │ Last ⇥     310 / 679   [go to #]
```

- Steps **clamp rather than refuse**: `+50` with 12 cases left lands on the last
  case instead of doing nothing.
- Buttons disable at the ends; a progress bar tracks position.
- The `go to #` box jumps to a case number.
- Navigation respects the active filters — stepping through a filtered list stays
  inside it.

| Key | Action |
|---|---|
| `j` / `→` / `↓` | next case |
| `k` / `←` / `↑` | previous case |
| `J` / `K` | ±10 |
| `shift`+`PageDown` / `PageUp` | ±50 |
| `Home` / `End` | first / last |
| `g` | focus the go-to box |
| `/` | focus the search box |
| `Esc` | leave a text box |

> `J` is literally `shift`+`j`, so a browser cannot distinguish them. ±50 is on
> `shift`+`PageDown`/`PageUp` and on the buttons instead.

### 3.5 Search

Scans **every column of every row**, including `SchemeSummary`, and highlights
matches in both the case list and the right panel. Case-insensitive substring, so
partial words match. Composes with the FraudType tabs.

### 3.6 Case list

A scrollable list of the filtered cases showing filename and fraud type, with the
current case highlighted. Toggled with the **☰ Cases** button so the two panels
can have the full width.

---

## 4. Running it

```bash
python webtool/setup_input.py --key DOJ_2025    # build the input folder (once)
python webtool/app.py                           # → http://127.0.0.1:8000
```

`app.py` prints the URL and opens a browser.

| Flag | Effect |
|---|---|
| `--input-dir DIR` | where to look for datasets (default `./downloaded/webtools`) |
| `--port N` | serve on another port (default `8000`) |
| `--host H` | bind address (default `127.0.0.1`) |
| `--no-browser` | do not open a browser |

`setup_input.py` builds the input folder from an existing corpus and extraction
run, **symlinking** the PDF folder so pointing at a 226 MB corpus costs no disk.
Use `--copy` for a standalone folder that can be moved elsewhere.

| Flag | Effect |
|---|---|
| `--key KEY` | dataset key, e.g. `DOJ_2025` |
| `--pdf-dir DIR` | source PDFs (default `./downloaded/<key>`) |
| `--csv FILE` | source summary CSV (default `./extracted/<key>/cases.csv`) |
| `--copy` | copy the PDFs instead of symlinking |

---

## 5. Implementation

```
webtool/
├── app.py            FastAPI server, JSON API, PDF serving
├── dataset.py        dataset discovery, CSV/PDF join, path safety
├── setup_input.py    builds the input folder from an existing corpus
├── static/
│   └── index.html    the entire UI — no build step, no CDN, no framework
└── README.md
```

### 5.1 HTTP API

| Endpoint | Returns |
|---|---|
| `GET /` | the UI |
| `GET /api/datasets` | datasets found, with row/PDF counts and column names |
| `GET /api/cases?dataset=&q=&fraud_type=` | filtered case list plus tab counts |
| `GET /api/case/{index}?dataset=` | one row, split into title / summary / fields |
| `GET /pdf/{dataset}/{filename}` | the PDF, served inline |

### 5.2 Requirements

`fastapi`, `uvicorn` — both in [`requirements.txt`](requirements.txt). The CSV is
read once at startup; restart to pick up a re-run of the extractor.

### 5.3 Security

The tool binds to `127.0.0.1` and is not exposed off the machine. PDFs are served
only when the filename appears in that dataset's CSV, and the resolved path is
checked to fall inside the dataset folder. Traversal attempts — `../`,
percent-encoded, unknown dataset, unknown file — return `404`.

### 5.4 Missing data

Rows whose PDF is absent are **kept and flagged**, not hidden: marked in the case
list and shown with a banner in the right panel. Startup reports any mismatch in
both directions (rows without a PDF, PDFs without a row).

---

## 6. Verification

Against `downloaded/webtools/DOJ_2025`:

| Check | Result |
|---|---|
| Row ↔ PDF join | **679 rows, 679 PDFs, 679 matched**, 0 orphans either way |
| Endpoints | all return correct payloads |
| Path traversal (`../`, percent-encoded, unknown dataset/file) | all `404` |
| Navigation | every button lands on the expected case; clamping holds at both ends; correct buttons disable at the edges |
| Go-to box and keyboard | land on the right case |
| FraudType tabs | 18 tabs; `Upcoding` filters 679 → 33 with list, position and right panel following |
| Search + tab composition | counts and list agree |
| Panels | PDF renders left; title, summary and fields render right |

---

## 7. Notes and limitations

- **The tool is a reader, not an analyser.** It presents cases; the judgement is
  the reader's.
- **The summary is only as good as the extraction.** Fields come from part 2 and
  carry its limitations — charged cases are allegations, and `CaseStatus` is what
  distinguishes them from findings.
- **Repeat coverage exists.** A case is often announced more than once (charge,
  plea, sentencing), so consecutive entries may describe the same matter.
- **Startup cost is linear in rows.** The CSV is held in memory; fine for
  thousands of rows, not built for millions.
