# Milestone 25A — Human-Owned Extension of a Loaded General Revision Edge

Decision: D158

## Product question

After 24C reopens one general durable revision edge as typed application evidence, what is the next actual researcher action?

The researcher may change the working-set rationale again.

25A answers the narrow question:

```text
"I have this exact verified edge loaded.
I want to revise its endpoint wording again."
```

The result is one new in-memory human revision explicitly attached to that exact loaded 24C edge.

25A does **not** persist the new revision.

It does not change the 24B file format or broaden the 24B creator.

That separation is deliberate.

## Why 25A exists

24B generalized durable representation:

```text
23B continuation
      ↓
24B edge
      ↓
24B edge
      ↓
...
```

24C generalized explicit loading:

```text
already-loaded predecessor
+
explicit 24B edge file
→
loaded 24C edge
```

But after loading an arbitrary edge, Pyxis still lacked a first-class application record for the next human action:

```text
loaded edge vN
+
new human wording
→
explicit human extension vN → vN+1
```

A caller could technically invoke public 22A directly on:

```text
loaded_edge.revision.revised_note
```

but that would produce only a generic note revision.

It would not retain that the revision explicitly extends **this exact loaded 24C edge**.

25A adds only that provenance relationship.

## Public API

The new explicit-module API is:

```python
create_chromium_research_working_set_note_revision_edge_extension(
    prior_edge,
    *,
    revised_note_text,
)
```

with:

```python
ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_extension
```

25A does not broaden the `pyxis.app` root export surface.

## Record

Successful creation returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord(
    extension_mode=(
        "caller_authored_extension_of_verified_research_working_set_note_revision_edge"
    ),
    prior_edge=<exact caller-supplied loaded 24C edge>,
    revision=<new public-22A revision>,
)
```

The record is frozen and slotted.

## Exact identity relationship

The new revision is created over exactly:

```text
prior_edge.revision.revised_note
```

Therefore successful 25A creation establishes:

```text
extension.prior_edge is prior_edge
```

and:

```text
extension.revision.prior_note
is
prior_edge.revision.revised_note
```

The revised note retains the exact same working-set object.

This is stronger than merely having the same endpoint text.

Thus:

```text
same endpoint wording
≠
explicit human extension of this loaded edge object
```

## Reusing 22A

25A does not create a second revision-text policy.

It delegates new human wording to public 22A:

```python
create_chromium_research_working_set_note_revision(...)
```

Therefore existing rules remain authoritative:

- `revised_note_text` must be a string;
- it must contain non-whitespace human text;
- exact textual equality with the prior note is rejected;
- exact whitespace differences are allowed;
- no semantic normalization occurs;
- no semantic-difference claim is made.

So:

```text
exact text difference
≠
semantic difference
```

## In-memory predecessor coherence

A correctly typed `ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord` is not sufficient by itself.

Before using its endpoint note, 25A reuses the local loaded-edge validation established by 24C.

That validation checks the loaded edge's immediate relationship to the predecessor object it retains.

The checks include:

- supported edge format;
- supported edge/revision/note modes;
- persisted predecessor format matches the retained predecessor's reported format;
- persisted predecessor record digest matches the retained predecessor's reported content identity;
- public 22A can reconstruct the loaded edge's current local revision from the retained predecessor endpoint and verified edge wording;
- the loaded edge's revision still points to the exact retained predecessor endpoint note;
- its revised note still retains the exact working-set object;
- its revised note mode and text still agree with the retained 24B verification evidence.

Therefore:

```text
loaded-edge Python type
≠
coherent immediate loaded-edge evidence
```

## Local validation only

25A deliberately inherits 24C's local-only validation rule.

Suppose the supplied loaded edge is:

```text
edge B
  predecessor = loaded edge A
```

25A re-establishes B's immediate local relationship to A.

It does **not** recursively revalidate A's relationship to its own predecessor.

That means:

```text
coherence of B → A
≠
whole-history validation beneath A
```

This is deliberate.

The requested user action is:

```text
"extend this loaded edge"
```

not:

```text
"audit every ancestor of this edge"
```

Whole-history validation would be a separate action with stronger traversal and ancestry authority.

## Falsifiability proof 1 — forged immediate predecessor identity

Start from one valid loaded 24C edge.

Forge only its retained:

```text
verification.predecessor_record_sha256
```

while keeping the Python record type intact.

25A rejects before creating the new revision because the loaded edge no longer matches its immediate retained predecessor.

This proves:

```text
loaded-edge shape
≠
immediate predecessor coherence
```

## Falsifiability proof 2 — forged endpoint text

Start from one valid loaded 24C edge.

Forge:

```text
prior_edge.revision.revised_note.note_text
```

without changing the retained 24B verification wording.

25A rejects before creating a successor.

Therefore:

```text
loaded endpoint object
≠
verified endpoint wording coherence
```

## Falsifiability proof 3 — deeper ancestry is outside scope

Create:

```text
loaded edge A
      ↓
loaded edge B
```

Then forge only A's relationship to the predecessor beneath A while leaving:

- A's own edge content identity unchanged;
- A's endpoint note unchanged;
- B's persisted reference to A unchanged;
- B's local revision over A unchanged.

Replace B's retained predecessor object with that forged-A wrapper.

B's immediate local relationship to A remains coherent.

25A therefore accepts B as the edge being extended.

This is not a weakness in 25A.

It is a proof of the intended boundary:

```text
extend one coherent loaded edge
≠
recursively audit its ancestry
```

## No file reads

25A operates only on already-loaded application evidence.

After a 24C edge has been loaded successfully, the caller may remove:

- the 24B edge sidecar;
- the 23B continuation sidecar;
- the 22B revision sidecar;
- the 21B note sidecar;
- the 20B working-set sidecar;
- individual 17C/18C/19C member sidecars.

25A still succeeds if the supplied loaded edge remains coherent in memory.

Thus:

```text
current durable-file availability
≠
ability to continue already-loaded application evidence
```

and:

```text
25A extension
≠
fresh 24C relinking
```

## Append-only application state

25A does not mutate the prior loaded edge.

For:

```text
v4 → v5
```

v4 remains unchanged.

The v5 note is a new object.

The new revision retains v4 as its exact prior note.

There is no mutable current-head pointer.

There is no revision counter.

There is no automatic replacement of old application state.

## Arbitrary depth

Because 24C can load an edge whose predecessor is another already-loaded 24C edge, 25A is not limited to the first general edge.

For example:

```text
loaded v4 edge
      ↓
loaded v5 edge
      ↓
25A extension
      ↓
v6
```

works through the same API.

The application action no longer needs a version-specific class for v5, v6, v7, and so on.

## Why persistence is not included

25A intentionally stops before writing a 24B edge whose predecessor is another 24B edge.

The next likely product pressure is:

```text
"I explicitly extended this loaded general edge.
Preserve that extension using the existing general 24B format."
```

That later persistence step can then use:

```text
prior_edge.verification.edge_format
+
prior_edge.verification.edge_record_sha256
```

as the durable predecessor identity.

But persistence must independently earn its own creation-time authority checks.

25A does not silently grant them.

Thus:

```text
in-memory explicit extension
≠
durable edge creation
```

## No stronger history semantics

25A does not establish:

- a global revision history;
- a current history head;
- chronology;
- trusted timestamps;
- revision numbers;
- uniqueness of successor;
- linearity;
- cycle absence;
- branch semantics;
- merge semantics;
- whole-history validity;
- semantic improvement;
- source truth;
- claim support;
- authorship identity;
- authentication.

## Authority boundary

The milestone preserves the research spine's separation:

```text
24C loaded edge evidence
≠
25A human decision to revise again
≠
future durable representation of that new revision
≠
whole-history authority
≠
semantic truth
```

Successful 25A creation establishes only:

> One exact human-authored revision explicitly extends one exact coherent already-loaded 24C revision edge in application memory.

Nothing stronger is implied.

## Focused test contract

The 25A test suite proves:

1. exact loaded-edge object retention and exact endpoint-note identity;
2. append-only `v4 → v5` behavior without mutation;
3. successful creation after all related durable files disappear;
4. wrong-type and invalid-text rejection;
5. exact endpoint no-op rejection through public 22A;
6. exact whitespace change acceptance without semantic claims;
7. rejection of forged immediate predecessor identity;
8. rejection of forged loaded endpoint wording;
9. explicit proof that deeper ancestry is not recursively revalidated;
10. explicit module importability.

## Scope exclusions

25A makes no changes to:

- 24B persistence format;
- 24B persistence creator;
- 24C loader;
- predecessor discovery;
- digest search;
- recursive file loading;
- history traversal;
- whole-history validation;
- cycle detection;
- current-head semantics;
- chronology;
- revision numbering;
- branching or merging;
- semantic comparison;
- claims;
- browser acquisition;
- LLM behavior;
- compiler/RIR/runtime/export/measurement systems;
- researcher UI;
- root exports;
- README;
- `docs/CURRENT_STATE.md`.

## Decision

D158:

> After one general durable revision edge has been explicitly reopened through 24C, Pyxis may create one new human-owned in-memory revision explicitly extending that exact loaded edge. The loaded edge's immediate local relationship must be re-established before use, but deeper ancestry is not recursively revalidated. New wording remains governed by public 22A exact-text rules. The extension performs no file reads, persistence, traversal, chronology inference, or semantic promotion.
