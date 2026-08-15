# Medical Fraud Case Download — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (part 1 of 4) |
| **Status** | Final — consolidates the original brief and every instruction given during the build |
| **Last updated** | 2026-08-14 |
| **Implementation** | [`fraudscrape/`](fraudscrape/), [`discover.py`](discover.py), [`download.py`](download.py), [`summarize.py`](summarize.py) |
| **Earlier drafts** | `instruction_download_v0.txt` |
| **Related** | [`instruction_extractInfo.md`](instruction_extractInfo.md) (2) · [`instruction_APIAnalisys.md`](instruction_APIAnalisys.md) (3) · [`instruction_designFeatures.md`](instruction_designFeatures.md) (4) |

---

## 1. Goal

Write Python scripts that find and download **all major medical fraud cases** and
related reports. Cases may involve Medicare, Medicaid or commercial/private
payers. Sources are federal agencies: FBI, CMS, HHS-OIG (including LEIE), DOJ and
GAO.

> **Terminology.** "IELE" in the original brief is read as **LEIE** — the HHS-OIG
> List of Excluded Individuals and Entities.

---

## 2. Coverage

- Download the reports and documents of **the last 5 years** — anything dated
  **1 January 2021 or later**.
- Documents dated before `2021-01-01` are excluded. Program and index pages that
  carry no publication date are kept and filed under `undated`.
- The cut-off is a **parameter, not a constant** (`--since`), so the window can be
  moved later.

---

## 3. Sources

### 3.1 Find the sources first

Identify the major sources **before** downloading anything.

### 3.2 Save the list of websites used

Two artefacts are required:

| File | Role |
|---|---|
| [`sources.json`](sources.json) | Machine-readable registry the scrapers read at run time. Per source: key, name, why it is used, the websites, how it is harvested, the exact endpoints requested, and the document types expected. |
| [`listofWebsites.txt`](listofWebsites.txt) | Plain-text list for reading, generated from `sources.json` by `list_sources.py`. |

A Markdown rendering ([`SOURCES.md`](SOURCES.md)) comes from the same registry.

### 3.3 Record what was rejected

Sources considered and **not** used are recorded with the reason for each
(members-only, paywalled, already syndicated elsewhere).

### 3.4 Sources used

| Key | Source | What is collected |
|---|---|---|
| `DOJ` | Department of Justice — Main Justice and all 93 U.S. Attorney's Offices | Health-care-fraud press releases: charges, convictions, sentencings, False Claims Act settlements, national takedowns |
| `HHS-OIG` | HHS Office of Inspector General | Enforcement-action database (criminal, civil, CMP, state Medicaid Fraud Control Unit cases), fraud and improper-payment audits and evaluations, LEIE exclusions data |
| `FBI` | FBI national office and 55 field offices | Health-care-fraud press releases and stories |
| `CMS` | Centers for Medicare & Medicaid Services | Program-integrity press releases, fact sheets and reports |
| `GAO` | Government Accountability Office | Reports and testimony on Medicare/Medicaid fraud risk, improper payments, program integrity |

---

## 4. Output layout

### 4.1 Year first, then source

```
downloaded/<year>/<Source>/<slug>_<hash>.html
downloaded/<year>/<Source>/<slug>_<hash>.pdf
downloaded/<year>/<Source>/<slug>_<hash>_attachments/*.pdf
```

For example `downloaded/2026/FBI/`, `downloaded/2021/DOJ/`.

`<Source>` is the agency the document was **found on** — `DOJ`, `HHS-OIG`, `FBI`,
`CMS` or `GAO`. `<hash>` is a short hash of the source URL, so identical titles
from different offices cannot collide.

> This supersedes the earlier `downloaded/<Source>/<year>/` arrangement.

### 4.2 HTML plus a PDF of that HTML

If the report is in web/HTML format, save it as HTML **and at the same time** save
a PDF of that HTML file. The PDF must be a rendering of the **saved page**, not a
separately downloaded file.

### 4.3 Native formats kept as-is

Documents that are already PDF/CSV/ZIP — full-text reports, indictments,
settlement agreements, the LEIE database — are saved unchanged.

### 4.4 Attachments

Exhibits linked from a page (indictments, complaints, settlement agreements,
full-text report PDFs) are downloaded into a `<document>_attachments/` folder
beside the page.

### 4.5 Provenance

Each saved `.html` begins with a comment recording the source, original URL,
resolved URL if it redirected, title, publication date, category and retrieval
timestamp — and carries a `<base href>` so the local copy still renders.

---

## 5. Summary file

Create a summary listing the number of downloaded documents **from each year and
each source**.

Produced as `summary/summary.md`, `summary/summary.csv` and
`summary/summary.json`, with a copy of the Markdown at [`SUMMARY.md`](SUMMARY.md).

It contains:

- a **year × source matrix** of document counts, with row and column totals;
- a file-type breakdown (HTML, PDF, other data files, attachments, size);
- document categories per source;
- the list of websites searched.

---

## 6. How to run the work

### 6.1 Test before the full run

Do a small test run that actually downloads documents from **every** source, and
inspect the results, before launching the full multi-hour run.

> In practice this caught two real defects: CMS publication dates were being read
> from the page's related-items rail instead of the article itself, and DOJ
> publishes each release under two URLs (`/opa/pr/…` and `/usao-xx/pr/…`) which
> had to be deduplicated.

### 6.2 Download year by year, newest first

Not one undifferentiated pass. One year at a time starting with the most recent,
refreshing the summary after each so the corpus is usable at every stage:

```bash
./run_by_year.sh 2026 2025 2024 2023 2022 2021
```

### 6.3 Log during the run

- every stage writes a timestamped log to `logs/`;
- discovery logs each source, each listing-page batch, and how many documents
  were kept;
- the downloader logs progress every 25 documents with a running
  ok / skipped / partial / error tally;
- `summarize.py` runs after each year, so `SUMMARY.md` is refreshed throughout
  rather than only at the end;
- `state/manifest.jsonl` and `state/download_log.jsonl` record, per document,
  what was found and what happened to it.

### 6.4 Show results early

The discovery manifest is written **incrementally** — after each source
completes, not only at the very end — so downloading can start on what has
already been found.

### 6.5 Report honestly

Report progress honestly while long jobs run, including what has not yet started.

---

## 7. Technical requirements

### 7.1 Pipeline stages, each runnable alone

| Script | Does |
|---|---|
| `list_sources.py` | render `sources.json` → `listofWebsites.txt`, `SOURCES.md` |
| `discover.py` | find documents → `state/manifest.jsonl` |
| `download.py` | fetch HTML/PDF → `downloaded/` |
| `verify.py` | report gaps in the corpus |
| `summarize.py` | counts per year and per source |
| `run_all.py` | discover → download → summarize |
| `run_by_year.sh` | download one year at a time, newest first |

### 7.2 Resumable

Rerunning skips whatever is already complete on disk and retries only the gaps.
`Ctrl-C` is safe. Listing pages, API responses and fetched page HTML are cached
under `state/`.

### 7.3 Polite

Per-host rate limiting, retries with backoff, and a real User-Agent. **The same
throttle applies** whether a page is fetched over plain HTTP or through the
browser.

### 7.4 Bot walls

`justice.gov`, `cms.gov` and `gao.gov` refuse plain HTTP clients, so those are
fetched with headless Chrome (Selenium). Chrome also renders saved HTML to PDF
and pulls binaries from those hosts. If a DOJ page cannot be fetched at all, the
release is rebuilt from the official justice.gov press-release API body — and the
saved file says so in its footer.

### 7.5 Relevance matching

A four-tier keyword matcher decides what counts as a medical fraud document,
deliberately avoiding both *"every fraud case"* and *"every Medicare press
release"*:

| Tier | Rule |
|---|---|
| 1 | **Strong phrases** — `health care fraud`, `Medicare fraud`, `Medicaid Fraud Control Unit`, … — accepted on their own |
| 2 | **Payer/program context** (Medicare, Medicaid, TRICARE, health plan, named commercial insurers) **and** any fraud term |
| 3 | **Clinical/provider context** (hospice, home health, pharmacy, laboratory, DME, telehealth, …) **and** a billing-style fraud term |
| 4 | **Generic prosecution verbs** (indicted, convicted, sentenced, guilty, conspiracy) are **excluded** from the fraud axis — they appear in nearly every press release |

For DOJ this runs *in addition to* the official `Healthcare Fraud` topic tag,
which on its own catches only about half the relevant releases.

### 7.6 Deduplicate

Collapse the same release published under more than one URL, keyed on
source + date + title.

### 7.7 Adding a source

Write one `discover(since, limit=None)` function, register it in
`fraudscrape/discovery/__init__.py`, and add the entry to `sources.json`. Nothing
else.

### 7.8 Dependencies

`requests`, `beautifulsoup4`, `selenium`, and Google Chrome.

---

## 8. Deliverables

| Path | Contents |
|---|---|
| `listofWebsites.txt` | List of websites used for the search |
| `sources.json` | Machine-readable source registry |
| `SOURCES.md` | Markdown rendering of the registry |
| `SUMMARY.md`, `summary/summary.{md,csv,json}` | Counts per year and per source |
| `downloaded/<year>/<Source>/` | The corpus — HTML + PDF + attachments |
| `state/manifest.jsonl` | Every document discovered, with metadata |
| `state/download_log.jsonl` | Per-document outcome |
| `logs/` | Run logs for discovery and each year |
| `README.md` | How to install, run and extend |
| `fraudscrape/` | The package |
| `discover.py`, `download.py`, `verify.py`, `summarize.py`, `run_all.py`, `list_sources.py`, `run_by_year.sh` | Entry points |

---

## 9. Acceptance — result of the full run (2026-08-13)

**9,741 documents, 0 gaps, 4.3 GB** — 9,740 HTML + 9,740 PDF + 2,237 attachments
+ the LEIE database (CSV).

| Year | HHS-OIG | DOJ | FBI | CMS | GAO | **Total** |
|---|---:|---:|---:|---:|---:|---:|
| 2021 | 869 | 805 | 24 | 1 | – | **1,699** |
| 2022 | 845 | 834 | 37 | – | – | **1,716** |
| 2023 | 929 | 807 | 38 | 1 | – | **1,775** |
| 2024 | 914 | 810 | 43 | 1 | – | **1,768** |
| 2025 | 983 | 679 | 45 | 1 | 3 | **1,711** |
| 2026 | 530 | 463 | 44 | 5 | 9 | **1,051** |
| undated | 7 | 3 | 4 | 5 | 2 | **21** |
| **Total** | **5,077** | **4,401** | **235** | **14** | **14** | **9,741** |

2026 is lower because it is year-to-date (through August).

### Known limitations

- **112 DOJ releases (2.5%)** were rebuilt from the justice.gov API because the
  live page was unreachable. The text is complete; the styling is a clean
  template. Each such file says so in its footer.
- Some **FBI URLs redirect to justice.gov**, so part of the FBI set duplicates DOJ
  content. Those are filed under FBI because that is where they were found (§4.1).
- **CMS and GAO are small by nature** — CMS publishes few fraud press releases and
  GAO's contribution is context reports rather than cases. The case volume is in
  DOJ and HHS-OIG.
- **NHCAA** commercial-payer case material is members-only and was not scraped.
  Commercial-payer cases are covered indirectly, through DOJ, FBI and HHS-OIG
  prosecutions of schemes against private insurers.

---

## 10. To refresh later

```bash
python3 discover.py     # picks up anything published since the last run
python3 download.py     # fetches only what is missing
python3 summarize.py
```

```bash
./run_by_year.sh 2026   # a single year
python3 run_all.py      # everything from scratch
```
