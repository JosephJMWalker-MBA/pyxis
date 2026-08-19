# Milestone 24C — Verified General Revision-Edge Relinking

Decision: D157

## Product question

After 24B introduced one repeatable durable revision-edge format, can Pyxis reopen one edge against one explicit already-loaded predecessor without discovering, traversing, or globally ordering revision history?

24C answers **yes**.

The caller supplies exactly two things:

```text
one already-loaded predecessor
+
one explicit 24B edge sidecar
```

The predecessor may be either:

```text
one loaded 23C continuation
```

or:

```text
one already-loaded 24C edge
```

Pyxis freshly verifies only the edge being opened, matches its persisted content-addressed predecessor reference against the exact predecessor object supplied by the caller, and then reconstructs one exact-text 22A human revision over that predecessor's exact endpoint note.

This creates a repeatable **explicit edge-by-edge loading boundary** without introducing automatic history traversal.

## Why 24C exists

24B deliberately separated:

```text
repeatable durable edge representation
```

from:

```text
verified predecessor attachment
```

A valid 24B file can contain:

- a wrong but well-formed predecessor digest;
- revised wording equal to the real predecessor wording;
- a same-24B-format predecessor reference whose target does not exist.

Those files can still pass 24B file-only verification by design.

24C adds only the next researcher action:

```text
"I have this predecessor already loaded. Reopen this exact edge against it."
```

It does not ask Pyxis to find the predecessor.

## Public API

The new explicit-module API is:

```python
load_chromium_research_working_set_note_revision_edge(
    predecessor,
    edge_source,
)
```

and:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_load
```

24C does not broaden the `pyxis.app` root export surface.

## Loaded record

Successful loading returns:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord(
    verification=<fresh 24B file verification>,
    predecessor=<exact caller-supplied loaded predecessor>,
    revision=<fresh 22A revision over predecessor endpoint>,
)
```

The exact predecessor object is retained.

Thus:

```text
same predecessor wording
≠
explicit attachment to this loaded predecessor object
```

## Supported predecessor application records

24C accepts exactly:

```text
ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
```

from 23C, or:

```text
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
```

from an earlier 24C call.

No raw sidecar verification object, 24A extension, raw 22A revision, arbitrary note, digest string, or filesystem path can substitute for the loaded predecessor application evidence.

## Base case — loaded 23C continuation

For the first general edge:

```text
loaded 23C continuation
        ↓
24B edge
        ↓
loaded 24C edge
```

24C re-establishes the retained local 23C relationships before accepting the predecessor.

It checks that:

- the continuation format and modes are supported;
- the retained 22C predecessor revision identity still matches the 23B verification evidence;
- public 23A can reconstruct the retained continuation from that exact predecessor and the verified v3 wording;
- the retained continuation still points to the exact retained 22C predecessor object;
- the retained continuation revision still uses the exact v2 note object;
- retained v3 wording still matches verified 23B wording.

This preserves the existing principle:

```text
loaded-record Python type
≠
coherent loaded application evidence
```

## Repeat case — already-loaded 24C edge

For another edge:

```text
loaded 24C edge A
        ↓
24B edge B
        ↓
loaded 24C edge B
```

24C checks the immediate local relationship retained by edge A:

- edge A's format and modes are supported;
- edge A's persisted predecessor format + digest still match the predecessor object retained by edge A;
- public 22A can reconstruct edge A's local revision from that retained predecessor endpoint and edge A's verified wording;
- edge A's revision still points to that exact local predecessor endpoint note;
- edge A's revised note still retains the exact working-set object;
- edge A's retained wording still matches edge A's verification evidence.

Only after that immediate loaded-edge relationship is coherent may edge A serve as the explicit predecessor for edge B.

## No recursive ancestry revalidation

24C does **not** recursively re-prove the entire ancestry of an already-loaded predecessor edge.

For example, given:

```text
loaded edge A
  predecessor = loaded edge B
```

24C may re-establish A's immediate relationship to B, but it does not recursively reopen or revalidate every ancestor carried beneath B.

Each earlier loaded record remains a distinct evidence layer produced by its own successful load operation.

Therefore:

```text
local predecessor coherence
≠
whole-history revalidation
```

This is deliberate.

A request to validate an entire history would be a different product action with stronger traversal and ancestry authority.

## Fresh verification applies only to the edge being opened

24C always begins with public:

```python
verify_chromium_research_working_set_note_revision_edge(edge_source)
```

This freshly re-establishes:

- canonical JSON structure;
- supported format;
- supported predecessor-reference shape;
- edge/revision/note modes;
- non-whitespace human text;
- edge-record SHA-256 self-integrity;
- canonical bytes.

It does not open the predecessor file.

## Content address is identity, not navigation

The persisted predecessor reference is:

```text
format + record_sha256
```

24C uses those values only to answer:

```text
"Does this edge name the exact predecessor object the caller supplied?"
```

It never interprets the digest as:

```text
"Go find this predecessor for me."
```

No digest search or directory scan occurs.

Thus:

```text
content address
=
comparison identity
```

but:

```text
content address
≠
navigation authority
```

## Exact predecessor match

For a loaded 23C predecessor, 24C compares the edge's persisted predecessor reference against:

```text
continuation format
+
continuation_record_sha256
```

For a loaded 24C predecessor, 24C compares against:

```text
edge format
+
edge_record_sha256
```

Digest comparison uses constant-time comparison.

A different but independently valid loaded predecessor is rejected.

Therefore:

```text
valid loaded predecessor
≠
correct predecessor for this edge
```

## Exact endpoint note

After predecessor identity matches, 24C derives exactly one endpoint note.

For a loaded 23C continuation:

```text
predecessor.continuation.revision.revised_note
```

For a loaded 24C edge:

```text
predecessor.revision.revised_note
```

Public 22A then reconstructs the new edge revision over that exact note.

Successful loading therefore retains:

```text
loaded.revision.prior_note
is
explicit_predecessor_endpoint_note
```

and the revised note retains the same exact working-set object.

## Exact no-op rejection is re-established at load time

24B file-only verification does not know the predecessor wording.

A caller can therefore change persisted edge wording back to the exact predecessor wording, recompute the edge-record digest, and still obtain a valid 24B file.

24C then reconstructs through public 22A.

Public 22A rejects:

```text
vN → exact same vN
```

So the self-consistent forged file cannot re-enter typed loaded application state through 24C.

Thus:

```text
24B file integrity
≠
actual exact-text revision relative to predecessor
```

and 24C earns that relationship again.

## Falsifiability proof 1 — recomputed wrong predecessor digest

Start with a valid 24B edge.

Replace its predecessor digest with another valid 64-hex digest and recompute the outer edge-record digest.

Public 24B verification succeeds.

Supply the real loaded predecessor to 24C.

24C rejects because the persisted predecessor identity does not match the explicit predecessor object.

This proves:

```text
24B file integrity
≠
predecessor attachment correctness
```

## Falsifiability proof 2 — recomputed no-op wording

Start with a valid edge whose wording differs from its predecessor endpoint.

Change the edge wording to exactly the real predecessor wording and recompute the edge-record digest.

Public 24B verification succeeds.

24C matches predecessor identity, then calls public 22A.

22A rejects the exact no-op.

Therefore:

```text
24B file integrity
≠
actual revision relative to predecessor
```

## Falsifiability proof 3 — different valid loaded predecessor

Create two independently valid loaded predecessors.

Supply an edge that references predecessor A together with loaded predecessor B.

B may be perfectly valid application evidence.

24C still rejects because B is not the predecessor named by the edge.

Thus:

```text
validity of predecessor B
≠
attachment of this edge to predecessor B
```

## Falsifiability proof 4 — forged loaded-edge local identity

Start with one valid loaded 24C edge.

Forge only its retained predecessor digest while preserving the outer loaded-edge Python type.

Use that forged loaded edge as the explicit predecessor for another edge.

24C rejects while re-establishing the loaded predecessor's immediate local relationship.

This proves:

```text
loaded-edge Python shape
≠
coherent local predecessor evidence
```

## Explicit edge-to-edge loading without traversal

The central 24C repeatability proof is:

1. create and load edge A;
2. create edge B whose predecessor reference names edge A's 24B content identity;
3. delete edge A's sidecar;
4. delete the earlier 20B, 21B, 22B, and 23B sidecars;
5. optionally delete individual member sidecars;
6. call 24C with the already-loaded edge A object and edge B's explicit path;
7. load edge B successfully.

This proves:

```text
current predecessor-file availability
≠
ability to extend already-loaded predecessor evidence
```

and:

```text
successful edge-to-edge loading
≠
recursive filesystem traversal
```

## What 24C does not read

When opening edge B against an already-loaded edge A, 24C does not need to open:

- edge A's sidecar;
- A's predecessor sidecar;
- 23B continuation sidecar;
- 22B revision sidecar;
- 21B note sidecar;
- 20B working-set sidecar;
- member sidecars;
- source captures;
- browser state.

Only edge B's explicit `edge_source` is freshly opened.

## Paths remain locations, not identities

The current edge sidecar may move before load.

If the caller supplies its new path and the bytes remain canonical and content-identical, 24C succeeds.

No predecessor path is stored or inferred.

Therefore:

```text
path location
≠
durable identity
```

## No automatic traversal

24C does not accept a directory or history root.

It accepts one explicit already-loaded predecessor object.

It does not:

- search for a matching predecessor digest;
- follow predecessor references recursively;
- enumerate sibling edges;
- discover successors;
- infer a root;
- infer a head;
- construct a chain automatically;
- construct a DAG automatically.

A researcher may call 24C repeatedly, one edge at a time, while explicitly carrying forward the loaded predecessor object.

That is caller-driven composition, not automatic history traversal.

## No linear-chain authority

24C does not require that one predecessor have exactly one successor.

Two independently persisted edges may reference the same predecessor identity.

24C does not call either one invalid merely because the other exists.

Thus:

```text
local predecessor edge
≠
unique global successor
```

No branch semantics are inferred from that possibility.

## No history head

Unlike `pyxis.revisions`, 24C introduces no concept of:

```text
current revision head
```

The caller chooses the predecessor object for each load.

Pyxis does not decide which loaded edge is current, latest, canonical, preferred, or authoritative.

Therefore:

```text
explicit caller-selected predecessor
≠
global current state
```

## No chronology authority

24C adds no:

- timestamp;
- trusted clock;
- sequence number;
- revision number;
- monotonic counter;
- current-head rule;
- global ordering.

A local predecessor relationship means only that one human revision was explicitly represented as changing wording relative to another exact note state.

It does not establish trusted wall-clock chronology.

## No semantic authority

24C does not infer that the newly loaded wording is:

- better;
- worse;
- more accurate;
- less accurate;
- more supported;
- less supported;
- contradictory;
- corroborating;
- convergent;
- divergent;
- more certain;
- less certain;
- closer to truth.

Exact textual inequality remains only exact textual inequality.

## Authority boundary

The research revision spine now distinguishes:

```text
24B file self-integrity
≠
explicit predecessor attachment
≠
exact-text revision re-establishment
≠
recursive ancestry validation
≠
history traversal
≠
global ordering
≠
semantic truth
```

24C earns only the second and third relationships for one explicitly supplied local predecessor.

## Successful 24C loading proves only

A successful result proves that:

1. the supplied edge sidecar is freshly 24B-integrity-valid;
2. the caller supplied one supported already-loaded predecessor record;
3. that predecessor's immediate loaded relationship is coherent enough for this local use;
4. the edge's persisted predecessor format matches the supplied predecessor format;
5. the edge's persisted predecessor content identity matches the supplied predecessor content identity;
6. public 22A can reconstruct the edge wording as an actual exact-text revision of the supplied predecessor's endpoint note;
7. the loaded record retains the exact caller-supplied predecessor object;
8. the reconstructed revision retains the exact predecessor endpoint note object;
9. the revised note retains the exact working-set object;
10. human wording is preserved verbatim.

This is:

```text
verified one-edge attachment to one explicit already-loaded predecessor
```

## Successful 24C loading does not prove

24C does **not** prove:

- predecessor-file availability;
- complete ancestry validity;
- recursive chain validity;
- durable graph acyclicity;
- one unique successor;
- one unique predecessor beyond the explicit local reference;
- a history root;
- a current history head;
- trusted chronology;
- revision numbering;
- authorship identity;
- source truth;
- claim support;
- semantic improvement;
- semantic difference;
- correctness;
- relevance;
- citation authority;
- browser freshness;
- machine agreement.

## Focused acceptance tests

24C is accepted only if tests prove:

1. base-case relinking against exact loaded 23C continuation;
2. moved current-edge path works because path is not identity;
3. different valid loaded continuation is rejected;
4. recomputed wrong predecessor digest passes 24B verification but fails 24C;
5. recomputed exact no-op wording passes 24B verification but fails 24C through 22A;
6. same-format edge-to-edge loading succeeds after predecessor and earlier sidecars disappear;
7. wrong explicit loaded-edge predecessor is rejected;
8. forged loaded-edge local predecessor identity is rejected;
9. current-edge tamper without matching digest fails fresh 24B verification first;
10. wrong input type is rejected and the explicit module is publicly importable.

## Decision

D157:

> A 24B content-addressed revision edge may re-enter typed application state only when the caller explicitly supplies one already-loaded predecessor whose durable content identity matches the edge reference, and when the edge's human wording can be freshly reconstructed through public 22A as an actual exact-text revision of that predecessor's endpoint note. The predecessor may itself be one already-loaded 24C edge, enabling caller-driven repeated edge composition without automatic predecessor discovery, recursive file loading, whole-history revalidation, a current-head rule, trusted chronology, or semantic authority.
