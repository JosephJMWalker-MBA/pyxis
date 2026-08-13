# Pyxis Development Archive

**Continuity snapshot — 2026-08-11; Repository Zero status updated through Milestone 11G on 2026-08-12**

This document preserves the reasoning that produced Pyxis, not just the current code. It exists so a future development session can continue from the accumulated lessons instead of rediscovering them or flattening the project into a generic code generator.

It should be read alongside:

- `ARCHITECTURE.md` — current architectural boundaries
- `DECISIONS.md` — implementation decisions already treated as constraints
- the source tree — the permanent Repository Zero implementation

---

## 1. What Pyxis became

Pyxis began as a Python-first browser/research harness: keep Chromium for the mature browser work it already does well, then expose Python capabilities around it instead of rebuilding a browser from scratch.

That starting point produced a broader engineering thesis:

> Python already provides enormous capability. Pyxis should conserve effort by composing existing strengths, make the transformations visible, and measure the cost of getting from intent to execution.

During prototyping, the center of gravity became clearer. The strongest reusable idea was not any one browser feature. It was the transparent path from human architectural intent to executable software:

```text
human intent
    ↓
canonical authoring state
    ↓
Repository Intermediate Representation (RIR)
    ↓
compiler
    ↓
generated implementation
    ↓
runtime
```

The browser/research product remains a foreseeable application of that architecture, but Repository Zero deliberately proves the compiler path first with a tiny `text_lab` Workspace.

`inspect_text` and `normalize_text` are not the product domain. They are controlled test weights for the architecture.

---

## 2. Product principles that survived implementation pressure

These principles repeatedly survived real implementation tests and should be treated as durable unless contrary evidence appears.

### 2.1 Chromium should remain Chromium

Pyxis should not spend engineering effort recreating mature browser infrastructure. Browser integration should eventually compose with Chromium rather than replace it.

### 2.2 Python-first does not mean Python-only ideology

Python is the preferred orchestration and capability language because of its ecosystem, readability, and usefulness as an educational surface. The deeper rule is to use mature tools rather than rebuild them unnecessarily.

### 2.3 Human intent must remain visible

A user should be able to trace:

```text
I asked for this
      ↓
Pyxis represented it this way
      ↓
therefore these compiler nodes exist
      ↓
therefore these files exist
      ↓
therefore this runtime behavior exists
```

If the system cannot explain that path, it is drifting away from the original value proposition.

### 2.4 Canonical source is authoritative

Generated code is a consequence, not a second source of truth.

UI actions, restore actions, export actions, and educational lessons must not patch generated files to simulate architectural change.

### 2.5 The compiler should be inspectable and deterministic

The same canonical state should lower to the same RIR and the same RIR should produce the same compiler products.

This is necessary for explanation, provenance, caching, waste measurement, testing, and safe revision behavior.

### 2.6 Evidence beats inference

Whenever the compiler already knows what happened, the UI should render that fact rather than infer it from Git, timestamps, filesystem shape, or heuristics.

Examples include artifact statuses such as `new`, `reused`, `regenerated`, and `removed`.

### 2.7 Changes should be previewed before mutation

Architectural edits should first produce a proposed canonical/RIR state and show their consequences.

Preview may derive and compare. It may not mutate.

### 2.8 Human rationale is part of provenance

A structural diff explains *what* changed. It does not explain *why*.

Architectural revisions therefore need an intent-bearing rationale before compilation.

### 2.9 History is append-only

Restore is not rollback. Reapply is not history rewriting.

Returning to an earlier architecture should create a new revision whose state happens to match an earlier state. The intervening history remains intact.

### 2.10 Export is packaging, not compilation

Portable output must package the exact compiler products that already ran inside Pyxis.

Export must not regenerate, reinterpret, or patch implementation.

### 2.11 READY is evidence-derived

A UI may show READY only because verification evidence says the output is ready, not because files happen to exist.

### 2.12 Pyxis should teach by being inspectable

The educational opportunity is not a tutorial bolted onto a code generator.

A transparent compiler lets users learn Python and software architecture by observing real consequences of real changes.

### 2.13 Presentation should render owned evidence, not rediscover state

A user interface should receive a read-only application contract assembled from canonical, compiler, runtime, revision, and verification evidence Pyxis already owns.

Presentation may validate coherence between evidence streams. It must not scan files, infer compiler status, execute code, or manufacture READY state.

### 2.14 Durable and transient evidence should remain distinct

Reopening a Workspace does not make every prior fact reconstructible.

Canonical state, persisted RIR, generation manifests, and revision logs have explicit persistence boundaries and may be reloaded. Runtime results, generation statuses, and export READY evidence are transient in Repository Zero unless the real application operation that produced them is still available.

The existence of implementation files must not be used to reverse-engineer those transient facts.

### 2.15 Evidence visibility should precede UI mutation

Before a Workspace UI is allowed to change anything, it should prove that the user can inspect the complete evidence contract already owned by the application.

A mutation control should therefore arrive only after canonical intent, RIR, compiler consequences, runtime results, revision provenance, and optional READY evidence can all be rendered without inference or hidden application work.

### 2.16 UI actions should cross named application operations

A renderer event is not permission to bypass the application boundary.

Before a visible control is connected, the intended action should exist as an independently testable application operation with explicit inputs, coherence checks, side effects, and fresh returned evidence. The renderer should receive application results rather than compiler/runtime/revision/export services.

### 2.17 Transient operation state belongs outside the renderer

A rendered presentation is not enough to perform the next stateful operation. If an application action returns fresh transient evidence, the application/controller layer should retain it directly.

The UI may retain the current presentation for rendering, but it should not reconstruct `BuildAndRunResult` or other live operation inputs from visible fields.

### 2.18 Proposed architecture is not current Workspace state

A preview may be retained as pending application state without changing what the Workspace currently is.

Current runtime evidence, compiler evidence, revision history, and READY evidence remain current until a rationale-bearing apply operation actually commits new canonical intent. The UI must visually and semantically distinguish proposed preview evidence from current Workspace evidence.

### 2.19 Visible preview does not imply mutation permission

Showing a proposed architecture in the real UI is still part of preview, not apply.

The visible preview surface should be clearly labeled as proposed/not applied, and current Workspace evidence should remain unchanged beside it. Rationale and Apply controls arrive only after the application layer proves the mutation operation that will own them.

### 2.20 Apply consumes retained intent and resets invalid transient verification

Once a preview is approved, Apply must consume the exact typed proposal that was shown rather than reconstructing intent from display text.

A successful architectural change creates new canonical/RIR/compiler identity. Fresh runtime evidence must be produced for that new build, while pre-change READY evidence stops being current even if the old portable files remain on disk.

Application state should advance only from fresh operation results. If multiple controllers retain independent copies of the same live run/export evidence, architectural mutation can make them diverge; visible mutation should therefore wait until one application-owned live-state authority coordinates both runtime and architecture operations.

### 2.21 Combined interaction state has one application authority

Runtime rerun, architecture preview, and architecture apply all consume the same transient current Workspace evidence. Once those operations can occur in one user session, the application layer must own one current run, one optional current READY result, and one optional pending architecture preview.

The renderer should not synchronize sibling controllers or infer which transient copy is newest. Successful operations advance the one application-owned state; failed operations leave it unchanged.

### 2.22 The renderer should receive that authority once

Once the shared live-state authority exists, the renderer should not preserve separate runtime and architecture controller inputs as a second synchronization problem.

A combined interactive shell receives one `WorkspaceController`. Runtime submission and architectural Preview route through that same object, so later operations inherit the application-owned ordering already proven below the UI. Read-only rendering still requires no controller at all.

### 2.23 Visible mutation should advance only from successful evidence

A renderer must not optimistically turn a pending proposal into current state merely because the user pressed Apply.

Rationale collection and the button event are UI concerns; rationale validation, retained-preview consumption, governed revision/build/runtime work, and READY invalidation remain application concerns. The UI replaces current evidence and clears proposed evidence only after the unified controller returns a fresh successful `WorkspacePresentation`. Failed or empty rationale leaves both evidence surfaces unchanged.

### 2.24 READY recovery is a verified state transition

Once architectural mutation correctly retires prior READY evidence, the live Workspace may regain READY only by producing a new verified export for its current compiler products.

A portable directory on disk is not a recovery mechanism. The application must preflight the current run, export the exact current `BuildResult` through the existing packaging path, verify identity and runtime behavior, and retain the resulting `WorkspaceExportResult` only after success. Failed refresh attempts leave current live state unchanged.

### 2.25 Visible READY recovery is evidence-gated

A renderer may use the absence of current READY evidence to decide whether a recovery control should be offered, but that does not make the renderer an evidence producer.

The export control appears because `WorkspacePresentation.export` is absent, not because Textual inspects the filesystem. It disappears only after `WorkspaceController.refresh_export()` returns a fresh presentation containing genuine READY verification evidence. Failed export attempts change only non-evidence interaction status and leave current presentation/controller state untouched.

### 2.26 Measurement should observe before it interprets

Measurement should attach to stable application boundaries rather than create alternate execution paths, and it should reuse work facts already owned by the compiler/materializer rather than infer them again.

New timing evidence may be observed with an explicit clock. Existing generation and materialization evidence should pass through unchanged. Interpretation such as efficiency, causality, or waste should be introduced only after the underlying observations are stable enough to support it.

### 2.27 Comparison is still observation, not explanation

Once two measured cycles exist, Pyxis may align their matching stages and compiler/materializer facts and state literal differences between them.

A duration delta is only `after - before`. A path status transition such as `new → reused` is only the transition the compiler reported. Seeing those facts in the same comparison does not prove one caused the other, and the comparison boundary should not smuggle in labels such as faster, better, efficient, or wasteful before an evidence model can justify them.

### 2.28 Measurement identity should be explicit before comparison grows

A measurement should carry the logical Workspace it belongs to and the exact architectural state that produced it rather than relying on caller memory.

Repository/Workspace identity and RIR identity already exist in `BuildResult` evidence. Measurement should reuse and cross-check those facts. Comparisons may span architectural revisions of one logical Workspace, but unrelated Workspace subjects must be rejected before timing or work deltas are constructed.

### 2.29 Runtime workload identity is separate from Workspace identity

Two observations can belong to the same logical Workspace and RIR while exercising different runtime inputs. Measurement should make that workload difference explicit without retaining raw user text unnecessarily.

A deterministic digest plus size evidence is enough to state whether the exact observed inputs match. Input mismatch should remain a descriptive confound rather than becoming either a comparison rejection or a performance explanation.

### 2.30 Execution environment identity is context, not telemetry

Two observations can share Workspace, RIR, and runtime workload identity while being produced by different Python/platform environments. Measurement should expose that execution-context difference without collecting host identity or dynamic machine telemetry.

The environment record should be coarse, immutable, and acquired outside the stages being timed. A mismatch remains a descriptive confound rather than a comparison rejection or causal explanation, and a match does not prove that unrecorded dynamic conditions were controlled.

### 2.31 Cohort membership is stricter than pairwise comparability

Pairwise comparison and repeated sampling answer different questions. Two coherent Workspace observations may be compared even when architecture, workload, or environment differs, because the mismatch itself is useful evidence. A repeated-measurement cohort instead claims that multiple observations belong to one exact measurement condition.

Before any future aggregation, cohort membership must therefore require the same logical Workspace, exact RIR identity, runtime-input evidence, execution-environment evidence, and ordered stage contract. Timing and build-work differences remain observations inside that condition rather than being used to decide membership.

### 2.32 Raw samples should preserve work context before summary

A coherent cohort is not yet permission to turn stage durations into context-free numeric vectors.

Before any summary statistic is introduced, each raw stage duration should remain paired with the exact compiler/materializer work evidence from the cycle that produced it. This preserves observed differences such as a first `new` build with writes and later `reused` builds with no generated writes without assigning those differences a causal label.

---

## 3. The broad architecture explored before Repository Zero

Before the current minimum slice was chosen, a larger architecture was developed. It is intentionally archived here so it is not lost, while remaining deferred until the core path is stable.

### Capability Cards

Capabilities were described by explicit purpose, inputs, and outputs rather than hidden ad hoc functions.

### Execution Graphs

Runtime work was modeled as explicit graph structure rather than opaque orchestration.

### Observation Pipeline

A recurring pipeline was defined as:

```text
Acquire → Assess → Observe → Normalize → Correlate → Present
```

This came from browser/research and OCR work where preserving what was observed separately from what was concluded proved important.

### Immutable Evidence Objects

Evidence should carry provenance, confidence, timestamps, spatial relationships where relevant, and stable identity.

### Rule Engine and Finding Objects

Rules consume evidence and produce findings. Rules do not mutate the evidence they inspect.

### Workspace Sessions

A Workspace session was envisioned as a timeline of snapshots, permissions, metrics, evidence references, and outputs.

### Explicit state machines

Mutable entities should have declared lifecycle transitions rather than informal status changes.

### Capability Test Harness

Capabilities should eventually ship with fixture, contract, security, and performance tests.

### Service Registry / dependency injection

External services and model providers should remain replaceable rather than being hardwired into capability logic.

### Capability Lifecycle

The explored lifecycle was:

```text
Proposed
→ Designed
→ Scaffolded
→ Implemented
→ Verified
→ Certified
→ Stable
→ Deprecated
→ Archived
```

### Planning Graph separate from Execution Graph

The plan for what should happen and the record of what did happen are different objects and should not be collapsed.

### Execution Ledger

Time, resource use, cache behavior, service calls, and avoidable work were intended to become machine-accounted evidence rather than vague performance impressions.

### Bootstrap Specification

A declarative bootstrap document was explored as the source for repository generation.

### Capability Registry

Capabilities should eventually be explicit registry entries rather than discovered implicitly from filesystem shape.

### Canonical Repository Layout

A larger repository organization was explored around Governance, Knowledge, Runtime, Capabilities, Interfaces, Quality, and Documentation.

### Capability Composition Specification

Atomic capabilities and declarative workflows should be separable.

### Canonical Data Model

The larger data model considered Identity, Configuration, Planning, Execution, Evidence, Evaluation, Artifacts, and Governance.

### Repository Constitution

A highest-level governance document was envisioned to declare architectural rules that lower-level generators may not violate.

None of these concepts are discarded. They are intentionally downstream of Repository Zero.

---

## 4. What implementation taught us

The most valuable lessons did not come from naming abstractions. They came from repeatedly forcing the architecture through small executable proofs.

### 4.1 A lesson must change canonical state, not fake generated output

The first useful educational proof removed `normalize_text` from canonical architecture and let the compiler propagate the consequence.

This established a durable rule:

> Educational lessons must invoke the real architecture path.

Otherwise the learner is being shown theater rather than the system.

### 4.2 Performance metrics need a human journey

Timing and waste became useful only when attached to a concrete workflow such as first compile → first run → guided edit → recompile.

Abstract compiler benchmarks did not explain whether the product was wasting the user's time.

### 4.3 Full-tree regeneration created measurable waste

A guided change that removed one capability exposed unnecessary regeneration of unaffected code.

That led to node-level semantic fingerprints and artifact integrity checks.

The important rule was not simply “cache files.” It was:

> Reuse is valid only when the semantic node is unchanged *and* the existing generated artifact still matches the compiler's recorded artifact hash.

This prevents a manually altered generated file from being silently accepted as reusable compiler output.

### 4.4 Incremental status belongs to the compiler contract

`new`, `reused`, `regenerated`, and `removed` are not UI guesses. They are compiler facts.

The UI should display compiler explanations directly.

### 4.5 Restoration must pass through current intent

Restoring `normalize_text` by recovering an old generated file would have violated the architecture.

The correct path is current canonical intent → RIR → compiler → new generated artifact.

This distinction became the foundation for safe revision history.

### 4.6 Git is useful but not sufficient provenance

Git can record file changes. It does not inherently capture the user's architectural rationale, proposed state, compiler consequence, or runtime consequence in the product model.

Pyxis therefore explored its own append-only revision events while still expecting Git to remain useful repository infrastructure.

### 4.7 Reapply is state reproduction, not rollback

A prior canonical state can be selected and reproduced as a new revision.

That preserves the full path:

```text
remove → restore → reapply
```

rather than pretending the middle event never happened.

### 4.8 Preview can predict structure, but should not invent a shadow runtime

Pyxis can safely predict observable behavior that follows directly from canonical structure—for example, which capability result keys will exist.

It should not simulate generated implementation details in a parallel “preview runtime.”

### 4.9 Consolidation became more valuable than new abstractions

A series of small proofs eventually created a new risk: fragmentation.

The response was to stop creating one-off demonstrators and require each proven concept to participate in one coherent first-run path.

This was the transition from prototypes to Repository Zero.

### 4.10 Portability became a compiler-ownership test

If an exported Workspace can run independently while preserving the same RIR identity and artifact hashes, that is evidence that implementation truly belongs to the compiler products rather than hidden Pyxis runtime magic.

### 4.11 Packaging exposed an honest environment constraint

An early clean-install proof failed because the target virtual environment did not contain `setuptools`.

The lesson was important: do not weaken acceptance criteria or claim success around infrastructure gaps.

The prototype was eventually made self-contained enough to prove a network-disabled clean installation using a tiny local standard-library build backend.

That proof is useful history, but Repository Zero should still prefer conventional tooling where it is available rather than making bespoke packaging infrastructure part of the core product prematurely.

Repository Zero later separated source-build evidence from installation evidence. A conventional source package builds a standard wheel using ordinary PEP 517 build isolation when build dependencies are obtainable. The verified wheel can then be installed and executed in a fresh virtual environment while network access is actively blocked. Because installation consumes a prebuilt wheel, Setuptools is not needed during that installation proof.

Milestone 9M tested the stronger source-build condition directly. The exact planned package bytes were copied into a disposable build context, normal PEP 517 build isolation was preserved, index/network access was disabled, and no vendored dependency, fallback backend, or workaround was supplied. The build failed before producing a wheel because the isolated environment could not resolve `setuptools>=77.0.3`.

Milestone 9N then resolved the requirement rather than changing packaging: offline rebuilding from raw source is not part of the Repository Zero portable contract. The portable deliverable is the conventional source repository plus the already-verified wheel. Offline guarantees attach to installation and execution of that verified wheel.

### 4.12 Presentation exposed a new ownership boundary

Milestone 10A asked a simple question before any UI framework was chosen: what facts should the UI actually receive?

The answer reinforced the architecture. Canonical identity must come from `WorkspaceSpec`, not from RIR copies. Compiler status must come from generation evidence, not file scans. Revision intent and completion must remain separate. READY must exist only when export verification already produced it. Runtime evidence should be immutable once handed to presentation.

That produced a pure `WorkspacePresentation` adapter instead of a UI-specific query layer.

### 4.13 Reopening a Workspace exposed the durable/transient boundary

Milestone 10B then asked how that presentation should be assembled for an existing Workspace.

The answer was not “read more files.” Canonical state, persisted RIR, generation manifests, and revision logs are durable because they have explicit persistence owners. Runtime results, compiler generation statuses, and READY are not durable simply because related files happen to remain on disk.

The permanent query therefore reloads only owned durable evidence, requires a supplied current `BuildAndRunResult`, and includes export READY evidence only when the actual `WorkspaceExportResult` is supplied. Persisted RIR/manifest identity must agree with the live run before the streams can be combined.

This prevents a reopened UI from manufacturing certainty after process loss.

### 4.14 The UI framework should be selected after the application boundary

Milestone 10C evaluated Textual, NiceGUI, PySide6, Streamlit, and Flet only after `WorkspacePresentation` and the existing-Workspace query boundary were already established.

Textual was selected for the first local evidence UI because it kept the first rendering surface Python-native, local, optional, and directly testable through the existing pytest path without forcing a browser/server, native Qt deployment surface, whole-script rerun model, or Flutter toolchain into Repository Zero.

The important lesson is not “Textual everywhere.” It is that renderer selection should happen after application ownership is clear, so a future renderer can change without changing product truth.

### 4.15 Complete evidence should be visible before actions are wired

Milestone 10D replaced the boot summary as the only visible UI proof with a genuine read-only Workspace detail screen.

The screen renders the complete current `WorkspacePresentation`: canonical intent, RIR, compiler artifacts/statuses, runtime output, revision timeline, and optional READY export verification. It deliberately has no mutation buttons or callbacks.

This exposed a useful sequencing rule: first prove that the user can inspect the evidence chain end to end; only then connect interface events back to named application operations.

### 4.16 The first UI operation should prove action ownership without architecture mutation

Milestone 10E deliberately chose runtime rerun rather than a rationale-bearing architectural edit for the first UI operation seam.

`rerun_workspace()` first preflights the caller's live run/export evidence through the existing Workspace query. Only coherent evidence may reach runtime. It then executes the existing materialized Workspace exactly once, reuses the same `BuildResult`, and returns both fresh transient run evidence and a fresh immutable presentation.

This isolates the event-boundary lesson from revision semantics: before the UI is allowed to change architecture, it proves that an ordinary user action can cross a named application operation without Textual acquiring runtime or compiler services.

### 4.17 The first visible interaction should change only the evidence it owns

Milestone 10F connected one Textual `Input.Submitted` event to the already-proven runtime rerun operation through `WorkspaceRuntimeController`.

The controller retains the current `BuildAndRunResult`; Textual retains only the current presentation for rendering. After submission, runtime evidence changes on screen while canonical intent, RIR identity, compiler status, revision provenance, and export verification remain exactly the same evidence.

That separation proves a complete event loop without giving the renderer ownership of transient application state or broader domain services.

### 4.18 Preview state must remain visibly proposed until apply

Milestone 10G carries the preview-first rule across the UI boundary without introducing any mutation control.

`preview_workspace_remove_normalize_text()` first proves that the supplied live run/READY evidence still belongs to the persisted Workspace, then reloads canonical intent and uses the existing in-memory architectural preview. `ArchitecturePreviewPresentation` exposes only current/proposed canonical hashes, capability deltas, predicted artifact-path consequences, and predicted runtime-key consequences.

The controller retains the typed `ArchitecturePreview` for a later rationale/apply operation, but the existing Workspace presentation remains current. That distinction prevents a preview from silently becoming a speculative replacement for canonical, runtime, revision, or READY evidence.

### 4.19 A visible preview should still leave the user in a reversible pre-commit state

Milestone 10H makes the proposed architecture visible without crossing into mutation.

The new Textual button calls only `WorkspaceArchitecturePreviewController.preview_remove_normalize_text()`. `ArchitecturePreviewDetail` renders the returned proposed evidence in a separate panel marked `PROPOSED — NOT APPLIED`, while `WorkspaceDetail` continues to show the unchanged current Workspace and READY evidence.

The important lesson is sequencing: seeing a consequence is not the same as authorizing it. Rationale collection and Apply must still be introduced through a separately tested application operation before the renderer may mutate canonical state.

### 4.20 Architectural mutation exposes shared live-state pressure

Milestone 10I proves the actual application-owned transition from shown proposal to committed architecture.

`apply_workspace_remove_normalize_text()` consumes the exact typed preview retained by the controller, requires rationale, preflights current run/READY evidence, delegates revision/canonical/compiler mutation to the existing governed apply path, executes the new materialized Workspace once, and returns fresh run/presentation evidence. The old READY proof is deliberately omitted from that new presentation.

The controller advances its run evidence and clears export/pending-preview state only after successful operation return. That result also reveals a new constraint for the future UI: `WorkspaceRuntimeController` and `WorkspaceArchitecturePreviewController` currently hold independent copies of live run/export evidence. Once architecture can mutate, those copies can diverge. The renderer should not become responsible for synchronizing them. Before visible Apply is introduced, a single application-owned live-state authority should coordinate runtime rerun, preview, and apply.

### 4.21 One live authority makes cross-operation sequencing explicit

Milestone 10J resolves that duplicated-state pressure with `WorkspaceController`.

The controller retains one current `BuildAndRunResult`, one optional current `WorkspaceExportResult`, and one optional pending `ArchitecturePreview`. It delegates runtime, preview, and apply behavior to the existing application operations rather than reimplementing them.

The acceptance path proves object-identity handoff across `rerun → preview → apply → rerun`: the run returned by the first rerun is exactly the run consumed by Preview and Apply; the run returned by Apply is exactly the run consumed by the final rerun. READY remains current across runtime-only work and is cleared by architectural mutation. Failed Apply leaves all shared state unchanged.

### 4.22 Renderer migration should preserve ordering evidence, not simulate synchronization

Milestone 10K moves the already-visible runtime and Preview interactions onto the same `WorkspaceController` rather than adding synchronization code between the earlier specialized controllers.

The headless UI proof submits runtime text first and then requests Preview. It verifies by object identity that Preview receives the exact fresh `BuildAndRunResult` produced by the preceding runtime operation, while READY remains the same valid pre-change evidence and the proposed architecture remains confined to `PROPOSED — NOT APPLIED` presentation.

This is the last state-ownership prerequisite before visible architectural mutation: the application owns one live state, and the renderer now receives that authority once.

### 4.23 Visible Apply should be a commit boundary, not optimistic UI state

Milestone 10L connects one rationale-bearing Apply control only after the proposed architecture already exists and is visible.

The runtime text passed to Apply comes directly from the visible runtime input; the proposal comes from the controller's retained typed `ArchitecturePreview`; and rationale validation remains in the application operation. Textual waits for `WorkspaceController.apply_pending_remove_normalize_text()` to return before replacing `WorkspaceDetail` or clearing `ArchitecturePreviewDetail`.

The acceptance path proves success and failure asymmetrically. Success reveals the new canonical/RIR/compiler/runtime/revision evidence and drops pre-change READY. Empty rationale or a simulated governed-apply failure leaves the current presentation, proposed presentation, controller run/export/pending-preview state, and repository bytes unchanged. Only a non-evidence status message changes.

### 4.24 READY recovery should reuse verification ownership

Milestone 10M closes the live-state loop after architectural mutation without weakening the meaning of READY.

`refresh_workspace_export()` first proves the supplied current run still matches persisted Workspace evidence. It then passes that exact run's `BuildResult` to the existing `export_workspace()` path, which continues to own planning, exact-byte materialization, identity verification, runtime equivalence, and READY. The application controller retains the returned export evidence only after the entire operation succeeds.

The acceptance path proves the post-Apply `BuildResult` is used by object identity, compilation is unavailable, stale run evidence fails before export begins, occupied destinations are rejected by the existing materializer, source/revision state is unchanged by export, and failed refresh does not partially restore READY.

### 4.25 Visible export closes the first UI lifecycle without making Textual an export layer

Milestone 10N connects the already-proven export-refresh operation to one evidence-gated Textual surface.

The real headless path starts READY, performs visible Preview → rationale → Apply, observes `No READY evidence`, enters an explicit fresh destination, and invokes Export/Verify. Instrumentation proves the export operation receives the exact post-Apply `BuildAndRunResult` plus the current visible runtime text; compilation is unavailable during export. Genuine READY then returns from the application operation and replaces current detail evidence.

The failure proof uses an occupied destination. The controller's run/export/pending-preview state and the current `WorkspacePresentation` remain unchanged; only a non-evidence status message changes. Textual never scans the destination, invents READY, overwrites output, or cleans it up.

### 4.26 Measurement should share the permanent operation rather than copy it

Milestone 11A reintroduces timing only after the first Workspace lifecycle is stable.

The first attempt could easily have become a second two-step orchestrator that called `build_workspace()` and `run_materialized_workspace()` itself. Instead, `build_and_run_workspace()` gained only a private stage-observer seam, and `measure_build_and_run_workspace()` invokes that existing operation exactly once. This keeps execution ownership in one place while still exposing exact `build` and `runtime` timing boundaries.

The fake-clock proof makes stage durations deterministic. The work side of the measurement does not infer anything: `generation_statuses`, `written_paths`, `reused_paths`, and `removed_paths` are the exact tuple objects already returned by `BuildResult`. A real incremental removal case proves `reused`, `regenerated`, and `removed` evidence pass through unchanged.

The lesson is to separate observation from interpretation. 11A records time and owned work facts; it does not yet say that one duration caused another, label any work as waste, persist a ledger, or render metrics in the UI.

### 4.27 A comparison can expose association without claiming cause

Milestone 11B compares two real measured cycles without introducing another execution boundary.

A first build and an identical rebuild of the same Workspace naturally produce different compiler/materializer evidence: the first cycle reports `new` artifacts and writes them, while the second reports `reused` artifacts and performs no generated writes. Fake clocks independently make the second build/runtime durations lower in the acceptance fixture.

`compare_build_and_run_measurements()` reports those facts side by side and calculates only arithmetic `after - before` duration deltas. It performs no timing, compilation, runtime execution, filesystem access, or work reclassification. The important restraint is semantic: the coexistence of more reuse and lower duration in this pair is a correlation in two observations, not a demonstrated causal effect and not yet a waste/efficiency judgment.

### 4.28 Subject identity is part of measurement coherence

Milestone 11C exposes a distinction the pairwise comparison previously relied on the caller to remember: two observations can be comparable as the same logical Workspace even when they represent different architectural states.

`MeasurementSubjectEvidence` therefore carries Repository ID, Workspace ID, and the exact RIR SHA-256. The RIR hash is cross-checked against the generation manifest before it becomes measurement evidence. Comparison then revalidates each retained subject against its own `BuildResult` before creating any timing or work deltas.

The resulting rule is narrow but important: same Repository/Workspace identity permits comparison across different RIR hashes; different logical subjects fail before comparison evidence is constructed; and replacing subject metadata cannot override the build evidence beneath it.

### 4.29 Runtime input identity reveals a comparability confound without storing payload

Milestone 11D makes the explicit runtime text measurable without turning measurement into payload storage.

`RuntimeInputEvidence` records SHA-256 over the exact UTF-8 bytes plus Unicode character count and UTF-8 byte count. The raw text still reaches the established runtime operation, but no raw-input field is retained in measurement evidence. A Unicode acceptance fixture proves character count and encoded byte count remain distinct facts.

Comparison carries the exact before/after input evidence and a literal `matches` flag. Matching input evidence does not prove timing comparability by itself; differing input evidence does not invalidate the comparison. It exposes that workload identity changed so later analysis cannot quietly treat the runtime conditions as controlled.

### 4.30 Environment evidence belongs outside the stages being measured

Milestone 11E adds execution context without contaminating the durations it is supposed to contextualize.

`measure_build_and_run_workspace()` accepts an injectable environment provider and calls it exactly once before `build_and_run_workspace()` begins emitting stage boundaries. The acceptance proof records the acquisition event before all four fake-clock reads, making the timing separation explicit rather than assumed.

The retained `ExecutionEnvironmentEvidence` is deliberately coarse: Python implementation/version and platform system/machine only. Comparison carries exact before/after environment objects and a literal `matches` flag; mismatch remains descriptively comparable, while neither match nor mismatch is treated as a cause of duration change.

### 4.31 Repeated observations need a condition boundary before they need statistics

Milestone 11F introduces `create_build_and_run_measurement_cohort()` rather than jumping directly from pairwise comparison to averages.

The cohort validates each retained observation's subject against its own `BuildResult`, then requires exact equality of logical Workspace identity, RIR SHA-256, runtime-input evidence, execution-environment evidence, and the ordered `build → runtime` stage contract. The exact `MeasuredBuildAndRunResult` objects are retained in caller order.

The acceptance path deliberately includes a first `new` build followed by `reused` builds. Those work differences do not invalidate the cohort because they are observed consequences, not condition identity. This leaves the next summary layer with the responsibility to preserve work context instead of silently averaging different work states together.

### 4.32 Stage projection should preserve pairing before compression

Milestone 11G introduces `project_build_and_run_measurement_stage_samples()` instead of making the first stage-oriented view a statistic.

For each cohort stage, the projection copies raw duration values in observation order and pairs every value with the exact `BuildWorkEvidence` object from the same measurement. The first `new`/written build and later `reused`/no-write builds therefore remain distinguishable even though they share the same cohort condition.

The lesson is that compression should happen only after the evidence needed to understand what is being compressed has been preserved. 11G still makes no claim that the work difference caused the duration difference.

---

## 5. Prototype and Repository Zero decision sequence

The numbered decisions capture the narrowing process.

### D055 — Guided Architectural Delta
Teach by modifying canonical architecture and letting the compiler expose consequences.

### D056 — Local Learning and Waste Report
Attach timing and waste to a user journey rather than abstract compiler throughput.

### D057 — Node-Level Incremental Generation
Reuse generated output only when semantic fingerprints and artifact integrity both agree.

### D058 — Visible Incremental Compilation
Expose compiler-derived artifact statuses and explanations to the user.

### D059 — Safe Capability Restoration
Restore from current canonical intent rather than deleted generated files.

### D060 — Append-Only Canonical Revision Events
Record operation, rationale, before/after hashes, chain identity, and compiler completion.

### D061 — Workspace Revision Timeline
Combine human rationale with compiler and runtime consequences in one history view.

### D062 — Reapply Canonical State as a New Revision
Reproduce prior state without rewriting history.

### D063 — Preview-First Reapply
Historical state may not be reapplied without first showing its architectural delta.

### D064 — Consolidated Minimal Product
A feature is not part of the product until it participates in the same first-run path.

### D065 — Installable CLI and Independent Export
Portable compiler products should execute independently from the Pyxis source tree.

### D066 — Verified Export
Export becomes READY only after provenance and runtime verification.

### D067 — Visible READY State
Readiness in the interface must come from verification evidence.

### D068 — Real Workspace Creation
First-run authoring should begin with only Workspace name and description.

### D069 — Created Workspace Runs Immediately
A newly created Workspace should quickly reach observable generated behavior.

### D070 — Preview Architectural Edits Before Compilation
Derive proposed state in memory and prohibit mutation until Apply.

### D071 — Architecture Changes Require Rationale + Provenance
A compiler diff does not explain intent; rationale belongs in the revision record.

### D072 — Reversible Change Uses the Same Path
Restoration is another forward revision, not rollback.

### D073 — Preview Includes Predicted Runtime Contract
Predict only runtime surfaces directly implied by canonical structure.

### D074 — Consolidate the First-Run Product Before Adding Features
The architectural risk shifted from insufficient proof to fragmented proofs.

### D075 — Export Is a Consequence of the Product Path
Export packages existing compiler products rather than introducing a parallel generator.

### D076 — First Run Ends With Export
Portability becomes part of the same Workspace journey.

### D077 — Package-Ready Repository
Portable output should look conventional to another Python developer.

### D078 — Self-Contained Install Proof
The prototype demonstrated clean, network-disabled installation while preserving generated artifact identity.

### D079 — Separate Source-Build and Wheel-Install Portability Proofs
Repository Zero separated conventional source-to-wheel construction from verified-wheel installation/execution.

### D080 — Reproduce a Portability Constraint Before Choosing Its Remedy
Repository Zero reproduced the offline PEP 517 build-dependency failure before deciding whether it deserved a solution.

### D081 — Portable Deliverable Is Conventional Source Plus a Verified Wheel
Repository Zero resolved D078 in favor of the smallest proven product contract. Offline installation/execution of the verified wheel is required; offline rebuilding from raw source is not.

### D082 — Workspace Presentation Is an Application-Owned Evidence Adapter
Repository Zero established a framework-independent read-only presentation contract assembled only from authoritative canonical state and already-produced application evidence. The UI renders that contract rather than rediscovering state or reimplementing product logic.

### D083 — Existing Workspace Queries Separate Durable and Transient Evidence
Repository Zero established a read-only application query that reloads durable canonical/RIR/manifest/revision evidence through owning loaders while requiring current run evidence explicitly and accepting READY only through actual export verification evidence.

### D084 — Textual Is the First Local Workspace UI Framework
Repository Zero selected Textual as an optional first local renderer after comparing viable Python-first UI technologies against the existing presentation/query boundaries. The decision applies to the first evidence UI, not every future Pyxis surface.

### D085 — Complete Workspace Evidence Is Rendered Before UI Actions Exist
Repository Zero requires the first genuine Workspace detail view to expose the complete current presentation contract read-only before mutation controls or callbacks are introduced.

### D086 — UI Actions Cross an Application-Owned Operation Boundary
Repository Zero proves the first action seam with a runtime-only `rerun_workspace()` application operation. It preflights live evidence, executes the already-materialized Workspace once, reuses the existing build evidence, and returns fresh run/presentation evidence without compiler, revision, export, or UI ownership leakage.

### D087 — Visible Runtime Interaction Retains Live Evidence Outside the Renderer
Repository Zero wires one Textual runtime input through an application-owned `WorkspaceRuntimeController`, which retains fresh `BuildAndRunResult` evidence across submissions while the renderer consumes only fresh `WorkspacePresentation` values.

### D088 — Architectural Preview Is Proposed Evidence, Not Current Workspace State
Repository Zero adds an application-owned architectural preview operation/presentation/controller seam over the existing `normalize_text` removal preview. The controller retains the typed pending preview for later apply; the renderer-facing object is immutable proposed evidence only, and current run/READY evidence remains current until apply.

### D089 — Visible Architectural Preview Remains Separate From Current Evidence
Repository Zero adds one Textual preview button and a dedicated `ArchitecturePreviewDetail` proposed-state surface. The action displays only immutable preview evidence, leaves current Workspace/READY evidence unchanged, and still provides no rationale or Apply control.

### D090 — Architectural Apply Consumes the Retained Preview and Invalidates Pre-Change READY
Repository Zero adds the application-owned rationale-bearing apply operation/controller seam. It consumes the exact retained typed preview, delegates mutation to the governed permanent apply path, returns fresh post-apply run/presentation evidence, clears consumed preview/export evidence only after success, and does not treat the old portable directory as current READY state.

### D091 — One Live Workspace Controller Owns Transient Interaction State
Repository Zero consolidates combined runtime/architecture interaction state into `WorkspaceController`: one current run, one optional current export result, and one optional pending architecture preview. Runtime, preview, and apply all delegate to the existing application operations and advance that one state only after success.

### D092 — Textual Runtime and Preview Interactions Share the Unified Workspace Controller
Repository Zero removes separate runtime/architecture controller inputs from the combined Textual shell. One optional `WorkspaceController` now owns both visible event paths, and the headless runtime → Preview proof verifies that Preview consumes the exact fresh run produced by the preceding runtime submission while READY remains current.

### D093 — Visible Apply Advances Only From Successful Application Evidence
Repository Zero adds one rationale input and one Apply button only after Preview succeeds. Textual passes rationale and visible runtime text to the unified controller, then waits for fresh application evidence before replacing current state or clearing proposed state. Empty rationale or failed Apply changes neither controller state nor current/proposed evidence.

### D094 — READY Can Re-Enter Live State Only Through Verified Export Refresh
Repository Zero adds `refresh_workspace_export()` plus `WorkspaceController.refresh_export()`. The operation preflights the exact current run, exports its current `BuildResult` through the existing verified packaging path to an explicitly supplied fresh destination, and returns genuine READY evidence plus fresh presentation. Controller export state advances only after successful verification; stale runs and failed/occupied destinations do not partially restore READY.

### D095 — Visible Export Refresh Is Evidence-Gated and Non-Optimistic
Repository Zero exposes one destination-path input and one Export/Verify action only while current presentation lacks READY evidence. Textual passes the path and visible runtime text to the unified controller, waits for successful verified evidence before replacing current presentation, and leaves current evidence/controller state unchanged on failure except for a non-evidence status message.

### D096 — Measurement Observes Established Operations and Carries Owned Work Evidence
Repository Zero adds one application-owned measurement wrapper over `build_and_run_workspace()`. An injectable monotonic clock records immutable ordered build/runtime duration evidence while compiler/materializer work facts pass through directly from `BuildResult`. Measurement does not create a shadow execution path, scan the filesystem, classify waste, persist metrics, or add UI.

### D097 — Measurement Comparison Reports Observation Deltas Without Causal Interpretation
Repository Zero adds a pure comparison over two existing measured cycles. Ordered stage durations are reported as before/after values plus arithmetic deltas; exact before/after build-work evidence is retained; compiler-status changes are stated per artifact path. Comparison performs no execution or filesystem work and makes no causal, efficiency, or waste claim.

### D098 — Measurement Subject Identity Separates Logical Workspace From Architectural State
Repository Zero adds immutable subject evidence to every measured cycle using Repository ID, Workspace ID, and generation-manifest RIR identity already owned by the build. Comparison revalidates that evidence before constructing deltas, permits different RIR states within one logical Workspace, and rejects unrelated or forged subjects before comparison evidence is produced.

### D099 — Runtime Input Identity Exposes Workload Comparability Without Retaining Raw Text
Repository Zero adds immutable runtime-input evidence containing SHA-256 over exact UTF-8 bytes, Unicode character count, and UTF-8 byte count. Comparison retains exact before/after workload evidence and reports whether it matches while still allowing descriptive comparison of different workloads. Input mismatch is a confound to expose, not a rejection rule or causal explanation.

### D100 — Execution Environment Identity Exposes Context Comparability Without Host-Specific Telemetry
Repository Zero adds immutable execution-environment evidence containing Python implementation/version and platform system/machine. Acquisition is injectable and occurs once before timed stages begin. Comparison retains exact before/after environment evidence and reports whether it matches while still allowing descriptive comparison of different environments. Environment mismatch is a confound to expose, not a rejection rule or causal explanation.

### D101 — Repeated-Measurement Cohorts Require One Exact Measurement Condition
Repository Zero adds a pure immutable cohort boundary over two or more already-measured cycles. Cohort membership requires exact validated Repository/Workspace/RIR identity, runtime-input evidence, execution-environment evidence, and ordered stage contract. The exact observations remain ordered and untouched; timing/work differences remain observations rather than membership criteria or aggregate conclusions.

### D102 — Raw Stage Samples Retain Work Context Before Summary
Repository Zero adds a pure stage-sample projection over a coherent cohort. Every raw duration remains in cohort observation order and is paired with the exact `BuildWorkEvidence` from the same measured cycle. The projection preserves observed work differences before any statistic, filtering, sorting, or causal label is introduced.

`DECISIONS.md` remains the compact normative record; this archive records why those decisions emerged.

---

## 6. Transition to Repository Zero

After D078, the architecture had survived a sufficiently strong prototype chain:

```text
author
  ↓
represent
  ↓
compile
  ↓
execute
  ↓
alter
  ↓
recompile
  ↓
export
  ↓
install elsewhere
  ↓
execute again
```

At that point, further disposable proof repositories had diminishing value.

The development mandate changed from:

> prove that the architecture could work

into:

> construct the permanent reference implementation from the proven architecture

This transition is important. Future work should not restart broad architectural exploration unless Repository Zero reveals a real contradiction.

---

## 7. Current Repository Zero implementation

Repository Zero has now carried the architecture through the permanent path rather than merely preserving prototype intent.

### 7.1 Authoring and canonical persistence

`WorkspaceSpec` remains the authoritative intent object. Workspace builds persist deterministic canonical state under `authoring/canonical/workspace.json` and reload it without deriving truth from generated code.

### 7.2 RIR persistence

Canonical state lowers deterministically into `RepositoryIR` / `WorkspaceIR`, persisted as `generated/repository.rir.json`. A strict read-only loader reconstructs typed RIR for later verification and runtime use.

### 7.3 Compiler products and generation evidence

The compiler emits deterministic `GeneratedArtifact` values for the `text_lab` capabilities and Workspace entrypoint. The generation manifest records RIR identity plus artifact paths, semantic node hashes, and artifact hashes.

Generation status is compiler evidence: `new`, `reused`, `regenerated`, or `removed`.

### 7.4 Incremental materialization

Materialization reconciles current compiler products against prior manifest ownership. Reused artifacts are not rewritten; regenerated/new artifacts are written; removed artifacts are deleted only when the prior manifest established compiler ownership.

Filesystem discovery does not substitute for compiler evidence.

### 7.5 Revision provenance

Architectural change follows preview → rationale → append-only revision → canonical mutation → compiler completion. Removal and restoration of `normalize_text` both use the same current-intent path; restore is a forward revision, not rollback.

Typed read-only loaders now recover revision events and completions through the revisions persistence boundary while preserving chain/completion validation.

### 7.6 Runtime

`run_materialized_workspace()` executes generated implementation from the materialized tree and does not compile or write. Runtime suppresses bytecode-cache writes so the repository boundary remains read-only in observable filesystem terms.

### 7.7 Verified export

Export follows the permanent application path:

```text
existing BuildResult
      ↓
ExportPlan
      ↓
exact-byte portable materialization
      ↓
exported RIR / manifest / artifact identity verification
      ↓
source ↔ export runtime equivalence
      ↓
READY
```

READY is derived only after identity and runtime evidence succeed for the same export tree, Repository, and Workspace.

### 7.8 Conventional source projection

The verified export projects compiler products byte-for-byte into a conventional `src/` package layout. Packaging support files remain a distinct ownership class.

The materialized `src/` package executes in a fresh subprocess with Pyxis unavailable and reproduces the already-verified Workspace behavior.

### 7.9 Standard wheel and offline installation

The conventional source package builds a standard wheel using ordinary PEP 517 tooling when its declared build dependencies are obtainable. Wheel inspection verifies that compiler-product bytes inside the archive still match their recorded hashes and that no Pyxis package has leaked into the payload.

The verified wheel installs into a fresh virtual environment with index access disabled, dependencies disabled, network resolution/connections blocked, user/system site leakage excluded, and Pyxis imports rejected. The installed console command reproduces verified package behavior.

### 7.10 Portable deliverable contract

Milestone 9N defines the permanent Repository Zero portable deliverable as:

```text
conventional source repository + verified wheel
```

The source form preserves inspectability, provenance, exact compiler-product relationships, and conventional Python packaging. The wheel form is the verified offline-installable execution artifact.

Offline source-to-wheel construction was characterized in 9M and fails because normal PEP 517 isolation cannot resolve `setuptools>=77.0.3` without an available index/build dependency. Under D081 that is an accepted source-build limitation, not an unresolved Repository Zero defect.

No local backend, vendored Setuptools, or weakened build isolation is required to close Milestone 9.

### 7.11 Application surfaces

The CLI remains a thin interface over application orchestration. `examples/text_lab/` is the permanent executable specification for the minimum Workspace. Export has a thin application-level orchestration seam over the proven build/export APIs.

### 7.12 Read-only Workspace presentation contract

`src/pyxis/app/presentation.py` defines the smallest framework-independent presentation surface for Milestone 10.

`create_workspace_presentation()` consumes authoritative `WorkspaceSpec`, an existing `BuildAndRunResult`, optional revision event/completion tuples, and optional existing `WorkspaceExportResult` carrying READY verification evidence.

It returns frozen presentation objects for canonical identity, RIR identity, compiler artifact status, revision history, runtime output, and optional export READY evidence.

The adapter performs no filesystem reads, no compilation, no runtime execution, and no export. Runtime mappings/sequences are recursively frozen. Removed artifacts retain the compiler-owned `removed` classification but receive no fabricated current node/artifact hashes. Revision events without completion evidence remain visible as incomplete intent rather than being converted into success. Mismatched canonical or export evidence is rejected.

### 7.13 Existing Workspace presentation query

`src/pyxis/app/query.py` owns assembly of that presentation for an existing Workspace.

`query_workspace_presentation()` loads only durable evidence through official boundaries:

```text
load_workspace_spec()
load_repository_ir()
load_generation_manifest()
load_revision_events()
load_revision_completions()
```

It requires a supplied current `BuildAndRunResult` because runtime output and generation statuses are transient. The supplied run's RIR and generation manifest must exactly match persisted state before presentation is assembled.

`WorkspaceExportResult` remains optional. Merely finding a portable export tree does not produce READY. When export evidence is supplied, its runtime source root must identify the queried Workspace and its materialization/verification roots must remain coherent.

Tests prove the query does not compile or execute, does not infer READY from export files, rejects stale run evidence after a Workspace change, rejects export evidence borrowed from another physical source root, and leaves the queried Workspace unchanged.

### 7.14 First local Workspace UI

Milestone 10C selected Textual for the first local Workspace UI after comparing it against NiceGUI, PySide6, Streamlit, and Flet. Textual remains optional through the `ui` dependency group; the compiler/runtime core has no required UI dependency.

Milestone 10D adds `WorkspaceDetail`, a vertically scrollable renderer for the complete presentation contract. The detail surface shows canonical intent/hash, RIR identity/hash, every compiler artifact status and current hashes where applicable, complete runtime output, revision provenance/completion evidence, and complete optional export READY verification evidence.

Runtime mappings are formatted as deterministic JSON only for legibility. Missing optional evidence is rendered neutrally. A removed artifact remains visible with `removed` status and no fabricated current hashes.

### 7.15 First application-owned UI operation seam

`src/pyxis/app/operations.py` owns `rerun_workspace()`.

The operation accepts the existing Workspace root, current `BuildAndRunResult`, new runtime text, and optional current export evidence. It preflights those live facts through `query_workspace_presentation()` before runtime execution, so stale RIR/manifest/export evidence cannot reach generated code.

A successful operation invokes `run_materialized_workspace()` exactly once, reuses the exact previous `BuildResult`, and returns `WorkspaceRerunResult` containing both the fresh `BuildAndRunResult` and fresh `WorkspacePresentation`. It does not compile, materialize, classify generation status, append revisions, export, or re-verify READY.

### 7.16 First visible runtime interaction

Milestone 10F originally connected the runtime `Input` through `WorkspaceRuntimeController`. That proof established that Textual submits one runtime action, receives fresh presentation evidence, and never reconstructs the `BuildAndRunResult` from rendered fields.

The 10F acceptance path starts from real governed revision evidence plus real READY export evidence. After one text submission, only runtime evidence changes; canonical, RIR, compiler, revision, and export presentation remain unchanged, and Workspace/export bytes remain unchanged.

### 7.17 Application-owned architectural preview presentation seam

`src/pyxis/app/architecture_preview.py` owns the Workspace-aware `preview_workspace_remove_normalize_text()` operation.

It first calls `query_workspace_presentation()` with current run/optional export evidence so stale live state fails before preview creation. It then loads authoritative canonical intent and delegates to the existing `preview_remove_normalize_text()` function. A canonical-hash cross-check prevents the operation from combining a preflighted presentation with canonical state that changed during assembly.

`src/pyxis/app/preview_presentation.py` defines immutable `CanonicalPreviewPresentation` and `ArchitecturePreviewPresentation`. These expose current/proposed canonical hashes and capabilities, capability additions/removals, predicted added/changed/removed compiler artifact paths, and current/proposed/added/removed runtime result keys. The adapter validates that proposed RIR and delta evidence agree with the canonical proposal but does not compile or execute it.

The 10G acceptance path proves that preview construction leaves both source and portable-export trees unchanged, current run/READY evidence remains queryable and identical afterward, compiler execution is unavailable, and stale live evidence is rejected before the underlying preview function runs.

### 7.18 First visible architectural preview

Milestone 10H originally connected the Preview button through `WorkspaceArchitecturePreviewController`. It established the dedicated `ArchitecturePreviewDetail` surface whose body begins with `PROPOSED — NOT APPLIED` and whose contents never replace current `WorkspaceDetail` evidence.

The 10H acceptance test starts from a real built/run/READY Workspace, disables compiler execution, snapshots every current evidence section plus both repository trees, triggers Preview once in a real headless Textual app, and verifies that only the proposed-preview panel changes.

### 7.19 First rationale-bearing architectural apply seam

`src/pyxis/app/architecture_apply.py` owns `apply_workspace_remove_normalize_text()` and returns `WorkspaceArchitectureApplyResult` containing the governed `ApplyResult`, fresh post-apply `BuildAndRunResult`, and fresh post-apply `WorkspacePresentation`.

The operation requires non-empty rationale and explicit runtime text. It preflights current live run/export evidence through `query_workspace_presentation()`, verifies that the retained preview's current canonical hash still matches current canonical evidence, and passes that exact preview object to `apply_remove_normalize_text()`.

The existing governed apply path appends revision intent, builds the proposed canonical state through the permanent compiler/materializer path, and appends completion evidence. The new application operation then runs the newly materialized Workspace once and queries fresh presentation evidence with `export=None`.

The 10I acceptance path proves the exact retained preview object reaches governed apply, runtime executes once from the proposed RepositoryIR, revision rationale/completion appear in the new presentation, `normalize_text` appears as `removed`, and physically unchanged pre-change portable files do not cause READY to survive in the new current presentation.

### 7.20 Unified live Workspace controller

`src/pyxis/app/controller.py` defines `WorkspaceController`, the live-state authority for combined runtime and architectural interactions.

It retains exactly one current `BuildAndRunResult`, one optional current `WorkspaceExportResult`, and one optional pending `ArchitecturePreview`. Its runtime, preview, apply, and export-refresh methods delegate to proven application operations and replace controller state only from successful operation results.

Runtime rerun keeps READY because architecture is unchanged. Preview retains the typed proposal against the same current run. Successful Apply advances that same run to the new architecture, clears READY, and consumes the pending preview. Verified export refresh leaves that run unchanged while replacing only current export evidence with newly verified READY. A later rerun therefore uses the current build and carries only export evidence that belongs to that architecture.

The earlier specialized controllers remain available as compatibility/application proof surfaces, but they are no longer accepted as separate live-state inputs by the combined Textual shell.

### 7.21 Textual uses the unified live Workspace controller

Milestone 10K migrates the current Textual interaction boundary itself. `WorkspaceShell` and `create_workspace_shell()` accept one optional `WorkspaceController`; when it is present, the shell renders the runtime `Input` and Preview button and routes both events to that same controller.

A runtime submission replaces current `WorkspacePresentation` from `WorkspaceController.rerun()`. Preview does not replace that current presentation; it calls `WorkspaceController.preview_remove_normalize_text()` and updates only `ArchitecturePreviewDetail`.

The combined 10K acceptance path starts from READY evidence, submits new runtime text, captures the fresh run retained by `WorkspaceController`, then clicks Preview. Instrumentation proves that the preview application operation receives that exact fresh run object and the same export evidence. READY remains visible, the runtime result remains the just-submitted result, the proposed panel remains `PROPOSED — NOT APPLIED`, compiler execution is unavailable, and both source/export trees remain byte-identical.

At the 10K boundary there was still exactly one runtime Input and one Preview button before Preview. Milestone 10L builds the rationale-bearing mutation interaction on top of that proven shared authority.

### 7.22 First visible rationale-bearing architectural Apply

After a successful Preview, `WorkspaceShell` dynamically mounts one `ArchitectureApplyControls` surface containing one rationale `Input`, one Apply button, and a non-evidence interaction-status field. Those controls do not exist before a typed pending preview has been produced.

Pressing Apply sends the rationale and the current visible runtime-input value to `WorkspaceController.apply_pending_remove_normalize_text()`. Textual does not reconstruct the architecture proposal, infer runtime input from displayed results, append revisions, compile, execute generated code, or manipulate READY itself.

The renderer waits for the controller call to succeed. On success, the returned fresh `WorkspacePresentation` replaces current `WorkspaceDetail`, `ArchitecturePreviewDetail` returns to `No pending architecture preview.`, and the rationale/Apply controls are removed. The unified controller now retains the post-apply run, no export evidence, and no pending preview.

The successful 10L acceptance path proves that `normalize_text` is shown as `removed` with no current hashes, the normalized rationale appears in a completed revision, fresh runtime evidence contains only `inspect_text`, and pre-change READY is visibly absent even though the old portable tree remains byte-identical.

Empty rationale and simulated governed-apply failure are also exercised through the real headless Textual event path. Both leave controller live-state object identity, current presentation, proposed presentation, and repository bytes unchanged. Only the interaction-status text changes.

### 7.23 Verified export refresh for current live state

`src/pyxis/app/export_refresh.py` owns `refresh_workspace_export()` and returns `WorkspaceExportRefreshResult` containing a genuine `WorkspaceExportResult` plus the fresh `WorkspacePresentation` assembled with that READY evidence.

The operation first calls `query_workspace_presentation()` with the current `BuildAndRunResult` and no export evidence, ensuring stale live state fails before export begins. It then calls the existing `export_workspace()` with the exact `current_run.build`, the physical Workspace root, an explicitly supplied destination, and explicit verification runtime text. A second query introduces the returned export evidence only after verification succeeds.

`WorkspaceController.refresh_export(destination, text)` delegates to that operation and assigns `_export` only after successful return. It does not replace the current run or pending preview.

The 10M acceptance path starts from a real post-Apply Workspace whose old portable tree still exists but whose controller correctly has no current export evidence. With compilation disabled, the operation exports the exact post-Apply build to a fresh destination and returns READY while leaving source/revision bytes unchanged. A stale pre-Apply run is rejected before `export_workspace()` can execute. An occupied destination raises through the existing materialization boundary and leaves controller run/export/pending-preview state unchanged; a subsequent fresh destination succeeds and retains the new READY result.

Textual is unchanged in 10M. No export control or destination picker exists yet.

### 7.24 First visible verified export refresh

Milestone 10N adds `ExportRefreshControls` to the interactive Textual shell only while the current `WorkspacePresentation` has no READY evidence. The surface contains one explicit destination-path input, one Export/Verify button, and one non-evidence status field.

The button passes `Path(destination_input.value)` and the current visible runtime-input value to `WorkspaceController.refresh_export()`. Textual performs no destination discovery, filesystem inspection, export planning, compilation, verification, overwrite, or cleanup.

On successful return, the fresh `WorkspacePresentation` replaces `WorkspaceDetail`, genuine READY becomes visible, and the export controls are removed. After a successful architecture Apply, those controls are mounted because the returned presentation has no READY evidence. Thus the visible lifecycle follows application evidence rather than local directory shape.

The 10N headless acceptance path proves the export operation receives the exact post-Apply run object plus visible runtime text, compilation is unavailable, current run identity remains unchanged across export, and READY appears only after verification. An occupied destination leaves current presentation and controller export state unchanged while the controls remain available for correction.

### 7.25 First application-owned measurement evidence

`src/pyxis/app/measurement.py` owns the first Repository Zero measurement boundary.

`measure_build_and_run_workspace()` accepts the same `WorkspaceSpec`, destination, and runtime text as `build_and_run_workspace()` plus an injectable monotonic clock. It calls the existing operation exactly once, using only its private stage observer to capture the established `build` and `runtime` start/end boundaries.

The result is `MeasuredBuildAndRunResult`: the unchanged `BuildAndRunResult` paired with immutable `BuildAndRunMeasurementEvidence`. Ordered `StageDurationEvidence` records elapsed build/runtime seconds. `BuildWorkEvidence` carries the exact `BuildResult.generation_statuses`, `written_paths`, `reused_paths`, and `removed_paths` tuples rather than deriving work from disk.

The acceptance tests compare measured and unmeasured fresh executions semantically, prove the measurement wrapper invokes the existing operation once, make stage timing exact with a fake clock, prove measurement dataclasses are frozen, and exercise a real incremental removal where `reused`, `regenerated`, and `removed` statuses plus written/reused/removed paths pass through unchanged.

No measurement persistence, UI, full ledger, waste score, or Preview/Apply/Export timing is introduced in 11A.

### 7.26 Pure measurement comparison

`compare_build_and_run_measurements()` consumes two existing `MeasuredBuildAndRunResult` values and returns immutable `BuildAndRunMeasurementComparisonEvidence`.

The function does no execution or acquisition. It requires the two measurement stage-name sequences to match exactly, then produces `StageDurationComparisonEvidence` containing each stage's before seconds, after seconds, and arithmetic delta. It retains the exact before/after `BuildWorkEvidence` objects and produces path-level `ArtifactGenerationStatusComparisonEvidence` without reclassifying compiler work.

The 11B acceptance fixture performs a genuine first build and identical rebuild on the same Workspace. All three artifacts transition from `new` to `reused`; generated writes go from all three artifact paths to none; reused paths go from none to all three. Fake-clock durations are exact and lower in the second observation. The comparison exposes those facts together but does not characterize the second run as faster due to reuse, efficient, or less wasteful.

A separate test rejects mismatched stage ordering rather than silently pairing unrelated stage positions. Comparison remains transient, pure, and in-memory only.

### 7.27 Measurement subject identity and comparison coherence

`BuildAndRunMeasurementEvidence` now includes immutable `MeasurementSubjectEvidence` derived from the same `BuildResult` whose timing/work evidence is being recorded.

The subject contains `repository_id`, `workspace_id`, and `rir_sha256`. Measurement computes the RepositoryIR SHA-256 through the existing deterministic identity function and requires it to equal `GenerationManifest.rir_sha256` before returning evidence. No Workspace path or filesystem scan participates in subject construction.

Before `compare_build_and_run_measurements()` constructs stage or work deltas, it revalidates each stored subject against its own `BuildResult`. Matching Repository/Workspace identity is required; matching RIR identity is not. This permits one logical Workspace to be compared across architectural revisions while preserving both exact RIR states. Unrelated Workspace subjects and tampered subject evidence fail before comparison evidence is produced.

### 7.28 Privacy-preserving runtime input identity

`BuildAndRunMeasurementEvidence` now also includes immutable `RuntimeInputEvidence` derived from the exact runtime text supplied to the permanent build/run operation.

Measurement UTF-8 encodes the text for evidence, records its deterministic SHA-256, Unicode character count, and UTF-8 byte count, and retains none of the raw text in the measurement object. The runtime still receives the original text through the established operation unchanged.

`compare_build_and_run_measurements()` carries the exact before/after `RuntimeInputEvidence` objects into `RuntimeInputComparisonEvidence` and sets `matches` only from exact evidence equality. A different input does not abort comparison: stage and work deltas are still returned, while `matches=False` makes the workload mismatch explicit for later interpretation.

The 11D acceptance fixture proves raw text is absent from the evidence shape/repr, Unicode character and byte counts differ as expected, same inputs report `matches=True`, different inputs report `matches=False`, and different workloads remain descriptively comparable.

### 7.29 Non-identifying execution environment identity

`BuildAndRunMeasurementEvidence` now includes immutable `ExecutionEnvironmentEvidence` beside subject, workload, stage, and work evidence.

The default environment provider records Python implementation, Python version, platform system, and platform machine only; missing system/machine values become `unknown`. The provider is injectable and its return type is validated before execution begins. Hostnames, usernames, absolute paths, process IDs, system load, memory pressure, and other identifying or dynamic telemetry are outside the 11E evidence contract.

Environment acquisition occurs once before any stage clock read. `compare_build_and_run_measurements()` retains exact before/after environment objects in `ExecutionEnvironmentComparisonEvidence`; identical environments report `matches=True`, different environments report `matches=False`, and mismatch does not prevent workload/stage/work comparison.

The 11E acceptance fixture proves the injected environment object is retained by identity, acquisition precedes all four clock reads, the dataclass contains only the four approved fields, and environment mismatch remains descriptively comparable while runtime input remains identical.

### 7.30 Repeated-measurement cohort coherence

`src/pyxis/app/measurement_cohort.py` owns the first repeated-observation boundary.

`create_build_and_run_measurement_cohort()` consumes an ordered iterable of at least two existing `MeasuredBuildAndRunResult` values and performs no execution or aggregation. It derives `MeasurementCohortConditionEvidence` from the first observation, reusing that observation's validated subject, exact runtime-input evidence, exact execution-environment evidence, and ordered `build → runtime` stage names.

Every retained observation is then revalidated against its own `BuildResult` and required to match that condition exactly, including the exact RIR SHA-256. The returned `BuildAndRunMeasurementCohortEvidence` preserves the exact measured objects in caller order. Its direct dataclass constructor enforces the same invariant, so callers cannot bypass cohort coherence by manually constructing the object.

The 11F acceptance fixture proves a first `new` build and later `reused` builds remain valid members of the same condition, while changed workload, changed environment, changed RIR, unrelated Workspace, reversed stage order, and fewer than two observations are rejected before a cohort exists. The cohort shape contains no aggregate fields.

### 7.31 Raw per-stage sample projection

`src/pyxis/app/measurement_samples.py` owns the first stage-oriented repeated-observation view.

`project_build_and_run_measurement_stage_samples()` consumes one already-coherent `BuildAndRunMeasurementCohortEvidence` and performs no execution, clock access, filesystem access, sorting, filtering, aggregation, or work classification. It retains the cohort's exact condition object and emits ordered `build` and `runtime` `MeasurementStageSamplesEvidence` values.

Each `StageSampleObservationEvidence` contains only the raw `duration_seconds` from that stage and the exact `BuildWorkEvidence` object from the same measured cycle. The projection therefore preserves both observation order and compiler/materializer context across stage views. Direct evidence construction requires stage order to match the cohort condition and requires equal observation counts across stages.

The 11G acceptance fixture projects a real three-observation cohort whose first build is `new`/written and later builds are `reused`/not written. Exact fake-clock duration sequences are preserved for both stages, and every projected sample's work object is identical to the source measurement's work evidence. The projection shape contains no aggregate or classification fields.

---

## 8. Proof status

Repository Zero is exercised by GitHub Actions on Python 3.11. The development sequence repeatedly ran the complete pytest suite after each narrow step.

The portability suite has executed real conventional wheel builds, independent source-layout runtime checks, fresh virtual-environment creation, network-blocked local-wheel installation, execution of the installed console command, and explicit offline source-build characterization.

Milestone 10A executes the presentation contract against real build/run/export/revision evidence and proves that presentation itself performs no new filesystem acquisition, compilation, or runtime execution.

Milestone 10B adds real existing-Workspace query tests and typed revision-loader tests. The query recovers only explicitly persisted evidence and refuses to reconstruct missing runtime/status/READY facts from repository shape.

Milestone 10C executes the real Textual framework headlessly in ordinary pytest while application query/compiler/runtime paths are disabled, proving that the renderer can consume `WorkspacePresentation` without absorbing application behavior.

Milestone 10D renders the complete presentation contract in that real Textual shell. Its acceptance test includes governed revision completion, a removed compiler artifact, runtime behavior after the change, complete READY evidence, explicit absence handling, and a zero-button assertion.

Milestone 10E proves the first application-owned UI operation independently of Textual. Runtime rerun preflights current evidence, executes exactly once, reuses build evidence, returns a fresh presentation, and leaves persisted Workspace/export bytes unchanged.

Milestone 10F executes the first complete visible event loop headlessly: one Textual input submission crosses the application controller/operation seam, updates runtime evidence on screen, retains fresh run evidence outside the renderer, and leaves all non-runtime evidence and repository bytes unchanged.

Milestone 10G proves the first application-owned architectural preview presentation seam independently of Textual. Preview facts remain immutable proposed evidence, the typed preview is retained outside presentation for later apply, and current run/READY evidence remains current because the Workspace is not mutated.

Milestone 10H executes the first visible architectural preview action headlessly. One button requests the retained application preview, a dedicated proposed-state panel becomes visible, current Workspace/READY evidence stays unchanged, compiler execution remains unavailable, and both source/export trees remain byte-identical.

Milestone 10I proves the first rationale-bearing architectural apply operation independently of Textual. The exact retained preview is consumed, governed revision/build completion runs through the permanent path, the changed Workspace is executed once, fresh current presentation includes the revision/compiler/runtime consequences, and old READY evidence is dropped even though the old portable bytes remain physically present.

Milestone 10J proves one application-owned live Workspace state authority across runtime and architecture operations. The acceptance path tracks exact object identity through rerun → preview → apply → rerun, proves READY survives only the non-architectural portion, proves post-apply runtime consumes the new `BuildResult`, and proves failed Apply leaves all shared controller state unchanged.

Milestone 10K executes runtime → Preview through that same authority in the real headless Textual shell. It proves the Preview operation receives the exact fresh run produced by the preceding runtime submission, READY remains current because no architecture changed, and current runtime evidence remains current beside the proposal.

Milestone 10L executes Preview → rationale → Apply through the same unified controller in the real headless Textual shell. Success proves the exact retained preview and explicit visible runtime text reach the application operation, then current UI evidence advances to the post-apply architecture while proposed evidence and pre-change READY disappear. Empty rationale and simulated operation failure prove neither application state nor current/proposed evidence advances before successful return.

Milestone 10M proves READY recovery independently of Textual. The exact post-Apply `BuildResult` reaches verified export with compilation disabled; stale live evidence fails before export; an occupied destination is rejected through the existing materialization boundary; source/revision state remains unchanged; and `WorkspaceController` retains new READY evidence only after the complete export verification operation succeeds.

Milestone 10N executes the complete visible READY lifecycle in the real headless Textual shell: current READY → Preview → rationale → Apply → no READY → explicit verified export → READY. The export step consumes the exact post-Apply run and visible runtime text with compilation disabled. An occupied destination proves failure changes neither current presentation nor controller state beyond a non-evidence status message.

Milestone 11A executes the first measurement boundary through the real `build_and_run_workspace()` operation. A fake clock proves exact ordered build/runtime durations; measured and unmeasured fresh cycles are semantically equivalent; work evidence is the same compiler/materializer-owned tuples returned by `BuildResult`; and a real incremental removal carries `reused`, `regenerated`, and `removed` evidence without reclassification.

Milestone 11B executes a real first build followed by an identical rebuild and compares the completed measurement records without running anything during comparison. Exact fake-clock stage deltas, `new → reused` artifact transitions, all-writes → no-writes, and no-reuse → all-reuse facts are returned as immutable evidence. A mismatched stage order is rejected, and no causal/efficiency/waste claim is introduced.

Milestone 11C measures one Workspace across two architectural states and proves the logical Repository/Workspace subject remains stable while the RIR SHA-256 changes. Comparison retains the exact stored subject evidence for each cycle, rejects unrelated Workspaces before any timing-delta object can be constructed, and rejects subject metadata that disagrees with its underlying `BuildResult`.

Milestone 11D measures Unicode runtime input without retaining its raw text, proves SHA-256 plus character/UTF-8 byte counts are immutable workload evidence, and compares repeated cycles with both identical and different inputs. Different input remains comparable with full stage/work evidence while `matches=False` explicitly prevents later analysis from assuming identical runtime workload conditions.

Milestone 11E injects exact execution-environment evidence and proves it is acquired once before any stage clock read. Identical environment facts report `matches=True`; changed Python/platform facts report `matches=False` while the same Workspace and workload still produce complete descriptive comparison evidence. No host-specific identity or dynamic telemetry is collected.

Milestone 11F forms a real three-observation cohort containing one fresh `new` build followed by two `reused` builds under the same exact Workspace/RIR/workload/environment/stage condition. The cohort retains those exact objects in order and exposes no aggregate fields. Separate rejection cases prove workload, environment, RIR, logical Workspace, stage contract, minimum-observation count, and direct-construction coherence are enforced before a cohort exists.

Milestone 11G projects that coherent cohort into raw `build` and `runtime` samples without executing or aggregating anything. Exact fake-clock duration order is preserved, and every sample carries the exact source `BuildWorkEvidence` object, keeping first-cycle `new`/written work visibly distinct from later `reused`/no-write work. Direct-construction guards enforce stage order and equal sample counts.

The permanent rule remains:

> Never broaden a claim beyond the exact condition that was executed and verified.

D081 applies that rule to portability. D082 applies it to presentation. D083 applies it to reopening Workspaces. D084 applies it to framework scope. D085 applies it to UI sequencing. D086 applies it to action ownership. D087 applies it to transient UI-operation state ownership. D088 applies it to the distinction between proposed architecture and current Workspace evidence. D089 applies it to visible preview semantics: proposed display is still not apply. D090 applies it to mutation: Apply consumes the retained proposal and resets transient evidence that no longer belongs to the new architecture. D091 applies it to combined interaction state: one live application authority owns the transient evidence shared across operations. D092 applies that same authority at the Textual boundary. D093 applies it to visible mutation: Textual advances evidence only after the application controller returns success. D094 applies it to READY recovery: verified export evidence, not filesystem presence, is what re-establishes current readiness. D095 applies the same discipline to the visible export action: controls are evidence-gated and rendering advances only after verified application success. D096 applies it to measurement: observe the existing operation and carry owned work facts before adding interpretation. D097 applies it to comparison: report observed deltas and status transitions without converting association into causal or waste claims. D098 applies it to measurement coherence: subject identity comes from owned build/RIR evidence, architectural state stays explicit, and unrelated subjects fail before comparison. D099 applies it to workload comparability: input identity is privacy-preserving evidence, mismatches remain visible and non-blocking, and neither match nor mismatch is itself a causal performance claim. D100 applies the same discipline to execution context: environment identity is coarse non-identifying evidence acquired outside timed stages, mismatches remain visible and non-blocking, and neither match nor mismatch explains duration. D101 applies it to repeated sampling: a cohort exists only for one exact recorded condition, while timing/work variation remains unaggregated observation evidence. D102 applies it to stage samples: raw duration evidence keeps exact per-cycle work context before any summary can compress it.

---

## 9. Milestone 9 closure

Milestone 9 — export as packaging — is complete for Repository Zero.

The proven chain is:

```text
exact compiler products
      ↓
verified portable export
      ↓
conventional source projection
      ↓
independent source-layout runtime
      ↓
standard wheel
      ↓
wheel payload identity verification
      ↓
fresh offline wheel installation
      ↓
installed execution with matching behavior
```

The deliverable is source plus verified wheel. Offline rebuilding from raw source is outside the Milestone 9 acceptance contract.

The 9M failure remains useful characterization evidence because it prevents future developers from accidentally claiming that conventional source builds are network-independent. It should not trigger a packaging redesign unless a future real product use case explicitly requires offline source reconstruction.

---

## 10. Foreseeable implementation path

The original milestone order proved useful:

- Milestone 1 — executable CI: complete.
- Milestone 2 — canonical persistence: complete.
- Milestone 3 — RIR + generation evidence: complete.
- Milestone 4 — thin CLI: complete.
- Milestone 5 — permanent `examples/text_lab/`: complete.
- Milestone 6 — preview-first architectural edit: complete.
- Milestone 7 — rationale-bearing append-only revisions and restoration: complete.
- Milestone 8 — evidence-backed incremental generation: complete.
- Milestone 9 — verified export, conventional source, verified wheel, and offline installed execution: complete.
- Milestone 10A — framework-independent read-only Workspace presentation contract: complete.
- Milestone 10B — existing Workspace presentation query with durable/transient evidence separation: complete.
- Milestone 10C — first local UI framework selection and headless boot-shell proof: complete.
- Milestone 10D — complete read-only Workspace detail screen: complete.
- Milestone 10E — first application-owned runtime-only UI operation seam: complete.
- Milestone 10F — first visible runtime interaction and retained live controller evidence: complete.
- Milestone 10G — application-owned architectural preview presentation/controller seam: complete.
- Milestone 10H — first visible architectural preview action and distinct proposed-state surface: complete.
- Milestone 10I — first application-owned rationale-bearing architectural apply seam: complete.
- Milestone 10J — one application-owned live Workspace state authority: complete.
- Milestone 10K — Textual runtime and Preview migrated to the unified Workspace controller: complete.
- Milestone 10L — first visible rationale-bearing architectural Apply through the unified controller: complete.
- Milestone 10M — application-owned verified export refresh and READY recovery: complete.
- Milestone 10N — first visible verified export refresh and READY restoration: complete.
- Milestone 11A — first application-owned build/run measurement evidence boundary: complete.
- Milestone 11B — pure descriptive comparison of two measured build/run cycles: complete.
- Milestone 11C — measurement subject identity and comparison coherence: complete.
- Milestone 11D — privacy-preserving runtime-input identity and workload-match evidence: complete.
- Milestone 11E — non-identifying execution-environment identity and context-match evidence: complete.
- Milestone 11F — exact repeated-measurement cohort coherence before aggregation: complete.
- Milestone 11G — raw per-stage samples with exact build-work context: complete.

### Milestone 10 — First local Workspace UI

Milestone 10 is complete for Repository Zero.

The first local UI now renders the complete current evidence contract, reruns the current architecture, previews one structural change without mutation, collects rationale only after preview, applies the exact retained proposal through governed revision/compiler/runtime boundaries, visibly retires pre-change READY, and can regain genuine READY through an explicit verified export of the exact current build. Read-only rendering still works with no controller, and every visible action remains downstream of named application operations.

This closes the minimum local Workspace lifecycle without adding generalized architecture editing, restoration UI, file pickers, overwrite/cleanup behavior, or filesystem-derived product state.

### Milestone 11 — Measurement

Milestone 11A establishes one stable observation primitive around the permanent build/run operation. Milestone 11B establishes a pure comparison primitive that can state exact timing and work differences between two such observations without pretending those differences explain themselves. Milestone 11C makes the logical Workspace and exact RIR state of each observation explicit and enforces subject coherence before comparison. Milestone 11D makes runtime workload identity explicit without retaining raw input and preserves descriptive comparison when workloads differ. Milestone 11E adds coarse non-identifying execution-environment identity outside the timed stages and preserves descriptive comparison when environments differ. Milestone 11F establishes a strict repeated-observation cohort boundary before any aggregation exists. Milestone 11G exposes raw stage-oriented samples while preserving exact per-cycle build-work context.

The Execution Ledger should continue to evolve from these proven observations rather than imagined fields.

### Next narrow step — Milestone 11H

Add one pure immutable **work-context partition** over an existing `BuildAndRunMeasurementStageSamplesEvidence` before computing any statistic.

For each stage, group raw `StageSampleObservationEvidence` values by exact `BuildWorkEvidence` equality. Preserve group order by first occurrence in the stage sample stream and preserve observation order within each group. The grouping key is the evidence itself; do not invent semantic classes such as `cold`, `warm`, `cached`, `first-run`, `steady-state`, `outlier`, or `normal`.

The purpose is to make distinct observed work contexts explicit so later summary code cannot silently combine a `new`/written sample with `reused`/no-write samples merely because all observations belong to one coherent cohort. Do not compute mean, median, min/max, variance, standard deviation, confidence intervals, quantiles, performance scores, or causal interpretation in 11H. Do not persist or render the partition yet.

### Milestone 12 — Browser/research capabilities

After the compiler/product spine and measurement foundations are stable, return to the original browser/research purpose.

Chromium remains the browser. Pyxis adds inspectable Python capabilities, evidence, provenance, permissions, and workflows around it.

---

## 11. What should remain deferred

Do not let archived ideas create pressure to implement them immediately.

Until the measurement evidence model proves what should actually be retained and interpreted, defer:

- broad capability marketplaces/catalogs
- model-provider abstractions beyond a real need
- autonomous agent permission systems
- browser replacement work
- complex visual editors
- branching/merge semantics for revision history
- distributed execution
- deployment platforms
- broad plugin systems
- full Execution Ledger persistence
- generalized waste/efficiency scoring
- measurement UI/charts
- premature optimization
- large schema/generalized ontology work
- bespoke offline source-build infrastructure without a demonstrated requirement

Repository Zero should stay small enough to understand end to end.

---

## 12. Failure modes to watch for

### Generated-code editing

If a feature fixes architecture by editing generated Python directly, it is almost certainly violating the model.

### UI inference replacing compiler evidence

Do not reconstruct compiler state from timestamps, Git diffs, file existence, or directory scans when the compiler can state it directly.

### UI filesystem acquisition bypassing application evidence

A renderer should not read canonical/RIR/manifest/revision/generated files directly just because they are available. Evidence acquisition belongs to the existing domain/application boundaries; presentation consumes the resulting facts.

### Reconstructing transient evidence from durable artifacts

Do not infer a prior generation status from the current manifest, rerun generated code merely because runtime output is absent, or label an export READY because its files still exist. If the evidence was not persisted, it is unavailable until the real operation produces it again.

### Mutable presentation evidence

Do not hand a UI mutable references to runtime or evidence objects that let presentation code alter the facts it is supposed to render.

### UI controls before application operation ownership

Do not wire Textual callbacks directly to compiler, runtime, revision, export, or persistence layers merely because the renderer now exists. A visible control should call an explicit application-owned operation whose input/output evidence boundary is independently testable.

### Losing fresh transient evidence after an operation

A presentation is not a substitute for the `BuildAndRunResult` that produced it. After an application operation, retain the returned fresh run evidence for future operations rather than trying to reconstruct it from presentation.

### Renderer becoming the live-state owner

Do not store the only authoritative current run state inside Textual widgets or derive it back from displayed JSON/status fields. The renderer displays presentation; the application controller retains transient operation evidence.

### Preview presented as if already applied

Do not merge `ArchitecturePreviewPresentation` fields into the current Workspace evidence surface in a way that makes proposed hashes, capabilities, artifact consequences, or runtime keys look current. Preview is proposed intent until rationale-bearing apply succeeds.

### Preview enrichment through shadow compilation/runtime

Do not compile proposed artifacts or execute a proposed shadow runtime merely to make the preview display richer. The preview may show only structural/compiler-path and observable runtime-contract facts already justified by canonical/RIR structure.

### Visible preview becoming implicit authorization

Do not treat clicking Preview, retaining a pending preview, or rendering `PROPOSED — NOT APPLIED` evidence as consent to mutate canonical state. Apply must require its own application-owned operation and human rationale.

### Recreating preview at Apply time

Do not derive an apply proposal from Textual labels, hashes, capability strings, or a fresh preview call. Apply must consume the exact retained typed preview that was shown and let the governed apply boundary validate it against current canonical state.

### Stale READY evidence surviving architectural mutation

Once apply changes canonical/RIR/compiler products, do not carry the previous `WorkspaceExportResult` forward as current READY evidence merely because the old portable directory still exists. READY belongs to the state that was actually verified.

### READY recovery by filesystem presence

Do not restore READY because a new or old portable directory exists. READY re-enters controller/presentation state only from a successful `WorkspaceExportResult` produced by the verified export refresh operation for the exact current build.

### Visible export controls becoming filesystem logic

Do not make Textual decide whether export is needed by checking destination paths, existing directories, timestamps, or prior output. The control is gated by current presentation evidence, and export validity remains owned by the application/export layers.

### Multiple live-state controllers diverging

Do not reintroduce separate runtime and architecture controller inputs into the combined renderer. `WorkspaceController` is the application-owned authority for current run/export/pending-preview evidence; Textual routes all existing interaction paths through that one object.

### Optimistic renderer mutation

Do not clear the preview, update canonical/compiler/revision/runtime evidence, remove READY, or restore READY in the UI before the responsible application operation returns success. A click is intent to attempt an operation, not evidence that it succeeded.

### Measurement changing the thing measured

Do not introduce alternate build/runtime paths merely to collect timing. Measurement should wrap the permanent application boundaries and preserve their returned evidence and side effects.

### Measurement inference replacing owned work evidence

Do not estimate compiler work from file timestamps or directory scans when `BuildResult` already reports generation statuses and written/reused/removed paths. Time may be newly observed; work classifications should remain owned by the compiler/materializer.

### Measurement comparison becoming causal explanation

A lower duration alongside more reuse is an observation, not proof that reuse caused the timing difference. Comparison may expose deltas and owned work facts before the system has enough evidence to make causal or waste claims.

### Comparing subjects without explicit identity

Do not regress to caller-memory or filesystem assumptions about whether two observations belong to the same Workspace. Measurement subject evidence must remain derived from and coherent with the Repository/RIR/manifest evidence owned by each build.

### Comparing runtime timing without workload identity

Two measurements may belong to the same Workspace and RIR yet have received different runtime inputs. Do not treat their runtime-duration delta as if workload conditions were controlled merely because subject identity matches. Use `RuntimeInputEvidence`/`matches` to expose that confound without retaining raw text or rejecting the observations.

### Treating input identity as causal explanation

Matching runtime-input evidence means only that the recorded input bytes and size facts match; mismatching evidence means they do not. Neither condition proves why a runtime duration changed.

### Treating environment identity as complete experimental control

Matching `ExecutionEnvironmentEvidence` means only that the recorded Python/platform facts match. It does not prove equal system load, scheduler state, thermal state, memory pressure, background activity, or any other unrecorded dynamic condition. Environment mismatch likewise exposes a confound without explaining the observed timing difference.

### Turning environment evidence into host fingerprinting

Do not add hostnames, usernames, absolute paths, process IDs, machine IDs, network addresses, or other identifying details merely to make environment identity more specific. Broader telemetry requires its own demonstrated measurement need and privacy analysis.

### Aggregating mixed measurement conditions

Do not compute repeated-sample summaries from observations that merely share a logical Workspace. A cohort intended for aggregation must already prove exact RIR, workload, environment, and stage-contract agreement. Use pairwise comparison when the mismatch itself is the subject of analysis.

### Treating cohort coherence as complete experimental control

A coherent cohort means only that the recorded condition axes match. It does not prove equal unrecorded scheduler/load/thermal state, and it does not erase observed build-work differences such as `new` versus `reused`. Preserve those facts into any future summary layer.

### Context-free stage samples

Do not strip `BuildWorkEvidence` away when projecting repeated observations into per-stage duration samples. A context-free vector can silently combine first-build writes with later reuse and make a later statistic look more homogeneous than the source evidence actually was.

### Semantic work-state labels ahead of evidence

Do not rename exact work-evidence groups as `warm`, `cold`, `cached`, `steady-state`, or similar causal/operational categories merely because their compiler statuses differ. Such labels require their own proven semantics; exact evidence equality is sufficient for the next partition boundary.

### Shadow implementations

Preview, export, CLI, UI, education, presentation, query, operations, controllers, packaging, and measurement layers must not quietly reimplement capability logic.

### Filesystem discovery becoming architecture

A capability should eventually exist because canonical/registry state declares it, not because a Python file happens to be in a directory.

### Abstraction ahead of pressure

The project produced its best progress when abstractions were introduced only after a small proof exposed the need.

### Prototype accumulation

Do not return to producing many disconnected demonstration repositories. Extend the permanent vertical slice.

### Treating text utilities as the product

`inspect_text` and `normalize_text` are intentionally boring. Their purpose is to make architectural consequences obvious.

### Treating Git as the entire product history model

Git is repository history. Pyxis revision provenance has different product semantics and should remain explicit.

### Claiming verification that did not run

Preserve the distinction between designed tests and executed tests.

### Collapsing build and install evidence

A verified wheel that installs offline does not imply the source repository can build a wheel offline. Keep those facts distinct even though D081 does not require the latter.

### Solving a non-requirement

Do not add a custom backend, vendor toolchain dependencies, or weaken conventional build behavior solely because 9M reproduced an offline source-build failure. A characterized limitation is not automatically a product defect.

---

## 13. A useful test for every new feature

Before adding something, ask:

1. What canonical intent does this represent?
2. Does it need to exist in the RIR?
3. Which compiler product changes because of it?
4. Can the consequence be predicted before mutation?
5. What provenance explains why it changed?
6. Does runtime consume generated implementation rather than a shadow path?
7. Can export preserve the exact compiler result?
8. Can a user inspect enough of this transformation to learn from it?
9. Can we measure whether the implementation wastes work?
10. Is this feature required by the current vertical slice, or are we expanding too early?
11. If portability is involved, which exact boundary is being claimed: source build, portable source, verified wheel, wheel installation, or installed execution?
12. Is a proposed workaround solving a demonstrated product requirement or merely removing an observed constraint?
13. If a UI is involved, which application-owned evidence object supplies each displayed fact?
14. Is presentation rendering existing evidence, or quietly acquiring/inferencing new state?
15. Is each displayed fact durable or transient, and does the code recover it only through the boundary that actually owns it?
16. If the UI initiates an action, which named application operation owns that action, and what fresh evidence does it return?
17. After an operation, which live evidence must be retained for the next operation rather than reconstructed from presentation?
18. Does the renderer own only display state, or has transient application/domain state leaked into widgets?
19. If architectural preview is involved, which facts are current and which are merely proposed, and can the user distinguish them before apply?
20. Does any visible preview action accidentally become permission to mutate, or is rationale-bearing apply still a distinct operation?
21. If Apply is involved, is it consuming the exact retained typed preview and explicitly retiring transient evidence that belonged only to the prior architecture?
22. Are multiple application controllers retaining duplicate live evidence that can diverge after the operation?
23. For a combined interactive session, is there exactly one application-owned authority for current run, current READY evidence, and pending architectural intent?
24. Does the renderer receive that live authority once, or has it recreated separate per-action state ownership above the application layer?
25. Does the renderer wait for successful application evidence before replacing current/proposed state, or is it optimistically assuming the operation succeeded?
26. If READY is being restored after architectural change, did a real verified export of the exact current build produce that evidence, or is file/directory presence being mistaken for verification?
27. If a control is evidence-gated, is the gate based on application presentation rather than filesystem observation?
28. If measurement is involved, does it wrap the permanent operation without altering behavior, and does it reuse compiler-owned work classifications rather than infer them?
29. If measurements are compared, are duration/work deltas kept descriptive until there is evidence for any causal or waste interpretation?
30. Do compared measurements identify their Workspace/architectural subject from owned evidence rather than caller assumptions or filesystem shape?
31. If runtime durations are compared, does the evidence say whether the runtime inputs were actually the same without retaining raw payload unnecessarily?
32. If workload identity matches or differs, is that fact being treated as a comparability condition rather than a causal explanation?
33. If execution environments are compared, does the evidence expose only coarse non-identifying context, acquire it outside timed stages, and treat match/mismatch as comparability evidence rather than causal explanation?
34. If repeated observations are grouped, does the cohort prove one exact recorded condition before aggregation, while preserving timing and build-work variation as observations rather than silently normalizing them away?
35. Before any stage summary is computed, are raw durations still paired with the exact work evidence that accompanied them, and are any work-context groups defined by evidence rather than semantic guesswork?

If those answers are unclear, the feature is probably ahead of the architecture.

---

## 14. Handoff guidance for a future development session

A future session should not begin by asking, “What should Pyxis be?”

That question has been explored enough for the minimum slice.

Begin instead with:

> What is the next smallest implementation that makes the permanent `WorkspaceSpec → RIR → compiler → materializer → runtime → verified export → presentation → query → application operation/controller → local UI → measurement` path more usable while preserving its boundaries?

Read the current code before modifying it.

Continue in small commits.

Do not bulk-import the old prototype repositories.

Migrate only behavior whose architectural value is still understood.

When a prototype lesson and current code disagree, reproduce the contradiction with a test before redesigning architecture.

For packaging, Milestone 9 is closed. The portable contract is conventional source plus a verified wheel, and the offline guarantee applies to installing/executing that wheel. Do not reopen offline source-build machinery unless a new real requirement explicitly demands it.

For UI work, Milestones 10A through 10N are complete and Milestone 10 is closed for Repository Zero. `WorkspacePresentation` remains the immutable current-evidence renderer contract; `query_workspace_presentation()` is the existing-Workspace assembly path; the application layer owns runtime/preview/apply/export-refresh behavior and one unified `WorkspaceController`; and Textual performs runtime, Preview, rationale-bearing Apply, and evidence-gated verified export through that one authority. The real headless lifecycle proves READY → Preview/Apply → no READY → verified export → READY, including non-optimistic failure behavior.

For measurement, Milestones 11A through 11G are complete. `measure_build_and_run_workspace()` observes the permanent build/run operation once, records exact stage timing, carries compiler/materializer work facts directly, attaches coherent Repository/Workspace/RIR subject identity, records privacy-preserving runtime-input identity/size evidence, and acquires coarse non-identifying Python/platform environment evidence once before timed stages. `compare_build_and_run_measurements()` remains the pure descriptive boundary for differing observations. `create_build_and_run_measurement_cohort()` is the stricter repeated-condition boundary. `project_build_and_run_measurement_stage_samples()` then exposes ordered raw `build`/`runtime` samples while preserving each cycle's exact `BuildWorkEvidence`.

The next pressure is separating distinct observed work contexts without inventing semantic labels. Milestone 11H should partition each stage's raw samples by exact `BuildWorkEvidence` equality, preserving first-occurrence group order and within-group observation order. Do not compute statistics, call groups warm/cold/cached, persist, render, or infer cause in the same step.

---

## 15. Current continuity sentence

At the 2026-08-12 Milestone 11G closure, Pyxis has a permanent evidence-bearing path from canonical Workspace intent through RIR, deterministic/incremental compiler products, read-only runtime, append-only revisions, exact-byte verified export, conventional package projection, independent package execution, standard wheel construction, fresh network-disabled installation/execution of the verified wheel, immutable current and proposed presentation contracts, an existing-Workspace evidence query, governed runtime/preview/apply/export-refresh application operations, one unified `WorkspaceController`, a complete first local Textual lifecycle, and application-owned measurement/comparison with explicit subject, workload, and execution-environment context plus exact repeated-measurement cohorts and raw per-stage sample projection. Measurement records exact ordered build/runtime durations, carries compiler/materializer work evidence directly from `BuildResult`, identifies the logical Repository/Workspace plus exact RIR state, records SHA-256 plus character/UTF-8 byte counts for runtime input without retaining raw text, and records coarse Python/platform environment identity before stage timing begins. Pairwise comparison remains descriptive across mismatches; cohort construction requires one exact recorded condition; stage projection preserves every raw duration in observation order beside the exact per-cycle `BuildWorkEvidence`, keeping `new`/written and `reused`/no-write observations distinct without causal labeling. Milestone 9 is closed. Milestone 10 is closed with 10A–10N complete. Milestones 11A–11G are complete; the next narrow step is 11H: exact work-context partitioning before statistics, persistence, UI, causal interpretation, or a full Execution Ledger.