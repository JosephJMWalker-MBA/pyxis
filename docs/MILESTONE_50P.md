# Milestone 50P — prove cumulative 37D continuation above second-basis bare overlay-v2 ancestry

Decision: **D270**  
Issue: **#270**

## Concrete researcher action

50O proves that the first ordinary persisted continuation above a v2-backed
second-basis epoch remains an unchanged locator-only 37C overlay-v1.

The next ordinary researcher action is:

> Continue once more from that persisted 37C state, cumulatively checkpoint the
> longer post-second-root history, and prove that the direct 37B overlay-v2 anchor
> remains fixed rather than forcing recursive continuation overlays or another
> durable version.

## Reuse review

Existing public 37D already performs cumulative continuation extension through the
same typed 37C plan/document family.

Its concrete mechanics are:

```text
explicit current 37C overlay
→ strict 37C decode
→ fresh current 37C reconstruction
→ exact current-state match
→ exact rollover ownership check
→ cumulative edge-sequence relink from fixed 37B anchor
→ preserve current_plan.prior_second_basis_epoch_overlay_source
→ append one successor edge
→ persist with unchanged 37C writer
→ strict 37C round-trip decode
→ fresh cumulative reconstruction
```

The cumulative boundary never owns the member vocabulary of the second changed
basis.

Its direct ancestry pointer remains one explicit 37B overlay path.

Therefore the strongest hypothesis was:

```text
37B overlay-v2 fixed anchor
+ 37C overlay-v1 continuation
does not imply
37D or 37C overlay-v2
```

## Decision

50P is **proof-only**.

No production-code changes.

No 37C or 37D durable-format changes.

The existing:

`pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1`

remains sufficient for cumulative 37D extension above a second-basis 37B overlay-v2
anchor.

## Executable crossing

The focused proof starts from the complete nested bare-selection lineage:

```text
first-root bare saved passage
→ first-root overlay-v2
→ ordinary first-root continuation
→ cumulative first-root continuation
→ second bare saved passage
→ second changed basis
→ second root
→ explicit adoption
→ 46E / 37A proof
→ 46F / 37B overlay-v2
→ first ordinary post-second-root continuation
→ 37C overlay-v1
```

That persisted 37C continuation is freshly reconstructed.

From the fresh governed continuation, the proof creates one additional ordinary
endpoint revision and explicit rollover, then supplies that exact state to public
37D cumulative checkpoint extension.

## Direct 37B anchor remains fixed

The next cumulative plan preserves exactly:

`current_plan.prior_second_basis_epoch_overlay_source`

which is the original persisted 37B overlay-v2 path.

It does **not** replace that direct anchor with:

- the current 37C overlay;
- an intermediate cumulative overlay;
- a recursively nested continuation path; or
- any copied changed-basis member configuration.

Only the new successor edge is appended to the exact existing
`declared_edge_sources` tuple.

## Next durable overlay remains 37C-v1

37D persists the next cumulative state through the unchanged 37C writer.

The resulting document remains exactly:

```json
{
  "format": "pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1",
  "prior_second_basis_epoch_overlay_source": "...",
  "declared_edge_sources": ["...", "..."],
  "declaration_source": "..."
}
```

The proof rejects accidental duplication of:

- `appended_working_set_members`;
- `exact_range_selection`;
- `capture_source`;
- `selection_source`;
- changed working-set/note locators;
- transition locators; or
- root locators.

The expanded bare-selection vocabulary remains owned only by the directly referenced
37B overlay-v2.

## Prior durable artifacts remain immutable

Before cumulative persistence, the proof records the bytes of:

- the current 37C overlay; and
- the one-hop declaration produced for the newly chosen rollover.

After successful 37D persistence, both remain byte-for-byte unchanged.

The cumulative operation writes only:

- the new cumulative declaration; and
- the new no-overwrite 37C locator overlay.

## Both bare saved passages survive cumulative reconstruction

Strict round-trip decode of the next 37C-v1 document reconstructs its explicit
37B-v2 fixed anchor through the public version-aware loader.

The retained first-root ancestry still contains a real no-note:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

and the second changed-basis layer still contains a distinct real no-note loaded
selection record.

The second bare member remains present in the cumulative terminal working set.

No note object is manufactured for either saved passage.

## Root and terminal continuity

Fresh cumulative reconstruction retains:

- exact first-root identity;
- exact second-root identity; and
- exact chosen cumulative terminal edge identity.

The final cumulative controller presentation matches the explicitly chosen rollover
terminal state.

These digests remain record/content identity anchors only and do not establish
authorship, trusted time, chronology, semantic support, or citation authority.

## Existing cumulative Textual product inherits the proof

50P launches the established inspectable persisted second-basis continuation product
from the real 50O 37C path.

Before submission, all cumulative durable locator fields are blank.

The researcher explicitly supplies:

- current 37C overlay path;
- chosen successor edge path;
- cumulative declaration destination; and
- next overlay destination.

Successful public 37D checkpointing promotes the freshly proven cumulative controller
as current governed state.

It does **not** replace immutable persisted launch provenance.

The launch provenance object and original 37C launch-location context remain exact
while only current governed-state inspection advances.

No overlay-v2-specific product control is introduced.

## Persisted cumulative relaunch inheritance

No new CLI branch is required.

The next cumulative 37C-v1 path is supplied to:

```text
pyxis research-shell --second-basis-epoch-continuation-overlay <next-37C-v1>
```

The existing CLI reconstructs:

```text
next 37C-v1
→ fixed 37B-v2 anchor
→ public 37A second-epoch reconstruction
→ cumulative declared edge sequence
→ persisted continuation lineage
→ established second-basis continuation product
```

The fresh launch is not the previously retained in-process cumulative object.

No controller-only or initial second-basis fallback is needed.

## Read-only inspection inheritance

The same cumulative 37C-v1 path is supplied twice to:

```text
pyxis research-inspect --second-basis-epoch-continuation-overlay <next-37C-v1>
```

Both runs emit byte-identical deterministic JSON equal to the established shared
second-basis continuation authority-inspection projection.

The report remains:

`pyxis.chromium.research_second_basis_epoch_authority_inspection.v1`

with role:

`read_only_inspection_not_authority`

and launch family:

`persisted 37C/37D continuation launch`

The cumulative declared continuation edge count is exactly two in the focused proof.

The path remains launch-location context only.

## Fail-closed current and anchor reconstruction

The proof exercises both failure sides.

If the explicit current 37C overlay is tampered before 37D extension, public 37D
fails while freshly decoding/reconstructing current state and writes neither the
cumulative declaration nor the next overlay.

If the fixed referenced 37B overlay-v2 is tampered after a valid cumulative checkpoint
exists, the next 37C document itself still decodes as locator-only configuration, but
fresh authority reconstruction fails when the explicit fixed anchor is opened.

Thus:

```text
valid locator configuration
!=
freshly reconstructed research authority
```

remains mechanically enforced at both continuation layers.

## Repository Zero proof

Test-only head:

`cac87227b3d0cac7f3f32031042928cc6c700b95`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

with no production-code correction.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50P changes only:

- one focused cumulative second-basis proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- 37B persistence/loading;
- public 37A reconstruction;
- 37C persistence/loading;
- 37D cumulative extension;
- continuation formats;
- CLI implementation;
- second-basis product shells;
- authority inspection;
- evidence formats;
- third-basis products; or
- browser behavior.

## Explicit stop boundary

50P proves only cumulative 37D continuation reuse above the v2-backed second-basis
anchor.

Do not infer:

- third-basis bare persistence;
- third-basis bare relaunch;
- third-basis continuation above bare ancestry;
- arbitrary Nth-basis version propagation;
- automatic path discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The next researcher-action review should return to the concrete third changed-basis
boundary rather than abstracting successful nested version cases prematurely.

## Compact result

After 50P:

```text
first-root bare cumulative ancestry
→ second-basis bare 37B overlay-v2
→ first post-second-root 37C-v1
→ fresh persisted continuation
→ another governed endpoint revision
→ explicit rollover
→ unchanged public 37D cumulative extension
→ same fixed direct 37B-v2 anchor
→ next unchanged 37C-v1
→ fresh cumulative relaunch
→ established continuation product
```

Version expansion remains local to the durable boundary that actually owns the
expanded bare-selection member vocabulary.
