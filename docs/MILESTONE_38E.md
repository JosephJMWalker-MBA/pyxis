# Milestone 38E — Repeatable cumulative 37D checkpointing in Textual

## Decision D198

Persisted second-epoch continuations may checkpoint repeated ordinary successors through the existing cumulative 37D application boundary only if every successful checkpoint is visibly promoted to the freshly proven cumulative controller before another endpoint revision is unlocked.

## Starting authority

The continuation shell receives one exact 38B launch wrapper:

```text
ChromiumResearchSecondBasisEpochContinuationShellLineage
  overlay_source
  reentry
```

38E separates two concepts that must not collapse:

```text
launch provenance = immutable 38B wrapper
current typed continuation = mutable only after successful 37D proof
```

Initially:

```text
current typed continuation = launch_lineage.reentry
live controller = current typed continuation.controller
```

## One cumulative cycle

```text
current persisted cumulative controller
→ explicit endpoint revision
→ explicit 30A one-hop rollover
→ visible one-hop controller
→ revision lock
→ four blank cumulative checkpoint inputs
→ existing 37D application proof
→ fresh cumulative continuation result
→ visible cumulative promotion
→ revision unlock
```

The one-hop controller is never silently replaced in hidden typed state. Promotion is explicit and visible.

## Why whole-presentation equality is wrong

Suppose the current persisted declaration is:

```text
E1 → E2 → E3
```

and the researcher chooses a one-hop successor `E4`.

The 30A rollover surface intentionally presents only the chosen one-hop continuation, while the fresh 37D controller presents:

```text
E1 → E2 → E3 → E4
```

Therefore the shell validates chosen continuation equivalence at the terminal edge:

- durable terminal edge SHA-256;
- exact final human note text.

The application boundary separately proves the full cumulative sequence and declaration.

## Cumulative checkpoint inputs

Each cycle requires four blank inputs:

```text
explicit current 37C/37D overlay path
explicit chosen successor edge path
no-overwrite cumulative declaration destination
no-overwrite next 37C/37D overlay destination
```

No field is prefilled from:

- the 38B launch wrapper;
- the previous successful checkpoint;
- prior rollover inputs.

Every operation location is supplied explicitly for that operation.

## Direct 37B anchor without path identity

37D keeps continuation overlays non-recursive:

```text
37B → 37C/37D cumulative overlay
```

rather than:

```text
37B → 37C → 37C → 37C ...
```

When a path-distinct current 37C/37D overlay is explicitly supplied, its decoded plan may itself contain a path-distinct but durably equivalent direct 37B locator.

The shell therefore requires:

```text
next_plan.prior_second_basis_epoch_overlay_source
== current_plan.prior_second_basis_epoch_overlay_source
```

for structural non-recursion, while durable equivalence to the shell's typed ancestry is proved through:

- second-epoch anchor presentation;
- second-epoch terminal edge identity;
- second-root identity;
- retained first-root identity.

Thus path equality to the launch-time anchor is not treated as identity.

## Visible promotion

On successful 37D checkpoint the shell:

1. rebuilds the session presentation from `fresh_reentry.controller.loaded`;
2. requires exact equality with the controller's retained presentation;
3. validates one working-set context per declared position;
4. removes the one-hop detail, locked revision, rollover controls, checkpoint form, and one-hop receipt;
5. sets `second_basis_epoch_continuation_reentry = fresh_reentry`;
6. sets the live controller/session/presentation/context to that fresh cumulative state;
7. clears `last_research_rollover`;
8. retains the original 38B launch wrapper unchanged;
9. mounts a cumulative success receipt;
10. mounts the fresh cumulative sequence detail;
11. unlocks a new endpoint revision and empty rollover.

## Failure semantics

A failed cumulative checkpoint leaves:

- the one-hop controller visible;
- endpoint revision locked;
- the current typed continuation unchanged;
- the 38B launch wrapper unchanged;
- the cumulative checkpoint form available for corrected explicit inputs.

No hidden lineage advancement occurs.

## Repeatability

A second successful cycle starts from the freshly promoted first cumulative result and requires blank locations again.

Tests prove:

- the ordered declared edge tuple grows on each cycle;
- the new overlay still directly references the explicit current plan's 37B anchor;
- no continuation overlay references another continuation overlay as ancestry;
- the immutable launch wrapper remains unchanged;
- the current typed continuation advances only after successful proof.

## Preserved non-authorities

38E adds no:

- new persistence format;
- new application API;
- ordinary restart-plan authority;
- path discovery or prefilling;
- automatic latest/current/head selection;
- chronology or branch semantics;
- semantic-support judgment;
- authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

38E establishes only this claim:

> A researcher operating from a persisted second-epoch continuation can repeatedly checkpoint ordinary successors through the existing cumulative 37D proof boundary. Each success visibly promotes the freshly proven cumulative controller before further revision is unlocked, while direct second-epoch ancestry and explicit-path authority rules remain intact.

## Next seam

A later milestone may add an explicit in-process handoff from the 38D first-checkpoint shell into this cumulative shell, analogous to 36D. That handoff must remain explicit and carry the freshly proven typed continuation object without promoting a path into persistent current-location authority.
