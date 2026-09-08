# Milestone 50W — checkpoint 40C and hand off 41E after bare 47G

Decision: **D277**  
Issue: **#284**

## Concrete researcher action

50V proves that a real bare third-basis public-40B overlay-v2 can be followed by the
existing explicit 47G typed handoff into a pathless third-basis first-checkpoint
receiver.

The next concrete action is:

> Continue once from that exact pathless 47G session, explicitly checkpoint the first
> post-third-root continuation using the still-known 40B-v2 path, then explicitly
> hand the freshly proven 40C continuation into cumulative mode without reloading the
> just-written 40C file.

## Reuse review

All required boundaries already existed:

```text
47G exact typed third-basis handoff
→ pathless first-checkpoint receiver
→ ordinary rollover
→ public 40C proof-gated checkpoint
→ explicit 41E handoff
→ pathless cumulative receiver
```

50T already proves that public 40C can anchor to a third-basis 40B overlay-v2.

41E already proves that a successful 40C checkpoint may be transferred explicitly by
exact `checkpoint.fresh_reentry` identity without carrying persisted path authority.

50W therefore tests their concrete composition rather than introducing another
version or handoff family.

## Decision

50W is **proof-only**.

No production-code changes.

No persistence-format changes.

No handoff changes.

No CLI or inspection-format changes.

## Starting authority

The focused proof creates a real third-basis 40B overlay-v2 whose retained ancestry
contains all three bare saved passages.

The exact:

`public 40B checkpoint.fresh_reentry`

is used as the 47G authority subject already proven by 50V.

The existing inspectable pathless 47G receiver starts with:

```text
third_basis_epoch_launch_lineage = None
third_basis_epoch_handoff_reentry = exact handoff
third_basis_epoch_reentry = exact handoff
research_controller = exact handoff controller
```

Its launch inspection remains:

```text
launch family: in-process 47G typed third-basis-epoch handoff
launch location context: none
```

## First rollover after 47G

One ordinary governed endpoint revision and rollover is performed.

Only then does the existing 40C checkpoint form mount.

All four durable path fields begin blank:

1. explicit current 40B overlay source;
2. explicit chosen successor edge source;
3. explicit continuation declaration source; and
4. explicit no-overwrite 40C destination.

The 47G handoff does not prefill the 40B-v2 path.

## Public 40C remains unchanged

The researcher explicitly supplies the original 40B-v2 path plus the chosen
successor/declaration/destination.

Unchanged public 40C:

- freshly decodes the 40B-v2 anchor;
- freshly reconstructs the full three-bare third-basis epoch;
- proves retained first-, second-, and third-root identity;
- proves the chosen rollover belongs to that exact third-basis session;
- freshly reconstructs the first post-third-root continuation; and
- writes strict locator-only 40C-v1.

The resulting document remains exactly:

`pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1`

and references the supplied 40B-v2 path without copying any bare-selection member
configuration.

## Three bare passages survive 40C

The fresh 40C result retains:

- first-root bare saved passage;
- second-basis bare saved passage; and
- third-basis bare saved passage.

Each remains a real loaded exact-range selection with no manufactured note.

The third bare loaded object remains retained by the reconstructed continuation
endpoint working set.

## 40C success does not auto-enter cumulative mode

Successful checkpointing keeps the first-checkpoint receiver revision-locked.

Exactly one explicit:

`Continue in cumulative mode`

action appears.

No automatic mode transition occurs.

The 47G launch-provenance object remains exact and pathless.

## Exact 41E authority subject

The 41E subject is exactly:

`checkpoint.fresh_reentry`

by Python object identity.

After successful 40C persistence, the proof deletes the newly written 40C overlay
before the explicit 41E action is selected.

41E still returns the exact retained fresh typed continuation object.

Therefore 41E performs no:

- 40C reload;
- 41A persisted-path proof;
- path inference; or
- path promotion.

The missing 40C file affects later disk-based relaunch, not the already-earned
same-process typed handoff.

## Existing pathless cumulative receiver

The exact 41E object initializes the established inspectable cumulative handoff
receiver:

```text
third_basis_epoch_continuation_launch_lineage = None
third_basis_epoch_continuation_handoff_reentry = exact handoff
third_basis_epoch_continuation_reentry = exact handoff
research_controller = exact handoff controller
```

No current-overlay path or launch-overlay path is stored.

Its inspection remains:

```text
launch family: in-process 41E typed continuation handoff
launch location context: none
current typed continuation: exact handed-off 40C result
declared continuation edge count: 1
```

## Next cumulative rollover

The researcher performs one additional ordinary governed rollover.

The existing 40D cumulative form mounts with all four durable fields blank:

1. explicit current 40C/40D overlay path;
2. explicit chosen successor edge path;
3. cumulative declaration destination; and
4. next continuation overlay destination.

No deleted 40C path is backfilled.

## Executable boundary correction

The first 50W executable head intentionally required the inspection current-state
projection to advance immediately after that cumulative-mode rollover.

Repository Zero falsified that assumption.

Existing 42A semantics deliberately separate:

```text
visible one-hop rollover
!=
promoted typed cumulative continuation
```

In cumulative mode, the typed current continuation advances only after a successful
public-40D proof and visible cumulative promotion.

Therefore the corrected 50W proof requires:

- the live controller to show the newly chosen one-hop rollover;
- the blank 40D form to mount against the exact prior typed continuation;
- immutable 41E launch provenance to remain object-identical and pathless; and
- the inspection current-state object to remain exactly the last proven typed 40C
  continuation until a later 40D checkpoint succeeds.

No production correction was warranted.

## Repository Zero proof

The corrected executable head:

`18081318e00c451c08b20bc953597897215a6e01`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50W changes only:

- one focused composition proof;
- this milestone record; and
- compact README continuity.

It does not change:

- public 40A;
- public 40B v1/v2;
- public 40C;
- public 40D;
- 47G;
- 41E;
- CLI behavior;
- inspection formats;
- first-/second-basis formats;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50W proves only:

```text
47G
→ ordinary rollover
→ explicit 40C checkpoint
→ explicit 41E handoff
→ pathless cumulative receiver
→ ordinary rollover
→ blank 40D form
```

Do not infer:

- automatic checkpointing;
- path carryover;
- automatic cumulative promotion;
- successful 40D persistence after this exact pathless chain;
- fourth-basis behavior;
- arbitrary-depth handoff/version propagation;
- path discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

A later milestone may prove the final explicit 40D persistence step after this exact
47G → 40C → 41E path if that remains a concrete researcher action.

## Compact result

After 50W:

```text
bare third-basis 40B-v2
→ exact pathless 47G receiver
→ ordinary rollover
→ explicit unchanged 40C-v1 checkpoint
→ exact pathless 41E handoff
→ cumulative receiver
→ ordinary rollover
→ blank existing 40D form
```

No durable version or path authority leaks into either in-process handoff.
