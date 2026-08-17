# Milestone 17D — Verified Durable Note Relinking

## Product question

Can one durable 17C paragraph-note sidecar re-enter the typed Pyxis research workflow against one explicit caller-supplied 16C loaded capture without searching for source files, trusting an unverified note object, reacquiring browser state, or turning digest agreement into authenticity?

17D answers **yes** through one explicit verify → match → reconstruct boundary.

## Why this milestone exists

17C made one exact human note durable while deliberately stopping before source relinking:

```text
17B human note
    ↓
minimal durable source reference + verbatim note
    ↓
17C canonical sidecar + self-integrity verification
```

That sidecar can say which durable source content it references, but 17C verification intentionally does not prove that a compatible source capture is present.

A useful research workflow eventually needs the inverse transition: given one already-loaded durable capture and one durable note sidecar, recover the typed human action without weakening any upstream authority boundary.

## Boundary

```text
caller-supplied ChromiumPageResearchLoadedCaptureEvidence
    +
caller-supplied note sidecar path
    ↓
fresh 17C sidecar verification
    ↓
compare source capture format + bundle SHA-256
against exact 16B verification retained by supplied 16C capture
    ↓
existing public 17A paragraph selection
    ↓
existing public 17B human note creation
    ↓
ChromiumPageResearchLoadedParagraphNoteRecord
    ├── exact fresh 17C verification evidence
    └── reconstructed 17B note
          └── selection retains exact supplied 16C capture + exact paragraph
```

Public API:

```python
load_chromium_research_paragraph_note(
    source,
    note_source,
)
```

Public result:

```python
ChromiumPageResearchLoadedParagraphNoteRecord(
    verification=<fresh exact 17C sidecar verification evidence>,
    note=<new 17B note linked to exact supplied source>,
)
```

A distinct `ChromiumResearchParagraphNoteSourceMismatchError` separates cross-artifact reference mismatch from 17C file-integrity failure.

## The note sidecar is re-verified from disk

17D accepts a note sidecar **path**, not a caller-supplied `ChromiumPageResearchParagraphNoteVerificationEvidence` object.

The verification dataclass is publicly constructible Python state. Accepting one as proof would allow a caller to bypass the established 17C file boundary merely by instantiating an object with plausible fields.

17D therefore always calls:

```python
verify_chromium_research_paragraph_note(note_source)
```

before attempting any relinking.

A corrupted sidecar with stale digest fails at the existing 17C integrity boundary and emits no loaded note record.

## The source is explicit rather than discovered

17D does not search the filesystem, capture index, browser, URL, endpoint, or bundle digest for a matching source.

The caller supplies one exact `ChromiumPageResearchLoadedCaptureEvidence` object.

Pyxis answers only:

> Does this freshly verified note sidecar reference this supplied durable source content?

That preserves agency and prevents content identity from silently becoming source-discovery authority.

## Content identity, not path identity

17C intentionally excluded source path from durable note identity. 17D preserves that rule.

The source match is:

```text
sidecar.source_capture_format
    == supplied_capture.verification.capture_format

sidecar.source_bundle_sha256
    == supplied_capture.verification.bundle_sha256
```

The bundle digest comparison uses `hmac.compare_digest`, but the digest remains ordinary SHA-256 content identity rather than a MAC/signature.

A focused test changes only the loaded capture's path while keeping the same retained content identity and proves relinking still succeeds.

Moving or copying a capture therefore does not break a note attachment merely because its location changed.

## The retained 16B verification evidence remains authoritative for matching

17D does not recompute the supplied capture's bundle digest from its typed object graph.

16C already established the typed reopening contract and deliberately retained the exact 16B verification evidence that authorized the load.

17D compares the sidecar reference to that retained verification identity rather than duplicating 16B/16C verification and reconstruction logic.

This preserves the established ownership chain:

```text
16B owns durable capture file integrity
16C owns typed capture reopening
17C owns durable note file integrity
17D owns matching the two already-established durable identities
17A owns paragraph selection
17B owns human note construction
```

## Reconstruction delegates to 17A and 17B

After the source reference matches, 17D does not manually construct selection or note dataclasses.

It calls the existing public boundaries:

```python
select_chromium_research_capture_paragraph(
    source,
    paragraph_ordinal=verification.paragraph_ordinal,
)

create_chromium_research_paragraph_note(
    selection,
    note_text=verification.note_text,
)
```

This means all previously proven limits remain active during durable re-entry.

The reconstructed selection retains the **exact supplied loaded-capture object** and the **exact paragraph object already contained by that source**. The note text is reconstructed verbatim from freshly verified 17C evidence.

## Relinking cannot expand bounded evidence

A durable note ordinal is not permission to reacquire missing evidence.

A focused test supplies a source whose paragraph observation records that a second paragraph existed but whose returned bounded prefix contains only paragraph 1. The note sidecar references paragraph 2.

Even when the sidecar's capture digest reference is made to match the supplied source verification object, the existing 17A boundary refuses the relink because paragraph 2 is outside returned evidence.

17D does not:

- reopen the source capture file;
- search for another copy of the capture;
- reconnect to Chromium;
- enlarge the old paragraph limit;
- synthesize missing text.

Durability therefore does not weaken bounded-observation semantics.

## Digest agreement is reference matching, not authenticity

Successful relinking proves a narrow relationship:

```text
freshly verified note sidecar
references the same capture content identity
retained by the supplied loaded capture
```

It does not prove:

- who created the capture;
- who wrote the note;
- that either file has not been replaced by an actor able to recompute SHA-256;
- publisher/source identity;
- trusted chain of custody;
- observation time;
- source truth;
- note truth;
- claim support;
- quotation validity;
- citation authority.

17C already proves its SHA-256 is self-integrity rather than authentication. 17D cannot promote two self-integrity digests into authentication merely because they agree.

## Tests

Six focused tests prove:

1. a freshly verified sidecar relinks to the exact caller-supplied loaded capture and exact existing paragraph while preserving note text verbatim;
2. source capture path is not attachment identity—same content identity at a different path still relinks;
3. a different source bundle SHA-256 raises the dedicated source-mismatch error;
4. a tampered sidecar with stale digest fails through the existing 17C verifier before relinking;
5. a sidecar ordinal outside the supplied source's bounded returned paragraph prefix remains unavailable and is not reacquired;
6. an unsupported supplied source-capture format is rejected before reconstruction.

## Validation

Behavior/public API proof:

- Actions #584 on `b8b51d4cd70e1da5a64aaa1400616f96f0541a40` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 log checked out exact head `b8b51d4cd70e1da5a64aaa1400616f96f0541a40`;
- **292 tests collected / 292 passed in 27.72s**;
- all six focused 17D tests passed alongside the complete established Repository Zero/browser/capture/selection/note/persistence suite.

## Explicit non-goals

17D adds no:

- capture-file discovery or lookup;
- capture index/search;
- source-path identity;
- source-capture re-verification or rehydration inside note loading;
- browser acquisition, navigation, or control;
- expansion of bounded paragraph evidence;
- generic durable-reference resolver;
- multi-note collection or notebook abstraction;
- note edit/update/delete/history semantics;
- tags, categories, questions, claims, or annotation ontology;
- author/user/account identity;
- timestamp or trusted temporal provenance;
- HMAC, signature, PKI, or cryptographic authorship;
- source/publisher authentication;
- quotation/citation verification;
- relevance, importance, confidence, truth, or claim-support scoring;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

## Decision — D134

**One durable 17C paragraph-note sidecar may re-enter the typed application layer only against one explicit caller-supplied 16C loaded capture. The relinking operation must freshly verify the sidecar from its file path, require its source capture format and bundle SHA-256 to match the exact 16B verification evidence retained by the supplied loaded capture, and then reconstruct the human action through the existing public 17A paragraph-selection and 17B note-creation boundaries. The reconstructed note must retain the exact supplied loaded-capture object and exact already-returned paragraph object, so durable relinking cannot reacquire or expand bounded evidence. Source path is not attachment identity, and digest agreement proves only durable content-reference matching; it does not authenticate either artifact, identify the human author, verify source provenance, establish chain of custody, prove truth or claim support, or strengthen quotation/citation authority.**
