# Milestone 22C — Verified Working-Set Note Revision Relinking

## Product question

Can Pyxis reopen one durable 22B human working-set-note revision only after proving that its persisted predecessor identity matches one explicit caller-supplied durable 21B note and that the persisted revised wording still constitutes an actual 22A exact-text revision of that predecessor?

22C answers **yes**.

## Why this milestone exists

22A introduced one append-only human change-of-mind action:

```text
prior human rationale
      ↓
explicit human revision
      ↓
revised human rationale
```

22B then made one such revision edge durable while deliberately proving only file-local integrity.

22B's falsifiability cases established that a canonical, self-consistent revision file may still contain either:

1. a structurally valid but wrong predecessor digest; or
2. revised wording equal to the real predecessor wording.

Both states correctly pass 22B verification because the predecessor note is not opened by the file-only verifier.

Therefore:

```text
22B file integrity
≠
predecessor identity correctness
```

and:

```text
22B file integrity
≠
actual revision relative to the real predecessor
```

22C adds the missing re-establishment boundary.

## Public module API

```python
load_chromium_research_working_set_note_revision(
    items,
    working_set_source,
    prior_note_source,
    revision_source,
)
```

returns:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord(
    verification=<fresh 22B verification>,
    prior_note=<fresh 21C predecessor relinking>,
    revision=<newly reconstructed 22A revision>,
)
```

Relinking mismatches use:

```python
ChromiumResearchWorkingSetNoteRevisionRelinkError
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_note_revision_load
```

22C does not broaden the `pyxis.app` root re-export surface.

## Caller-owned explicit inputs

22C requires four explicit inputs:

1. the complete ordered already-loaded 17D/18D/19D member sequence;
2. the caller-supplied 20B working-set sidecar path;
3. the caller-supplied 21B predecessor-note sidecar path;
4. the caller-supplied 22B revision sidecar path.

Pyxis performs no predecessor discovery, digest search, filesystem scanning, path-history lookup, chain traversal, semantic matching, or source search.

## Fresh 22B verification

22C accepts a revision path, not a prebuilt verification object.

It always calls:

```python
verify_chromium_research_working_set_note_revision(revision_source)
```

first.

This establishes only the 22B canonical structure and self-integrity contract.

It does not yet establish that the persisted predecessor reference is correct.

## Fresh predecessor relinking through 21C

22C calls:

```python
load_chromium_research_working_set_note(
    supplied_items,
    working_set_source,
    prior_note_source,
)
```

That public 21C boundary freshly re-establishes:

```text
20B working-set verification
+
20C ordered membership relinking
+
21B note verification
+
21C note-to-parent attachment coherence
```

22C does not duplicate those checks.

The complete member sequence remains caller supplied, ordered, and exact.

## The new 22C predecessor identity check

After 21C succeeds, 22C compares exactly:

```text
verified 22B prior-note format
verified 22B prior-note record SHA-256
```

against:

```text
fresh 21C predecessor note format
fresh 21C predecessor note record SHA-256
```

SHA-256 remains only durable content identity/self-integrity evidence.

It is not authentication, authorship, trusted time, or chain of custody.

A different but fully valid 21B predecessor can successfully relink through 21C and still be rejected by 22C.

Thus:

```text
valid durable predecessor
≠
correct predecessor for this revision
```

## The revision action is freshly re-established through 22A

After predecessor identity matches, 22C calls:

```python
create_chromium_research_working_set_note_revision(
    loaded_prior.note,
    revised_note_text=verification.revised_note_text,
)
```

This matters because 22A owns the exact textual no-op boundary.

If the persisted revised wording equals the freshly reconstructed predecessor wording exactly, public 22A rejects the operation.

22C converts that failure into:

```python
ChromiumResearchWorkingSetNoteRevisionRelinkError
```

Therefore successful 22C establishes not only predecessor identity coherence but also that the durable revised wording can still be re-established as one exact-text revision of that explicit predecessor.

## Principal falsifiability proof 1 — wrong predecessor digest

Start with a valid 22B revision sidecar.

Replace:

```text
prior_note_reference.note_record_sha256
```

with another valid-looking SHA-256, recompute the outer revision-record digest, and rewrite canonical JSON.

22B verification succeeds by design.

22C then freshly relinks the actual predecessor through 21C and compares durable note identities.

The digests differ.

22C rejects.

Therefore:

```text
22B file integrity
≠
predecessor identity correctness
```

while 22C earns that attachment relationship relative to explicit caller-supplied predecessor evidence.

## Principal falsifiability proof 2 — revised text equal to predecessor

Start with a valid 22B revision sidecar.

Replace the persisted revised human wording with the real predecessor's exact wording, recompute the outer revision-record digest, and rewrite canonical JSON.

22B verification succeeds by design.

22C then:

1. freshly relinks the predecessor through 21C;
2. confirms predecessor identity;
3. passes the persisted revised wording into public 22A.

22A rejects the exact textual no-op.

22C rejects.

Therefore:

```text
22B file integrity
≠
actual revision relative to the real predecessor
```

and successful 22C earns only exact-text revision re-establishment, not semantic difference.

## Exact textual revision is still not semantic change

22A deliberately treats exact string inequality as the narrow revision boundary.

Therefore 22C does not infer whether the revised wording is:

- more correct;
- more important;
- substantively different;
- stronger or weaker;
- supported or contradicted;
- more confident;
- closer to truth.

A whitespace-only difference between two otherwise equal non-whitespace notes may still satisfy 22A because the exact human wording differs.

Thus:

```text
exact textual revision
≠
semantic revision
```

## Exact reconstructed object relationships

Successful 22C preserves:

```text
loaded.revision.prior_note is loaded.prior_note.note
```

and:

```text
loaded.revision.revised_note.working_set
is
loaded.prior_note.note.working_set
```

The reconstructed 22A revision therefore operates over the exact 21C-reconstructed predecessor note and exact working-set object.

The verified 22B evidence remains separately retained.

## The proof chain remains visible

The loaded 22C record keeps three layers distinct:

```text
verification
  = fresh 22B file-local verification

prior_note
  = fresh 21C durable predecessor relinking

revision
  = newly reconstructed 22A human revision
```

These answer different questions.

Thus:

```text
revision-file verification
≠
predecessor relinking
≠
revision-action re-establishment
```

## Paths remain locations, not identities

The 20B working-set sidecar, 21B predecessor-note sidecar, and 22B revision sidecar may move.

The caller supplies their current locations.

If the durable content verifies and the explicit identity relationships match, 22C succeeds.

No path becomes authority.

## Individual member sidecars are not reread

22C reaches the predecessor through 21C.

21C ultimately relies on already-loaded 17D/18D/19D application evidence and does not reread the individual member sidecars.

Therefore those individual sidecars may disappear after their earlier successful relinking while 22C still succeeds, provided the explicit 20B, 21B, and 22B durable artifacts remain available.

This does not make deleted member sidecars recoverable.

## Order and count remain owned by 20C/21C

22C does not weaken the working-set contract.

Supplying the same members in a different order is rejected through the earlier relinking boundary.

Missing or extra members are likewise rejected.

The revision does not turn an ordered working set into a bag.

## No durable chain traversal yet

22C reopens one revision edge:

```text
one explicit durable predecessor note
      ↓
one durable revision edge
```

It does not traverse:

```text
v1 → v2 → v3
```

because a 22B revision artifact is not silently promoted into a 21B note artifact.

22C adds no revision numbers, sequence numbers, predecessor-of-predecessor discovery, next pointers, chronology, DAG semantics, branches, or merges.

One verified revision edge is not a durable revision history.

## Authority boundary

The research authority chain now includes:

```text
source evidence
≠
human selection
≠
human working-set membership
≠
human rationale
≠
human revision of rationale
≠
durable revision representation
≠
verified predecessor attachment
≠
exact-text revision re-establishment
≠
semantic truth
```

22C adds cross-file attachment coherence and exact human-action reconstruction only.

## What successful 22C loading proves

Successful 22C loading proves only that:

1. the caller supplied a 22B sidecar whose bytes freshly satisfy the 22B canonical/self-integrity contract;
2. the caller supplied a 20B/21B predecessor path pair and complete ordered already-loaded member sequence that freshly satisfy 21C;
3. the 22B predecessor format matches the freshly relinked predecessor note format;
4. the 22B predecessor note-record SHA-256 matches the freshly relinked predecessor note identity;
5. the persisted revised human text can be reconstructed through public 22A over the exact 21C predecessor note;
6. that reconstruction satisfies 22A's exact textual no-op rejection;
7. the revised text is preserved verbatim.

This is:

```text
verified durable human revision attachment coherence
relative to one explicit predecessor note and loaded-member sequence
```

## What successful 22C loading does not prove

22C does **not** prove:

- why the researcher revised the note;
- semantic difference beyond exact string inequality;
- that the revised note is more accurate;
- that the predecessor was wrong;
- that either wording is true;
- chronological ordering beyond the explicit predecessor relationship encoded in this one edge;
- trusted time;
- revision numbering;
- complete revision history;
- source support, contradiction, corroboration, entailment, or causation;
- source authenticity or reliability;
- quotation or citation validity;
- claim support;
- authorship identity;
- chain of custody;
- browser freshness;
- machine agreement.

## Focused tests

Eight focused tests cover:

1. successful relinking after moving the 20B parent, 21B predecessor, and 22B revision files, retaining exact supplied member identities and verbatim revised text;
2. rejection of a different but independently valid 21B predecessor after it successfully relinks through 21C;
3. rejection of the recomputed, 22B-valid wrong predecessor digest;
4. rejection of the recomputed, 22B-valid revised text equal to the real predecessor wording;
5. fresh 22B verification, including rejection of changed bytes without a matching digest;
6. successful relinking after all individual member sidecars are deleted;
7. preservation of 21C/20C exact order and count authority;
8. explicit public module importability.

## Explicit non-goals

22C adds no:

- predecessor discovery;
- digest search;
- automatic file lookup;
- revision-chain traversal;
- revision numbers;
- sequence numbers;
- timestamps;
- trusted chronology;
- branch/merge semantics;
- semantic diff;
- confidence model;
- claim model;
- notebook database;
- tags/folders/taxonomy;
- search/ranking/deduplication;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- compiler/RIR/runtime/export/measurement changes;
- researcher UI.

## Decision — D151

**Pyxis may re-establish one durable 22B human working-set-note revision only against one explicit caller-supplied durable 21B predecessor note and its explicit 20B working-set parent. 22C must freshly verify the 22B revision, freshly relink the predecessor through public 21C, require exact durable predecessor format/content-identity agreement, and then reconstruct the human revision through public 22A over the exact 21C predecessor note. A self-consistent 22B file with a wrong predecessor digest must remain 22B-valid but fail 22C. A self-consistent 22B file whose revised text equals the real predecessor wording must remain 22B-valid but fail 22C through 22A's exact no-op boundary. Successful 22C proves only explicit durable predecessor attachment coherence and exact-text human revision re-establishment; it does not establish chronology, semantic difference, truth, authorship, trusted time, chain history, source authority, or machine judgment.**
