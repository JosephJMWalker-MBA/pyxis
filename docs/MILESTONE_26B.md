# Milestone 26B — Durable Explicit Revision-Edge Sequence Declaration

Decision: D161

## Product question

After 26A lets a researcher reopen several already-known durable revision edges in one explicit ordered call, what friction remains at the next restart?

The researcher still has to remember and redeclare the same ordered segment.

26B answers the narrow question:

```text
"I explicitly reopened this exact ordered segment.
I want to preserve that declaration so the order and identities are durable."
```

Pyxis can now persist that declaration without claiming that the segment is:

- complete;
- canonical;
- chronological;
- the latest history;
- a current head;
- the only valid path;
- semantically better than another sequence.

## Why this follows 26A

26A established one application-state record:

```text
starting loaded predecessor
+
explicit ordered edge paths
→
fresh public-24C relinking per member
→
loaded ordered sequence
```

That removes repetitive 24C caller ceremony.

But the human-owned declaration itself disappears with application memory.

26B persists only that declaration's content identities:

```text
starting predecessor format + record SHA-256
+
ordered edge format + record SHA-256 identities
```

No note text, source evidence, browser evidence, filesystem paths, timestamps, revision numbers, or head marker are copied.

## Public API

The new explicit-module API is:

```python
persist_chromium_research_working_set_note_revision_edge_sequence(
    sequence,
    destination,
)
```

and:

```python
verify_chromium_research_working_set_note_revision_edge_sequence(source)
```

with immutable evidence/reference types:

```python
ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference
ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence
```

and file-integrity failure type:

```python
ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence
```

26B does not broaden the `pyxis.app` root export surface.

## Durable format

26B introduces:

```text
pyxis.chromium.research_working_set_note_revision_edge_sequence.v1
```

The canonical document shape is:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1",
  "sequence_record": {
    "edge_references": [
      {
        "format": "pyxis.chromium.research_working_set_note_revision_edge.v1",
        "record_sha256": "<edge digest>"
      }
    ],
    "sequence_mode": "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence",
    "starting_predecessor_reference": {
      "format": "<23B continuation or 24B edge format>",
      "record_sha256": "<starting record digest>"
    }
  },
  "sequence_record_sha256": "<digest of canonical sequence_record>"
}
```

The edge-reference list is non-empty and ordered.

The starting predecessor may be either:

```text
pyxis.chromium.research_working_set_note_revision_continuation.v1
```

or:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

Every sequence member is a 24B edge identity.

## Persistence re-establishes the in-memory declaration

26B does not serialize an arbitrary tuple of hashes.

Persistence requires one exact:

```text
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
```

created under the 26A application boundary.

Before writing, 26B requires:

- the established 26A sequence mode;
- at least one loaded edge;
- a supported already-loaded starting predecessor;
- exact object identity between each loaded edge and the preceding application record;
- each loaded edge's existing bounded local 24C coherence;
- each edge's retained predecessor format and digest to match the preceding record identity.

Thus:

```text
sequence dataclass shape
≠
coherent loaded sequence declaration
```

## No referenced-file reread at persistence time

26B deliberately does not reopen the edge files.

Once 26A has successfully loaded the sequence, the referenced files may be moved or deleted before 26B persistence.

The starting predecessor's durable file may also be gone.

Older sidecars beneath the starting predecessor may likewise be absent.

This follows the same authority principle used by durable research working sets:

```text
already-loaded human declaration
≠
requirement for continued filesystem availability
```

The 26B file is a durable representation of already-established application evidence.

It is not a fresh relinking boundary.

## Retained verification self-integrity is rechecked in memory

Avoiding file rereads must not mean blindly trusting mutable-looking verification fields.

Every loaded 23B or 24B verification record already retains the exact canonical document JSON from its successful file verification.

26B uses that retained evidence to recheck, in memory:

- canonical JSON structure through the existing 23B/24B persisted-document validators;
- the recorded record SHA-256 against a fresh digest of the retained canonical record payload;
- the verification object's retained record digest against that recomputed digest;
- canonical document bytes;
- retained byte count;
- format/mode/predecessor/text fields against the retained canonical payload.

No filesystem read is needed for those checks.

This catches a forged loaded wrapper such as:

```text
real loaded edge
→ replace verification.edge_record_sha256 with another digest
→ attempt 26B persistence
```

The attempt is rejected before destination creation because the replacement digest no longer matches the retained canonical `document_json`.

Therefore:

```text
loaded record type
+
locally coherent object graph
≠
permission to promote an incoherent retained content identity
```

## Retained self-integrity is not authentication

The in-memory self-integrity check does not make the retained document cryptographically authenticated.

A sufficiently privileged caller could construct an entirely new self-consistent Python verification object and matching canonical document JSON.

26B does not claim otherwise.

Thus:

```text
retained canonical self-integrity
≠
authentication
≠
trusted authorship
≠
fresh filesystem verification
```

The purpose of the check is narrower: a simple forged field replacement cannot silently become a durable sequence identity.

## Exact order remains human-owned

26B stores the exact 26A edge order.

It does not sort by:

- path;
- digest;
- creation time;
- text;
- revision depth;
- filename;
- any semantic signal.

If a forged in-memory sequence reverses two already-loaded edges, exact preceding-object identity fails and persistence rejects.

Therefore:

```text
human-declared sequence order
≠
machine-derived ordering
```

## Paths remain locations, not identities

No referenced path is stored in the sequence declaration.

The durable file contains only:

```text
format + record SHA-256
```

for the starting predecessor and each edge.

This means moving an edge file does not mutate the declared identity.

It also means the sequence declaration alone cannot locate that edge later.

Thus:

```text
content identity
≠
filesystem location
```

and:

```text
durable declaration
≠
discovery mechanism
```

## File-only verification is deliberately weaker

`verify_chromium_research_working_set_note_revision_edge_sequence(...)` reads only the 26B declaration file.

It validates:

- UTF-8;
- JSON shape;
- supported sequence format;
- supported sequence mode;
- starting-predecessor reference shape and format;
- non-empty ordered edge-reference list;
- edge-reference format and SHA-256 shape;
- recorded sequence-record digest;
- canonical Pyxis JSON bytes.

It does not open:

- the starting predecessor;
- any edge file;
- any working-set file;
- any note/revision/continuation sidecar;
- any browser capture.

Therefore file-only verification cannot prove attachment coherence.

## Falsifiability proof 1 — wrong starting identity with recomputed digest

Take one valid 26B file.

Change only:

```text
starting_predecessor_reference.record_sha256
```

to another syntactically valid SHA-256.

Then recompute the outer sequence-record SHA-256 and canonical document bytes.

26B file-only verification succeeds intentionally.

Why?

Because the declaration is internally self-consistent and the verifier does not have the starting predecessor object or file.

Thus:

```text
26B file integrity
≠
starting-predecessor correctness
```

## Falsifiability proof 2 — different declared order with recomputed digest

Take a valid two-edge 26B file.

Reverse the two edge references.

Recompute the sequence-record SHA-256 and canonical bytes.

File-only verification succeeds intentionally.

This does not mean the reversed sequence is relinkable.

It proves only that the file consistently declares that order.

Thus:

```text
26B file integrity
≠
edge adjacency correctness
```

and:

```text
stored order
≠
verified historical order
```

A future explicit relinking boundary may compare this declaration against explicit application/file evidence.

26B does not do that.

## Raw tamper still fails

If a sequence reference is changed without recomputing the sequence-record digest, verification rejects.

That is the file-integrity claim 26B does earn.

## Starting from 23C is preserved

26A can begin from either:

- a loaded 23C continuation; or
- a loaded 24C edge.

26B preserves both cases.

For a 23C start, the durable declaration records the exact continuation format and continuation-record SHA-256.

For a 24C start, it records the exact edge format and edge-record SHA-256.

It does not normalize both into a synthetic generic history-node identity.

The original record family remains explicit.

## No source or note duplication

26B does not serialize:

- v1/v2/v3/v4/v5/v6 note wording;
- working-set members;
- paragraph selections;
- exact text ranges;
- comparison-note data;
- browser URL or page evidence;
- source-capture identity;
- filenames or paths.

The declaration stays small and content-addressed.

## Determinism and no overwrite

For the same exact coherent 26A sequence, 26B produces deterministic canonical bytes.

The sequence-record SHA-256 is deterministic.

Two different destination paths receive identical bytes.

Persistence uses exclusive creation.

An existing destination is never silently overwritten.

## What successful 26B persistence proves

Successful persistence establishes only:

> One exact coherent already-loaded 26A sequence declaration was represented as canonical deterministic content-addressed JSON after its retained application relationships and retained verification self-integrity were rechecked in memory.

Nothing stronger is implied.

## What successful 26B persistence does not prove

26B does not establish:

- fresh availability of any referenced file;
- future relinkability;
- complete ancestry;
- earliest revision;
- latest revision;
- chronology;
- trusted time;
- current head;
- uniqueness of successor;
- global linearity;
- absence of sibling edges;
- branch structure;
- merge structure;
- cycle absence elsewhere;
- directory completeness;
- path discovery;
- digest discovery;
- semantic improvement;
- source truth;
- claim support;
- citation validity;
- authorship authentication.

## Authority boundary

26B preserves the separation:

```text
24C local loaded edge evidence
≠
26A caller-declared ordered relinked segment
≠
26B durable declaration of that segment
≠
26B file-only integrity
≠
future sequence relinking
≠
canonical history
≠
semantic truth
```

The key new statement is:

```text
human-declared durable ordering
≠
history authority
```

## Focused test contract

The 26B focused tests prove:

1. persistence stores only the starting predecessor identity and ordered edge identities;
2. no edge/note text or filesystem path is copied;
3. an explicit loaded 23C continuation may be the starting predecessor;
4. persistence succeeds after all referenced edge files and older sidecars are removed;
5. a forged retained loaded-edge digest is rejected before write by in-memory retained-document self-integrity;
6. forged in-memory edge order is rejected before write;
7. raw file tamper without digest recomputation is rejected;
8. a recomputed wrong starting-predecessor digest passes file-only verification intentionally;
9. a recomputed different declared edge order passes file-only verification intentionally;
10. deterministic bytes, no-overwrite behavior, wrong-type rejection, explicit-module importability, and empty-edge-list verification rejection remain explicit.

## Scope exclusions

26B makes no changes to:

- 23B persistence or verification;
- 24B edge format or verification;
- 24C edge relinking;
- 25A human edge extension;
- 25B successor-edge persistence;
- 26A sequence relinking;
- root exports;
- README;
- `docs/CURRENT_STATE.md`;
- browser acquisition;
- Chromium DevTools behavior;
- research capture;
- working-set membership;
- LLM behavior;
- compiler/RIR/runtime/export/measurement behavior;
- researcher UI;
- directory scanning;
- digest search;
- path discovery;
- automatic traversal;
- current-head semantics;
- timestamps;
- chronology;
- branch/merge semantics;
- whole-history validation.

## Decision D161

**Persist one already-loaded explicit 26A revision-edge sequence as a minimal ordered content-addressed declaration. Re-establish the sequence's bounded in-memory relationships and recheck retained canonical verification self-integrity without rereading referenced files. Keep standalone verification deliberately file-local so durable declaration integrity remains separate from predecessor/adjacency authority, path discovery, chronology, current-head semantics, and semantic truth.**
