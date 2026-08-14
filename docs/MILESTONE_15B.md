# Milestone 15B — Read-Only Chromium Link Evidence

**Decision D122 — Observing navigation choices does not grant navigation authority. Pyxis may acquire bounded DOM-order link evidence from one explicitly addressable existing Chromium page, but it does not rank, classify, select, or follow those links.**

## Product question

Can Pyxis show a researcher the navigation choices already present on an observed page as typed, immutable evidence without taking authority to follow any of them?

15B answers **yes** with a second deliberately narrow read-only observation.

## Boundary

15B reuses the exact browser endpoint and target-selection authority established by 15A.

```text
explicit Chromium DevTools endpoint
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate link read
    ↓
frozen ChromiumPageLinksEvidence
```

No second target-selection implementation is introduced. Exactly one page may still be selected implicitly; multiple page targets still require an exact `target_id`.

## Transport evidence

`pyxis.browser.read_chromium_page_links()` executes one Pyxis-owned fixed expression over the selected page:

```text
document.querySelectorAll('a[href]')
    ↓
DOM order
    ↓
bounded prefix of link nodes
    ↓
for each returned link:
    1-based ordinal
    browser-resolved link.href
    bounded link.innerText prefix
    exact Unicode code-point count
```

The snapshot also carries the current page URL and the complete count of matching `a[href]` nodes, so collection truncation is mechanical rather than inferred.

The fixed expression uses `Array.from(text)` for anchor-text counting and slicing, preserving the Unicode code-point semantics already established by 15A.

## Application evidence

`pyxis.app.observe_chromium_page_links()` returns:

```text
ChromiumPageLinksEvidence
├── endpoint
├── target_id
├── url
├── source = document.querySelectorAll('a[href]')
├── links
│   └── ChromiumPageLinkEvidence
│       ├── ordinal
│       ├── href
│       ├── text_prefix
│       ├── text_character_count
│       ├── text_limit
│       └── truncated
├── link_count
├── link_limit
└── truncated
```

The application layer preserves browser-resolved href values exactly as observed. A `mailto:` or `javascript:` value is not silently promoted, rejected, classified, or normalized into a navigation recommendation.

## What the evidence does not mean

DOM order is evidence of document order only. It is not relevance, importance, safety, quality, recommendation, or intent.

A resolved `href` is evidence of what the browser exposes for that anchor. It is not authorization to request the resource.

Anchor text is evidence from the page. Pyxis does not infer that the text accurately describes the destination.

Collection truncation means only that the explicit link limit was smaller than the observed matching-link count.

## Real-browser proof

The ordinary supported-Python suite now proves both browser observations against one disposable real headless Chromium/Chrome target:

1. 15A reads the page URL, title, and bounded rendered-text evidence.
2. 15B reads three existing anchor choices from the same target, returning only the first two under an explicit `link_limit=2`.
3. The first relative href is verified as the browser-resolved file URL.
4. The `mailto:` href is preserved unchanged.
5. Unicode anchor text is bounded and counted in code points.
6. The third link is not returned, while `link_count=3` and collection `truncated=True` preserve that fact.

An intermediate integration attempt passed two fixture URLs to browser startup so 15A and 15B could use separate pages. On Actions #451, both installed Chromium-family binaries exited with code 13 before publishing DevTools on Python 3.11. The new application and transport link tests themselves passed; the failing path never reached Pyxis DevTools acquisition.

The harness was simplified instead of adding recovery behavior to production: one explicit fixture page now contains both the rendered text and links. Production still performs one target-list read plus one fixed link read and has no browser-launch, navigation, tab-creation, or hidden retry authority.

Actions #452 on `0f4fe856553f22983bc72bbfe5f973f20e42ab4e` passed Python 3.11, 3.12, 3.13, and 3.14. The full suite contains **226 tests** and the real-browser integration path is part of that ordinary suite.

## Explicit non-goals

15B adds no:

- navigation or link following;
- active-tab inference;
- clicks or form submission;
- target creation or closure;
- arbitrary CDP command API;
- caller-supplied JavaScript;
- link ranking or recommendation;
- link relevance scoring;
- scheme allow/deny policy;
- destination safety classification;
- deduplication or canonicalization;
- HTTP fetching outside the existing page;
- browser/page/link persistence;
- LLM interpretation;
- autonomous research workflow;
- browser UI.

## Decision

D122 establishes: **read-only evidence about available navigation choices is still observation, not control. Pyxis may expose bounded DOM-order link facts from an explicitly selected existing Chromium page, while selection of a destination and any act of navigation remain outside the authority of this milestone.**
