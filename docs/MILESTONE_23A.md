# Milestone 23A — Human-Owned Revision Continuation

## Product question

Can a researcher continue from one already-verified durable human revision with another explicit human revision while preserving which exact verified revision is being continued, without rereading durable files, traversing revision history, assigning sequence numbers, or asking Pyxis to interpret what changed?

23A answers **yes**.

## Why this milestone exists

22A–22C established one complete durable revision edge:

```text
v1 human rationale
 ↓
22A human revision
 ↓
22B durable revision representation
 ↓
22C verified predecessor attachment + revision re-establishment
 ↓
v2 reconstructed human rationale
```

That closes one change-of-mind loop.

But research continues.

A researcher may later say:

```text
"I changed my mind again."
```

Public 22A could already revise the reconstructed `v2` note in memory.

What it did **not** preserve was the stronger provenance statement:

```text
"this new revision explicitly continues this exact verified 22C revision"
```

23A adds that narrow relationship.

It is intentionally not durable yet.

## Public module API

```python
create_chromium_research_working_set_note_revision_continuation(
    prior_revision,
    revised_note_text=...,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord(
    continuation_mode=(
        "caller_authored_continuation_of_verified_research_working_set_note_revision"
    ),
    prior_revision=<exact supplied 22C loaded record>,
    revision=<new 22A revision over exact reconstructed v2 note>,
)
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_note_revision_continuation
```

23A does not broaden the `pyxis.app` root re-export surface.

## Exact continuation relationship

The key object identity is:

```text
continuation.prior_revision is prior_revision
```

and:

```text
continuation.revision.prior_note
is
prior_revision.revision.revised_note
```

Therefore the new human revision does not merely happen to reuse the same wording or working set.

It is explicitly attached in application state to the exact verified durable revision object the caller supplied.

This distinguishes:

```text
human note with same content
≠
explicit continuation from this verified revision
```

## The same working set is retained

23A delegates new revision creation to public 22A using:

```python
prior_revision.revision.revised_note
```

22A then creates the new revised note over that exact prior note's working-set object.

Therefore:

```text
continuation.revision.revised_note.working_set
is
prior_revision.revision.revised_note.working_set
```

23A does not create a new evidence-membership decision.

Changing rationale again does not silently change the working set.

## 23A preserves v1 → v2 → v3 as application relationships

A successful sequence may now be represented as:

```text
v1
 ↓
verified durable 22C revision
 ↓
v2
 ↓
23A explicit continuation
 ↓
v3
```

Both earlier notes remain unchanged.

The loaded 22C record remains unchanged.

The 23A record retains it exactly.

Thus:

```text
continued revision
≠
mutation of earlier revision state
```

and:

```text
v3
≠
overwrite of v2
```

## The loaded predecessor is not trusted by outer dataclass shape alone

23A accepts one `ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord`.

But `isinstance(...)` is not treated as sufficient authority.

Before creating the new revision, 23A re-establishes the retained in-memory relationships using existing public 21A/22A constructors plus the verification facts already carried by the loaded 22C record.

It checks, among other things, that:

```text
22B predecessor-note format
=
21C loaded predecessor-note format
```

and:

```text
22B predecessor-note record SHA-256
=
21C retained predecessor-note record SHA-256
```

and that the loaded 22C revision still reconstructs through public 22A from:

```text
exact loaded predecessor note
+
verified revised human text
```

The reconstructed validation object is not substituted for the caller's loaded 22C object.

The exact supplied object is retained.

Therefore:

```text
outer dataclass shape
≠
coherent loaded predecessor state
```

## Falsifiability proof 1 — forged retained predecessor identity

Starting from one valid loaded 22C record:

```text
replace retained predecessor-note SHA-256
with another valid-looking digest
```

while leaving the outer loaded-record type intact.

23A rejects the object before creating v3.

This proves:

```text
loaded-record Python type
≠
retained predecessor identity coherence
```

## Falsifiability proof 2 — forged reconstructed v2 text

Starting from one valid loaded 22C record:

```text
replace loaded.revision.revised_note.note_text
with different text
```

while leaving the verified 22B revised text unchanged.

23A re-establishes the prior revision and detects that the retained reconstructed v2 text no longer matches the verified revision evidence.

It rejects before creating v3.

Thus:

```text
retained revised-note object
≠
authority merely because it is nested inside a loaded record
```

## 23A performs no file reads

23A consumes only:

```text
one already-loaded 22C record
+
one caller-supplied revised human text value
```

It does not open:

- the 20B working-set sidecar;
- the 21B predecessor-note sidecar;
- the 22B revision sidecar;
- any 17C/18C/19C member sidecar;
- any source capture;
- browser state.

A caller may therefore:

1. successfully load a revision through 22C;
2. remove those durable files from the current filesystem;
3. still create a 23A continuation from the already-loaded application evidence.

This proves only:

```text
current sidecar availability
≠
already-loaded verified revision application evidence
```

It does not make deleted durable artifacts recoverable.

## The new human wording remains verbatim

`revised_note_text` flows through public 22A.

Accepted text preserves exactly:

- leading whitespace;
- trailing whitespace;
- line breaks;
- Unicode;
- punctuation;
- capitalization;
- uncertainty;
- tentative language.

Whitespace-only text remains rejected.

No normalization or rewriting occurs.

## Exact no-op rejection remains owned by 22A

If the researcher supplies exactly the current reconstructed v2 wording again:

```text
v2 → v2
```

public 22A rejects the operation.

23A does not duplicate that logic.

A whitespace-only difference in otherwise equal non-whitespace text may still be accepted because 22A's revision boundary is exact string inequality, not semantic difference.

Thus:

```text
exact textual difference
≠
semantic difference
```

## No persistence yet

23A deliberately does not write a durable continuation artifact.

That choice prevents the milestone from prematurely deciding:

- whether a successor should reference a 22B revision or another successor format;
- whether repeated continuations should share one recursive format;
- whether a revised note should become a standalone durable 21B note;
- whether a continuation graph should permit branching;
- how explicit caller-supplied predecessor chains should be represented.

Those are durable-format authority decisions and require their own milestone.

23A earns only the human/application action first.

## No automatic chain traversal

23A does not search backward from v2 to v1.

It does not inspect filesystem directories for predecessors.

It does not follow digests.

It does not build:

```text
v1 → v2 → v3
```

from durable files automatically.

The caller explicitly supplies the already-loaded verified predecessor revision.

Therefore:

```text
explicit continuation relationship
≠
automatic revision-history reconstruction
```

## No chronology authority

The words `prior` and `continuation` describe the explicit human relationship represented by the supplied objects.

23A stores no clock time.

It does not establish:

- wall-clock ordering;
- trusted timestamps;
- revision numbers;
- sequence numbers;
- elapsed time;
- authorship identity;
- global history order.

Thus:

```text
explicit human predecessor relationship
≠
trusted chronology
```

## No semantic authority

23A records only that the human supplied another exact wording after explicitly choosing one verified revision as the predecessor.

It does not infer that v3 is:

- more correct;
- more supported;
- less supported;
- stronger;
- weaker;
- more certain;
- less certain;
- contradictory;
- corroborated;
- improved;
- closer to truth.

It does not explain why the human changed the note.

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
explicit human continuation from that verified revision
≠
semantic truth
```

23A adds human continuation provenance only.

## What successful 23A creation proves

Successful 23A creation proves only that:

1. the caller supplied one loaded 22C revision record;
2. its retained predecessor-note durable identity is coherent with its retained loaded predecessor;
3. its retained reconstructed revision can be re-established through public 22A from the exact loaded predecessor note and verified revised text;
4. the caller supplied another valid non-whitespace human text value;
5. that value differs exactly from the reconstructed v2 wording;
6. the exact caller-supplied loaded 22C object is retained;
7. the new 22A revision uses exactly the reconstructed v2 note as its prior note;
8. the new human text is preserved verbatim.

This is:

```text
explicit human continuation from one verified durable revision
```

## What successful 23A creation does not prove

23A does **not** prove:

- why the researcher changed the rationale again;
- semantic difference beyond exact string inequality;
- that v3 is more accurate than v2;
- that v2 is more accurate than v1;
- that any wording is true;
- source support, contradiction, corroboration, entailment, or causation;
- relevance, completeness, or representativeness;
- source authenticity or reliability;
- quotation or citation validity;
- claim support;
- authorship identity;
- trusted time or chronology;
- chain of custody;
- machine agreement;
- a durable v2 → v3 edge;
- automatic v1 → v2 → v3 traversal;
- revision numbering;
- current file availability;
- browser freshness.

## Focused tests

Nine focused tests cover:

1. exact loaded-predecessor identity retention, exact v2 prior-note identity, exact working-set identity, verbatim Unicode/multiline v3 text, and record immutability;
2. explicit `v1 → v2 → v3` application relationships without mutation of v1, v2, or the loaded 22C record;
3. successful continuation after the 20B, 21B, 22B, and individual member sidecars are deleted, proving no hidden file reread;
4. rejection of wrong predecessor type, non-string revised text, and whitespace-only revised text;
5. rejection of exact v2 textual no-op;
6. acceptance of an exact whitespace change without semantic promotion;
7. rejection of a forged retained predecessor-note durable identity;
8. rejection of forged reconstructed v2 wording that disagrees with retained verified revision evidence;
9. explicit public module importability.

## Explicit non-goals

23A adds no:

- persistence;
- durable continuation format;
- durable successor reference;
- revision-chain loader;
- recursive traversal;
- predecessor discovery;
- digest search;
- revision numbers;
- timestamps;
- trusted chronology;
- authorship verification;
- semantic diff;
- confidence model;
- claim model;
- notebook database;
- taxonomy;
- search;
- ranking;
- deduplication;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- compiler/RIR/runtime/export/measurement changes;
- researcher UI.

## Decision — D152

**Pyxis may represent one new human working-set-note revision as an explicit continuation of one already-loaded 22C verified durable revision. The operation must retain the exact caller-supplied loaded predecessor object; must re-establish its retained in-memory predecessor identity and reconstructed revision relationships without rereading durable files; and must create the new revision through public 22A over exactly the predecessor revision's reconstructed revised note. Exact textual no-ops remain rejected by 22A. The continuation is application-state provenance only and establishes neither durable history nor chronology nor semantic authority.**
