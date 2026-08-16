# Milestone 17C — Durable Human Note Sidecar

## Product question

Can one exact 17B human-authored paragraph note become durable without copying its underlying page/capture evidence into a second source representation, inferring metadata the system did not observe, or turning a checksum into authorship/authentication proof?

17C answers **yes** through one deterministic no-overwrite sidecar format.

## Why this milestone exists

17B proved the first human interpretation boundary:

```text
source evidence
    ↓
explicit human selection
    ↓
verbatim human note
```

That note remained an in-memory record. A research workflow cannot depend on the Python process staying alive if the human's work is meant to survive.

The naive persistence approach would serialize the complete 17B object graph. That would recursively copy the loaded 16C capture, selected paragraph evidence, page URL, endpoint, and all other browser evidence merely to preserve one human note.

That would be the wrong authority shape. The source evidence is already durable under 16B. 17C therefore persists a **reference to that durable source**, not another copy of it.

## Boundary

```text
ChromiumPageResearchParagraphNoteRecord
    ↓
validate exact 17B note + source reference facts
    ↓
source capture format + bundle SHA-256
+ explicit paragraph ordinal / selection mode
+ exact note mode / verbatim note text
    ↓
canonical deterministic JSON
    ↓
SHA-256 over complete reference + note payload
    ↓
exclusive-create caller-chosen sidecar
```

Public API:

```python
persist_chromium_research_paragraph_note(
    note,
    destination,
)

verify_chromium_research_paragraph_note(source)
```

Persistence result:

```python
ChromiumPageResearchParagraphNotePersistenceEvidence(
    path=...,
    note_format="pyxis.chromium.research_paragraph_note.v1",
    note_record_sha256=...,
    byte_count=...,
    note=<exact supplied 17B note object>,
)
```

Verification result exposes the sidecar's exact persisted source-reference, selection, and note fields plus canonical document text.

## Durable identity is not Python object identity

17B deliberately retains the exact selection and paragraph objects by Python object identity while the process is alive.

Object identity cannot truthfully survive process boundaries.

17C therefore changes the identity mechanism at the persistence boundary instead of pretending otherwise:

```text
in memory
exact object identity

on disk
source capture content identity
+ explicit paragraph ordinal
```

The durable source reference is:

```text
capture format: pyxis.chromium.research_capture.v1
bundle SHA-256: <64 lowercase hex characters>
paragraph ordinal: <positive integer>
```

The selection and note modes are also persisted exactly so downstream code does not need to infer which human-action contracts produced the sidecar.

## No source-evidence duplication

The 17C sidecar intentionally does **not** persist:

- page URL;
- Chromium endpoint;
- target ID;
- page title/body text;
- paragraph text;
- paragraph element ID;
- headings;
- links;
- metadata;
- tables;
- lists;
- the complete 16A bundle;
- the 16B capture document;
- the 16C loaded-capture object graph.

Those facts remain owned by the already-durable source capture.

The sidecar records only enough source identity to make a future explicit relinking check possible.

## Source path is not persisted identity

The source capture's filesystem path is intentionally absent from the sidecar.

A path is a location, not content identity. The same verified capture bytes may be copied or moved without becoming different source evidence, while a different capture can occupy the same path later.

17C therefore does not hard-code a source path into the human note record.

A future relinking operation may accept a caller-supplied capture and compare its verified bundle SHA-256 with the sidecar reference. 17C itself does not perform that operation.

## Verbatim human text remains verbatim

The sidecar persists the exact 17B `note_text` string.

Leading/trailing spaces, line breaks, Unicode, punctuation, capitalization, spelling, and wording remain unchanged.

Whitespace stripping is used only to reject a forged persisted record containing no substantive caller text. It does not normalize the stored value.

## Deterministic no-overwrite file contract

The note format is:

```text
pyxis.chromium.research_paragraph_note.v1
```

The complete reference + note payload is canonical JSON using:

- UTF-8;
- direct Unicode;
- sorted object keys;
- compact separators;
- no NaN/Infinity values;
- one final newline on the complete document.

The caller supplies the exact destination path. Its parent directory must already exist. Existing files are never overwritten.

The deterministic payload means the same exact source-reference/selection/note facts produce the same `note_record_sha256` regardless of destination path.

## SHA-256 is self-integrity only

`note_record_sha256` covers the complete persisted note record:

```text
source capture content reference
+ selection mode
+ paragraph ordinal
+ note mode
+ verbatim human text
```

This catches an ordinary payload mutation when the recorded digest is left unchanged.

It does **not** authenticate the human author or protect against an actor who can rewrite both the payload and digest.

A dedicated test deliberately changes the human note text, recomputes the digest, rewrites canonical bytes, and proves verification succeeds on the new self-consistent file.

That is expected behavior and documents the authority limit directly.

17C therefore adds no cryptographic authorship, signature, HMAC, account identity, trusted writer identity, or chain-of-custody claim.

## Verification reads only the sidecar

`verify_chromium_research_paragraph_note()` reads only the note sidecar.

It checks:

- valid UTF-8/JSON;
- exact top-level and nested field sets;
- supported note format;
- supported source-capture format;
- valid source bundle SHA-256 shape;
- established selection mode;
- positive integer paragraph ordinal;
- established note mode;
- nonblank exact note text;
- note-record SHA-256;
- exact canonical document bytes.

It does not:

- locate the source capture;
- read the source capture;
- verify the source capture;
- rehydrate browser evidence;
- prove the referenced paragraph exists;
- recreate a 17A selection;
- recreate a 17B note object;
- authenticate the caller.

A test uses a deliberately nonexistent source-capture path in the live 16C verification object and proves note persistence + note verification still succeed. The source path is neither persisted nor read.

## Tests

Focused tests prove:

1. persistence retains the exact supplied 17B note object in runtime evidence while writing only the minimal durable reference + human note to disk;
2. URL, endpoint, target ID, paragraph text, and source path are absent from the persisted sidecar;
3. the file is deterministic canonical JSON and `note_record_sha256` covers the complete reference + note payload;
4. verification preserves exact human text and succeeds without the referenced source capture being present;
5. overwrite and missing-parent cases fail explicitly;
6. an invalid durable source bundle digest is rejected before persistence;
7. payload mutation without digest update is rejected;
8. semantically valid but noncanonical JSON bytes are rejected;
9. changing payload + recomputing the digest produces another self-consistent file, proving SHA-256 is not authentication.

Several assertions are combined into six focused test functions so the milestone adds no artificial test-count inflation.

## Validation

Implementation/public API proof:

- Actions #575 on `10b5e13641d5a92b7b3de14c496296bfa92ec4c5` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 log checked out exact head `10b5e13641d5a92b7b3de14c496296bfa92ec4c5`;
- **286 tests collected / 286 passed in 40.31s**;
- all six focused 17C persistence/verification tests passed alongside the complete established Repository Zero/browser/capture/selection/note suite.

## Explicit non-goals

17C adds no:

- source-capture copy inside the note file;
- paragraph/page text duplication;
- source path persistence;
- source-capture lookup or relinking;
- source-capture verification during note verification;
- typed note rehydration;
- recreation of 17A/17B object identity;
- browser acquisition or control;
- note overwrite/update/delete/history semantics;
- multi-note collection or notebook abstraction;
- capture index/search;
- tags, categories, labels, note types, questions, or claims;
- author/user/account identity;
- timestamp or observation time;
- HMAC, signatures, or cryptographic authorship;
- relevance, importance, confidence, truth, or support scoring;
- quotation/citation verification;
- source provenance authentication;
- semantic passage extraction;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

## Decision — D133

**One immutable 17B paragraph-note record may be persisted as deterministic no-overwrite sidecar JSON containing only the established durable source-capture content reference (`capture_format` + `bundle_sha256`), the explicit paragraph ordinal/selection mode, and the exact note mode/verbatim caller text. Persistence must not copy the selected paragraph, page, loaded capture, source path, or other browser evidence into a second source representation. The sidecar SHA-256 covers the complete source-reference + human-action payload and is self-integrity evidence only, not authorship, authentication, source verification, claim support, or trusted provenance. Sidecar verification reads only the sidecar; relinking the durable reference to a caller-supplied verified capture is a separate future authority boundary.**
