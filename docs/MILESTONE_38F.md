# Milestone 38F — Explicit in-process handoff into cumulative second-epoch mode

Status: proposed implementation pending executed test evidence.

Decision: D199

## Question

Milestones 38D / D197 and 38E / D198 deliberately left one gap between them.

38D can proof-gate the first ordinary continuation above a persisted second evidence-basis epoch and write a 37C overlay. 38E can launch from a proven persisted 37C/37D configuration and perform repeatable cumulative checkpoints.

The missing question is whether the researcher can continue immediately after the first 37C checkpoint without pretending that checkpoint success itself changes modes or that the newly written overlay path has silently become current authority.

## Decision D199

Pyxis may cross that gap only through an explicit in-process typed handoff.

After one successful first 37C checkpoint, the first-checkpoint shell remains revision-locked and exposes an explicit `Continue in cumulative mode` action. The action returns the exact `checkpoint.fresh_reentry` already earned by the proof-gated application boundary.

The receiving cumulative shell has a separate raw-typed handoff constructor. It accepts that exact `ChromiumResearchSecondBasisEpochContinuationReentryResult` without inventing a 38B path/re-entry wrapper and without reopening the persisted overlay.

Therefore:

```text
successful checkpoint
!= automatic mode transition
```

and:

```text
fresh typed in-process continuation
!= persistent current-path authority
```

## Two distinct cumulative entry families

Persisted launch retains the existing 38B path proof:

```text
explicit 37C/37D overlay path
→ strict configuration decode
→ fresh continuation re-entry
→ 38B explicit path/result lineage proof
→ persisted-launch cumulative shell
```

Immediate handoff is deliberately different:

```text
successful 37C checkpoint
→ exact checkpoint.fresh_reentry
→ explicit human handoff action
→ raw-typed cumulative handoff shell
```

The second route performs no continuation-overlay reload and no new 38B path proof because no path is being asserted as authority. The exact typed result already exists in memory as the output of the successful 37C proof boundary.

## Additive UI adapters

38F does not rewrite the previously earned 38D and 38E factories.

It adds:

- `SecondBasisEpochCumulativeHandoffResearchSessionShell`
  - extends the 38D first-checkpoint shell;
  - exposes no handoff before a successful 37C checkpoint;
  - leaves revision locked after success;
  - mounts a visible explanation and explicit handoff button;
  - returns exactly `checkpoint.fresh_reentry` only when that button is chosen.

- `SecondBasisEpochContinuationHandoffResearchSessionShell`
  - reuses the 38E cumulative behavior;
  - initializes directly from one exact typed continuation re-entry;
  - deliberately bypasses the persisted-launch constructor that requires a 38B path wrapper;
  - stores no overlay path;
  - fabricates no launch-lineage wrapper;
  - begins with endpoint revision unlocked and no cumulative checkpoint form.

The old milestone factories remain meaningful snapshots of their original authority boundaries. The public CLI opts into the new 38F adapters.

## CLI transition

The `--second-basis-epoch-overlay` route remains responsible for the ordinary explicit 37B launch and its 38B proof. The launched first-checkpoint shell may now return either:

- `None` for ordinary close; or
- one exact `ChromiumResearchSecondBasisEpochContinuationReentryResult` after the researcher explicitly chooses the handoff.

Only the typed second result launches the raw-handoff cumulative shell.

No continuation overlay path is passed between the two shells.

The separate public route:

```text
--second-basis-epoch-continuation-overlay <path>
```

remains unchanged in authority: it still freshly reconstructs the explicit persisted continuation and proves the 38B path/result pairing before launching cumulative mode.

## Next cumulative checkpoint

The handoff does not imply knowledge of the newly saved overlay's current location.

Immediately after handoff:

- current typed continuation = exact handed-off re-entry;
- persistent launch lineage = absent;
- current overlay path = absent;
- ordinary restart lineage = absent;
- revision = unlocked;
- cumulative checkpoint controls = absent.

Only after the next explicit revision and rollover does the 38E cumulative checkpoint form appear. Its four location fields are blank:

1. current 37C/37D overlay path;
2. chosen successor edge path;
3. cumulative declaration destination;
4. next continuation overlay destination.

The researcher must supply the current persisted location explicitly if they want to checkpoint that next state.

## Failure and close behavior

A failed first 37C checkpoint never exposes the handoff action.

A successful checkpoint followed by normal shell close does not launch cumulative mode. The persisted 37C overlay remains available for an explicit later relaunch through the normal path-proofed CLI route.

Thus immediate typed handoff and later persisted relaunch are parallel explicit choices, not hidden promotion rules.

## Authority deliberately not added

38F adds no claim about:

- latest/current/head state;
- branch or chronology authority;
- path identity;
- discovery or format guessing;
- authorship or authenticity;
- trusted time;
- semantic support;
- citation authority;
- third basis-change epochs;
- arbitrary-depth basis-change schemas.

No persistence format or application checkpoint API changes.

## Acceptance statement

If the executed test suite succeeds, 38F permits only this statement:

> After one freshly proven 37C checkpoint, a researcher may explicitly hand the exact in-memory continuation into cumulative 37D mode. The transition is user-chosen, performs no disk re-entry, carries no persistent path as current authority, and leaves explicit close/relaunch as an equally valid alternative.
