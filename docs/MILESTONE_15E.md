# Milestone 15E — read-only Chromium paragraph evidence

## Product question

Can Pyxis expose authored paragraphs as individually inspectable passage evidence without inventing sentence boundaries, relevance, citation identity, or browser control?

15E answers **yes**.

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
document.querySelectorAll('p')
    ↓
bounded DOM-order paragraph evidence
```

`pyxis.browser.read_chromium_page_paragraphs()` reads only existing `<p>` elements from the selected page. For each returned paragraph it preserves:

- 1-based DOM ordinal;
- literal authored `id` string, or an empty string when no `id` is present;
- bounded `innerText` prefix;
- exact Unicode code-point count.

The snapshot also records the complete matching-paragraph count so collection truncation is mechanically derivable from the explicit paragraph limit.

`pyxis.app.observe_chromium_page_paragraphs()` reuses the established endpoint normalization and exact target-selection authority and projects the transport snapshot into frozen application evidence.

## What paragraph evidence does not mean

A `<p>` element is an authored DOM fact, not a Pyxis semantic segmentation claim.

DOM order is not relevance. A paragraph is not automatically a quote-worthy passage. An authored element `id` is not guaranteed to be unique, stable across page revisions, permanent, or suitable as a citation key. Empty IDs remain empty and duplicate IDs remain duplicate.

15E does not:

- split paragraphs into sentences;
- merge adjacent paragraphs;
- infer article sections or semantic blocks;
- rank, recommend, summarize, or classify passages;
- treat paragraph text as a verified quotation from an immutable source;
- treat element IDs as stable citation locators;
- deduplicate or repair duplicate IDs;
- scroll to a paragraph;
- navigate or follow links;
- activate tabs;
- click or submit forms;
- create or close targets;
- persist browser evidence;
- invoke an LLM;
- add browser UI.

## Real Chromium proof

15E adds a small independent real-browser acceptance test rather than rewriting the existing 15A–15D shared Chromium fixture.

The test launches one disposable headless Chromium-family browser with a local page containing three literal `<p>` elements:

```html
<p id="passage">First 😀 paragraph</p>
<p id="passage">Methods</p>
<p>Appendix passage</p>
```

The duplicate `id="passage"` is intentional. Under `paragraph_limit=2` and `paragraph_text_limit=7`:

- three paragraphs yield two returned immutable records plus `paragraph_count=3` and `truncated=True`;
- the duplicate IDs remain duplicate;
- `First 😀 paragraph` is bounded to `First 😀` while retaining its complete Unicode code-point count;
- `Methods` remains untruncated;
- the third paragraph remains represented by the complete count/truncation facts;
- no navigation, scrolling, activation, or other browser control occurs.

## Validation

Implementation head:

- `291a0f2b617300b0be9cc1df6306096cf3de0967`
- Actions #491
- Python 3.11: full suite passed
- Python 3.12: full suite passed
- Python 3.13: full suite passed
- Python 3.14: full suite passed
- inspected Python 3.11 log: 242 tests collected; existing real Chromium integration passed; new paragraph real-browser integration passed; **242 passed**

## Decision D125

**Literal paragraph elements are valid read-only passage evidence, but paragraph boundaries and authored element IDs remain page-authored facts rather than Pyxis semantic segmentation or citation authority. Pyxis may expose bounded DOM-order `<p>` evidence from one explicitly selected existing Chromium page while preserving duplicate/empty IDs and granting no ranking, quotation-verification, locator-stability, or browser-control authority.**
