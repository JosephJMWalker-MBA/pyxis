# Milestone 50F — fresh-process root-backed re-entry with a bare saved passage

Decision: **D260**  
Issue: **#252**

## Concrete researcher action

50E proves in-process adoption of a changed basis containing one bare exact-range selection.

50F asks whether that governed session can be reconstructed after process loss from explicit durable locators only.

The required path is:

```text
ordinary-session durable re-entry inputs
+ exact-range-selection capture + selection locators
+ working_set.v2
+ working_set_note.v2
+ transition-v1
+ root-v1
+ first edge-v1
+ root-started sequence declaration-v1
→ existing 35B fresh re-entry
→ fresh governed controller
```

## Review result

No production seam was demonstrated.

Existing 35B delegates:

- the old session to established ordinary re-entry;
- appended working-set members to the established re-entry locator union;
- the changed basis/root to public 34A/34B-derived loaders;
- the root-started declaration to the established sequence declaration loader.

The member locator union already includes:

`ChromiumResearchExactRangeSelectionReentryLocator(capture_source, selection_source)`.

Therefore 50F is proof-only unless execution shows otherwise.

## Fresh identity semantics

50F deliberately does **not** require Python object identity across process reconstruction.

For the bare selection:

```text
original loaded member
is not
freshly reloaded member
```

while the following must remain exact:

- selected text;
- start/end offsets;
- source capture bundle SHA-256;
- durable selection-record SHA-256;
- changed working-set/note formats;
- root record identity;
- sequence declaration identity;
- declared endpoint edge identity;
- governed presentation semantics.

This is fresh reconstruction, not in-memory retention.

## Durable source requirement

Unlike 50E, the capture and bare-selection sidecars remain present because 35B must freshly reopen them.

The proof constructs a real persisted capture, creates and persists one exact-range selection, and supplies both paths explicitly through the existing exact-range-selection re-entry locator.

No browser is consulted.

## Expected version path

```text
fresh exact-range selection
→ research_working_set.v2
→ research_working_set_note.v2
→ transition-v1
→ root-v1
→ edge-v1
→ sequence declaration-v1
```

No new format is introduced.

## Presentation proof

After fresh re-entry, the reconstructed endpoint working set must contain the newly loaded bare-selection object.

The established governed working-set presentation must project that member as:

```text
member_kind = exact_range_selection
human_note_text = None
```

with the exact selected source text.

## Authority boundaries

35B continues to require every durable locator explicitly.

50F adds no:

- directory scan;
- digest search;
- path inference;
- browser reacquisition;
- automatic branch selection;
- current/latest/head semantics;
- source truth or citation authority.

## Stop boundary

50F proves existing 35B fresh-process root-backed re-entry only.

It does not automatically establish compatibility for later persisted restart-configuration products or second/third changed-basis epoch products. Those remain separate researcher-action reviews.

## Production-code result

If Repository Zero passes, 50F changes no production code.

That means the existing fresh-process re-entry architecture already composes the generalized member and changed-basis contracts earned by 49A and 50A–50E.

## Acceptance statement

50F permits only this statement:

> A root-backed governed session whose changed basis contains one bare saved exact-range selection can be reconstructed in a fresh process from explicit durable locators through existing 35B, producing a new loaded selection object with the same durable/source identities and equivalent governed presentation, without production-code or durable-format changes.
