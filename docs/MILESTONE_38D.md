# Milestone 38D — First Textual 37C checkpoint from proven second-epoch launch lineage

## Decision D197

A 37B-backed second-epoch Textual shell may checkpoint exactly one explicitly chosen ordinary continuation through the existing 37C application boundary only after the live shell reaches that continuation through the established endpoint-revision and 30A rollover flow.

The retained 38B launch overlay path is not automatically reused as checkpoint location authority.

## Starting authority

38C provides:

```text
ChromiumResearchSecondBasisEpochShellLineage
  overlay_source
  reentry
```

where `reentry` is the fresh second-epoch result reconstructed from `overlay_source` during explicit 38B proof.

The dedicated shell retains that exact wrapper while its base `ResearchSessionShell` operates on:

```text
lineage.reentry.controller
```

with no ordinary 31A `research_reentry`.

## First continuation flow

38D permits:

```text
proven 37B launch lineage
→ explicit endpoint revision
→ explicit 30A one-hop rollover
→ visible one-hop continuation
→ revision lock
→ explicit 37C checkpoint form
```

The base shell still performs revision and rollover. The second-epoch subclass only changes what is authorized after the rollover has been chosen.

## Checkpoint inputs are blank

The 37C checkpoint form requires four explicit current locations:

```text
current 37B overlay path
chosen successor edge path
one-hop continuation declaration path
no-overwrite 37C overlay destination
```

Every field starts blank.

38D deliberately does **not** prefill:

- `second_basis_epoch_launch_lineage.overlay_source`;
- the successor path entered during endpoint revision/rollover;
- the continuation declaration destination entered during rollover.

Those values were sufficient for their earlier operations. They are not silently promoted into durable checkpoint authority.

## Application boundary

Saving delegates only to:

```text
persist_chromium_research_second_basis_epoch_continuation_checkpoint(...)
```

with:

```text
prior_reentry = second_basis_epoch_launch_lineage.reentry
rollover = last_research_rollover
```

and the four newly entered explicit locations.

The application boundary freshly decodes and reconstructs the supplied 37B overlay before writing anything. It proves:

- retained prior root-backed continuation presentation and endpoint;
- retained first-root durable identity;
- second-root durable identity;
- second-epoch presentation and endpoint;
- chosen rollover prior relationship;
- chosen continuation presentation and endpoint.

Therefore the UI does not duplicate evidence-verification logic or infer current paths.

## Path remains location, not identity

The explicit checkpoint-time 37B path may differ from the path retained by the 38B launch wrapper.

A path-distinct configuration is admissible only if the existing 37C application proof freshly reconstructs the same durable second-epoch authority.

Thus:

```text
launch path equality is not required
```

but:

```text
fresh durable ancestry/session equivalence is required
```

No moved path is discovered automatically.

## Locked success semantics

After a successful 37C checkpoint:

- the exact prior launch-lineage re-entry remains retained;
- the exact rollover remains retained by the checkpoint result;
- the visible one-hop controller remains mounted;
- the checkpoint form is locked;
- endpoint revision remains locked;
- the 38B launch wrapper is not rewritten;
- no cumulative-mode handoff occurs.

The shell instructs explicit relaunch through:

```text
pyxis research-shell --second-basis-epoch-continuation-overlay <saved-overlay>
```

for further work.

This is intentionally analogous to the original first root-backed checkpoint boundary before explicit in-process handoff was added separately.

## Failure semantics

Any missing path, mismatched successor/declaration, tampered ancestry, or no-overwrite failure leaves:

- the chosen one-hop continuation visible;
- endpoint revision locked;
- the retained 38B launch lineage unchanged;
- no 37C checkpoint result promoted into shell state.

## UI scope

Only `SecondBasisEpochResearchSessionShell` gains 38D checkpoint behavior.

`SecondBasisEpochContinuationResearchSessionShell` remains the 38C lineage-retaining controller shell in this milestone. Repeatable cumulative 37D checkpointing from that shell is a separate next boundary.

Ordinary `ResearchSessionRestartPlanControls` remain absent throughout.

## Preserved non-authorities

38D introduces no:

- new persistence format;
- new application checkpoint API;
- path discovery or prefilling authority;
- automatic mode switch;
- format autodetection;
- directory scan or predecessor search;
- latest/current/head state;
- chronology or branch semantics;
- semantic-support judgment;
- authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

38D establishes only this claim:

> A researcher launched from one proven 37B second-epoch lineage can explicitly choose one ordinary continuation and checkpoint it through the existing 37C proof boundary from Textual. The shell requires fresh explicit durable locations, keeps revision locked until and after checkpoint success, and does not convert launch context into implicit current-path or cumulative-mode authority.

## Next seam

The next safe milestone is repeatable cumulative 37D checkpointing in `SecondBasisEpochContinuationResearchSessionShell`, including visible promotion from the one-hop rollover presentation to the freshly proven cumulative controller before another revision is unlocked.
