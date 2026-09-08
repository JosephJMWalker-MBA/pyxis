# Milestone 50V — prove 47G typed handoff after third-basis overlay-v2 persistence

Decision: **D276**  
Issue: **#282**

## Concrete researcher action

50R–50U prove the persisted restart path for a third-basis bare saved passage through:

```text
47E / public 40A
→ 47F / public 40B overlay-v2
→ persisted relaunch
→ ordinary 40C-v1 continuation
→ cumulative 40D / 40C-v1
```

A separate established same-process action remains:

> Immediately after successful 47F persistence, explicitly continue with the exact
> freshly proven third-basis session instead of closing and reloading the just-written
> 40B overlay.

That is the existing 47G typed handoff.

## Reuse review

47G already owns the correct authority seam:

```text
successful 47F persistence
+ explicit human handoff action
→ exact public-40B checkpoint.fresh_reentry
→ pathless third-basis first-checkpoint receiver
```

The handoff does not consume:

- the 40B overlay format string;
- the saved 40B path;
- persisted 41A launch lineage; or
- a caller-selected durable version.

50R widened only the public-40B document codec and persistence evidence.

Both overlay-v1 and overlay-v2 still return the same typed public-40B checkpoint
structure whose exact fresh authority subject is:

`checkpoint.fresh_reentry`

Therefore the strongest hypothesis was:

```text
47F writes 40B overlay-v2
does not imply
new 47G handoff code
```

## Decision

50V is **proof-only**.

No production-code changes.

No persistence-format changes.

No handoff changes.

No CLI or inspection-format changes.

## Full three-bare source history

The focused proof begins with the same real ancestry as 50R:

```text
first-root bare saved passage
→ first-root overlay-v2
→ ordinary first-root continuation
→ cumulative first-root continuation
→ second-basis bare saved passage
→ second-basis 37B overlay-v2
→ ordinary second-epoch 37C-v1 continuation
→ cumulative second-epoch 37D / 37C-v1
→ third bare saved passage
```

That third bare selection is then carried through the existing 47G-enabled
persisted-source changed-basis product.

The normal third-basis product flow remains:

```text
44A preparation
→ 47A transition
→ 47B third root
→ 47C first edge
→ 47D explicit adoption
→ 47E / public 40A fresh proof
→ 47F / public 40B persistence
```

## 47F writes real overlay-v2

The existing 47F product receives the exact bare 47E proof.

Public 40B selects:

`pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2`

from the typed third-basis member vocabulary.

The persisted appended member remains exact:

```json
{
  "kind": "exact_range_selection",
  "capture_source": "...",
  "selection_source": "..."
}
```

No note locator is manufactured.

## Persistence remains separate from handoff

Successful 47F persistence does not exit the source product.

The focused proof retains the exact mounted:

- changed-basis controller;
- research session;
- generic research re-entry; and
- prior second-epoch continuation.

The source product's immutable launch-provenance object also remains exact.

The current-state inspection legitimately advances during the earlier 47A–47E
changed-basis workflow. The 50V invariant therefore begins at the exact pre-47F
current state: neither 47F persistence nor the later explicit 47G exit mutates that
state further.

Exactly one 47G handoff control appears only after successful v2 persistence.

## Exact 47G authority subject

The handoff subject is exactly:

`result.checkpoint.fresh_reentry`

That object is the fresh public-40B proof result produced during 47F.

It is deliberately not:

`verification.fresh_reentry`

from the earlier 47E proof.

The focused proof establishes that distinction by Python object identity.

## Handoff survives loss of the saved v2 document

After successful 47F persistence, the proof deletes the just-written 40B-v2 overlay
file before selecting the 47G action.

The explicit handoff still succeeds and returns the exact retained:

`result.checkpoint.fresh_reentry`

object by identity.

Therefore 47G does not:

- reload the persisted overlay;
- infer launch authority from the path;
- require the path to remain available; or
- fabricate 41A persisted lineage.

The missing file would matter only to a later disk-based restart.

## All three bare passages survive typed transfer

The exact handed-off typed object still contains three distinct real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

records.

The first bare saved passage remains in first-root ancestry.

The second remains in second-basis ancestry.

The third remains in the third-basis layer.

Each has exact selected text:

`"Bare"`

and no manufactured note.

## Existing pathless receiver inherits the proof

The exact returned object is supplied directly to the existing inspectable 47G
receiver.

The receiver remains:

```text
third_basis_epoch_launch_lineage = None
third_basis_epoch_handoff_reentry = exact handoff
third_basis_epoch_reentry = exact handoff
research_controller = exact handoff controller
```

No persisted 40B path is loaded, stored, inferred, or backfilled.

## Read-only 47G inspection remains pathless

The existing 47G launch-inspection projection remains:

```text
launch family: in-process 47G typed third-basis-epoch handoff
launch location context: none
first-root SHA-256: exact retained first root
second-root SHA-256: exact retained second root
third-root SHA-256: exact retained third root
launch endpoint SHA-256: exact handed-off endpoint
```

No overlay-version field is required.

The launch-provenance object remains immutable and pathless.

## Ordinary rollover remains the next explicit action

The pathless receiver begins with no 40C checkpoint form.

After one ordinary governed rollover, the existing 40C form mounts.

All four durable locator fields are blank:

- current 40B overlay source;
- successor edge source;
- continuation declaration source; and
- no-overwrite 40C destination.

The handoff does not prefill the deleted 40B-v2 path or any other location.

The receiver's current-state inspection advances to:

`explicit rollover after in-process 47G handoff`

while the exact launch-provenance object remains object-identical and pathless.

The third bare saved passage remains the exact loaded working-set member retained by
the rollover endpoint.

## Repository Zero proof

Corrected test-only head:

`0255deee5c47b526f05bc4a415c043f341b1b45a`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

with no production-code correction.

The first focused head exposed only a test-boundary mistake: it compared current-state
inspection to the initial second-epoch launch state even though 47A–47E are explicitly
allowed to advance visible current state. The proof was corrected to snapshot the
exact pre-47F state, which is the authority boundary 50V actually claims.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50V changes only:

- one focused bare-v2 47G compatibility proof;
- this milestone record; and
- compact README continuity.

It does not change:

- public 40A;
- public 40B v1/v2 behavior;
- 47F persistence;
- 47G source/receiver classes;
- persisted 41A lineage;
- public 40C/40D;
- CLI behavior;
- authority-inspection formats;
- first-/second-basis formats;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50V proves only same-process 47G typed handoff compatibility with a bare third-basis
40B-v2 persistence result.

Do not infer:

- automatic handoff;
- persisted-path carryover into the receiver;
- automatic 40C persistence;
- fourth-basis persistence;
- fourth-basis relaunch;
- generic Nth-basis handoff/version propagation;
- automatic path discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The three-basis bare-selection path is now covered across both persisted restart and
same-process handoff.

Any next milestone should begin from a genuinely missing researcher action rather
than another symmetry proof.

## Compact result

After 50V:

```text
third bare saved passage
→ 47E / public 40A
→ 47F / public 40B overlay-v2
→ exact public-40B fresh_reentry retained in memory
→ saved overlay may disappear
→ explicit 47G action
→ exact typed object transferred pathlessly
→ established inspectable third-basis first-checkpoint receiver
→ ordinary rollover
→ blank existing 40C checkpoint surface
```

The durable version distinction remains irrelevant to the in-process typed handoff.
