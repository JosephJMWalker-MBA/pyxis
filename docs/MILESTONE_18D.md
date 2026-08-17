# Milestone 18D — Verified Exact-Range Note Relinking

## Product question

Can one durable 18C exact-range human note re-enter the typed Pyxis application layer only when its persisted source reference and text coordinates can be re-established against one explicit caller-supplied loaded capture?

18D answers **yes** through one narrow relinking boundary.

## Why this milestone exists

18C deliberately separated file integrity from source-range validity.

A sidecar may be canonical, internally self-consistent, and protected by a matching SHA-256 while still recording coordinates that do not address the supplied source. The strongest 18C falsifiability test proves exactly that: a sidecar rewritten to `end_offset=999` with a recomputed digest remains file-valid.

That result is not a defect. It establishes the authority limit of file-only verification.

18D adds the missing explicit relationship check:

```text
caller-supplied 16C loaded capture
+ caller-supplied 18C sidecar path
    ↓
fresh 18C sidecar verification
    ↓
exact capture format + bundle SHA-256 match
    ↓
existing public 17A paragraph selection
    ↓
existing public 18A exact text-range selection
    ↓
existing public 18B note creation
    ↓
verified sidecar evidence + reconstructed typed human note
```

## Public API

```python
load_chromium_research_paragraph_text_selection_note(
    source,
    note_source,
)
```

returns:

```python
ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord(
    verification=<fresh 18C sidecar verification evidence>,
    note=<newly reconstructed 18B note record>,
)
```

Source-reference mismatch raises:

```python
ChromiumResearchParagraphTextSelectionNoteSourceMismatchError
```

## Fresh sidecar verification is mandatory

18D accepts a sidecar **path**, not a caller-created verification dataclass.

It always calls:

```python
verify_chromium_research_paragraph_text_selection_note(note_source)
```

before attempting relinking.

This means malformed bytes, digest mismatch, noncanonical encoding, unsupported sidecar modes, or invalid persisted coordinate shape remain owned by 18C verification.

18D does not create a second file-integrity boundary.

## Source capture is explicit

The caller supplies one exact:

```python
ChromiumPageResearchLoadedCaptureEvidence
```

18D does not search for a capture by:

- source path;
- note path;
- URL;
- bundle digest;
- browser state;
- page title;
- paragraph text;
- any index or registry.

The supplied capture is the only candidate source.

## Durable content identity must match

Before any selection is reconstructed, 18D compares the sidecar's verified durable source identity with the exact 16B verification evidence retained by the caller-supplied 16C capture:

```text
capture format
+
bundle SHA-256
```

The capture format must be the established:

```text
pyxis.chromium.research_capture.v1
```

The bundle digest must be valid lowercase SHA-256 and must exactly match the sidecar reference.

A different bundle is rejected before paragraph/range/note reconstruction.

## Path remains location, not identity

Source path is not part of the durable attachment identity.

A supplied loaded capture whose retained content identity matches may relink even when its `verification.path` differs from the path present when the original note was created.

This preserves the rule established by 17C/17D and 18C:

```text
filesystem path ≠ source-content identity
```

## Coordinate validity is re-established, not trusted

After source-content identity matches, 18D reconstructs the human action through the existing public boundaries.

First:

```python
select_chromium_research_capture_paragraph(
    source,
    paragraph_ordinal=verification.paragraph_ordinal,
)
```

This re-establishes the 17A paragraph relationship against the exact supplied loaded capture and its already-returned bounded paragraph tuple.

Then:

```python
select_chromium_research_paragraph_text(
    paragraph_selection,
    start_offset=verification.start_offset,
    end_offset=verification.end_offset,
)
```

This re-establishes the 18A coordinate relationship against the exact returned paragraph text prefix.

Only after both succeed does 18D call:

```python
create_chromium_research_paragraph_text_selection_note(
    text_selection,
    note_text=verification.note_text,
)
```

This reconstructs the 18B note through the established note/range validity boundary.

18D does not manually instantiate 17A, 18A, or 18B records.

## The `end_offset=999` proof

18C intentionally proved that this transformation is possible:

```text
valid sidecar
    ↓
rewrite end_offset: 4 → 999
    ↓
recompute SHA-256
    ↓
write canonical JSON
    ↓
18C verification succeeds
```

18D uses that same fact as its strongest acceptance test.

The self-consistent sidecar first passes 18C verification. Then 18D receives the explicit matching loaded capture and attempts reconstruction.

The existing 18A selector rejects `end_offset=999` because the coordinate is outside the paragraph's returned source evidence.

Therefore:

```text
file integrity
≠
source-range validity
```

and:

```text
source-content reference match
+
18A coordinate reconstruction
=
re-established attachment coherence
```

No new cryptographic or semantic claim is introduced.

## Bounded evidence remains bounded

18D cannot use a durable note to recover evidence that was not returned by the supplied capture.

If a sidecar references paragraph ordinal 2 but the supplied loaded capture retains only paragraph 1 in a collection-truncated returned prefix, the existing 17A operation rejects the relink.

Likewise, an 18C coordinate cannot address a paragraph suffix outside the already-returned `text_prefix` merely because a larger complete character count says more text existed.

18D does not:

- reopen the capture file;
- reacquire Chromium;
- enlarge observation limits;
- search source text;
- reconstruct omitted browser evidence;
- infer missing characters.

## Fresh runtime object identity

Python object identity does not survive persistence.

18D reconstructs a new runtime object chain:

```text
exact caller-supplied 16C loaded capture
    ↓
new 17A paragraph selection
    ↓
new 18A text-range selection
    ↓
new 18B note record
```

The reconstructed 17A selection retains:

- the exact caller-supplied loaded-capture object;
- the exact already-existing paragraph object inside that source.

The reconstructed 18A selection retains that newly reconstructed 17A object and derives `selected_text` from the source paragraph at the verified coordinates.

The reconstructed 18B note retains that newly reconstructed 18A object and the exact persisted caller text.

18D does not pretend the pre-persistence Python objects survived.

## What successful relinking proves

Successful 18D relinking proves only that:

1. the sidecar passed fresh 18C file verification;
2. its durable capture format + bundle digest match the caller-supplied loaded capture's retained 16B identity;
3. its paragraph ordinal can be reconstructed through 17A against the supplied bounded evidence;
4. its exact Unicode range can be reconstructed through 18A against the supplied returned paragraph text;
5. its human note can be reconstructed through 18B with exact persisted text.

That is **attachment coherence**.

It is not:

- source authentication;
- note authorship authentication;
- chain of custody;
- trusted observation time;
- verified quotation evidence;
- citation stability;
- claim support;
- relevance;
- truth;
- source provenance verification;
- semantic interpretation.

## Tests

Seven focused tests prove:

1. a verified 18C sidecar relinks to the exact supplied capture, exact existing paragraph, reconstructed exact range, derived selected text, and verbatim human note;
2. source filesystem path does not control durable identity;
3. a different capture bundle digest is rejected;
4. an unsupported supplied capture format is rejected before reconstruction;
5. sidecar bytes are freshly re-verified rather than trusted from shape alone;
6. a recomputed-digest `end_offset=999` sidecar passes 18C verification but is rejected during 18A reconstruction;
7. a sidecar cannot expand a supplied collection-truncated paragraph prefix;
8. the new loader is available through the public `pyxis.app` surface.

The mismatch-format assertions share one focused test, so the milestone adds seven test functions rather than inflating test count artificially.

## Validation

Behavior/public API proof:

- Actions #623 on `a89ce2dbeb26dcbb49d158bfc3b9d6496587db10` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.14 checked out exact head `a89ce2dbeb26dcbb49d158bfc3b9d6496587db10`;
- **318 tests collected / 318 passed in 27.42s**;
- all seven focused 18D tests passed alongside the complete established Repository Zero/browser/capture/selection/note/durability suite.

## Explicit non-goals

18D adds no:

- automatic source-capture discovery;
- source capture file read or rehydration;
- browser acquisition or control;
- sidecar persistence changes;
- source-text persistence;
- text search or fuzzy matching;
- coordinate repair;
- quotation/citation verification;
- source authentication;
- author identity;
- timestamp or trusted temporal provenance;
- HMAC/signatures;
- chain-of-custody system;
- note editing/delete/history;
- multi-note or notebook abstraction;
- generic annotation/selection registry;
- multi-range selection;
- capture index/search;
- tags/questions/claims;
- relevance/truth/confidence/support scoring;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

## Decision — D138

**One durable 18C exact-range note sidecar may re-enter the typed application layer only against one explicit caller-supplied 16C loaded capture. Relinking must freshly verify the sidecar from its file path, require its source capture format + bundle SHA-256 to match the exact 16B verification identity retained by the supplied capture, and then reconstruct the human action through the existing public 17A paragraph-selection, 18A exact-text-selection, and 18B note-creation boundaries. Persisted coordinates are not source-valid merely because the 18C sidecar is canonical and checksum-valid; 18A must re-establish that the zero-based half-open Unicode range addresses the supplied paragraph's already-returned text evidence, and any bounded/unreturned evidence remains unavailable. The reconstructed chain must retain the exact caller-supplied loaded-capture object and exact existing paragraph object while creating fresh 17A/18A/18B runtime objects. Source path remains location rather than attachment identity. Successful relinking proves attachment coherence only; it does not authenticate either artifact or human author, verify source provenance, establish chain of custody or trusted time, prove truth or claim support, or promote the selected range into verified quotation/citation evidence.**
