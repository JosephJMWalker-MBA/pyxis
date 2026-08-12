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
