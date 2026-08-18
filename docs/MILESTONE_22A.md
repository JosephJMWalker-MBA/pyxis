# Milestone 22A — Human-Owned Working-Set Note Revision

## Product question

Can a researcher revise one existing human-authored working-set rationale without mutating or erasing the prior wording, while keeping both versions attached to the same exact working-set object and without asking Pyxis to judge why the interpretation changed?

22A answers **yes**.

## Why this milestone exists

21A–21C established a complete rationale loop:

```text
20A human-owned working set
 ↓
21A human-authored rationale
 ↓
21B durable rationale
 ↓
21C verified durable rationale relinking
```

That lets a researcher preserve and reopen:

```text
"this is why I am carrying these pieces together"
```

But research is not static.

After reading more material, the researcher may reasonably say:

```text
"I no longer phrase my interpretation that way."
```

The wrong implementation would be to mutate the prior note in place. That would destroy the exact earlier human wording and make later reasoning look more stable than it actually was.

22A therefore adds the narrow next human action:

```text
prior human rationale
      ↓
explicit human revision
      ↓
new human rationale
```

while preserving the prior note exactly.

## Public module API

```python
create_chromium_research_working_set_note_revision(
    prior_note,
    revised_note_text=...,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRevisionRecord(
    revision_mode="caller_authored_revision_of_research_working_set_note",
    prior_note=<exact supplied 21A note object>,
    revised_note=<new 21A note over exact same working-set object>,
)
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_note_revision
```

22A does not broaden the `pyxis.app` root re-export surface.

## Revision is append-only, not mutation

22A never changes the supplied prior note.

Instead it returns one new immutable record that retains:

```text
exact prior note object
+
new revised note object
```

The prior note remains independently usable and inspectable.

Therefore:

```text
human revision
≠
in-place overwrite
```

and:

```text
new interpretation
≠
erasure of old interpretation
```

This makes changes in the researcher's thinking representable rather than invisible.

## The same exact working set is retained

The revised note is created through public 21A using:

```python
prior_note.working_set
```

The returned relationship is therefore:

```text
revision.revised_note.working_set is revision.prior_note.working_set
```

22A does not create a new working-set membership decision.

If membership itself should change, the researcher must create another 20A working set explicitly.

Thus:

```text
revision of rationale
≠
revision of evidence membership
```

This distinction prevents a text edit from silently changing which evidence the researcher had grouped together.

## The prior note is re-established through 21A

22A does not trust the outer dataclass type alone.

Before accepting a revision it calls the public 21A constructor over the supplied prior note's exact working set and text.

That reuses:

- 21A note-mode authority;
- 20A working-set member-coherence authority;
- the established human-text contract.

The validation result is discarded.

The returned revision retains the exact caller-supplied prior note object.

Therefore:

```text
validation object
≠
recorded prior-note object
```

and:

```text
reuse established authority
≠
duplicate validation logic
```

## A 21C-reconstructed note can be revised

21C returns:

```text
loaded.note
```

as one reconstructed 21A human note attached to the exact working set reconstructed through 20C.

22A accepts that `loaded.note` directly.

It does not require the 21C wrapper or consume the retained 21B/20C verification evidence.

That separation is intentional.

21C answers:

```text
"this durable rationale was coherently relinked to this durable parent"
```

22A answers:

```text
"the human is now revising this already-established in-memory rationale"
```

Thus:

```text
fresh durable relinking
≠
prerequisite for every subsequent human revision
```

## 22A performs no file reads

22A consumes only one in-memory 21A note record and caller-supplied revised text.

It does not read:

- the 21B working-set-note sidecar;
- the 20B working-set sidecar;
- any 17C/18C/19C member sidecar;
- any source capture;
- browser state.

A note reconstructed through 21C may therefore be revised after those files move or disappear during the current application lifetime.

This proves only:

```text
ability to revise already-established in-memory human interpretation
```

It does not prove deleted durable artifacts remain recoverable or freshly verifiable.

## Human revised text remains verbatim

`revised_note_text` is caller-authored text.

22A preserves accepted text exactly through 21A, including:

- leading whitespace;
- trailing whitespace;
- line breaks;
- Unicode;
- punctuation;
- capitalization;
- uncertainty;
- tentative language;
- unresolved questions.

Whitespace-only revised text is rejected.

Accepted text is not normalized, summarized, corrected, classified, ranked, or rewritten.

## Exact no-ops are rejected

If:

```text
revised_note_text == prior_note.note_text
```

22A rejects the operation.

That comparison is exact string equality only.

It does not attempt to determine semantic equivalence.

Therefore:

```text
"Same words"
→ "Same words"
```

is rejected as no revision event.

But:

```text
"Same words"
→ " Same words "
```

is accepted because the human supplied different exact wording.

This does not mean Pyxis considers the whitespace change important.

It means Pyxis refuses to invent semantic equivalence beyond exact equality.

Thus:

```text
exact textual difference
≠
semantic difference
```

## Revision chains are application relationships, not durable history yet

A caller may take:

```text
v1
```

revise it to:

```text
v2
```

then pass the resulting revised 21A note into another 22A action to produce:

```text
v3
```

The earlier immutable records remain unchanged.

This permits an application-level append-only sequence such as:

```text
v1 → v2 → v3
```

But 22A does not yet serialize that lineage.

It therefore does not establish:

- durable revision IDs;
- durable predecessor references;
- revision-number authority;
- trusted chronology;
- persisted revision history.

Those would require separate authority boundaries.

## Revision does not explain itself

22A stores no machine-generated or machine-inferred explanation for why the researcher changed wording.

It does not calculate:

- semantic diffs;
- confidence changes;
- contradiction detection;
- evidence gains/losses;
- support scores;
- belief strength;
- correctness improvements.

The researcher may revise from:

```text
"These records probably describe one event."
```

to:

```text
"I now think these records describe separate events."
```

22A records only the exact human transition between two pieces of wording.

It does not conclude that either wording is true.

## Authority boundary

The relevant chain is now:

```text
source evidence
≠
human selection
≠
human working-set membership
≠
human working-set rationale
≠
human revision of rationale
≠
source truth
≠
machine semantic judgment
```

Revision provenance is human-action provenance, not semantic authority.

## What successful 22A creation proves

Successful 22A creation proves only that:

1. the caller supplied one established 21A working-set note record;
2. the supplied prior note re-establishes through the existing 21A/20A coherence boundaries;
3. the caller supplied non-whitespace string revised text;
4. the revised text differs exactly from the prior text;
5. Pyxis retained the exact caller-supplied prior note object;
6. Pyxis created one new 21A note over the exact same working-set object;
7. the new human text is preserved verbatim.

This is:

```text
append-only human revision of one working-set rationale
```

## What successful 22A creation does not prove

22A does **not** prove:

- why the researcher changed the note;
- that the revised note is more accurate;
- that the prior note was wrong;
- that either note is true;
- semantic difference beyond exact string inequality;
- source support, contradiction, corroboration, entailment, or causation;
- relevance, completeness, or representativeness;
- source authenticity or reliability;
- quotation or citation validity;
- claim support;
- authorship identity;
- trusted time or chronology;
- chain of custody;
- machine agreement;
- durable revision identity;
- durable revision lineage;
- current file availability;
- browser freshness.

## Focused tests

Nine focused tests cover:

1. exact prior-note identity retention, exact same working-set object retention, verbatim revised Unicode/multiline text, immutability, and prior-note non-mutation;
2. successful revision of a note reconstructed through 21C;
3. successful revision after the 21B note sidecar, 20B working-set sidecar, and all individual member sidecars are deleted, proving no hidden file reread;
4. rejection of wrong prior type, non-string revised text, and whitespace-only revised text;
5. rejection of exact textual no-op while accepting an exact whitespace change;
6. rejection of incoherent nested member state through delegated 21A/20A validation;
7. rejection of an unsupported prior note mode;
8. append-only `v1 → v2 → v3` chaining without mutation of earlier records;
9. explicit public module importability.

## Explicit non-goals

22A adds no:

- in-place note editing;
- revision persistence;
- revision verification;
- revision relinking;
- revision IDs;
- revision numbering;
- timestamps;
- authorship verification;
- reason-for-change field;
- semantic diff;
- confidence model;
- claim model;
- notebook database;
- title/folder/tag/label taxonomy;
- search;
- ranking;
- deduplication;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- compiler/RIR/runtime/export/measurement changes;
- researcher UI.

## Decision — D149

**Pyxis may represent one human-owned revision of one existing 21A working-set note as a new immutable append-only application record. The operation must re-establish the supplied prior note through the public 21A constructor and its delegated 20A working-set coherence boundary, discard that validation result, and retain the exact caller-supplied prior note object. The revised wording must be a non-whitespace string, must differ from the prior note by exact string inequality, and must be preserved verbatim by creating one new 21A note over the exact same working-set object. The prior note must never be mutated or replaced. A 21C-reconstructed note may participate through its `.note` value without requiring fresh durable verification, and 22A must perform no file reads. Exact textual difference establishes only that the human supplied different wording; it grants no semantic-difference, correctness, truth, support, authorship, chronology, or machine-judgment authority. Revision of rationale and revision of working-set membership remain separate human actions.**
