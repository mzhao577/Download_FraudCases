# webtool2 on Streamlit Community Cloud

A Streamlit build of [`webtool2/`](../webtool2), for deploying to
[Streamlit Community Cloud](https://share.streamlit.io) instead of a Hugging Face
Space.

Unlike [`hfspace/`](../hfspace) — which had to run Streamlit *in the browser*
because a Hugging Face static Space has no server — Community Cloud runs a real
Streamlit server. **The PDF pane works here.**

```bash
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

## Layout

| Where | Contents |
|---|---|
| **Sidebar** | Search, the tab dimension, the tab value, the **PDF pane height**, and the case list |
| **Top** | `⇤ First │ −50 │ −10 │ ← Previous │ Next → │ +10 │ +50 │ Last ⇥`, position, progress |
| **Main, left** | The source PDF |
| **Main, right** | Title and chips, `SchemeSummary`, the prevention design, then the remaining fields |

Filters and search behave as in the local tool: free text across every column
with matches highlighted, and **tab counts taken after the search but before the
tab filter**, so selecting one tab does not blank the others. The prevention
block is data-driven — every column after `SchemeSummary` renders there, so a
fifth analysis column needs no code change.

## Sizing the PDF pane

Streamlit has no drag-resizable panes, so the height is a control in the sidebar:

| Control | Effect |
|---|---|
| **PDF pane height** | 300–2000 px. Taller shows more of the page; shorter brings the summary alongside it. |
| **Fit PDF to page length** | Drops the fixed box and grows to the whole document — the page itself then scrolls. |

The setting persists as you move between cases. The slider stays visible but
greyed while *fit* is on, so switching back does not lose your height.

## Where the PDFs come from

Resolved in this order, so one codebase covers every deployment:

| Order | Source | Set up by |
|---|---|---|
| 1 | `streamlit_app/pdf/<DocumentName>` | Copying the PDFs into that folder |
| 2 | `PDF_BASE_URL` + the filename | A static host, via `st.secrets` or the environment |
| 3 | *neither* | Nothing — the pane says so and every field still renders |

For local development, symlink the corpus instead of copying it:

```bash
ln -s ../downloaded/DOJ_2025 streamlit_app/pdf
```

`streamlit_app/pdf/` is gitignored, so the corpus never enters git history by
accident. **That has a consequence for Community Cloud**, which deploys only what
is committed: see the table below.

> These PDFs are the pipeline's own Chrome renderings of the saved press-release
> pages, not files hosted by DOJ. There is no upstream URL that serves the same
> bytes, so they cannot be fetched from justice.gov at runtime — they have to
> travel with the app or come from a host you control.

## Deploying

1. Push this folder to GitHub.
2. On [share.streamlit.io](https://share.streamlit.io), **Create app** → pick the
   repo and branch.
3. Set **Main file path** to `streamlit_app/app.py`.
4. Deploy.

Dependencies come from `streamlit_app/requirements.txt`. Community Cloud
prefers a requirements file **in the entrypoint's own directory** over the
repository root, which matters here: the root `requirements.txt` is the
scraping pipeline's (selenium, fastapi, anthropic) and lists neither Streamlit
nor pandas.

A **private repo works** — Community Cloud creates a read-only deploy key, which
needs the extra `repo` OAuth scope when you connect GitHub. Going public is not
required.

### Choosing a PDF route

| Route | PDF pane | Cost |
|---|---|---|
| **Commit the PDFs** to `streamlit_app/pdf/` (drop the gitignore line) | ✅ | ~228 MB in the repo and in every clone |
| **Set `PDF_BASE_URL`** to a static host you control | ✅ | Somewhere to host 228 MB; add the secret in *App settings → Secrets* |
| **Ship the CSV only** | ✗ notice instead | Nothing; the repo stays ~1.5 MB |

For the second route, add to **App settings → Secrets**:

```toml
PDF_BASE_URL = "https://example.com/path/to/pdfs"
```

## Community Cloud limits worth knowing

- **1 GB resource limit** per app. This app holds a 1.5 MB CSV in memory and
  reads one ~400 KB PDF at a time, so it is nowhere near the ceiling — but
  committing the PDFs raises the clone size, not the memory use.
- **3 free apps** per account.
- **Apps sleep when idle** and take a few seconds to wake.

## Known differences from `127.0.0.1:8001`

- **No `j`/`k` keyboard shortcuts.** Streamlit cannot bind them; use the buttons
  or the case list.
- **The case list is in the sidebar**, not a third column — Streamlit's layout
  does not give three panels enough width to stay readable.
- **Each interaction is a rerun.** Navigation feels a touch heavier than the
  local tool's client-side switching.

For a pixel-identical copy of the local tool, see
[`hfspace_webtool2/`](../hfspace_webtool2), which serves webtool2's own
`index.html` unchanged.

## Notes

`st.pdf` needs the `streamlit-pdf` package, which requires the `components.v2`
API added in Streamlit **1.61** — hence the floor in `requirements.txt`. When
that package is missing or mismatched, `st.pdf` does not raise: it draws a
broken-document placeholder. The app therefore probes for the component at
import and, if it is unavailable, **renders the pages to images with
`pypdfium2`** instead, inside a scrollable box of the chosen height, with a
download button beneath.

That fallback is what runs on a machine with an older Streamlit — including
this repo's own environment, which is pinned at 1.54 for the scraping pipeline.
It is not an `<embed>` or an iframe on purpose: Streamlit's HTML component is a
**sandboxed** iframe, and Chrome refuses to load the PDF plugin inside one, so
every in-frame approach shows a broken-document icon regardless of the URL
scheme used.

The case text is summarised from public DOJ press releases. The prevention
designs are model-generated reconstructions of what *would* have been visible in
claims data — none has been tested against real claim lines, and every threshold
needs calibration against a control population before use.
