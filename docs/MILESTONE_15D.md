# Milestone 15D — Read-Only Page-Declared Metadata Evidence

**Decision D124 — Page-declared metadata is evidence of what the page declares, not verified provenance. Pyxis may expose bounded document-language, canonical-link, and meta-description declarations from one explicitly selected existing Chromium page, but duplicate or conflicting declarations must remain visible rather than being silently resolved into source truth.**

## Product question

Can Pyxis expose the source-identity hints already declared by a page so a researcher can inspect them without Pyxis promoting those declarations into verified provenance?

15D answers **yes** with a fourth deliberately narrow read-only Chromium evidence boundary.

## Boundary

15D reuses the exact endpoint and target-selection authority established by 15A and reused by 15B/15C.

```text
explicit Chromium DevTools endpoint
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate metadata read
    ↓
frozen ChromiumPageMetadataEvidence
```

Exactly one page may still be selected implicitly. Multiple page targets still require an exact `target_id`. No browser focus or active-tab heuristic is introduced.

## Transport evidence

`pyxis.browser.read_chromium_page_metadata()` executes one Pyxis-owned fixed expression over the selected page.

It reads only:

```text
document.documentElement.getAttribute('lang')

document.querySelectorAll("link[rel~='canonical' i][href]")
    ↓
DOM order
    ↓
raw authored href
+ browser-resolved href

document.querySelectorAll("meta[name='description' i]")
    ↓
DOM order
    ↓
bounded authored content
+ exact Unicode code-point count
```

Canonical-link and description collections each retain their complete matching count plus an explicit returned-item limit, so collection truncation remains mechanical rather than inferred.

Description counting/slicing uses `Array.from(content)`, preserving the same Unicode code-point semantics used by the earlier browser evidence boundaries.

## Application evidence

`pyxis.app.observe_chromium_page_metadata()` returns immutable `ChromiumPageMetadataEvidence` containing:

```text
endpoint
selected target_id
current page url
literal document_language
language_source
canonical_source
canonical_links
    ordinal
    raw_href
    resolved_href
canonical_link_count
canonical_link_limit
canonical_links_truncated
description_source
descriptions
    ordinal
    content_prefix
    content_character_count
    content_limit
    truncated
description_count
description_limit
descriptions_truncated
```

The raw canonical href and Chromium-resolved href are both retained because they are different observations. Pyxis does not overwrite one with the other.

## What the evidence does not mean

A document `lang` attribute is not proof that the page content is actually written in that language. 15D preserves the authored string exactly and does not normalize or validate it.

A `<link rel="canonical">` declaration is not proof of canonical identity. Multiple or conflicting declarations remain multiple declarations.

A meta description is not a verified abstract, summary, author statement, citation, or destination description. Duplicate or conflicting descriptions remain visible.

Browser resolution of a relative canonical href is an observed browser fact. It does not grant permission to request that URL and does not make the destination authoritative.

## Real-browser proof

The ordinary supported-Python suite now proves four browser evidence families against one disposable real headless Chromium/Chrome page target:

1. 15A bounded rendered page text;
2. 15B bounded DOM-order link choices;
3. 15C bounded literal heading markers;
4. 15D bounded page-declared metadata.

The 15D fixture deliberately contains potentially conflicting evidence:

- authored document language `EN-us`, which remains unnormalized;
- two canonical-link declarations, including an uppercase `CANONICAL` relation;
- two meta-description declarations, including mixed-case `Description` naming;
- a relative first canonical href whose raw form remains `canonical.html` while its browser-resolved form becomes the exact local file URL;
- first description `Study 😀 notes`, returned under a seven-code-point text limit as `Study 😀` while retaining its complete character count.

Under `canonical_link_limit=1` and `description_limit=1`, the application returns one declaration from each collection while preserving complete counts of two and explicit truncation facts. No declaration is selected as authoritative.

Actions #478 on `947962c3aab3301eb245b75bc2f57eaf536d9aa5` exercised the implementation on Python 3.11, 3.12, 3.13, and 3.14. The full suite contains **236 tests**; the inspected Python 3.11 lane passed all 236 and includes the real-browser page/link/heading/metadata integration path.

## Explicit non-goals

15D adds no:

- verified canonical-identity determination;
- language-tag validation or normalization;
- canonical-link conflict resolution;
- meta-description selection or semantic comparison;
- author, publication-date, Open Graph, JSON-LD, schema.org, or citation extraction;
- destination fetching;
- navigation or link following;
- active-tab inference;
- clicks, form submission, scrolling, or viewport ownership;
- target creation or closure;
- arbitrary CDP command API;
- caller-supplied JavaScript;
- persistence;
- provenance scoring;
- source-quality judgment;
- LLM interpretation;
- autonomous research workflow;
- browser UI.

## Decision

D124 establishes: **page-authored metadata may be exposed as bounded immutable research evidence, but declaration is not verification. Pyxis preserves literal language, raw and resolved canonical hrefs, duplicate declarations, conflicts, counts, and truncation facts without silently converting any of them into verified source identity or provenance.**
