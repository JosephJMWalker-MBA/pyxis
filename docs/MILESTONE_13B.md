# Milestone 13B — Observed Architecture Consequence Reconciliation

**Decision D119 — 2026-08-14**

## Product question

Milestone 13A made one proposed architecture consequence chain inspectable before mutation. Milestone 13B asks the separate post-Apply question:

> Can Pyxis reconcile that earlier proposed trace with the revision, compiler-generation, RIR, and runtime evidence actually produced by Apply without rewriting proposed evidence into observed truth?

## Decision

A retained architecture preview may be paired after successful Apply with a **separate immutable observed-evidence record** derived only from evidence already produced by the governed Apply path.

The earlier `ArchitecturePreviewPresentation` remains unchanged as proposed evidence. It is never amended, promoted, or relabeled as post-change authority.

The reconciliation may compute only narrow structural comparisons between the proposed and observed records. A difference is surfaced as a difference; it is not repaired, scored, explained away, or coerced into a successful prediction.

## Observed evidence source

13B does not rediscover post-Apply state. The observed record is assembled only from evidence already owned by the successful Apply result and its fresh `WorkspacePresentation`:

```text
successful governed Apply
    ↓
append-only RevisionEvent + RevisionCompletion
    ↓
post-Apply BuildResult
    ├── current RIR
    ├── generation manifest
    └── generation statuses
    ↓
post-Apply runtime result
    ↓
fresh WorkspacePresentation
```

The reconciliation performs no filesystem read, compilation, materialization, runtime execution, persistence, export, or measurement acquisition of its own.

## Reconciliation boundaries

The current proof compares only exact structural facts:

```text
proposed current/proposed canonical identities
    ↕
observed revision before/after canonical identities

proposed canonical identity
    ↕
observed post-Apply canonical identity

proposed RIR capabilities
    ↕
observed post-Apply RIR capabilities

predicted compiler-product action
    ↕
observed compiler generation status

proposed runtime keys
    ↕
observed runtime-result keys

revision-completion RIR identity
    ↕
observed post-Apply RIR identity
```

For compiler-product consequences the mapping is deliberately mechanical:

```text
proposed add     → expected observed status: new
proposed change  → expected observed status: regenerated
proposed remove  → expected observed status: removed
```

Unchanged compiler products remain present in the observed generation record, but they are not retroactively added to the earlier proposed consequence trace.

## Presentation boundary

The Textual shell preserves the epistemic transition visibly:

```text
before Apply
    PROPOSED CONSEQUENCE TRACE — NOT APPLIED

successful Apply
    proposed trace surface clears
    ↓
    POST-APPLY RECONCILIATION — OBSERVED EVIDENCE
```

The observed panel explicitly states that the earlier preview remains separate proposed evidence. It renders `MATCH` or `DIFFERS` only for the exact structural equalities owned by the reconciliation object.

No summary score, confidence value, causal interpretation, generated explanation, quality judgment, or architecture recommendation is introduced.

## Controller lifetime

`WorkspaceController` retains at most one latest successful architecture reconciliation.

- successful Apply installs the reconciliation produced by that Apply;
- failed Apply does not advance it;
- a later successful architecture Preview clears the prior reconciliation before presenting a different proposal;
- ordinary runtime rerun and export refresh do not reinterpret the reconciliation.

This prevents a completed comparison from being mistaken for evidence about a later pending architecture edit.

## Mismatch behavior

A dedicated application test alters only a test copy of observed artifact-presentation evidence after a genuine Apply. The proposed `split_lines` artifact action remains `add`, the mechanically expected status remains `new`, the altered observed status is `reused`, and reconciliation reports `matches=False`.

The preview object remains unchanged.

This proves the boundary can represent disagreement rather than merely confirm the happy path.

## Visible proof

The first visible reconciliation proof remains intentionally concrete: addition of `split_lines`.

After Apply, the UI shows observed evidence that:

- the revision operation is `add_capability:split_lines`;
- the revision canonical transition matches the earlier preview transition;
- post-Apply canonical identity matches the proposed canonical identity;
- post-Apply RIR capabilities match the proposed capabilities;
- `generated/capabilities/split_lines.py` was predicted as added and observed as `new`;
- `generated/workspaces/text_lab/main.py` was predicted as changed and observed as `regenerated`;
- observed runtime keys match the proposed runtime keys;
- revision completion RIR identity matches the observed RIR identity.

Application coverage also proves the subtractive `normalize_text` path observes its capability artifact as `removed` and its post-Apply runtime key set without `normalize_text`.

## Validation

- Actions #403 passed the corrected application reconciliation head `dc479d7393bfab9a6f00b2bd38358bc674352900` with all **213** Repository Zero tests.
- Actions #406 passed the visible reconciliation head `e94df90a10220619deb9128ce46958a7a08caf79` with all **214** Repository Zero tests.

## Deliberate non-goals

13B introduces no:

- new architecture operation;
- generic operation registry or command schema;
- compiler behavior;
- RIR schema change;
- canonical persistence behavior;
- revision mutation semantics;
- runtime behavior;
- filesystem rediscovery;
- export or READY behavior;
- measurement behavior;
- prediction score or confidence;
- causal claim;
- AI explanation or generated narrative;
- automatic correction when proposed and observed evidence differ.

## Result

D119 establishes the next evidence rule for Pyxis architecture inspectability:

> **Proposed architecture evidence and observed post-Apply evidence may be reconciled, but they remain distinct evidence objects. Reconciliation may expose exact structural matches or differences; it must not rewrite proposal into observation or turn agreement into a score, explanation, or causal claim.**
