# Milestone 50K — prove cumulative 35E loop above bare-selection overlay-v2 anchor

Decision: **D265**  
Issue: **#260**

## Concrete researcher action

50J proves one ordinary continuation can be checkpointed and relaunched through the
existing 35D continuation overlay-v1 above a first-root bare-selection overlay-v2.

The next ordinary researcher action is:

> Make another governed continuation, checkpoint the cumulative post-root history,
> and relaunch that cumulative state without losing the bare saved passage or
> changing the direct first-root ancestry anchor.

## Reuse review

Existing 35E cumulative persistence already operates through the fixed-anchor
cumulative-extension kernel.

For the first-root family it performs:

```text
exact current 35D/35E overlay
→ strict 35D decode
→ fresh continuation re-entry
→ exact current/rollover reconciliation
→ append one explicit successor edge to cumulative edge tuple
→ persist cumulative edge declaration
→ construct next plan with unchanged direct 35C anchor
→ fresh next continuation re-entry
→ persist through existing 35D overlay writer
→ strict 35D round-trip
```

The 36C product shell delegates to that same public 35E boundary and explicitly
checks that the fixed 35C ancestry anchor does not change before promoting the
visible cumulative controller.

Neither boundary encodes the member vocabulary stored inside the referenced 35C
overlay.

Therefore the strongest hypothesis was:

```text
first-root 35C overlay-v2 ancestry
does not imply
35E or continuation overlay-v2
```

## Decision

50K is **proof-only**.

No production-code changes.

No durable-format changes.

The next cumulative continuation remains:

`pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1`

while its direct ancestry anchor remains the first-root 35C overlay-v2.

## Application crossing

The focused proof starts from the real 50J path:

```text
bare-selection first-root overlay-v2
→ fresh root-backed reconstruction
→ first ordinary continuation
→ 35D continuation overlay-v1
```

From that freshly reconstructed continuation it creates one second ordinary endpoint
revision and performs explicit 30A rollover.

The exact current 35D overlay, explicit successor edge, cumulative declaration
destination, and next-overlay destination are then supplied to public 35E.

## Fixed direct ancestry anchor

The next 35D/35E plan retains exactly:

`prior_root_backed_overlay_source == first-root overlay-v2 path`

It does not point to the previous continuation overlay.

The cumulative post-root edge tuple grows from one edge to two:

```text
first post-root edge
→ first successor

second cumulative checkpoint
→ first successor
→ second successor
```

No recursive continuation-overlay ancestry is introduced.

## Continuation overlay-v1 remains sufficient

The next durable document remains exactly the existing locator-only continuation
shape:

```json
{
  "format": "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1",
  "prior_root_backed_overlay_source": "...",
  "declared_edge_sources": ["...", "..."],
  "declaration_source": "..."
}
```

The proof rejects accidental duplication of changed-basis member details such as:

- `appended_working_set_members`;
- `exact_range_selection`;
- `capture_source`;
- `selection_source`;
- changed working-set/note sources; or
- root source.

The prior first-root overlay remains the owner of the changed-basis locator
vocabulary.

## Prior durable artifacts remain untouched

35E does not rewrite the prior continuation checkpoint.

The proof preserves exact bytes for:

- the current 35D continuation overlay; and
- the second one-hop rollover declaration.

The cumulative checkpoint writes only its caller-explicit new declaration and new
overlay destinations.

## Cumulative presentation semantics

A one-hop rollover and a cumulative declaration intentionally assign different
declared positions to the same terminal durable edge.

For the second post-root continuation:

```text
one-hop presentation terminal declared_position = 1
cumulative presentation terminal declared_position = 2
```

The initial 50K proof incorrectly compared those presentation member objects for
full equality. Repository Zero correctly rejected that assertion while 1,410 other
tests passed.

The proof was corrected without production changes.

50K now compares the intended invariants across the two representations:

- exact terminal durable edge identity; and
- exact terminal human-authored note wording.

The distinct declared positions are asserted explicitly rather than treated as a
defect.

## Bare saved passage survives cumulative reconstruction

Fresh 35E reconstruction still reaches the direct first-root overlay-v2 through the
unchanged 35D plan.

The reconstructed ancestry contains one real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

with exact selected text:

`"Bare"`

and no manufactured note object.

That same freshly loaded member remains present in the cumulative endpoint working
set.

Thus cumulative post-root declaration changes presentation context, not the
semantics of the retained bare saved passage.

## Existing 36C product inheritance

No Textual branch for overlay-v2 is added.

The existing cumulative product shell performs:

```text
fresh 35D/35E continuation
→ ordinary revision
→ explicit 30A rollover
→ lock revision
→ mount four blank 35E path fields
→ public 35E proof/persistence
→ verify fixed first-root anchor
→ replace one-hop controller with exact fresh cumulative controller
→ unlock next ordinary revision
```

A focused Textual test drives that real product flow above v2-backed ancestry.

The four checkpoint paths remain blank until the researcher explicitly supplies
them.

Successful promotion preserves the exact first-root overlay-v2 anchor and mounts the
two-edge cumulative presentation before revision becomes available again.

## Persisted cumulative relaunch

The newly written cumulative overlay-v1 is supplied to the existing command:

```text
pyxis research-shell --root-backed-continuation-overlay <overlay>
```

The CLI keeps the existing typed continuation lineage and product dispatch.

Fresh relaunch:

- reconstructs the direct first-root overlay-v2 ancestry;
- retains two declared continuation edges;
- preserves cumulative governed presentation; and
- retains the bare saved passage without note synthesis.

No version-specific CLI behavior is required.

## Read-only inspection inheritance

The same cumulative overlay is supplied twice to:

```text
pyxis research-inspect --root-backed-continuation-overlay <overlay>
```

The output is byte-identical across both runs and exactly equals the shared
continuation authority-inspection projection.

It remains:

`read_only_inspection_not_authority`

with launch family:

`persisted 35D/35E root-backed continuation launch`

and reports exactly two declared continuation edges.

No inspection format changes.

## Repository Zero proof

The initial proof head exposed one test-expectation defect:

```text
cumulative declared_position 2
!=
one-hop declared_position 1
```

All other 1,410 tests passed on that lane.

The assertion was narrowed to the established cumulative semantics with no
production-code change.

The corrected proof head then passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50K changes only:

- one focused cumulative proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- 35C persistence/loading;
- 35D persistence/loading;
- 35E cumulative persistence;
- the fixed-anchor cumulative kernel;
- the 36C Textual shell;
- CLI behavior;
- authority inspection;
- evidence formats; or
- any second-/third-epoch format.

## Explicit stop boundary

50K proves only cumulative ordinary continuation within the first-root epoch.

A fresh downstream review found a real separate serialization boundary at the
second changed-basis epoch:

`pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1`

still delegates appended-member encoding/decoding to the frozen original
three-kind locator codec.

Do not infer second-basis bare-selection persistence from 50K.

Also do not infer:

- third-basis bare-selection persistence;
- 31B plan-v2;
- automatic locator discovery;
- current/latest/head authority;
- browser highlighting or mutation;
- automatic adoption;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

## Compact result

After 50K, the bare-passage path is proven through a repeatable first-root
post-change cumulative workflow:

```text
bare saved passage
→ first-root overlay-v2
→ first 35D continuation-v1
→ fresh continuation relaunch
→ second ordinary revision
→ 30A rollover
→ unchanged 35E cumulative checkpoint
→ direct first-root overlay-v2 anchor retained
→ two-edge continuation overlay-v1
→ visible 36C cumulative promotion
→ process restart
→ existing cumulative continuation product
```

The v2 distinction remains confined to the configuration boundary that actually
owns the bare-selection member vocabulary.
