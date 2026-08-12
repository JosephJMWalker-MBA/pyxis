# Pyxis Architecture

## Product thesis

Pyxis turns human architectural intent into executable, inspectable systems through a transparent compiler path.

The minimum proven path is:

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

Changes flow through the same path:

```text
preview proposed canonical state
    ↓
show predicted artifact/runtime consequences
    ↓
record rationale
    ↓
append revision
    ↓
write canonical state
    ↓
compile
    ↓
run changed Workspace
```

## Architectural boundaries

### Canonical state

Canonical authoring data is the authoritative expression of intended architecture.

### RIR

The Repository Intermediate Representation is the normalized compiler input derived from canonical state. It makes architectural relationships inspectable before code generation.

### Generated implementation

Generated files are compiler products. UI actions and export logic must not patch generated implementation directly.

### Revisions

Architectural changes are append-only events carrying human rationale, before/after canonical hashes, and compiler completion evidence.

Revision event and completion logs have typed read-only loaders. Existing Workspace queries consume those loaders rather than parsing JSONL outside the revisions persistence layer.

### Presentation

`WorkspacePresentation` is the framework-independent read-only application contract for a future user interface.

It is composed only from evidence already produced by permanent product boundaries:

```text
WorkspaceSpec
    +
BuildAndRunResult
    +
RevisionEvent / RevisionCompletion evidence
    +
optional READY WorkspaceExportResult
    ↓
WorkspacePresentation
```

The presentation layer may validate coherence between those evidence streams, but it does not acquire new facts. It performs no filesystem reads or discovery, no compilation, no runtime execution, no export, and no readiness inference.

The contract preserves the authority of each layer:

- canonical identity, name, description, capabilities, and canonical hash come from authoritative `WorkspaceSpec`;
- RIR structure and identity come from the existing build RIR and generation manifest;
- artifact `new` / `reused` / `regenerated` / `removed` status comes directly from compiler-owned generation evidence;
- runtime output comes from an already-completed run and is exposed recursively through immutable mappings/sequences;
- revision intent remains distinct from optional compiler completion evidence; and
- export presentation is absent until actual evidence-backed `READY` verification exists.

A removed compiler product has no current manifest entry, so presentation must not fabricate current node or artifact hashes for it. A future UI renders these facts rather than scanning files or reconstructing product state itself.

### Existing Workspace query

`query_workspace_presentation()` is the application-owned assembly boundary for reopening an existing Workspace while preserving the distinction between durable and transient evidence.

It reloads durable evidence only through owning persistence APIs:

```text
Workspace root
    ↓
load_workspace_spec()
load_repository_ir()
load_generation_manifest()
load_revision_events()
load_revision_completions()
    +
supplied current BuildAndRunResult
    +
optional supplied WorkspaceExportResult
    ↓
coherence checks
    ↓
create_workspace_presentation()
```

Persisted RIR and generation-manifest evidence must exactly agree with the supplied run before the presentation can be assembled. Revision history is loaded because it is durable. Runtime output and generation statuses are not loaded because Repository Zero does not persist them.

The presence of generated Python files, RIR JSON, or a generation manifest must never be treated as permission to infer generation status or rerun the Workspace automatically. If no current `BuildAndRunResult` is available, the full `WorkspacePresentation` is unavailable until the Workspace is run again or a future explicit persistence design is introduced.

Likewise, an export directory on disk does not imply `READY`. Export facts enter the query only through an actual `WorkspaceExportResult`, and its runtime evidence must identify the queried physical source Workspace. This prevents identical copies of a Workspace from accidentally borrowing each other's transient export evidence.

The query boundary is read-only application orchestration. It does not compile, execute, classify, verify exports, scan arbitrary files, or synthesize missing facts.

### Application-owned Workspace operations

A UI event may not jump from Textual directly into compiler/runtime/revision/export/persistence layers. Named application operations own action semantics and return fresh evidence that the renderer can consume.

Milestone 10E establishes the first operation with `rerun_workspace()`:

```text
Workspace root
    +
current BuildAndRunResult
    +
new runtime text
    +
optional existing WorkspaceExportResult
    ↓
query_workspace_presentation() preflight
    ↓
run_materialized_workspace()
    ↓
new BuildAndRunResult using the same BuildResult
    ↓
query_workspace_presentation()
    ↓
WorkspaceRerunResult
    ├── fresh BuildAndRunResult
    └── fresh WorkspacePresentation
```

The preflight deliberately happens before runtime execution. It rejects stale run evidence or mismatched export evidence against the persisted Workspace before generated code can run.

A successful rerun is runtime-only. It executes the already-materialized generated entrypoint exactly once and reuses the exact existing `BuildResult`. It does not compile, classify generation status, materialize artifacts, mutate revisions, export, or verify an export.

Optional existing READY evidence may remain part of the returned presentation because no architectural/compiler state changed. That evidence retains its original verification input hash; a rerun with different text does not transform the old READY proof into verification of the new input.

`WorkspaceRerunResult` returns both fresh transient run evidence and the presentation derived from it.

Milestone 10F adds `WorkspaceRuntimeController` as the smallest application-owned live-state holder needed by the first interactive renderer. It retains the Workspace root, current `BuildAndRunResult`, and optional existing export evidence. Its only operation delegates to `rerun_workspace()`, replaces the retained run only after a successful rerun, and returns the fresh `WorkspacePresentation`.

The controller is not a new runtime or session implementation. It exists so transient run evidence remains application-owned across repeated UI events rather than being reconstructed from rendered presentation fields.

### Application-owned architectural preview

Milestone 10G introduces the first UI-facing architectural preview seam without adding a mutation control.

The application path is:

```text
Workspace root
    +
current BuildAndRunResult
    +
optional existing WorkspaceExportResult
    ↓
query_workspace_presentation() preflight
    ↓
load_workspace_spec()
    ↓
preview_remove_normalize_text()
    ↓
ArchitecturePreview
    ↓
create_architecture_preview_presentation()
    ↓
ArchitecturePreviewPresentation
```

The preflight requires the caller's live run/READY evidence to still match the persisted Workspace before the proposed architecture is created. The canonical state is then reloaded through its owning persistence boundary rather than reconstructed from presentation fields.

`ArchitecturePreviewPresentation` is immutable and contains only preview facts already justified by current/proposed canonical intent and the existing `ArchitecturePreview`: current/proposed canonical identity and SHA-256, capability additions/removals, predicted added/changed/removed artifact paths, and the current/proposed observable runtime-key contract. It does not compile proposed artifacts or execute proposed generated code.

`WorkspaceArchitecturePreviewController` retains the typed pending `ArchitecturePreview` for a later rationale/apply operation while returning only presentation-safe preview evidence from its preview method.

A pending preview is not current Workspace state. Preview creation performs no canonical write, compiler invocation, materialization, revision append, runtime execution, export, or READY verification. Therefore the current `BuildAndRunResult` and legitimate current READY evidence remain valid until an apply operation actually commits new canonical intent.

### Application-owned architectural apply

Milestone 10I proves the first rationale-bearing architectural mutation seam independently of Textual.

The application path is:

```text
Workspace root
    +
exact retained ArchitecturePreview
    +
current BuildAndRunResult
    +
optional current WorkspaceExportResult
    +
non-empty human rationale
    +
explicit runtime text
    ↓
query_workspace_presentation() preflight
    ↓
confirm preview current canonical hash
    ↓
apply_remove_normalize_text()
    ↓
append revision intent
    ↓
build_workspace(proposed_spec)
    ↓
append revision completion
    ↓
run_materialized_workspace(new RepositoryIR)
    ↓
fresh BuildAndRunResult
    ↓
query_workspace_presentation(export=None)
    ↓
WorkspaceArchitectureApplyResult
```

The operation does not reconstruct the proposal from renderer fields and does not call preview again at Apply time. The exact typed `ArchitecturePreview` retained by the application controller is the object passed to the existing governed `apply_remove_normalize_text()` boundary.

Rationale is required and normalized before any mutation. Current run/export evidence is preflighted before the governed apply path begins. The existing apply layer remains responsible for validating that the preview still matches canonical intent and the supported edit, appending the intent-bearing revision before canonical/compiler mutation, building through the permanent compiler/materializer path, and appending completion only after a successful build.

`BuildAndRunResult` does not contain the runtime input that originally produced it. The apply operation therefore requires explicit runtime text rather than deriving or guessing input from runtime output. After the new build succeeds, the newly materialized Workspace is executed exactly once and its result becomes fresh transient run evidence.

Architectural mutation invalidates pre-change READY as current evidence. The prior portable directory may remain physically present, but its `WorkspaceExportResult` is not passed into the post-apply query because it verified the old RIR/compiler products. A newly applied Workspace presents no READY evidence until a new export verification operation proves the new state.

`WorkspaceArchitecturePreviewController` retains the resulting fresh `BuildAndRunResult`, clears its retained export evidence, and clears the consumed pending preview only after the application operation returns successfully. Validation or governed-apply failure leaves the controller's retained values unchanged.

Milestone 10I still adds no Textual rationale input or Apply control. Renderer mutation remains unavailable until the UI can invoke this already-proven application boundary without creating a second live-state owner.

### First local Workspace UI

Textual is the selected framework for the first local Workspace UI. It is introduced as an optional renderer dependency and remains strictly downstream of the application-owned presentation and operation boundaries.

The proven interactive path is now:

```text
current evidence:
WorkspacePresentation
    +
optional WorkspaceRuntimeController
    +
optional WorkspaceArchitecturePreviewController
    ↓
WorkspaceShell (Textual)
    ↓
WorkspaceDetail

runtime interaction:
Input.Submitted
    ↓
WorkspaceRuntimeController.rerun(text)
    ↓
fresh WorkspacePresentation
    ↓
WorkspaceDetail.replace_presentation()

architecture preview interaction:
Button.Pressed
    ↓
WorkspaceArchitecturePreviewController.preview_remove_normalize_text()
    ↓
ArchitecturePreviewPresentation
    ↓
ArchitecturePreviewDetail
```

`WorkspaceShell` still receives no Workspace root and no compiler/runtime/revision/export/persistence service. It may receive application-owned controllers alongside the current immutable presentation.

Milestone 10C proved the renderer boundary with a minimal summary shell. Milestone 10D extends the same shell with `WorkspaceDetail`, a vertically scrollable evidence surface that renders the complete current presentation contract:

- canonical Workspace ID, name, description, capabilities, and canonical SHA-256;
- RIR schema version, Repository/Workspace IDs, entrypoint, capabilities, and RIR SHA-256;
- every compiler artifact path, generation status, node SHA-256, and artifact SHA-256 where current evidence exists;
- the complete immutable runtime result formatted as JSON for inspection;
- every revision event with rationale, before/after canonical identity, parent relationship, completion state, and optional completion hashes; and
- optional export READY evidence including export root, RIR/manifest/input hashes, and compiler-product count.

Optional evidence remains explicitly absent when it was not supplied. `No READY evidence` means exactly that; the renderer does not convert absence into an inferred `NOT READY` state. Likewise a `removed` compiler artifact remains visible as `removed` while its current node/artifact hashes remain absent.

Milestone 10E proves the application-owned runtime rerun seam independently before a control is connected.

Milestone 10F introduces the first visible runtime interaction: one Textual `Input` whose Enter submission calls only `WorkspaceRuntimeController.rerun()`. The returned presentation replaces the fields in the existing `WorkspaceDetail`; the shell also retains that presentation for rendering identity, while the controller retains the fresh `BuildAndRunResult` needed by the next operation.

`WorkspaceDetail.replace_presentation()` is renderer-only. It updates existing `Static` widgets from a supplied immutable presentation and performs no evidence acquisition or domain work.

Milestone 10G proves the architectural preview presentation/controller boundary independently before a visible architecture control is connected.

Milestone 10H introduces exactly one visible architectural action: a button that calls only `WorkspaceArchitecturePreviewController.preview_remove_normalize_text()`. Its result is rendered in `ArchitecturePreviewDetail`, a separate proposed-state panel labeled `PROPOSED — NOT APPLIED` and visually distinguished from `WorkspaceDetail`.

The preview panel shows current/proposed canonical hashes and capabilities, predicted compiler-product path consequences, and current/proposed runtime-key contracts. Displaying it does not replace `WorkspaceShell.presentation`, update current Workspace evidence, invalidate READY, write files, compile, append revisions, or execute runtime code. The typed pending preview remains in the application controller.

Milestone 10I proves the rationale-bearing apply operation/controller seam but deliberately leaves Textual unchanged. The renderer therefore still exposes Preview only; it has no rationale field or Apply action yet.

Textual belongs to the optional `ui` dependency group; the compiler/runtime core retains no required UI dependency. Headless Textual tests belong in the ordinary Repository Zero pytest suite so UI behavior remains subject to the same evidence discipline as other product boundaries.

D084 selects Textual for the first local evidence UI only. D085 requires complete evidence visibility before mutation controls. D086 requires UI actions to cross named application-owned operation boundaries. D087 keeps transient run evidence in the application controller rather than the renderer. D088 keeps proposed architecture distinct from current Workspace/READY evidence until apply. D089 requires visible proposed architecture to remain visibly separate from current evidence. D090 requires apply to consume that retained preview and invalidates pre-change READY as current evidence. Future browser/research surfaces remain independent product decisions and must not bypass `WorkspacePresentation` or application operations merely because another rendering technology becomes appropriate.

### Export

Export is packaging, not compilation. It packages existing compiler products and verifies their identity and runtime behavior.

Portable packaging keeps two forms deliberately distinct:

- `generated/` remains the original compiler-product/evidence surface.
- the conventional `src/` package layout is an exact-byte projection of those compiler products plus packaging-only support files.

The Repository Zero portability chain is:

```text
exact compiler products
      ↓
verified portable source repository
      ↓
conventional src/ projection
      ↓
standalone package runtime without Pyxis
      ↓
standard wheel built with ordinary PEP 517 tooling
      ↓
wheel payload identity verification
      ↓
fresh network-disabled wheel installation
      ↓
installed console execution with matching behavior
```

The **portable deliverable** is the pair:

```text
conventional source repository + verified wheel
```

The two forms serve different purposes. The source repository preserves inspectability, provenance, conventional Python structure, and the exact relationship back to compiler products. The verified wheel is the offline-installable execution artifact whose payload identity and behavior have already been proven.

The permanent portability guarantee is therefore:

- the conventional source repository can build a standard wheel when its declared PEP 517 build dependencies are obtainable;
- the included verified wheel preserves compiler-product identity;
- that verified wheel can be installed and executed in a fresh environment with network access blocked, no external build dependencies, and no Pyxis participation; and
- installed behavior matches the already-verified Workspace behavior.

Offline source-to-wheel construction is **not** a Repository Zero requirement. Milestone 9M deliberately characterized that stronger condition and reproduced its failure: with network/index access blocked and normal PEP 517 build isolation preserved, the isolated environment cannot resolve `setuptools>=77.0.3`, so no wheel is produced.

That observation remains useful evidence about the source form, but D081 accepts it as a conventional build-time dependency boundary rather than introducing bespoke packaging machinery. A future requirement may reopen that decision only if an actual product need demands raw-source offline rebuilding.

### Milestone 9 closure

Repository Zero considers export/portability proven when the exact compiler products can be exported with provenance, verified for identity and runtime behavior, projected into a conventional Python source repository, built into an identity-verified wheel, and that verified wheel can be installed and executed offline with matching behavior.

Milestone 9 does not require a second build backend or self-contained offline reconstruction of the wheel from raw source.

## Minimum permanent demonstrator

`examples/text_lab/` should remain the executable architectural specification for the first vertical slice.

Its two initial capabilities are deliberately simple:

- `inspect_text`
- `normalize_text`

They exist to prove the compiler and revision model, not because text utilities are the long-term product domain.

## Deferred concerns

The following remain important but should not expand Repository Zero until the vertical slice is stable:

- browser integration
- broader capability catalog
- provider-neutral AI services
- timing and waste instrumentation
- security permission models
- educational overlays beyond compiler inspection
- deployment integrations
