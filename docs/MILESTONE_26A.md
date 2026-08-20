# Milestone 26A — Explicit Ordered Revision-Edge Sequence Relinking

Decision: D160

## Product question

After 25B made the generalized revision-edge loop genuinely repeatable, what is the next actual researcher friction?

A researcher who has several durable revision edges should not have to manually write the same 24C call repeatedly just to reopen an already-known sequence.

26A answers the narrow question:

```text
"I already have the correct starting predecessor loaded.
These are the exact edge files I want to reopen, in this exact order."
```

Pyxis can now relink that explicit ordered sequence in one application call.

26A does **not** discover files or infer history.

## Why this follows 25B

25B completed the reusable loop:

```text
24C loaded edge
      ↓
25A human extension
      ↓
25B durable successor edge
      ↓
24C loaded successor edge
      ↓
repeat
```

That loop removed version-specific schemas and classes.

But reopening several already-known edges still required caller ceremony:

```python
edge_1 = load_chromium_research_working_set_note_revision_edge(start, path_1)
edge_2 = load_chromium_research_working_set_note_revision_edge(edge_1, path_2)
edge_3 = load_chromium_research_working_set_note_revision_edge(edge_2, path_3)
```

The repeated code adds no new epistemic boundary.

26A packages exactly that explicit operation without changing 24C's authority.

## Public API

The new explicit-module API is:

```python
load_chromium_research_working_set_note_revision_edge_sequence(
    starting_predecessor,
    edge_sources,
)
```

with:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
```

and positional failure type:

```python
ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load
```

26A does not broaden the `pyxis.app` root export surface.

## Inputs are caller-owned

26A requires:

1. one already-loaded starting predecessor, either:
   - a loaded 23C continuation; or
   - a loaded 24C revision edge;
2. one non-empty ordered iterable of explicit edge-file paths.

The caller chooses both.

Pyxis does not search for either.

Thus:

```text
caller-supplied starting state
+
caller-supplied file order
≠
machine-discovered history
```

## Sequence operation

26A snapshots the supplied iterable into an ordered tuple.

It then performs:

```text
current = starting_predecessor

for source in edge_sources:
    current = public_24C(current, source)
```

Each successful edge is retained as a freshly loaded public-24C record.

The result retains:

```text
sequence.starting_predecessor
is
exact caller-supplied starting object
```

and for the first edge:

```text
sequence.edges[0].predecessor
is
sequence.starting_predecessor
```

while every later edge satisfies:

```text
sequence.edges[n].predecessor
is
sequence.edges[n - 1]
```

Exact object identity matters.

## Reuse of 24C

26A does not duplicate revision-edge validation.

Every member delegates to:

```python
load_chromium_research_working_set_note_revision_edge(...)
```

Therefore each edge still receives the existing 24C behavior:

- fresh 24B file verification;
- explicit predecessor format match;
- explicit predecessor content-identity match;
- reconstruction through public 22A;
- exact textual non-no-op re-establishment;
- exact predecessor-note identity;
- exact working-set retention.

26A adds orchestration only.

Thus:

```text
26A ordered orchestration
≠
new edge authority model
```

## Positional failure

If member `n` cannot be relinked, 26A stops immediately and raises a sequence relink error identifying zero-based member `n`.

It does not skip the member.

It does not try a later file.

It does not search for a replacement.

It does not reorder the input.

This makes caller assertions falsifiable.

## Falsifiability proof 1 — skipped predecessor

Suppose the durable relationship is:

```text
loaded v4
   ↓
v5 edge
   ↓
v6 edge
```

The caller supplies:

```text
starting predecessor = loaded v4
edge sources = [v6]
```

The v6 edge references v5, not v4.

26A fails at member `0` through public 24C.

It does not infer that v5 must exist somewhere.

It does not search for v5.

Therefore:

```text
known descendant file
≠
authority to invent missing ancestry
```

## Falsifiability proof 2 — sibling edges are not silently linearized

Suppose two valid durable edges both reference the same loaded predecessor:

```text
        sibling A
       ↗
loaded v4
       ↘
        sibling B
```

The caller supplies:

```text
[sibling A, sibling B]
```

The first edge loads successfully.

The second edge is then tested against the exact first loaded edge, because the caller asserted an ordered sequence.

It still references v4, so 26A fails at member `1`.

Pyxis does not reinterpret the two files as a branch.

It does not sort or regroup them.

Thus:

```text
explicit ordered sequence
≠
unordered set
≠
branch discovery
```

## Falsifiability proof 3 — first failure stops the operation

If the first supplied edge is tampered and a later supplied path is missing, 26A reports failure at member `0` with the underlying 24B integrity failure as its cause.

The missing later file is never needed to explain the failed operation.

Thus:

```text
sequence relinking
≠
best-effort skipping
```

## Starting in the middle is allowed

The starting predecessor may itself be an already-loaded 24C edge.

For example:

```text
loaded v5
+
[v6 edge, v7 edge]
→
loaded explicit v5 → v6 → v7 segment
```

26A therefore does not require every sequence to begin at the original 23C continuation.

This is important for incremental researcher re-entry.

## Older durable files are not required

Because the starting predecessor is already-loaded application evidence, its own durable file need not still exist.

Older sidecars beneath it also need not still exist.

For example, after v4 is already loaded, the caller may remove:

- the v4 edge file;
- the 23B continuation file;
- the 22B revision file;
- the 21B note file;
- the 20B working-set file;
- individual 17C/18C/19C member sidecars.

26A can still relink explicit v5 and v6 edge files from the already-loaded v4 object.

Thus:

```text
availability of pre-sequence durable ancestry
≠
ability to relink an explicit later segment
```

## Local validation below the start remains bounded

26A does not strengthen 24C into recursive history validation.

Before the first new edge can load, 24C validates the starting predecessor only to the extent already defined by 24C.

If the starting predecessor is a loaded edge, its immediate local relationship is re-established.

An older relationship beneath that local predecessor is not recursively audited.

Therefore:

```text
validated explicit sequence segment
≠
validated ancestry below the supplied start
```

This is deliberate.

The researcher asked:

```text
"reopen this asserted segment from this starting object"
```

not:

```text
"audit every durable ancestor reachable beneath it"
```

## Paths remain locations, not identities

Each supplied edge file may be moved before 26A is called.

The caller supplies the new paths explicitly.

Public 24C verifies the contents and predecessor identity at those locations.

Successful loading retains each verification path as location evidence, but path does not become edge identity.

Thus:

```text
filesystem path
≠
revision-edge content identity
```

## No empty sequence

26A requires at least one edge source.

An empty call would add no new evidence and, importantly, would not exercise public 24C against the starting predecessor.

Rejecting an empty sequence keeps successful 26A results tied to at least one freshly relinked durable edge.

## No single-path ambiguity

`edge_sources` is explicitly a collection input.

Passing one `Path` object directly is rejected rather than risking accidental iteration semantics.

A one-edge sequence remains valid when expressed explicitly as:

```python
[path]
```

or another ordered iterable containing one path.

## What successful 26A proves

Successful 26A establishes only:

> Starting from one exact caller-supplied already-loaded predecessor, every explicitly supplied durable edge file was freshly relinked through public 24C in exactly the supplied order, with each newly loaded edge becoming the exact predecessor object for the next member.

That is enough to represent one explicit re-opened revision segment.

## What successful 26A does not prove

26A does not establish:

- that the supplied sequence is complete;
- that it begins at the earliest revision;
- that it ends at the latest revision;
- a current head;
- chronology;
- trusted time;
- revision numbering;
- global linearity;
- uniqueness of successors;
- absence of siblings;
- absence of branches;
- absence of cycles elsewhere;
- canonical history;
- directory completeness;
- predecessor discovery;
- digest search;
- semantic improvement;
- semantic difference beyond public 22A exact-text inequality;
- source truth;
- claim support;
- authorship identity;
- authentication.

## No automatic traversal

Although 26A processes multiple files, it is not an automatic history walker.

Automatic traversal would begin from one record and use persisted references to locate predecessor or successor files.

26A does nothing like that.

All file locations are supplied by the caller in advance.

Therefore:

```text
iteration over caller-supplied paths
≠
automatic graph traversal
```

## No persistence

26A creates one immutable application record only.

It does not persist a sequence manifest.

It does not create a new durable history object.

It does not alter any edge file.

A future durable sequence/manifest capability, if product pressure earns it, would require its own authority boundary.

Thus:

```text
loaded explicit sequence
≠
durable sequence identity
```

## Record shape

Successful loading returns:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord(
    sequence_mode=(
        "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
    ),
    starting_predecessor=<exact supplied loaded object>,
    edges=(<fresh edge 0>, <fresh edge 1>, ...),
)
```

The record is frozen and slotted.

The loaded edge tuple is immutable.

## Authority boundary

26A preserves:

```text
caller-declared file order
≠
verified local adjacency
≠
complete history
≠
current head
≠
chronology
≠
semantic truth
```

and:

```text
explicit multi-edge relinking
≠
file discovery
≠
digest navigation
≠
automatic traversal
```

## Focused test contract

The 26A focused tests prove:

1. two existing-format durable successor edges relink in explicit order with exact predecessor-object identity;
2. a sequence may resume from an already-loaded 24C edge;
3. moved file paths work because paths remain locations rather than identities;
4. a skipped predecessor is rejected at exact member `0`;
5. two sibling edges are not reordered or silently treated as a chain and fail at member `1`;
6. an invalid first edge stops the operation before a later missing member matters;
7. the already-loaded starting edge file and older sidecars may disappear while later explicit sequence files still relink;
8. ancestry below the supplied starting object's local boundary is not recursively revalidated;
9. invalid starting type, empty sequence, and ambiguous single-Path collection input are rejected;
10. the explicit module surface is publicly importable.

## Scope exclusions

26A makes no changes to:

- 24B persistence or verification;
- 24C single-edge relinking;
- 25A human extension;
- 25B persistence;
- durable edge schemas;
- root exports;
- README;
- `docs/CURRENT_STATE.md`;
- Chromium acquisition;
- browser navigation or interaction;
- source capture;
- source authenticity;
- claims;
- citations;
- LLM behavior;
- compiler/RIR/runtime/export behavior;
- measurement behavior;
- researcher UI;
- filesystem scanning;
- digest search;
- predecessor or successor discovery;
- automatic history traversal;
- current-head semantics;
- branch or merge semantics;
- chronology or timestamps.

## Decision

D160 adds one narrow researcher convenience only:

> Pyxis may freshly relink a non-empty caller-explicit ordered sequence of existing durable revision edges from one exact already-loaded starting predecessor by repeatedly composing the existing public 24C boundary.

No stronger history authority is introduced.
