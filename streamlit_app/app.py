#!/usr/bin/env python3
"""Case review with the prevention design - Streamlit build of webtool2.

Written for Streamlit Community Cloud, where the app runs as a real Streamlit
server (unlike the Hugging Face static Space, which had to answer webtool2's API
in the browser). That means the PDF pane works again.

Reading order follows the local tool: the case list and filters on the left, and
in the main area the source PDF beside the summary, the prevention design and the
remaining fields.

    streamlit run streamlit_app/app.py

The PDFs are resolved in this order, so the same code works whether or not the
corpus travels with the app:

    1. a local folder - streamlit_app/pdf/<DocumentName>
    2. PDF_BASE_URL - a static host, set in st.secrets or the environment
    3. neither - the PDF pane explains it, and every field still renders

See README.md in this folder for the deployment routes.
"""
from __future__ import annotations

import html
import io
import os
import re
from pathlib import Path

import pandas as pd
import streamlit as st

# st.pdf renders through the optional streamlit-pdf package. When that package
# is missing or mismatched it does NOT raise - it draws a broken-document
# placeholder - so probe it up front and use the browser's own viewer instead.
try:
    import streamlit_pdf as _pdf_component  # noqa: F401
    HAVE_PDF_COMPONENT = True
except Exception:  # noqa: BLE001
    HAVE_PDF_COMPONENT = False

HERE = Path(__file__).resolve().parent
DATA_DIR = next((p for p in (HERE / "data", Path("data")) if p.is_dir()), HERE / "data")
PDF_DIR = next((p for p in (HERE / "pdf", Path("pdf")) if p.is_dir()), None)

DOC_COLUMN = "DocumentName"
SUMMARY_COLUMN = "SchemeSummary"
TITLE_COLUMNS = ("DocumentName", "FraudType", "CaseStatus")
# Columns offered as the tab dimension, in order of preference.
TAB_COLUMNS = ("FeatureCategory", "FraudType", "Service", "CaseStatus")

ACCENT, ACCENT_SOFT = "#1f5fa9", "#eaf1fa"
PREV, PREV_SOFT, PREV_LINE = "#0f7a5a", "#e8f6f1", "#bfe3d6"
MUTED, LINE = "#5b6472", "#dfe3e9"

CSS = f"""
<style>
  .block-container {{ padding-top: 2rem; padding-bottom: 1rem; max-width: 100%; }}
  div[data-testid="stToolbar"], #MainMenu, footer {{ visibility: hidden; height: 0; }}
  .case-title {{ font-size: 17px; font-weight: 600; line-height: 1.35; margin: 0 0 8px;
                word-break: break-word; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }}
  .chip {{ font-size: 11px; padding: 2px 9px; border-radius: 999px; background: {ACCENT_SOFT};
          color: {ACCENT}; border: 1px solid #cfe0f2; white-space: nowrap; }}
  .chip.k {{ background: #f1f3f6; color: {MUTED}; border-color: {LINE}; }}
  .chip.p {{ background: #fff; color: {PREV}; border-color: {PREV_LINE}; }}
  h2.sec {{ font-size: 11px !important; text-transform: uppercase; letter-spacing: .07em;
           color: {MUTED}; margin: 2px 0 8px; font-weight: 600; }}
  .summary {{ font-size: 15px; line-height: 1.62; background: #fbfcfd; border: 1px solid {LINE};
             border-left: 3px solid {ACCENT}; border-radius: 6px; padding: 12px 14px; margin: 0; }}
  .prev {{ background: {PREV_SOFT}; border: 1px solid {PREV_LINE}; border-radius: 8px;
          padding: 14px 16px; margin: 14px 0 4px; }}
  .prev h2.sec {{ color: {PREV}; }}
  .prev .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: .06em;
                 color: {PREV}; font-weight: 600; margin: 12px 0 4px; }}
  .prev .val {{ font-size: 14px; line-height: 1.6; margin: 0; background: #fff;
               border: 1px solid {PREV_LINE}; border-radius: 6px; padding: 10px 12px; }}
  .prev ol {{ margin: 4px 0 0; padding-left: 22px; }}
  .prev ol li {{ font-size: 14px; line-height: 1.55; margin-bottom: 7px; }}
  .prev .none {{ color: {MUTED}; font-style: italic; background: none; border: 0; padding: 0; }}
  .fields .row {{ display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid {LINE};
                 font-size: 13.5px; }}
  .fields .k {{ flex: 0 0 150px; color: {MUTED}; }}
  .fields .v {{ flex: 1 1 auto; min-width: 0; word-break: break-word; }}
  .pos {{ font-variant-numeric: tabular-nums; font-weight: 600; white-space: nowrap;
         text-align: center; padding-top: 6px; }}
  .pos .of {{ color: {MUTED}; font-weight: 400; }}
  .nopdf {{ border: 1px dashed {LINE}; border-radius: 8px; padding: 28px 20px; text-align: center;
           color: {MUTED}; font-size: 13.5px; line-height: 1.6; background: #fbfcfd; }}
  div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton button {{ width: 100%; }}
  mark {{ background: #ffe9a8; padding: 0 1px; }}
</style>
"""


# ----------------------------------------------------------------- data layer
def resolve(columns: list[str], wanted: str) -> str | None:
    """Case-insensitive column lookup, as in webtool2/dataset.py."""
    return {c.lower(): c for c in columns}.get(wanted.lower())


@st.cache_data(show_spinner=False)
def load_dataset() -> tuple[pd.DataFrame, str]:
    csvs = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.is_dir() else []
    if not csvs:
        return pd.DataFrame(), ""
    # Prefer the richest file when several are present (..._withFeatures wins).
    path = max(csvs, key=lambda p: len(re.split(r"[^A-Za-z0-9]+", p.stem)))
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")
    return df, path.name


def highlight_columns(columns: list[str]) -> list[str]:
    """Columns after the summary column - the prevention design."""
    s = resolve(columns, SUMMARY_COLUMN)
    return columns[columns.index(s) + 1:] if s and s in columns else []


@st.cache_data(show_spinner=False)
def search(df: pd.DataFrame, q: str) -> pd.DataFrame:
    """Free text across every column, as the local tool does."""
    q = q.strip().lower()
    if not q:
        return df
    mask = pd.Series(False, index=df.index)
    for col in df.columns:
        mask |= df[col].str.lower().str.contains(q, regex=False, na=False)
    return df[mask]


def pdf_base_url() -> str:
    """A static host for the PDFs, from secrets or the environment."""
    try:
        if "PDF_BASE_URL" in st.secrets:
            return str(st.secrets["PDF_BASE_URL"]).rstrip("/") + "/"
    except Exception:  # noqa: BLE001 - no secrets file is normal
        pass
    url = os.environ.get("PDF_BASE_URL", "").strip()
    return url.rstrip("/") + "/" if url else ""


# ------------------------------------------------------------------ rendering
def esc(v: object) -> str:
    return html.escape(str(v or "").strip())


def mark(text: str, needle: str) -> str:
    """Escape, then highlight the search term - the local tool does the same."""
    out = esc(text)
    if needle:
        out = re.sub(f"({re.escape(html.escape(needle))})", r"<mark>\1</mark>", out,
                     flags=re.IGNORECASE)
    return out


def humanise(column: str) -> str:
    """DesiredServiceGroups -> Desired Service Groups, for readable labels."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", column).replace("_", " ")


def numbered_items(value: str) -> list[str]:
    """Split '1) ... 2) ... 3) ...' into its parts; empty list if unnumbered."""
    if not re.match(r"^\s*1\)", value):
        return []
    parts = re.split(r"(?:(?<=\.)|(?<=\s))(?=\d\)\s)", value.strip())
    return [re.sub(r"^\d\)\s*", "", p).strip() for p in parts if p.strip()]


def render_prevention(row: pd.Series, cols: list[str], q: str) -> str:
    out = ['<div class="prev"><h2 class="sec">Prevention design</h2>']
    for col in cols:
        value = str(row.get(col, "") or "").strip()
        out.append(f'<div class="label">{esc(humanise(col))}</div>')
        if not value:
            out.append('<p class="val none">not set</p>')
        elif ";" in value and len(value) < 120:
            pills = "".join(f'<span class="chip p">{mark(v.strip(), q)}</span>'
                            for v in value.split(";") if v.strip())
            out.append(f'<div class="chips">{pills}</div>')
        elif (items := numbered_items(value)):
            out.append("<ol>" + "".join(f"<li>{mark(i, q)}</li>" for i in items) + "</ol>")
        else:
            out.append(f'<p class="val">{mark(value, q)}</p>')
    out.append("</div>")
    return "".join(out)


def render_fields(row: pd.Series, cols: list[str], q: str) -> str:
    rows = "".join(
        f'<div class="row"><div class="k">{esc(humanise(c))}</div>'
        f'<div class="v">{mark(row.get(c, ""), q) or "&mdash;"}</div></div>'
        for c in cols)
    return f'<div class="fields">{rows}</div>'


@st.cache_data(show_spinner=False, max_entries=4)
def render_pages(data: bytes, scale: float = 1.7, max_pages: int = 20) -> list[bytes]:
    """PDF bytes -> one PNG per page, for the no-component fallback.

    PDFium is not thread-safe, which is why the pipeline reads PDFs on one
    thread; a Streamlit session runs its script serially, so rendering here is
    safe. Capped at max_pages - these press releases are a few pages each.
    """
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return []
    out: list[bytes] = []
    try:
        doc = pdfium.PdfDocument(data)
        for i in range(min(len(doc), max_pages)):
            buf = io.BytesIO()
            doc[i].render(scale=scale).to_pil().save(buf, format="PNG")
            out.append(buf.getvalue())
    except Exception:  # noqa: BLE001 - a corrupt file must not kill the page
        return out
    return out


@st.cache_data(show_spinner=False, max_entries=8)
def fetch_pdf(url: str) -> bytes | None:
    """Pull a PDF from PDF_BASE_URL so it can be rendered like a local one."""
    from urllib.request import urlopen
    try:
        with urlopen(url, timeout=20) as r:  # noqa: S310 - operator-supplied host
            return r.read()
    except Exception:  # noqa: BLE001
        return None


def show_pdf(name: str, height: int | str = 780) -> None:
    """Render the source document, from a local folder or a static host.

    height is a pixel count, or "stretch" to grow with the document rather than
    scrolling inside a fixed box.
    """
    local = (PDF_DIR / name) if PDF_DIR else None
    source: object | None = None
    if local is not None and local.is_file():
        source = local.read_bytes()
    elif (base := pdf_base_url()):
        from urllib.parse import quote
        source = base + quote(name)

    if source is None:
        st.markdown(
            '<div class="nopdf"><strong>Source PDF not available in this deployment.</strong><br>'
            'Add the PDFs to <code>streamlit_app/pdf/</code>, or set <code>PDF_BASE_URL</code> '
            'to a static host. Every extracted field is shown on the right either way.</div>',
            unsafe_allow_html=True)
        return

    if HAVE_PDF_COMPONENT:
        try:
            st.pdf(source, height=height)
            return
        except Exception:  # noqa: BLE001
            pass  # fall through to the page images below

    # No streamlit-pdf. An <embed> is not an option either: Streamlit's HTML
    # component is a sandboxed iframe, and Chrome refuses to load the PDF plugin
    # inside one. Rendering the pages to images sidesteps the plugin entirely.
    px = 1400 if height == "stretch" else int(height)
    data = source if isinstance(source, bytes) else fetch_pdf(str(source))
    pages = render_pages(data) if data else []

    if not pages:
        st.warning("Could not render this PDF here. Install `streamlit[pdf]` for the "
                   "built-in viewer, or use the download button below.")
    else:
        with st.container(height=px, border=True):
            for img in pages:
                st.image(img, width="stretch")
    if data:
        st.download_button("Download the source PDF", data, file_name=name,
                           mime="application/pdf", width="stretch",
                           key=f"dl{name}")


# ----------------------------------------------------------------------- page
st.set_page_config(page_title="Fraud Case Review - Prevention Design",
                   page_icon="🔎", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

df, source_name = load_dataset()
if df.empty:
    st.error(f"No CSV found in {DATA_DIR}. Add the summary CSV and reload.")
    st.stop()

columns = list(df.columns)
doc_col = resolve(columns, DOC_COLUMN) or columns[0]
summary_col = resolve(columns, SUMMARY_COLUMN)
prev_cols = highlight_columns(columns)
title_cols = [c for c in (resolve(columns, t) for t in TITLE_COLUMNS) if c and c != doc_col]
tab_cols = [c for c in (resolve(columns, t) for t in TAB_COLUMNS) if c]
rest_cols = [c for c in columns if c not in {doc_col, summary_col, *prev_cols}]

st.session_state.setdefault("idx", 0)


def reset_idx() -> None:
    st.session_state.idx = 0


# --- sidebar: filters and the case list ------------------------------------
with st.sidebar:
    st.markdown("#### Fraud case review")
    st.caption(f"{len(df)} cases · {len(columns)} columns")
    q = st.text_input("Search", key="q", placeholder="free text, every column",
                      on_change=reset_idx)
    tab_col = st.selectbox("Tabs by", tab_cols, key="tabcol", on_change=reset_idx) \
        if tab_cols else None

    # Counts follow the search but precede the tab filter, so selecting a tab
    # does not blank the others - the same rule as webtool2.
    hits = search(df, q)
    tab_value = "All"
    if tab_col:
        counts = hits[tab_col].replace("", "(blank)").value_counts()
        options = ["All"] + [f"{k}  ({v})" for k, v in counts.items()]
        choice = st.selectbox(tab_col, options, key="tabval", on_change=reset_idx)
        tab_value = "All" if choice == "All" else choice.rsplit("  (", 1)[0]

view = hits if tab_value == "All" else \
    hits[hits[tab_col].replace("", "(blank)") == tab_value]
total = len(view)

if total == 0:
    st.warning("No cases match this search and tab. Clear the search to start again.")
    st.stop()

st.session_state.idx = max(0, min(st.session_state.idx, total - 1))


def step(n: int) -> None:
    st.session_state.idx = max(0, min(st.session_state.idx + n, total - 1))


def jump(to: int) -> None:
    st.session_state.idx = max(0, min(to, total - 1))


with st.sidebar:
    # Streamlit has no drag-resizable panes, so the PDF height is a control.
    # It persists across cases and reruns because the widget carries a key.
    st.divider()
    fit = st.checkbox("Fit PDF to page length", key="pdffit",
                      help="Grow the pane to the whole document instead of scrolling "
                           "inside a fixed box. The page itself then scrolls.")
    # Rendered even when unused: a widget that stops rendering loses its state,
    # which would reset a chosen height every time "fit" is toggled.
    chosen = st.slider(
        "PDF pane height", min_value=300, max_value=2000, value=780, step=20, key="pdfh",
        disabled=fit,
        help="Taller shows more of the page; shorter puts the summary alongside it.")
    pdf_height: int | str = "stretch" if fit else chosen
    st.divider()

    st.caption(f"Showing **{total}** of {len(df)}")
    listing = view[[doc_col]].reset_index(drop=True)
    listing.insert(0, "#", range(1, total + 1))
    event = st.dataframe(
        listing, hide_index=True, height=420, key="caselist",
        on_select="rerun", selection_mode="single-row",
        column_config={doc_col: st.column_config.TextColumn("Case", width="large")})
    picked = event.selection.rows[0] if event.selection.rows else None
    # A click moves the position; the nav buttons stay authoritative otherwise,
    # so a stale selection never drags the view back.
    if picked is not None and picked != st.session_state.get("_pick"):
        st.session_state._pick = picked
        if picked != st.session_state.idx:
            st.session_state.idx = picked
            st.rerun()
    st.caption(f"Source: `{source_name}`")

# --- navigation -------------------------------------------------------------
nav = st.columns([1, 1, 1, 1.4, 1.4, 1, 1, 1, 1.6, 3])
for col, (label, fn) in zip(nav, [
        ("⇤ First", lambda: jump(0)), ("−50", lambda: step(-50)), ("−10", lambda: step(-10)),
        ("← Previous", lambda: step(-1)), ("Next →", lambda: step(1)),
        ("+10", lambda: step(10)), ("+50", lambda: step(50)),
        ("Last ⇥", lambda: jump(total - 1))]):
    col.button(label, on_click=fn, width="stretch", key=f"nav{label}",
               disabled=total == 1)
nav[8].markdown(f'<div class="pos">{st.session_state.idx + 1} '
                f'<span class="of">of {total}</span></div>', unsafe_allow_html=True)
nav[9].progress((st.session_state.idx + 1) / total)

# --- the two panels ---------------------------------------------------------
row = view.iloc[st.session_state.idx]
left, right = st.columns([1, 1], gap="medium")

with left:
    show_pdf(str(row[doc_col]).strip(), pdf_height)

with right:
    st.markdown(
        f'<div class="case-title">{mark(row[doc_col], q)}</div>'
        f'<div class="chips">'
        + "".join(f'<span class="chip">{esc(row[c])}</span>'
                  for c in title_cols if str(row[c]).strip())
        + f'<span class="chip k">case {st.session_state.idx + 1} of {total}</span></div>',
        unsafe_allow_html=True)
    if summary_col:
        st.markdown('<h2 class="sec">Scheme summary</h2>'
                    f'<p class="summary">{mark(row[summary_col], q) or "no summary"}</p>',
                    unsafe_allow_html=True)
    if prev_cols:
        st.markdown(render_prevention(row, prev_cols, q), unsafe_allow_html=True)
    with st.expander(f"All other fields ({len(rest_cols)})", expanded=False):
        st.markdown(render_fields(row, rest_cols, q), unsafe_allow_html=True)
