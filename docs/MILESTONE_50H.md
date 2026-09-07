# Milestone 50H — persist bare-selection root-backed restart overlay v2

Decision: **D262**  
Issue: **#254**

## Concrete researcher action

50F proves that public 35B can freshly reconstruct a first changed-basis governed
session whose appended evidence contains a bare exact-range selection.

50G exposes that proof through the existing 44F Textual workflow.

The next concrete researcher action is the already-established 44G/35C action:

> Save that exact proven root-backed locator configuration so the researcher does
> not have to manually re-enter every changed-basis locator on the next launch.

Before 50H, that action stopped at the durable serialization boundary.

## Demonstrated gap

The typed 35B locator vocabulary already includes:

`ChromiumResearchExactRangeSelectionReentryLocator`

with exactly:

```text
capture_source
selection_source
```

But the durable configuration formats remained intentionally frozen.

31B plan-v1 supports exactly:

```text
paragraph_note
exact_range_note
comparison_note
```

The first-root 35C overlay-v1 reused that same historical member encoder/decoder.

Second-epoch 37B and third-epoch 40B overlays also reuse the frozen 31B v1 member
codec.

Therefore widening that shared codec in place would silently change several
historical strict-format contracts.

## Decision

50H adds one new first-root overlay format:

`pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2`

No 31B plan-v2 is introduced.

No existing v1 format is widened.

No second- or third-epoch overlay is changed.

## Version selection

The existing public first-root 35C persistence function selects the durable overlay
format from the exact typed appended-member vocabulary.

```text
no ChromiumResearchExactRangeSelectionReentryLocator
→ existing root-backed overlay-v1

one or more ChromiumResearchExactRangeSelectionReentryLocator
→ root-backed overlay-v2
```

The prior ordinary session plan remains an unchanged 31B plan-v1 document in both
cases.

This is format selection, not authority selection.

## Overlay-v2 member vocabulary

Overlay-v2 supports exactly four appended member kinds:

```text
paragraph_note
exact_range_note
comparison_note
exact_range_selection
```

The first three delegate to the frozen v1 member encoder and decoder, preserving
their exact historical key shapes.

The new bare-selection member is:

```json
{
  "kind": "exact_range_selection",
  "capture_source": "...",
  "selection_source": "..."
}
```

It permits no `note_source`.

A bare saved passage therefore remains semantically distinct from a note-bearing
annotation even in restart configuration.

## Strict loading

The public root-backed overlay loader dispatches on the explicit top-level
`format` value.

```text
overlay-v1
→ frozen v1 member decoder

overlay-v2
→ v2 member decoder
   → exact_range_selection handled locally
   → historical note-bearing kinds delegated to v1 decoder
```

Unknown overlay versions reject.

Overlay-v1 containing `exact_range_selection` still rejects.

Overlay-v2 bare members reject when they:

- omit `selection_source`;
- add `note_source`;
- use an unsupported kind;
- otherwise violate the exact expected object shape.

Both versions produce the same established typed
`ChromiumResearchRootBackedSessionReentryPlan`.

## Proof-before-write remains unchanged

50H does not weaken the 35C checkpoint contract.

Public persistence still performs:

1. strict decode of the caller-supplied ordinary 31B plan-v1 document;
2. exact equality with the prior plan retained by the earned 35B result;
3. construction of one candidate typed root-backed locator plan;
4. fresh public 35B re-entry from those explicit locations;
5. exact governed-presentation comparison;
6. exact declared-endpoint durable identity comparison;
7. exact 34A root durable identity comparison;
8. no-overwrite persistence only after those checks pass;
9. strict round-trip loading of the written overlay;
10. exact typed-plan equality after round-trip.

The only new behavior is the selected durable member vocabulary.

## Configuration, not evidence

Overlay-v2 remains operational restart configuration.

Its bare member stores only locations.

It does not store:

- selected passage text;
- human note text;
- an evidence digest registry;
- trusted time;
- authorship;
- semantic support;
- citation authority;
- current/latest/head state;
- inferred paths;
- source discovery results.

The referenced artifacts must still earn authority through the existing public
load/relink/re-entry boundaries.

## Existing v1 behavior remains frozen

Focused proof confirms note-only first-root 35C persistence still emits:

`pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1`

and round-trips through the same public loader.

The private historical `_OVERLAY_FORMAT` alias remains pointed at v1 so existing
v1-focused tests/readers do not accidentally reinterpret the addition of v2 as a
mutation of the original format.

31B plan-v1 remains unchanged and still rejects the bare-selection member family.

## Public 44G inheritance

No 44G application wrapper or Textual shell change is required.

The existing product already supplies exactly:

```text
successful exact 44F proof
+ explicit ordinary 31B plan path
+ explicit no-overwrite overlay destination
→ public 35C persistence
```

Because version selection now lives inside the established public 35C persistence
boundary, the existing 44G UI inherits overlay-v2 automatically.

A focused Textual test drives the real bare-selection changed-basis path through:

```text
44A preparation
→ 44B transition
→ 44C root
→ 44D edge
→ 44E adoption
→ 44F bare-selection fresh re-entry proof
→ unchanged 44G overlay controls
→ root-backed overlay-v2
```

The mounted governed controller/session remain unchanged during persistence.

## Fail-closed proof

The 50H tests also prove the bare-selection v2 path preserves existing failures:

- a different valid ordinary prior plan rejects before write;
- a tampered root rejects during mandatory fresh reconstruction before write;
- an existing destination is never overwritten;
- malformed v2 member shapes reject;
- unknown overlay versions reject.

## Repository Zero proof

The implementation/test head passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

before this milestone record was added.

The documentation head must pass the same exact-head matrix before merge.

## Explicit stop boundary

50H closes only the first-root 35C restart-configuration gap.

Do not infer that bare-selection serialization has propagated to:

- second-basis-epoch 37B overlays;
- third-basis-epoch 40B overlays;
- 31B plan-v1;
- a hypothetical 31B plan-v2;
- browser highlighting;
- automatic path discovery;
- automatic adoption;
- global branch/head authority;
- search, tags, export, citation, or semantic interpretation.

Any later-epoch restart serialization must be justified by its own concrete
researcher action and ancestry semantics.

## Compact result

After 50H, the first changed-basis product can perform:

```text
saved exact passage without note
→ v2 working-set lineage
→ transition-v1
→ root-v1
→ edge-v1
→ explicit governed-session adoption
→ typed fresh 35B re-entry
→ 44F product verification
→ proof-gated 35C restart persistence
→ root-backed overlay-v2
→ strict round-trip typed plan
→ fresh public 35B reconstruction
```

without mutating the historical v1 configuration contracts or inventing note
semantics for the saved passage.
