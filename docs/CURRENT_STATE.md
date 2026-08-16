# Pyxis Current State

**Continuity front door — Pyxis current through Milestone 17A / D131 (2026-08-16).**

This file exists because the GitHub connector cannot safely apply line-level edits to the already-large `ARCHITECTURE.md` and `DEVELOPMENT_ARCHIVE.md`. A prior attempt to replace those files wholesale produced a deletion-heavy diff and was deliberately abandoned rather than normalize a historical rewrite.

Nothing here supersedes proven historical evidence. It provides one current map over the preserved central documents and the later milestone records.

## Read order

For a new development session, read in this order:

1. `README.md`
2. this file (`docs/CURRENT_STATE.md`)
3. `docs/ARCHITECTURE.md`
4. `docs/DECISIONS.md`
5. `docs/DEVELOPMENT_ARCHIVE.md`
6. `docs/MILESTONE_11K_CONTINUITY.md`, `docs/MILESTONE_11L.md` through `docs/MILESTONE_11T.md`, then `docs/MILESTONE_12A.md`, `docs/MILESTONE_12B.md`, `docs/MILESTONE_13A.md`, `docs/MILESTONE_13B.md`, `docs/MILESTONE_14A.md`, `docs/MILESTONE_15A.md`, `docs/MILESTONE_15B.md`, `docs/MILESTONE_15C.md`, `docs/MILESTONE_15D.md`, `docs/MILESTONE_15E.md`, `docs/MILESTONE_15F.md`, `docs/MILESTONE_15G.md`, `docs/MILESTONE_16A.md`, `docs/MILESTONE_16B.md`, `docs/MILESTONE_16C.md`, and `docs/MILESTONE_17A.md`

The large central documents remain intact historical/current foundations. Their status headers lag later implementation because the connector could not safely patch them in place. This file makes those later deltas explicit in one place rather than requiring a future session to rediscover the gap.

## Current Pyxis checkpoint

Pyxis retains fifteen proven evidence families and now adds one explicit browser-research composition boundary, one durable capture boundary, one verified typed-rehydration boundary, and one explicit human-owned passage-selection boundary. The first eight families remain the Repository Zero reference spine; 15A through 15G add seven concrete browser-facing evidence boundaries without changing that spine, 16A composes those seven existing browser families without creating a new source of truth, 16B persists the completed bundle without reacquiring or reinterpreting the page, 16C can reopen that durable evidence as typed application evidence without requiring Chromium to remain alive, and 17A lets the caller point to one exact already-returned paragraph without semantic promotion:

```text
compiler / runtime / revision / export lifecycle
            +
interactive evidence UI
            +
descriptive measurement pipeline
            +
live measurement provenance / invalidation / re-entry
            +
two concrete governed architecture operations
  with shared private application orchestration
            +
preview-only architecture consequence trace
            +
post-Apply proposed-vs-observed consequence reconciliation
            +
bounded Python support / multi-version CI
            +
read-only Chromium page observation evidence
            +
read-only Chromium link-choice evidence
            +
read-only Chromium heading-outline evidence
            +
read-only Chromium page-declared metadata evidence
            +
read-only Chromium paragraph evidence
            +
read-only Chromium table-structure evidence
            +
read-only Chromium list-structure evidence
            +
sequential read-only Chromium research evidence bundle
            +
deterministic durable Chromium research capture
            +
verified typed Chromium research capture rehydration
            +
human-owned verified-capture paragraph selection
```

The permanent Repository Zero authority chain remains:

```text
human intent
    ↓
canonical WorkspaceSpec
    ↓
Repository Intermediate Representation (RIR)
    ↓
deterministic compiler
    ↓
compiler-owned generation evidence
    ↓
filesystem materialization
    ↓
runtime
```

Architectural change remains preview → rationale → append-only revision → canonical mutation → compile/materialize → run. Generated code is never a second source of truth. Export packages existing compiler products and READY remains verification evidence rather than filesystem inference.

The first local Textual Workspace UI is complete for the current Repository Zero slice: it renders current evidence, reruns the materialized Workspace, previews either removal of `normalize_text` or addition of `split_lines`, traces the proposed consequences of that preview across already-owned evidence stages, requires rationale before Apply, retires stale READY after architecture change, removes stale measurement evidence when exact RIR identity changes, and restores READY only through verified export refresh. After successful Apply it clears the proposed consequence surface and can render a separate observed reconciliation derived from the revision/compiler/RIR/runtime evidence actually produced by that Apply. One `WorkspaceController` remains the live transient-state authority.

15A returns the product to its original browser/research purpose while preserving Chromium as the mature browser. A caller may supply one explicit Chromium DevTools endpoint and receive frozen application evidence for one existing page. Pyxis does not discover the browser, infer the active tab when multiple pages exist, navigate, interact, persist browser state, or interpret the page.

15B reuses that exact endpoint and target-selection authority to expose bounded DOM-order link choices already present on the selected page. It preserves browser-resolved href values, bounded anchor text, exact Unicode counts, and collection truncation evidence without ranking, classifying, selecting, or following a link.

15C reuses that same page-selection authority to expose bounded DOM-order `h1`–`h6` markers with literal HTML levels and bounded text. Heading gaps remain exactly as authored; Pyxis does not repair them into a semantic tree, summarize sections, or turn document structure into navigation authority.

15D reuses the same page-selection authority to expose page-declared source-identity hints without promoting them into verified provenance. It preserves the authored document-language string, bounded canonical-link declarations with raw and browser-resolved hrefs, and bounded meta-description declarations. Duplicate or conflicting declarations remain visible rather than being silently resolved.

15E reuses the same page-selection authority to expose literal `<p>` elements as bounded DOM-order passage evidence. It preserves authored element IDs exactly as present, including duplicates and empty values, without treating paragraph boundaries as semantic segmentation or IDs as stable citation locators.

15F reuses the same page-selection authority to expose bounded literal HTML-table structure. It preserves table/row/cell DOM order, direct captions, literal `TH`/`TD` cell identity, browser-exposed row/column spans, exact counts, and nested truncation facts without expanding spans, inferring header relationships, typing values, or flattening the structure into a normalized dataset.

15G reuses the same page-selection authority to expose bounded literal ordered/unordered-list structure. It preserves global list DOM order, literal `OL`/`UL` identity, raw authored `start`/`value` strings, direct `LI` children, exact counts, and mechanical parent-list/item ordinals for nested lists. Direct-list item text excludes descendant-list text so nesting remains separate evidence rather than being silently flattened. Pyxis does not repair numbering or turn DOM nesting into semantic hierarchy.

16A composes those seven proven browser evidence families through one application-level convenience boundary. The first page read selects the target under the existing 15A rules; the remaining six reads reuse that exact target ID in fixed order. Every constituent evidence object must retain the same endpoint, target ID, and page URL before the bundle is emitted. The bundle records `acquisition_mode="sequential_non_atomic_url_coherent"`: URL agreement is a coherence check, not proof that one frozen DOM state existed across all seven reads.

16B persists that completed 16A bundle as deterministic canonical JSON at one exact caller-chosen new file path. Saving never re-observes Chromium. The complete bundle payload is retained with a SHA-256 self-integrity digest, and later verification checks canonical bytes, the recorded digest, and persisted endpoint/target/URL coherence without reconnecting to the page. The checksum is not authentication or verified provenance, and 16B adds no timestamp because persistence time would not represent the seven sequential browser-read moments.

16C reopens one verified 16B capture as typed application evidence only after the complete nested payload passes exact JSON-type, field-set, source, ordinal, count, limit, truncation, and structural validation plus a lossless reconstruction check. The load result retains the exact 16B file-verification evidence beside a newly constructed 16A-shaped bundle, so reopened durable evidence remains distinguishable from fresh Chromium observation. The real-browser acceptance proof terminates Chromium before load and still reconstructs evidence equal to the original bundle.

17A lets the caller explicitly select one already-returned paragraph from that verified rehydrated capture by exact 1-based DOM ordinal. The selection retains the exact loaded-capture object and exact paragraph object rather than copying text into a new quote/citation representation. Duplicate authored IDs do not control selection, and a paragraph known only through a truncated complete count cannot be selected or reacquired. Selection records caller choice only; it does not prove relevance, truth, quotation validity, citation authority, locator stability, source authenticity, or browser-control authority.

## Second concrete architecture operation — 12A / D116

Milestone 12A deliberately adds a second concrete operation before introducing any generalized architecture-edit abstraction.

The new capability is:

```text
split_lines
    ↓
text.splitlines()
    ↓
{
  "lines": [...],
  "line_count": ...
}
```

`split_lines` is not part of the default `WorkspaceSpec`. It appears only when explicit proposed canonical intent adds it.

The proven path is:

```text
Preview addition of split_lines
    ↓
proposed canonical/RIR evidence
    ├── added capability: split_lines
    ├── new artifact: generated/capabilities/split_lines.py
    ├── changed composed Workspace entrypoint
    └── added runtime key: split_lines
    ↓
visible human rationale
    + explicit visible runtime input
    ↓
Apply exact retained preview
    ↓
append revision operation: add_capability:split_lines
    ↓
canonical write → RIR → compiler/materializer
    ├── existing capability products reused
    ├── split_lines product new
    └── Workspace entrypoint regenerated
    ↓
run new Workspace
    ↓
fresh WorkspacePresentation
    ↓
pre-change READY retired
    +
pre-change measurement snapshot removed by exact-RIR provenance rule
```

D116 therefore proves that the governed architecture path is not limited to one removal operation. It also intentionally exposes duplication among the concrete preview/apply/controller/UI seams. That duplication became the evidence examined by 12B; 12A itself introduced no generic operation registry, command schema, dynamic architecture editor, or generalized mutation form.

Proof: Actions #373 passed on `d8b6f0ebe9cbb97960b026efc61b4a7b602ca94e`; all 206 Repository Zero tests passed.

## Shared orchestration boundary — 12B / D117

12B compared `remove_normalize_text` and `add_split_lines` directly rather than assuming that two operations automatically justify a generic operation model.

The comparison found two sequences that are genuinely operation-independent:

```text
Workspace preview orchestration
    ↓
resolve root
→ preflight current run/export evidence
→ load canonical state
→ invoke one concrete preview builder
→ project immutable preview evidence
→ verify canonical identity remained coherent
```

and:

```text
Workspace Apply orchestration
    ↓
require/normalize rationale
→ preflight current run/export evidence
→ verify retained preview against current canonical state
→ invoke one concrete governed Apply function
→ run materialized post-change Workspace with explicit runtime input
→ rebuild current presentation
→ omit pre-change READY evidence
```

Those exact sequences are now private shared helpers in `architecture_preview.py` and `architecture_apply.py`. Public application seams remain concretely named for `remove_normalize_text` and `add_split_lines`.

12B explicitly does **not** generalize capability mutations, `ArchitectureDelta` facts, revision operation identities, compiler capability registration, `WorkspaceController` operation methods, Textual controls/event IDs, or user-facing operation copy. It introduces no operation registry, command object/schema, dynamic editor, or architecture DSL.

This matches the lower governed Apply boundary already proven by `_apply_previewed_edit`: shared governance/orchestration may be private while concrete wrappers retain operation identity and validation.

D117 therefore establishes a narrower rule than “two examples justify abstraction”: **extract only behavior demonstrated to be invariant, and leave semantic identity concrete until additional product pressure proves that abstraction is needed.**

Proof: Actions #380 passed on `4d75b37a03d0bb70de503ac98d78e3e747e61141`; all 206 Repository Zero tests passed.

## Architecture consequence trace — 13A / D118

13A moves the product from merely co-displaying evidence toward making the architecture-to-code transformation directly inspectable.

`ArchitecturePreviewPresentation` now contains an immutable stage-ordered trace made only from facts already owned and validated by the preview:

```text
requested architecture change
    ↓
proposed canonical state
    ↓
proposed RIR
    ↓
compiler products
    ↓
runtime contract
```

Each step carries only stage, action, subject kind, and exact subject. For the visible `split_lines` proof, the trace states that the preview requests adding the capability, shows the same capability in proposed canonical and RIR state, identifies the new capability artifact and changed Workspace entrypoint, and identifies the added runtime key.

The trace renderer is nested inside the existing preview evidence panel and remains explicitly **PROPOSED — NOT APPLIED**. It does not compile, run, persist, mutate, append revisions, refresh READY, acquire measurements, explain code, score impact, or infer causality. Current Workspace evidence remains unchanged during Preview.

The application trace projection also produces the corresponding remove-action shape for `normalize_text`, while the first visible acceptance proof remains deliberately focused on `split_lines`.

D118 therefore permits Pyxis to make an already-owned preview consequence chain explicit for the user without creating a new source of truth or an explanatory model.

Proof: Actions #392 passed on `f8b75582176811d968335e001280942d59ad024e`; all 209 Repository Zero tests passed.

## Observed architecture consequence reconciliation — 13B / D119

13B keeps the 13A preview intact and asks what happened after the exact retained preview was actually applied.

The reconciliation has two deliberately distinct halves:

```text
PROPOSED
ArchitecturePreviewPresentation
    ↓
unchanged historical preview evidence

OBSERVED
successful Apply-owned evidence
    ├── RevisionEvent / RevisionCompletion
    ├── post-Apply canonical identity
    ├── post-Apply RIR
    ├── compiler generation statuses
    └── post-Apply runtime-result keys
```

`ArchitectureConsequenceReconciliationPresentation` retains the original preview object under `proposed` and places the fresh Apply-derived facts under a separate immutable `observed` record. It does not reopen the filesystem, recompile, rerun, persist, export, or acquire measurement evidence in order to reconcile the two.

The only comparisons currently permitted are narrow structural equalities:

- preview current/proposed canonical hashes vs revision before/after canonical hashes;
- proposed canonical hash vs observed post-Apply canonical hash;
- proposed RIR capabilities vs observed post-Apply RIR capabilities;
- predicted compiler-product action vs observed generation status;
- proposed runtime keys vs observed runtime-result keys;
- revision-completion RIR SHA-256 vs observed post-Apply RIR SHA-256.

Compiler-product reconciliation is mechanically defined as:

```text
proposed add     → expected status new
proposed change  → expected status regenerated
proposed remove  → expected status removed
```

A mismatch is represented directly as `matches=False`. A dedicated test alters only a test copy of observed artifact presentation evidence after a genuine Apply and proves that a proposed `add` remains a proposed `add`, the expected status remains `new`, the altered observed status remains `reused`, and the reconciliation reports the difference without rewriting either side.

The combined `WorkspaceController` retains at most one latest successful reconciliation. Successful Apply installs it. A later successful architecture Preview clears it before presenting a different proposal. Failed Apply does not advance it. Ordinary runtime rerun and export refresh do not reinterpret it.

The Textual transition is explicit:

```text
before Apply
    PROPOSED CONSEQUENCE TRACE — NOT APPLIED

successful Apply
    proposed trace clears
    ↓
    POST-APPLY RECONCILIATION — OBSERVED EVIDENCE
```

The observed renderer explicitly states that the earlier preview remains separate proposed evidence. It renders only exact `MATCH` / `DIFFERS` comparisons and adds no summary score, confidence estimate, causal claim, generated explanation, quality judgment, or architecture recommendation.

The first visible proof remains the concrete `split_lines` addition. Application coverage also proves `normalize_text` removal is observed as a `removed` compiler product and as absent from post-Apply runtime keys.

D119 therefore establishes: **proposed architecture evidence and observed post-Apply evidence may be reconciled, but they remain distinct evidence objects. Agreement is structural evidence, not a prediction-quality score or causal explanation.**

Proof: Actions #403 passed on `dc479d7393bfab9a6f00b2bd38358bc674352900` with all 213 Repository Zero tests; Actions #406 passed on `e94df90a10220619deb9128ce46958a7a08caf79` with all 214 Repository Zero tests.

## Python support contract — 14A / D120

14A closes a release-contract mismatch rather than adding application behavior. Before this milestone, package metadata declared Python `>=3.11` while ordinary CI exercised only Python 3.11. That open-ended metadata therefore claimed more compatibility than Repository Zero had actually proven.

The package support contract is now:

```text
Python >=3.11,<3.15
```

The ordinary Repository Zero workflow runs the same complete suite independently on four supported interpreter lanes:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The matrix uses `fail-fast: false`, so one interpreter cannot suppress compatibility evidence from another. Each lane installs Pyxis with the same `.[dev]` dependencies and runs the same `python -m pytest` command; no compatibility-specific smoke suite or skipped product path replaces the full tests.

Actions #414 on `a9077e53016de9e90795a30847f6cbf2febb505a` proved:

- Python 3.11: 214 passed;
- Python 3.12: 214 passed;
- Python 3.13: 214 passed;
- Python 3.14: 214 passed.

Python 3.15 and later are intentionally outside the current metadata contract. A future interpreter line must be added deliberately and pass the full suite before the upper bound moves.

D120 therefore establishes: **Pyxis package compatibility claims are bounded by interpreter versions explicitly represented in package metadata and independently proven by the full CI matrix. Expanding that range requires new evidence.**

14A changes no compiler, RIR, canonical authoring, revision, runtime, export, measurement, architecture-operation, preview, reconciliation, or Textual behavior.

## First read-only Chromium evidence boundary — 15A / D121

15A returns to the original browser/research purpose only after the Repository Zero compiler/product spine, evidence UI, measurement foundations, architecture-change path, reconciliation boundary, and release-support contract are stable.

Chromium remains Chromium. Browser state remains caller-owned.

The first browser-facing path is:

```text
explicit Chromium DevTools HTTP(S) endpoint
    ↓
read /json/list
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate read
    ↓
frozen ChromiumPageObservationEvidence
```

`pyxis.browser` owns the concrete Chromium transport. `pyxis.app.observe_chromium_page()` owns the immutable application evidence contract.

The fixed observation reads only the selected page's current URL, title, and `document.body.innerText`. Rendered text is bounded by an explicit prefix limit while retaining the complete Unicode code-point count and a mechanical truncation fact. `Array.from(text)` is used in the fixed browser expression so JavaScript counting/slicing and Python evidence validation share code-point semantics even for characters such as emoji.

Target selection is deliberately non-heuristic. Exactly one page may be selected implicitly. When multiple page targets exist, Pyxis refuses to infer the active/current tab from target order or browser metadata and requires an exact `target_id`.

The operation does not accept arbitrary CDP methods or caller-supplied JavaScript. It does not navigate, activate, click, submit, create/close targets, persist browser/page state, mutate Workspace state, invoke an LLM, or add UI.

`websocket-client` is optional under the `browser` dependency group; it is also in `dev` so the ordinary supported-Python matrix exercises the concrete transport. Core Pyxis still has no required browser dependency.

15A includes a real-browser integration proof rather than only mocked transport tests. The ordinary suite launches a disposable headless Chrome/Chromium instance, receives its DevTools endpoint, discovers the exact local fixture page, and calls the production observation path. Intermediate CI runs exposed two fixture assumptions—target visibility before DOM readiness and variable browser startup latency—which were corrected in test synchronization without adding product retries, navigation, or skips.

Actions #432 passed on `1f039148079b875ba706f7f1052b7a1596e1db32` across Python 3.11, 3.12, 3.13, and 3.14. The full suite contains 221 tests and includes the real-browser integration path.

D121 therefore establishes: **browser observation authority does not imply browser-control authority. Pyxis may acquire frozen read-only evidence from one explicitly addressable existing Chromium page while the browser and its state remain caller-owned. Any navigation, interaction, persistence, interpretation, or autonomous workflow requires a separate product decision and proof.**

## Read-only Chromium link evidence — 15B / D122

15B asks the next concrete research question without crossing into browser control: can Pyxis expose the navigation choices already present on the selected page so a researcher can inspect them without Pyxis selecting or following a destination?

The operation reuses the 15A endpoint and target-selection boundary. There is no second active-tab heuristic or target authority.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('a[href]')
    ↓
bounded DOM-order link prefix
    ↓
frozen ChromiumPageLinksEvidence
```

`pyxis.browser.read_chromium_page_links()` reads only the current page URL and matching anchors. For each returned anchor it preserves a 1-based DOM-order ordinal, the browser-resolved `link.href`, a bounded `link.innerText` prefix, and the exact Unicode code-point count. The snapshot also records the complete matching-link count so collection truncation is mechanically derivable from the explicit limit.

`pyxis.app.observe_chromium_page_links()` projects those facts into immutable application evidence with explicit source `document.querySelectorAll('a[href]')`, link and text limits, and per-link plus collection truncation facts.

DOM order is not relevance. A resolved href is not permission to request it. Anchor text is not assumed to truthfully describe the destination. Non-HTTP values such as `mailto:` or `javascript:` are preserved as observed rather than promoted, rejected, or classified by this milestone.

15B does not rank, recommend, deduplicate, canonicalize, classify schemes or destination safety, fetch destination resources, navigate, activate, click, submit, create/close targets, persist evidence, invoke an LLM, or add UI.

The real-browser proof uses one caller-owned disposable page containing both text and links. The same exact target proves 15A page evidence and 15B link evidence. Under `link_limit=2`, three existing anchors produce two returned records plus `link_count=3` and `truncated=True`; a relative href is verified after browser resolution, `mailto:` is preserved, and Unicode anchor text is bounded/countable in code points.

An intermediate harness attempt launched two fixture file URLs at browser startup. Actions #451 showed both installed Chromium-family binaries exiting with code 13 before DevTools publication on Python 3.11; all new link unit/application tests passed and the failing path never reached production link acquisition. The harness was simplified to one explicit page rather than adding any production launch or navigation recovery.

Actions #452 passed on `0f4fe856553f22983bc72bbfe5f973f20e42ab4e` across Python 3.11, 3.12, 3.13, and 3.14. The full suite contains 226 tests and includes the real-browser page/link evidence path.

D122 therefore establishes: **observing available navigation choices is still observation, not control. Pyxis may expose bounded DOM-order link evidence from one explicitly addressable existing Chromium page, while destination selection and every act of navigation remain outside this milestone's authority.**

## Read-only Chromium heading-outline evidence — 15C / D123

15C asks a separate research question: can Pyxis expose the section markers already encoded by the page author so a researcher can inspect document structure without Pyxis summarizing the page or inferring a semantic tree?

The operation reuses the existing endpoint and exact page-selection boundary. `pyxis.app.chromium_headings` imports the existing private target selector rather than duplicating it.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('h1,h2,h3,h4,h5,h6')
    ↓
bounded DOM-order heading prefix
    ↓
frozen ChromiumPageHeadingsEvidence
```

`pyxis.browser.read_chromium_page_headings()` preserves a 1-based DOM-order ordinal, the literal HTML heading level from 1 through 6, a bounded `heading.innerText` prefix, and exact Unicode code-point count for every returned heading. The snapshot also records the complete matching-heading count so collection truncation is mechanical.

`pyxis.app.observe_chromium_page_headings()` projects those facts into immutable evidence with explicit source `document.querySelectorAll('h1,h2,h3,h4,h5,h6')`, heading and text limits, and per-heading plus collection truncation facts.

Heading level is page-authored evidence, not a Pyxis quality judgment or inferred hierarchy. A skipped sequence such as `h1 → h4` remains exactly `1 → 4`; Pyxis does not repair the gap, create missing levels, or classify the authoring pattern as an accessibility defect. Heading text is not treated as a verified summary of the following section.

15C does not summarize, rank sections, infer a semantic tree, repair heading levels, extract ARIA landmarks, navigate, scroll, activate, click, submit, create/close targets, persist evidence, invoke an LLM, or add UI.

The same real-browser fixture now proves all three observation families against one explicit caller-owned page target. It contains literal `h1`, `h3`, and `h6` elements. Under `heading_limit=2`, the first two are returned as levels 1 and 3 while the third remains represented only through `heading_count=3` and `truncated=True`. Unicode heading text is bounded and counted in code points.

Actions #465 passed on `05e19a3516972ffaf3b8b7f692cffe42d465e4e5` across Python 3.11, 3.12, 3.13, and 3.14. The full suite contains 231 tests and includes the real-browser page/link/heading evidence path.

D123 therefore establishes: **literal author-provided heading markers are valid read-only research evidence. Pyxis may expose bounded DOM-order h1–h6 facts from one explicitly selected existing Chromium page, but the encoded levels remain observations rather than a repaired hierarchy, summary, quality score, or control surface.**

## Read-only page-declared metadata evidence — 15D / D124

15D asks whether Pyxis can expose the source-identity hints already declared by a page without converting those hints into verified provenance.

The operation reuses the existing endpoint and exact target-selection boundary. `pyxis.app.chromium_metadata` imports the same private target selector used by 15C rather than duplicating page-selection logic.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
authored document lang
+ link[rel~=canonical] declarations
+ meta[name=description] declarations
    ↓
frozen ChromiumPageMetadataEvidence
```

`pyxis.browser.read_chromium_page_metadata()` preserves the literal authored document `lang` string; bounded canonical-link declarations in DOM order with both raw `getAttribute('href')` and browser-resolved `link.href`; and bounded meta-description declarations with exact Unicode code-point counts. Complete canonical-link and description counts make collection truncation mechanical.

`pyxis.app.observe_chromium_page_metadata()` projects those facts into immutable application evidence with explicit source strings and explicit limits. Duplicate or conflicting canonical links and descriptions remain separate declarations. Language is not normalized or validated.

A canonical declaration is not verified canonical identity. A meta description is not a verified abstract or citation. A document language attribute is not proof that the rendered content actually uses that language. Browser resolution of a relative canonical href is an observed browser fact, not authorization to request or trust the destination.

15D does not choose an authoritative canonical URL or description, validate language tags, extract author/publication-date/Open Graph/JSON-LD/schema.org/citation metadata, fetch destinations, navigate, activate, click, submit, scroll, create/close targets, persist evidence, score provenance, invoke an LLM, or add UI.

The same real-browser fixture now proves all four observation families against one explicit caller-owned page target. The 15D fixture deliberately contains `EN-us`, two canonical declarations, and two description declarations. Under one-item collection limits, Pyxis returns the first observed declaration while preserving total counts of two and explicit truncation. The first relative canonical retains raw `canonical.html` alongside its exact Chromium-resolved file URL; the mixed-case metadata selectors are observed without selecting either declaration as authoritative.

Actions #478 passed the 15D implementation suite on Python 3.11, 3.12, 3.13, and 3.14 at `947962c3aab3301eb245b75bc2f57eaf536d9aa5`. The full suite contains 236 tests and includes the real-browser page/link/heading/metadata evidence path.

D124 therefore establishes: **page-declared metadata is evidence of what the page declares, not verified provenance. Pyxis may expose bounded document-language, canonical-link, and meta-description declarations from one explicitly selected existing Chromium page, while duplicate or conflicting declarations remain visible rather than being silently resolved into source truth.**

## Read-only Chromium paragraph evidence — 15E / D125

15E asks whether Pyxis can expose authored paragraphs as individually inspectable passage evidence without inventing sentence boundaries, relevance, citation identity, or browser control.

The operation reuses the established endpoint and exact page-selection authority.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('p')
    ↓
bounded DOM-order paragraph prefix
    ↓
frozen ChromiumPageParagraphsEvidence
```

`pyxis.browser.read_chromium_page_paragraphs()` preserves a 1-based DOM ordinal, the literal authored `id` string or empty string, a bounded `paragraph.innerText` prefix, and exact Unicode code-point count for every returned paragraph. The snapshot also records the complete matching-paragraph count so collection truncation is mechanical.

`pyxis.app.observe_chromium_page_paragraphs()` projects those facts into immutable evidence with explicit source `document.querySelectorAll('p')`, paragraph and text limits, and per-paragraph plus collection truncation facts.

Paragraph boundaries are page-authored DOM evidence, not Pyxis semantic segmentation. DOM order is not relevance. An element ID is not guaranteed unique, stable across page revisions, permanent, or suitable as a citation key. Duplicate IDs remain duplicate and missing IDs remain empty.

15E does not split paragraphs into sentences, merge adjacent passages, infer sections, rank/recommend/summarize passages, verify quotations, certify citation stability, deduplicate IDs, scroll, navigate, activate, click, submit, create/close targets, persist evidence, invoke an LLM, or add UI.

The real-browser proof is deliberately separate from the existing 15A–15D fixture so those established tests are not rewritten. One disposable Chromium page contains three `<p>` elements, including duplicate `id="passage"` values. Under `paragraph_limit=2` and `paragraph_text_limit=7`, Pyxis returns two records while preserving `paragraph_count=3`, collection truncation, duplicate IDs, bounded Unicode text, and no browser-control behavior.

Actions #491 passed on `291a0f2b617300b0be9cc1df6306096cf3de0967` across Python 3.11, 3.12, 3.13, and 3.14. The full suite contains 242 tests; the inspected Python 3.11 log shows both the existing Chromium integration and the new paragraph real-browser integration passing.

D125 therefore establishes: **literal paragraph elements are valid read-only passage evidence, but paragraph boundaries and authored element IDs remain page-authored facts rather than Pyxis semantic segmentation or citation authority. Pyxis may expose bounded DOM-order `<p>` evidence from one explicitly selected existing Chromium page while preserving duplicate/empty IDs and granting no ranking, quotation-verification, locator-stability, or browser-control authority.**

## Read-only Chromium table evidence — 15F / D126

15F asks whether Pyxis can expose literal HTML table structure for research inspection without converting that structure into an inferred or normalized dataset.

The operation reuses the established endpoint and exact page-selection authority.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('table')
    ↓
bounded table → row → direct TH/TD cell evidence
    ↓
frozen ChromiumPageTablesEvidence
```

`pyxis.browser.read_chromium_page_tables()` preserves 1-based table/row/cell DOM ordinals, a direct caption when present, literal `TH`/`TD` cell tag identity, browser-exposed `rowSpan` and `colSpan`, bounded rendered text, and exact Unicode code-point counts. Descendant rows whose nearest table ancestor is a nested table are excluded from the outer table's row evidence.

The read is bounded independently by table count, rows per returned table, cells per returned row, and caption/cell text. Each collection retains its complete observed count, so table-, row-, and cell-level truncation remain mechanical rather than inferred.

`pyxis.app.observe_chromium_page_tables()` projects those facts into immutable evidence with explicit source `document.querySelectorAll('table')` and explicit nested limits.

Table markup is structure evidence, not automatically a rectangular dataset. `TH` is literal tag identity rather than a Pyxis-inferred header mapping. `rowspan` and `colspan` remain spans rather than being expanded into duplicated grid cells. Rendered strings remain strings; Pyxis does not infer numbers, dates, units, categories, schemas, or data quality.

15F does not infer header relationships, expand spans, flatten tables into CSV-like rows, coerce values, merge multi-row headers, infer units or schemas, rank tables, judge statistical/data quality, reinterpret visual/CSS layout as table semantics, scroll, navigate, activate, click, submit, create/close targets, persist evidence, invoke an LLM, or add UI.

The independent real-browser proof contains two tables. The first has caption `Study 😀 table`, two rows, a `TH` with `rowspan="2"`, a `TD` with `colspan="2"`, and a first row containing three cells. Under `table_limit=1`, `row_limit=1`, `cell_limit=2`, and `text_limit=7`, Pyxis returns one table, one row, and two cells while preserving complete counts of two tables, two first-table rows, and three first-row cells. The literal TH/TD identities and spans remain unchanged; caption/cell Unicode text is bounded and counted exactly.

Actions #504 passed on `670e74274e09e22c71fcb414ae3cb27efc053647` across Python 3.11, 3.12, 3.13, and 3.14. The inspected Python 3.11 log collected 248 tests; established Chromium integrations and the new table real-browser integration all passed; **248 passed**.

D126 therefore establishes: **literal HTML table structure is valid read-only research evidence, but table markup is not automatically a normalized dataset. Pyxis may expose bounded table/row/cell DOM facts from one explicitly selected existing Chromium page, including literal TH/TD identity and browser-exposed row/column spans, while granting no header-inference, span-expansion, value-typing, dataset-normalization, ranking, interpretation, or browser-control authority.**

## Read-only Chromium list evidence — 15G / D127

15G asks whether Pyxis can expose authored ordered/unordered list structure for research inspection without flattening nested lists, repairing numbering, or promoting DOM nesting into semantic hierarchy.

The operation reuses the established endpoint and exact page-selection authority.

```text
explicit selected existing page
    ↓
one fixed Runtime.evaluate read
    ↓
document.querySelectorAll('ol,ul')
    ↓
bounded global DOM-order OL/UL evidence
    ↓
direct LI children + mechanical nesting coordinates
```

`pyxis.browser.read_chromium_page_lists()` preserves global 1-based list DOM ordinals, literal `OL`/`UL` tag identity, raw authored `start` strings, direct `LI` children, raw authored item `value` strings, bounded direct-list text, exact Unicode code-point counts, and complete list/item counts. When a list is nested, it also preserves the nearest ancestor-list ordinal and the direct parent-item ordinal within that ancestor list.

Parent-item `innerText` would include descendant-list content and silently flatten two DOM structures. The fixed 15G read instead walks text nodes and includes a text node only when its nearest `ol,ul` ancestor is the list currently being observed. Descendant-list text therefore remains separate evidence owned by the descendant list record.

`pyxis.app.observe_chromium_page_lists()` projects those facts into immutable evidence with explicit source `document.querySelectorAll('ol,ul')`, list/item/text limits, and mechanical collection/item/text truncation facts.

List markup is structure evidence, not semantic hierarchy or corrected numbering. Raw `start`/`value` strings are preserved even when unusual or invalid for the authored element; Pyxis does not discard, parse, repair, or validate them into a numbering model. A nested list is nested because the DOM nests it, not because Pyxis decided it is a subargument, substep, dependency, priority, or conceptual child.

15G does not calculate displayed list numbers, repair numbering, validate authored attributes, interpret CSS counters/styles, flatten nested lists, infer a semantic outline, classify task/substep relationships, rank items, infer priority, summarize list content, scroll, navigate, activate, click, submit, create/close targets, persist evidence, invoke an LLM, or add UI.

The independent real-browser proof contains one `OL start="3"` with three direct items, a nested `UL start="99"` inside the second item, and a separate third list. Under `list_limit=2`, `item_limit=2`, and `text_limit=7`, Pyxis returns two lists while preserving `list_count=3`; returns two outer items while preserving `item_count=3`; retains raw `value="7"` and bounded `Alpha 😀` text for the first item; retains the parent item's direct text as `Parent tail` without the nested `Nested` text; and preserves the nested list at parent-list ordinal 1 / parent-item ordinal 2 with raw `start="99"`, raw nested item `value="42"`, and separate `Nested` text.

Actions #517 passed on `5f3f5fbdefc2b27d1d54395cce69e7044c4ec60b` across Python 3.11, 3.12, 3.13, and 3.14. The inspected Python 3.11 log collected 254 tests; established Chromium integrations and the new list real-browser integration all passed; **254 passed**.

D127 therefore establishes: **literal ordered/unordered list structure is valid read-only research evidence, but DOM nesting and authored numbering attributes are not semantic hierarchy or corrected numbering. Pyxis may expose bounded DOM-order `OL`/`UL` records from one explicitly selected existing Chromium page, including raw authored `start`/`value` attributes, direct `LI` children, direct-list text evidence that excludes descendant-list text, and mechanical parent-list/item ordinals, while granting no list repair, semantic grouping, ranking, interpretation, navigation, or browser-control authority.**

## Read-only Chromium research evidence bundle — 16A / D128

16A asks whether Pyxis can compose the seven proven browser evidence families into one convenient research-page object without pretending seven sequential reads form one atomic DOM snapshot.

The new boundary is application composition only:

```text
caller-supplied Chromium endpoint
    ↓
page observation / established target selection
    ↓
exact selected target id
    ↓
links → headings → metadata → paragraphs → tables → lists
    ↓
exact endpoint + target + URL coherence after each read
    ↓
frozen ChromiumPageResearchEvidenceBundle
```

`pyxis.app.observe_chromium_page_research_bundle()` calls the existing seven public observers rather than adding a second transport path. The first `observe_chromium_page()` call selects the page under the existing 15A authority. Every later family receives that exact selected target ID explicitly.

The resulting `ChromiumPageResearchEvidenceBundle` contains the exact existing page, link, heading, metadata, paragraph, table, and list evidence objects. It does not copy their facts into a second representation, merge their semantics, rank across families, or become a new source of truth.

The fixed acquisition order is `page → links → headings → metadata → paragraphs → tables → lists`. The bundle records `acquisition_mode="sequential_non_atomic_url_coherent"`. After each constituent read, endpoint, target ID, and URL must exactly match the initial page evidence. A mismatch raises `ChromiumReadError`, stops later acquisition, and emits no bundle.

That coherence rule is deliberately weaker than an atomic-snapshot claim. A same-URL DOM mutation can still occur between reads. 16A adds no DOM hash, page-version token, mutation observer, freeze protocol, browser-state ownership, or other mechanism that would justify saying all seven objects describe one frozen browser instant.

16A also adds no bundle-wide limit configuration. Each constituent observer keeps its already-proven bounded defaults; callers that need different limits may continue to call the individual observers directly.

The independent real-browser proof uses one static local page containing all seven supported evidence shapes: title/body text, one link, one `h1`, authored language/canonical/description metadata, one paragraph, one table, and one ordered list with authored `start`/`value`. The production bundle operation retains one exact endpoint, target ID, and URL across all seven members while preserving each family's literal evidence.

Actions #527 passed on `b4e803ec725fb7bff34020ee94f894bb7cc759af` across Python 3.11, 3.12, 3.13, and 3.14. The inspected Python 3.11 log collected **260 tests**; the five focused 16A application tests, the real Chromium research-bundle integration, and all established browser integrations passed; **260 passed**.

D128 therefore establishes: **existing read-only Chromium evidence families may be composed into one research-page bundle only when composition preserves their independent evidence ownership and makes acquisition order, exact target reuse, URL coherence, and non-atomicity explicit. URL agreement across sequential reads is a coherence check, not proof of one frozen DOM state. A bundle is a convenience boundary, not a new browser snapshot authority or source of truth.**

## Durable Chromium research capture — 16B / D129

16B asks whether one completed 16A bundle can become durable evidence without silently reacquiring the page or granting persistence stronger authority than the observation itself possessed.

The persistence path is deliberately downstream-only:

```text
completed ChromiumPageResearchEvidenceBundle
    ↓
revalidate 16A mode/order + endpoint/target/URL coherence
    ↓
complete deterministic bundle JSON
    ↓
SHA-256 over canonical bundle bytes
    ↓
exclusive-create caller-chosen capture file
    ↓
later canonical-byte + digest verification
```

`pyxis.app.persist_chromium_page_research_capture()` accepts the already-observed bundle and an exact destination file. It does not call Chromium, discover a browser, select a target, or perform a second observation. The destination parent must already exist and the destination itself must not; existing files are never overwritten.

The capture format is `pyxis.chromium.research_capture.v1`. Its `bundle` field contains the complete 16A dataclass projection, not a selected or ranked subset. Canonical UTF-8 JSON uses direct Unicode, sorted keys, compact separators, finite numeric values only, and one final newline. `bundle_sha256` is computed over the canonical complete bundle payload.

`pyxis.app.verify_chromium_page_research_capture()` later reads only the file. It verifies UTF-8/JSON shape, the supported format, exact acquisition mode/order, persisted endpoint/target/URL coherence across all seven members, the recomputed bundle digest, and exact canonical document bytes. It does not reconnect to Chromium or rehydrate a new typed bundle.

That SHA-256 proves only self-integrity of the stored payload against the digest recorded beside it. An actor with authority to rewrite both payload and checksum can create another self-consistent file, so D129 does not claim authentication, publisher identity, verified provenance, chain-of-custody against a writer, or cryptographic authorship.

16B deliberately adds no timestamp. File-write time describes persistence, not the seven sequential browser-read moments that produced the bundle. If temporal provenance becomes a product need, it must be acquired with explicit observation-time semantics rather than inferred from save time or filesystem metadata.

The real Chromium acceptance path extends the existing 16A fixture rather than launching a second browser. The production bundle from one live caller-owned page is passed by exact object identity into persistence and then verified from disk. Actions #537 on `60fdb77ae1a56dd2654311fac70b743f4c99e797` passed on Python 3.11, 3.12, 3.13, and 3.14. The inspected Python 3.11 log collected **265 tests**, including all five focused capture tests and the live Chromium → bundle → persist → verify integration; **265 passed**.

D129 therefore establishes: **a completed read-only Chromium research bundle may be persisted as a deterministic, no-overwrite capture artifact whose complete bundle payload is protected by explicit SHA-256 integrity evidence. Persistence and later file verification preserve already-acquired evidence; they do not reacquire page state, authenticate the producer or source, verify provenance, add a trusted timestamp, rehydrate new semantic authority, or strengthen the bundle's sequential/non-atomic browser claim.**

## Verified Chromium research capture rehydration — 16C / D130

16C asks whether one durable 16B capture can re-enter the typed Pyxis application layer after the browser is gone without confusing file integrity with valid nested application evidence or erasing the capture origin.

The reopening path is deliberately downstream of the existing verifier:

```text
persisted 16B capture
    ↓
16B canonical-byte + SHA-256 verification
    ↓
exact nested JSON type reconstruction
    ↓
full application evidence validation
    ↓
lossless payload round-trip proof
    ↓
ChromiumPageResearchLoadedCaptureEvidence
    ├── exact 16B verification evidence
    └── reconstructed ChromiumPageResearchEvidenceBundle
```

`pyxis.app.load_chromium_page_research_capture()` does not duplicate the file-integrity boundary. It first calls `verify_chromium_page_research_capture()`. Only after that succeeds does it decode the persisted bundle into the established frozen evidence dataclasses.

Rehydration is stricter than file verification because a writer able to alter both payload and digest can create a different self-consistent 16B file. Before typed evidence is emitted, 16C therefore validates exact JSON types and dataclass field sets, established evidence-source strings, endpoint/target/URL coherence, acquisition mode/order, contiguous ordinals, non-negative counts/limits, exact truncation relationships, text bounds, heading levels, literal table cell identity/spans, and literal list/nesting constraints. A checksum-valid capture with a negative link count or boolean where an integer limit belongs passes the 16B self-integrity check but is rejected by 16C.

After typed construction, serializing the reconstructed bundle through its dataclass projection must reproduce the persisted bundle payload exactly. Reopening is lossless and performs no normalization, repair, migration, enrichment, or evidence dropping.

The public result retains both the exact `ChromiumPageResearchCaptureVerificationEvidence` that authorized reopening and the new `ChromiumPageResearchEvidenceBundle`. This deliberately prevents a rehydrated bundle from masquerading as evidence freshly acquired from Chromium. The bundle's facts remain the persisted observations, and they gain no authenticity, publisher/source identity, trusted time, quotation/citation, locator-stability, or atomic-snapshot authority merely because their Python types were reconstructed.

The real-browser acceptance proof now extends the complete durable lifecycle. Pyxis acquires a genuine 16A bundle, persists/verifies it through 16B, explicitly terminates the Chromium process, and only then loads the capture through 16C. The new typed bundle is value-equal to the original live evidence while remaining a distinct new object. Actions #547 on `fd3c16682d6e0c88cf77a09c1aa429ae3049f78d` passed on Python 3.11, 3.12, 3.13, and 3.14. The inspected Python 3.11 log collected **268 tests**, passed all eight research-capture tests and the browser-terminated integration, and finished **268 passed in 40.32s**.

D130 therefore establishes: **an integrity-verified durable Chromium research capture may be reopened as typed application evidence only when the complete persisted nested payload passes exact structural/domain validation and lossless reconstruction. Rehydration must retain the 16B file-verification evidence that authorized the load; the reconstructed bundle is not fresh browser observation and gains no stronger authenticity, source-provenance, temporal, citation, quotation, or atomic-snapshot authority.**

## Human-owned verified-capture paragraph selection — 17A / D131

17A asks whether one already-returned paragraph from verified rehydrated Chromium research evidence can be explicitly chosen by the researcher without Pyxis deciding what matters or strengthening the selected evidence's epistemic status.

The boundary is pure application selection:

```text
ChromiumPageResearchLoadedCaptureEvidence
    ↓
caller supplies exact 1-based paragraph ordinal
    ↓
selection-relevant origin + paragraph coherence
    ↓
require evidence already present in returned bounded prefix
    ↓
ChromiumPageResearchParagraphSelectionEvidence
    ├── exact loaded-capture object
    └── exact existing paragraph object
```

`pyxis.app.select_chromium_research_capture_paragraph()` performs no Chromium call, browser discovery, file read, SHA-256 verification, persistence, ranking, semantic interpretation, or text expansion. The caller supplies the exact ordinal; Pyxis does not choose by authored ID, text similarity, heading context, or model inference.

The returned frozen selection records `selection_mode="caller_explicit_returned_paragraph_ordinal"`. Its `source` field is the exact supplied 16C loaded-capture object, and its `paragraph` field is the exact `ChromiumPageParagraphEvidence` already contained by that source. This prevents selection from becoming a copied quote/citation representation or second source of truth. Duplicate authored IDs therefore cannot redirect an ordinal choice.

Bounded evidence remains bounded. When `paragraph_count` says another paragraph existed but the returned tuple was truncated before that ordinal, selection fails rather than reconnecting to Chromium, rereading the capture, enlarging a prior observation limit, or synthesizing missing text.

Upstream ownership also remains explicit. 16B owns file integrity, 16C owns complete typed rehydration, and 17A validates only the source/paragraph coherence needed for selection. A caller choice is provenance about the researcher's action, not evidence that the chosen passage is relevant, important, true, a verified quotation, a stable citation, authentic source material, or support for a claim.

Actions #556 on `32397e95c22693502004c2228617e03c8ead22f1` passed across Python 3.11, 3.12, 3.13, and 3.14; the inspected Python 3.11 log collected **273 tests** and passed the first five focused 17A tests. Actions #557 on `9f53a1e38d55624b15f0be3eee7ba7dc0dee06f5` passed across all four supported interpreters; the inspected Python 3.11 log collected **274 tests**, passed all six 17A tests including public `persist → load → select` composition, and finished **274 passed in 32.46s**.

D131 therefore establishes: **an explicit caller may select one already-returned paragraph from verified rehydrated Chromium research evidence by exact ordinal, producing a frozen selection that retains the exact loaded-capture evidence object and exact paragraph evidence object. Selection records caller choice only: it does not imply relevance, importance, truth, quotation validity, citation authority, locator stability, source authenticity, or browser-control authority. Evidence outside the bounded returned paragraph prefix must not be reacquired, expanded, or synthesized as a side effect of selection.**

## Measurement state through 11T

The measurement sequence is intentionally descriptive and provenance-heavy:

```text
11A  measured build/run over the established operation
11B  pairwise descriptive comparison
11C  Repository / Workspace / exact RIR subject identity
11D  privacy-preserving runtime-input identity
11E  coarse execution-environment identity
11F  exact-condition cohort
11G  raw stage samples retaining exact BuildWorkEvidence
11H  exact-work partition without semantic labels
11I  sample count / minimum / maximum
11J  median
11K  arithmetic mean independently recomputed from raw durations
11L  population standard deviation for the complete exact group
11M  provenance-checked summary bundle; no new values
11N  read-only summary presentation
11O  presentation-only Textual renderer
11P  optional supplied measurement snapshot in Workspace shell
11Q  Repository / Workspace / exact RIR co-display gate
11R  live invalidation after successful RIR-changing Apply
11S  transient non-evidence invalidation notice
11T  caller-supplied current-RIR presentation may re-enter through the same gate
```

### D107 — 11L

Population standard deviation is descriptive evidence for one exact recorded work-context group. It uses the complete group denominator, retains exact 11K mean provenance, and makes no inferential claim.

### D108 — 11M

The descriptive summary bundle validates source links among the already-existing envelope, median, mean, and dispersion evidence and adds no values.

### D109 — 11N

Measurement summary presentation is a read-only projection of exact 11M evidence. It preserves stage/group order and exact `BuildWorkEvidence` provenance while adding no statistic, semantic work-state label, score, or causal interpretation.

### D110 — 11O

Textual measurement rendering is presentation-only. It receives existing 11N evidence and adds no acquisition, execution, persistence, statistic, label, score, or mutation.

### D111 — 11P

The public Workspace shell may optionally mount an already-supplied 11N measurement presentation through the exact 11O renderer. Existing Workspace operations do not acquire, re-project, refresh, replace, or interpret that snapshot.

### D112 — 11Q

Workspace/measurement co-display requires exact Repository ID, Workspace ID, and RIR SHA-256 coherence before Textual initialization. The gate reads existing evidence only.

### D113 — 11R

A live supplied measurement snapshot remains only while its Repository/Workspace/RIR identity matches current Workspace presentation. Same-RIR and failed operations keep it; successful RIR-changing Apply removes it after Apply succeeds.

### D114 — 11S

Measurement invalidation notices are transient UI status, not evidence. The notice appears only after stale measurement has already been removed, carries no measurement object/statistics or controls, and expires on the next user operation.

### D115 — 11T

While no measurement snapshot is mounted, an already-produced caller-supplied measurement presentation for the current RIR may re-enter the live shell through the existing Repository/Workspace/RIR gate. Successful re-entry mounts the exact supplied object and clears any prior invalidation notice only after mount succeeds. Mismatch or attempted replacement fails before shell evidence changes.

11T adds no measurement acquisition, re-projection, recomputation, refresh control, inferred current measurement, or new statistic.

## Invariants that remain unchanged

- Canonical authoring state is authoritative.
- Compiler output, filesystem materialization, runtime, revision provenance, and export remain separate boundaries.
- Incremental generation status comes from compiler evidence plus integrity checks, not tree scanning or generated-code inference.
- Presentation and Textual render evidence owned elsewhere.
- UI actions cross named application operations.
- Runtime does not compile.
- READY is evidence-derived.
- Measurement work facts come from `BuildResult`; measurement does not rediscover them.
- Cohorts require one exact subject/RIR/workload/environment/stage condition.
- Work-context equality is not renamed into cold/warm/cached/steady-state/outlier semantics.
- Timing/work association is not causal evidence and is not converted into efficiency or waste scoring.
- Concrete architecture semantics remain explicit even where proven orchestration is privately shared.
- A broader architecture-operation abstraction requires new product pressure, not merely a count of existing operations.
- Architecture consequence traces are projections of preview evidence, not new architectural truth or explanatory inference.
- Proposed architecture evidence is never rewritten as observed evidence after Apply.
- Reconciliation reports exact structural agreement or difference; it does not convert agreement into a score, confidence, or causal claim.
- Package compatibility claims remain bounded by explicitly proven interpreter lanes.
- Chromium remains the browser; Pyxis does not infer browser-control authority from read-only observation capability.
- Browser target selection is explicit when multiple pages exist rather than inferred from target ordering or focus heuristics.
- Browser observation evidence is distinct from navigation, interaction, persistence, and interpretation.
- Link DOM order is document-order evidence, not ranking or recommendation.
- Observed href values are not navigation permission, destination selection, or safety classification.
- Heading DOM order and literal h1–h6 levels are page-authored evidence, not a repaired semantic hierarchy.
- Skipped heading levels remain skipped unless a separate future product decision explicitly earns interpretive authority.
- Page-declared language, canonical links, and descriptions remain declarations rather than verified provenance.
- Conflicting metadata declarations remain visible unless a separate future product decision explicitly earns resolution authority.
- Paragraph boundaries remain page-authored DOM evidence rather than Pyxis semantic segmentation.
- Paragraph element IDs remain literal authored strings rather than guaranteed unique/stable citation locators.
- Table DOM order, literal TH/TD identity, and browser-exposed spans remain structure evidence rather than a normalized dataset or inferred header map.
- Span expansion, value typing, dataset normalization, and header relationship inference require separate future authority.
- List DOM order, literal OL/UL identity, authored `start`/`value` strings, and nesting coordinates remain structure evidence rather than corrected numbering or semantic hierarchy.
- Direct-list item text excludes descendant-list text so nested list evidence remains structurally separate rather than silently flattened.
- Research-bundle composition preserves the seven constituent application evidence objects rather than creating a second normalized representation or source of truth.
- Exact endpoint/target/URL agreement across sequential bundle reads is coherence evidence, not proof of one atomic or frozen DOM state.
- Research-capture persistence consumes an existing coherent 16A bundle and never reacquires the page as a hidden side effect of saving.
- A capture SHA-256 is self-integrity evidence, not authentication, source verification, publisher identity, or trusted provenance.
- Persisting or verifying a capture does not strengthen the original sequential/non-atomic browser evidence claim.
- File verification is necessary but not sufficient to emit rehydrated typed evidence; the complete nested payload must satisfy the application evidence contract.
- Typed rehydration must preserve the exact capture-verification evidence that authorized reopening rather than erase durable acquisition origin.
- Reconstructing a `ChromiumPageResearchEvidenceBundle` from disk does not make it a fresh browser observation or add authenticity, provenance, temporal, citation, quotation, or atomic-snapshot authority.
- Explicit passage selection retains exact already-owned source and paragraph evidence rather than copying selected text into a new quotation or citation representation.
- Caller selection is provenance about a human choice, not evidence of relevance, importance, truth, quotation validity, citation authority, locator stability, or source authenticity.
- Evidence outside a bounded returned paragraph tuple is not reacquired, expanded, or synthesized as a side effect of selection.

## Current development discipline

Do **not** continue the 11-series by adding another statistic merely because one is available. The existing descriptive set is sufficient to prove the measurement architecture and its provenance path.

12B closed the abstraction question for the current two operations. 13A proved a user can follow an architecture proposal into code/runtime-contract consequences without Pyxis inventing meaning. 13B separately proves the earlier proposal can be compared with the evidence actually produced after Apply without promoting preview evidence into post-change authority. Do not continue this thread by adding a prediction score, confidence estimate, generated explanation, or generic operation model merely because reconciliation now exists. The next milestone should answer a new concrete Pyxis product question.

14A resolves the previously open Python support mismatch: package metadata is now `>=3.11,<3.15`, and the full suite is proven on Python 3.11, 3.12, 3.13, and 3.14. Do not move the upper bound or add a future interpreter lane merely because a new Python version exists; evaluate it deliberately and expand the support contract only after the complete suite passes.

15A proves the first read-only Chromium observation boundary. Do not immediately grow that proof into navigation, clicks, form submission, arbitrary CDP access, browser-state persistence, autonomous research, LLM interpretation, a generic browser abstraction, or browser UI merely because an existing page can now be observed.

15B proves that the available link choices on the selected page can also be exposed as bounded immutable evidence without following them. Do not convert DOM order into ranking, observed href values into permissions, or this evidence surface into navigation control. Any future destination selection or navigation operation requires its own concrete product question, explicit authority boundary, and proof.

15C proves that literal h1–h6 markers can be exposed as bounded document-structure evidence without semantic repair or summarization. Do not convert heading level into quality, skipped levels into automatically corrected hierarchy, heading text into verified section summaries, or the outline into scrolling/navigation authority. Any future semantic interpretation, accessibility judgment, or browser control requires its own product question and evidence.

15D proves that page-declared language, canonical links, and descriptions can be exposed without being promoted into verified provenance. Do not silently choose among conflicting declarations, normalize authored language into a confidence claim, fetch a declared canonical destination, or turn metadata presence into source-quality evidence. Any future provenance verification or conflict resolution requires its own concrete product question and independently owned evidence.

15E proves that authored `<p>` elements can be exposed as bounded passage-level evidence without semantic segmentation. Do not turn paragraph ordinals into relevance ranking, paragraph IDs into stable citation keys, or rendered paragraph text into a verified quotation claim. Any future citation/quotation verification, locator stability, semantic passage extraction, or browser control requires its own product question and evidence.

15F proves that literal HTML-table structure can be exposed as bounded nested evidence without turning that structure into an invented dataset. Do not infer header-to-cell relationships, expand spans into synthesized grid coordinates, flatten tables into CSV-like rows, coerce rendered strings into typed values, or rank tables merely because the structure is visible. Any future table normalization, schema inference, typed-data extraction, or browser control requires its own product question and evidence.

15G proves that literal ordered/unordered-list structure can be exposed without flattening nested lists or inventing semantic hierarchy. Do not repair authored numbering, calculate displayed counters, normalize invalid `start`/`value` attributes, interpret nested lists as substeps/dependencies/priorities, or merge descendant-list text into parent-item evidence merely because the DOM relationship is visible. Any future semantic outline, list normalization, priority inference, or browser control requires its own product question and evidence.

16A proves the seven existing browser evidence families can be composed for research convenience without being promoted into one atomic snapshot. Do not add a DOM-freeze claim, page-version identity, semantic cross-family join, citation verifier, source verifier, browser-agent loop, generalized evidence-query language, or navigation/control surface merely because the bundle makes those directions convenient. Any such capability needs its own product pressure, authority boundary, and proof.

16B proves an already-completed bundle can be preserved durably without turning persistence into reacquisition, interpretation, authentication, or stronger browser evidence. Do not infer observation time from file mtime/save time, treat the embedded digest as cryptographic authorship, add silent overwrite/update semantics, or create a capture database/index merely because one deterministic file format exists.

16C proves that verified durable evidence can re-enter the typed application layer without Chromium, while file integrity and nested evidence validity remain separate gates and acquisition origin remains visible. Do not treat typed reopening as permission for indexing/search, cross-capture comparison, signed provenance, source verification, quotation/citation verification, semantic interpretation, autonomous research, or researcher UI.

17A proves one caller-owned single-paragraph selection from a verified loaded capture. Do not generalize it into multi-selection sets, a generic evidence-family selection registry, persisted selections, annotation/notes/claims/questions, relevance ranking, quotation/citation verification, semantic interpretation, or UI merely because one explicit human-owned choice is now representable. Each such capability needs its own concrete researcher pressure, authority boundary, and proof.

## Why the older central status lines are not being rewritten now

`MILESTONE_11K_CONTINUITY.md` already records that the connector rejected the large replacements required to fold 11K into the central documents. The same limitation remains. Whole-file replacement of the central architecture/archive was tested again during 11T continuity work, and the resulting diff would have removed large amounts of historical reasoning from their canonical paths. That approach was abandoned.

Until a safe line-patch workflow is available, `CURRENT_STATE.md` is the single current overlay. It is intentionally small, explicit, and reversible. The preserved large documents plus milestone proofs remain the detailed evidence base.