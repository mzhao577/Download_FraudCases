#!/usr/bin/env python3
"""Case review with the prevention design - Streamlit port of webtool2.

Same reading order as the local tool: the case list on the left, and on the
right the title, SchemeSummary, then the prevention design, then every other
field. The PDF pane is gone - a Hugging Face Space ships the CSV only - so the
list takes that space instead.

The prevention block is data-driven exactly as in webtool2/dataset.py: any
column positioned AFTER the summary column is a highlight column. Add a fifth
analysis column to the CSV and it renders there with no code change.

    streamlit run app.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import pandas as pd
import streamlit as st

HERE = Path(__file__).resolve().parent
# Under stlite the app is mounted at the virtual-filesystem root, so fall back
# to a plain relative path when app.py's own folder has no data/.
DATA_DIR = next((p for p in (HERE / "data", Path("data")) if p.is_dir()), HERE / "data")

DOC_COLUMN = "DocumentName"
SUMMARY_COLUMN = "SchemeSummary"
TITLE_COLUMNS = ("DocumentName", "FraudType")
# Columns offered as the tab dimension, in order of preference.
TAB_COLUMNS = ("FeatureCategory", "FraudType", "Service", "CaseStatus")
# Columns worth showing in the case list next to the name.
LIST_COLUMNS = ("ReportDT", "Service", "FraudType", "FeatureCategory")

ACCENT = "#1f5fa9"
ACCENT_SOFT = "#eaf1fa"
PREV = "#0f7a5a"
PREV_SOFT = "#e8f6f1"
PREV_LINE = "#bfe3d6"
MUTED = "#5b6472"
LINE = "#dfe3e9"

CSS = f"""
<style>
  .block-container {{ padding-top: 2.2rem; padding-bottom: 1rem; max-width: 100%; }}
  div[data-testid="stToolbar"], #MainMenu, footer {{ visibility: hidden; height: 0; }}
  .case-title {{ font-size: 17px; font-weight: 600; line-height: 1.35; margin: 0 0 8px; }}
  .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 4px; }}
  .chip {{ font-size: 11px; padding: 2px 9px; border-radius: 999px; background: {ACCENT_SOFT};
          color: {ACCENT}; border: 1px solid #cfe0f2; white-space: nowrap; }}
  .chip.k {{ background: #f1f3f6; color: {MUTED}; border-color: {LINE}; }}
  .chip.p {{ background: #fff; color: {PREV}; border-color: {PREV_LINE}; }}
  h2.sec {{ font-size: 11px !important; text-transform: uppercase; letter-spacing: .07em;
           color: {MUTED}; margin: 0 0 8px; font-weight: 600; }}
  .summary {{ font-size: 15px; line-height: 1.62; background: #fbfcfd; border: 1px solid {LINE};
             border-left: 3px solid {ACCENT}; border-radius: 6px; padding: 12px 14px; margin: 0; }}
  .prev {{ background: {PREV_SOFT}; border: 1px solid {PREV_LINE}; border-radius: 8px;
          padding: 14px 16px; margin: 14px 0 4px; }}
  .prev h2.sec {{ color: {PREV}; }}
  .prev .label {{ font-size: 11px; text-transform: uppercase; letter-spacing: .06em;
                 color: {PREV}; font-weight: 600; margin: 10px 0 4px; }}
  .prev .val {{ font-size: 14px; line-height: 1.6; margin: 0; }}
  .prev ol {{ margin: 4px 0 0; padding-left: 20px; }}
  .prev ol li {{ font-size: 14px; line-height: 1.55; margin-bottom: 7px; }}
  .prev .none {{ color: {MUTED}; font-style: italic; }}
  .fields {{ font-size: 13.5px; }}
  .fields .row {{ display: flex; gap: 12px; padding: 6px 0; border-bottom: 1px solid {LINE}; }}
  .fields .k {{ flex: 0 0 150px; color: {MUTED}; }}
  .fields .v {{ flex: 1 1 auto; min-width: 0; word-wrap: break-word; }}
  .pos {{ font-variant-numeric: tabular-nums; font-weight: 600; white-space: nowrap;
         text-align: center; padding-top: 6px; }}
  .pos .of {{ color: {MUTED}; font-weight: 400; }}
  div[data-testid="stHorizontalBlock"] div[data-testid="column"] .stButton button {{ width: 100%; }}
</style>
"""


# ----------------------------------------------------------------- data layer
def resolve(columns: list[str], wanted: str) -> str | None:
    """Case-insensitive column lookup, as in webtool2/dataset.py."""
    return {c.lower(): c for c in columns}.get(wanted.lower())


@st.cache_data(show_spinner=False)
def load_dataset() -> tuple[pd.DataFrame, list[str], str]:
    csvs = sorted(DATA_DIR.glob("*.csv"))
    if not csvs:
        return pd.DataFrame(), [], ""
    # Prefer the richest file when several are present (..._withFeatures wins).
    path = max(csvs, key=lambda p: len(re.split(r"[^A-Za-z0-9]+", p.stem)))
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig").fillna("")
    return df, list(df.columns), path.name


def highlight_columns(columns: list[str]) -> list[str]:
    """Columns after the summary column - the prevention design."""
    s = resolve(columns, SUMMARY_COLUMN)
    if not s or s not in columns:
        return []
    return columns[columns.index(s) + 1:]


@st.cache_data(show_spinner=False)
def search(df: pd.DataFrame, q: str) -> pd.DataFrame:
    """Free text across every column, as the local tool does."""
    q = q.strip().lower()
    if not q:
        return df
    hay = df.apply(lambda col: col.str.lower(), axis=0)
    mask = pd.Series(False, index=df.index)
    for col in hay.columns:
        mask |= hay[col].str.contains(q, regex=False, na=False)
    return df[mask]


# ------------------------------------------------------------------ rendering
def esc(v: object) -> str:
    return html.escape(str(v or "").strip())


def chips(values: list[str], kind: str = "") -> str:
    cls = f"chip {kind}".strip()
    return "".join(f'<span class="{cls}">{esc(v)}</span>' for v in values if str(v).strip())


def looks_like_list(value: str) -> bool:
    """Short semicolon-separated values render as pills, prose as a block."""
    return ";" in value and len(value) < 120


def humanise(column: str) -> str:
    """DesiredServiceGroups -> Desired Service Groups, for the panel labels."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", column)


def numbered_items(value: str) -> list[str]:
    """Split '1) ... 2) ... 3) ...' into its parts; empty list if unnumbered."""
    if not re.match(r"^\s*1\)", value):
        return []
    parts = re.split(r"(?:(?<=\.)|(?<=\s))(?=\d\)\s)", value.strip())
    return [re.sub(r"^\d\)\s*", "", p).strip() for p in parts if p.strip()]


def render_prevention(row: pd.Series, cols: list[str]) -> str:
    out = ['<div class="prev"><h2 class="sec">Prevention design</h2>']
    for col in cols:
        value = str(row.get(col, "") or "").strip()
        out.append(f'<div class="label">{esc(humanise(col))}</div>')
        if not value:
            out.append('<p class="val none">not set</p>')
        elif looks_like_list(value):
            out.append(f'<div class="chips">{chips([v.strip() for v in value.split(";")], "p")}</div>')
        elif (items := numbered_items(value)):
            out.append("<ol>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ol>")
        else:
            out.append(f'<p class="val">{esc(value)}</p>')
    out.append("</div>")
    return "".join(out)


def render_fields(row: pd.Series, cols: list[str]) -> str:
    rows = "".join(
        f'<div class="row"><div class="k">{esc(c)}</div>'
        f'<div class="v">{esc(row.get(c, "")) or "&mdash;"}</div></div>'
        for c in cols)
    return f'<div class="fields">{rows}</div>'


# ----------------------------------------------------------------------- page
st.set_page_config(page_title="Fraud Case Review - Prevention Design",
                   page_icon="🔎", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

df, columns, source_name = load_dataset()
if df.empty:
    st.error(f"No CSV found in {DATA_DIR}. Add the summary CSV and reload.")
    st.stop()

doc_col = resolve(columns, DOC_COLUMN) or columns[0]
summary_col = resolve(columns, SUMMARY_COLUMN)
title_cols = [c for c in (resolve(columns, t) for t in TITLE_COLUMNS) if c]
prev_cols = highlight_columns(columns)
tab_cols = [c for c in (resolve(columns, t) for t in TAB_COLUMNS) if c]
rest_cols = [c for c in columns if c not in {doc_col, summary_col, *prev_cols}]

st.session_state.setdefault("idx", 0)


def reset_idx() -> None:
    st.session_state.idx = 0


# --- controls ---------------------------------------------------------------
head, ctrl = st.columns([3, 4])
with head:
    st.markdown("#### Fraud case review — prevention design")
    st.caption(f"{len(df)} cases · {len(columns)} columns · {source_name}")
with ctrl:
    c1, c2, c3 = st.columns([3, 2, 3])
    q = c1.text_input("Search", key="q", placeholder="free text, every column",
                      on_change=reset_idx)
    tab_col = c2.selectbox("Tabs by", tab_cols, key="tabcol", on_change=reset_idx) \
        if tab_cols else None

# Counts follow the search but precede the tab filter, so selecting a tab does
# not blank the others - same rule as webtool2.
hits = search(df, q)
tab_value = "All"
if tab_col:
    counts = hits[tab_col].replace("", "(blank)").value_counts()
    options = ["All"] + [f"{k}  ({v})" for k, v in counts.items()]
    choice = c3.selectbox(f"{tab_col}", options, key="tabval", on_change=reset_idx)
    tab_value = "All" if choice == "All" else choice.rsplit("  (", 1)[0]

view = hits if tab_value == "All" else \
    hits[hits[tab_col].replace("", "(blank)") == tab_value]

total = len(view)
if total == 0:
    st.warning("No cases match this search and tab. Clear the search to start again.")
    st.stop()

st.session_state.idx = max(0, min(st.session_state.idx, total - 1))


# --- navigation -------------------------------------------------------------
def step(n: int) -> None:
    st.session_state.idx = max(0, min(st.session_state.idx + n, total - 1))


def jump(to: int) -> None:
    st.session_state.idx = max(0, min(to, total - 1))


nav = st.columns([1, 1, 1, 1.4, 1.4, 1, 1, 1, 2, 3])
labels = [("⇤ First", lambda: jump(0)), ("−50", lambda: step(-50)),
          ("−10", lambda: step(-10)), ("← Previous", lambda: step(-1)),
          ("Next →", lambda: step(1)), ("+10", lambda: step(10)),
          ("+50", lambda: step(50)), ("Last ⇥", lambda: jump(total - 1))]
for col, (label, fn) in zip(nav, labels):
    col.button(label, on_click=fn, use_container_width=True,
               key=f"nav{label}", disabled=total == 1)
nav[8].markdown(f'<div class="pos">{st.session_state.idx + 1} '
                f'<span class="of">of {total}</span></div>', unsafe_allow_html=True)
nav[9].progress((st.session_state.idx + 1) / total)

# --- list + detail ----------------------------------------------------------
left, right = st.columns([1.05, 2], gap="medium")

with left:
    list_cols = [c for c in (resolve(columns, c) for c in LIST_COLUMNS) if c]
    shown = view[[doc_col, *list_cols]].reset_index(drop=True)
    shown.insert(0, "#", range(1, total + 1))
    event = st.dataframe(shown, hide_index=True, height=620, key="caselist",
                         on_select="rerun", selection_mode="single-row",
                         column_config={doc_col: st.column_config.TextColumn("Case", width="large")})
    picked = event.selection.rows[0] if event.selection.rows else None
    # A click in the list moves the position; the nav buttons stay authoritative
    # otherwise, so a stale selection never drags the view back.
    if picked is not None and picked != st.session_state.get("_last_pick"):
        st.session_state._last_pick = picked
        if picked != st.session_state.idx:
            st.session_state.idx = picked
            st.rerun()

with right:
    row = view.iloc[st.session_state.idx]
    st.markdown(f'<div class="case-title">{esc(row[doc_col])}</div>'
                f'<div class="chips">{chips([row[c] for c in title_cols if c != doc_col])}'
                f'{chips([row[c] for c in (resolve(columns, "CaseStatus"),) if c], "k")}</div>',
                unsafe_allow_html=True)
    if summary_col:
        st.markdown('<h2 class="sec">Scheme summary</h2>'
                    f'<p class="summary">{esc(row[summary_col]) or "no summary"}</p>',
                    unsafe_allow_html=True)
    if prev_cols:
        st.markdown(render_prevention(row, prev_cols), unsafe_allow_html=True)
    with st.expander(f"All other fields ({len(rest_cols)})", expanded=False):
        st.markdown(render_fields(row, rest_cols), unsafe_allow_html=True)
