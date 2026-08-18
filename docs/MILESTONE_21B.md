# Milestone 21B — Durable Working-Set Note

## Product question

Can Pyxis make one already-created 21A human-authored working-set note durable while preserving the note verbatim and referencing the exact durable 20B working set it belongs to, without copying the working-set member graph again or pretending note-file integrity proves that the parent reference is correct?

21B answers **yes**.

## Why this milestone exists

21A established the first set-level human interpretation boundary:

```text
20A working set
      ↓
21A human-authored note
      ↓
"this is why I am carrying these pieces together"
```

But the 21A record is only in-memory application state.

If the researcher closes the process, the set-level rationale disappears even when the working set itself has already been made durable through 20B.

21B adds only the missing durability boundary:

```text
21A working-set note
      +
explicit durable 20B working-set sidecar
      ↓
re-establish 21A live-note validity
      ↓
re-establish 20B parent identity through public 20C
      ↓
serialize parent durable identity + verbatim human note
      ↓
canonical no-overwrite sidecar
      ↓
SHA-256 self-integrity
```

This does not create a notebook database or a richer information architecture.

## A durable note requires a durable parent

21A intentionally accepts any valid in-memory 20A working-set record.

21B is narrower.

A durable working-set note must identify which durable working set it belongs to.

Therefore 21B requires the caller to supply:

```python
persist_chromium_research_working_set_note(
    note,
    working_set_source,
    destination,
)
```

where:

- `note` is an already-created 21A working-set note;
- `working_set_source` is the caller-supplied path to the durable 20B working-set sidecar that is claimed to be the note's parent;
- `destination` is the no-overwrite 21B sidecar path.

21B does not silently manufacture a durable parent identity from an ephemeral working set.

Thus:

```text
in-memory parent
≠
durable parent identity
```

and:

```text
21A eligibility
≠
21B persistence eligibility
```

The extra requirement is intentional because durability must reference durable content.

## Public module API

Persistence:

```python
persist_chromium_research_working_set_note(
    note,
    working_set_source,
    destination,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNotePersistenceEvidence(
    path=...,
    note_format="pyxis.chromium.research_working_set_note.v1",
    note_record_sha256=...,
    byte_count=...,
    note=<exact supplied 21A note object>,
)
```

Verification:

```python
verify_chromium_research_working_set_note(source)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteVerificationEvidence(
    path=...,
    note_format="pyxis.chromium.research_working_set_note.v1",
    note_record_sha256=...,
    byte_count=...,
    working_set_format="pyxis.chromium.research_working_set.v1",
    working_set_record_sha256=...,
    note_mode="caller_authored_note_on_research_working_set",
    note_text=<verbatim text>,
    document_json=...,
)
```

Integrity failures use:

```python
ChromiumResearchWorkingSetNoteIntegrityError
```

The API is exposed through the explicit module:

```python
pyxis.app.chromium_research_working_set_note_persistence
```

21B does not broaden the `pyxis.app` root re-export surface.

## The durable record is intentionally minimal

The 21B sidecar contains:

```text
format
note_record_sha256
note_record:
  working_set_reference:
    format
    working_set_record_sha256
  note:
    mode
    text
```

The parent reference stores exactly:

```text
working-set sidecar format
working-set record SHA-256
```

The note stores exactly:

```text
human-note mode
verbatim human text
```

21B deliberately does **not** copy into the note sidecar:

- member kinds;
- member sidecar formats;
- member sidecar record digests;
- paragraph ordinals;
- exact text-range coordinates;
- source capture digests;
- selected source text;
- member-level human notes;
- URLs;
- browser target IDs;
- working-set sidecar path;
- member sidecar paths;
- source-capture paths;
- loaded application object graphs.

The 20B working-set sidecar already owns the durable member sequence.

Thus:

```text
working-set-note durability
≠
second serialization of working-set membership
```

## Parent coherence is re-established through public 20C

21B does not duplicate the 20B/20C member-identity logic.

Before writing, persistence performs two distinct re-establishment steps.

First, it re-establishes the 21A live note through:

```python
create_chromium_research_working_set_note(
    note.working_set,
    note_text=note.note_text,
)
```

The validation result is discarded so the persistence result can retain the exact supplied 21A note object.

Second, it calls:

```python
load_chromium_research_working_set(
    note.working_set.items,
    working_set_source,
)
```

That public 20C boundary:

1. freshly verifies the caller-supplied 20B working-set sidecar;
2. re-establishes the note parent's member sequence through public 20A;
3. matches every durable member identity position-by-position;
4. preserves order and intentional duplicates;
5. rejects a different durable working set.

21B then takes only the resulting 20B durable working-set identity needed for its own sidecar.

This preserves:

```text
20C owns durable working-set/member coherence
21B owns durable note attachment to that verified parent identity
```

not:

```text
21B reimplements 20C
```

## Exact live note identity is retained in persistence evidence

The returned persistence evidence contains:

```text
note is exact supplied 21A note object
```

The sidecar itself does not serialize Python object identity.

Therefore:

```text
runtime object identity
≠
durable identity
```

but the live persistence operation still preserves the exact object relationship in its returned application evidence.

## The working-set path is location, not identity

`working_set_source` is only the caller-supplied location used to freshly re-establish the durable parent.

The 21B sidecar stores no parent filesystem path.

If the 20B sidecar moves before 21B persistence, the caller may supply the new path.

If its content still verifies and matches the note's working set through 20C, persistence succeeds and records the same durable parent identity.

Thus:

```text
working-set path
≠
working-set durable identity
```

## Individual member sidecars are not reread

21B does read the explicitly supplied 20B working-set sidecar because that is the parent durability authority it is establishing.

It does **not** reread the individual 17C/18C/19C member sidecars.

This follows from delegating parent coherence to 20C, which operates on already-loaded 17D/18D/19D member records.

A researcher may therefore:

1. relink individual member records earlier;
2. create and persist a 20A/20B working set;
3. create a 21A rationale;
4. lose or move individual member sidecars during the current application lifetime;
5. still persist the 21A rationale against the still-available 20B parent working-set sidecar.

This means:

```text
21B durable parent verification
≠
fresh verification of every member sidecar
```

and:

```text
current individual member-file availability
≠
ability to persist rationale against an already-durable coherent working set
```

It does not claim missing member files can later be recovered.

## Human text remains verbatim

21B copies the established 21A note text exactly into the durable note record.

It does not normalize, trim, summarize, correct, classify, rank, or rewrite accepted text.

Leading/trailing whitespace, Unicode, punctuation, line breaks, uncertainty, questions, and tentative wording remain exactly as the researcher supplied them to 21A.

Thus:

```text
21A human wording
=
21B durable human wording
```

Persistence does not upgrade the note into machine interpretation.

## Canonical no-overwrite JSON

21B uses the established durability pattern:

- UTF-8 JSON;
- sorted object keys;
- compact separators;
- no NaN values;
- exactly one trailing newline;
- SHA-256 over canonical `note_record` bytes;
- exclusive-create destination semantics.

The same 21A note persisted against the same durable 20B parent produces byte-identical 21B files at two different destinations.

A second write to an existing destination fails rather than replacing it.

The SHA-256 is self-integrity evidence only.

It is not authentication, authorship, trusted time, chain of custody, semantic correctness, or proof that the referenced working set remains available.

## File verification remains file-local

`verify_chromium_research_working_set_note(...)` reads only the 21B sidecar.

It validates:

- exact top-level format;
- exact note-record shape;
- exact parent working-set format;
- structurally valid parent working-set record SHA-256;
- established note mode;
- non-whitespace human note text;
- recorded note-record SHA-256;
- canonical file bytes.

It does **not**:

- open the referenced 20B working-set sidecar;
- search for a working set by digest;
- relink the parent;
- open individual member sidecars;
- open source captures;
- contact Chromium;
- evaluate the note's semantics.

Therefore successful 21B verification proves only file-local durable representation and self-integrity.

## Falsifiability proof: a wrong parent digest can remain 21B-valid

The principal authority test deliberately creates a valid 21B sidecar, then changes:

```text
working_set_reference.working_set_record_sha256
```

to another structurally valid lowercase 64-hex digest.

The test then recomputes:

```text
note_record_sha256
```

and rewrites canonical JSON.

21B verification **must succeed**.

That behavior is intentional.

The file is internally self-consistent, and 21B verification has not been given an actual durable parent against which to compare the reference.

Therefore:

```text
working-set-note file integrity
≠
parent working-set identity correctness
```

and:

```text
21B verification
≠
working-set-note relinking
```

A future explicit relinking boundary must earn the authority to compare the persisted parent identity against caller-supplied durable/loaded working-set evidence.

This is the acceptance seed for the next durability-reestablishment step **if** that becomes the next real researcher pressure.

## A different durable parent is rejected during persistence

21B persistence is stronger than 21B file verification because persistence has both:

- the live 21A note with its exact working-set member sequence;
- the caller-supplied 20B working-set sidecar path.

If the caller supplies a valid but different 20B working-set sidecar, public 20C rejects the mismatch before the 21B destination is written.

This proves:

```text
successful persistence attachment
=
coherent live 21A note + explicitly supplied matching durable 20B parent
```

not merely:

```text
valid-looking parent digest
```

## What successful 21B persistence proves

Successful persistence proves only that:

1. the caller supplied an established 21A working-set note;
2. its live note/working-set relationship re-establishes through public 21A;
3. the caller supplied a 20B working-set sidecar path;
4. that sidecar freshly verifies and relinks through public 20C against the exact member sequence retained by the note's working set;
5. the resulting durable 20B working-set format and record SHA-256 were recorded as the note's parent identity;
6. the established 21A note mode and verbatim human note text were serialized exactly;
7. a canonical no-overwrite 21B file was written whose recorded note-record SHA-256 matches its canonical note record.

This is:

```text
durable representation of one human rationale
attached to one explicitly re-established durable working-set identity
```

## What successful 21B persistence does not prove

21B does **not** prove:

- that the rationale is correct;
- that the members are semantically related;
- contradiction, corroboration, entailment, causation, or relevance;
- completeness or representativeness;
- source authenticity, reliability, or truth;
- quotation or citation validity;
- claim support;
- human authorship identity beyond caller-supplied text entering the operation;
- trusted time;
- chain of custody;
- that individual member sidecars currently exist;
- that member sidecars would freshly verify now;
- that the parent working-set path will continue to exist;
- machine agreement;
- browser freshness.

Persistence preserves human rationale and attachment identity. It does not upgrade semantic or evidentiary authority.

## Focused tests

Eight focused tests cover:

1. minimal serialization of only durable 20B parent identity plus verbatim 21A note, with no duplicated member/source graph;
2. successful persistence after the 20B parent sidecar moves, proving parent path is location rather than identity;
3. rejection of a different valid 20B durable parent before destination creation;
4. successful persistence after individual member sidecars are deleted, proving no hidden member-file reread;
5. rejection of a parent-reference mutation when the 21B note-record digest is not recomputed;
6. acceptance of a structurally valid wrong parent digest after recomputing the 21B note-record digest, proving file integrity is not parent identity correctness;
7. deterministic byte identity across destinations plus exclusive-create no-overwrite behavior;
8. explicit public importability through the 21B persistence module.

## Explicit non-goals

21B adds no:

- working-set-note relinking;
- working-set discovery;
- digest-based parent search;
- automatic parent-file lookup;
- fresh individual member relinking;
- member-file discovery;
- notebook database;
- title/folder/tag/label taxonomy;
- search;
- ranking;
- deduplication;
- semantic clustering;
- similarity scoring;
- contradiction/corroboration detection;
- claim modeling;
- source authentication;
- quotation/citation verification;
- authorship verification;
- trusted timestamps;
- revision history;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- researcher UI.

## Decision — D147

**Pyxis may persist one already-created 21A human-authored research working-set note only when the caller also supplies an explicit durable 20B working-set sidecar path that can be freshly re-established as the note's parent through the public 20C relinking boundary using the exact loaded-member sequence retained by the note's 20A working set. Persistence must first re-establish the live note through the public 21A constructor, then reuse 20C rather than duplicating working-set/member identity validation, and must record only the established durable 20B parent identity `(working-set format + working-set record SHA-256)` plus the established 21A note mode and verbatim human text. The 21B sidecar must not copy the working-set member graph, source evidence, member notes, paths, browser state, or inferred semantics. Verification of the 21B file remains file-local: it may establish only supported canonical structure and SHA-256 self-integrity. A self-consistent 21B file whose parent working-set digest has been replaced by another valid-looking digest must remain 21B-valid after the note-record digest is recomputed, because parent identity correctness requires a separate explicit relinking boundary. Durable working-set identity, durable human rationale, file integrity, parent re-establishment, and semantic truth remain separate authority layers.**
