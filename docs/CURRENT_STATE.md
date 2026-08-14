# Pyxis Current State

**Continuity front door — Pyxis current through Milestone 15B / D122 (2026-08-14).**

This file exists because the GitHub connector cannot safely apply line-level edits to the already-large `ARCHITECTURE.md` and `DEVELOPMENT_ARCHIVE.md`. A prior attempt to replace those files wholesale produced a deletion-heavy diff and was deliberately abandoned rather than normalize a historical rewrite.

Nothing here supersedes proven historical evidence. It provides one current map over the preserved central documents and the later milestone records.

## Read order

For a new development session, read in this order:

1. `README.md`
2. this file (`docs/CURRENT_STATE.md`)
3. `docs/ARCHITECTURE.md`
4. `docs/DECISIONS.md`
5. `docs/DEVELOPMENT_ARCHIVE.md`
6. `docs/MILESTONE_11K_CONTINUITY.md`, `docs/MILESTONE_11L.md` through `docs/MILESTONE_11T.md`, then `docs/MILESTONE_12A.md`, `docs/MILESTONE_12B.md`, `docs/MILESTONE_13A.md`, `docs/MILESTONE_13B.md`, `docs/MILESTONE_14A.md`, `docs/MILESTONE_15A.md`, and `docs/MILESTONE_15B.md`

The large central documents remain intact historical/current foundations. Their status headers lag later implementation because the connector could not safely patch them in place. This file makes those later deltas explicit in one place rather than requiring a future session to rediscover the gap.

## Current Pyxis checkpoint

Pyxis now has ten proven families. The first eight remain the Repository Zero reference spine; 15A and 15B add two concrete browser-facing evidence boundaries without changing that spine:

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

## Current development discipline

Do **not** continue the 11-series by adding another statistic merely because one is available. The existing descriptive set is sufficient to prove the measurement architecture and its provenance path.

12B closed the abstraction question for the current two operations. 13A proved a user can follow an architecture proposal into code/runtime-contract consequences without Pyxis inventing meaning. 13B separately proves the earlier proposal can be compared with the evidence actually produced after Apply without promoting preview evidence into post-change authority. Do not continue this thread by adding a prediction score, confidence estimate, generated explanation, or generic operation model merely because reconciliation now exists. The next milestone should answer a new concrete Pyxis product question.

14A resolves the previously open Python support mismatch: package metadata is now `>=3.11,<3.15`, and the full suite is proven on Python 3.11, 3.12, 3.13, and 3.14. Do not move the upper bound or add a future interpreter lane merely because a new Python version exists; evaluate it deliberately and expand the support contract only after the complete suite passes.

15A proves the first read-only Chromium observation boundary. Do not immediately grow that proof into navigation, clicks, form submission, arbitrary CDP access, browser-state persistence, autonomous research, LLM interpretation, a generic browser abstraction, or browser UI merely because an existing page can now be observed.

15B proves that the available link choices on the selected page can also be exposed as bounded immutable evidence without following them. Do not convert DOM order into ranking, observed href values into permissions, or this evidence surface into navigation control. Any future destination selection or navigation operation requires its own concrete product question, explicit authority boundary, and proof.

## Why the older central status lines are not being rewritten now

`MILESTONE_11K_CONTINUITY.md` already records that the connector rejected the large replacements required to fold 11K into the central documents. The same limitation remains. Whole-file replacement of the central architecture/archive was tested again during 11T continuity work, and the resulting diff would have removed large amounts of historical reasoning from their canonical paths. That approach was abandoned.

Until a safe line-patch workflow is available, `CURRENT_STATE.md` is the single current overlay. It is intentionally small, explicit, and reversible. The preserved large documents plus milestone proofs remain the detailed evidence base.