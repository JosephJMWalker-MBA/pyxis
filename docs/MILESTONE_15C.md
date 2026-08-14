# Milestone 15C — Read-Only Chromium Heading-Outline Evidence

**Decision D123 — Author-provided heading markers may be exposed as read-only document-structure evidence, but Pyxis does not repair heading levels, infer a semantic tree, summarize sections, or convert outline evidence into navigation authority.**

## Product question

Can Pyxis let a researcher inspect the section markers already encoded by the page author before interpreting the page, while keeping browser state caller-owned and preserving the observation-only authority established by 15A and 15B?

15C answers **yes** with one additional fixed read-only observation.

## Why this capability is earned

15A exposes bounded rendered page text. 15B exposes bounded link choices already present on the same selected page. Those two evidence families still leave one concrete research gap: a long page's rendered text prefix does not tell the researcher which section markers the author actually encoded.

15C addresses only that gap. It does not follow links, scroll, summarize, rank sections, or infer an outline beyond literal `h1` through `h6` facts.

## Boundary

15C reuses the exact endpoint and page-selection authority already established by 15A/15B:

```text
explicit Chromium DevTools endpoint
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate heading read
    ↓
frozen ChromiumPageHeadingsEvidence
```

The application operation imports the existing private target selector. No second active/current-tab heuristic or duplicate selector is introduced.

## Transport evidence

`pyxis.browser.read_chromium_page_headings()` executes one Pyxis-owned fixed expression over the selected page:

```text
document.querySelectorAll('h1,h2,h3,h4,h5,h6')
    ↓
DOM order
    ↓
bounded prefix of matching heading nodes
    ↓
for each returned heading:
    1-based ordinal
    explicit HTML heading level 1–6
    bounded heading.innerText prefix
    exact Unicode code-point count
```

The snapshot also carries the current page URL and complete matching-heading count, so collection truncation is mechanical.

The fixed expression uses `Array.from(text)` for heading-text counting and slicing, preserving the Unicode code-point semantics established by 15A and reused by 15B.

## Application evidence

`pyxis.app.observe_chromium_page_headings()` returns:

```text
ChromiumPageHeadingsEvidence
├── endpoint
├── target_id
├── url
├── source = document.querySelectorAll('h1,h2,h3,h4,h5,h6')
├── headings
│   └── ChromiumPageHeadingEvidence
│       ├── ordinal
│       ├── level
│       ├── text_prefix
│       ├── text_character_count
│       ├── text_limit
│       └── truncated
├── heading_count
├── heading_limit
└── truncated
```

The evidence is frozen. Transport and application validation require contiguous returned DOM ordinals, levels in the literal HTML range 1–6, bounded text prefixes, and coherent counts.

## What the evidence does not mean

A heading level is the HTML level the page encoded. It is not a Pyxis quality judgment.

DOM order is document order only. It is not importance or relevance.

A sequence such as:

```text
h1 → h4
```

remains exactly `1 → 4`. Pyxis does not repair it to `1 → 2`, classify it as an accessibility error, or infer missing hierarchy nodes.

Heading text is page evidence. Pyxis does not treat it as a verified summary of the section that follows.

Collection truncation means only that the explicit heading limit was smaller than the observed matching-heading count.

## Real-browser proof

The ordinary supported-Python suite now proves three independent read-only observation families against the same disposable real headless Chromium/Chrome target:

1. 15A reads URL/title/bounded rendered page text.
2. 15B reads bounded DOM-order link evidence.
3. 15C reads three literal heading markers encoded as `h1`, `h3`, and `h6`, while returning only the first two under `heading_limit=2`.
4. The first heading `Intro 😀 section` is bounded to `Intro 😀` under `heading_text_limit=7` while retaining its complete Unicode code-point count.
5. The second returned heading remains level 3; Pyxis does not convert the observed `h1 → h3` sequence into a synthesized hierarchy.
6. The third `h6` is not returned, while `heading_count=3` and collection `truncated=True` preserve that fact.

Actions #465 on `05e19a3516972ffaf3b8b7f692cffe42d465e4e5` passed Python 3.11, 3.12, 3.13, and 3.14. The full suite contains **231 tests**, including the real-browser integration path.

## Explicit non-goals

15C adds no:

- navigation or link following;
- scrolling or viewport ownership;
- active-tab inference;
- clicks or form submission;
- target creation or closure;
- arbitrary CDP command API;
- caller-supplied JavaScript;
- semantic document-tree inference;
- heading-level repair;
- accessibility conformance judgment;
- section ranking or recommendation;
- section summarization;
- ARIA landmark extraction;
- destination fetching;
- persistence;
- LLM interpretation;
- autonomous research workflow;
- browser UI.

## Decision

D123 establishes: **literal author-provided heading markers are valid read-only research evidence. Pyxis may expose bounded DOM-order h1–h6 facts from one explicitly selected existing Chromium page, but the encoded levels remain observations rather than a repaired hierarchy, summary, quality score, or control surface.**
