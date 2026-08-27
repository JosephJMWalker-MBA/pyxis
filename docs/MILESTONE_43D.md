# Milestone 43D — bounded cumulative rollover-mount kernel

Decision: **D216**

## Purpose

Milestone 43D extracts only the post-rollover Textual mechanics that were independently proven by the root-backed, second-evidence-basis, and third-evidence-basis cumulative continuation families.

This is a UI refactor milestone. It does not create new persistence authority, new ancestry semantics, or a generic epoch model.

## Prior-art basis

The extraction is grounded in three concrete product milestones that already shipped and survived their own tests:

- 36C / D188 — root-backed cumulative checkpoint shell;
- 38E / D198 — second-basis-epoch cumulative checkpoint shell;
- 41D / D209 — third-basis-epoch cumulative checkpoint shell.

Each family independently established the same transition after the base research shell had already mounted the explicit one-hop rollover.

## Extracted procedure

The private UI helper begins only after the concrete subclass has called:

```python
await super()._mount_research_rollover(result)
```

It then performs only these shared mechanics:

1. require `shell.last_research_rollover is rollover`;
2. remove a stale concrete cumulative-checkpoint success receipt if one exists;
3. reject ordinary `ResearchSessionRestartPlanControls` on the cumulative shell;
4. remove the unlocked endpoint-revision controls;
5. remove the empty rollover controls;
6. mount endpoint-revision controls with `restart_checkpoint_required=True`;
7. mount fresh empty rollover controls;
8. mount the concrete cumulative checkpoint controls built from the exact current typed re-entry and exact rollover.

The private module is:

```text
src/pyxis/ui/chromium_research_cumulative_checkpoint_rollover_textual.py
```

Its `__all__` is deliberately empty.

## Concrete authority remains concrete

### Root-backed family

The root-backed shell still owns:

- `ChromiumResearchRootBackedSessionContinuationReentryResult`;
- the exact current re-entry field;
- the 35E persistence call;
- explicit current-overlay/successor/declaration/next-overlay paths;
- exact current-reentry and rollover checks;
- the fixed 35C anchor;
- terminal edge SHA-256 and revised-note text checks;
- retained root identity;
- concrete success wording and selectors.

### Second evidence-basis epoch

The second-epoch shell still owns:

- `ChromiumResearchSecondBasisEpochContinuationReentryResult`;
- immutable persisted launch lineage and mutable current typed continuation;
- the 37D persistence call;
- the fixed 37B direct anchor;
- terminal edge SHA-256 and revised-note text checks;
- second-epoch anchor presentation/endpoint;
- retained first- and second-root identities;
- concrete success wording and selectors.

### Third evidence-basis epoch

The third-epoch shell still owns:

- `ChromiumResearchThirdBasisEpochContinuationReentryResult`;
- immutable persisted launch lineage or the separately established typed handoff state;
- the 40D persistence call;
- the fixed 40B direct anchor;
- terminal edge SHA-256 and revised-note text checks;
- third-epoch anchor presentation/endpoint;
- retained three-root ancestry;
- concrete success wording and selectors.

## Why the base rollover call stays concrete

43D does **not** move the call to `super()._mount_research_rollover(result)` into the private helper.

That call is the point where the ordinary research shell creates and retains the visible one-hop continuation. The cumulative subclass remains responsible for invoking that established behavior explicitly. The private 43D procedure only reshapes the already-mounted one-hop surface into the checkpoint-gated cumulative surface.

This keeps the authority chain visible:

```text
EXPLICIT ENDPOINT REVISION
        ↓
BASE 30A ROLLOVER
one-hop continuation is mounted and retained
        ↓
43D PRIVATE SURFACE PROCEDURE
verify exact retained rollover
remove stale prior-cycle receipt
forbid ordinary restart-plan controls
lock revision pending cumulative checkpoint
mount concrete cumulative checkpoint form
        ↓
CONCRETE 35E / 37D / 40D SAVE + PROOF
        ↓
43C PRIVATE POST-PROOF PROMOTION
```

## Relation to the bounded extraction stack

The cumulative path now has four deliberately narrow shared procedures:

```text
43A / D213
application-layer fixed-anchor cumulative extension mechanics

43B / D214
Textual cumulative checkpoint form composition + old-form locking

43C / D215
post-proof visible cumulative promotion

43D / D216
post-base-rollover checkpoint-gating surface transition
```

The shared units are procedural only. The concrete families still surround them with the authority semantics that were independently earned.

## Why save orchestration remains concrete

A larger apparent repetition remains in the cumulative save methods:

```text
read four explicit paths
validate blanks
invoke concrete persistence
catch concrete failure
run concrete shell/result proof
lock old controls
invoke 43C promotion
```

43D does not extract that sequence.

The middle of that sequence crosses the authority boundary: the persistence function and proof predicate are different for 35E, 37D, and 40D. Until further evidence shows that an orchestration kernel can remain mechanically useful without obscuring those proof responsibilities, the save handlers remain concrete.

## Validation contract

Focused 43D coverage proves:

- the private helper enforces exact retained-rollover object identity;
- stale prior-cycle success receipt is removed before the new form is mounted;
- ordinary restart-plan controls are rejected before the old revision/rollover controls are replaced;
- the newly mounted endpoint revision is checkpoint-locked;
- a fresh empty rollover control is mounted;
- the concrete checkpoint-controls factory receives the exact current typed re-entry and exact rollover;
- all three cumulative shell methods call the base rollover first and the 43D helper second;
- all three concrete specs retain their prior selectors and error wording;
- the private module exports no public authority surface.

The mature 36C, 38E, and 41D mounted UI suites remain the stronger behavioral regression authority for complete cumulative cycles.

## Explicit non-authorities

43D adds no claim of:

- latest/current/head;
- chronology or branch authority;
- path identity;
- authorship, authenticity, or trusted time;
- semantic support or citation authority;
- arbitrary-depth ancestry;
- generic `epoch[n]` semantics.

SHA-256 remains integrity/record identity only.

## Acceptance statement

After 43D, root-backed, second-epoch, and third-epoch cumulative shells may share one private post-base-rollover Textual procedure without sharing their persistence, ancestry, lineage, or checkpoint-proof authority.
