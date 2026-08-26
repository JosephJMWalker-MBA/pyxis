# Milestone 39A — Visible second-epoch authority inspection

Status: proposed implementation pending executed test evidence.

Decision: D200

## Question

Milestones 38B through 38F progressively proved the second evidence-basis epoch as a usable standalone product path:

- persisted second-epoch launch lineage;
- persisted continuation launch lineage;
- first checkpoint above the second root;
- repeatable cumulative checkpointing;
- explicit in-process handoff from first-checkpoint mode into cumulative mode.

Those boundaries are now structurally strong, but much of the authority remains implicit in typed Python state or appears only in transient checkpoint receipts.

The next product question is therefore not another basis-change epoch. It is whether the researcher can visibly inspect the authority already present without turning the inspection itself into authority.

## Decision D200

Pyxis may expose a read-only second-epoch authority inspection surface only if it preserves a strict distinction between:

1. **immutable launch provenance**; and
2. **current governed state**.

The launch section records where and how the shell was entered. The current section records what session/continuation the shell presently governs.

They are not the same thing.

```text
launch provenance
!= current typed continuation
```

and:

```text
displayed launch path
!= current/latest/head authority
```

## Immutable launch provenance

The panel retains only values already proven before UI launch:

- launch family;
- persisted launch overlay location when the launch actually used one;
- retained first-root SHA-256;
- retained second-root SHA-256;
- launch endpoint SHA-256.

Three product launch families are represented:

```text
persisted 37B launch
persisted 37C/37D continuation launch
in-process 38F typed continuation handoff
```

A persisted launch may display its exact explicit overlay source as **launch location context only**.

An in-process handoff has no persistent launch location and must visibly say so. The panel must not derive one from nested plans or from a path supplied later for checkpointing.

## Current governed state

The current section may advance independently of launch provenance.

It reports:

- current state kind;
- source of the current state transition;
- current endpoint SHA-256;
- current declared continuation edge count when the state is an exact typed continuation.

Examples:

```text
persisted 37B launch
→ explicit one-hop rollover
```

updates the current visible endpoint while launch provenance remains fixed.

Likewise:

```text
persisted 37C/37D launch
→ successful 37D cumulative promotion
```

or:

```text
in-process 38F handoff
→ successful 37D cumulative promotion
```

updates current typed continuation state while retaining the exact original launch-provenance object.

## Additive product adapters

39A leaves the previously earned 38D/38E/38F factories available.

The current CLI opts into additive inspection-aware adapters:

- `InspectableSecondBasisEpochCumulativeHandoffResearchSessionShell`
- `InspectableSecondBasisEpochContinuationResearchSessionShell`
- `InspectableSecondBasisEpochContinuationHandoffResearchSessionShell`

The inspection widget is:

- `SecondBasisEpochAuthorityInspectionPanel`

The adapters reuse the already-earned mutation/checkpoint behavior and add only read-only presentation.

## Cumulative-promotion invariant

Before a cumulative promotion, the adapter retains the exact launch-provenance object.

After the existing 38E promotion completes, 39A requires:

1. the launch-provenance object is still the same object;
2. first-root SHA-256 still matches;
3. second-root SHA-256 still matches;
4. only the current endpoint, edge count, and transition-source description advance.

If current typed continuation ancestry disagrees with immutable launch provenance, inspection update fails rather than rewriting history.

## Path discipline

A displayed path is location context only.

39A adds no claim that a path is:

- current;
- latest;
- head;
- branch identity;
- durable object identity;
- chronology authority.

The strongest negative test is the 38F handoff case:

1. the shell begins with no persistent launch path;
2. a later cumulative checkpoint requires the researcher to explicitly supply the current 37C/37D overlay path;
3. checkpoint success must not backfill that supplied path into launch provenance.

Thus:

```text
later explicit checkpoint location
!= earlier launch provenance
```

## Hash discipline

The displayed first-root, second-root, and endpoint SHA-256 values are integrity / record-identity anchors already present in verified loaded records.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

## UI authority

The inspection surface has:

- no buttons;
- no inputs;
- no file reads;
- no writes;
- no overlay reload;
- no format detection;
- no discovery;
- no restart-plan authority;
- no checkpoint authority of its own.

It renders from already-proven in-memory objects and controllers only.

## Regression guard from 38F

38F exposed an important CI failure mode: a stale lazy-import monkeypatch missed a newly introduced UI adapter module, causing pytest to launch a real interactive Textual app. Each GitHub-hosted job then sat at 73% until the six-hour hosted-runner maximum cancelled it.

39A updates the CLI lazy-import tests to intercept the current adapter module directly. Future UI routing milestones should treat this as a regression guard: a dependency-boundary test must fail fast rather than accidentally entering interactive UI.

## Non-goals

39A does not add:

- third evidence-basis epoch support;
- arbitrary-depth basis-change schema;
- generic recursive lineage;
- persistence formats;
- new checkpoint APIs;
- automatic path reuse;
- discovery or latest/current/head selection.

## Acceptance statement

If the executed test suite succeeds, 39A permits only this statement:

> A researcher can visibly distinguish immutable second-epoch launch provenance from the current governed state. Persisted launch locations are shown only as non-authoritative location context, in-process handoffs carry no launch path, and cumulative promotion advances only the current-state view without rewriting launch provenance.
