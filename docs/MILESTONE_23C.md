# Milestone 23C — Verified Revision Continuation Relinking

Decision: D154

## Product question

Can Pyxis reopen one durable 23B human revision continuation only after proving that it references the exact caller-supplied durable 22B predecessor revision and that the persisted v3 wording can still be re-established as an actual human revision of the freshly reconstructed v2 note?

23C answers **yes**.

## Why this milestone exists

23B deliberately separated file integrity from cross-file authority.

A 23B file can prove:

```text
"these bytes are canonical and self-consistent"
```

without proving:

```text
"this predecessor digest names the supplied durable revision"
```

or:

```text
"this persisted v3 wording is still different from the real v2 wording"
```

That separation is intentional.

23C earns those two relationships again at load time.

## Public module API

```python
load_chromium_research_working_set_note_revision_continuation(
    items,
    working_set_source,
    prior_note_source,
    prior_revision_source,
    continuation_source,
)
```

returns:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord(
    verification=<fresh 23B verification>,
    prior_revision=<fresh 22C loaded revision>,
    continuation=<freshly reconstructed 23A continuation>,
)
```

The module also exposes:

```python
ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError
```

The API lives in:

```text
pyxis.app.chromium_research_working_set_note_revision_continuation_load
```

23C does not broaden the `pyxis.app` root export surface.

## Authority layers remain separate

The loaded record intentionally retains three distinct forms of evidence:

1. fresh 23B file-local verification;
2. fresh 22C predecessor relinking;
3. fresh 23A human continuation reconstruction.

These are not collapsed into one authority claim.

Thus:

```text
23B file integrity
≠
22B predecessor attachment coherence
≠
actual human continuation re-establishment
```

## Load sequence

23C performs the following steps in order.

### 1. Snapshot the caller-supplied member sequence

The caller supplies the complete ordered sequence of already-loaded 17D/18D/19D research records.

23C snapshots that iterable to a tuple.

It does not sort, deduplicate, discover, or replace members.

### 2. Freshly verify the 23B continuation sidecar

Public:

```python
verify_chromium_research_working_set_note_revision_continuation(...)
```

is called first.

This re-establishes only canonical structure and self-integrity of the 23B file.

### 3. Freshly relink the explicit 22B predecessor revision

Public:

```python
load_chromium_research_working_set_note_revision(...)
```

is then called with:

- the exact caller-supplied member sequence;
- the explicit 20B working-set sidecar;
- the explicit 21B predecessor-note sidecar;
- the explicit 22B predecessor-revision sidecar.

That invokes the already-earned 20C/21C/22C boundaries rather than duplicating them.

### 4. Match the persisted predecessor revision identity

23C compares:

```text
23B persisted predecessor revision format
```

with:

```text
fresh 22C predecessor revision format
```

and constant-time compares:

```text
23B persisted predecessor revision-record SHA-256
```

with:

```text
fresh 22C predecessor revision-record SHA-256
```

A valid durable revision is not sufficient.

It must be the exact durable revision referenced by this continuation record.

Therefore:

```text
valid predecessor revision
≠
correct predecessor revision for this continuation
```

### 5. Reconstruct the human continuation through public 23A

Only after predecessor identity matches does 23C call:

```python
create_chromium_research_working_set_note_revision_continuation(
    loaded_prior,
    revised_note_text=verification.revised_note_text,
)
```

Public 23A then delegates actual revision creation to public 22A.

That means an exact:

```text
v2 → v2
```

no-op cannot re-enter typed application state through 23C.

The persisted text must again satisfy the already-earned exact-text human revision boundary.

## Exact object relationships

For a successful result:

```text
loaded.continuation.prior_revision
is
loaded.prior_revision
```

and:

```text
loaded.continuation.revision.prior_note
is
loaded.prior_revision.revision.revised_note
```

and:

```text
loaded.continuation.revision.revised_note.working_set
is
loaded.prior_revision.revision.revised_note.working_set
```

The newly reconstructed continuation therefore points to the exact predecessor object created by the fresh 22C load.

## Falsifiability proof 1 — wrong predecessor digest with valid 23B integrity

Start with a valid 23B sidecar.

Replace the persisted predecessor revision digest with another valid-looking SHA-256.

Recompute the outer 23B continuation-record digest and canonical JSON.

Public 23B verification succeeds by design.

23C then freshly loads the real caller-supplied 22B predecessor and compares its verified durable identity against the forged 23B predecessor reference.

23C rejects.

This proves:

```text
23B file integrity
≠
predecessor attachment coherence
```

## Falsifiability proof 2 — different but independently valid predecessor

Start with one valid durable 23B continuation referencing revision A.

Create another independently valid 22B revision B over the same earlier note.

Supply revision B to 23C.

Public 22C successfully relinks B.

23C still rejects because B's durable revision identity differs from the predecessor identity persisted by the continuation.

This proves the new authority is genuinely owned by 23C rather than merely inherited from 22C failure.

## Falsifiability proof 3 — v3 changed back to exact real v2

Start with a valid 23B continuation whose v3 wording differs from v2.

Change persisted v3 text to the exact real v2 wording.

Recompute the 23B continuation-record SHA-256 and canonical JSON.

Public 23B verification succeeds by design.

23C then freshly relinks the real predecessor and asks public 23A/22A to reconstruct the continuation.

The exact no-op is rejected.

Thus:

```text
23B file integrity
≠
proof that the persisted wording remains an actual continuation
```

and successful 23C relinking earns that exact-text relationship again.

## Fresh integrity failure remains a 23B concern

If the 23B text or predecessor reference is changed without recomputing the outer digest, fresh 23B verification fails before predecessor relinking occurs.

23C does not replace or weaken 23B integrity authority.

## Paths remain locations, not identities

The caller may move:

- the 20B working-set sidecar;
- the 21B predecessor-note sidecar;
- the 22B predecessor-revision sidecar;
- the 23B continuation sidecar.

If the new paths are explicitly supplied and durable identities still match, 23C succeeds.

No historical path is required.

Therefore:

```text
path location
≠
durable identity
```

## Individual member sidecars are still not reread

23C ultimately relinks the predecessor through 22C using already-loaded member records.

The 17C/18C/19C member sidecars may therefore have disappeared after their earlier successful relinking.

23C can still succeed if:

- the already-loaded member records are supplied;
- the 20B working-set sidecar is available;
- the 21B note sidecar is available;
- the 22B revision sidecar is available;
- the 23B continuation sidecar is available.

This proves only:

```text
current individual member-sidecar availability
≠
23C relinking against already-loaded members
```

It does not perform fresh 17D/18D/19D member relinking.

## Caller member order remains authoritative

The complete ordered member sequence remains explicit caller input.

A wrong order is rejected through the existing 20C/21C/22C chain.

23C does not reorder, auto-swap, search, or discover members.

Therefore:

```text
successful continuation relinking
≠
automatic working-set discovery
```

## No recursive continuation history

23C reopens exactly:

```text
one 22B predecessor revision
      ↓
one 23B continuation
```

It does not make a 23B continuation into a new durable predecessor format.

It does not define:

```text
23B continuation
      ↓
23B continuation
```

or traverse:

```text
v1 → v2 → v3 → v4 → ...
```

No recursive history representation, branch semantics, DAG semantics, predecessor discovery, successor discovery, or automatic chain traversal is introduced.

Thus:

```text
verified continuation edge
≠
revision-history engine
```

## No chronology authority

23C establishes an explicit predecessor relationship, not trusted time.

It introduces no:

- timestamp;
- trusted clock;
- revision number;
- sequence number;
- monotonic counter;
- elapsed duration;
- global ordering.

Therefore:

```text
explicit predecessor relationship
≠
trusted chronology
```

## No semantic authority

Successful 23C relinking does not mean v3 is:

- more correct;
- less correct;
- stronger;
- weaker;
- more supported;
- less supported;
- more certain;
- less certain;
- contradictory;
- corroborated;
- improved;
- closer to truth.

It establishes only exact durable attachment and exact-text human revision coherence.

## Successful 23C proves only

A successful 23C result proves that:

1. the supplied 23B sidecar is freshly file-integrity-valid;
2. the supplied complete ordered already-loaded member sequence supports fresh predecessor relinking through the existing 20C/21C/22C chain;
3. the explicit supplied 22B predecessor's durable format matches the predecessor format referenced by 23B;
4. the explicit supplied 22B predecessor's durable content identity matches the predecessor identity referenced by 23B;
5. the persisted v3 human wording can be freshly reconstructed through public 23A/22A as an actual exact-text revision of the v2 note produced by that predecessor;
6. the reconstructed continuation retains the exact fresh 22C predecessor object;
7. the reconstructed revision retains the exact v2 note object from that predecessor;
8. the persisted human text is preserved verbatim.

This is:

```text
verified durable continuation attachment coherence
```

## Successful 23C does not prove

23C does **not** prove:

- trusted chronology;
- authorship identity;
- why the researcher changed wording;
- semantic significance of the textual change;
- that v3 is better than v2;
- that v2 is better than v1;
- truth;
- source support;
- contradiction;
- corroboration;
- entailment;
- causation;
- relevance;
- completeness;
- source authenticity;
- citation validity;
- quotation validity;
- chain of custody;
- fresh browser observation;
- fresh member relinking;
- recursive revision history;
- predecessor or successor discovery;
- revision numbering;
- machine agreement.

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
human revision
≠
durable revision representation
≠
verified revision relinking
≠
explicit human continuation
≠
durable continuation representation
≠
verified continuation relinking
≠
semantic truth
```

The governing principle remains:

**Integrity is not authority.**

23C adds only the authority needed to re-establish one durable human continuation edge against one explicit caller-supplied durable predecessor.

It adds nothing more.
