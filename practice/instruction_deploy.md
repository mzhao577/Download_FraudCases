# Hosting the Case Review Tool — Specification

| | |
|---|---|
| **Project** | Download_FraudCases (deployment layer for parts 3–4) |
| **Status** | Final — consolidates the original brief and the instructions given during the work |
| **Last updated** | 2026-08-17 |
| **Implementation** | [`hfspace_webtool2/`](hfspace_webtool2/) (current) · [`hfspace/`](hfspace/) (Streamlit port, superseded) |
| **Earlier drafts** | `instruction_deploy_v0.txt` |
| **Related** | [`instruction_APIAnalisys.md`](instruction_APIAnalisys.md) (the tool being hosted) · [`instruction_designFeatures_v2.md`](instruction_designFeatures_v2.md) (the data it shows) |

---

## 1. Goal

The original brief, verbatim from `instruction_deploy_v0.txt`:

> Please deploy the web tool to huggingface, using streamlit.

---

## 2. Instructions as given

The brief was one line; the target was settled by the instructions that followed.
Recorded in order, because each one changed the deliverable.

| # | Instruction | Effect |
|---|---|---|
| 1 | "Please deploy the web tool to huggingface, using streamlit." | The original brief. |
| 2 | *Which tool* → **webtool2** | Deploy the prevention-design tool, not the v1 summary tool. Its CSV is a superset of v1's. |
| 3 | *Visibility* → **private** | Initial choice, later reversed (see #6). |
| 4 | *PDFs* → **CSV only** | Initial choice, later reversed (see #7). |
| 5 | *Deploy path* → **static Space via stlite** | Chosen after Hugging Face refused a Streamlit Space and a Docker Space (§4). Keeps the free tier. |
| 6 | "Is the link alive now? Why could I not open it even though I have logged in." → **make it public** | A private Space renders as *not found* to anyone the session does not recognise, which is indistinguishable from a dead link. Public is the requirement. |
| 7 | "I would like to deploy the webtool 2, **just like the this link: http://127.0.0.1:8001/**" | **The governing requirement.** Parity with the local tool: PDF pane, tab strip, navigation, keyboard shortcuts. Reverses #4 — the PDFs ship. |
| 8 | "write instruction_deploy_v0.txt as well as the intermediate instruction … into instruction_deploy.md" | This file. |

---

## 3. Consolidated requirement

Host `webtool2` so that a visitor with the URL sees **what `127.0.0.1:8001`
shows**, with no login and no local setup.

| Requirement | Detail |
|---|---|
| **Same UI** | Layout, CSS, tab strip, navigation and keyboard shortcuts identical to the local tool — not a re-implementation |
| **PDF pane** | The source document renders on the left, as it does locally |
| **Prevention design** | Under the summary, data-driven: any column after `SchemeSummary` is a highlight column |
| **Public** | Opens for anyone with the URL |
| **Free tier** | No paid Hugging Face plan |
| **Current data** | The 679-row `_withFeatures.csv` from `designFeatures_v2`, not a stale copy |

---

## 4. Platform constraints found at deploy time

These are the reasons the implementation is not a Streamlit Space. Verify before
assuming any of it has changed.

| Constraint | Evidence |
|---|---|
| **Hugging Face retired the Streamlit SDK.** | `create_repo(space_sdk="streamlit")` → `400 Invalid option: expected one of "gradio"｜"docker"｜"static"` |
| **Docker and Gradio Spaces need PRO.** | `create_repo(space_sdk="docker")` → `402 Payment Required` — "hosting Gradio and Docker Spaces on free cpu-basic requires a PRO subscription" |
| **Static Spaces are free.** | Both Spaces below run on `sdk: static` |
| **So: no server.** | Anything server-side — FastAPI, a Streamlit runtime — has to move into the browser |
| **`short_description` ≤ 60 chars** | Longer fails README YAML validation on upload |
| **LFS files 302 to a CDN** | `curl` needs `-L`; browsers follow it automatically. Verified: `200 application/pdf`, byte-identical |

---

## 5. What was built

### 5.1 Current — `hfspace_webtool2/`, webtool2 at parity

**https://huggingface.co/spaces/mzhao577/fraud-case-review-webtool2** — public, `sdk: static`

```
index.html          webtool2/static/index.html, copied, plus one <script> tag
static-api.js       the four endpoints, answered in the browser
build.py            re-assembles this folder from the live tool
README.md           Space card (YAML frontmatter)
data/               extractedSummary_2025_DOJ_withFeatures.csv, 679 × 19
pdf/                679 DOJ PDFs (228 MB, LFS) + manifest.json
```

The UI is **copied, never hand-edited** — that is what keeps parity. Only the
data layer is replaced: `static-api.js` intercepts `fetch()` and serves the same
four endpoints `webtool2/app.py` serves, with the same JSON shapes.

| Endpoint | Served by |
|---|---|
| `/api/datasets` | `static-api.js`, from the CSV header |
| `/api/cases?q&tab_column&tab_value` | `static-api.js` — search, tab counts, filter |
| `/api/case/{index}` | `static-api.js` — title / summary / highlight / fields |
| `pdf/<DocumentName>` | plain static files, listed in `pdf/manifest.json` |

Two rules must be preserved when touching the shim:

- **Tab counts are taken after the search but before the tab filter**, so picking
  one tab does not blank the others (matches `app.py`).
- **Highlight columns are positional** — everything after `SchemeSummary` — so a
  fifth analysis column appears with no code change.

A static host cannot stat a folder, so `has_pdf` comes from `pdf/manifest.json`,
written by `build.py`. With no manifest the shim assumes every row has its PDF.

### 5.2 Superseded — `hfspace/`, the Streamlit port

**https://huggingface.co/spaces/mzhao577/fraud-case-review** — public, `sdk: static`

Answers the brief's "using streamlit" literally: the same `app.py` is real
Streamlit, run in the browser by [stlite](https://github.com/whitphx/stlite)
(Streamlit on Pyodide/WebAssembly), pinned to `@stlite/browser@1.8.1`, which
bundles Streamlit 1.57. It also runs unchanged under `streamlit run app.py`, and
carries a `Dockerfile` for a server-side Space on a PRO account.

It has **no PDF pane** and **no keyboard shortcuts** (Streamlit cannot bind
them), which is why instruction #7 replaced it. Keep it only as the Streamlit
answer to the original brief; delete it if that no longer matters.

---

## 6. Rework

### 6.1 Rebuild after the data or the tool changes

```bash
python webtool2/setup_input.py --key DOJ_2025    # refresh downloaded/webtool2 from designFeatures_v2
python hfspace_webtool2/build.py --pdfs          # re-assemble; --limit N for a smoke build
```

`build.py` re-copies `index.html` from `webtool2/static/`, so a change to the
local tool reaches the Space by rerunning it. It refuses to run if `index.html`
already references `static-api.js`, which would mean it was pointed at its own
output.

### 6.2 Test locally before pushing

```bash
cd hfspace_webtool2 && python3 -m http.server 8700
# then open http://127.0.0.1:8700/index.html
```

### 6.3 Redeploy

```python
from huggingface_hub import upload_folder
upload_folder(repo_id="mzhao577/fraud-case-review-webtool2", repo_type="space",
              folder_path="hfspace_webtool2",
              allow_patterns=["README.md", "index.html", "static-api.js", "build.py",
                              "data/*.csv", "pdf/*.pdf", "pdf/manifest.json"],
              commit_message="…")
```

Creating from scratch: `create_repo(..., repo_type="space", space_sdk="static", private=True)`,
then `update_repo_settings(..., private=False)` once verified. Needs a write token
(`hf auth whoami` to check). 228 MB takes a few minutes; `upload_large_folder`
is the alternative if it starts failing.

---

## 7. Verification standard

HTTP 200 is not evidence the tool works — a static host returns 200 for a page
whose JavaScript then fails. **Drive the deployed URL in a real browser, logged
out**, and check the things the user actually uses. Results at deployment:

| Check | Result |
|---|---|
| Anonymous load of the Space and the static host | both `200` |
| Case count and list | 679 cases, 679 list rows |
| PDF pane | iframe wired to `pdf/<name>`; PDF serves `200 application/pdf`, byte-identical to source |
| Tab strip | current categories with counts — `Order Without Treating Encounter 63`, `No Claims System Nexus 53`, … |
| Keyboard | `j` moves `1 / 679` → `2 / 679` |
| Search | `hospice` → `25 of 679`, matches highlighted in list and panel |
| Prevention panel | renders, pills for list-like values |
| Console | no errors |

---

## 8. Notes and gotchas

- **A private Space looks like a dead link.** Hugging Face serves *not found*,
  not *not authorised*, to a session it does not recognise. If the link "doesn't
  work", check visibility and which account the browser is signed into before
  debugging the app.
- **`*.static.hf.space` is not the link to share.** It has no login flow of its
  own. Share the `huggingface.co/spaces/…` URL.
- **`downloaded/webtool2/` can go stale.** It holds a *copy* of the CSV, not a
  symlink. The first build shipped the pre-regeneration categories because of
  this. Always run `setup_input.py` first — it fixes the local tool too.
- **Never hand-edit the deployed `index.html`.** Parity is maintained by copying;
  an edit there is lost on the next build and silently diverges from `:8001`.
- **Pin the stlite version.** `hfspace/index.html` pins `@stlite/browser@1.8.1`;
  an unpinned CDN URL would change the bundled Streamlit under the app.
- **Everything runs client-side.** No API key is deployed and nothing a visitor
  does leaves their browser — but by the same token the whole CSV is downloaded,
  so anything in it is public once the Space is.
- **What is published.** The PDFs are public DOJ press releases. The prevention
  designs are model-generated reconstructions of what *would* have been visible
  in claims data — untested against real claim lines, every threshold needing
  calibration before use. The Space cards say so; keep that wording if the data
  changes.
