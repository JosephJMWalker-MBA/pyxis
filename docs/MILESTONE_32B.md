# Milestone 32B — Standalone Restart-Plan Checkpoint

Decision: D176

## Product question

31B made the governed research workflow directly launchable:

```text
pyxis research-shell --plan <explicit-locator-plan.json>
```

32A then made one explicitly chosen continuation restartable by constructing and
freshly proving a new locator plan before persisting it.

That still left one product gap.

Inside the standalone Textual shell a researcher could:

```text
launch v6
→ write v7
→ explicitly roll over to v7
→ continue authoring from v7
```

but the UI had no way to persist the 32A restart plan for v7.

If the process exited after rollover, the durable v7 edge and declaration existed,
but the launch plan used to start the process still described v6.

32B closes that gap in the standalone product surface.

## Core workflow

For shells launched with an exact 31A re-entry result, the governed loop becomes:

```text
fresh 31A re-entry
→ inspect
→ write one endpoint successor
→ explicit 30A rollover
→ continuation becomes visible
→ endpoint revision temporarily locks
→ explicitly provide current successor path
→ explicitly provide current continuation declaration path
→ explicitly provide new no-overwrite plan destination
→ 32A fresh restart proof + persistence
→ restart lineage advances
→ endpoint revision unlocks
```

The checkpoint is deliberately between rollover and the next revision.

## Why revision pauses after rollover

Without the checkpoint, the live UI could outrun the locator lineage:

```text
launch v6 plan
→ roll over to v7
→ immediately write/roll over to v8
```

At that point the shell would have a live v8 controller while its only retained
fresh-process locator lineage still described v6.

32A cannot legitimately create a v8 restart plan directly from the v6 re-entry
result, because the v8 rollover was chosen from v7.

32B therefore makes restartability an explicit UI state transition:

```text
chosen continuation
!=
restartable continuation
```

and requires the latter before the re-entry-aware standalone shell authorizes the
next successor write.

This is a UI workflow rule only. The underlying 29A and 30A programmatic APIs are
unchanged and still permit lower-level callers to manage their own sequencing.

## Re-entry-aware shell authority

`ResearchSessionShell` continues to accept the existing controller-only form.

32B adds an optional exact:

```text
ChromiumResearchSessionReentryResult
```

When supplied, the shell validates that the re-entry result describes the same
session presentation, declaration identity, and declared endpoint identity as the
supplied controller.

The shell does not derive a locator plan from loaded evidence.

Therefore:

```text
loaded controller
!=
permission to invent restart lineage
```

Only an explicitly supplied 31A result grants the shell the locator lineage needed
for the 32A checkpoint.

## Compatibility

Two standalone modes remain valid.

### Controller-only mode

```text
create_research_session_shell(controller)
```

This retains the pre-32B behavior. No restart-plan control is introduced, because the
caller supplied no locator lineage for Pyxis to advance.

### Re-entry-aware mode

```text
create_research_session_shell(
    reentry.controller,
    reentry=reentry,
)
```

This mode gains the restart checkpoint after every successful rollover.

The public `pyxis research-shell --plan ...` path uses this mode because the CLI
already has the exact 31A result returned by fresh durable reconstruction.

## CLI handoff

Before 32B, the CLI discarded the outer 31A result after re-entry and passed only:

```text
result.controller
```

to the standalone shell.

32B passes the complete:

```text
ChromiumResearchSessionReentryResult
```

through the lazy UI handoff.

The CLI still performs no research-domain reconstruction beyond invoking established
application boundaries.

The Textual dependency remains lazy and optional.

## New restart-plan controls

32B adds:

```text
ResearchSessionRestartPlanControls
```

The control is mounted only after a successful rollover in a re-entry-aware shell.

It displays the chosen successor identity and continuation declaration identity as a
receipt of the already-earned rollover, then requires three explicit path inputs:

1. current durable location of the exact chosen successor edge;
2. current durable location of the exact continuation declaration;
3. no-overwrite destination for the next locator-plan document.

All three inputs start blank.

The shell does not reuse the earlier rollover text fields as location authority.

Thus:

```text
path used moments ago
!=
current path authority
```

This preserves the existing rule:

```text
path = location, not identity
```

## Save action delegates to 32A

The UI does not implement locator transformation or fresh restart verification.

It calls only:

```text
persist_chromium_research_session_continuation_reentry_plan(...)
```

with:

```text
current shell re-entry lineage
+ exact last rollover result
+ explicit current successor path
+ explicit current continuation declaration path
+ explicit plan destination
```

32A remains the authority for:

- transforming old declared paths into predecessor locator order;
- requiring the exact chosen successor;
- requiring the exact continuation declaration;
- fresh 31A reconstruction before write;
- exact presentation/endpoint agreement;
- no-overwrite plan persistence;
- strict locator-document round trip.

Therefore:

```text
UI button
!=
restart authority
```

The UI is only the human selection/input surface over the established 32A boundary.

## Successful checkpoint state transition

After one successful restart-plan save, the shell retains:

```text
result.fresh_reentry
```

as its new explicit restart lineage.

The currently mounted live continuation controller is not replaced by the freshly
reconstructed controller object.

Those controllers may be distinct Python objects while presenting the same verified
durable session.

Therefore:

```text
fresh restart controller object
!=
live UI controller object
```

and:

```text
presentation/content coherence
!=
Python object identity
```

The new lineage is what allows the next rollover checkpoint to compose correctly.

## Revision unlock

After 32A succeeds, the endpoint revision controls unlock for the currently mounted
continuation.

The restart-plan controls themselves lock after success so the same UI checkpoint
cannot silently overwrite or mutate the saved operational choice.

The successful receipt states that the plan is restart configuration only and is not
a global latest/current/head claim.

## Failure behavior

If any of the three explicit paths is blank, the checkpoint fails and revision stays
locked.

If the successor path identifies a different valid sibling, 32A rejects and revision
stays locked.

If the continuation declaration is stale or wrong, 32A rejects and revision stays
locked.

If prior durable lineage was tampered with, 32A's fresh re-entry rejects and revision
stays locked.

If the plan destination already exists, no-overwrite persistence rejects and revision
stays locked.

The shell never falls back to:

- the path entered during rollover;
- a nearby file;
- directory scanning;
- digest search;
- newest-file selection;
- latest/head discovery;
- automatic overwrite.

## Moved durable files

A focused test rolls over successfully, moves both the successor edge and continuation
declaration, then supplies their new locations to the checkpoint.

32A freshly reconstructs the continuation and writes the new plan successfully.

The earlier rollover locations receive no privilege.

## Repeatable checkpoint loop

A focused UI test proves:

```text
launch v6
→ write v7
→ roll over to v7
→ v7 revision locked
→ save/prove v7 restart plan
→ v7 revision unlocked
→ write v8
→ roll over to v8
→ v8 revision locked
→ save/prove v8 restart plan
→ v8 revision unlocked
```

The v8 restart plan carries forward the explicit locator lineage earned by the v7
restart plan.

No field or operation named `latest`, `current_head`, or canonical head is introduced.

Thus:

```text
restart lineage advanced by explicit checkpoints
!=
global head state
```

## Existing standalone behavior remains

The older standalone tests continue to exercise controller-only shells.

Those shells can still perform the existing write/rollover loop without a restart
checkpoint because they never claimed to own a restart locator lineage.

32B does not reinterpret their authority after the fact.

## Falsifiability

Focused 32B coverage proves:

1. an exact 31A result can be retained alongside the standalone controller;
2. no checkpoint is shown before a rollover;
3. rollover mounts a blank restart checkpoint and locks further revision;
4. a successful 32A save advances only the restart lineage and unlocks revision;
5. each missing explicit path fails without unlocking or writing a plan;
6. a valid sibling successor cannot substitute for the chosen rollover successor;
7. no-overwrite plan failure leaves the checkpoint locked;
8. moved durable files work only through explicitly supplied new locations;
9. the v7 → checkpoint → v8 → checkpoint workflow composes correctly;
10. a forged/mismatched re-entry lineage rejects before it becomes shell authority;
11. the public CLI passes the full 31A result to the UI rather than discarding locator lineage.

## Scope

32B changes only:

- new `src/pyxis/ui/chromium_research_session_restart_plan_textual.py`;
- restart-checkpoint state in `ResearchEndpointRevisionControls`;
- re-entry-aware restart checkpoint wiring in `ResearchSessionShell`;
- the thin CLI handoff so the exact 31A result reaches the shell;
- focused CLI and standalone UI tests;
- this milestone document.

It does not change:

- 32A application semantics;
- locator-plan schema;
- research evidence persistence formats;
- 29A endpoint revision semantics;
- 30A rollover semantics;
- Chromium acquisition;
- Repository Zero Workspace/compiler/runtime/export/measurement behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 32B proves

Successful 32B establishes only:

> A standalone Pyxis research shell launched from one explicit durable locator plan
> can roll into one explicitly chosen continuation, visibly pause further endpoint
> authoring until the researcher supplies current durable locations and a new plan
> destination, delegate a fresh restart proof and no-overwrite plan write to 32A,
> retain the newly proven 31A lineage, and then continue authoring from the mounted
> continuation without inventing discovery, overwrite, chronology, or global-head
> authority.

It does not prove complete ancestry, source authenticity, semantic support, citation
authority, unique succession, trusted chronology, or a canonical research head.
