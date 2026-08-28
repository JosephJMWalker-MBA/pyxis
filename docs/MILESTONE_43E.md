# Milestone 43E — bounded cumulative explicit-path submission kernel

**Decision:** D217  
**Status:** implementation pending executed Repository Zero evidence

## Purpose

Milestone 43E extends the private cumulative checkpoint form mechanics introduced by
43B/D214 with one additional procedure that has now been independently repeated by
the root-backed 35E, second-epoch 37D, and third-epoch 40D product shells:

> collect the four explicitly entered cumulative checkpoint paths, reject blanks in
> the established order using concrete family wording, and return those exact values
> as `Path` objects to the concrete save handler.

This milestone is a UI refactor. It grants no new persistence, proof, lineage, restart,
discovery, path, chronology, browser, or semantic authority.

## Prior evidence

43B already established a private form kernel for three independently earned
cumulative checkpoint control families. That kernel owns the four blank input IDs,
the status widget ID, form composition, and post-success locking while concrete
controls retain their public types, wording, selectors, and typed result checks.

After 43D, the three cumulative save handlers still contained the same mechanical
input section:

1. query the current-overlay input;
2. query the successor-edge input;
3. query the cumulative-declaration destination input;
4. query the next-overlay destination input;
5. reject a blank current overlay;
6. reject a blank successor;
7. reject a blank declaration destination;
8. reject a blank next-overlay destination;
9. build four `Path` values;
10. call the concrete family persistence function with those four values.

The surrounding authority predicates are not equivalent merely because the input
mechanics repeat. D217 therefore extracts only steps 1–9 into the existing private
43B form boundary.

## Decision D217

Add one private frozen submission value:

```text
_CumulativeCheckpointPathSubmission
    current_overlay_source: Path
    successor_edge_source: Path
    cumulative_declaration_destination: Path
    next_overlay_destination: Path
```

and one private form method:

```text
_CumulativeCheckpointTextualControls
    ._collect_cumulative_checkpoint_path_submission(...)
```

The method:

- uses only the four input IDs and status ID already owned by the concrete form spec;
- checks blank values in the existing current → successor → declaration → next-overlay
  order;
- receives the four concrete failure strings from the concrete save handler;
- updates the already-existing concrete status widget on failure;
- returns `None` after one failed blank check;
- returns one private frozen submission on success;
- constructs `Path` from the exact original input value after using `.strip()` only
  for the blank test, preserving prior behavior.

The module remains private and exports no authority surface through `__all__`.

## Concrete save order remains unchanged

For all three cumulative families the save boundary remains:

```text
CONCRETE CONTROLS + STATUS
        ↓
CONCRETE MISSING-ROLLOVER CHECK
        ↓
CONCRETE DISPLAYED ROLLOVER IDENTITY CHECK
        ↓
CONCRETE CURRENT TYPED RE-ENTRY IDENTITY CHECK
        ↓
43E PRIVATE FOUR-PATH COLLECTION
        ↓
CONCRETE PERSISTENCE CALL
        ↓
CONCRETE PERSISTENCE EXCEPTION HANDLING
        ↓
CONCRETE 35E / 37D / 40D RESULT + ANCESTRY PROOF
        ↓
43B OLD-FORM LOCK
        ↓
43C VISIBLE PROMOTION
```

43E cannot invoke persistence, choose a path, infer a path, prove a path, substitute a
path, or promote a path to current/latest/head authority.

## Root-backed 35E remains concrete

The root-backed save handler still owns:

- exact `ChromiumResearchRootBackedSessionContinuationReentryResult` identity;
- exact retained `ChromiumResearchSessionRolloverResult` identity;
- the concrete 35E persistence function;
- fixed direct 35C anchor preservation;
- terminal edge SHA-256 equivalence;
- terminal revised-note text equivalence;
- retained root identity;
- concrete persistence-error prefix;
- concrete success lock and visible promotion.

Its only delegated input behavior is the four explicit path reads and blank checks.

## Second epoch 37D remains concrete

The second-epoch save handler still owns:

- immutable persisted launch lineage separately from mutable current typed continuation;
- exact current 37C/37D typed continuation identity;
- exact retained rollover identity;
- the concrete 37D persistence function;
- fixed direct 37B anchor preservation;
- terminal edge SHA-256 and revised-note text equivalence;
- second-epoch anchor presentation and endpoint identity;
- retained first- and second-root identities;
- concrete persistence-error prefix;
- concrete success lock and visible promotion.

The first-checkpoint 37C shell is outside 43E and remains unchanged.

## Third epoch 40D remains concrete

The third-epoch save handler still owns:

- persisted launch lineage or separately established typed handoff state;
- exact mutable current third-epoch continuation identity;
- exact retained rollover identity;
- the concrete 40D persistence function;
- fixed direct 40B anchor preservation;
- terminal edge SHA-256 and revised-note text equivalence;
- third-epoch anchor presentation and endpoint identity;
- retained three-root ancestry;
- concrete persistence-error prefix;
- concrete success lock and visible promotion.

The first-checkpoint 40C shell is outside 43E and remains unchanged.

## Bounded cumulative extraction stack

The cumulative product now contains five deliberately narrow reuse boundaries:

```text
43A / D213
private application fixed-anchor cumulative extension mechanics

43B / D214
private Textual four-path form composition + old-form locking mechanics

43C / D215
private post-proof visible cumulative promotion mechanics

43D / D216
private post-base-rollover cumulative checkpoint gating mechanics

43E / D217
private four explicit path collection + blank-validation mechanics
inside the existing 43B form boundary
```

These are procedural extractions, not a generic ancestry or epoch model.

## Falsifiability

43E is acceptable only if tests demonstrate that:

1. blank validation remains current overlay → successor → declaration → next overlay;
2. each concrete failure string remains exact and caller-owned;
3. successful submission returns `Path` objects built from the exact entered values;
4. root-backed, second-epoch, and third-epoch save handlers each delegate only path
   collection to the private form method;
5. each concrete persistence call receives the exact four returned submission fields
   under its existing keyword names;
6. concrete proof, lock, and promotion still execute after persistence;
7. the mature mounted 36C/38E/41D cumulative checkpoint suites remain green;
8. the private form module still exports no public authority API.

## Non-goals

43E adds no:

- generic save-handler orchestrator;
- persistence abstraction or persistence API change;
- result-proof abstraction;
- exception-handling abstraction;
- rollover/current identity abstraction;
- result-locking change;
- promotion change;
- 43A, 43C, or 43D kernel change;
- first-checkpoint 37C or 40C change;
- CSS change;
- handoff change;
- constructor change;
- generic cumulative shell superclass or mixin;
- fourth evidence-basis epoch;
- generic `epoch[n]` or arbitrary-depth ancestry;
- generic shell lineage;
- CLI behavior;
- durable-format change;
- path discovery or prefilling;
- `latest`, `current`, or `head` inference;
- path identity or chronology/branch authority;
- authorship, authenticity, or trusted-time claim;
- semantic-support or citation authority.

## Acceptance statement

Milestone 43E is complete when the three mature cumulative save handlers still retain
all family-specific authority checks and persistence/proof behavior while delegating
only their repeated four explicit path reads, blank checks, and `Path` conversion to
the existing private cumulative form kernel, with the full Repository Zero suite
passing on every supported Python version.
