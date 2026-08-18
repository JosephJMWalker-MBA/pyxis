# Milestone 19C — Durable Comparison-Note Sidecar

## Product question

Can Pyxis persist one already-created 19B human comparison note as a deterministic durable sidecar that references both source ranges without copying either source passage or pretending file integrity proves those references still address source evidence?

19C answers **yes**.

## Why this milestone exists

19A introduced explicit human juxtaposition of two exact 18A ranges.

19B attached one verbatim human-authored interpretation to that juxtaposition.

19C makes that layered human action durable:

```text
source A content identity + paragraph/range coordinates
                         \
                          → human-owned comparison mode
                         /              ↓
source B content identity + paragraph/range coordinates
                                  human-authored note
                                           ↓
                              deterministic sidecar
```

The sidecar is a durable reference to the comparison and note. It is not a second copy of either source.

## Public API

```python
persist_chromium_research_paragraph_text_selection_comparison_note(
    note,
    destination,
)
```

returns:

```python
ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence
```

and:

```python
verify_chromium_research_paragraph_text_selection_comparison_note(source)
```

returns:

```python
ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence
```

The persistence result retains the exact caller-supplied 19B note object by runtime identity.

## Durable record shape

The canonical sidecar stores only:

```text
format
note_record_sha256
note_record:
  comparison:
    mode
    first:
      source capture format
      source bundle_sha256
      paragraph selection mode + ordinal
      text-range mode + Unicode start/end offsets
    second:
      source capture format
      source bundle_sha256
      paragraph selection mode + ordinal
      text-range mode + Unicode start/end offsets
  note:
    mode
    verbatim human text
```

It deliberately does **not** store:

- selected source text;
- paragraph text;
- page URL;
- Chromium endpoint;
- target ID;
- source capture path;
- loaded-capture graph;
- browser acquisition evidence beyond the durable capture format/content identity;
- inferred semantic relationship.

Therefore runtime object identity does not pretend to survive process boundaries.

## Two independent durable source identities

19C keeps the two sides explicit.

Each comparison side has its own:

```text
capture format + bundle_sha256 + paragraph ordinal + Unicode [start:end)
```

There is no synthetic "comparison source hash" that replaces those two source-content identities.

This matters because the human comparison is an action over two source references, not a new source document.

The two references may still identify the same capture and same range because 19A permits intentional self-comparison without significance judgment.

## Live persistence validation remains layered

Persistence accepts only an existing 19B comparison-note record.

Before writing, it re-establishes:

```text
19B note validity
    ↓
19A comparison validity
    ↓
18A exact-range validity for first side
18A exact-range validity for second side
```

It then validates that each retained source is verified rehydrated capture evidence with the established capture format and a SHA-256-shaped bundle identity.

No competing range/comparison validator is introduced.

## Deterministic no-overwrite persistence

The durable document uses:

- canonical UTF-8 JSON;
- sorted keys;
- compact separators;
- no NaN values;
- exactly one trailing newline;
- exclusive creation (`xb`) so existing files are not overwritten.

Persisting the same 19B note to two distinct paths yields byte-identical documents and the same `note_record_sha256` because destination path is not part of the durable identity.

## File integrity boundary

`note_record_sha256` covers the complete durable record:

```text
first source reference
+
second source reference
+
comparison mode
+
verbatim human note
```

Verification proves only that:

1. the file is valid UTF-8 JSON;
2. its top-level and nested record shapes are exactly supported;
3. modes, offset units, coordinate primitive domains, and SHA-256 shapes are supported;
4. the persisted record digest matches canonical record bytes;
5. the complete file uses canonical Pyxis JSON encoding.

This is self-integrity evidence.

It is not authentication, authorship, source verification, trusted time, or semantic authority.

## Falsifiability proof: `end_offset = 999`

19C deliberately preserves the strongest 18C-style negative proof across the two-source comparison boundary.

A valid sidecar can be modified so that the second persisted range changes from a source-valid end offset to:

```text
end_offset = 999
```

If the caller recomputes `note_record_sha256` and writes canonical JSON, 19C verification succeeds.

That is intentional.

19C can prove the persisted file is structurally valid and internally self-consistent. It cannot prove that `999` is still inside the referenced source paragraph because verification does not reopen either source capture.

Therefore:

```text
file integrity
≠
source-range validity
```

The `999` case is the acceptance seed for 19D.

## No implicit relinking

Verification does not:

- search for source captures by digest;
- read any source capture path;
- reopen either loaded capture;
- reconstruct either 17A paragraph selection;
- reconstruct either 18A exact range;
- reconstruct 19A comparison;
- reconstruct 19B note.

A sidecar references two source-content identities, but those references are not yet relinked to explicit caller-supplied source evidence.

That relationship remains a separate proof.

## What successful persistence proves

Successful persistence proves that an already-valid live 19B comparison note was serialized as the supported deterministic no-overwrite durable record and that the persistence result retained the exact supplied in-memory note object.

It does not prove that the resulting file will relink later.

## What successful verification proves

Successful verification proves only file-local integrity and supported durable-reference shape.

It does **not** prove:

- either capture exists now;
- either capture is authentic;
- either capture path is known;
- either paragraph ordinal is currently addressable in source evidence;
- either exact range is currently in bounds;
- either persisted range contains the same text a researcher previously saw;
- the two passages are similar, different, contradictory, corroborating, or relevant;
- the human note is true;
- the human author is authenticated;
- when the note was written;
- any quotation or citation is valid;
- any machine agrees with the note.

## Focused tests

Eight focused tests cover:

1. two distinct durable source identities, exact note retention, verbatim note text, and absence of copied source text/URLs/paths;
2. deterministic bytes plus no-overwrite behavior;
3. required parent directory, live 19B→19A→18A validation, and wrong-type refusal;
4. digest-tamper rejection plus canonical-JSON enforcement;
5. the self-consistent `end_offset=999` falsifiability proof;
6. persisted comparison/source/range/note domain-shape rejection;
7. same-selection comparison persistence without significance judgment;
8. public `pyxis.app` exposure.

## Explicit non-goals

19C adds no:

- comparison-note relinking or rehydration;
- automatic source discovery by digest or path;
- source capture reread during verification;
- selected source-text persistence;
- browser acquisition, navigation, or control;
- similarity or distance score;
- contradiction, entailment, or corroboration detection;
- claim/support model;
- relevance or confidence judgment;
- quotation/citation verification;
- source authentication;
- author identity or trusted timestamp;
- embeddings or LLM work;
- notebook, collection, or generic annotation framework;
- researcher UI.

## Decision — D141

**Pyxis may persist one already-valid 19B human comparison note as deterministic no-overwrite canonical JSON containing exactly two explicit durable source-content references, the caller-owned comparison mode, and the caller's verbatim note. Each source reference must retain capture format plus bundle SHA-256, paragraph ordinal/selection mode, and Unicode exact-range coordinates without copying selected source text, source paths, URLs, loaded-capture graphs, or browser transport state. Persistence must re-establish the live 19B→19A→18A contract before writing, while verification remains file-local and proves canonical encoding, supported structural/domain shape, and SHA-256 self-integrity only. A self-consistent sidecar with a recomputed digest and an out-of-bounds persisted coordinate such as `end_offset=999` must remain file-valid, demonstrating that file integrity does not prove source-range validity. Explicit relinking of both source references remains a separate future authority boundary. Source evidence, human selection, human juxtaposition, human interpretation, durable representation, and source re-establishment remain distinct layers.**
