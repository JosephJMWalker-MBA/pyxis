# Milestone 26C — Verified Explicit Revision-Edge Sequence Declaration Relinking

Decision: D162

## Product question

After 26B makes one human-declared ordered revision-edge segment durable, what is the next actual restart action?

The researcher now has two separate things:

1. a durable 26B declaration that names one starting predecessor and one ordered list of edge content identities; and
2. the actual application/file evidence they explicitly choose to reopen now.

26C answers the narrow question:

```text
"I have this declaration file.
I have this explicit starting record already loaded.
I have these explicit edge files in this exact order.
Do they re-establish the segment that the declaration names?"
```

Pyxis can now answer that question without allowing the declaration to locate or discover any record.

## Why this follows 26B

26B deliberately left file-only verification weaker than attachment authority.

A 26B declaration can be internally self-consistent while containing:

- the wrong starting-predecessor digest;
- a different ordered list of otherwise well-shaped edge identities;
- identities whose files no longer exist;
- identities that do not form the adjacency sequence the researcher wants to reopen.

That weakness is intentional.

26C adds the separate re-establishment boundary rather than strengthening 26B verification into hidden traversal.

The authority chain is:

```text
fresh 26B declaration-file verification
+
fresh 26A relinking of caller-explicit starting state and edge paths
+
position-by-position content-identity reconciliation
```

This is not history discovery.

## Public API

The new explicit-module API is:

```python
load_chromium_research_working_set_note_revision_edge_sequence_declaration(
    starting_predecessor,
    edge_sources,
    declaration_source,
)
```

with immutable result:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
```

and explicit attachment failure:

```python
ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load
```

26C does not broaden the `pyxis.app` root export surface.

## Caller ownership remains explicit

The caller supplies all three inputs independently:

- one already-loaded 23C continuation or 24C edge as the starting predecessor;
- one non-empty ordered iterable of exact edge paths;
- one exact 26B declaration path.

The declaration does not provide paths.

Pyxis does not search for paths by digest.

Pyxis does not scan a directory.

Pyxis does not infer a missing predecessor.

Pyxis does not choose a latest edge.

Thus:

```text
durable content identity
!=
record location
```

and:

```text
declaration
!=
discovery instruction
```

## Step 1 — fresh 26B verification

26C first calls:

```python
verify_chromium_research_working_set_note_revision_edge_sequence(
    declaration_source
)
```

This occurs before explicit edge relinking.

Therefore raw declaration corruption fails at the declaration-file boundary before Pyxis needs any edge path to explain the failure.

This ordering matters.

For example:

```text
corrupt declaration
+
missing edge files
→
declaration integrity failure first
```

Pyxis does not mask a broken declaration with a later filesystem error.

## Step 2 — fresh 26A explicit sequence relinking

After the declaration verifies as a file, 26C calls public 26A:

```python
load_chromium_research_working_set_note_revision_edge_sequence(
    starting_predecessor,
    edge_sources,
)
```

The caller still owns the exact order.

Public 26A still owns:

- non-empty ordered input;
- exact starting application object;
- one fresh public-24C load per edge;
- exact predecessor-object chaining;
- stop-on-first-invalid behavior;
- no reordering;
- no skipping;
- no predecessor discovery;
- no branch interpretation;
- bounded ancestry below the start.

26C does not duplicate those rules.

## Step 3 — reconcile the declaration to the explicit sequence

Once 26A succeeds, 26C compares the two evidence surfaces.

First, it derives the freshly relinked starting content identity using the same retained-content-identity logic 26B used when persisting the declaration.

It requires exact:

```text
record format
+
record SHA-256
```

agreement with the declaration's starting reference.

Then it requires the declared edge count to equal the fresh 26A edge count.

Finally, for each zero-based position `n`, it derives the fresh edge content identity and requires exact format + digest agreement with declaration member `n`.

No sorting occurs.

No set comparison occurs.

No unordered membership test occurs.

Thus:

```text
same members in another order
!=
same declared sequence
```

## Exact identity algorithm is reused

26C does not invent a new digest interpretation.

It reuses the same 26B retained-reference functions that were used to derive content identities at persistence time.

For a loaded 23C continuation, that means the canonical retained continuation record identity.

For a loaded 24C edge, that means the canonical retained edge record identity.

For every freshly loaded sequence edge, that means the canonical retained edge record identity.

This keeps write-time and load-time identity claims symmetrical.

## Result object

A successful result retains:

```python
loaded.verification
```

as fresh 26B declaration-file verification evidence, and:

```python
loaded.sequence
```

as the fresh 26A sequence record reconstructed from caller-explicit application/file evidence.

The result does not create a second sequence model.

It composes the two existing evidence layers.

## Falsifiability proof 1 — recomputed wrong starting identity

Take a valid 26B declaration.

Change only:

```text
starting_predecessor_reference.record_sha256
```

and recompute the declaration record digest and canonical document bytes.

Then:

```text
26B file-only verification
→ succeeds intentionally
```

because the file is internally self-consistent.

But if the caller supplies the real explicit starting predecessor and real edge paths:

```text
26C
→ rejects starting-predecessor identity mismatch
```

Therefore:

```text
26B file integrity
!=
starting attachment coherence
```

## Falsifiability proof 2 — recomputed different declared order

Take a valid two-edge 26B declaration.

Reverse its two edge references and recompute the declaration digest.

Then:

```text
26B file-only verification
→ succeeds intentionally
```

But if the caller explicitly relinks the real edge sequence in its actual order:

```text
26C
→ rejects member 0 identity mismatch
```

Pyxis does not reorder either side to make them agree.

Thus:

```text
same content identities
+
different human-declared order
!=
same declaration attachment
```

## Falsifiability proof 3 — declaration does not locate omitted members

Suppose the durable declaration names:

```text
v5, v6
```

The caller supplies only:

```text
[v5 path]
```

Public 26A successfully relinks that one explicit edge.

26C then rejects the member-count mismatch.

It does not use the declaration's v6 digest to search the filesystem for v6.

Therefore:

```text
declared missing member identity
!=
authority to discover its location
```

## Falsifiability proof 4 — explicit path order remains authoritative

Suppose the actual chain is:

```text
loaded v4 → v5 → v6
```

The caller supplies:

```text
[v6 path, v5 path]
```

26A fails immediately because v6 does not reference loaded v4.

26C reports that fresh explicit sequence relinking failed.

It does not inspect the declaration and silently reorder the supplied paths into `[v5, v6]`.

Thus:

```text
declaration order
!=
authority to rewrite caller input
```

## Falsifiability proof 5 — valid declaration plus corrupt explicit edge

A valid declaration alone is not enough.

If one explicitly supplied edge file is corrupted after declaration creation, fresh public 24C fails through 26A and 26C rejects the relink.

Therefore:

```text
valid durable declaration
!=
fresh referenced-edge integrity
```

## Fresh declaration verification precedes edge access

26C's operation ordering is intentional:

```text
verify declaration
→ relink explicit sequence
→ compare identities
```

It is not:

```text
open all edges
→ maybe inspect declaration later
```

This means declaration corruption is reported as declaration corruption even if edge paths are simultaneously unavailable.

That separation keeps failure evidence meaningful.

## Moved paths remain valid

The declaration path may move.

Any supplied edge path may move.

The caller supplies the new locations explicitly.

26C verifies and relinks those contents at the new locations.

Successful reconciliation depends on content identity, not the old path.

Thus:

```text
path relocation
!=
identity mutation
```

## Loaded continuation start remains supported

26C preserves 26A and 26B support for beginning a declared segment at an already-loaded 23C continuation.

For example:

```text
loaded 23C continuation
→ v4 edge
→ v5 edge
→ v6 edge
```

may be declared durably by 26B and freshly re-established by 26C when the caller explicitly supplies that same continuation object plus the three edge paths.

No special alternate loader is needed.

## What successful 26C proves

Successful 26C establishes only:

> One freshly verified 26B declaration names the same starting content identity and the same ordered edge content identities as one freshly relinked 26A sequence built from the caller's explicit already-loaded starting predecessor and explicit ordered edge paths.

That is a meaningful restart/re-entry guarantee.

## What successful 26C does not prove

26C does not establish:

- that the declared segment is complete;
- that it begins at the earliest revision;
- that it ends at the latest revision;
- a current head;
- chronology;
- trusted timestamps;
- revision numbers;
- unique successor relationships outside the supplied segment;
- absence of siblings or branches;
- absence of cycles elsewhere;
- canonical history;
- directory completeness;
- digest-to-path discovery;
- semantic improvement;
- semantic difference beyond existing exact-text rules;
- source truth;
- claim support;
- source authenticity;
- authorship identity;
- authentication.

## Authority boundary

26C preserves the following distinction:

```text
fresh declaration file integrity
+
fresh explicit local adjacency
+
exact declared identity/order match
!=
complete or canonical revision history
```

And more compactly:

**durable declaration ≠ discovery authority ≠ explicit relinking ≠ canonical history**.

## Scope exclusions

26C does not add:

- a new durable format;
- directory scans;
- digest search;
- automatic predecessor or successor discovery;
- graph traversal;
- a current-head pointer;
- revision numbering;
- timestamps;
- chronology;
- branch or merge policy;
- semantic diffing;
- LLM analysis;
- browser acquisition changes;
- compiler/RIR/runtime/export/measurement changes;
- researcher UI;
- root exports;
- README changes;
- `docs/CURRENT_STATE.md` changes.

## Tests

The focused 26C proof covers:

1. fresh exact declaration + explicit-sequence reconciliation with exact object chaining and human text retained by the fresh 26A sequence;
2. moved declaration and edge paths;
3. recomputed wrong starting identity that 26B verifies but 26C rejects;
4. recomputed reordered declaration that 26B verifies but 26C rejects at member 0;
5. omitted declared member rejected by count without discovery;
6. reversed explicit edge paths rejected through fresh 26A rather than reordered;
7. raw declaration integrity failure before any explicit edge loading;
8. valid declaration plus corrupted explicit edge rejected through fresh 26A/24C;
9. explicit loaded-23C-continuation starting predecessor support;
10. explicit-module importability and caller-input type boundaries.

## Result

26B made the human-owned sequence declaration durable.

26C makes that declaration useful after restart without turning it into a history index.

The researcher may now say:

```text
"Here is the declaration I preserved.
Here is the start I explicitly trust as application evidence.
Here are the files I explicitly chose, in this order.
Re-establish whether they are the segment I declared."
```

Pyxis can answer that exact question—and no stronger one.
