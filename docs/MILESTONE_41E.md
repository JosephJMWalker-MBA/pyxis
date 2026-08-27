# Milestone 41E — Explicit in-process handoff into cumulative third-epoch mode

Status: proposed implementation pending executed test evidence.

Decision: D210

## Question

Milestones 41C / D208 and 41D / D209 deliberately leave one gap between them.

41C can proof-gate the first ordinary continuation above a persisted third evidence-basis epoch and write a 40C overlay. 41D can launch from a proven persisted 40C/40D continuation and perform repeatable cumulative checkpoints.

The missing question is whether the researcher can continue immediately after the first successful 40C checkpoint without pretending that checkpoint success itself changes modes or that the newly written overlay path has silently become current authority.

## Decision D210

Pyxis may cross that gap only through an explicit in-process typed handoff.

After one successful first 40C checkpoint, the first-checkpoint shell remains revision-locked and exposes an explicit `Continue in cumulative mode` action. The action returns the exact `checkpoint.fresh_reentry` already earned by the proof-gated 40C application boundary.

The receiving cumulative shell has a separate raw-typed handoff constructor. It accepts that exact `ChromiumResearchThirdBasisEpochContinuationReentryResult` without inventing a 41A path/re-entry wrapper and without reopening the persisted overlay.

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

Persisted launch retains the existing 41A path proof:

```text
explicit 40C/40D overlay path
→ strict configuration decode
→ fresh continuation re-entry
→ 41A explicit path/result lineage proof
→ persisted-launch cumulative shell
```

Immediate handoff is deliberately different:

```text
successful 40C checkpoint
→ exact checkpoint.fresh_reentry
→ explicit human handoff action
→ raw-typed cumulative handoff shell
```

The second route performs no continuation-overlay reload and no new 41A continuation path proof because no path is being asserted as authority. The exact typed result already exists in memory as the output of the successful 40C proof boundary.

## Additive UI adapters

41E does not rewrite the previously earned 41C and 41D factories.

It adds:

- `ThirdBasisEpochCumulativeHandoffResearchSessionShell`
  - extends the 41C first-checkpoint shell;
  - exposes no handoff before a successful 40C checkpoint;
  - leaves revision locked after success;
  - mounts a visible explanation and explicit handoff button;
  - returns exactly `checkpoint.fresh_reentry` only when that button is chosen.

- `ThirdBasisEpochContinuationHandoffResearchSessionShell`
  - reuses the 41D cumulative behavior;
  - initializes directly from one exact typed continuation re-entry;
  - deliberately bypasses the persisted-launch constructor that requires a 41A path wrapper;
  - stores no overlay path;
  - fabricates no launch-lineage wrapper;
  - begins with endpoint revision unlocked and no cumulative checkpoint form.

The old milestone factories remain meaningful snapshots of their original authority boundaries. The public CLI opts into the new 41E adapters only for the 40B first-checkpoint route and the explicit in-process transition it may return.

## CLI transition

The `--third-basis-epoch-overlay` route remains responsible for ordinary explicit 40B launch and its 41A proof. The launched first-checkpoint shell may now return either:

- `None` for ordinary close; or
- one exact `ChromiumResearchThirdBasisEpochContinuationReentryResult` after the researcher explicitly chooses the handoff.

Only the typed second result launches the raw-handoff cumulative shell.

No continuation overlay path is passed between the two shells.

The separate public route:

```text
--third-basis-epoch-continuation-overlay <path>
```

remains unchanged in authority: it still freshly reconstructs the explicit persisted continuation and proves the 41A path/result pairing before launching cumulative mode.

## Next cumulative checkpoint

The handoff does not imply knowledge of the newly saved overlay's current location.

Immediately after handoff:

- current typed continuation = exact handed-off re-entry;
- persistent launch lineage = absent;
- current overlay path = absent;
- ordinary restart lineage = absent;
- revision = unlocked;
- cumulative checkpoint controls = absent.

Only after the next explicit revision and rollover does the 41D cumulative checkpoint form appear. Its four location fields are blank:

1. current 40C/40D overlay path;
2. chosen successor edge path;
3. cumulative declaration destination;
4. next continuation overlay destination.

The researcher must supply the current persisted location explicitly if they want to checkpoint that next state.

## Failure and close behavior

A failed first 40C checkpoint never exposes the handoff action.

A successful checkpoint followed by normal shell close does not launch cumulative mode. The persisted 40C overlay remains available for an explicit later relaunch through the normal path-proofed CLI route.

Thus immediate typed handoff and later persisted relaunch are parallel explicit choices, not hidden promotion rules.

## Test obligations

41E tests require:

- no handoff control before successful 40C proof;
- failed 40C checkpoint never exposes handoff;
- successful checkpoint remains revision-locked while exposing the explicit action;
- the action returns the exact `checkpoint.fresh_reentry` object;
- raw typed handoff mode fabricates no launch-lineage wrapper and stores no overlay path;
- the first post-handoff cumulative form appears only after a new revision and rollover;
- all four operation paths are blank at that point;
- normal close does not trigger a mode transition;
- CLI chains only an explicit correctly typed handoff;
- in-process handoff performs no continuation-overlay reload and no continuation path proof;
- persisted continuation CLI launch remains in the 41A path-proofed family.

## Authority deliberately not added

41E adds no claim about:

- latest/current/head state;
- branch or chronology authority;
- path identity;
- discovery or format guessing;
- authorship or authenticity;
- trusted time;
- semantic support;
- citation authority;
- fourth evidence-basis epoch support;
- generic or arbitrary-depth basis-change schemas.

No persistence format or application checkpoint API changes.

## Acceptance statement

If the executed test suite succeeds, 41E permits only this statement:

> After one freshly proven 40C checkpoint, a researcher may explicitly hand the exact in-memory third-epoch continuation into cumulative 40D mode. The transition is user-chosen, performs no disk re-entry, carries no persistent path as current authority, and leaves explicit close/relaunch as an equally valid alternative.

## Next seam

With third-epoch launch, first checkpoint, cumulative checkpointing, and explicit handoff aligned, the next product-facing seam may be read-only three-root authority inspection parity. That should expose already-earned launch provenance and current governed state without creating new authority or extending to a fourth epoch.
