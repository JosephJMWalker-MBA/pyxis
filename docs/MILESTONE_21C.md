# Milestone 21C — Verified Working-Set Note Relinking

## Product question

Can Pyxis reopen one durable 21B human-authored working-set note only after re-establishing that its persisted parent identity matches one explicit caller-supplied durable 20B working set and complete ordered sequence of already-loaded members?

21C answers **yes**.

## Why this milestone exists

21A created human rationale over one exact working set:

```text
20A working set
      ↓
21A human-authored rationale
```

21B then made that rationale durable by storing only:

```text
20B parent working-set format
20B parent working-set record SHA-256
21A note mode
21A verbatim note text
```

But 21B intentionally proved only file-local self-integrity.

Its falsifiability test demonstrated that the persisted parent digest can be replaced with another structurally valid SHA-256, the outer note digest can be recomputed, and 21B verification will still succeed.

Therefore 21B cannot establish that the recorded parent reference is correct.

21C adds the missing re-establishment boundary:

```text
21B note sidecar path
      ↓
fresh 21B verification
      +
caller-supplied complete ordered loaded-member sequence
      +
caller-supplied 20B working-set sidecar path
      ↓
fresh 20C parent relinking
      ↓
exact durable parent identity match
      ↓
reconstruct 21A note over exact reconstructed 20A working set
```

## Public module API

```python
load_chromium_research_working_set_note(
    items,
    working_set_source,
    note_source,
)
```

returns:

```python
ChromiumPageResearchLoadedWorkingSetNoteRecord(
    verification=<fresh 21B verification>,
    working_set=<fresh 20C loaded working-set record>,
    note=<new 21A note over working_set.working_set>,
)
```

Parent mismatches use:

```python
ChromiumResearchWorkingSetNoteParentMismatchError
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_note_load
```

21C does not broaden the `pyxis.app` root re-export surface.

## Caller-owned explicit inputs

21C requires three explicit inputs:

1. the complete ordered sequence of already-loaded 17D/18D/19D member records;
2. the caller-supplied path to the candidate 20B working-set parent;
3. the caller-supplied path to the 21B working-set-note sidecar.

Pyxis does not search for the parent by:

- working-set digest;
- note digest;
- filesystem path history;
- member digest;
- source digest;
- URL;
- note text;
- semantic similarity.

There is no automatic parent discovery.

## 21B is freshly verified

21C accepts a note sidecar path, not a prebuilt verification object.

It always calls:

```python
verify_chromium_research_working_set_note(note_source)
```

before parent attachment is accepted.

This preserves:

```text
caller-supplied location
≠
verified durable note evidence
```

A moved 21B sidecar may still relink because filesystem path is not durable note identity.

## The parent is freshly re-established through 20C

21C does not reproduce working-set membership verification.

It calls:

```python
load_chromium_research_working_set(
    supplied_items,
    working_set_source,
)
```

That public 20C boundary:

1. freshly verifies the supplied 20B sidecar;
2. requires the complete member count;
3. re-establishes supported member coherence through 20A;
4. matches every durable member reference position-by-position;
5. preserves order and intentional duplicates;
6. retains the exact caller-supplied loaded member objects in the reconstructed 20A working set.

Therefore 21C inherits but does not duplicate 20C's authority.

## The new 21C authority check

After 20C succeeds, 21C compares the durable parent reference persisted in 21B against the fresh 20B verification retained by the loaded parent.

It compares exactly:

```text
working-set format
working-set record SHA-256
```

The SHA-256 is used only as the durable content identity already established by 20B.

It is not authentication, authorship, trusted time, chain of custody, or proof of semantic correctness.

Successful equality establishes only:

```text
this verified 21B note records the same durable 20B parent identity
as the explicitly supplied and freshly relinked working set
```

## A different valid durable parent is rejected

A caller may supply another perfectly valid 20B working set with its own coherent loaded-member sequence.

20C can successfully load that different parent.

21C must still reject it if its durable identity differs from the parent reference stored by the 21B note.

This matters because:

```text
valid working set
≠
correct parent for this note
```

The new attachment relationship belongs to 21C.

## Principal falsifiability proof

21B deliberately allows this file-local state:

```text
parent working-set digest changed to another valid 64-hex value
      ↓
21B note-record digest recomputed
      ↓
canonical JSON rewritten
      ↓
21B verification succeeds
```

21C then receives the actual intended durable 20B parent and loaded members.

Fresh 20C parent relinking succeeds.

The parent digest retained by that fresh 20B verification does not equal the falsified parent digest retained by the verified 21B note.

21C rejects with:

```python
ChromiumResearchWorkingSetNoteParentMismatchError
```

Therefore:

```text
21B working-set-note file integrity
≠
parent working-set identity correctness
```

while:

```text
successful 21C relinking
=
verified durable note-to-parent identity coherence
relative to one explicit caller-supplied 20B parent and loaded-member sequence
```

## Human note reconstruction remains human interpretation

After durable parent identity matches, 21C reconstructs the note through public 21A:

```python
create_chromium_research_working_set_note(
    loaded_parent.working_set,
    note_text=verification.note_text,
)
```

The reconstructed note therefore:

- uses the exact 20A working-set object produced by fresh 20C loading;
- preserves the 21B human note text verbatim;
- reuses 21A's established note-mode and parent-coherence boundary.

The returned relationship is explicit:

```text
loaded.note.working_set is loaded.working_set.working_set
```

The human wording is not summarized, normalized, classified, corrected, or interpreted by Pyxis.

## The proof chain remains visible

The loaded 21C record retains three distinct layers:

```text
verification
  = fresh 21B file-local note verification

working_set
  = fresh 20C durable parent relinking evidence

note
  = reconstructed 21A human interpretation
```

These are not collapsed because they answer different questions.

Thus:

```text
note-file verification
≠
parent relinking
≠
human interpretation
```

## Paths remain locations, not identities

Both the 20B parent sidecar and the 21B note sidecar may move before 21C.

The caller supplies their current locations.

If their durable content verifies and the recorded parent identity matches, relinking succeeds.

Neither path is serialized into the reconstructed note as authority.

## Individual member sidecars are not reread

21C explicitly reads:

- the supplied 21B note sidecar;
- the supplied 20B working-set sidecar.

It does not reread individual 17C/18C/19C member sidecars.

The already-loaded 17D/18D/19D records remain the caller-supplied application evidence used by 20C.

Therefore individual member sidecars may have moved or disappeared after their earlier successful relinking and 21C can still succeed during the same application lifetime.

This proves only:

```text
current individual member-file availability
≠
ability to re-establish a durable working-set note against already-loaded member evidence
```

It does not make missing member files recoverable.

## Order and count remain owned by 20C

21C does not weaken the established working-set contract.

If the 20B parent records:

```text
A, B
```

then supplying:

```text
B, A
```

fails through 20C.

Missing or extra members also fail through 20C.

Thus 21C does not treat the working set as an unordered bag merely because the note references the set by one digest.

## What successful 21C loading proves

Successful 21C loading proves only that:

1. the caller supplied a 21B sidecar whose bytes freshly satisfy the 21B canonical structure and self-integrity contract;
2. the caller supplied a 20B sidecar and complete ordered loaded-member sequence that freshly satisfy 20C relinking;
3. the verified 21B parent working-set format matches the fresh 20B parent format;
4. the verified 21B parent working-set record SHA-256 matches the fresh 20B parent record SHA-256;
5. the persisted human note can be reconstructed through 21A over the exact 20A working-set object returned by 20C;
6. the human text is preserved verbatim.

This is **durable human working-set-note attachment coherence relative to one explicit caller-supplied durable working set and loaded-member sequence**.

## What successful 21C loading does not prove

21C does **not** prove:

- that the human rationale is correct;
- that members are semantically related;
- support, contradiction, corroboration, entailment, or causation;
- relevance, importance, completeness, or representativeness;
- source authenticity, reliability, or truth;
- quotation or citation validity;
- claim support;
- authorship identity;
- trusted time;
- chain of custody;
- browser freshness;
- current existence of individual member sidecars;
- machine agreement.

Relinking restores a durable attachment relationship. It does not upgrade semantic authority.

## Focused tests

Eight focused tests cover:

1. successful relinking after both the 20B parent and 21B note sidecars move, with exact caller-supplied member identities and verbatim note text retained;
2. rejection of a different but valid durable 20B parent after that parent independently succeeds through 20C;
3. rejection of the recomputed, 21B-valid wrong parent digest against the actual supplied parent;
4. fresh 21B note verification, including rejection of note bytes changed without a matching digest;
5. successful relinking after all individual member sidecars are deleted, proving no hidden member-file reread;
6. preservation of 20C's exact ordering authority;
7. preservation of 20C's exact member-count authority;
8. explicit public importability through the 21C module.

## Explicit non-goals

21C adds no:

- parent discovery;
- digest search;
- automatic file lookup;
- notebook database;
- title/folder/tag/label taxonomy;
- search or ranking;
- semantic clustering;
- similarity scoring;
- contradiction/corroboration detection;
- claim modeling;
- source authentication;
- citation verification;
- authorship verification;
- trusted timestamps;
- revision history;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- researcher UI.

## Decision — D148

**Pyxis may load one durable 21B human-authored working-set note only when the caller explicitly supplies the complete ordered sequence of already-loaded research members, one 20B working-set sidecar path, and one 21B working-set-note sidecar path. Pyxis must freshly verify the 21B sidecar, freshly re-establish the supplied durable parent through public 20C, and require the 21B parent working-set format and working-set record SHA-256 to match the fresh 20B verification evidence. Only after that match may Pyxis reconstruct the human note through public 21A over the exact 20A working-set object produced by 20C. The returned loaded record must keep fresh 21B verification, fresh 20C parent evidence, and reconstructed 21A interpretation as separate typed layers. Pyxis must not discover parents, search by digest, reorder members, reread individual member sidecars, infer note semantics, or treat SHA-256 equality as authentication or semantic authority.**
