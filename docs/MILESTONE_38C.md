# Milestone 38C — Dedicated second-epoch Textual launch shells

## Decision D196

Pyxis retains the exact proof-carrying 38B launch lineage inside dedicated second-epoch Textual shell types before adding any second-epoch checkpoint controls.

## Problem

38A made persisted 37B and 37C/37D sessions publicly launchable, but mounted them through the generic controller-only shell. 38B then proved a stronger in-memory authority object: one explicit overlay location paired with the fresh typed re-entry reconstructed from that exact location.

Passing only `reentry.controller` into Textual would discard that proof boundary just before future checkpoint work needs it.

At the same time, simply supplying an overlay path alongside a controller would be unsafe: an arbitrary `(path, object)` pair has not earned authority merely because both values are present.

## Boundary

38C adds:

```text
SecondBasisEpochResearchSessionShell
SecondBasisEpochContinuationResearchSessionShell
```

Each shell accepts only its exact 38B lineage wrapper and mounts:

```text
lineage.reentry.controller
```

through the existing `ResearchSessionShell` base behavior.

The base shell receives no ordinary 31A `research_reentry`.

Therefore 38C retains second-epoch launch lineage without inventing ordinary restart-plan authority.

## Public launch sequence

### Persisted 37B session

```text
explicit --second-basis-epoch-overlay
→ strict 37B decode
→ 37A fresh re-entry
→ 38B re-prove explicit path/result pairing
→ ChromiumResearchSecondBasisEpochShellLineage
→ SecondBasisEpochResearchSessionShell
```

### Persisted 37C or cumulative 37D continuation

```text
explicit --second-basis-epoch-continuation-overlay
→ strict 37C decode
→ 37C fresh re-entry
→ 38B re-prove explicit path/result pairing
→ ChromiumResearchSecondBasisEpochContinuationShellLineage
→ SecondBasisEpochContinuationResearchSessionShell
```

The second reconstruction is deliberate. The shell receives the fresh result returned by the explicit 38B path-binding proof, not the earlier unbound re-entry object.

## Launch lineage is not moving-head authority

The retained 38B wrapper is launch context:

```text
explicit persisted source
↕ freshly proven relationship
fresh launched re-entry
```

If the base shell later performs endpoint revision and an explicit 30A rollover, the live controller may move to an uncheckpointed continuation.

38C does not rewrite the retained launch wrapper to follow that live controller.

Therefore:

```text
launch lineage != implicit current persisted lineage
```

and:

```text
live in-memory continuation != proven restart configuration
```

This distinction is required before any later checkpoint-aware UI can be added safely.

## UI authority retained

Both dedicated shells continue to use the established base-shell surface for:

- governed declared-session inspection;
- endpoint revision;
- explicit 30A rollover.

They deliberately do not add:

- ordinary restart-plan controls;
- 37C first-continuation checkpoint controls;
- 37D cumulative checkpoint controls;
- path prefilling;
- automatic persistence;
- handoff behavior.

`research_reentry` remains `None` in both shells.

## CLI behavior

The two second-epoch CLI families no longer route through `_run_controller_only_research_session_shell`.

They now route only through their dedicated lineage-retaining shell factories after successful 38B proof.

The ordinary, 35C, and 35D/35E launch families are unchanged.

## Preserved authority rules

38C does not change:

- any persistence format;
- 37A, 37B, 37C, or 37D reconstruction/checkpoint semantics;
- evidence verification behavior;
- path identity semantics;
- browser authority;
- ordinary or first-root restart lineage.

It introduces no directory scanning, discovery, format guessing, latest/current/head selection, chronology, branch semantics, semantic-support judgment, authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

38C establishes only this claim:

> Public second-epoch launches retain the exact proof-carrying 38B path/re-entry lineage inside dedicated Textual shells. The shells still exercise only the generic governed controller mutation surface and do not invent ordinary restart lineage or second-epoch checkpoint authority.

## Next seam

The next safe product boundary can add the first second-epoch checkpoint transition to the 37B-backed dedicated shell, because that shell now possesses one exact proven launch lineage rather than an unverified path/object pair.
