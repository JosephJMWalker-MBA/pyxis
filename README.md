# Pyxis

Pyxis is an **evidence-first Python research system** with two proven, connected spines:

1. a transparent architecture-to-code compiler/runtime that keeps human intent, canonical state, generated products, runtime evidence, revisions, and export boundaries inspectable; and
2. a read-only Chromium research workflow that preserves observation, human selection, comparison, rationale, and revision history without silently promoting any layer into stronger authority.

## Current status — through Milestone 43E / D217

Pyxis currently proves:

- **Architecture → code → runtime → portable output:** canonical Workspace authoring, RIR, deterministic compilation, generated Workspace execution, governed architecture preview/Apply, append-only revision evidence, incremental recompilation, proposed-vs-observed consequence reconciliation, export verification, conventional source output, and a verified wheel path.
- **Evidence-preserving UI and measurement:** a Textual Workspace shell renders application-owned evidence; descriptive measurement remains provenance-heavy and explicitly non-causal.
- **Read-only Chromium research:** caller-owned Chromium pages can be observed through an explicit DevTools endpoint for bounded page text, links, headings, metadata, paragraphs, tables, and lists. Pyxis does not infer an active tab when multiple pages exist and does not acquire navigation or interaction authority from observation capability.
- **Durable research evidence:** browser evidence can be composed into durable verified captures, reopened after Chromium exits, and used for explicit human selections, notes, comparisons, working sets, and rationale without silently promoting interpretation into source authority.
- **Governed durable research continuity:** explicit revision segments can be inspected, revised, persisted, adopted, checkpointed, exited, and freshly re-entered from caller-supplied durable locators without ambient history discovery or a global latest/current/head model.
- **Changed evidence-basis ancestry:** three distinct evidence-basis roots can be retained through explicit transition/root machinery. The concrete third epoch now has persisted Textual launch, first and repeatable cumulative checkpointing, explicit in-process handoff, and fresh re-entry while retaining one direct 40B ancestry anchor and freshly re-earning first-, second-, and third-root ancestry.
- **Inspection without authority promotion:** second- and third-epoch launch provenance remain distinct from mutable current governed state through application-owned read-only projections. Both persisted families can emit deterministic `pyxis research-inspect` JSON without turning paths, hashes, or presentation into stronger authority; exact in-process handoffs do not invent persistent launch paths.
- **Bounded cumulative reuse:** root-backed, second-epoch, and third-epoch continuation share only triply-proven private mechanics for fixed-anchor cumulative extension, checkpoint forms, explicit path submission, rollover gating, and visible post-proof promotion. Concrete persistence, ancestry proof, launch lineage, and root/epoch semantics remain concrete rather than becoming a generic `epoch[n]` model.
- **Bounded compatibility:** package metadata declares Python `>=3.11,<3.15`, and the supported lanes are exercised across Python 3.11, 3.12, 3.13, and 3.14.

The detailed narrative below remains the original central proof trail through **Milestone 18C / D137** and is intentionally preserved rather than rewritten wholesale. For current orientation, continue through [`docs/CURRENT_FRONTIER.md`](docs/CURRENT_FRONTIER.md), [`docs/CURRENT_FRONTIER_35_36.md`](docs/CURRENT_FRONTIER_35_36.md), [`docs/CURRENT_FRONTIER_37_38.md`](docs/CURRENT_FRONTIER_37_38.md), [`docs/CURRENT_FRONTIER_39_40.md`](docs/CURRENT_FRONTIER_39_40.md), and [`docs/CURRENT_FRONTIER_41_43.md`](docs/CURRENT_FRONTIER_41_43.md). Milestone-specific records, implementation, tests, and executed CI remain stronger authority than any compact summary.

## Authority boundaries

Pyxis deliberately does **not** treat implementation convenience as authority. In particular:

- generated code is not a second canonical source;
- proposed architecture evidence is not observed post-Apply evidence;
- descriptive timing is not causal performance evidence;
- DOM order is not relevance or recommendation;
- page-declared metadata is not verified provenance;
- SHA-256 self-integrity is not authentication, authorship, or trusted time;
- researcher selection is provenance about human choice, not truth, quotation, or citation proof;
- human notes and comparisons are interpretation attached to evidence, not source evidence themselves;
- durable reference matching is not source discovery or chain-of-custody proof;
- exact-text differences are not semantic differences;
- a loaded revision edge is not a globally validated history, current head, or linear-chain authority; and
- read-only browser observation does not imply navigation, interaction, autonomous research, or arbitrary DevTools authority.

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

Milestone 15F adds literal HTML-table structure evidence without normalizing it into a dataset: Pyxis can expose bounded DOM-order tables, captions, rows, direct `TH`/`TD` cells, browser-exposed row/column spans, and exact counts. Spans remain spans; Pyxis does not synthesize grid cells, infer header relationships, coerce values, flatten tables into CSV-like rows, or rank tables.

Milestone 15G adds literal ordered/unordered list evidence without flattening or semantic repair: Pyxis can expose bounded global DOM-order `OL`/`UL` records, direct `LI` children, raw authored `start`/`value` attributes, and mechanical parent-list/item ordinals for nested lists. Parent-item direct text excludes descendant-list text so nested structure remains separate evidence; Pyxis does not repair numbering or turn DOM nesting into conceptual hierarchy.

Milestone 16A composes those seven proven evidence families into one immutable research-page bundle without inventing an atomic browser snapshot. The first read selects the page under existing rules; the next six reuse that exact target ID. Every member must retain the same endpoint, target, and URL, while the bundle explicitly records that acquisition is sequential and non-atomic.

Milestone 16B persists one already-observed 16A bundle as deterministic no-overwrite JSON with explicit SHA-256 integrity evidence. Saving never re-reads Chromium, and verification checks only the durable file contract; the checksum is not authentication, verified provenance, or a trusted timestamp.

Milestone 16C reopens one verified 16B capture as typed application evidence only after exact nested structural/domain validation and lossless reconstruction. The load result retains the exact file-verification evidence beside a newly reconstructed bundle, so durable evidence can outlive Chromium without masquerading as a fresh browser observation.

Milestone 17A adds the first explicit researcher-owned action over that durable evidence: the caller may select one already-returned paragraph by exact ordinal. The frozen selection retains the exact loaded-capture object and exact paragraph object, refuses evidence outside a bounded returned prefix, and does not turn human choice into relevance, quotation, citation, truth, or source-authenticity authority.

Milestone 17B lets the caller attach one exact human-authored note to one exact 17A selection. The immutable note record retains the exact selection object and caller text verbatim while keeping human interpretation visibly separate from page/source evidence; it adds no inferred author, timestamp, claim support, truth, relevance, citation, or machine-interpretation authority.

Milestone 17C makes that one 17B note durable without copying the source evidence. A deterministic no-overwrite sidecar stores only the source capture format + bundle SHA-256, explicit paragraph ordinal/selection mode, and exact note mode/verbatim caller text. Its digest covers the complete attachment record but remains self-integrity only; note verification does not reopen or relink the source capture.

Milestone 17D reopens that durable human action only against one explicit caller-supplied 16C capture. Pyxis freshly verifies the sidecar, matches its capture format + bundle SHA-256 to the exact 16B verification evidence retained by the supplied capture, and then reconstructs the existing 17A selection and 17B note. Source path does not control identity, bounded evidence is not expanded, and digest agreement remains reference matching rather than authentication.

Milestone 18A begins a finer human-selection phase without changing source authority: the caller may refine one exact 17A paragraph selection to one non-empty zero-based half-open Unicode code-point range wholly inside the already-returned paragraph `text_prefix`. The result retains the exact 17A selection and stores only coordinates; `selected_text` is derived from the source rather than copied into a second representation. Truncated/unreturned characters remain unreachable, and exact range choice is not quotation verification, citation authority, relevance, truth, or source authentication.

Milestone 18B lets the caller attach one exact human-authored note to one exact 18A text-range selection. The note retains the exact range object and caller text verbatim, reuses 18A to re-establish parent/range validity rather than creating a second validator, and does not decide whether the selected source characters are meaningful. Human interpretation remains distinct from page/source evidence and gains no relevance, truth, claim-support, quotation/citation, authorship, temporal, provenance, or machine-interpretation authority.

Milestone 18C makes that exact-range human note durable without storing selected source text. A deterministic no-overwrite sidecar stores only the established source-capture content identity, the paragraph selection mode/ordinal, the exact Unicode range mode/unit/start/end coordinates, and the exact note mode/verbatim text. Persistence reuses 18B/18A validation; file-only verification proves canonical structure and SHA-256 self-integrity but deliberately does not prove the recorded coordinates address a source capture it did not read.

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
- Sequential composition of browser evidence must not be relabeled as one atomic DOM snapshot.
- Persisting browser evidence must preserve already-acquired facts rather than reacquire, reinterpret, authenticate, or strengthen them.
- Rehydrated durable evidence must retain the verification evidence that authorized reopening; reconstructing types must not erase acquisition origin.
- Explicit researcher selection must point to existing evidence and preserve its limits; human choice is provenance, not relevance or truth proof.
- Caller-authored notes may reference exact selected evidence, but human interpretation remains distinct from page/source evidence and must not be silently promoted into a claim about the source.
- Durable human-note persistence should reference already-durable source content rather than copy browser evidence into a second representation; its checksum is integrity, not authorship.
- Durable note relinking must be explicit against a caller-supplied loaded capture; content-digest agreement is reference matching, not discovery, authentication, truth, or permission to expand bounded evidence.
- Exact text-range selection should retain parent evidence plus explicit coordinates; derived selected text is not a second source representation or verified quotation.
- Human notes over exact text ranges should retain the exact range object and reuse range validation; attaching interpretation does not promote the range or note into source truth.
- Durable exact-range notes should persist source-content identity plus explicit coordinates, never copied selected text; file integrity does not prove those coordinates address an unread source.
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

`observe_chromium_page_headings()` returns the page URL, complete matching-heading count, explicit heading limit, and a frozen tuple of heading records. Each record preserves the literal HTML level from 1 through 6. A sequence such as `h1 → h4` remains exactly `1 → 4`; Pyxis adds no missing hierarchy, quality judgment, or section summary.

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

Milestone 16A adds an application-level composition over those seven existing observers:

```text
page
  ↓
links
  ↓
headings
  ↓
metadata
  ↓
paragraphs
  ↓
tables
  ↓
lists
  ↓
exact endpoint + target + URL coherence
  ↓
ChromiumPageResearchEvidenceBundle
```

`observe_chromium_page_research_bundle()` performs no new CDP operation. The first page observation selects one exact existing target; every later observer receives that target ID explicitly. The bundle retains the seven constituent evidence objects unchanged, records the fixed acquisition order, and records `acquisition_mode="sequential_non_atomic_url_coherent"`. A changed endpoint, target, or URL aborts acquisition and emits no bundle. Same-URL DOM mutation remains possible, so URL agreement is a coherence gate rather than proof of one frozen DOM state. 16A adds no bundle-wide limit policy; each constituent observer keeps its established bounded defaults.

Milestone 16B adds one persistence boundary downstream of that completed bundle:

```text
ChromiumPageResearchEvidenceBundle
      ↓
validate established 16A coherence
      ↓
complete deterministic bundle JSON
      ↓
SHA-256 over canonical bundle bytes
      ↓
exclusive-create caller-chosen capture file
      ↓
later canonical-byte + digest verification
```

`persist_chromium_page_research_capture()` never observes Chromium. It requires the established 16A acquisition mode/order and exact endpoint/target/URL coherence, then writes the complete bundle payload into format `pyxis.chromium.research_capture.v1`. The destination parent must already exist and the destination itself must not; existing files are never overwritten. `verify_chromium_page_research_capture()` later checks UTF-8/JSON shape, supported format, persisted acquisition identity, exact member coherence, the bundle SHA-256, and exact canonical JSON bytes without reconnecting to the page or constructing a new typed bundle. The checksum is self-integrity evidence only: an actor able to rewrite both payload and digest can create another self-consistent file, so 16B does not claim authentication or verified provenance. No timestamp is added because persistence time would not represent the seven sequential browser-read moments.

Milestone 16C adds a distinct typed reopening boundary after 16B verification:

```text
verified 16B capture
      ↓
exact nested JSON type reconstruction
      ↓
full application evidence validation
      ↓
lossless typed reconstruction
      ↓
verification evidence + reconstructed bundle
```

`load_chromium_page_research_capture()` first invokes the existing 16B verifier and then validates the complete nested evidence contract before constructing a new immutable `ChromiumPageResearchEvidenceBundle`. Exact JSON types, field sets, source strings, ordinals, counts, limits, truncation relationships, table/list structural constraints, and bundle coherence must all survive. A capture can therefore have a recomputed self-consistent SHA-256 and still be rejected as invalid typed evidence. The public `ChromiumPageResearchLoadedCaptureEvidence` retains the exact 16B verification object beside the reconstructed bundle, and a final round-trip check proves reconstruction did not normalize or discard persisted evidence. The real-browser acceptance path terminates Chromium before reopening the capture, proving that durable typed evidence can re-enter the application without browser reacquisition.

Milestone 17A adds one explicit human-owned selection boundary downstream of 16C:

```text
ChromiumPageResearchLoadedCaptureEvidence
      ↓
caller supplies exact paragraph ordinal
      ↓
selection-relevant origin + paragraph coherence
      ↓
require paragraph already present in bounded returned evidence
      ↓
exact source object + exact paragraph object
      ↓
ChromiumPageResearchParagraphSelectionEvidence
```

`select_chromium_research_capture_paragraph()` never chooses a paragraph. The caller supplies one exact 1-based DOM ordinal. The result records `selection_mode="caller_explicit_returned_paragraph_ordinal"`, retains the exact supplied loaded-capture object, and retains the exact selected `ChromiumPageParagraphEvidence` object already inside that source. Duplicate authored IDs do not affect ordinal choice. If a paragraph is known only through a larger `paragraph_count` because the returned collection was truncated, selection refuses it rather than reconnecting to Chromium, rereading the capture file, enlarging a prior limit, or synthesizing missing text. Selection is therefore caller-choice provenance only; it is not relevance, factual correctness, quotation validity, citation authority, locator stability, source authenticity, or semantic-passage proof.

Milestone 17B adds one explicit human-authored note boundary downstream of 17A:

```text
ChromiumPageResearchParagraphSelectionEvidence
      ↓
caller supplies one exact nonblank note string
      ↓
validate selection mode + exact paragraph object identity
      ↓
preserve caller text verbatim
      ↓
ChromiumPageResearchParagraphNoteRecord
```

`create_chromium_research_paragraph_note()` is pure application logic. It retains the exact supplied 17A selection object and stores the caller's string without trimming or normalization; whitespace stripping is used only to refuse an all-whitespace non-note. The selected paragraph must still be the exact object by identity at its ordinal inside the exact loaded-capture source. An equal-by-value paragraph copy is rejected. The result is deliberately called a `NoteRecord`, not page evidence: it records human interpretation attached to selected evidence, not a statement that the page proves the note. 17B adds no author identity, timestamp, tag, note type, relevance, confidence, claim-support semantics, quotation/citation authority, or machine interpretation.

Milestone 17C adds one durable sidecar boundary downstream of 17B:

```text
ChromiumPageResearchParagraphNoteRecord
      ↓
source capture format + bundle SHA-256
+ paragraph ordinal / selection mode
+ note mode / verbatim note text
      ↓
canonical deterministic JSON
      ↓
SHA-256 over complete attachment record
      ↓
exclusive-create human-note sidecar
```

`persist_chromium_research_paragraph_note()` does not serialize the 17B object graph. The sidecar format `pyxis.chromium.research_paragraph_note.v1` stores only the already-durable source capture content reference, the exact paragraph ordinal/selection mode, and the note mode/text. Page URL, endpoint, target ID, paragraph text, source file path, and the complete capture remain absent. Runtime persistence evidence retains the exact supplied 17B note object, while the on-disk identity changes honestly from Python object identity to durable source-content identity.

`verify_chromium_research_paragraph_note()` reads only the sidecar and checks its exact shape, modes, source bundle-digest shape, positive paragraph ordinal, nonblank verbatim note text, recorded SHA-256, and canonical bytes. It does not locate, read, verify, or rehydrate the referenced capture and therefore does not recreate a 17A selection or 17B note object. The sidecar checksum is self-integrity only: an actor able to rewrite the payload and digest can create another self-consistent sidecar, so 17C adds no authorship or authentication authority.

Milestone 17D adds one explicit relinking boundary downstream of 17C:

```text
caller-supplied 16C loaded capture
+ caller-supplied 17C sidecar path
      ↓
fresh sidecar verification
      ↓
exact capture format + bundle SHA-256 match
      ↓
existing 17A selection
      ↓
existing 17B note creation
      ↓
verification evidence + reconstructed human note
```

`load_chromium_research_paragraph_note()` always re-verifies the sidecar from disk rather than accepting a caller-constructed verification object as proof. It compares the verified sidecar reference only with the exact 16B verification evidence retained by the supplied 16C capture. It does not search for a source file or recompute capture identity from the typed bundle. After the match, reconstruction delegates to the established public selector and note constructor, so the resulting note retains the exact supplied loaded-capture object and exact already-returned paragraph object. A different source path with the same durable content identity is acceptable; a different bundle digest is not. A sidecar ordinal outside the supplied capture's bounded returned paragraph prefix remains unavailable and is never reacquired.

Milestone 18A adds one exact text-range refinement boundary downstream of 17A:

```text
ChromiumPageResearchParagraphSelectionEvidence
      ↓
caller supplies start_offset + end_offset
      ↓
zero-based half-open Unicode code-point range
      ↓
require range wholly inside returned text_prefix
      ↓
exact parent selection + coordinates
      ↓
derived selected_text
```

`select_chromium_research_paragraph_text()` retains the exact supplied 17A selection and records `offset_unit="unicode_code_point"`. It stores no copied selected-text field; `selected_text` is derived from the exact parent paragraph evidence at the recorded coordinates. The operation rejects bool-as-int coordinates, empty/reversed/negative ranges, equal-by-value replacement of the source paragraph, and every coordinate outside the already-returned text prefix. A truncated paragraph may have its complete returned prefix selected, but its unreturned suffix remains unavailable even when `text_character_count` proves additional characters existed. 18A adds no search, semantic segmentation, note attachment, persistence, quotation verification, citation stability, relevance, or source-authenticity authority.

Milestone 18B adds one exact human-note boundary downstream of 18A:

```text
ChromiumPageResearchParagraphTextSelectionEvidence
      ↓
caller supplies one exact nonblank note string
      ↓
require established range mode + Unicode offset unit
      ↓
reuse public 18A validation
      ↓
exact supplied range object + verbatim note text
      ↓
ChromiumPageResearchParagraphTextSelectionNoteRecord
```

`create_chromium_research_paragraph_text_selection_note()` retains the exact supplied 18A range object and preserves the caller's note string without normalization. It delegates parent/range validity back through `select_chromium_research_paragraph_text()` rather than creating another coordinate/source-validation authority. The selected source range itself is not interpreted: a non-empty range containing whitespace or punctuation remains a valid caller choice. The note is human interpretation linked to that exact choice, not source evidence, verified quotation evidence, citation authority, claim support, relevance, truth, source authentication, inferred authorship/time, or machine interpretation. 18B adds no range-note persistence, edit/history semantics, generic annotation abstraction, or UI.

Milestone 18C adds one durable exact-range-note sidecar downstream of 18B:

```text
ChromiumPageResearchParagraphTextSelectionNoteRecord
      ↓
re-establish live 18B / 18A validity
      ↓
source capture format + bundle SHA-256
+ paragraph mode + ordinal
+ text-range mode + Unicode start/end coordinates
+ note mode + verbatim note text
      ↓
canonical deterministic JSON
      ↓
SHA-256 over durable reference + human action
      ↓
exclusive-create exact-range-note sidecar
```

`persist_chromium_research_paragraph_text_selection_note()` retains the exact supplied 18B note in runtime persistence evidence while writing only durable source-content identity, paragraph/range coordinates, and the human note. It never stores `selected_text`, paragraph/page text, element ID, URL, endpoint, target ID, loaded-capture state, or source path. Before writing it reuses the public 18B constructor, which in turn reuses 18A range validation, so a forged range outside a bounded returned prefix is rejected without creating a second validator. `verify_chromium_research_paragraph_text_selection_note()` is deliberately file-local: it validates exact shape, coordinate semantics, canonical bytes, and SHA-256 but does not read the source capture or claim the persisted coordinates actually address it. A self-consistent rewritten sidecar can therefore remain file-valid; explicit source relinking is a separate future authority boundary.

These boundaries do **not** navigate, activate tabs, click, submit forms, create or close targets, accept arbitrary DevTools commands or user JavaScript, persist browser state, freeze the DOM, claim atomic page state, authenticate capture or note authorship, verify source provenance, create trusted timestamps, treat rehydrated evidence as fresh observation, automatically choose research evidence, promote caller-authored notes into source truth, discover captures from durable references, treat exact text ranges as verified quotations, treat range notes as claim support, treat exact-range sidecar integrity as source-range proof, invoke an LLM, rank links/sections/passages/tables/lists, repair document structure or list numbering, resolve provenance conflicts, verify quotations, normalize tables, infer header relationships, expand spans, coerce values, flatten nested lists, infer semantic hierarchy, or add autonomous research behavior. The optional `browser` dependency provides the concrete WebSocket transport; Pyxis core does not require a browser dependency.

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

For a fresh development session, use this compact orientation chain:

1. [`README.md`](README.md) — product identity and authority philosophy.
2. [`docs/CURRENT_FRONTIER.md`](docs/CURRENT_FRONTIER.md) — 25B–34B.
3. [`docs/CURRENT_FRONTIER_35_36.md`](docs/CURRENT_FRONTIER_35_36.md) — 35A–36D.
4. [`docs/CURRENT_FRONTIER_37_38.md`](docs/CURRENT_FRONTIER_37_38.md) — 37A–38F.
5. [`docs/CURRENT_FRONTIER_39_40.md`](docs/CURRENT_FRONTIER_39_40.md) — 39A–40D / D205.
6. [`docs/CURRENT_FRONTIER_41_43.md`](docs/CURRENT_FRONTIER_41_43.md) — 41A–43E / D217, the current implemented frontier and post-43E decision boundary.

Then open the relevant milestone-specific document and implementation/tests for the decision being changed. The repository also keeps three complementary detailed records so future development does not depend on chat history:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — architectural boundaries and detailed evolution
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — normative implementation decisions
- [`docs/DEVELOPMENT_ARCHIVE.md`](docs/DEVELOPMENT_ARCHIVE.md) — development history, learned logic, prototype lessons, current gaps, and foreseeable implementation path

The large central documents contain intentionally preserved historical status language. Treat implementation + tests + milestone records as stronger authority than compact continuity summaries, and compact continuity summaries as stronger orientation than stale historical presentation wording.

## Historical detailed status snapshot — through Milestone 18C / D137

The following paragraph is retained as the original detailed status snapshot rather than rewritten into a second competing milestone history.

Pyxis is proven through Milestone 18C / D137: Repository Zero retains the compiler/runtime/revision/export lifecycle, interactive evidence UI, descriptive measurement pipeline, live measurement provenance/invalidation/re-entry path, two concrete governed architecture operations, shared private architecture orchestration, preview-only architecture consequence trace, distinct post-Apply proposed-vs-observed reconciliation, and bounded Python 3.11–3.14 release contract. The browser-facing product has seven real read-only evidence families over explicitly addressable existing Chromium pages, one application-level research bundle that composes those families through fixed sequential acquisition with exact target/URL coherence while explicitly denying atomic-DOM semantics, one deterministic no-overwrite capture format that preserves the complete already-observed bundle with SHA-256 self-integrity evidence, one verified rehydration boundary that can reconstruct the typed bundle after the browser is gone while retaining the exact capture-verification evidence, one human-owned paragraph-selection boundary that points to exact already-returned durable evidence without reacquisition or semantic promotion, one human-authored paragraph-note boundary that preserves exact caller text over the exact selection while keeping interpretation distinct from source evidence, one deterministic paragraph-note sidecar that preserves only the durable source-content reference + human action without duplicating source evidence or claiming authorship, one verified paragraph-note relinking boundary that reconstructs that exact human action against an explicit matching loaded capture without source discovery, path identity, bounded-evidence expansion, or authenticity promotion, one exact paragraph-text refinement boundary that records explicit Unicode code-point coordinates over already-returned text while deriving rather than duplicating selected source text, one exact-range human-note boundary that preserves verbatim human interpretation over the exact range while reusing 18A validation and adding no semantic or epistemic promotion, and one deterministic exact-range-note sidecar that preserves only durable source-content identity + explicit paragraph/range coordinates + verbatim human text while refusing to treat file integrity as proof of source-range validity.

Do not add another statistic, abstraction, score, explanatory layer, compatibility lane, provenance resolver, citation resolver, dataset normalizer, semantic list interpreter, atomic-snapshot claim, capture database, authenticity claim, generic selection/annotation registry, durable-reference resolver, or browser-control surface merely because the current architecture makes one possible. The next implementation milestone should answer a new concrete researcher action. Exact-range-note relinking/rehydration, text-range persistence independent of notes, multi-range selection sets, generic selection registries, note editing/history, multiple-note or notebook abstractions, questions, tags, trusted temporal provenance, capture indexing/search, cross-capture comparison, HMAC/signature systems, verified source identity, quotation verification, citation stability, table normalization/header inference/span expansion/value typing, list-number repair/semantic hierarchy, cross-family semantic joins, DOM-freeze/version identity, navigation, interaction, permissions, autonomous research workflows, machine semantic interpretation, generated notes, and browser UI each still require their own evidence before they are allowed to grow from the current observation, composition, source persistence/rehydration, human-selection, paragraph-note durability/relinking, exact text-range selection, exact-range note, and exact-range-note persistence boundaries.