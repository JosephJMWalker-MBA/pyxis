# Milestone 46G — explicit second-basis epoch typed handoff

Decision: D234

## Product boundary

46F established a durable 37B locator overlay for the exact historical second-basis
epoch freshly proven by 46E. It deliberately did not replace the currently mounted
root-backed continuation product.

46G adds one explicit in-process product seam:

```text
exact successful 46F persistence
+ explicit human handoff action
→ exact 46F checkpoint.fresh_reentry
→ established second-basis-epoch first-checkpoint product
```

The handoff is not automatic promotion and does not derive authority from the path of
the just-written 37B overlay.

## Authority distinction

```text
successful 46F persistence
!= mode promotion

persisted 37B overlay location
!= in-process 46G launch provenance

exact typed 46G handoff
!= fabricated persisted shell lineage

46G launch
!= current/latest/head selection
```

The old product remains mounted after 46F. Only the explicit 46G action exits it with
the exact already-earned typed result.

## Prior art and reuse

The implementation reuses existing Pyxis boundaries rather than creating another
restart or continuation mechanism.

- 44H / D225 established the first-root precedent: overlay persistence and in-process
  mode handoff are separate acts; the handoff transfers the exact checkpoint fresh
  re-entry and never reloads the saved overlay path.
- 38F already established a pathless typed receiver for second-epoch continuation
  mode. It sets persisted launch lineage to `None` rather than fabricating provenance.
- `SecondBasisEpochResearchSessionShell` already owns the 37C first-continuation
  checkpoint boundary.
- `ChromiumResearchSecondBasisEpochShellLineage` remains reserved for an explicit
  persisted 37B path that has been freshly proven against earned second-epoch state.
- second-epoch authority inspection already separates immutable launch provenance from
  mutable current governed state.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Narrow compatibility refactor

Before 46G, the persisted initial second-epoch shell read its active typed prior only
through:

```python
self.second_basis_epoch_launch_lineage.reentry
```

That made a pathless receiver impossible without inventing a fake persisted lineage.
46G separates the two concepts:

```python
self.second_basis_epoch_launch_lineage = lineage
self.second_basis_epoch_reentry = lineage.reentry
```

37C now consumes `self.second_basis_epoch_reentry`.

For ordinary persisted 37B launches, both fields still identify the same freshly
proved launch authority. The change is intentionally behavior-neutral there.

## Pathless initial receiver

`SecondBasisEpochHandoffResearchSessionShell` accepts exactly one
`ChromiumResearchSecondBasisEpochReentryResult` and deliberately bypasses persisted
launch construction.

It begins with:

```text
second_basis_epoch_launch_lineage = None
second_basis_epoch_handoff_reentry = exact handoff
second_basis_epoch_reentry = exact handoff
last_second_basis_epoch_continuation_checkpoint = None
```

It mounts the exact handoff controller and has no ordinary research re-entry lineage.
No 37B overlay source is stored or inferred.

The receiver inherits the established first-checkpoint product. After one explicit
rollover, the normal 37C form appears and every durable locator is blank. The caller
must explicitly supply the current 37B overlay path, successor edge path, continuation
declaration path, and no-overwrite 37C destination. Public 37C remains authoritative
for the write and fresh proof.

## 46G product action

`SecondChangedBasisEpochHandoffResearchSessionShell` extends the 46F surface.

No handoff control exists before successful 46F persistence. A failed 46F write leaves
the handoff absent and retryable.

After one new exact success, 46G mounts one explicit action. Persistence alone still
leaves the old product mounted. When the user chooses the action, the shell exits with:

```python
last_second_changed_basis_epoch_reentry_overlay.checkpoint.fresh_reentry
```

That exact object is transferred. It is not the earlier 46E fresh re-entry and it is
not a reconstruction loaded from the saved 37B overlay.

The just-written overlay may disappear after successful 46F and before the button is
pressed; the already-earned typed handoff remains the in-process authority subject.

## Runner

`run_second_changed_basis_epoch_handoff_research_session_shell` chains only an explicit
46G result into the pathless inspectable second-epoch receiver.

Normal close returns `None` and launches no receiver.

The runner carries no path and performs no restart reconstruction.

## Read-only authority inspection

46G adds a concrete initial-session projection rather than widening the existing 38F
continuation-handoff projection.

The 46G launch inspection records:

```text
launch family: in-process 46G typed second-basis-epoch handoff
launch location context: none
first root: exact retained first-root SHA-256
second root: exact second-root SHA-256
launch endpoint: exact handed-off endpoint SHA-256
```

These hashes remain integrity / record-identity anchors only. They do not establish
trusted time, authenticity, chronology, semantic support, or citation authority.

After a later rollover, the exact launch-provenance object is retained and only current
governed state advances.

## Compatibility

46G does not change:

- public 37A or 37B reconstruction/persistence;
- any persistence format;
- persisted 37B shell-lineage proof;
- persisted 37B inspection semantics;
- existing 38F continuation handoff behavior;
- 37C or 37D persistence rules;
- CLI flags or locator interpretation;
- root-backed launch provenance;
- browser behavior.

## Focused acceptance coverage

The 46G tests demonstrate:

1. persisted 37B launch lineage remains exact after the narrow active-reentry split;
2. a raw initial receiver retains the exact typed handoff with no launch lineage/path;
3. raw rollover exposes the existing 37C form with every durable locator blank;
4. 46G inspection is pathless and preserves exact immutable launch provenance across
   rollover;
5. 46G controls are absent before successful 46F persistence;
6. successful 46F persistence does not automatically exit or change mounted state;
7. the explicit button returns the exact 37B checkpoint fresh re-entry rather than the
   earlier 46E result or a reloaded reconstruction;
8. failed/no-overwrite 46F persistence never exposes the handoff;
9. normal runner close launches nothing, while an explicit handoff is passed object-
   identically to the pathless inspectable receiver.

## Non-goals

46G does not add a 37B disk relaunch inside the handoff, automatic mode promotion,
automatic 37C persistence, a new CLI flag, a new persistence format, locator discovery
or prefill, launch-path backfill, global current/latest/head selection, generic Nth-
epoch abstractions, a third/fourth basis product bridge, browser reacquisition,
semantic-support authority, citation authority, or autonomous research.

## Next question

After 46G is demonstrated, the next frontier should be reviewed from the established
second-epoch first-checkpoint product rather than assumed from numerical symmetry.
Existing 37C, 38F, and 37D machinery already covers substantial continuation behavior,
so any next milestone must identify a concrete missing product seam before adding code.
