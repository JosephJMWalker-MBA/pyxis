# Milestone 18C — Durable Exact-Range Note Sidecar

## Product question

Can one exact 18B human-authored text-range note become durable without copying selected source text, recursively serializing the loaded capture, pretending Python object identity survives a process boundary, or turning a checksum into proof that the persisted coordinates still address a source the verifier did not read?

18C answers **yes** through one deterministic no-overwrite sidecar format.

## Why this milestone exists

18A and 18B established a finer-grained human research path:

```text
verified durable capture
    ↓
explicit paragraph selection
    ↓
explicit Unicode text range
    ↓
verbatim human note
```

The exact range note was still only an in-memory object. A researcher could precisely record which already-returned characters mattered and why, but that human work would disappear with the process.

Persisting the complete 18B object graph would be the wrong solution. It would duplicate the loaded source capture, paragraph evidence, and selected source text merely to preserve one human action.

The source is already durable under 16B. The paragraph/range choice can be represented durably by explicit coordinates. 18C therefore persists **durable source identity + layered human selection identity + exact human text**, not another source copy.

## Boundary

```text
ChromiumPageResearchParagraphTextSelectionNoteRecord
    ↓
re-establish live 18B / 18A validity
    ↓
source capture format + bundle SHA-256
+ paragraph selection mode + ordinal
+ text selection mode + Unicode offset unit
+ start_offset + end_offset
+ exact note mode + verbatim note text
    ↓
canonical deterministic JSON
    ↓
SHA-256 over complete durable reference + human action
    ↓
exclusive-create caller-chosen sidecar
```

Public API:

```python
persist_chromium_research_paragraph_text_selection_note(
    note,
    destination,
)

verify_chromium_research_paragraph_text_selection_note(source)
```

Persistence result:

```python
ChromiumPageResearchParagraphTextSelectionNotePersistenceEvidence(
    path=...,
    note_format="pyxis.chromium.research_paragraph_text_selection_note.v1",
    note_record_sha256=...,
    byte_count=...,
    note=<exact supplied 18B note object>,
)
```

Verification exposes the exact persisted source-reference, paragraph/range coordinates, note fields, digest, byte count, and canonical document text.

## Durable identity follows the authority chain

18B retains exact Python object identity while the process is alive:

```text
exact 16C loaded capture object
    ↓
exact 17A paragraph-selection object
    ↓
exact 18A range-selection object
    ↓
exact 18B note object
```

That identity cannot truthfully survive persistence.

18C changes the identity mechanism explicitly at the process boundary:

```text
in memory
exact object identity

on disk
capture content identity
+ paragraph ordinal
+ exact Unicode coordinates
+ explicit selection modes
```

The durable source identity is still the established 16B pair:

```text
capture format: pyxis.chromium.research_capture.v1
bundle SHA-256: <64 lowercase hex characters>
```

The exact human selection is then layered on top:

```text
paragraph:
    mode = caller_explicit_returned_paragraph_ordinal
    ordinal = <positive integer>

text_range:
    mode = caller_explicit_returned_paragraph_text_range
    offset_unit = unicode_code_point
    start_offset = <non-negative integer>
    end_offset = <integer greater than start_offset>
```

That is enough information for a future explicit relinking operation to reconstruct the existing 17A → 18A → 18B chain against a caller-supplied matching capture.

## Selected source text is deliberately absent

18C does **not** persist `selection.selected_text`.

Selected text remains derived source evidence owned by the source paragraph:

```text
paragraph.text_prefix[start_offset:end_offset]
```

The sidecar therefore does not contain:

- selected source text;
- paragraph text;
- paragraph element ID;
- page URL;
- Chromium endpoint;
- target ID;
- page title/body text;
- headings, links, metadata, tables, or lists;
- the complete 16A bundle;
- the 16B capture document;
- the 16C loaded-capture object graph;
- the source capture filesystem path.

A focused test persists a range selecting `😀B ` from `A😀B café` and proves neither the complete paragraph nor the selected substring appears in the sidecar.

## Source path is still location, not identity

The source capture path is intentionally absent.

A source file may move without its verified content identity changing. A different file may later occupy the same path. Persisting the path would therefore confuse location with source identity.

18C stores only the capture format + bundle SHA-256 and the human selection coordinates.

Future relinking must receive an explicit loaded capture and compare its retained durable content identity with the sidecar. 18C does not discover a capture automatically.

## Live persistence reuses existing authority

`persist_chromium_research_paragraph_text_selection_note()` does not manually reconstruct 18A/18B validation rules.

Before writing, it calls the established 18B constructor with the exact retained selection and note text:

```python
create_chromium_research_paragraph_text_selection_note(
    note.selection,
    note_text=note.note_text,
)
```

18B in turn delegates range validity to 18A.

That means persistence re-establishes:

- the exact 17A paragraph object identity;
- the established text-selection mode;
- Unicode code-point coordinate semantics;
- zero-based half-open range semantics;
- returned-prefix bounds;
- truncated/unreturned suffix refusal;
- nonblank exact caller-authored note text.

The temporary validation record is not substituted into persistence evidence. The returned persistence evidence still retains the exact caller-supplied 18B note object.

Persistence separately checks the retained source capture format and bundle-SHA shape because those facts become the durable source reference.

## Deterministic no-overwrite file contract

The format is:

```text
pyxis.chromium.research_paragraph_text_selection_note.v1
```

The complete durable reference + human action is canonical JSON using:

- UTF-8;
- direct Unicode;
- sorted object keys;
- compact separators;
- no NaN/Infinity values;
- one final newline on the complete document.

The caller chooses the destination. Its parent directory must already exist. Existing files are never overwritten.

The same exact source reference, range coordinates, and human note therefore produce the same `note_record_sha256` regardless of filesystem destination.

## SHA-256 remains self-integrity only

The digest covers:

```text
source capture content reference
+ paragraph selection identity
+ exact text-range coordinates
+ note mode
+ verbatim human note text
```

It detects ordinary mutation when the recorded digest is not changed.

It does **not** authenticate the human, source, or coordinates against some external authority. An actor able to rewrite both payload and digest can create another self-consistent sidecar.

18C demonstrates that limitation more strongly than 17C did.

A focused test changes:

```text
end_offset: 4 → 999
```

and also changes the note text, recomputes the digest, rewrites canonical bytes, and proves file-only verification succeeds.

That is intentional.

The verifier did not read the source capture. It therefore has no authority to claim that offset 999 addresses returned source evidence.

A future relinking boundary must re-establish that relationship against an explicit caller-supplied capture.

## File-only verification has a narrow job

`verify_chromium_research_paragraph_text_selection_note()` reads only the sidecar.

It validates:

- valid UTF-8 and JSON;
- exact top-level/nested field sets;
- supported exact-range-note format;
- supported source-capture format;
- source bundle SHA-256 shape;
- established paragraph selection mode;
- positive paragraph ordinal;
- established text-selection mode;
- `unicode_code_point` offset unit;
- non-negative integer start offset;
- integer end offset greater than start;
- established note mode;
- nonblank exact note text;
- recorded note-record SHA-256;
- exact canonical document bytes.

It does **not**:

- locate the source capture;
- read or verify the source capture;
- prove the paragraph ordinal exists in that capture;
- prove the persisted coordinates fit its returned paragraph prefix;
- derive selected source text;
- recreate 17A, 18A, or 18B typed objects;
- authenticate the human author;
- verify a quotation or citation.

This refusal is an authority feature, not a missing validation step.

## Tests

Seven focused tests prove:

1. persistence retains the exact supplied 18B note object while writing only durable source identity + layered paragraph/range identity + human note;
2. URL, endpoint, target ID, element ID, paragraph text, selected text, and source path are absent from the sidecar;
3. verification reads only the sidecar and preserves exact paragraph/range coordinates plus verbatim human text;
4. overwrite and missing-parent cases fail explicitly;
5. persistence reuses 18A bounded-range validation and separately rejects malformed durable source-digest identity;
6. payload mutation without digest update and semantically valid noncanonical JSON bytes are rejected;
7. changing the range/note and recomputing the digest yields another self-consistent sidecar, proving SHA-256/file verification is not source-range authentication;
8. the complete persist/verify path is available through the public `pyxis.app` API.

Several assertions are combined into seven focused test functions rather than inflating the test count artificially.

## Validation

Behavior/public API proof:

- Actions #612 on `542bc83dafce254f9cd1f5323b0421ac8570bf02` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 checked out exact head `542bc83dafce254f9cd1f5323b0421ac8570bf02`;
- **311 tests collected / 311 passed in 30.83s**;
- all seven focused 18C tests passed alongside the complete established Repository Zero, Chromium, capture, paragraph-selection, paragraph-note, note-persistence/relinking, exact-range-selection, and exact-range-note stack.

## Explicit non-goals

18C adds no:

- selected source-text storage;
- page/paragraph/source-evidence duplication;
- source path persistence;
- source-capture lookup or discovery;
- source-capture read or verification during sidecar verification;
- proof that persisted coordinates address a source capture;
- typed exact-range-note rehydration/relinking;
- recreation of 17A/18A/18B object identity;
- browser acquisition or control;
- range-note overwrite/update/delete/history semantics;
- multi-range or multi-note collection;
- generic annotation or selection registry;
- tags, categories, labels, questions, claims, or confidence fields;
- author/user/account identity;
- timestamp or observation time;
- HMAC, signatures, or cryptographic authorship;
- relevance, importance, truth, support, or quality scoring;
- quotation/citation verification;
- source provenance authentication;
- semantic passage extraction;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

## Decision — D137

**One immutable 18B exact-range note may be persisted as deterministic no-overwrite sidecar JSON containing only the established durable source-capture content reference (`capture_format` + `bundle_sha256`), the layered human selection identity (17A paragraph selection mode + ordinal and 18A text-selection mode + Unicode offset unit + zero-based half-open start/end offsets), and the exact 18B note mode/verbatim caller text. Persistence must re-establish the live note/range contract through the existing 18B/18A boundaries and retain the exact supplied 18B note object in runtime persistence evidence, but it must not copy selected source text, paragraph/page evidence, loaded-capture state, source path, or other browser evidence into the sidecar. The sidecar SHA-256 covers the complete durable reference + human-action payload and is self-integrity evidence only, not authorship, authentication, source verification, quotation/citation proof, or proof that persisted coordinates address the referenced source. Sidecar verification reads only the sidecar and may validate coordinate shape but must not claim source-range validity without an explicit caller-supplied matching capture; typed relinking is a separate future authority boundary.**
