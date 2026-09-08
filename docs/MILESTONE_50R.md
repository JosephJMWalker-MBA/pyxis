# Milestone 50R — persist third-basis bare restart configuration as overlay-v2

Decision: **D272**  
Issue: **#274**

## Concrete researcher action

50Q proves that a third changed-basis bare saved passage can cross the established
47A→47E product flow and be freshly reconstructed through public 40A while preserving
two earlier bare passages in ancestry.

The next concrete researcher action is:

> Persist that exact verified third-basis session as durable restart configuration so a
> later process can reconstruct it without converting the third bare passage into a
> note or widening unrelated continuation formats.

## Reuse review

Public 40B already owns the correct durable boundary:

```text
earned public 40A third-basis result
+ explicit current prior 37C/37D second-epoch continuation-overlay path
+ explicit no-overwrite destination
→ candidate third-basis re-entry plan
→ independent fresh public 40A reconstruction
→ retained first-/second-/third-root comparison
→ strict locator-overlay write
→ strict round-trip decode
```

50Q proved that the typed 40A plan already accepts:

`ChromiumResearchExactRangeSelectionReentryLocator`

The only incompatible layer was the 40B document codec.

Historical 40B overlay-v1 intentionally delegates appended-member encoding and decoding
to the frozen three-kind research-session codec:

- paragraph note;
- exact-range note; and
- comparison note.

That v1 codec therefore correctly rejected the new bare exact-range-selection locator.

The closest exact precedent is 50M / public 37B. The earned rule is:

```text
new member vocabulary
→ version only the durable boundary that owns that vocabulary
```

not every downstream product or ancestor format.

## Decision

40B gains one narrowly scoped overlay-v2.

Historical overlay-v1 remains frozen.

Public 40A remains unchanged.

Existing 47F product wiring remains unchanged and inherits the widened public 40B
boundary.

## Durable formats

Historical format remains:

`pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1`

New format:

`pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2`

V2 adds exactly one appended-member shape:

```json
{
  "kind": "exact_range_selection",
  "capture_source": "...",
  "selection_source": "..."
}
```

The shape contains no `note_source`.

All historical note-bearing v1 member shapes are delegated unchanged when loading v2.

## Version selection

Persistence chooses the durable format from the exact typed candidate plan.

If any appended third-basis member is a
`ChromiumResearchExactRangeSelectionReentryLocator`, 40B writes overlay-v2.

Otherwise it writes overlay-v1.

There is:

- no caller-selectable version argument;
- no filename/version inference;
- no product-mode inference; and
- no version propagation from the referenced second-epoch ancestry.

Thus second-basis overlay-v2 ancestry does not itself force third-basis overlay-v2.
Only the third-basis member vocabulary does.

## Mandatory fresh proof remains unchanged

Before any overlay bytes are written, public 40B still rebuilds its candidate plan and
re-enters through unchanged public 40A.

The fresh result must still match the earned result across:

- retained prior second-epoch continuation presentation;
- retained prior second-epoch continuation endpoint;
- first-root identity;
- second-root identity;
- third-root identity;
- final third-basis presentation; and
- final third-basis endpoint identity.

The versioned document codec does not weaken or bypass any of those checks.

## Full three-bare proof

The executable 50R fixture starts from the real nested ancestry:

```text
first-root bare saved passage
→ first-root overlay-v2
→ first-root ordinary continuation
→ first-root cumulative continuation
→ second-basis bare saved passage
→ second-basis overlay-v2
→ second-epoch ordinary continuation
→ second-epoch cumulative continuation
→ third bare saved passage
→ 44A
→ 47A transition
→ 47B third root
→ 47C first edge
→ 47D adoption
→ 47E / public 40A fresh proof
```

That exact successful 47E proof is supplied to unchanged 47F/public 40B.

## V2 persisted proof

The resulting third-basis restart document is exact overlay-v2.

Its appended bare member has exactly:

- `kind`;
- `capture_source`; and
- `selection_source`.

No note locator is manufactured.

Strict round-trip decoding returns the exact candidate typed 40A plan.

The mandatory fresh 40A reconstruction loads the third bare passage as a real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

with exact selected text:

`"Bare"`

and no `.note` attribute.

That exact loaded object is retained in the reconstructed third-root successor working
set and final third-basis endpoint working set.

The two earlier bare passages also survive inside the freshly reconstructed retained
second-epoch ancestry.

## V1 remains frozen

A note-only third-basis history still persists exact overlay-v1.

The v1 loader remains delegated to the historical three-kind codec.

A v1 document containing a bare `exact_range_selection` shape still fails closed.

Therefore:

```text
40B overlay-v1
!=
silently widened historical contract
```

## V2 compatibility and malformed-shape rejection

V2 delegates historical note-bearing member shapes unchanged.

The v2 bare shape fails closed when:

- `selection_source` is missing;
- an unexpected `note_source` is added; or
- the member kind is changed to an incompatible historical kind.

Unknown overlay versions also fail closed.

No permissive guessing is introduced.

## No-overwrite and tamper behavior

Existing no-overwrite persistence remains exact.

If the destination already exists, its bytes remain unchanged.

If referenced third-root or ancestry evidence is tampered before persistence, the
mandatory fresh public-40A proof fails before the destination is written.

The overlay remains operational locator configuration, not research authority.

It does not store:

- selected source text;
- human note text;
- evidence digests;
- timestamps;
- current/latest/head markers;
- semantic-support claims;
- authorship claims; or
- citation authority.

## Existing 47F product inherits the widened boundary

The real 47F Textual product is driven from a real bare 47E proof.

No new product control is introduced.

The researcher still explicitly supplies:

- current prior second-epoch continuation-overlay path; and
- no-overwrite 40B destination.

The unchanged product persists overlay-v2 through public 40B.

Successful persistence leaves unchanged:

- mounted governed controller;
- mounted research session;
- mounted generic research re-entry;
- retained second-basis continuation; and
- immutable second-epoch launch provenance/current inspection state.

## Receipt correctness

40B persistence evidence now records the actual selected overlay format.

The existing 47F success receipt renders that exact value.

This removes the historical hardcoded-v1 assumption while preserving the old receipt
text for actual v1 writes.

## Repository Zero proof

Executable head:

`94d41a98210ff6e56668ad996ba9f3bdf14ce259`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50R changes only:

- public 40B third-basis overlay persistence/loading;
- the 47F success receipt's format reporting;
- focused application and Textual proof modules;
- this milestone record; and
- compact README continuity.

It does not change:

- public 40A;
- generic session re-entry-plan v1;
- first-root overlay formats;
- second-basis overlay formats;
- 37C/37D continuation formats;
- 47A–47E product semantics;
- third-basis launch lineage;
- CLI launch/inspection behavior;
- 40C/40D continuation formats;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50R proves only durable 40B restart configuration for a third-basis bare saved passage.

Do not infer:

- persisted relaunch from third-basis overlay-v2;
- 47G typed handoff from v2 persistence;
- 40C first continuation above v2-backed third-basis ancestry;
- 40D cumulative continuation above that ancestry;
- fourth-basis bare persistence;
- generic arbitrary-depth epoch/version codecs;
- automatic path discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The next researcher-action review should prove consumption of the persisted third-basis
overlay-v2 through the existing launch/product/inspection seams before touching 40C or
40D.

## Compact result

After 50R:

```text
three nested bare saved passages
→ unchanged public 40A third-basis reconstruction
→ proof-gated public 40B persistence
→ third-basis overlay-v2 only because the third-basis member vocabulary requires it
→ unchanged v1 for note-only histories
→ existing 47F product inherits persistence
```

Version expansion remains local to the durable boundary that actually owns the
expanded locator vocabulary.
