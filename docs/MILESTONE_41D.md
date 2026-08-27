# Milestone 41D — Repeatable cumulative 40D checkpointing in Textual

## Decision D209

Persisted third-epoch continuations may checkpoint repeated ordinary successors through the existing cumulative 40D application boundary only if every successful checkpoint is visibly promoted to the freshly proven cumulative controller before another endpoint revision is unlocked.

## Starting authority

The continuation shell receives one exact 41A launch wrapper:

```text
ChromiumResearchThirdBasisEpochContinuationShellLineage
  overlay_source
  reentry
```

41D keeps two concepts separate:

```text
launch provenance = immutable 41A wrapper
current typed continuation = mutable only after successful 40D proof
```

Initially:

```text
current typed continuation = launch_lineage.reentry
live controller = current typed continuation.controller
```

The launch wrapper is never rewritten when cumulative work advances.

## One cumulative cycle

```text
current persisted 40C/40D cumulative controller
→ explicit endpoint revision
→ explicit 30A one-hop rollover
→ visible one-hop controller
→ revision lock
→ four blank cumulative checkpoint inputs
→ existing 40D application proof
→ fresh cumulative continuation result
→ visible cumulative promotion
→ revision unlock
```

The one-hop controller is not silently promoted into typed durable state. Promotion happens only after the existing 40D proof succeeds.

## Why whole-presentation equality is wrong

Suppose the current persisted post-third-root declaration is:

```text
E1 → E2 → E3
```

and the researcher chooses one successor `E4`.

The 30A rollover intentionally presents only the chosen one-hop continuation. The freshly reconstructed 40D controller presents the full cumulative segment:

```text
E1 → E2 → E3 → E4
```

Therefore the shell compares the visible one-hop choice to the freshly proven cumulative result by:

- durable terminal edge SHA-256; and
- exact final human note text.

The 40D application boundary separately proves the complete cumulative sequence and declaration.

## Cumulative checkpoint inputs

Every cycle begins with four blank fields:

```text
explicit current 40C/40D overlay path
explicit chosen successor edge path
no-overwrite cumulative declaration destination
no-overwrite next 40C/40D overlay destination
```

No field is prefilled from:

- the 41A launch wrapper;
- the previous successful checkpoint;
- prior endpoint-revision inputs; or
- rollover declaration inputs.

Every operation location is supplied explicitly for that operation.

## Direct 40B anchor without recursive continuation ancestry

40D keeps cumulative continuation overlays directly anchored to the same explicit 40B third-epoch overlay:

```text
40B → 40C/40D cumulative overlay
```

rather than:

```text
40B → 40C → 40C → 40C ...
```

The shell requires:

```text
next_plan.prior_third_basis_epoch_overlay_source
== current_plan.prior_third_basis_epoch_overlay_source
```

for structural non-recursion.

A path-distinct current 40C/40D overlay remains admissible only when the existing application proof freshly reconstructs the same governed continuation and retained three-root ancestry. Path equality to launch-time configuration is not session identity.

## Three-root preservation

After 40D proof, before UI promotion, the shell verifies that the freshly proven cumulative result retains:

- the same third-epoch anchor presentation;
- the same third-epoch anchor endpoint identity;
- the same third-root durable identity;
- the same second-root durable identity; and
- the same retained first-root durable identity.

This is a shell-level consistency check over the result returned by the application boundary. It does not replace or duplicate the application layer's fresh reconstruction proof.

## Visible promotion

On successful 40D checkpoint the continuation shell:

1. rebuilds the session presentation from `fresh_reentry.controller.loaded`;
2. requires exact equality with the controller's retained presentation;
3. validates one working-set context per declared position;
4. removes the visible one-hop detail, locked revision controls, rollover controls, checkpoint form, and one-hop receipt;
5. sets `third_basis_epoch_continuation_reentry = fresh_reentry`;
6. sets the live controller/session/presentation/context to the fresh cumulative state;
7. clears `last_research_rollover`;
8. retains the original 41A launch wrapper unchanged;
9. mounts a cumulative success receipt;
10. mounts the freshly proven cumulative sequence detail; and
11. unlocks one new endpoint revision and empty rollover surface.

Hidden typed state therefore never outruns the visible cumulative presentation.

## Failure semantics

A failed cumulative checkpoint leaves:

- the chosen one-hop continuation visible;
- endpoint revision locked;
- the current typed continuation unchanged;
- the immutable 41A launch wrapper unchanged;
- the cumulative checkpoint form available for corrected explicit inputs; and
- no new cumulative declaration or overlay promoted into shell state.

No hidden lineage advancement occurs.

## Repeatability

A second successful cycle begins from the freshly promoted result of the first cycle and requires all four paths blank again.

Tests prove:

- the ordered post-third-root edge tuple grows each cycle;
- the direct 40B ancestry anchor remains fixed structurally;
- no continuation overlay becomes recursive ancestry for the next overlay;
- all three basis-change roots remain retained;
- the immutable 41A launch wrapper remains unchanged;
- the current typed continuation advances only after successful proof; and
- a shell launched from an already-cumulative 40D overlay can continue through the same boundary.

## Preserved non-authorities

41D introduces no:

- new persistence format;
- new application checkpoint API;
- ordinary restart-plan authority;
- path discovery or prefilling;
- automatic mode transition;
- in-process handoff from the 41C first-checkpoint shell;
- three-root inspection UI/report;
- automatic latest/current/head selection;
- chronology or branch semantics;
- fourth evidence-basis epoch;
- generic `epoch[n]` / arbitrary-depth lineage;
- semantic-support judgment; or
- authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

41D establishes only this claim:

> A researcher operating from one explicitly proven persisted 40C/40D third-epoch continuation can repeatedly checkpoint ordinary successors through the existing cumulative 40D proof boundary. Each success visibly promotes the freshly proven cumulative controller before further revision is unlocked, while the direct 40B anchor, retained three-root ancestry, explicit-path discipline, and immutable 41A launch provenance remain intact.

## Next seam

A later milestone may add an explicit in-process handoff from the 41C first-checkpoint shell into this cumulative continuation mode. That handoff must remain explicit, carry the freshly proven typed 40C continuation object, and avoid promoting any checkpoint path into implicit current-location authority.
