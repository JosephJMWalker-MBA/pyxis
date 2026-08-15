# Pyxis

Pyxis turns software architecture into executable, inspectable systems—connecting human intent to generated code through a transparent compiler, with measurable consequences and portable output.

## Current focus

Repository Zero has a permanent evidence-bearing vertical slice:

```text
Create Workspace
      ↓
Canonical authoring state
      ↓
RIR
      ↓
Compiler
      ↓
Generated Workspace
      ↓
Run
      ↓
Preview architectural change
      ↓
Trace proposed architectural consequences
      ↓
Record rationale + append-only revision
      ↓
Incremental recompilation
      ↓
Run changed Workspace
      ↓
Reconcile proposed consequences with observed evidence
      ↓
Export exact compiler products
      ↓
Verify provenance + runtime behavior
      ↓
Conventional portable source repository
      ↓
Verified wheel
      ↓
Fresh offline installation + execution
```

The first local Textual Workspace UI consumes those application boundaries rather than recreating them. Repository Zero also has a descriptive measurement path over the established build/run operation, with exact subject/workload/environment/work provenance, read-only summary presentation, and live Workspace/RIR provenance rules through Milestone 11T. Two concrete architecture operations prove both additive and subtractive governed edits, with only demonstrated invariant orchestration shared privately. Milestone 13A adds a preview-only architecture consequence trace that connects requested change → proposed canonical state → proposed RIR → compiler-product consequences → runtime-contract consequences using only already-owned preview evidence. Milestone 13B keeps that proposal intact after Apply and reconciles it with a separate observed record built only from the resulting revision, compiler-generation, RIR, and runtime evidence. Milestone 14A bounds the package support contract to Python 3.11–3.14 and proves the complete Repository Zero suite independently on every supported interpreter lane.

Milestone 15A returns Pyxis to its original browser/research purpose without changing that proven compiler spine. Chromium remains Chromium and remains caller-owned. Given an explicit Chromium DevTools endpoint, Pyxis can observe one existing page through a concrete read-only boundary and return frozen URL/title/bounded rendered-text evidence. If more than one page exists, target selection must be explicit rather than inferred from browser ordering or focus heuristics.

Milestone 15B adds a second read-only research fact without adding browser control: Pyxis can expose bounded DOM-order link choices already present on that selected page. It preserves browser-resolved href values, bounded anchor text, exact Unicode counts, and collection truncation evidence while refusing to rank, classify, select, or follow any link.

Milestone 15C adds literal page-outline evidence without interpretation: Pyxis can expose bounded DOM-order `h1`–`h6` markers with their explicit HTML levels and bounded text. Skipped levels remain skipped; Pyxis does not repair them into a synthesized hierarchy, summarize sections, or turn outline evidence into navigation authority.

Milestone 15D adds page-declared metadata without promoting declaration into provenance truth: Pyxis can expose the authored document-language string, bounded canonical-link declarations with both raw and browser-resolved hrefs, and bounded meta-description declarations. Duplicate or conflicting declarations remain visible instead of being silently resolved.

Milestone 15E adds literal paragraph-level passage evidence without semantic segmentation: Pyxis can expose bounded DOM-order `<p>` elements with authored IDs and exact Unicode counts. Duplicate or empty IDs remain exactly as authored and are not promoted into stable citation locators.

Milestone 15F adds literal HTML-table structure evidence without normalizing it into a dataset: Pyxis can expose bounded DOM-order tables, captions, rows, direct `TH`/`TD` cells, browser-exposed row/column spans, and exact counts. Spans remain spans; Pyxis does not synthesize grid cells, infer header relationships, coerce value types, flatten tables into CSV-like rows, or rank tables.

Milestone 15G adds literal ordered/unordered list evidence without flattening or semantic repair: Pyxis can expose bounded global DOM-order `OL`/`UL` records, direct `LI` children, raw authored `start`/`value` attributes, and mechanical parent-list/item ordinals for nested lists. Parent-item direct text excludes descendant-list text so nested structure remains separate evidence; Pyxis does not repair numbering or turn DOM nesting into conceptual hierarchy.

The first demonstrator remains intentionally small so each transformation can be inspected end to end.

## Core principles

- Human intent should remain visible in the implementation path.
- Canonical source is authoritative; generated files are compiler products.
- Architectural changes are previewed before mutation.
- Proposed architecture evidence and observed post-Apply evidence remain distinct.
- Revisions are append-only and carry rationale.
- Incremental generation is based on compiler evidence, not filesystem inference.
- Export packages existing compiler output rather than regenerating it.
- READY is derived from verification evidence.
- Presentation and UI render application-owned evidence rather than rediscovering product state.
- Measurement observes established operations and remains descriptive rather than causal.
- Chromium should remain Chromium; Pyxis should compose with mature browser infrastructure rather than rebuild it.
- Browser state remains caller-owned unless a later explicit capability earns narrower control authority.
- Read-only browser evidence should remain distinct from navigation, automation, and interpretation.
- Available link choices are evidence, not navigation recommendations or permissions.
- Heading levels are page-authored evidence, not a Pyxis-repaired semantic hierarchy.
- Page-declared metadata is evidence of declaration, not verified provenance or source identity.
- Paragraph boundaries and authored IDs are page-authored evidence, not Pyxis citation authority or semantic segmentation.
- HTML table structure is evidence; normalized datasets, header relationships, span expansion, and typed values require separate authority.
- Ordered/unordered list identity, authored numbering attributes, and DOM nesting are structure evidence, not corrected numbering or semantic hierarchy.
- Package compatibility claims should be bounded by interpreter versions proven in CI.
- Portable output should look like a conventional Python repository.
- The smallest demonstrator should remain understandable end to end.
- Pyxis should leave users better Python programmers by making the transformation from architecture to code inspectable.

## Chromium observation

Milestone 15A establishes the first concrete browser-facing application seam:

```text
explicit Chromium DevTools endpoint
      ↓
read existing page targets
      ↓
exact page selection
      ↓
one fixed read-only page observation
      ↓
frozen application evidence
```

`observe_chromium_page()` returns the selected target ID, current URL, current title, and a bounded prefix of `document.body.innerText` with an exact Unicode code-point count and truncation fact.

Milestone 15B reuses that same endpoint and target-selection authority for a separate fixed link read:

```text
selected existing page
      ↓
document.querySelectorAll('a[href]')
      ↓
bounded DOM-order link evidence
      ↓
resolved href + bounded innerText + exact counts
```

`observe_chromium_page_links()` returns the page URL, complete matching-link count, explicit link limit, and a frozen tuple of 1-based DOM-order link records. It preserves observed href values such as `mailto:` without adding scheme policy, ranking, recommendation, or destination selection.

Milestone 15C reuses the same page-selection authority for one fixed heading read:

```text
selected existing page
      ↓
document.querySelectorAll('h1,h2,h3,h4,h5,h6')
      ↓
bounded DOM-order heading evidence
      ↓
explicit level + bounded innerText + exact counts
```

`observe_chromium_page_headings()` returns the page URL, complete matching-heading count, explicit heading limit, and a frozen tuple of heading records. Each record preserves the literal HTML level from 1 through 6. A sequence such as `h1 → h4` remains `1 → 4`; Pyxis adds no missing hierarchy, quality judgment, or section summary.

Milestone 15D reuses the same page-selection authority for one fixed metadata read:

```text
selected existing page
      ↓
authored document lang
+ canonical-link declarations
+ meta-description declarations
      ↓
bounded immutable declaration evidence
```

`observe_chromium_page_metadata()` preserves the literal document `lang` attribute, every returned canonical declaration's raw authored href alongside Chromium's resolved href, and bounded description content with exact Unicode counts. Complete declaration counts and explicit collection limits preserve truncation mechanically. Multiple or conflicting declarations are not collapsed into one canonical identity or one authoritative description.

Milestone 15E adds a separate fixed paragraph read:

```text
selected existing page
      ↓
document.querySelectorAll('p')
      ↓
bounded DOM-order paragraph evidence
      ↓
authored id + bounded innerText + exact counts
```

`observe_chromium_page_paragraphs()` returns the page URL, complete paragraph count, explicit paragraph limit, and a frozen tuple of paragraph records. Each record preserves the authored `id` string exactly as present, including duplicates or empty values. The operation does not split sentences, merge paragraphs, rank passages, verify quotations, or treat IDs as stable citation keys.

Milestone 15F adds a separate fixed table-structure read:

```text
selected existing page
      ↓
document.querySelectorAll('table')
      ↓
bounded table → row → direct TH/TD cell evidence
      ↓
literal tags + spans + bounded innerText + exact counts
```

`observe_chromium_page_tables()` returns the page URL, complete table count, explicit table limit, and frozen nested table evidence. Each returned table preserves a bounded direct caption, complete row count, and bounded row prefix; each returned row preserves a complete direct-cell count and bounded cell prefix; each returned cell preserves literal `TH`/`TD`, browser-exposed `rowSpan`/`colSpan`, bounded rendered text, and exact Unicode counts. Descendant rows belonging to a nested table are excluded from the outer table's row evidence. The operation does not expand spans, infer header mappings, normalize a rectangular grid, coerce values, or flatten the structure into a dataset.

Milestone 15G adds a separate fixed list-structure read:

```text
selected existing page
      ↓
document.querySelectorAll('ol,ul')
      ↓
bounded global DOM-order list evidence
      ↓
literal OL/UL + direct LI children + authored attributes
      ↓
mechanical parent-list/item coordinates
```

`observe_chromium_page_lists()` returns the page URL, complete matching-list count, explicit list limit, and frozen list evidence. Each list preserves literal `OL`/`UL`, the raw authored `start` attribute, its direct `LI` count/prefix, and—when nested—the nearest ancestor-list ordinal plus direct parent-item ordinal. Each item preserves its raw authored `value` attribute and bounded direct-list text with exact Unicode counts. Direct-list text excludes descendant `OL`/`UL` text so nested content is not silently flattened into its parent item. The operation does not compute displayed numbering, validate or repair attributes, flatten nesting, or infer a semantic outline.

These boundaries do **not** navigate, activate tabs, click, submit forms, create or close targets, accept arbitrary DevTools commands or user JavaScript, persist browser state, invoke an LLM, rank links/sections/passages/tables/lists, repair document structure or list numbering, resolve provenance conflicts, verify quotations, normalize tables, infer header relationships, expand spans, coerce values, flatten nested lists, infer semantic hierarchy, or add autonomous research behavior. The optional `browser` dependency provides the concrete WebSocket transport; Pyxis core does not require a browser dependency.

## Portable output

Repository Zero defines one portable deliverable with two complementary forms:

```text
conventional source repository + verified wheel
```

The source repository preserves the exact compiler products, provenance evidence, and conventional Python package structure. The verified wheel is checked against that source/manifest evidence and is the artifact covered by Pyxis's offline portability guarantee.

The verified wheel has been proven to install and execute in a fresh environment with network access blocked, without Pyxis participating, while reproducing the already-verified Workspace behavior.

Raw source-to-wheel construction remains conventional PEP 517 packaging and may require declared build dependencies to be obtainable. Pyxis does not require the raw source repository to rebuild its wheel while offline.

## Python support

Pyxis currently declares:

```text
Python >=3.11,<3.15
```

The same full test suite is exercised in CI on Python 3.11, 3.12, 3.13, and 3.14. Future interpreter lines are not implicitly supported by open-ended package metadata; the supported range expands only after a new lane is deliberately added and proven.

## Repository Zero

The permanent implementation is organized around explicit boundaries under `src/pyxis/`, including:

```text
src/pyxis/
├── authoring/
├── rir/
├── compiler/
├── runtime/
├── revisions/
├── exporting/
├── browser/
└── app/
```

The permanent reference example is `examples/text_lab/`.

## Project continuity

Start with [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) for the current map through Milestone 15G / D127.

The repository also keeps three complementary detailed records so future development does not depend on chat history:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — architectural boundaries and detailed evolution
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — normative implementation decisions
- [`docs/DEVELOPMENT_ARCHIVE.md`](docs/DEVELOPMENT_ARCHIVE.md) — development history, learned logic, prototype lessons, current gaps, and foreseeable implementation path

Later milestone documents remain the narrow proof trail for changes not safely foldable into the large central files through the current GitHub connector.

## Status

Pyxis is proven through Milestone 15G / D127: Repository Zero retains the compiler/runtime/revision/export lifecycle, interactive evidence UI, descriptive measurement pipeline, live measurement provenance/invalidation/re-entry path, two concrete governed architecture operations, shared private architecture orchestration, preview-only architecture consequence trace, distinct post-Apply proposed-vs-observed reconciliation, and bounded Python 3.11–3.14 release contract. The browser-facing product now has seven real read-only evidence boundaries over explicitly addressable existing Chromium pages: bounded page-content observation, bounded DOM-order link-choice observation, bounded literal heading-outline observation, bounded page-declared metadata observation, bounded literal paragraph passage observation, bounded literal HTML-table structure observation, and bounded literal ordered/unordered-list structure observation.

Do not add another statistic, abstraction, score, explanatory layer, compatibility lane, provenance resolver, citation resolver, dataset normalizer, semantic list interpreter, or browser-control surface merely because the current architecture makes one possible. The next implementation milestone should answer a new concrete product question. Verified source identity, quotation verification, citation stability, table normalization/header inference/span expansion/value typing, list-number repair/semantic hierarchy, navigation, interaction, permissions, persistence, research workflows, semantic interpretation, and browser UI each require their own evidence before they are allowed to grow from the current observation boundaries.
