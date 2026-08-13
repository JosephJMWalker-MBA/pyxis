# Pyxis Current State

**Continuity front door — Repository Zero current through Milestone 11T / D115 (2026-08-13).**

This file exists because the GitHub connector cannot safely apply line-level edits to the already-large `ARCHITECTURE.md` and `DEVELOPMENT_ARCHIVE.md`. A prior attempt to replace those files wholesale produced a deletion-heavy diff and was deliberately abandoned rather than normalize a historical rewrite.

Nothing here supersedes proven historical evidence. It provides one current map over the preserved central documents and the later milestone records.

## Read order

For a new development session, read in this order:

1. `README.md`
2. this file (`docs/CURRENT_STATE.md`)
3. `docs/ARCHITECTURE.md`
4. `docs/DECISIONS.md`
5. `docs/DEVELOPMENT_ARCHIVE.md`
6. `docs/MILESTONE_11K_CONTINUITY.md` and `docs/MILESTONE_11L.md` through `docs/MILESTONE_11T.md`

The large central documents remain intact historical/current foundations. Their status headers lag later implementation because the connector could not safely patch them in place. This file makes those later deltas explicit in one place rather than requiring a future session to rediscover the gap.

## Current Repository Zero checkpoint

Repository Zero has four proven families:

```text
compiler / runtime / revision / export lifecycle
            +
interactive evidence UI
            +
descriptive measurement pipeline
            +
live measurement provenance / invalidation / re-entry
```

The permanent authority chain remains:

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

The first local Textual Workspace UI is complete for Repository Zero: it renders current evidence, reruns the materialized Workspace, previews the controlled `remove_normalize_text` architecture edit, requires rationale for Apply, retires stale READY after architecture change, and restores READY only through verified export refresh. One `WorkspaceController` remains the live transient-state authority.

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
- The demonstrator-specific architecture operation should remain concrete until a second genuine edit creates pressure for a general abstraction.

## Current development discipline

Do **not** continue the 11-series by adding another statistic merely because one is available. The existing descriptive set is sufficient to prove the measurement architecture and its provenance path.

The next implementation milestone should answer a concrete Pyxis product question. Possible future pressures already visible in the project include a second genuine architecture operation, broader journey measurement, browser/research integration, persistence, or release/support hardening. None is selected by this continuity file.

The package currently declares Python `>=3.11` while ordinary CI proves Python 3.11. That is not a Repository Zero blocker, but future release hardening should either prove additional supported interpreter lanes or narrow the declared support contract.

## Why the older central status lines are not being rewritten now

`MILESTONE_11K_CONTINUITY.md` already records that the connector rejected the large replacements required to fold 11K into the central documents. The same limitation remains. Whole-file replacement of the central architecture/archive was tested again during 11T continuity work, and the resulting diff would have removed large amounts of historical reasoning from their canonical paths. That approach was abandoned.

Until a safe line-patch workflow is available, `CURRENT_STATE.md` is the single current overlay. It is intentionally small, explicit, and reversible. The preserved large documents plus milestone proofs remain the detailed evidence base.
