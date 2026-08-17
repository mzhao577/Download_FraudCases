/*
 * Static build of webtool2's API.
 *
 * The UI in index.html is unchanged from the local tool - same markup, same
 * CSS, same keyboard handling. It talks to four endpoints, which a Hugging
 * Face static Space cannot serve, so this file intercepts fetch() and answers
 * them from the CSV in the browser:
 *
 *     /api/datasets            -> dataset summaries
 *     /api/cases?q&tab_*       -> filtered list + tab counts
 *     /api/case/{index}        -> one case, split into title/summary/highlight/fields
 *     pdf/<DocumentName>       -> served as a plain static file
 *
 * The shapes match webtool2/app.py exactly, including the rule that tab counts
 * are taken AFTER the search but BEFORE the tab filter.
 */
(() => {
  "use strict";

  const DATA_CSV = "data/extractedSummary_2025_DOJ_withFeatures.csv";
  const PDF_MANIFEST = "pdf/manifest.json";
  const PDF_DIR = "pdf/";
  const KEY = "DOJ_2025";

  const DOC_COLUMN = "DocumentName";
  const SUMMARY_COLUMN = "SchemeSummary";
  const TITLE_COLUMNS = ["DocumentName", "FraudType"];
  const TAB_COLUMNS = ["FeatureCategory", "FraudType", "Service", "CaseStatus"];

  // ------------------------------------------------------------------ CSV
  // RFC 4180: quoted fields may hold commas, newlines and doubled quotes.
  function parseCSV(text) {
    if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);   // strip BOM
    const rows = [];
    let row = [], field = "", quoted = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quoted) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; }
          else quoted = false;
        } else field += c;
        continue;
      }
      if (c === '"') quoted = true;
      else if (c === ",") { row.push(field); field = ""; }
      else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
      else if (c !== "\r") field += c;
    }
    if (field.length || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  const resolve = (columns, wanted) =>
    columns.find(c => c.toLowerCase() === wanted.toLowerCase()) || null;

  // --------------------------------------------------------------- dataset
  let loading = null;

  function loadDataset() {
    if (loading) return loading;
    loading = (async () => {
      const [csvText, pdfNames] = await Promise.all([
        fetch(DATA_CSV).then(r => {
          if (!r.ok) throw new Error(`cannot load ${DATA_CSV}: HTTP ${r.status}`);
          return r.text();
        }),
        // A static host cannot stat the folder, so the build writes a manifest.
        // Without one, assume every row has its PDF.
        fetch(PDF_MANIFEST).then(r => (r.ok ? r.json() : [])).catch(() => []),
      ]);

      const table = parseCSV(csvText).filter(r => r.length > 1 || (r[0] || "").trim() !== "");
      const columns = table.shift();
      const have = new Set(pdfNames);
      const docCol = resolve(columns, DOC_COLUMN) || columns[0];

      const rows = table.map((cells, i) => {
        const row = {};
        columns.forEach((c, j) => { row[c] = cells[j] ?? ""; });
        row._index = i;
        row._has_pdf = have.size ? have.has((row[docCol] || "").trim()) : true;
        return row;
      });

      const summaryCol = resolve(columns, SUMMARY_COLUMN);
      const titleCols = TITLE_COLUMNS.map(t => resolve(columns, t)).filter(Boolean);
      const tabCols = TAB_COLUMNS.map(t => resolve(columns, t)).filter(Boolean);
      // Highlight columns: everything positioned after the summary column.
      const highlight = summaryCol && columns.includes(summaryCol)
        ? columns.slice(columns.indexOf(summaryCol) + 1) : [];

      return { key: KEY, columns, rows, docCol, summaryCol, titleCols, tabCols, highlight };
    })();
    return loading;
  }

  // ------------------------------------------------------------- endpoints
  function apiDatasets(d) {
    return [{
      key: d.key,
      cases: d.rows.length,
      pdfs: d.rows.filter(r => r._has_pdf).length,
      missing_pdf: d.rows.filter(r => !r._has_pdf).length,
      orphan_pdfs: 0,
      columns: d.columns,
      doc_column: d.docCol,
      summary_column: d.summaryCol,
      title_columns: d.titleCols,
      highlight_columns: d.highlight,
      tab_columns: d.tabCols,
    }];
  }

  function apiCases(d, params) {
    const q = (params.get("q") || "").trim().toLowerCase();
    const asked = params.get("tab_column");
    const tcol = d.columns.includes(asked) ? asked : (d.tabCols[0] || null);
    const tabValue = params.get("tab_value") || "";

    let rows = d.rows;
    if (q) {
      rows = rows.filter(r => d.columns.some(c => String(r[c] ?? "").toLowerCase().includes(q)));
    }

    // Counts follow the search but precede the tab filter.
    const counts = new Map();
    if (tcol) {
      for (const r of rows) {
        const v = (r[tcol] || "").trim();
        if (v) counts.set(v, (counts.get(v) || 0) + 1);
      }
    }
    const searchedTotal = rows.length;

    if (tcol && tabValue) rows = rows.filter(r => (r[tcol] || "") === tabValue);

    const cases = rows.map(r => {
      const out = {
        index: r._index,
        doc: r[d.docCol] ?? "",
        has_pdf: r._has_pdf,
        tab: tcol ? (r[tcol] ?? "") : "",
      };
      d.titleCols.forEach(c => { out[c] = r[c] ?? ""; });
      return out;
    });

    return {
      total: d.rows.length,
      count: cases.length,
      searched_total: searchedTotal,
      tab_column: tcol,
      tab_columns: d.tabCols,
      tabs: [...counts.entries()]
        .sort((a, b) => (b[1] - a[1]) || a[0].localeCompare(b[0]))
        .map(([value, count]) => ({ value, count })),
      cases,
    };
  }

  function apiCase(d, index) {
    const row = d.rows[index];
    if (!row) return null;
    const shown = new Set([...d.titleCols, ...d.highlight, d.summaryCol]);
    const doc = row[d.docCol] ?? "";
    return {
      index,
      dataset: d.key,
      doc,
      has_pdf: row._has_pdf,
      title: d.titleCols.map(c => ({ name: c, value: row[c] ?? "" })),
      summary_column: d.summaryCol,
      summary_text: d.summaryCol ? (row[d.summaryCol] ?? "") : "",
      highlight: d.highlight.map(c => ({ name: c, value: row[c] ?? "" })),
      fields: d.columns.filter(c => !shown.has(c)).map(c => ({ name: c, value: row[c] ?? "" })),
      pdf_url: row._has_pdf ? PDF_DIR + encodeURIComponent(doc) : null,
    };
  }

  // ----------------------------------------------------------- fetch shim
  const json = (body, status = 200) =>
    new Response(JSON.stringify(body), {
      status, headers: { "Content-Type": "application/json" },
    });

  const original = window.fetch.bind(window);

  window.fetch = async (input, init) => {
    const raw = typeof input === "string" ? input : (input && input.url) || "";
    if (!raw.includes("/api/")) return original(input, init);

    const url = new URL(raw, location.href);
    const path = url.pathname.replace(/^.*(\/api\/)/, "/api/");
    let d;
    try {
      d = await loadDataset();
    } catch (err) {
      return json({ detail: String(err) }, 500);
    }

    if (path === "/api/datasets") return json(apiDatasets(d));
    if (path === "/api/cases") return json(apiCases(d, url.searchParams));

    const m = path.match(/^\/api\/case\/(\d+)$/);
    if (m) {
      const one = apiCase(d, Number(m[1]));
      return one ? json(one) : json({ detail: `case ${m[1]} out of range` }, 404);
    }
    return json({ detail: `unknown endpoint ${path}` }, 404);
  };
})();
