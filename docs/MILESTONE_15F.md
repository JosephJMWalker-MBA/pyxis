# Milestone 15F — read-only Chromium table evidence

## Product question

Can Pyxis expose literal HTML table structure for research inspection without inferring headers, expanding spans, typing values, flattening the table into a dataset, or taking browser-control authority?

15F answers **yes**.

## Boundary

```text
explicit Chromium DevTools endpoint
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('table')
    ↓
bounded table → row → cell evidence
```

`pyxis.browser.read_chromium_page_tables()` reads existing `table` elements in DOM order. For each returned table it preserves:

- 1-based table ordinal;
- direct caption `innerText` when present, bounded by an explicit text limit;
- exact caption Unicode code-point count;
- complete row count plus a bounded row prefix.

For each returned row it preserves:

- 1-based row ordinal within the table;
- complete direct-cell count plus a bounded cell prefix.

For each returned direct cell it preserves:

- 1-based cell ordinal within the row;
- literal `TH` or `TD` tag identity;
- browser-exposed `rowSpan`;
- browser-exposed `colSpan`;
- bounded rendered `innerText`;
- exact Unicode code-point count.

Rows are collected from the exact observed table only: descendant rows whose nearest `table` ancestor is a nested table are excluded from the outer table's row evidence.

`pyxis.app.observe_chromium_page_tables()` reuses the established endpoint normalization and exact target-selection authority and projects those transport facts into frozen application evidence.

## Nested bounds

15F uses independent mechanical limits:

```text
table_limit
    ↓
row_limit per returned table
    ↓
cell_limit per returned row
    ↓
text_limit for caption/cell text
```

Every bounded collection retains its complete observed count. Truncation is therefore evidence-derived rather than inferred from missing data.

## What table evidence does not mean

An HTML table is page structure, not automatically a clean rectangular dataset.

A `TH` tag is literal element identity, not a Pyxis-inferred header relationship. `rowspan` and `colspan` remain spans; Pyxis does not duplicate values into synthesized grid cells. A rendered string that looks numeric remains a string. DOM order is not relevance or data quality.

15F does not:

- infer which header applies to which data cell;
- expand `rowspan` or `colspan` into a normalized matrix;
- flatten tables into CSV-like rows;
- coerce strings into numbers, dates, booleans, or categories;
- infer units or column schemas;
- merge multi-row headers;
- deduplicate repeated values;
- rank or recommend tables;
- judge data quality or statistical validity;
- extract visual/CSS layout as semantic structure;
- navigate, scroll, activate, click, or submit forms;
- create or close browser targets;
- persist browser evidence;
- invoke an LLM;
- add browser UI.

## Real Chromium proof

15F adds a small independent real-browser acceptance test rather than rewriting the established browser fixtures.

The disposable page contains two literal tables. The first includes:

```html
<table>
  <caption>Study 😀 table</caption>
  <tr>
    <th rowspan="2">Metric</th>
    <td colspan="2">Alpha 😀 value</td>
    <td>Extra</td>
  </tr>
  <tr>
    <td>Beta</td>
    <td>Gamma</td>
  </tr>
</table>
```

Under:

```text
table_limit = 1
row_limit   = 1
cell_limit  = 2
text_limit  = 7
```

Pyxis proves:

- two tables yield one returned table plus `table_count=2` and `truncated=True`;
- the first table's two rows yield one returned row plus `row_count=2` and `rows_truncated=True`;
- the first row's three cells yield two returned cells plus `cell_count=3` and row truncation;
- `Study 😀 table` is bounded to `Study 😀` while retaining the complete Unicode count;
- the first cell remains literal `TH`, `row_span=2`, `col_span=1`;
- the second remains literal `TD`, `row_span=1`, `col_span=2`;
- `Alpha 😀 value` is bounded to `Alpha 😀` while retaining its complete Unicode count;
- no span expansion, header inference, navigation, scrolling, activation, or other browser control occurs.

## Validation

Implementation head:

- `670e74274e09e22c71fcb414ae3cb27efc053647`
- Actions #504
- Python 3.11: full suite passed
- Python 3.12: full suite passed
- Python 3.13: full suite passed
- Python 3.14: full suite passed
- inspected Python 3.11 log: 248 tests collected; established real Chromium integrations passed; new table real-browser integration passed; **248 passed**

A preceding implementation-only head, `f5b57b965c0c9e62cfa4821634e9f8ee6b303dd0` / Actions #503, also passed the full suite on Python 3.11–3.14 before the independent real-browser table proof was added.

## Decision D126

**Literal HTML table structure is valid read-only research evidence, but table markup is not automatically a normalized dataset. Pyxis may expose bounded table/row/cell DOM facts from one explicitly selected existing Chromium page, including literal TH/TD identity and browser-exposed row/column spans, while granting no header-inference, span-expansion, value-typing, dataset-normalization, ranking, interpretation, or browser-control authority.**
