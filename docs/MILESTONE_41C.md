# Milestone 41C — First Textual 40C checkpoint from proven third-epoch launch lineage

## Decision D208

A 40B-backed third-epoch Textual shell may checkpoint exactly one explicitly chosen ordinary continuation through the existing 40C application boundary only after the live shell reaches that continuation through the established endpoint-revision and 30A rollover flow.

The retained 41A launch overlay path is not automatically reused as checkpoint location authority.

## Starting authority

41B provides:

```text
ChromiumResearchThirdBasisEpochShellLineage
  overlay_source
  reentry
```

where `reentry` is the fresh three-root result reconstructed from `overlay_source` during explicit 41A proof.

The dedicated shell retains that exact wrapper while its base `ResearchSessionShell` operates on:

```text
lineage.reentry.controller
```

with no ordinary 31A `research_reentry`.

## First continuation flow

41C permits:

```text
proven 40B launch lineage
→ explicit endpoint revision
→ explicit 30A one-hop rollover
→ visible one-hop continuation
→ revision lock
→ explicit 40C checkpoint form
```

The base shell still performs revision and rollover. The third-epoch subclass only changes what is authorized after the rollover has been explicitly chosen.

## Checkpoint inputs are blank

The 40C checkpoint form requires four explicit current locations:

```text
current 40B overlay path
chosen successor edge path
one-hop continuation declaration path
no-overwrite 40C overlay destination
```

Every field starts blank.

41C deliberately does **not** prefill:

- `third_basis_epoch_launch_lineage.overlay_source`;
- the successor path entered during endpoint revision/rollover;
- the continuation declaration destination entered during rollover.

Those values were sufficient for their earlier operations. They are not silently promoted into durable checkpoint authority.

## Application boundary

Saving delegates only to:

```text
persist_chromium_research_third_basis_epoch_continuation_checkpoint(...)
```

with:

```text
prior_reentry = third_basis_epoch_launch_lineage.reentry
rollover = last_research_rollover
```

and the four newly entered explicit locations.

The application boundary already freshly decodes and reconstructs the supplied 40B overlay before writing anything. It proves the retained first-, second-, and third-root identities, the retained post-second-root continuation state, the third-epoch governed presentation and endpoint, the chosen rollover prior relationship, and the chosen continuation presentation and endpoint.

Therefore 41C adds no new persistence algorithm and the UI does not duplicate evidence-verification logic.

## Path remains location, not identity

The explicit checkpoint-time 40B path may differ from the path retained by the 41A launch wrapper.

A path-distinct configuration is admissible only if the existing 40C application proof freshly reconstructs the same durable three-root authority and governed third-epoch state.

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

After a successful 40C checkpoint:

- the exact prior 41A launch-lineage re-entry remains retained;
- the exact rollover remains retained by the checkpoint result;
- the visible one-hop controller remains mounted;
- the checkpoint form is locked;
- endpoint revision remains locked;
- the 41A launch wrapper is not rewritten;
- no cumulative-mode handoff occurs.

The shell instructs explicit relaunch through:

```text
pyxis research-shell --third-basis-epoch-continuation-overlay <saved-overlay>
```

for further work.

This is intentionally analogous to 38D's first second-epoch checkpoint boundary.

## Failure semantics

Any missing path, mismatched successor/declaration, tampered retained root, or no-overwrite failure leaves:

- the chosen one-hop continuation visible;
- endpoint revision locked;
- the retained 41A launch lineage unchanged;
- no 40C checkpoint result promoted into shell state.

## UI scope

Only `ThirdBasisEpochResearchSessionShell` gains 41C checkpoint behavior.

`ThirdBasisEpochContinuationResearchSessionShell` remains the 41B lineage-retaining controller shell in this milestone. Repeatable cumulative 40D checkpointing from that shell is a separate future boundary.

Ordinary `ResearchSessionRestartPlanControls` remain absent throughout.

## Preserved non-authorities

41C introduces no:

- new persistence format;
- new application checkpoint API;
- path discovery or prefilling authority;
- automatic mode switch;
- format autodetection;
- directory scan or predecessor search;
- latest/current/head state;
- chronology or branch semantics;
- three-root inspection surface;
- fourth evidence-basis epoch;
- generic `epoch[n]` lineage;
- semantic-support judgment;
- authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

41C establishes only this claim:

> A researcher launched from one proven 40B third-epoch lineage can explicitly choose one ordinary continuation and checkpoint it through the existing 40C proof boundary from Textual. The shell requires fresh explicit durable locations, freshly preserves all three retained evidence-basis roots, keeps revision locked until and after checkpoint success, and does not convert launch context into implicit current-path or cumulative-mode authority.

## Next seam

The next safe product boundary can add repeatable cumulative 40D checkpointing in `ThirdBasisEpochContinuationResearchSessionShell`, including visible promotion from the one-hop rollover presentation to the freshly proven cumulative controller before another revision is unlocked.
