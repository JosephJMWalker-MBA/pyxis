# Milestone 50M — persist bare selection as second-basis overlay-v2

Decision: **D267**  
Issue: **#264**

## Concrete researcher action

50L proves that one exact bare saved passage can cross a second changed evidence basis
and be freshly reconstructed through the existing 46E / public-37A boundary.

That proof intentionally stopped before persistence because strict 37B overlay-v1
still delegated appended-member encoding and decoding to the frozen original
three-kind locator codec.

The next concrete researcher action is:

> Persist that exact proven second-basis bare-selection reconstruction as explicit
> durable restart configuration without widening any upstream plan, transition, root,
> edge, continuation, or browser authority.

## Reuse review

The application layer did not require a new re-entry model.

Existing public 37A already uses:

`ChromiumResearchSecondBasisEpochReentryPlan`

whose `appended_working_set_members` field accepts the generalized working-set
member locator union, including:

`ChromiumResearchExactRangeSelectionReentryLocator`

Public 37B also already performs the correct proof-gated sequence:

```text
earned 37A reconstruction
+ explicit current prior-continuation overlay
+ explicit no-overwrite destination
→ rebuild exact candidate plan
→ fresh 37A reconstruction
→ compare prior continuation presentation and endpoint
→ compare retained first-root identity
→ compare second-root identity
→ compare second-basis governed presentation and endpoint
→ persist locator-only overlay
→ strict round-trip decode
```

The actual blocker was therefore confined to the second-basis document codec.

## Decision

Add one narrowly versioned second-basis overlay-v2.

Historical note-only persistence remains:

`pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1`

A typed second-basis plan containing at least one bare exact-range-selection locator
persists as:

`pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v2`

No public 37A plan or re-entry semantics change.

## Version selection remains typed

Persistence chooses v2 only when the exact typed plan contains a real:

`ChromiumResearchExactRangeSelectionReentryLocator`

It does not infer version from paths, filenames, prior overlay version, working-set
version, or serialized content.

Note-only appended-member vocabularies continue through the unchanged v1 encoder.

## Strict bare locator shape

Under overlay-v2, one bare selection member is encoded exactly as:

```json
{
  "kind": "exact_range_selection",
  "capture_source": "...",
  "selection_source": "..."
}
```

There is no `note_source`.

No selected text, note text, digest, timestamp, chronology, head marker, semantic
claim, authorship claim, or citation claim is copied into the locator overlay.

## Historical member shapes remain unchanged

Overlay-v2 delegates the three established note-bearing shapes to the frozen v1
member codec:

- paragraph note;
- exact-range note; and
- comparison note.

Thus v2 expands only the member vocabulary required by the new persisted action.

## Versioned loading remains strict

The second-basis overlay loader now dispatches explicitly on only:

- overlay-v1; or
- overlay-v2.

Overlay-v1 still rejects a bare member shape.

Overlay-v2 accepts the exact bare locator shape and otherwise delegates historical
member decoding unchanged.

The proof rejects:

- missing `selection_source`;
- extra `note_source`;
- cross-shaped bare members;
- unsupported member kinds; and
- unknown overlay versions.

No format guessing or migration occurs.

## Proof-gated persistence remains unchanged

50M does not weaken public 37B.

Before any v2 bytes are written, public 37B freshly reconstructs the exact candidate
through public 37A and rechecks:

- prior continuation governed presentation;
- prior continuation terminal durable edge;
- retained first-root identity;
- second-root identity;
- second-basis governed presentation; and
- second-basis terminal durable edge.

Tampered ancestry or second-root evidence therefore still fails before write.

The destination remains strict no-overwrite.

## Exact 50L crossing now persists

The focused proof starts from the same architectural boundary earned in 50L:

```text
first-root bare cumulative continuation
→ second bare saved passage
→ working-set/note v2
→ transition-v1
→ second root-v1
→ edge-v1
→ explicit 46D adoption
→ 46E / public-37A fresh reconstruction
```

That exact 46E verification is then supplied to existing 46F / public-37B.

Persistence succeeds as overlay-v2.

Strict loading of the written document reconstructs the exact existing 37A typed
plan, and mandatory fresh proof preserves both ancestry layers and the second-basis
governed endpoint.

## 46F product inheritance

No new 46F product branch is introduced.

The existing proof-gated 46F surface still asks only for:

- the explicit current prior 35D/35E continuation-overlay path; and
- one explicit no-overwrite 37B destination.

For a bare second-basis verification, the unchanged product now inherits the
application-layer v2 persistence selection.

Successful persistence does not replace:

- the mounted governed controller;
- the mounted research session;
- retained first-root continuation ancestry;
- research re-entry state; or
- launch provenance.

## Persisted format becomes explicit result evidence

Reuse review exposed a presentation defect that predated 50M.

First-root 35C had already gained overlay-v2 in 50H, but the 44G success receipt still
hardcoded overlay-v1.

The 46F receipt likewise hardcoded second-basis overlay-v1 and would become false as
soon as 50M persisted v2.

Both persistence-result types now expose the exact selected `overlay_format`.
Success receipts render that value rather than guessing or hardcoding a version.

The focused proof mechanically establishes:

- first-root bare 35C persistence reports overlay-v2 truthfully;
- second-basis bare 37B persistence reports overlay-v2 truthfully; and
- historical note-only persistence still reports overlay-v1.

No persistence semantics are changed by this reporting correction.

## Repository Zero proof

Executable head:

`0397f8fabc6b530a0c6dc082e1e27ca627aee94b`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50M changes only:

- second-basis 37B overlay encoding/decoding/version selection;
- explicit persisted-format evidence on the two already-versioned overlay result
  families;
- truthful 44G and 46F format receipts;
- focused application and Textual proof coverage;
- this milestone record; and
- compact README continuity.

It does not change:

- public 37A plan construction;
- public 37A fresh reconstruction;
- 44A changed-basis preparation;
- 46A transition persistence;
- 46B root persistence;
- 46C edge persistence;
- 46D adoption;
- 46E verification semantics;
- first-root overlay-v2 semantics;
- continuation overlay-v1;
- CLI dispatch;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50M proves only durable second-basis restart configuration.

It does **not** prove:

- relaunch from a second-basis overlay-v2;
- 46G handoff from a v2-backed second basis;
- second-basis continuation above v2 ancestry;
- second-basis cumulative continuation above v2 ancestry;
- third-basis bare persistence;
- a generic arbitrary-version locator codec;
- automatic locator discovery;
- current/latest/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

A fresh researcher-action review is required before treating a persisted second-basis
overlay-v2 as a launch input.

## Compact result

After 50M:

```text
first-root bare cumulative continuation
→ second bare saved passage
→ second changed basis
→ 46D adoption
→ 46E / 37A fresh proof
→ unchanged 46F persistence surface
→ typed 37B version selection
→ second-basis overlay-v2
→ strict round-trip decode
→ mandatory fresh 37A re-proof
→ mounted state and launch provenance unchanged
```

The new version exists only at the durable configuration boundary that actually owns
the expanded bare-selection member vocabulary.
