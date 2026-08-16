# Download_FraudCases

Two pipelines:

1. **Download** (`instruction_download.md`) — find and download major medical /
   health care fraud cases and reports from U.S. federal sources since 1 Jan 2021.
2. **Extract patterns** (`instruction_extractInfo.md`) — turn a folder of case PDFs
   into a structured feature table plus an analysis of the recurring fraud schemes.
   See [Part 2](#part-2--extracting-case-features-and-fraud-patterns) below.
3. **Review cases** (`instruction_APIAnalisys.md`) — a two-panel web tool for reading
   cases one at a time. See [`webtool/`](webtool/) and [`webtool2/`](webtool2/);
   start both with [`./start_services.sh`](start_services.sh).
4. **Design monitoring features** (`instruction_designFeatures.md`) — turn the case
   corpus into ~10 computable provider-monitoring features. See
   [`designFeatures/monitoring_features.md`](designFeatures/monitoring_features.md).

---

## Part 1 — Downloading the cases

Python scripts that find and download **major medical / health care fraud cases and
reports** published by U.S. federal sources since **1 January 2021** — cases involving
Medicare, Medicaid, TRICARE and commercial/private payers.

Every document lands under `./downloaded/<Source>/<year>/`. Web pages are saved
**both as `.html` and as a `.pdf` rendering of that same saved page**, exactly as the
instructions ask. Documents that are already PDFs (report full texts, indictments,
settlement agreements) are saved as-is.

---

## 1. Sources

The list of websites used for the search lives in **[`sources.json`](sources.json)** —
it is the canonical, machine-readable registry the scrapers read at run time, and it
records for each source *why* it is used, *which* URLs are harvested and *how*.
A human-readable rendering of the same list is reproduced at the bottom of
[`SUMMARY.md`](SUMMARY.md) after a run.

| Key | Source | What is collected |
|---|---|---|
| `DOJ` | Department of Justice — Main Justice + all 93 U.S. Attorney's Offices | Health-care-fraud press releases: charges, convictions, sentencings, False Claims Act settlements, national takedowns |
| `HHS-OIG` | HHS Office of Inspector General | Enforcement-action database (criminal, civil, CMP, state MFCU cases), fraud/improper-payment audits and evaluations, LEIE exclusions data |
| `FBI` | FBI national office + 55 field offices | Health-care-fraud press releases and stories |
| `CMS` | Centers for Medicare & Medicaid Services | Program-integrity press releases, fact sheets and reports |
| `GAO` | Government Accountability Office | Reports and testimony on Medicare/Medicaid fraud risk, improper payments, program integrity |

`sources.json` also records the sources that were **considered but not scraped**
(NHCAA, individual state MFCU sites, PACER) and the reason for each.

## 2. Install

```bash
pip install -r requirements.txt
```

Also required: **Google Chrome** (used headless). Three of the five sites
(justice.gov, cms.gov, gao.gov) sit behind bot-management walls that refuse plain
HTTP clients, and Chrome is what turns saved HTML into PDF. Selenium downloads its
own driver automatically.

## 3. Run

```bash
python run_all.py                 # discover -> download -> summarize (several hours)
```

or step by step:

```bash
python list_sources.py            # render sources.json -> SOURCES.md
python discover.py                # build state/manifest.jsonl
python download.py --workers 4    # fill ./downloaded/
python verify.py                  # report any gaps in the corpus
python summarize.py               # write summary/ and SUMMARY.md
```

Useful flags:

| Flag | Effect |
|---|---|
| `--sources DOJ FBI` | restrict to certain sources (any step) |
| `--since 2023-01-01` | change the coverage cut-off (default `2021-01-01`) |
| `--limit N` | stop after N documents — smoke testing |
| `--workers N` | parallel downloaders, one headless Chrome each (default 4) |
| `--no-pdf` | save HTML only; roughly 3x faster |
| `--no-attachments` | do not follow links to exhibit/report PDFs; much less disk |
| `--force` | re-download documents already on disk |

Everything is **resumable**: rerunning skips files that already exist, listing pages
and API responses are cached under `state/cache/`, and a fresh run only picks up
what is new. Interrupting with Ctrl-C is safe.

## 4. Output layout

Organised **year first, then source** (`downloaded/2026/FBI/`):

```
downloaded/
  2024/DOJ/pharmacist-guilty-in-20-million-kickback-scheme_a1b2c3d4e5f6.html
  2024/DOJ/pharmacist-guilty-in-20-million-kickback-scheme_a1b2c3d4e5f6.pdf
  2024/DOJ/pharmacist-guilty-in-20-million-kickback-scheme_a1b2c3d4e5f6_attachments/
      indictment.pdf
  2023/HHS-OIG/...
  2022/FBI/...
  2021/CMS/...
  2025/GAO/...
  undated/...          program and index pages that carry no publication date
summary/
  summary.md      summary.csv      summary.json
SUMMARY.md        <- copy of summary/summary.md
state/
  manifest.jsonl        every document discovered, with metadata
  download_log.jsonl    per-document outcome (ok / skipped / partial / error)
  cache/                cached API responses and page HTML
logs/
```

The filename suffix is a short hash of the source URL, so titles can repeat across
offices without colliding. Each saved `.html` starts with a provenance comment
recording the source, original URL, publication date and retrieval timestamp, and
carries a `<base href>` so the local copy still renders.

## 5. Summary file

`summarize.py` writes the required counts — documents per **year** and per
**source** — to `summary/summary.md` (plus `.csv` and `.json`, and a copy at
`SUMMARY.md`). It reports the source × year matrix, the file-type breakdown
(HTML / PDF / data files / attachments), document categories, and the list of
websites searched.

## 6. How documents are identified as medical fraud

`fraudscrape/config.py` holds a four-tier matcher, deliberately built to avoid both
"every fraud case" and "every Medicare press release":

1. **Strong phrases** — `health care fraud`, `Medicare fraud`, `Medicaid Fraud Control Unit`, … — accepted on their own.
2. **Payer/program context** (`Medicare`, `Medicaid`, `TRICARE`, `health plan`, named commercial insurers) **and** any fraud term.
3. **Clinical/provider context** (hospice, home health, pharmacy, laboratory, DME, telehealth, …) **and** a *billing-style* fraud term (kickback, false claims, upcoding, medically unnecessary, …).
4. Generic prosecution verbs (indicted, convicted, sentenced, guilty, conspiracy) are excluded from the fraud axis — they appear in nearly every DOJ release.

For DOJ this runs *in addition to* the official `Healthcare Fraud` topic tag, which
catches only about half of the relevant releases on its own.

## 7. Layout of the code

```
sources.json               the website list (edit this to add/remove a source)
list_sources.py            step 0 - render sources.json -> listofWebsites.txt, SOURCES.md
migrate_layout.py          one-off - move an old <Source>/<year>/ corpus to <year>/<Source>/
discover.py                step 1 - build the manifest
download.py                step 2 - fetch HTML + PDF + attachments
verify.py                  optional - find documents missing their HTML or PDF
summarize.py               step 3 - counts per year and per source
run_all.py                 discover -> download -> summarize
fraudscrape/
  config.py                paths, coverage window, keyword matcher, source registry
  models.py                Doc record, slugs, date parsing, manifest I/O
  net.py                   requests session, retries, per-host rate limiting
  browser.py               headless-Chrome pool: page fetch, HTML->PDF, binary fetch
  pagefetch.py             cache -> HTTP -> Chrome, one way in for every page
  fetch.py                 save one document (HTML, PDF, attachments)
  summary.py               the summary report
  discovery/
    doj.py  hhs_oig.py  fbi.py  cms.py  gao.py
```

Adding a source means writing one `discover(since, limit=None) -> list[Doc]`
function, registering it in `fraudscrape/discovery/__init__.py`, and adding the
entry to `sources.json`.

## 8. Notes and limits

- All five sources are public U.S. government sites; requests are rate-limited per
  host and pages are cached so reruns do not re-fetch.
- justice.gov press-release pages are fetched with headless Chrome. If that is
  blocked for a given release, the page is rebuilt from the official justice.gov
  press-release API body — the saved HTML then says so in its footer.
- Commercial-payer material is covered indirectly: DOJ, FBI and HHS-OIG cases
  routinely include private-insurer victims, but NHCAA's own case library is
  members-only and is not scraped.
- A full run downloads several thousand documents and roughly 5–15 GB with
  attachments enabled. Use `--no-attachments` for a much smaller corpus.

---

# Part 2 — Extracting case features and fraud patterns

Implements `instruction_extractInfo.md`: read a folder of case PDFs (one case per
file), extract a structured record from each with Claude, and analyse the recurring
schemes — input for a model that predicts fraud against Medicare, Medicaid and
commercial payers.

```bash
./ExtractedAll_in1InputFolder.sh testdata_DOJ_2026   # -> ./extracted/testdata_DOJ_2026/
python extract_patterns.py                      # ./downloaded/testdata_DOJ_2026
python extract_patterns.py --input-dir DIR      # any folder of case PDFs
python extract_patterns.py --limit 3            # smoke test
python extract_patterns.py --effort high        # deeper reading per document
python extract_patterns.py --no-analysis        # fields only, skip the narrative
```

Requires `ANTHROPIC_API_KEY` (or an `ant auth login` profile). Uses `claude-opus-5`.

## Output — `./extracted/`

| File | Contents |
|---|---|
| `cases.csv` | One row per case, the fields below |
| `cases.json` | The same rows plus the computed counts |
| `patterns.md` | Counts, a case table, and the pattern analysis |
| `errors.json` | Written only if a document failed |

## Extracted fields

`DocumentName`, `ReportDT`, `JurisdictionName`, `OccurDt`, `FraudEntity`,
`Service`, `State_County`, `PayerName`, `FraudAmt`, `SettlementAmt`, `JailTime`,
`FraudType` — plus three additions: `FraudTypeAll`, `CaseStatus`, `SchemeSummary`.

Two notes on the brief's field list: `urisdictionName` is read as `JurisdictionName`
(dropped J), and `jailTime` is normalised to `JailTime`. `FraudTypeAll` exists because
a single case routinely combines two schemes (kickbacks *and* phantom claims) and one
label per case throws most of that signal away.

`FraudType` uses the **closed 18-type taxonomy** in `instruction_extractInfo.md`
§4. It is declared as an enum in the output schema, so a label outside the list
cannot be returned; anything that fits none of them is `Other - Unknown`. That file
is the source of truth — when the taxonomy changes there, update `FRAUD_TYPES` and
`FRAUD_TYPE_GUIDE` in `fraudextract/schema.py` to match.

## How it works

```
fraudextract/
  config.py     paths, model, effort, fallback model
  schema.py     the Pydantic record + fraud-type taxonomy
  pdftext.py    PDF -> text (PDFium), strips site chrome
  extract.py    one Claude call per document, structured outputs
  patterns.py   deterministic counts, then the narrative analysis, then the files
extract_patterns.py   the CLI
```

- **Structured outputs** (`messages.parse` with a Pydantic schema) guarantee every
  record validates — no JSON repair, no regex fallback.
- **Counting is done in code, not by the model.** Claude is asked only for the
  judgement layer: what the recurring schemes are and what they have in common.
- **Prompt caching** on the system prompt (taxonomy + rules), which is identical
  across documents. The first document runs alone so the rest read its cache.
- **PDF text is read on one thread.** PDFium is not thread-safe — reading inside the
  worker pool raises `Failed to load page` or kills the interpreter. Only the API
  calls are parallel.
- **Resumable**: each document's result is cached under `extracted/.cache/`; rerun to
  pick up where it left off, `--force` to re-extract.
- **Repeat coverage is detected**: charge, plea and sentencing are announced as
  separate press releases, so "one PDF = one case" overcounts. Documents sharing a
  lead defendant are grouped and a distinct-case count is reported alongside the
  document count.
- Refusals and API errors are handled per document — one bad document never fails
  the run, and `stop_reason` is checked before any content is read.

---

# Running the review tools — `start_services.sh`

Both web tools in one command, instead of two terminals and two `python3` lines.

```bash
./start_services.sh              # start both, print the links
./start_services.sh status       # what is running, and on which dataset
./start_services.sh stop         # stop both
./start_services.sh restart      # stop, then start (how you load a different CSV)
```

| | Port | Shows |
|---|---|---|
| `webtool`  | 8000 | `SchemeSummary` at the top, the other extracted fields below |
| `webtool2` | 8001 | the same, with the four **prevention-design** columns rendered directly under the summary |

Useful options:

```bash
./start_services.sh --only webtool2                 # just one of them
./start_services.sh --csv designFeatures_v2/extractedSummary_2025_DOJ_withFeatures.csv \
                    --pdf-dir downloaded/DOJ_2025   # point webtool at a summary file
./start_services.sh --port 9000 --port2 9001        # when 8000/8001 are taken
./start_services.sh --only webtool --foreground     # run in this terminal, ctrl-c to stop
```

`--csv` applies to **webtool** only — `webtool2` reads its input folder, prepared
by `python3 webtool2/setup_input.py --key DOJ_2025`. `--pdf-dir` is optional
whenever the PDF folder name can be worked out from the CSV name.

Starting is idempotent: a tool already answering on its port is left running, and
the script says so rather than starting a second copy. Each instance logs to
`logs/<tool>-<port>.log`; a tool that fails to start prints the tail of its log.

---

# Moving the corpus between machines

`downloaded/` (4.7 GB) and `state/` (1.5 GB) are gitignored, so a clone gets the
code but no documents. Ship them as **GitHub Release assets** — they live outside
git history, so the repo stays small.

```bash
./corpus_push.sh                 # this machine: archive, split, upload
./corpus_push.sh --dry-run       # build the parts, upload nothing
./corpus_push.sh --no-state      # ./downloaded only

# on the other laptop
git clone https://github.com/mzhao577/Download_FraudCases.git
cd Download_FraudCases
./corpus_pull.sh                 # newest snapshot; --list to choose, --tag to pin
python verify.py                 # confirm the corpus is complete
```

GitHub allows **2 GiB per asset, 1000 assets per release, no total-size or
bandwidth limit**, so the archive is streamed through `split` into 1900 MB parts.
Every part is SHA-256 checksummed; `corpus_pull.sh` verifies before unpacking and
refuses to continue on a mismatch. Assets on a private repo are private — `gh`
supplies the credentials, so a plain browser or `curl` download will not work.

**Alternatives:** if both laptops are on the same network, `rsync -avh --progress`
is faster and has no 2 GiB chunking. If you only need *a* corpus rather than
*this exact* corpus, skip the transfer and re-run `discover.py && download.py`.
