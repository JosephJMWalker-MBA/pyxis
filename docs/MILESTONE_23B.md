# Milestone 23B — Durable Revision Continuation

Decision: D153

## Product question

Can Pyxis make one 23A human continuation durable only after proving that the continuation really points to the caller's explicit durable 22B predecessor revision, without turning that one edge into an automatically traversable revision history?

23B answers **yes**.

## Why this milestone exists

23A established one application-state relationship:

```text
verified durable v1 → v2 revision
            ↓
explicit human continuation
            ↓
v3 wording
```

That relationship was intentionally in-memory only.

If the process ended, the stronger statement:

```text
"this v3 wording explicitly continued this exact verified v2 revision"
```

was lost.

23B makes exactly that continuation edge durable.

It does not make a revision history engine.

## Public module API

The new explicit-module API is:

```python
persist_chromium_research_working_set_note_revision_continuation(
    continuation,
    working_set_source,
    prior_note_source,
    prior_revision_source,
    destination,
)
```

and:

```python
verify_chromium_research_working_set_note_revision_continuation(source)
```

with evidence types:

```python
ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence
ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence
```

and file-integrity failure type:

```python
ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError
```

The API lives in:

```text
pyxis.app.chromium_research_working_set_note_revision_continuation_persistence
```

23B does not broaden the `pyxis.app` root export surface.

## Durable format

The file format is:

```text
pyxis.chromium.research_working_set_note_revision_continuation.v1
```

The canonical continuation record is:

```json
{
  "prior_revision_reference": {
    "format": "pyxis.chromium.research_working_set_note_revision.v1",
    "revision_record_sha256": "<64-hex>"
  },
  "continuation": {
    "mode": "caller_authored_continuation_of_verified_research_working_set_note_revision",
    "revision": {
      "mode": "caller_authored_revision_of_research_working_set_note",
      "revised_note": {
        "mode": "caller_authored_note_on_research_working_set",
        "text": "<verbatim v3 human wording>"
      }
    }
  }
}
```

The outer document is:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision_continuation.v1",
  "continuation_record": { "...": "..." },
  "continuation_record_sha256": "<sha256 of canonical continuation_record>"
}
```

JSON is deterministic, canonical, UTF-8, newline terminated, and no-overwrite.

## What is deliberately not serialized

23B does not copy:

- v1 human wording;
- v2 human wording;
- 21B predecessor-note identity;
- 20B working-set identity;
- working-set members;
- member kinds or member digests;
- paragraph ordinals;
- text coordinates;
- selected source text;
- URLs or titles;
- source captures;
- browser evidence;
- filesystem paths;
- timestamps;
- authorship identity;
- semantic analysis.

The 22B predecessor revision already has its own durable attachment to the earlier note. 23B references that revision by durable content identity rather than duplicating its internal graph.

Thus:

```text
reference to durable predecessor
≠
duplication of predecessor state
```

## Persistence requires an actual durable predecessor

23A can exist after every related file disappears because it consumes already-loaded application evidence.

23B is different.

To make that continuation durable, the caller must provide current paths for:

1. the 20B working-set sidecar;
2. the 21B predecessor-note sidecar;
3. the 22B predecessor-revision sidecar;
4. the new 23B destination.

Before writing anything, 23B calls public 22C using the exact already-loaded member sequence retained by the 23A predecessor.

That freshly re-establishes:

```text
20B working-set verification
+
20C ordered working-set relinking
+
21B note verification
+
21C note attachment relinking
+
22B revision verification
+
22C predecessor attachment + exact-text revision reconstruction
```

23B does not duplicate those earlier boundaries.

## The new 23B predecessor check

After public 22C succeeds, 23B compares:

```text
fresh durable predecessor revision format
fresh durable predecessor revision-record SHA-256
```

against the corresponding retained verification facts inside the exact loaded 22C object carried by the 23A continuation.

The SHA comparison uses constant-time comparison.

A different but perfectly valid 22B revision may successfully load through 22C and still be rejected by 23B because it is not the revision the 23A continuation actually continued.

Therefore:

```text
valid durable revision
≠
correct durable predecessor for this continuation
```

## The live 23A contract is re-established first

The outer continuation dataclass is not trusted merely because it has the correct Python type.

23B first reconstructs the live continuation through public 23A using:

```text
exact retained loaded 22C predecessor
+
exact v3 wording from the supplied continuation
```

This reuses 23A's in-memory predecessor-coherence checks and 22A's exact no-op boundary.

23B then checks the retained continuation and revision modes and exact object relationships.

Therefore:

```text
23A dataclass shape
≠
valid live continuation contract
```

## Exact member identity remains caller-owned

The fresh 22C load is given the exact ordered member sequence retained by the supplied 23A predecessor.

After the fresh load, 23B verifies that the loaded predecessor continues to retain those same member objects in the same count and order.

23B does not sort, deduplicate, discover, or substitute members.

Thus:

```text
continuation persistence
≠
new working-set membership decision
```

## Individual member sidecars are not reread

Public 22C ultimately operates on already-loaded 17D/18D/19D member evidence through the existing 20C/21C boundaries.

Therefore individual member sidecars may disappear after their earlier successful relinking while 23B persistence still succeeds, provided the explicit 20B, 21B, and 22B durable artifacts remain available.

This proves only:

```text
current member-sidecar availability
≠
ability to establish this durable continuation edge
```

It does not make deleted member artifacts recoverable.

## Paths remain locations, not identities

The caller may move the 20B, 21B, or 22B files before 23B persistence.

If the caller supplies the new paths and all durable identities relink correctly, persistence succeeds.

No path is serialized into the 23B file.

Thus:

```text
path location
≠
durable identity
```

## File-only verification remains deliberately weaker

`verify_chromium_research_working_set_note_revision_continuation(...)` reads only the 23B file.

It validates:

- UTF-8;
- exact schema;
- supported format;
- supported modes;
- non-whitespace human text;
- SHA-256 shapes;
- continuation-record SHA-256;
- canonical bytes.

It does not open:

- the referenced 22B revision;
- the 21B note;
- the 20B working set;
- member sidecars;
- source captures;
- browser state.

Therefore file-local verification does not establish cross-file attachment correctness.

## Falsifiability proof 1 — wrong predecessor revision digest

Start with a valid 23B file.

Replace:

```text
prior_revision_reference.revision_record_sha256
```

with another valid-looking SHA-256.

Recompute the outer continuation-record digest and rewrite canonical JSON.

23B verification succeeds by design.

Therefore:

```text
23B file integrity
≠
predecessor revision identity correctness
```

A later relinking boundary must earn that relationship again.

## Falsifiability proof 2 — v3 changed back to real v2 wording

Start with a valid 23B file whose v3 wording differs from the real predecessor v2 wording.

Replace the persisted v3 text with the exact real v2 text.

Recompute the outer continuation-record digest and rewrite canonical JSON.

23B verification succeeds by design because it does not open the predecessor revision.

Therefore:

```text
23B file integrity
≠
proof that persisted v3 is still an actual revision of the real v2 predecessor
```

A later relinker must re-establish the human continuation action through public boundaries.

## Persistence-time no-op authority still comes from 23A/22A

At initial persistence time, the caller supplies a live 23A record.

23B re-establishes that record through public 23A before writing.

Public 23A delegates the new revision creation to public 22A.

Therefore an exact v2 → v2 no-op is rejected before a valid 23B file can be created through the public persistence API.

The falsified file-only case above demonstrates why that creation-time fact cannot be inferred merely from later file integrity.

## No recursive continuation format yet

23B persists:

```text
one 22B revision
      ↓
one 23B continuation
```

It does not yet define:

```text
23B continuation
      ↓
next 23B continuation
```

The predecessor reference is intentionally a 22B revision identity, not a union of arbitrary predecessor formats.

This means 23B does not silently decide:

- recursive history representation;
- branch semantics;
- merge semantics;
- revision DAG semantics;
- successor discovery;
- predecessor discovery;
- chain traversal;
- global ordering.

Those decisions require separate product pressure and a separate authority boundary.

Thus:

```text
one durable continuation edge
≠
durable revision history
```

## No chronology authority

The terms `prior` and `continuation` encode the explicit relationship chosen by the human and carried by the supplied objects.

23B adds no:

- wall-clock timestamp;
- trusted clock;
- revision number;
- sequence number;
- monotonic counter;
- elapsed duration;
- global order.

Therefore:

```text
explicit predecessor relationship
≠
trusted chronology
```

## No semantic authority

23B does not infer whether v3 is:

- better;
- worse;
- more accurate;
- more supported;
- less supported;
- contradictory;
- corroborated;
- more confident;
- less confident;
- closer to truth.

It records only durable human wording attached to one explicit predecessor revision identity.

## Integrity remains distinct from authority

The authority chain now includes:

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
semantic truth
```

23B adds durable representation only.

## What successful 23B persistence proves

Successful persistence proves only that, at write time:

1. the caller supplied one live 23A continuation;
2. that continuation re-established successfully through public 23A;
3. the caller supplied explicit readable 20B, 21B, and 22B predecessor artifacts;
4. public 22C freshly relinked those artifacts against the exact supplied loaded member sequence;
5. the freshly loaded 22B revision identity matched the retained 22C predecessor identity inside the 23A continuation;
6. exact member count/order/object identity remained coherent;
7. the v3 wording was valid human text and an exact-text revision under the existing 23A/22A contract;
8. the 23B file was written canonically without overwriting an existing destination.

This is:

```text
one durably represented explicit continuation edge
```

## What successful 23B verification proves

File-only verification proves only:

1. canonical 23B structure;
2. supported formats and modes;
3. SHA-256 shape validity;
4. continuation-record self-integrity;
5. canonical bytes;
6. retained v3 human text exactly as stored.

It does not prove that the referenced predecessor is the intended real predecessor.

## What 23B does not prove or do

23B does **not** prove or perform:

- predecessor authenticity;
- authorship authentication;
- trusted time;
- chain of custody;
- source truth;
- semantic difference;
- semantic improvement;
- claim support;
- contradiction or corroboration;
- quotation authority;
- citation authority;
- automatic predecessor discovery;
- automatic successor discovery;
- chain traversal;
- recursive continuation persistence;
- revision numbering;
- branch or merge semantics;
- notebook-schema changes;
- browser acquisition;
- LLM interpretation;
- compiler/RIR/runtime/export changes;
- researcher UI changes.

## Decision D153

Pyxis may persist one 23A human revision continuation only after freshly re-establishing the supplied durable 22B predecessor through public 22C and matching that fresh predecessor content identity to the exact verified revision retained by the live continuation.

The resulting 23B sidecar stores only:

```text
predecessor 22B revision content identity
+
explicit continuation mode
+
continued 22A revision mode
+
verbatim v3 human wording
```

Its SHA-256 establishes file-local self-integrity only.

It does not establish predecessor correctness, chronology, semantic change, or a durable revision history.
