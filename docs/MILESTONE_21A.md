# Milestone 21A — Human-Authored Working-Set Note

## Product question

Can a researcher attach verbatim human-authored text to one exact 20A research working set so Pyxis can preserve why the researcher is carrying those pieces forward together, without converting that rationale into source evidence, semantic authority, machine interpretation, or a notebook taxonomy?

21A answers **yes**.

## Why this milestone exists

20A–20C established a complete working-set representation loop:

```text
20A human-owned ordered working set
 ↓
20B durable identity-only working-set sidecar
 ↓
20C verified ordered relinking against caller-supplied loaded members
```

That lets a researcher preserve and later re-establish:

```text
"these are the pieces I am carrying forward together"
```

But Pyxis still has no explicit place for the next ordinary researcher action:

```text
"and this is why I am carrying them together"
```

Without 21A, that rationale would have to be forced into:

- one individual member note, even when it concerns the whole set;
- a filename or folder name;
- an external notebook with weaker attachment identity;
- machine-generated semantics that the researcher did not author.

21A adds only the narrow human-interpretation boundary.

## Public module API

```python
create_chromium_research_working_set_note(
    working_set,
    note_text=...,
)
```

returns:

```python
ChromiumPageResearchWorkingSetNoteRecord(
    note_mode="caller_authored_note_on_research_working_set",
    working_set=<exact supplied 20A working-set object>,
    note_text=<exact caller-authored text>,
)
```

The API is exposed through the explicit module:

```python
pyxis.app.chromium_research_working_set_note
```

21A does not broaden the `pyxis.app` root re-export surface.

## The parent is a 20A working-set record

21A accepts:

```python
ChromiumPageResearchWorkingSetRecord
```

not:

```python
ChromiumPageResearchLoadedWorkingSetRecord
```

A working set reconstructed through 20C participates through:

```python
loaded.working_set
```

This distinction is intentional.

20C verification evidence answers:

```text
"this durable working-set reference was coherently re-established against these supplied loaded members"
```

21A answers a different question:

```text
"the human wrote this text about this working-set object"
```

The researcher should not need a fresh disk-load wrapper merely to interpret an already-valid in-memory working set.

Thus:

```text
fresh durable relinking
≠
prerequisite for human interpretation
```

## The exact supplied working-set object is retained

21A validates through 20A but does not replace the caller's object with a newly constructed one.

The operation:

1. confirms the input is a `ChromiumPageResearchWorkingSetRecord`;
2. confirms the established working-set mode;
3. calls the public 20A constructor over the exact retained item sequence;
4. discards the validation result;
5. stores the exact caller-supplied working-set object in the note record.

Therefore:

```text
validation object
≠
recorded parent object
```

and successful creation preserves:

```text
note.working_set is supplied_working_set
```

This matters because runtime object identity is part of the current application-state relationship even though it is not a durable identity claim.

## 20A remains the owner of member coherence

21A does not reproduce the validation logic for:

- 17D paragraph-note records;
- 18D exact-range-note records;
- 19D comparison-note records;
- their nested note/source relationships;
- their retained sidecar verification facts.

Instead it delegates to:

```python
create_chromium_research_working_set(working_set.items)
```

Therefore an outer working-set dataclass whose nested member verification has been forged or made incoherent is rejected by the existing 20A boundary.

This preserves the architecture rule:

```text
reuse established authority
≠
duplicate validation
```

## Human text is retained verbatim

`note_text` is caller-authored text.

21A preserves exactly:

- leading whitespace;
- trailing whitespace;
- line breaks;
- Unicode;
- punctuation;
- capitalization;
- tentative wording;
- unresolved questions;
- uncertainty;
- contradiction in the researcher's own thinking.

Whitespace-only text is rejected because it does not constitute a note.

The accepted text is not normalized, summarized, corrected, classified, or rewritten.

Thus:

```text
human wording
=
human wording
```

not:

```text
human wording
→ machine-cleaned interpretation
```

## The note is about the set, not evidence from the set

A researcher might write:

```text
"These three records may describe the same operational failure from different angles."
```

21A records only:

```text
researcher authored that sentence about this working set
```

It does not establish:

```text
the three records actually describe the same failure
```

Similarly, the researcher may write words such as:

- supports;
- contradicts;
- confirms;
- weakens;
- explains;
- likely;
- suspicious;
- important;
- representative.

Those words remain human interpretation.

They do not become Pyxis judgments merely because they appear in a typed record.

The authority boundary is therefore:

```text
source evidence
≠
human member selection
≠
human working-set membership
≠
human working-set rationale
≠
machine semantic judgment
```

## 21A does not reread files

21A consumes only one in-memory 20A working-set record.

It does not read:

- the 20B working-set sidecar;
- individual 17C/18C/19C member sidecars;
- source-capture files;
- browser state.

A working set reconstructed through 20C can therefore receive a 21A note even after the working-set sidecar and individual member sidecars have subsequently moved or disappeared during the same application lifetime.

This proves only:

```text
human interpretation of already-loaded coherent application state
```

It does not prove that any deleted or moved file would freshly verify again.

Thus:

```text
current file availability
≠
ability to interpret already-loaded coherent state
```

## 21A is not a notebook model

21A deliberately adds no:

- title field;
- folder hierarchy;
- labels;
- tags;
- status;
- priority;
- theme field;
- category field;
- owner field;
- due date;
- timestamps;
- revision history;
- search index;
- sorting rule;
- ranking;
- automatic summary;
- semantic embedding.

The only new state is:

```text
one exact working set
+
one verbatim human note
```

This avoids turning the first set-level interpretive action into premature information architecture.

## 21A is not persistence

21A creates an in-memory immutable application record.

It does not serialize the working-set note.

It therefore makes no claim about:

- durable working-set-note identity;
- no-overwrite storage;
- canonical JSON;
- working-set-note SHA-256;
- later working-set-note relinking.

If durability becomes the next real researcher pressure, it must be earned separately rather than assumed by this milestone.

## What successful 21A creation proves

Successful 21A creation proves only that:

1. the caller supplied one established 20A working-set record;
2. the supplied working set uses the established human-owned ordered working-set mode;
3. its member sequence can be re-established through the existing public 20A coherence boundary;
4. the caller supplied non-whitespace string text;
5. Pyxis retained that text verbatim;
6. the returned immutable note record retains the exact caller-supplied working-set object.

This is:

```text
human-authored interpretation attached to one exact coherent working set
```

## What successful 21A creation does not prove

21A does **not** prove:

- that the members are semantically related;
- that the researcher's rationale is correct;
- that any member supports another;
- contradiction, corroboration, entailment, causation, or relevance;
- completeness or representativeness of the working set;
- importance or priority from member order;
- meaning from duplicate membership;
- source authenticity, reliability, or truth;
- quotation or citation validity;
- claim support;
- authorship identity beyond the fact that caller-supplied text entered this operation;
- trusted time;
- chain of custody;
- provenance upgrade;
- machine agreement;
- current file availability;
- fresh member-sidecar verification;
- browser freshness.

Human interpretation remains human interpretation.

## Focused tests

Seven focused tests cover:

1. exact working-set object retention, verbatim Unicode/multiline human text, and immutable note record behavior;
2. successful note creation over the exact 20A working set reconstructed by 20C, retaining its exact loaded members;
3. successful note creation after the 20B working-set sidecar and all individual member sidecars are deleted, proving no hidden file reread;
4. rejection of a non-working-set parent, non-string note text, and whitespace-only note text;
5. rejection of an unsupported working-set mode;
6. delegation to 20A for rejection of an in-memory member-verification mismatch hidden inside an outer working-set record;
7. explicit public module importability.

## Explicit non-goals

21A adds no:

- working-set-note persistence;
- working-set-note verification;
- working-set-note relinking;
- member discovery;
- digest lookup;
- source or member-file reread;
- notebook database;
- title/folder/tag/label taxonomy;
- search;
- ranking;
- deduplication;
- semantic clustering;
- similarity scoring;
- contradiction/corroboration detection;
- claim modeling;
- source authentication;
- quotation/citation verification;
- authorship verification;
- trusted timestamps;
- revision history;
- embeddings;
- LLM interpretation;
- browser acquisition/control;
- researcher UI.

## Decision — D146

**Pyxis may attach one verbatim caller-authored note to one exact established 20A research working-set record. The note operation must require the established human-owned ordered working-set mode, re-establish member coherence only by delegating to the public 20A working-set constructor over the retained member sequence, discard that validation result, and retain the exact caller-supplied working-set object as the note parent. Caller text must be a non-whitespace string and must be preserved byte-for-text semantics exactly as supplied, including whitespace, Unicode, punctuation, and line breaks. A 20C-loaded working set may participate through its reconstructed `.working_set` value, but 21A must not require or consume 20C verification evidence and must not reread the working-set sidecar, individual member sidecars, source captures, or browser state. The resulting note records only human interpretation about the working set and grants no semantic relationship, claim support, relevance, completeness, source authenticity, citation authority, authorship, trusted time, or machine-judgment authority. Human working-set membership and human rationale about that membership remain separate authority layers.**
