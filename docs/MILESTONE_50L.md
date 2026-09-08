# Milestone 50L — prove bare selection through second-basis 46E / 37A

Decision: **D266**  
Issue: **#262**

## Concrete researcher action

50K proves that a bare saved passage can survive the cumulative first-root continuation
loop while the direct first-root overlay-v2 remains the fixed ancestry anchor.

The next concrete researcher action is:

> Start a second changed evidence basis with another bare saved passage, explicitly
> adopt the second-root session, and prove that exact second-basis session can be
> freshly reconstructed through the existing 46E / public-37A product flow.

## Reuse review

The application-layer second-basis path was already structurally ready.

Existing public boundaries already provide:

```text
44A changed-basis preparation
→ working-set/note v1 or v2 pair selection
→ 46A / public 33B transition-v1
→ 46B / public 34A root-v1
→ 46C ordinary edge-v1
→ 46D explicit second-basis adoption
→ 46E / public 37A fresh reconstruction
```

Public 37A already accepts the generalized
`ChromiumResearchWorkingSetMemberReentryLocator` union, and the existing member
loader already understands
`ChromiumResearchExactRangeSelectionReentryLocator`.

The actual gap was narrower: the 46E Textual surface still assumed every
non-comparison member had a note.

## Decision

Widen only the 46E product-verification surface for one bare exact-range selection.

Production changes are limited to:

- `chromium_research_second_changed_basis_epoch_reentry_textual.py`; and
- `second_changed_basis_epoch_reentry_research_session_shell.py`.

No application re-entry, transition, root, edge, adoption, or durable persistence
format changes are introduced.

## Bare member presentation

The established 46E member classifier now recognizes a loaded bare
`ChromiumPageResearchLoadedParagraphTextSelectionRecord`.

Its visible summary states:

`Human note: none attached — saved source passage only`

It does not render `None` as authored note text.

Historical note-bearing paragraph, exact-range-note, and comparison members retain
their existing presentation and fields.

## Bare locator collection

For a bare exact-range selection, 46E now collects exactly:

```text
capture_source
selection_source
```

It does not mount or require `note_source`.

Those two explicit paths construct the already-established application-layer:

`ChromiumResearchExactRangeSelectionReentryLocator`

No new locator type or member-loading implementation is added.

## Application crossing

The focused proof starts from a real persisted first-root cumulative continuation
whose ancestry already contains a bare saved passage.

From that continuation it performs the existing second changed-basis sequence:

```text
bare second-basis candidate
→ 44A working-set-v2 / working-set-note-v2
→ 46A transition-v1
→ 46B root-v1
→ 46C ordinary edge-v1
→ 46D explicit governed-session adoption
```

The exact second-basis candidate remains the loaded bare selection object through
preparation and adoption.

## Direct 37A reconstruction proves the application layer

Before relying on the Textual submit path, the focused proof calls the existing
public 46E application boundary directly with the exact bare locator.

Fresh reconstruction succeeds and yields one real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

with selected text:

`"Bare"`

and no manufactured `.note` attribute.

That direct proof mechanically separates application correctness from UI event
handling.

## 46E Textual product proof

The real 46E form mounts only after exact 46D adoption.

All locator fields begin blank.

The proof first intentionally omits `selection_source` and verifies that UI
validation fails before application verification with:

`appended bare selection member 0 requires capture and selection paths`

The form remains unlocked.

After the explicit selection-sidecar path is supplied, the same 46E product path
successfully delegates to public 37A and receives the exact fresh reconstruction.

The fresh controller:

- is a new reconstruction object;
- matches the exact 46D governed presentation;
- retains the exact second root;
- retains the exact 46D declaration;
- retains the exact endpoint edge;
- retains the fresh first-root continuation ancestry; and
- contains the bare second-basis selection without note synthesis.

## Mounted authority remains unchanged

46E remains a proof surface.

Successful fresh reconstruction does not replace:

- the currently mounted adopted controller;
- the mounted research session;
- retained first-root continuation ancestry; or
- launch provenance.

The successful form locks only after the exact 46E proof succeeds.

## Test-harness correction

The first full Repository Zero run exposed a test synchronization defect rather than
a product defect.

The direct application call succeeded, but the test immediately retried the 46E
Textual button after the intentional validation failure. Textual keeps a pressed
button in its transient `-active` state during the visual press cycle, and a second
activation during that state can be ignored.

The test was corrected to wait for the real button to become activatable again
before submitting the completed locator fields, and then to wait on the actual 46E
proof state rather than assuming one scheduler turn is sufficient.

No production semantics were changed for this correction.

## 46F / 37B remains deliberately closed

50L does not widen second-basis persistence.

After successful 46E fresh reconstruction, the focused proof supplies that result to
the existing 46F / public-37B persistence boundary.

The strict second-basis overlay-v1 member codec rejects the bare locator as an
unsupported member locator.

The destination is asserted not to exist after rejection.

Therefore:

```text
46E / 37A bare fresh reconstruction
does not imply
46F / 37B bare durable serialization
```

No second-basis overlay-v2 is introduced in 50L.

## Repository Zero proof

The final executable 50L proof head passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50L changes only:

- the existing 46E Textual member presentation;
- the existing 46E locator collector;
- one focused second-basis bare-selection proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- public 37A application reconstruction;
- 44A preparation;
- 46A transition persistence;
- 46B root persistence;
- 46C edge persistence;
- 46D adoption;
- 46F / 37B persistence;
- any durable format;
- first-root overlay-v2;
- continuation overlay-v1;
- CLI dispatch;
- inspection authority;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50L proves only fresh-process reconstructability of a bare selection through the
second-basis 46E / 37A product boundary.

Do not infer:

- 37B durable bare-selection serialization;
- successful 46F persistence for bare selections;
- second-basis persisted relaunch;
- second-basis cumulative continuation;
- third-basis bare-selection support;
- automatic locator discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The next researcher-action review must decide whether the proven second-basis
reconstruction earns a versioned persistence boundary, or whether a narrower
downstream action should be proven first.

## Compact result

After 50L, the bare-passage path crosses a second changed evidence basis through
fresh reconstruction without widening persistence:

```text
first-root bare cumulative continuation
→ second bare saved passage
→ working-set/note v2
→ transition-v1
→ second root-v1
→ edge-v1
→ explicit 46D adoption
→ 46E bare locator form
→ existing public 37A fresh reconstruction
→ exact second-basis governed presentation recovered
→ bare selection retained with no manufactured note
→ 46F / 37B overlay-v1 still fails closed
```

The version distinction remains confined to the boundary that actually owns the
changed member vocabulary.
