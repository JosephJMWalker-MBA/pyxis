# Milestone 24A — Verified Continuation Extension

Decision: D155

## Product question

Can a researcher who has successfully reopened one durable 23B continuation through 23C change their rationale again while preserving the stronger application-state statement:

```text
"this new human revision explicitly continues this exact verified durable continuation"
```

without rereading files, introducing recursive durable history, assigning revision numbers, or asking Pyxis to interpret what changed?

24A answers **yes**.

## Why this milestone exists

22A–22C established one durable human revision edge:

```text
v1
 ↓
v2
```

23A–23C established and reopened one explicit continuation:

```text
v1
 ↓
v2
 ↓
v3
```

After 23C, the researcher has a freshly reconstructed v3 note attached to one verified durable continuation.

Research does not stop there.

The next ordinary action is:

```text
"I changed my mind again."
```

Public 22A could already revise the v3 note by itself.

But doing only that would lose the stronger provenance statement that the new revision was explicitly made from this exact loaded 23C continuation.

24A adds that narrow application-state relationship.

It deliberately does not decide the durable recursive-history format.

## Public module API

```python
create_chromium_research_working_set_note_revision_continuation_extension(
    prior_continuation,
    *,
    revised_note_text=...,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord(
    extension_mode=(
        "caller_authored_extension_of_verified_research_working_set_note_revision_continuation"
    ),
    prior_continuation=<exact supplied 23C loaded record>,
    revision=<new 22A revision over exact reconstructed v3 note>,
)
```

The API lives in:

```text
pyxis.app.chromium_research_working_set_note_revision_continuation_extension
```

24A does not broaden the `pyxis.app` root export surface.

## Exact extension relationship

Successful creation retains:

```text
extension.prior_continuation
is
prior_continuation
```

and:

```text
extension.revision.prior_note
is
prior_continuation.continuation.revision.revised_note
```

The new v4 wording therefore does not merely happen to use the same working set or the same v3 string.

It is explicitly attached in application state to the exact verified 23C continuation object the caller supplied.

Thus:

```text
same v3 wording
≠
explicit extension of this verified durable continuation
```

## The working set remains unchanged

24A delegates new revision creation to public 22A over:

```python
prior_continuation.continuation.revision.revised_note
```

Public 22A creates the revised note over that exact prior note's working-set object.

Therefore:

```text
extension.revision.revised_note.working_set
is
prior_continuation.continuation.revision.revised_note.working_set
```

Changing rationale again does not silently create a new working-set membership decision.

## v1 → v2 → v3 → v4 is represented without mutation

A successful application-state sequence may now be represented as:

```text
v1
 ↓
22C verified durable revision
 ↓
v2
 ↓
23C verified durable continuation
 ↓
v3
 ↓
24A explicit extension
 ↓
v4
```

The earlier v1, v2, and v3 note objects remain unchanged.

The loaded 22C predecessor remains unchanged.

The loaded 23C continuation remains unchanged.

24A appends a new explicit human action rather than overwriting prior interpretation.

Therefore:

```text
v4
≠
mutation of v3
```

and:

```text
extension
≠
rewrite of earlier durable provenance
```

## Loaded 23C state is not trusted by Python type alone

24A accepts one:

```python
ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
```

but `isinstance(...)` is not treated as sufficient authority.

Before creating v4, 24A re-establishes retained in-memory relationships from the evidence already carried by the loaded 23C record.

It checks the retained 23B verification facts, including:

```text
continuation format
predecessor revision format
continuation mode
revision mode
revised-note mode
```

It checks that the predecessor revision content identity retained by 23B still matches the retained 22C predecessor:

```text
23B prior revision-record SHA-256
=
22C loaded predecessor revision-record SHA-256
```

using constant-time digest comparison.

It then reconstructs the prior continuation through public 23A using:

```text
exact retained 22C predecessor
+
verified v3 wording
```

and checks the exact object relationships retained by the loaded 23C record.

Therefore:

```text
loaded-record Python shape
≠
coherent verified-continuation application state
```

## Falsifiability proof 1 — forged retained predecessor identity

Start with a valid loaded 23C record.

Replace only the retained 23B predecessor revision digest with another valid-looking SHA-256 while keeping the outer dataclass type unchanged.

24A rejects before creating v4.

This proves:

```text
outer loaded-record type
≠
retained predecessor identity coherence
```

## Falsifiability proof 2 — forged reconstructed v3 wording

Start with a valid loaded 23C record.

Replace:

```text
loaded.continuation.revision.revised_note.note_text
```

with different wording while leaving the retained verified 23B v3 text unchanged.

24A re-establishes the prior continuation and rejects the mismatch before creating v4.

Therefore:

```text
nested v3 note object
≠
authority merely because it is carried by a loaded wrapper
```

## 24A performs no file reads

24A consumes only:

```text
one already-loaded 23C continuation record
+
one caller-supplied revised human text value
```

It does not open:

- the 20B working-set sidecar;
- the 21B predecessor-note sidecar;
- the 22B revision sidecar;
- the 23B continuation sidecar;
- any 17C/18C/19C member sidecar;
- any source capture;
- browser state.

A caller may therefore:

1. successfully load through 23C;
2. remove every related sidecar from the current filesystem;
3. still create a 24A extension from the already-loaded application evidence.

This proves only:

```text
current file availability
≠
already-loaded verified-continuation application evidence
```

It does not make deleted artifacts recoverable.

## New human wording remains verbatim

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

Whitespace-only text is rejected.

No normalization or rewriting occurs.

## Exact no-op rejection remains owned by 22A

If the researcher supplies the exact reconstructed v3 wording again:

```text
v3 → v3
```

public 22A rejects the operation.

24A does not duplicate that rule.

A non-whitespace string that differs only in whitespace may still be accepted because the revision boundary remains exact string inequality rather than semantic difference.

Thus:

```text
exact textual difference
≠
semantic difference
```

## No persistence in 24A

24A intentionally does not write a durable v3 → v4 artifact.

That leaves the next durable-format question explicit rather than silently deciding whether:

- a 23B continuation becomes a legal durable predecessor;
- a new successor format references 23B directly;
- repeated continuations use one recursive union format;
- branching is permitted;
- successor/predecessor discovery exists;
- chain traversal exists.

Those are durable-history authority decisions.

24A earns only the human/application action first.

## No automatic chain traversal

Although application state can now explicitly represent:

```text
v1 → v2 → v3 → v4
```

24A does not discover or traverse that chain.

The caller explicitly supplies one already-loaded 23C continuation.

24A does not search directories, follow hashes, resolve predecessors, construct a DAG, or infer a history head.

Therefore:

```text
explicit extension relationship
≠
revision-history engine
```

## No chronology authority

The terms `prior` and `extension` describe explicit human/object relationships.

24A adds no:

- timestamp;
- trusted clock;
- revision number;
- sequence number;
- monotonic counter;
- elapsed duration;
- global ordering;
- authorship identity.

Thus:

```text
explicit predecessor relationship
≠
trusted chronology
```

## No semantic authority

24A records only that the human supplied another exact wording after explicitly selecting one verified continuation as the predecessor state.

It does not infer that v4 is:

- more correct;
- less correct;
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

It does not infer why the human changed the note.

## Authority boundary

The browser/research authority chain now includes:

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
human continuation
≠
durable continuation representation
≠
verified continuation relinking
≠
human extension of that verified continuation
≠
semantic truth
```

24A adds explicit human continuation-of-continuation provenance in application state only.

## Successful 24A creation proves only

A successful 24A result proves that:

1. the caller supplied one loaded 23C continuation record;
2. its retained 23B continuation format and modes are supported;
3. its retained predecessor revision durable identity matches its retained loaded 22C predecessor;
4. its retained v3 continuation can be re-established through public 23A from the exact retained predecessor and verified v3 wording;
5. the exact caller-supplied loaded 23C object is retained;
6. the caller supplied another valid non-whitespace human text value;
7. that value differs exactly from reconstructed v3 wording;
8. the new 22A revision uses exactly the reconstructed v3 note as its prior note;
9. the working-set object remains exact;
10. the new human text is preserved verbatim.

This is:

```text
explicit human extension from one verified durable continuation
```

## Successful 24A creation does not prove

24A does **not** prove:

- trusted chronology;
- revision numbering;
- automatic history traversal;
- that v4 is better than v3;
- that v3 is better than v2;
- that any wording is true;
- source support, contradiction, corroboration, entailment, or causation;
- relevance, completeness, or representativeness;
- source authenticity or reliability;
- quotation or citation validity;
- claim support;
- authorship identity;
- chain of custody;
- semantic difference beyond exact string inequality;
- a durable v3 → v4 edge;
- recursive durable revision history;
- branch or merge semantics;
- machine agreement.

## Scope discipline

24A adds only:

- one explicit application-state extension record;
- one constructor;
- retained-loaded-state validation;
- focused tests;
- this milestone document.

24A adds no:

- persistence;
- relinking;
- new durable format;
- recursive predecessor union;
- revision IDs or numbers;
- timestamps;
- branch/DAG semantics;
- automatic traversal;
- source refetch;
- claims;
- semantic diff;
- confidence scoring;
- LLM behavior;
- browser acquisition;
- compiler/RIR/runtime/export/measurement changes;
- UI;
- root re-export;
- README rewrite;
- CURRENT_STATE rewrite.

## Decision

D155 establishes:

> A researcher may explicitly extend one already-loaded verified durable continuation with another append-only human revision. Pyxis retains the exact loaded 23C predecessor object, re-establishes its retained in-memory coherence before use, creates the new wording through the existing 22A exact-text revision boundary over the exact reconstructed v3 note, and performs no file reads. This application-state extension adds no recursive durable-history, chronology, or semantic authority.
