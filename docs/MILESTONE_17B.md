# Milestone 17B — Human-Owned Selection Note

## Product question

Can a researcher attach one human-authored note to one exact 17A paragraph selection without Pyxis turning that note into page/source evidence, normalizing the caller's wording, inferring authorship or time, or introducing a generic annotation system?

17B answers **yes** through one narrow pure application boundary.

## Why this milestone exists

17A proved that a human can point to one exact already-returned paragraph from verified durable research evidence without Pyxis choosing, ranking, or semantically promoting that passage.

The next concrete researcher action is to record what the human thinks about that selected evidence.

That interpretation must remain separate from the source evidence it references.

## Boundary

```text
ChromiumPageResearchParagraphSelectionEvidence
    ↓
caller supplies one exact nonblank note string
    ↓
validate selection mode + exact paragraph object identity
    ↓
preserve caller text verbatim
    ↓
frozen ChromiumPageResearchParagraphNoteRecord
```

Public API:

```python
create_chromium_research_paragraph_note(
    selection,
    note_text=...,
)
```

Result:

```python
ChromiumPageResearchParagraphNoteRecord(
    note_mode="caller_authored_exact_text_on_paragraph_selection",
    selection=<exact 17A selection object>,
    note_text=<exact caller string>,
)
```

## Record, not page evidence

The result is intentionally named `ChromiumPageResearchParagraphNoteRecord`, not `...Evidence`.

The selected paragraph remains the page evidence. The note records what the caller wrote about that evidence.

The note does not become:

- evidence that the page says what the note says;
- evidence that the note is true;
- evidence that the selected paragraph supports the note;
- a verified quotation;
- a citation;
- a source-authenticity claim;
- a relevance score;
- a machine interpretation.

The note and the selected evidence are linked but retain different authority.

## Exact selection identity

17B accepts only a `ChromiumPageResearchParagraphSelectionEvidence` using the established 17A selection mode.

The selected paragraph must still be the **exact object by identity** at its recorded ordinal inside the exact loaded-capture source retained by the selection.

An equal-by-value copy is rejected.

This prevents a downstream caller from fabricating a structurally similar paragraph object and attaching a note while presenting it as the exact source evidence selected under 17A.

17B does not rerun the complete 17A source validator, reopen the capture file, or reacquire Chromium. 17A owns selection creation; 17B checks only the identity facts necessary for its own boundary.

## Verbatim caller text

`note_text` must be a Python string containing at least one non-whitespace character.

The nonblank check uses whitespace stripping only as validation. The stored text itself is not stripped or normalized.

Leading/trailing spaces, line breaks, Unicode, punctuation, capitalization, spelling, and wording remain exactly as supplied.

17B adds no note-length policy because no concrete product requirement has earned an arbitrary truncation limit at this layer.

## No inferred metadata

17B deliberately does not invent metadata it did not observe.

The note record contains no:

- timestamp;
- author/user ID;
- device identity;
- session identity;
- note title;
- tag;
- category;
- confidence;
- relevance;
- claim type;
- question type;
- rationale type.

A future need for any of those must define how that fact is actually acquired and what authority it carries.

## Tests

Focused tests prove:

1. the record is frozen and retains the exact supplied 17A selection object;
2. caller text containing whitespace, Unicode, punctuation, and line breaks is preserved verbatim;
3. non-string and whitespace-only notes are rejected;
4. an unsupported/forged selection mode is rejected;
5. an equal-by-value but non-identical paragraph object is rejected;
6. the public `select → note` composition retains both human actions and the exact underlying loaded-capture/paragraph identity.

## Validation

Implementation/public API proof:

- Actions #566 on `133d5062ec0788f542671c5ceefd4f4b78db6e6c` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 log: **280 collected / 280 passed in 38.96s**;
- inspected Python 3.12 log: **280 collected / 280 passed in 28.80s**;
- all six 17B focused tests passed alongside the complete existing browser/capture/selection and Repository Zero suites.

## Explicit non-goals

17B adds no:

- browser acquisition or control;
- capture-file read or verification;
- persistence of notes or selections;
- note editing/update/delete semantics;
- multi-note collection or notebook abstraction;
- generic annotation registry;
- tags, categories, labels, or note types;
- inferred author identity or timestamps;
- relevance, importance, confidence, or truth scoring;
- claim/support/contradiction modeling;
- quotation or citation verification;
- source verification or provenance authentication;
- semantic passage extraction;
- cross-family semantic joins;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

## Decision — D132

**One explicit 17A paragraph selection may be linked to one immutable caller-authored note record whose text is preserved verbatim. The note record retains the exact selection object and therefore the exact selected source-evidence identity, but caller-authored interpretation remains distinct from page/source evidence: attaching a note does not establish relevance, truth, claim support, quotation validity, citation authority, source authenticity, authorship identity, observation time, or machine interpretation. Downstream note creation may validate the exact selection/paragraph identity required for its own boundary, but it must not reacquire browser state or silently redo upstream capture/selection authority.**
