# Pyxis Architecture

**Current through Milestone 11T / D115.**

This is the canonical current architecture. The detailed pre-consolidation architecture remains preserved in Git history at commit `675f2b5e37b5edb32d17e9e480a4d16246826486`; the milestone records remain the narrow proof trail for 11K–11T.

## Product thesis

Pyxis turns human architectural intent into executable, inspectable systems through a transparent compiler path:

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

Architectural change follows the same authority chain:

```text
preview proposed canonical state
    ↓
show predicted consequences
    ↓
record human rationale
    ↓
append revision intent
    ↓
write canonical state
    ↓
compile + materialize
    ↓
append completion evidence
    ↓
run the changed Workspace
```

Generated code is never a second source of truth.

## Permanent authority boundaries

### Canonical authoring state

`WorkspaceSpec` is the authoritative expression of intended architecture. UI, restore, export, and runtime paths may not patch generated files to simulate an architectural change.

### Repository Intermediate Representation

RIR is normalized compiler input derived from canonical state. It makes Repository/Workspace/capability relationships and exact RIR identity inspectable before code generation.

### Compiler and incremental generation

The compiler is deterministic and returns explicit compiler products plus generation evidence. Artifact status is one of `new`, `reused`, `regenerated`, or `removed`.

Reuse is justified only when semantic node identity is unchanged, the current compiler output still matches the prior manifest identity, and the already-materialized artifact still matches that identity. Classification itself is pure and does not scan the filesystem. Materialization separately writes new/regenerated products, preserves proven reused products, and removes only paths previously owned by the manifest.

Compiler output remains separate from filesystem materialization; runtime never compiles.

### Revisions

Architectural mutation is append-only provenance. A revision records human rationale and before/after canonical identity before the governed compiler path mutates current architecture. Completion evidence is appended only after compilation/materialization succeeds. Restore/reapply creates a new revision; history is not rewritten.

### Runtime

Runtime executes already-materialized generated code. Runtime-only reruns reuse the exact current `BuildResult`; they do not compile, reclassify generation status, mutate revisions, or re-establish READY.

### Export and READY

Export is packaging, not compilation. It packages the exact existing compiler products, projects them into a conventional Python source repository, verifies identity and runtime behavior, and may include a verified wheel.

READY exists only when actual verification evidence exists. Destination presence is never sufficient. An architectural Apply invalidates pre-change READY as current evidence; READY can re-enter live state only through a fresh verified export of the exact current build.

The portable deliverable remains `conventional source repository + verified wheel`. Offline installation/execution is guaranteed for the verified wheel, not for rebuilding that wheel from raw source without access to declared build dependencies.

## Application and presentation boundaries

### WorkspacePresentation

`WorkspacePresentation` is the framework-independent read-only adapter for evidence Pyxis already owns. It may validate coherence but may not discover files, compile, execute runtime code, export, classify generation status, or infer readiness.

Canonical identity comes from `WorkspaceSpec`; RIR/compiler facts come from existing build/manifest evidence; runtime output comes from an already-completed run; revision history comes from the revisions persistence layer; READY appears only from supplied verified export evidence.

### Existing Workspace query

`query_workspace_presentation()` reloads only durable evidence through owning persistence APIs and requires callers to supply transient run/export evidence. Persisted files never authorize inference of transient generation status, runtime output, or READY.

### Named application operations

Renderer events cross named application operations rather than compiler/runtime/revision/export services directly. Repository Zero proves runtime rerun, architecture preview, rationale-bearing Apply, and verified export refresh as application-owned seams.

### One live Workspace controller

`WorkspaceController` is the single application-owned transient-state authority for a live session:

```text
current BuildAndRunResult
+ optional current WorkspaceExportResult
+ optional pending ArchitecturePreview
```

Its methods delegate to the established application operations and advance retained state only after successful operation results.

## First local Workspace UI

Textual is an optional renderer dependency, not a compiler/runtime dependency. The live shell receives immutable presentation evidence plus the optional `WorkspaceController`; it receives no Workspace root or lower-level services.

The completed local lifecycle can:

- render canonical, RIR, compiler, runtime, revision, and optional READY evidence;
- rerun the current materialized Workspace;
- preview one controlled architectural change separately from current evidence;
- require visible human rationale before Apply;
- advance current evidence only after successful governed Apply;
- retire pre-change READY after architecture changes; and
- restore READY only through verified export refresh.

Renderer status/error messages are explicitly non-evidence.

## Application-owned measurement

Measurement was added only after the build/run and UI boundaries were stable. It observes the established `build_and_run_workspace()` path rather than duplicating it.

The current measurement evidence pipeline is:

```text
11A  measured build/run
     exact build + runtime durations
     exact compiler/materializer work evidence
      ↓
11B  pairwise descriptive comparison
      ↓
11C  Repository / Workspace / exact RIR subject identity
      ↓
11D  privacy-preserving runtime-input identity
      ↓
11E  coarse execution-environment identity
      ↓
11F  exact-condition repeated-measurement cohort
      ↓
11G  raw stage samples retaining exact work evidence
      ↓
11H  partition by exact BuildWorkEvidence equality
      ↓
11I  count / minimum / maximum envelope
      ↓
11J  median
      ↓
11K  arithmetic mean, independently recomputed from raw durations
      ↓
11L  population standard deviation using the complete group denominator
      ↓
11M  provenance-checked descriptive summary bundle
      ↓
11N  read-only measurement summary presentation
      ↓
11O  presentation-only Textual renderer
      ↓
11P  optional supplied snapshot in the normal Workspace shell
      ↓
11Q  Repository / Workspace / exact RIR co-display gate
      ↓
11R  live invalidation after successful RIR-changing Apply
      ↓
11S  transient non-evidence invalidation notice
      ↓
11T  caller-supplied current-RIR presentation may re-enter through the same gate
```

### Measurement invariants

Measurement evidence remains descriptive and inspectable back to its source objects.

- Work facts come from `BuildResult`; measurement does not rediscover them.
- Cohorts require exact subject/RIR, workload, environment, and stage-contract equality.
- Raw duration observations retain exact work context before summary.
- Work-context groups are equality classes of `BuildWorkEvidence`, not inferred semantic states.
- Count/min/max, median, mean, and population standard deviation remain separate immutable evidence layers with exact source provenance.
- Mean is recomputed from raw observations; it is not derived from median.
- Population standard deviation describes the complete recorded group and makes no inferential population claim beyond that group.
- The summary bundle validates links and introduces no new value.
- Presentation/rendering introduces no new statistic, score, label, acquisition, persistence, or causal interpretation.

No current measurement layer calls a group warm, cached, cold, first-run, steady-state, normal, or outlier. Timing differences are not converted into efficiency, waste, performance quality, or causal claims.

## Live measurement provenance

A supplied measurement presentation can be co-displayed only when its subject matches the current Workspace presentation on:

```text
Repository ID
Workspace ID
exact RIR SHA-256
```

The gate reads existing evidence only.

Runtime reruns, export refresh, preview, and failed operations that leave the exact RIR unchanged preserve a coherent supplied snapshot. After a successful RIR-changing Apply, the stale snapshot is removed only after Apply succeeds. A fixed notice may then explain that the prior snapshot described the previous RIR; that notice is UI status, carries no measurement object/statistics, adds no controls, and expires on the next user operation.

Milestone 11T adds one narrow re-entry seam: while no measurement snapshot is mounted, a caller may supply an already-produced `BuildAndRunMeasurementSummaryPresentation`. The shell applies the same Repository/Workspace/RIR gate before UI mutation, mounts the exact object on success, and clears the old invalidation notice only after successful mount. Mismatch fails without changing shell evidence. Re-entry is not replacement, refresh, acquisition, re-projection, or recomputation.

## Minimum permanent demonstrator

`examples/text_lab/` remains the executable architectural specification. `inspect_text` and `normalize_text` are controlled test weights, not the long-term product domain.

The first architecture operation remains demonstrator-specific. Do not generalize it merely for aesthetic symmetry; a second genuine architecture edit should supply the evidence for a more general operation model.

## Deferred concerns

Repository Zero should not expand merely because a possible feature exists. Deferred concerns include broader capability catalogs, browser/research integration, generalized permission/security models, full Execution Ledger persistence or generalized waste interpretation, broader operation timing, deployment integrations, and additional measurement statistics absent a concrete product need.

## Historical detail

For the exact detailed architecture before this consolidation, read the version of this file at commit `675f2b5e37b5edb32d17e9e480a4d16246826486`. For later measurement evolution, read `MILESTONE_11K_CONTINUITY.md` and `MILESTONE_11L.md` through `MILESTONE_11T.md`. Those milestone records remain the narrow proof trail; this document is the current architectural map.
