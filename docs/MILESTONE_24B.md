# Milestone 24B — General Durable Revision Edge

Decision: D156

## Product question

After a researcher has explicitly represented:

```text
v1 → v2 → v3 → v4
```

should Pyxis keep inventing a new durable artifact format for every later human change of wording?

24B answers **no**.

The repeated researcher action is now established strongly enough to justify one general content-addressed revision-edge format.

24B persists the current 24A `v3 → v4` extension against its exact durable 23B predecessor, while defining a durable edge record whose predecessor reference may name either:

1. the existing 23B continuation format; or
2. another 24B revision-edge record.

That makes repeated revision edges **representable** without yet making them automatically discoverable, traversable, ordered, or authoritative as a history.

## Why this milestone is different from another persistence step

22A–22C established one human rationale revision:

```text
v1 → v2
```

23A–23C established one explicit continuation:

```text
v1 → v2 → v3
```

24A established another ordinary human action:

```text
v1 → v2 → v3 → v4
```

At that point, adding a special-purpose `v3 → v4` file format and then repeating the same pattern for v5, v6, and v7 would no longer be the narrowest product design.

The repeated action itself is now concrete product pressure.

24B therefore generalizes only the **durable edge representation**.

It does not generalize loading, traversal, chronology, branching policy, merge policy, or semantic interpretation.

## Why `pyxis.revisions` is not reused directly

Pyxis already has Repository Zero revision machinery under:

```text
pyxis.revisions
```

That subsystem deliberately models canonical architecture mutation as a single append-only chain with concepts such as:

```text
parent_revision_id
current chain head
append only if parent == head
```

Those are valid authority rules for Repository Zero architecture changes.

They have **not** been earned for researcher-authored rationale revisions.

The research spine currently establishes only explicit local predecessor relationships.

It does not establish:

- one global research-history head;
- one total order;
- uniqueness of successor;
- absence of branching;
- trusted chronology;
- merge semantics;
- current truth.

Therefore:

```text
existing revision-chain implementation
≠
correct authority model for research rationale history
```

24B borrows the useful content-addressed predecessor idea without importing the stronger linear-chain rules.

## Public module API

The new explicit-module API is:

```python
persist_chromium_research_working_set_note_revision_edge(
    extension,
    working_set_source,
    prior_note_source,
    prior_revision_source,
    prior_continuation_source,
    destination,
)
```

and:

```python
verify_chromium_research_working_set_note_revision_edge(source)
```

with:

```python
ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence
ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence
ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_persistence
```

24B does not broaden the `pyxis.app` root export surface.

## Durable format

The new durable format is:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

The canonical edge record is:

```json
{
  "predecessor_reference": {
    "format": "<supported predecessor format>",
    "record_sha256": "<64-hex predecessor record identity>"
  },
  "edge": {
    "mode": "caller_authored_research_working_set_note_revision_edge",
    "revision": {
      "mode": "caller_authored_revision_of_research_working_set_note",
      "revised_note": {
        "mode": "caller_authored_note_on_research_working_set",
        "text": "<verbatim human wording>"
      }
    }
  }
}
```

The outer document is:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision_edge.v1",
  "edge_record": { "...": "..." },
  "edge_record_sha256": "<sha256 of canonical edge_record>"
}
```

JSON remains deterministic, canonical, UTF-8, newline terminated, and no-overwrite.

## One generic predecessor reference

The predecessor reference is deliberately generic:

```text
format + record_sha256
```

The meaning of `record_sha256` is always:

```text
SHA-256 identity of the predecessor format's canonical record payload
```

For a 23B predecessor, that is the predecessor's:

```text
continuation_record_sha256
```

For a future 24B predecessor, that is the predecessor's:

```text
edge_record_sha256
```

No filesystem path is part of durable identity.

## Supported predecessor formats

The 24B file schema accepts exactly two predecessor formats:

```text
pyxis.chromium.research_working_set_note_revision_continuation.v1
```

and:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

The first anchors the general edge representation to the already-earned durable v3 state.

The second makes another edge representable without introducing another schema.

Thus:

```text
same-format predecessor reference
=
recursive representability
```

but:

```text
recursive representability
≠
recursive loading
≠
chain traversal
≠
history authority
```

## What the 24B creator emits today

Although the file schema can represent a 24B predecessor, the 24B public persistence function currently accepts only one live 24A extension.

A 24A extension explicitly points to one already-loaded 23C continuation.

Therefore the public creator in this milestone emits:

```text
23B continuation record
        ↓
24B general revision edge
```

It does **not** yet create:

```text
24B edge
   ↓
24B edge
```

That later creation path must first earn a loaded/relinked predecessor representation in application state.

The schema is capable of expressing the relationship; the application has not yet earned authority to create or traverse it automatically.

## Creation-time authority

24B persistence is intentionally stronger than 24B file-only verification.

Before writing, Pyxis re-establishes the supplied live 24A extension through public:

```python
create_chromium_research_working_set_note_revision_continuation_extension(...)
```

This reuses the 24A checks that the loaded 23C object remains coherent.

It then freshly relinks the explicit durable predecessor through public 23C using:

```text
exact already-loaded member sequence
+
explicit 20B working-set sidecar
+
explicit 21B predecessor-note sidecar
+
explicit 22B predecessor-revision sidecar
+
explicit 23B predecessor-continuation sidecar
```

Only after that fresh relinking does 24B compare the durable predecessor content identity against the predecessor identity retained by the exact 24A extension.

The comparison uses constant-time digest comparison.

Therefore:

```text
valid durable continuation
≠
correct durable predecessor for this edge
```

## Exact member identity remains caller-owned

The fresh 23C load receives the exact ordered working-set member sequence already retained by the 24A extension's predecessor.

After the fresh load, 24B checks that those exact member objects remain retained position by position.

24B performs no:

- sorting;
- deduplication;
- member discovery;
- substitution;
- semantic clustering.

Thus:

```text
revision-edge persistence
≠
new working-set membership decision
```

## Individual member sidecars are still not reread

The fresh 23C predecessor relinking ultimately relies on already-loaded 17D/18D/19D member records through the existing 20C/21C/22C boundaries.

The individual member sidecars may therefore disappear after their earlier successful relinking while 24B persistence still succeeds, provided the explicit durable 20B, 21B, 22B, and 23B artifacts remain available.

This proves only:

```text
current individual member-sidecar availability
≠
ability to establish this durable edge
```

## Paths remain locations, not identities

The 20B, 21B, 22B, and 23B files may be moved before persistence.

If the caller supplies the new paths and the durable identities re-establish coherently, 24B succeeds.

The 24B file stores none of those paths.

Therefore:

```text
path location
≠
durable identity
```

## Minimal serialization

24B stores only:

```text
predecessor format
+
predecessor record SHA-256
+
generic edge mode
+
revision mode
+
revised-note mode
+
verbatim new human wording
```

It does not copy:

- v1 wording;
- v2 wording;
- v3 wording;
- working-set identity directly;
- working-set members;
- member digests;
- paragraph ordinals;
- text coordinates;
- selected source text;
- URLs;
- browser evidence;
- filesystem paths;
- timestamps;
- author identity;
- semantic analysis.

The predecessor reference points to existing durable state rather than duplicating it.

## File-only verification remains deliberately weaker

`verify_chromium_research_working_set_note_revision_edge(...)` reads only the 24B file.

It validates:

- UTF-8;
- exact schema;
- supported 24B format;
- one of the two supported predecessor formats;
- SHA-256 shapes;
- edge/revision/note modes;
- non-whitespace human text;
- edge-record self-integrity;
- canonical bytes.

It does not open:

- a 23B continuation;
- another 24B edge;
- the 22B revision;
- the 21B note;
- the 20B working set;
- member sidecars;
- source captures;
- browser state.

Therefore:

```text
24B file integrity
≠
predecessor existence
≠
predecessor correctness
≠
actual revision relative to predecessor
```

## Falsifiability proof 1 — wrong predecessor digest

Start with a valid edge created against the real 23B predecessor.

Replace:

```text
predecessor_reference.record_sha256
```

with another valid-looking SHA-256.

Recompute the outer `edge_record_sha256` and canonical JSON.

24B verification succeeds by design.

Therefore:

```text
24B self-integrity
≠
predecessor identity correctness
```

A later relinking boundary must earn that relationship.

## Falsifiability proof 2 — revised wording changed back to predecessor wording

Start with a valid edge whose v4 wording differs from the real v3 wording.

Change persisted v4 text back to the exact real v3 text.

Recompute the outer edge-record digest.

24B verification succeeds by design because the predecessor is not opened.

Therefore:

```text
24B self-integrity
≠
proof of an actual cross-file revision
```

A later relinker must re-establish the exact no-op boundary through public application constructors.

## Falsifiability proof 3 — same-format predecessor reference

Start with a valid 24B file.

Replace its predecessor reference with:

```json
{
  "format": "pyxis.chromium.research_working_set_note_revision_edge.v1",
  "record_sha256": "<valid-looking 64-hex digest>"
}
```

Recompute the outer digest.

24B file-only verification succeeds intentionally.

This proves only that the recursive edge shape is representable.

It does **not** prove:

- the referenced edge exists;
- the referenced edge is valid;
- the referenced edge is earlier;
- the referenced edge is an ancestor;
- the reference is acyclic;
- the reference belongs to the same working set;
- the new wording differs from that predecessor;
- a chain can be traversed.

Thus:

```text
same-format reference validity
≠
recursive history validity
```

## No global head

24B deliberately does not introduce a current head.

Two different 24B files may, as a matter of representation, point at the same predecessor identity.

24B does not decide whether that means:

- two alternatives;
- a branch;
- an error;
- two drafts;
- concurrent human thought;
- anything else.

That relationship is not interpreted here.

Therefore:

```text
explicit predecessor edge
≠
unique successor
```

and:

```text
content-addressed edges
≠
linear history
```

## No traversal

24B does not:

- scan directories;
- search by digest;
- follow predecessor references;
- recursively open files;
- find descendants;
- compute ancestry;
- detect cycles;
- construct a DAG;
- find a head;
- sort revisions.

The file schema can represent another edge as predecessor without any of those behaviors.

## No chronology authority

The predecessor relationship is explicit content attachment, not trusted time.

24B introduces no:

- timestamp;
- trusted clock;
- revision number;
- sequence number;
- monotonic counter;
- elapsed duration;
- global order.

Therefore:

```text
predecessor relation
≠
trusted chronology
```

## No semantic authority

24B does not infer whether the new wording is:

- better;
- worse;
- more accurate;
- less accurate;
- more supported;
- less supported;
- contradictory;
- corroborated;
- more certain;
- less certain;
- closer to truth.

It does not explain why the human changed the note.

It persists one exact human wording attached to one content-addressed predecessor reference.

## Integrity remains distinct from authority

The central distinction is:

```text
creation-time fresh predecessor relinking
+
exact live 24A extension coherence
→
24B creation-time durable edge attachment
```

while later file-only verification proves only:

```text
canonical 24B bytes
+
self-integrity
+
structurally supported predecessor reference
```

Thus:

```text
integrity
≠
authority
```

continues to hold.

## Successful 24B persistence proves only

A successful public persistence call proves that:

1. the caller supplied one coherent 24A extension;
2. the 24A predecessor is one coherent already-loaded 23C continuation;
3. the explicit supplied 20B/21B/22B/23B artifacts freshly relink through existing public boundaries;
4. the freshly loaded 23B predecessor format matches the retained predecessor format;
5. the freshly loaded 23B predecessor record SHA-256 matches the retained predecessor record SHA-256;
6. the exact supplied member objects remain retained in order;
7. the new human wording remains an actual exact-text revision through the 24A/22A boundary;
8. the persisted edge stores only the predecessor content identity plus verbatim new wording and supported modes;
9. the destination was created without overwrite.

This is:

```text
one content-addressed durable human rationale revision edge
```

## Successful 24B persistence does not prove

It does not prove:

- semantic improvement;
- factual truth;
- claim support;
- source authenticity;
- authorship identity;
- trusted chronology;
- one global history;
- one current head;
- unique successor;
- branch semantics;
- merge semantics;
- recursive ancestry;
- cycle freedom;
- automatic traversal;
- automatic predecessor discovery.

## Verification proves only

Successful file-only verification proves:

1. the bytes are valid UTF-8;
2. the document has the exact 24B shape;
3. the predecessor format is structurally one of the supported formats;
4. the predecessor digest has SHA-256 shape;
5. the modes are supported;
6. the human text is non-whitespace;
7. the recorded edge digest matches the canonical edge payload;
8. the complete bytes are canonical Pyxis JSON.

Nothing cross-file follows automatically.

## Focused acceptance surface

24B is accepted only if focused tests demonstrate:

1. minimal predecessor-identity + v4 serialization;
2. path independence;
3. rejection of a different but independently valid 23B predecessor before write;
4. no hidden reread of individual member sidecars;
5. re-establishment of the live 24A contract before write;
6. rejection of ordinary tamper without digest recomputation;
7. intentionally successful file-only verification after recomputing a wrong predecessor digest;
8. intentionally successful file-only verification after changing v4 back to real v3 and recomputing the digest;
9. intentionally successful file-only verification of a same-24B-format predecessor reference without traversal;
10. deterministic canonical bytes and no-overwrite behavior;
11. explicit module importability and wrong-type rejection.

## Scope boundary

24B adds only:

```text
24A explicit extension
→
one general durable revision-edge representation
```

It does not add:

- a 24B edge loader;
- edge-to-edge creation in application state;
- recursive relinking;
- traversal;
- cycle detection;
- a history head;
- branch or merge semantics;
- revision numbers;
- timestamps;
- semantic diff;
- claims;
- LLM analysis;
- browser acquisition;
- compiler/RIR/runtime/export changes;
- researcher UI.

Those remain separate product decisions.

## Authority boundary added by D156

The browser/research spine now includes:

```text
verified durable continuation
≠
human extension of that continuation
≠
general durable revision-edge representation
≠
verified recursive ancestry
≠
chronology
≠
semantic truth
```

The new durable design principle is:

```text
repeatable representation
without automatic history authority
```
