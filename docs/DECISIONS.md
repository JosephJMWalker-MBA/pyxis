# Pyxis Decision Record

This document captures the implementation decisions proven during prototyping and carried into Repository Zero.

## D063 — Preview-first historical reapply
Historical canonical state is never applied directly. Reapplication previews architectural consequences and creates a new revision.

## D064 — Consolidate into one minimal product
A capability is not part of Pyxis until it participates in the same Workspace, compiler, runtime, and revision path.

## D065 — Independent export
Exported compiler products must run independently of the Pyxis source tree.

## D066 — Verified export
An export is READY only after provenance and runtime verification succeed.

## D067 — Visible READY state
First-run UX should end in a visible readiness state derived from verification evidence.

## D068 — Minimal Workspace creation
First-run Workspace creation begins with only a name and description.

## D069 — Created Workspaces run immediately
The first user-created Workspace must execute the generated entrypoint from its own detail screen.

## D070 — Preview architecture edits before mutation
Preview may derive proposed canonical/RIR states but may not mutate canonical or generated files.

## D071 — Rationale belongs in provenance
Architectural changes require human rationale before compilation and append a revision event.

## D072 — Restore is not rollback
Restoration creates a new intent-bearing revision through the same compiler path; history remains immutable.

## D073 — Preview observable runtime contract
Pyxis may predict runtime capability surfaces that follow directly from canonical structure, without simulating implementation behavior.

## D074 — Consolidate before expanding
Proof-specific surfaces should be removed in favor of one coherent first-run product path.

## D075 — Export is packaging, not compilation
Export packages exact compiler products and must not reinterpret or regenerate implementation.

## D076 — Export belongs in the Workspace journey
A user should reach verified portable output from the same first-run Workspace experience.

## D077 — Conventional package shape
Portable output should resemble a normal Python repository rather than a special Pyxis-only artifact.

## D078 — Self-contained portability proof
The minimum exported repository can be installed and executed without network access or external build dependencies while preserving generated artifact identity.

D081 defines the permanent Repository Zero interpretation of this requirement: the offline guarantee applies to the verified wheel included with the portable deliverable, not to rebuilding that wheel from source while offline.

## D079 — Separate source-build and wheel-install portability proofs
Repository Zero must treat source-to-wheel construction and wheel installation as separate evidence boundaries.

The permanent proof establishes that a conventional source package can build a standard wheel using ordinary PEP 517 tooling when its build dependencies are obtainable, and that a verified prebuilt wheel can then be installed and executed in a fresh environment with network access blocked and without Pyxis participating.

Milestone 9M separately tested the stronger source-build condition without altering the package shape: normal PEP 517 build isolation was preserved, network/index access was disabled, no build dependencies were vendored or injected, and no fallback backend was provided. Under those conditions the current source package fails before wheel construction because the isolated build environment cannot resolve its declared `setuptools>=77.0.3` requirement.

The successful offline wheel-install proof therefore remains distinct from the reproduced offline source-build failure.

## D080 — Reproduce a portability constraint before choosing its remedy
The 9M failure establishes that the stronger interpretation of D078—raw exported source must construct its wheel with no network or externally available build dependency—is **not satisfied by the current conventional package**.

That evidence does not select a solution. Repository Zero must not reintroduce the prototype's local build backend, vendor Setuptools, disable normal build isolation, or otherwise change packaging merely to make the test green. First decide whether offline source-to-wheel construction is actually a required product property. Only then should a remedy be evaluated against the existing constraints: exact compiler-product identity, conventional portable shape where possible, and export remaining packaging rather than compilation.

## D081 — Portable deliverable is conventional source plus a verified wheel
Repository Zero resolves the D078 scope question in favor of the smallest proven product contract.

A portable Pyxis Workspace consists of:

- the conventional source repository containing the exact compiler products and inspectable provenance evidence; and
- a verified wheel built from that source projection whose compiler-product payload identity has been checked against the same evidence.

The portability guarantee is that the **verified wheel can be installed and executed in a fresh environment without network access, external build dependencies, or Pyxis participation while preserving the proven Workspace behavior**.

Rebuilding the wheel from raw source while offline is not a Repository Zero product requirement. Conventional source builds may use ordinary PEP 517 build isolation and may require their declared build dependencies to be obtainable.

The Milestone 9M offline source-build failure remains valuable characterization evidence, but it is an accepted limitation of the source form under this contract rather than a defect requiring a bespoke backend. Repository Zero will not vendor build tooling, weaken normal build isolation, or reintroduce the prototype local backend solely to eliminate that limitation.

This decision closes the Milestone 9 packaging requirement. Future packaging work must be driven by a new demonstrated product need rather than by the stronger D078 interpretation that D081 has now explicitly declined.

## D082 — Workspace presentation is an application-owned evidence adapter
A user interface must consume a read-only Workspace presentation contract assembled from evidence Pyxis already owns. The presentation layer may validate that supplied evidence belongs to the same Workspace, but it may not load or scan repository files, compile, execute runtime code, export, infer compiler status, or synthesize readiness.

Canonical identity must come from authoritative `WorkspaceSpec`, not copied RIR fields. RIR identity and compiler artifact status come from existing build/manifest evidence. Runtime output comes from an existing run result. Revision presentation preserves append-only event intent separately from optional compiler completion evidence. Export presentation exists only when actual `READY` verification evidence is supplied.

The presentation contract itself must remain read-only. Runtime mappings/sequences are recursively exposed as immutable values so a UI cannot mutate application evidence through the view model. A `removed` artifact status must not invent current hashes that no longer exist in the current generation manifest.

This boundary is framework-independent. A future UI renders the contract; it does not become a second query, compiler, runtime, revision, or verification implementation.

## D083 — Existing Workspace queries separate durable and transient evidence
An application query for an existing Workspace may reload only evidence that has an owning persistence boundary: canonical `WorkspaceSpec`, persisted RIR, generation manifest, and append-only revision event/completion history.

Runtime output and generation statuses remain transient evidence. The existence of generated files, a manifest, or an RIR does not permit the query layer to recreate `BuildAndRunResult`, infer `new`/`reused`/`regenerated`/`removed`, or execute the Workspace automatically. A caller must supply the current `BuildAndRunResult`, and it must agree with the persisted RIR and generation manifest before presentation is assembled.

Export readiness is transient verification evidence under the current Repository Zero model. A portable directory on disk does not imply `READY`. Export presentation may be included only when the actual `WorkspaceExportResult` is supplied, refers to the queried source Workspace, and remains coherent with its verified export root.

Revision history is durable evidence and therefore gains typed read-only loaders owned by the revisions persistence layer. The application query consumes those loaders rather than parsing JSONL itself.

This decision keeps reopening an existing Workspace honest: durable facts can be recovered after process loss; transient facts must be rerun or explicitly retained rather than reconstructed heuristically.

## D084 — Textual is the first local Workspace UI framework
Repository Zero selects Textual for the first local Workspace UI because it satisfies the current product need with the smallest new runtime surface: Python-native application code, local cross-platform execution, built-in interactive widgets/layout/styling, and a headless test harness that can be exercised directly from pytest.

Textual is a renderer boundary only. `WorkspaceShell` receives an existing immutable `WorkspacePresentation`; it does not accept a Workspace path and must not load/query persisted state, compile, run generated code, mutate revisions, export, or infer readiness. Textual therefore sits strictly downstream of D082 and D083.

The framework is installed through the optional `ui` extra rather than becoming a dependency of Pyxis's compiler/runtime core. Development dependencies include Textual only so the normal Repository Zero CI suite can execute the UI boundary headlessly.

This is a decision about the **first local evidence UI**, not a permanent claim that every future Pyxis surface must use Textual or remain terminal-based. Textual can run locally and may also be served in a browser, but future browser/research integration must be selected from its own demonstrated product requirements rather than being forced through D084.

The alternatives considered were intentionally rejected for the current slice, not categorically: NiceGUI introduces a local web-server and browser frontend stack; PySide6 introduces a substantially heavier native Qt/platform surface; Streamlit's whole-script rerun model is a poor match for Pyxis's explicit application-operation boundaries; and Flet's shipped-app integration path brings a Flutter build/test toolchain before Repository Zero needs desktop/mobile packaging.

## D085 — Complete Workspace evidence is rendered before UI actions exist
The first genuine Workspace detail screen must render the complete current `WorkspacePresentation` contract before the renderer gains mutation controls.

The read-only detail surface includes authoritative canonical intent and hash, RIR identity and hash, every compiler artifact status and current integrity identity, the full runtime result, the append-only revision timeline including optional completion evidence, and the complete optional export READY evidence. Missing optional evidence is rendered explicitly as absent; it is not converted into a guessed negative state.

Renderer formatting may make immutable evidence legible—for example by formatting runtime mappings as JSON or displaying absent hashes as an em dash—but it may not acquire, derive, classify, execute, verify, or mutate application state. A `removed` compiler artifact therefore remains `removed` with no invented current hashes.

Milestone 10D deliberately contains no buttons or mutation callbacks. Information architecture and evidence visibility are proven before UI events are connected to application operations. Navigation/layout mechanisms may evolve later without weakening D082/D083 or changing the evidence contract.

## D086 — UI actions cross an application-owned operation boundary
A renderer must not invoke compiler, runtime, revision, export, or persistence services directly. A user action first crosses a named application operation whose inputs, coherence checks, side effects, and returned evidence can be tested without a UI framework.

Milestone 10E proves the first such seam with `rerun_workspace()`, a non-architectural runtime-only operation. It accepts the Workspace root, the caller's current `BuildAndRunResult`, new runtime text, and optional existing `WorkspaceExportResult`.

Before generated code executes, the operation uses `query_workspace_presentation()` to require that supplied live run/export evidence still belongs to the persisted Workspace. Stale evidence therefore fails before runtime. On success the operation executes the existing materialized entrypoint exactly once, reuses the exact same `BuildResult`, creates a fresh `BuildAndRunResult`, and queries a fresh immutable `WorkspacePresentation`.

A runtime-only rerun does not compile, classify generation status, materialize artifacts, mutate revisions, export, or re-verify READY. Existing legitimate export evidence may remain visible because architecture and compiler products did not change; its recorded verification input hash remains the input that was actually verified and must not be relabeled as verification of the new runtime input.

The application result carries both the fresh transient run evidence and the fresh presentation so a future UI controller can retain the former while rendering only the latter. Milestone 10E intentionally adds no Textual callback or button; the operation boundary is proven independently before the first control is wired.

## D087 — Visible runtime interaction retains live evidence outside the renderer
The first visible Workspace interaction is a single Textual text-input submission connected only to an application-owned `WorkspaceRuntimeController`.

The controller retains the current transient `BuildAndRunResult`, Workspace root, and optional existing export evidence. Its `rerun(text)` method delegates to the already-proven `rerun_workspace()` operation, replaces its retained run evidence only after success, and returns the fresh `WorkspacePresentation` to the renderer. Textual therefore does not own or reconstruct the transient run state required by the next operation.

`WorkspaceShell` receives the controller as one application boundary rather than receiving compiler, runtime, revision, export, or persistence services. When the runtime `Input` is submitted, the shell calls the controller exactly once and replaces the fields in the existing `WorkspaceDetail` from the returned presentation. `WorkspaceDetail` remains presentation-only.

Milestone 10F introduces no button and no architectural mutation. The headless acceptance path proves that the single submission changes only runtime evidence on screen while canonical, RIR, compiler, revision, and export presentation remain unchanged; the controller retains the new run evidence; compilation remains unavailable; and both Workspace and portable-export bytes remain unchanged.

This establishes the first complete UI event loop without weakening D082–D086:

```text
Textual Input.Submitted
    ↓
WorkspaceRuntimeController.rerun(text)
    ↓
rerun_workspace()
    ↓
fresh BuildAndRunResult retained by controller
    +
fresh WorkspacePresentation returned to renderer
    ↓
WorkspaceDetail refresh
```

## D088 — Architectural preview is proposed evidence, not current Workspace state
A UI-facing architecture preview must be assembled through an application-owned preview boundary before any rationale/apply control is introduced.

Milestone 10G adds `preview_workspace_remove_normalize_text()`. The operation first preflights the supplied current `BuildAndRunResult` and optional READY evidence through `query_workspace_presentation()`, then reloads authoritative canonical intent and invokes the already-proven in-memory `preview_remove_normalize_text()` path. Stale live evidence is therefore rejected before preview creation.

`ArchitecturePreviewPresentation` exposes only immutable presentation-safe facts already owned by that preview: current/proposed canonical identity and hashes, capability additions/removals, predicted added/changed/removed compiler-product paths, and current/proposed observable runtime-key contracts. It does not compile generated implementation or execute a shadow runtime to enrich the preview.

`WorkspaceArchitecturePreviewController` retains the typed pending `ArchitecturePreview` needed by a later rationale-bearing apply operation while returning only `ArchitecturePreviewPresentation` from its preview method. Creating a preview does not mutate canonical state, materialize artifacts, append revisions, execute runtime code, export, or invalidate the current run/READY evidence.

A pending preview therefore means only **proposed intent exists in memory**. Current Workspace presentation and current READY evidence remain current until a later application-owned apply operation commits the proposal through the canonical → RIR → compiler → revision path.

## D089 — Visible architectural preview remains visually separate from current evidence
The first visible architectural action is preview-only. `WorkspaceShell` may receive a `WorkspaceArchitecturePreviewController` and expose exactly one button for previewing removal of `normalize_text`.

Pressing that button calls only `WorkspaceArchitecturePreviewController.preview_remove_normalize_text()` and sends the returned immutable `ArchitecturePreviewPresentation` to a dedicated `ArchitecturePreviewDetail` renderer. The preview renderer is separate from `WorkspaceDetail` and labels its content `PROPOSED — NOT APPLIED` so proposed canonical hashes, capabilities, compiler-product paths, and runtime keys cannot be mistaken for current Workspace evidence.

Creating or displaying the preview must not replace `WorkspaceShell.presentation`, mutate `WorkspaceDetail`, invalidate existing READY evidence, write files, compile, append a revision, or execute runtime code. The application controller retains the typed pending preview; Textual owns only the button event and proposed-evidence display state.

Milestone 10H deliberately adds no rationale field and no Apply control. A visible preview is still only proposed intent. Mutation remains unavailable until a separately proven rationale-bearing application operation exists.

## D090 — Architectural apply consumes the retained preview and invalidates pre-change READY
The first application-owned architectural mutation operation must consume the exact typed `ArchitecturePreview` retained by the preview controller. It may not recreate a proposal from renderer fields or from a second preview call at Apply time.

Milestone 10I adds `apply_workspace_remove_normalize_text()`. The operation requires a non-empty human rationale, preflights the caller's current `BuildAndRunResult` and optional current `WorkspaceExportResult`, confirms the pending preview still describes the current canonical Workspace, and then delegates mutation to the existing governed `apply_remove_normalize_text()` path. That governed path remains the owner of revision append, canonical mutation, compilation/materialization, generation status, and completion evidence.

Because `BuildAndRunResult` does not persist the runtime input that produced it, the operation requires explicit runtime text rather than inferring input from rendered/runtime output. After governed apply succeeds, the operation executes the newly materialized Workspace once, creates a fresh `BuildAndRunResult`, and queries a fresh `WorkspacePresentation` from the new durable/transient evidence.

Pre-change READY evidence is deliberately not carried into that post-apply presentation. The old portable directory may still exist, but its verification belongs to the pre-change RIR/compiler products and therefore is not current evidence after architecture changes.

`WorkspaceArchitecturePreviewController` updates its retained run, clears its retained export evidence, and clears the consumed pending preview only after the application operation returns successfully. Validation or governed-apply failure leaves those retained controller values unchanged. Milestone 10I adds no Textual rationale or Apply control; mutation ownership is proven independently before rendering can invoke it.

## D091 — One live Workspace controller owns transient interaction state
A combined interactive Workspace session must have one application-owned authority for the transient state shared by runtime and architectural operations: one current `BuildAndRunResult`, one optional current `WorkspaceExportResult`, and one optional pending `ArchitecturePreview`.

Milestone 10J adds `WorkspaceController`. Its methods delegate only to the already-proven `rerun_workspace()`, `preview_workspace_remove_normalize_text()`, and `apply_workspace_remove_normalize_text()` operations. The controller does not absorb runtime, preview, revision, compiler, export, or presentation implementation.

A successful runtime rerun replaces the one current run while preserving still-valid READY evidence and any pending architecture preview because canonical/RIR/compiler identity has not changed. Preview is created against that same current run and retained as the exact typed proposal for Apply. Successful Apply consumes that retained preview, replaces the same current run with post-apply evidence, clears pre-change READY, and clears the consumed preview. A later runtime rerun therefore necessarily uses the post-apply `BuildResult` rather than a stale pre-change copy.

Controller state advances only after delegated operations return successfully. Failure must not partially replace the shared run/export/preview state.

The specialized `WorkspaceRuntimeController` and `WorkspaceArchitecturePreviewController` remain temporarily for compatibility with the already-proven Textual slices, but they must not be composed as independent live-state authorities in the eventual combined UI. Textual remains unchanged in 10J; the renderer should migrate to `WorkspaceController` before rationale/Apply controls are exposed.

## Repository Zero rule

New implementation work should extend the permanent vertical slice rather than create another disposable proof repository.
