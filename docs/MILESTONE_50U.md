# Milestone 50U — prove cumulative 40D continuation above third-basis bare overlay-v2 ancestry

Decision: **D275**  
Issue: **#280**

## Concrete researcher action

50T proves that the first ordinary persisted continuation above a v2-backed
third-basis epoch remains an unchanged locator-only 40C overlay-v1.

The next ordinary researcher action is:

> Continue once more from that persisted 40C state, cumulatively checkpoint the
> longer post-third-root history, and prove that the direct 40B overlay-v2 anchor
> remains fixed rather than forcing recursive continuation overlays or another
> durable version.

## Reuse review

Existing public 40D already performs cumulative continuation extension through the
same typed 40C plan/document family.

Its concrete mechanics are:

```text
explicit current 40C/40D overlay
→ strict 40C decode
→ fresh current 40C reconstruction
→ exact current-state match
→ exact rollover ownership check
→ cumulative edge-sequence relink from fixed 40B anchor
→ preserve current_plan.prior_third_basis_epoch_overlay_source
→ append one successor edge
→ persist with unchanged 40C writer
→ strict 40C round-trip decode
→ fresh cumulative reconstruction
```

The cumulative boundary never owns the member vocabulary of the third changed basis.

Its direct ancestry pointer remains one explicit 40B overlay path.

Therefore the strongest hypothesis was:

```text
40B overlay-v2 fixed anchor
+ 40C overlay-v1 continuation
does not imply
40D or 40C overlay-v2
```

## Decision

50U is **proof-only**.

No production-code changes.

No 40C or 40D durable-format changes.

The existing:

`pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1`

remains sufficient for cumulative 40D extension above a third-basis 40B overlay-v2
anchor.

## Executable crossing

The focused proof starts from the complete nested three-bare lineage:

```text
first-root bare saved passage
→ first-root overlay-v2
→ first-root ordinary continuation
→ first-root cumulative continuation
→ second-basis bare saved passage
→ second-basis 37B overlay-v2
→ second-epoch ordinary 37C-v1 continuation
→ second-epoch cumulative 37D / 37C-v1
→ third bare saved passage
→ third-basis 40B overlay-v2
→ persisted third-basis relaunch
→ first ordinary 40C-v1 continuation
```

That persisted 40C continuation is freshly reconstructed.

From the fresh governed continuation, the proof creates one additional ordinary
endpoint revision and explicit rollover, then supplies that exact state to public
40D cumulative checkpoint extension.

## Direct 40B anchor remains fixed

The next cumulative plan preserves exactly:

`current_plan.prior_third_basis_epoch_overlay_source`

which is the original persisted 40B overlay-v2 path.

It does **not** replace that direct anchor with:

- the current 40C overlay;
- an intermediate cumulative overlay;
- a recursively nested continuation path; or
- any copied changed-basis member configuration.

Only the new successor edge is appended to the exact existing
`declared_edge_sources` tuple.

## Next durable overlay remains 40C-v1

40D persists the next cumulative state through the unchanged 40C writer.

The resulting document remains exactly:

```json
{
  "format": "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1",
  "prior_third_basis_epoch_overlay_source": "...",
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
40B overlay-v2.

## Prior durable artifacts remain immutable

Before cumulative persistence, the proof records the bytes of:

- the current 40C overlay; and
- the one-hop declaration produced for the newly chosen rollover.

After successful 40D persistence, both remain byte-for-byte unchanged.

The cumulative operation writes only:

- the new cumulative declaration; and
- the new no-overwrite 40C locator overlay.

## All three bare saved passages survive cumulative reconstruction

Strict round-trip decode of the next 40C-v1 document reconstructs its explicit
40B-v2 fixed anchor through the public version-aware loader.

The first-root ancestry still contains a real no-note loaded exact selection.

The second-basis ancestry still contains a distinct real no-note loaded exact
selection.

The third-basis layer still contains its own real no-note loaded exact selection.

The third bare object remains retained by the final cumulative continuation endpoint
working set.

No note object is manufactured for any saved passage.

## Root and terminal continuity

Fresh cumulative reconstruction retains:

- exact first-root identity;
- exact second-root identity;
- exact third-root identity; and
- exact chosen cumulative terminal edge identity.

The final cumulative controller endpoint matches the explicitly chosen rollover.

These digests remain record/content identity anchors only and do not establish
authorship, trusted time, chronology, semantic support, or citation authority.

## Existing cumulative Textual product inherits the proof

50U launches the established inspectable persisted third-basis continuation product
from the real 50T 40C path.

Before submission, all cumulative durable locator fields are blank.

The researcher explicitly supplies:

- current 40C overlay path;
- chosen successor edge path;
- cumulative declaration destination; and
- next overlay destination.

Successful public 40D checkpointing promotes the freshly proven cumulative controller
as current governed state.

It does **not** replace immutable persisted launch provenance.

The launch-provenance object and original 40C launch-location context remain exact
while only current governed-state inspection advances.

No overlay-v2-specific product control is introduced.

## Persisted cumulative relaunch inheritance

No new CLI branch is required.

The next cumulative 40C-v1 path is supplied to:

```text
pyxis research-shell --third-basis-epoch-continuation-overlay <next-40C-v1>
```

The existing CLI reconstructs:

```text
next 40C-v1
→ fixed 40B-v2 anchor
→ public 40A third-epoch reconstruction
→ cumulative declared edge sequence
→ persisted continuation lineage
→ established third-basis continuation product
```

The fresh launch is not the previously retained in-process cumulative object.

No older product-family fallback is needed.

## Read-only inspection inheritance

The same cumulative 40C-v1 path is supplied twice to:

```text
pyxis research-inspect --third-basis-epoch-continuation-overlay <next-40C-v1>
```

Both runs emit byte-identical deterministic JSON equal to the established shared
third-basis continuation authority-inspection projection.

The report remains:

`pyxis.chromium.research_third_basis_epoch_authority_inspection.v1`

with role:

`read_only_inspection_not_authority`

and launch family:

`persisted 40C/40D continuation launch`

The cumulative declared continuation edge count is exactly two in the focused proof.

The path remains launch-location context only.

## Fail-closed current and anchor reconstruction

The proof exercises both failure sides.

If the explicit current 40C overlay is tampered before 40D extension, public 40D
fails while freshly decoding/reconstructing current state and writes neither the
cumulative declaration nor the next overlay.

If the fixed referenced 40B overlay-v2 is tampered after a valid cumulative checkpoint
exists, the next 40C document itself still decodes as locator-only configuration, but
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

`73abe7e51c9f9b0fc0acfe5598dd85be364e13ab`

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

50U changes only:

- one focused cumulative third-basis proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- public 40A;
- public 40B v1/v2;
- public 40C persistence/loading;
- public 40D production implementation;
- 41A lineage;
- CLI implementation;
- third-basis product shells;
- authority inspection;
- first-/second-basis formats;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50U proves only cumulative 40D continuation reuse above the v2-backed third-basis
anchor.

Do not infer:

- 47G in-process handoff compatibility with v2 47F persistence;
- fourth-basis bare persistence;
- fourth-basis relaunch;
- fourth-basis continuation above bare ancestry;
- arbitrary Nth-basis version propagation;
- automatic path discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The next researcher-action review should return to a concrete user action rather than
extend the version pattern automatically.

## Compact result

After 50U:

```text
three-bare third-basis 40B overlay-v2
→ first post-third-root 40C-v1
→ fresh persisted continuation
→ another governed endpoint revision
→ explicit rollover
→ unchanged public 40D cumulative extension
→ same fixed direct 40B-v2 anchor
→ next unchanged 40C-v1
→ fresh cumulative relaunch
→ established continuation product
```

Version expansion remains local to the durable boundary that actually owns the
expanded locator vocabulary.
