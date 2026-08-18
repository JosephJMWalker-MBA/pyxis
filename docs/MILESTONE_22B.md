# Milestone 22B — Durable Working-Set Note Revision

## Product question

Can Pyxis preserve one explicit 22A human change-of-mind action durably without mutating the predecessor note, duplicating the working-set evidence graph, inventing chronology, or pretending file integrity proves that the predecessor relationship is correct?

22B answers **yes**.

## Why this milestone exists

21A–21C established a complete durable rationale loop:

```text
20A working set
 ↓
21A human rationale
 ↓
21B durable rationale
 ↓
21C verified rationale relinking
```

22A then added the next human action:

```text
prior rationale
 ↓
explicit human revision
 ↓
revised rationale
```

while preserving the prior note unchanged.

But 22A is application-state only.

If the process ends, the fact that the researcher changed the wording disappears even if both note texts were meaningful during the session.

22B adds one narrow durable representation of that revision action.

## Public module API

```python
persist_chromium_research_working_set_note_revision(
    revision,
    working_set_source,
    prior_note_source,
    destination,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence(...)
```

and:

```python
verify_chromium_research_working_set_note_revision(source)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence(...)
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_note_revision_persistence
```

22B does not broaden the `pyxis.app` root re-export surface.

## Durable format

22B writes:

```text
pyxis.chromium.research_working_set_note_revision.v1
```

with canonical JSON shaped as:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision.v1",
  "revision_record": {
    "prior_note_reference": {
      "format": "pyxis.chromium.research_working_set_note.v1",
      "note_record_sha256": "..."
    },
    "revision": {
      "mode": "caller_authored_revision_of_research_working_set_note",
      "revised_note": {
        "mode": "caller_authored_note_on_research_working_set",
        "text": "..."
      }
    }
  },
  "revision_record_sha256": "..."
}
```

The outer SHA-256 is computed over canonical `revision_record` bytes.

As elsewhere in Pyxis, SHA-256 is used only for self-integrity/content identity.

It is not authentication, authorship, trusted time, or chain of custody.

## The durable revision stores only the predecessor identity and new wording

22B deliberately does **not** copy the predecessor note text.

It stores only:

```text
predecessor note format
predecessor note-record SHA-256
revision mode
revised note mode
revised human text
```

It does not store:

- the predecessor human wording;
- the 20B working-set reference;
- working-set members;
- paragraph ordinals;
- exact-range coordinates;
- comparison members;
- source capture identities;
- source text;
- browser evidence;
- filesystem paths.

The predecessor 21B note remains the durable owner of its own wording and parent relationship.

Thus:

```text
durable predecessor note
≠
durable revision action
```

and:

```text
revision persistence
≠
second note/evidence store
```

## Persistence requires an actual durable predecessor

22B does not permit one purely in-memory 22A revision to become durable while its predecessor remains ephemeral.

The caller must explicitly supply:

1. one 22A revision record;
2. the current path of the predecessor's 20B working-set sidecar;
3. the current path of the predecessor's 21B working-set-note sidecar;
4. one new destination path.

Persistence calls public 21C using the exact member sequence retained by `revision.prior_note`.

That means the predecessor is freshly re-established through:

```text
21B note verification
+
20C parent relinking
+
21C note-to-parent attachment verification
```

before 22B writes anything.

## 22A is re-established before persistence

The supplied revision is not trusted merely because it has the expected dataclass type.

22B recreates the operation through public 22A using:

```python
create_chromium_research_working_set_note_revision(
    revision.prior_note,
    revised_note_text=revision.revised_note.note_text,
)
```

That reuses:

- 22A revision-mode authority;
- 21A note-mode authority;
- 20A working-set coherence authority;
- the exact textual no-op rejection.

The validation result is not substituted for the caller's record.

Persistence evidence retains the exact supplied 22A revision object.

Thus:

```text
re-establish operation validity
≠
replace caller-owned revision object
```

## The durable predecessor must match the 22A predecessor

After public 21C succeeds, 22B compares the freshly reconstructed predecessor note against `revision.prior_note`.

The following must agree:

```text
note mode
exact human text
complete ordered loaded-member sequence
```

The supplied member objects are retained position-by-position through 21C.

A different but perfectly valid durable 21B note over the same working set is therefore rejected if its human wording differs from the 22A predecessor.

This proves:

```text
valid durable note
≠
correct predecessor for this revision
```

The destination is not created when that check fails.

## Paths remain locations, not identities

The caller supplies current locations for the 20B working set and 21B predecessor note.

Both files may move before 22B persistence.

If their content verifies and relinks correctly, persistence succeeds.

No supplied path is serialized into the revision record.

Therefore:

```text
filesystem location
≠
durable predecessor identity
```

## Individual member sidecars are not reread

22B reaches the predecessor through 21C.

21C uses already-loaded 17D/18D/19D member evidence and does not reread individual member note sidecars.

Therefore the individual member sidecars may disappear after their earlier successful relinking and 22B may still persist the revision, provided the explicit 20B working-set and 21B predecessor-note sidecars remain available.

This proves only:

```text
current individual member-sidecar availability
≠
ability to persist a revision against already-loaded member evidence
```

It does not make deleted member sidecars recoverable.

## File-only verification is deliberately weaker than predecessor relinking

`verify_chromium_research_working_set_note_revision(...)` opens only the 22B revision sidecar.

It does not open:

- the referenced 21B predecessor note;
- the referenced 20B working set;
- individual member sidecars;
- source captures;
- browser state.

It verifies only:

- UTF-8;
- JSON shape;
- exact supported format strings;
- exact supported revision/note modes;
- SHA-256 field shape;
- non-whitespace revised human text;
- canonical bytes;
- outer revision-record self-integrity.

This deliberately creates two falsifiable gaps.

## Falsifiability proof 1 — wrong predecessor identity can remain file-valid

Starting from a valid 22B sidecar:

```text
replace prior_note_reference.note_record_sha256
with another valid-looking 64-hex digest
 ↓
recompute revision_record_sha256
 ↓
rewrite canonical JSON
```

22B file verification succeeds.

That is correct behavior.

The file is internally self-consistent, but file-only verification has no external predecessor evidence against which to judge the reference.

Therefore:

```text
22B file integrity
≠
predecessor note identity correctness
```

## Falsifiability proof 2 — a self-consistent file may no longer describe an actual revision

Starting from a valid 22B sidecar:

```text
replace revised_note.text
with the real predecessor's exact text
 ↓
recompute revision_record_sha256
 ↓
rewrite canonical JSON
```

22B file verification also succeeds.

This too is correct behavior.

The predecessor text is deliberately not duplicated in the revision sidecar and the verifier does not open the predecessor.

Therefore it cannot establish exact inequality between predecessor and revised wording.

Thus:

```text
22B file integrity
≠
actual human revision relative to the real predecessor
```

A later explicit relinking boundary must earn both predecessor identity and revision validity.

## Persistence-time validity and verification-time validity are different claims

At persistence time, Pyxis has explicit access to:

```text
22A live revision
+
21B predecessor sidecar
+
20B parent sidecar
+
already-loaded members
```

It can therefore require a real predecessor match and re-establish 22A's no-op boundary.

At file-only verification time, Pyxis has only:

```text
22B revision sidecar bytes
```

It cannot honestly make the same claim.

Thus:

```text
successful persistence
≠
what can later be proven from the revision file alone
```

This distinction is intentional.

## No durable revision chain yet

22A permits an in-memory sequence such as:

```text
v1 → v2 → v3
```

22B persists **one revision edge** against one explicit durable 21B predecessor note.

It does not automatically make a 22B revision file behave like a 21B note file.

It does not create:

- revision numbers;
- sequence numbers;
- a previous-revision pointer;
- a next-revision pointer;
- durable chronological ordering;
- a revision DAG;
- branch/merge semantics.

A later milestone may decide how durable revision edges should be reopened or composed.

22B does not prejudge that design.

Therefore:

```text
one durable revision action
≠
durable revision history
```

## Deterministic persistence and no overwrite

For the same valid inputs, 22B produces the same canonical bytes and revision-record SHA-256.

Persistence uses exclusive creation.

An existing destination is never overwritten.

Therefore old durable revision bytes are not silently replaced by a later action.

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
predecessor re-establishment
≠
semantic truth
```

22B adds durable human-action provenance only.

It does not upgrade the truth status of either wording.

## What successful 22B persistence proves

Successful persistence proves only that, at write time:

1. the caller supplied one 22A revision record;
2. that revision re-established through 22A/21A/20A;
3. the caller supplied one 20B parent path and one 21B predecessor-note path;
4. the predecessor freshly relinked through 21C against the exact loaded members retained by the 22A predecessor;
5. the relinked predecessor human note matched the 22A predecessor mode and exact wording;
6. the revised note retained the same exact in-memory working-set object as the prior note;
7. the revised wording remained a genuine exact-text revision under 22A's rules;
8. Pyxis wrote a new canonical, no-overwrite revision sidecar containing only predecessor durable identity plus revised human wording;
9. persistence evidence retained the exact supplied 22A revision object.

This is:

```text
durable representation of one validated human revision action
against one explicit durable predecessor note
```

## What file-only 22B verification proves

Successful verification proves only that:

1. the supplied bytes are valid UTF-8 and JSON;
2. the document has the exact 22B shape;
3. format and mode strings are supported;
4. digest fields have valid SHA-256 shape;
5. revised text is non-whitespace human text;
6. the persisted revision record matches its recorded SHA-256;
7. the full document uses canonical Pyxis JSON bytes.

It does **not** prove that the predecessor digest is correct or that revised text actually differs from that predecessor.

## What 22B does not prove

22B does **not** prove:

- that the predecessor note reference is correct from file bytes alone;
- that the revised wording differs from the real predecessor from file bytes alone;
- why the researcher changed wording;
- that the revised wording is better or more accurate;
- that the predecessor wording was wrong;
- that either wording is true;
- semantic difference beyond 22A's creation-time exact string inequality;
- source support, contradiction, corroboration, entailment, or causation;
- relevance, completeness, or representativeness;
- source authenticity or reliability;
- citation or quotation validity;
- claim support;
- authorship identity;
- trusted time or chronology;
- chain of custody;
- current individual member-file availability;
- browser freshness;
- machine agreement.

## Focused tests

Nine focused tests cover:

1. minimal identity-only predecessor reference plus verbatim revised Unicode/multiline text, exact live revision identity retention, and absence of copied predecessor/member/working-set/path data;
2. persistence after predecessor and parent paths move, proving paths are locations rather than identities;
3. rejection of a different but valid durable predecessor before destination creation;
4. successful persistence after individual member sidecars are deleted, proving no hidden member-file reread;
5. rejection when persisted bytes change without a matching revision-record digest;
6. acceptance by file-only verification after predecessor digest replacement plus recomputed outer digest;
7. acceptance by file-only verification after revised text is changed to the real predecessor wording plus recomputed outer digest;
8. deterministic canonical persistence and no-overwrite behavior;
9. explicit public importability through the 22B module.

## Explicit non-goals

22B adds no:

- revision relinking;
- revision discovery;
- revision-chain traversal;
- revision IDs beyond the file's content digest;
- revision numbers;
- timestamps;
- trusted chronology;
- authorship verification;
- reason-for-change field;
- semantic diff;
- confidence model;
- claims;
- notebook database;
- taxonomy;
- search/ranking/deduplication;
- embeddings;
- LLM interpretation;
- browser work;
- compiler/RIR/runtime/export/measurement changes;
- researcher UI.

## Decision — D150

**Pyxis may persist one 22A human working-set-note revision only after freshly re-establishing the supplied live revision through public 22A and freshly relinking one explicit durable 21B predecessor note through public 21C against the predecessor's exact loaded-member sequence and explicit 20B parent sidecar. The durable revision format stores only the predecessor note format/content identity plus the exact revision mode and revised human note mode/text. It does not duplicate predecessor wording, working-set evidence, source evidence, or paths. File-only verification proves canonical self-integrity only and deliberately does not open the predecessor. Therefore a structurally valid wrong predecessor digest, or revised text changed to equal the real predecessor text, may remain file-valid after the revision-record digest is recomputed. Successful 22B persistence is one durable validated revision action, not durable revision-chain authority, trusted chronology, semantic improvement, or truth.**
