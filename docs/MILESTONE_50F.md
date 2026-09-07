# Milestone 50F — typed fresh-process re-entry for bare exact-range selections

Decision: **D260**  
Issue: **#248**

## Concrete researcher action

50E proves that one exact bare saved passage can move through the existing first changed-basis product surface and become part of the active governed session in-process.

The next existing researcher action is fresh-process root-backed re-entry through public 35B.

Before 50F, that action could reconstruct only appended 17D/18D/19D note-bearing member families because the shared 31A member-reentry locator seam had no representation for a durable 49A/49B bare selection.

## Demonstrated gap

The root-backed 35B plan stores appended members as typed working-set-member re-entry locators and reconstructs each by delegating to the shared 31A `_load_member(...)` boundary.

The shared union previously contained only:

```text
ChromiumResearchParagraphNoteReentryLocator
ChromiumResearchExactRangeNoteReentryLocator
ChromiumResearchComparisonNoteReentryLocator
```

A bare `exact_range_selection` therefore had no explicit fresh-process locator even though 49A/49B already defined all required durable evidence.

## Reuse decision

49B is the correct reconstruction primitive.

A durable bare selection needs only:

```text
explicit capture_source
+
explicit selection_source
→ public 16C capture load
→ public 49B exact selection relink
```

No selected text needs to be copied into the locator plan.

No new research-evidence format is needed.

## Typed locator

50F adds:

`ChromiumResearchExactRangeSelectionReentryLocator`

with exactly:

```text
capture_source: Path
selection_source: Path
```

The shared application-layer `ChromiumResearchWorkingSetMemberReentryLocator` union includes this typed locator.

Plan creation validates only that both values are Paths.

It does not read either file.

## Fresh member loading

The shared `_load_member(...)` dispatcher now handles the new locator by:

1. loading the explicit capture through public 16C;
2. loading/relinking the explicit durable selection through public 49B;
3. returning `ChromiumPageResearchLoadedParagraphTextSelectionRecord`.

This preserves the bare member as source evidence.

It does not synthesize a note, comment, citation, tag, or interpretation.

## 35B crossing

The focused 50F proof constructs one real first changed-basis lineage:

```text
ordinary governed session
+ persisted bare selection
→ working_set.v2 / working_set_note.v2 preparation
→ transition-v1
→ root-v1
→ first edge-v1
→ explicit 35A adoption
→ typed 35B fresh re-entry
```

The new process receives only explicit durable locators.

The appended member is freshly reloaded through public 16C + 49B.

The root loader then reconstructs the changed v2 working set from:

```text
fresh prior-session members
+
fresh bare appended member
```

and re-establishes the exact transition/root/declaration lineage.

## Identity and presentation

Fresh 35B application evidence is not required to preserve in-memory object identity from the old process.

Instead the proof requires durable identity and presentation equivalence.

The freshly loaded bare member must:

- be a `ChromiumPageResearchLoadedParagraphTextSelectionRecord`;
- derive selected text from the explicitly loaded capture;
- retain the exact supplied selection-sidecar verification path;
- remain note-free.

The fresh root-backed controller must match the adopted controller by:

- root record SHA-256;
- declaration record SHA-256;
- declared endpoint edge SHA-256;
- governed presentation.

The newly reconstructed changed working set remains v2 and contains the fresh bare member at the exact caller-declared position.

## Fail-closed attachment

A locator pairing the real selection sidecar with a different capture must fail at the public 49B source-identity attachment boundary.

A locator naming a different valid selection over the same capture may itself relink, but must fail when the reconstructed member no longer matches the durable changed working-set identity.

Thus:

```text
valid member file
!=
correct changed-basis member
```

## Ordinary governed continuation

After fresh 35B reconstruction, the returned existing controller can immediately perform the established ordinary endpoint-revision action.

The resulting edge retains the fresh changed working-set object, including the bare selection.

50F does not introduce a parallel controller or continuation path.

## Critical serialization boundary

50F changes the **typed application plan only**.

It does not widen the persisted 31B document:

`pyxis.chromium.research_session_reentry_locator_plan.v1`

31B explicitly established that the v1 document accepts exactly these member kinds:

```text
paragraph_note
exact_range_note
comparison_note
```

and rejects unknown kinds.

Therefore a typed 31A plan containing `ChromiumResearchExactRangeSelectionReentryLocator` remains intentionally unserializable through the v1 31B writer.

Likewise a manually authored v1 plan containing:

```json
{"kind": "exact_range_selection", ...}
```

still fails strict v1 decoding.

## 35C overlay remains closed

The root-backed overlay:

`pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1`

reuses the frozen 31B member encoder/decoder.

50F deliberately leaves that behavior unchanged.

A successful typed 35B re-entry containing the new locator cannot yet be checkpointed through the existing v1 overlay writer.

A manually authored v1 overlay containing `exact_range_selection` likewise fails strict decoding.

This is the explicit next serialization boundary, not an accidental omission.

## Why no plan/overlay v2 yet

Typed fresh re-entry is now a demonstrated researcher need.

The durable restart-document question is distinct.

A later review should determine:

- whether the 31B ordinary plan needs a v2 member vocabulary at all for this workflow;
- whether only the 35C root-backed overlay needs a v2;
- whether one shared tagged-locator vocabulary should govern both;
- compatibility expectations for older Pyxis readers;
- how CLI/Textual restart configuration should expose the new locator.

50F does not prejudge that design.

## Focused falsification

50F proves:

1. the typed bare-selection locator is path-only and performs no reads at plan creation;
2. the shared typed locator union accepts it;
3. fresh loading delegates to public 16C + 49B;
4. wrong capture attachment fails;
5. a wrong valid selection sidecar fails changed-working-set relinking;
6. a real 50E-style adopted session can be freshly reconstructed through 35B;
7. the fresh appended member remains a bare loaded exact-range selection;
8. selected text is derived from the explicitly supplied capture;
9. the fresh transition successor is working-set/note v2;
10. the bare member retains its exact declared position in the changed working set;
11. fresh root/declaration/endpoint identities match the adopted session;
12. governed presentation matches;
13. ordinary governed revision works immediately after fresh re-entry;
14. 31B v1 persistence rejects the new typed locator;
15. 31B v1 decoding rejects `exact_range_selection`;
16. 35C overlay-v1 persistence rejects the new typed locator;
17. 35C overlay-v1 decoding rejects `exact_range_selection`.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50F adds no:

- 31B plan v2;
- 31B v1 member-kind widening;
- 35C overlay v2;
- 35C v1 member-kind widening;
- CLI syntax;
- Textual restart form;
- new research-evidence format;
- selected-text persistence in locator configuration;
- source discovery;
- browser acquisition;
- fuzzy anchoring;
- automatic adoption;
- chronology/current/latest/head authority;
- citation or semantic-support authority.

## Acceptance statement

50F permits only this statement:

> A caller can freshly reconstruct a root-backed governed session whose changed evidence basis added one durable bare exact-range selection by supplying an explicit typed capture-plus-selection locator that reuses public 16C and 49B, while the existing strict 31B and 35C v1 locator documents remain closed to that new member kind.
