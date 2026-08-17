# Milestone 18B — Human-Owned Exact-Range Note

## Product question

Can a researcher attach one exact human-authored note to one exact 18A text-range selection without widening the range, reinterpreting the selected characters, duplicating 18A validation, or promoting the note into source/quotation/citation authority?

18B answers **yes** through one pure application boundary.

## Why this follows 18A

18A established a new researcher action:

```text
verified durable capture
    ↓
explicit paragraph selection
    ↓
explicit exact text range
```

That answers "which exact already-visible characters did the researcher choose?"

It does not answer the next human action:

```text
Why did those exact characters matter to the researcher?
```

17B already proved the correct epistemic shape for human interpretation at paragraph granularity: exact human-authored text may be attached to selected evidence while remaining distinct from source evidence.

18B carries that discipline forward at exact-range granularity without mutating the 17B schema into a generic union or introducing an annotation framework.

## Boundary

```text
ChromiumPageResearchParagraphTextSelectionEvidence
    ↓
caller supplies one exact nonblank note string
    ↓
validate 18A mode + offset unit
    ↓
reuse public 18A selector for parent/range validity
    ↓
preserve exact caller-supplied 18A object
    ↓
preserve note text verbatim
    ↓
ChromiumPageResearchParagraphTextSelectionNoteRecord
```

Public API:

```python
create_chromium_research_paragraph_text_selection_note(
    selection,
    note_text=...,
)
```

Result:

```python
ChromiumPageResearchParagraphTextSelectionNoteRecord(
    note_mode="caller_authored_exact_text_on_paragraph_text_selection",
    selection=<exact supplied 18A selection>,
    note_text=<verbatim caller text>,
)
```

## 18A owns range validity

18B intentionally does not implement a second coordinate/source validator.

After checking the concrete 18A mode and offset unit, it calls:

```python
select_chromium_research_paragraph_text(
    selection.source,
    start_offset=selection.start_offset,
    end_offset=selection.end_offset,
)
```

That existing public operation re-establishes:

- exact 17A paragraph-source identity;
- exact paragraph object identity inside the loaded capture;
- integer/boolean coordinate rules;
- zero-based half-open range semantics;
- Unicode code-point coordinates;
- returned-prefix bounds;
- truncated-suffix refusal.

The validation result is not substituted into the note. The note retains the exact caller-supplied 18A object.

This keeps ownership explicit:

```text
18A owns exact range validity
18B owns human interpretation attached to that range
```

## Exact selection identity remains visible

The note stores the exact supplied 18A selection object by identity.

Therefore its inspectable chain remains:

```text
16C loaded capture
    ↓
17A exact paragraph object
    ↓
18A exact code-point coordinates
    ↓
18B exact human note
```

18B does not copy the selected source substring into a new field. The selected text remains derived from 18A's coordinates and the original paragraph evidence.

## Verbatim human-authored text

The note text must be a Python `str` containing at least one non-whitespace character.

Validation may use `strip()` only to determine whether the supplied value is blank. The stored value itself is not normalized.

18B preserves exactly:

- leading/trailing whitespace;
- line breaks;
- Unicode;
- punctuation;
- capitalization;
- spelling;
- wording.

No author identity or timestamp is inferred.

## Selected source characters are not interpreted

18A requires a non-empty coordinate range, not semantically meaningful text.

18B preserves that rule.

A caller may, for example, select a single returned space character and attach a note explaining why that spacing mattered. 18B does not refuse the source selection because its derived text is whitespace.

This distinction is deliberate:

```text
selected source range: may contain any already-returned characters
human note: must contain non-whitespace caller-authored text
```

Pyxis records the human action without deciding whether the selected source characters are meaningful, important, relevant, or evidentiary.

## Forged range objects do not bypass 18A

`ChromiumPageResearchParagraphTextSelectionEvidence` is a public dataclass and can therefore be manually constructed or altered through ordinary Python techniques such as `dataclasses.replace()`.

18B does not trust the dataclass merely because its type matches.

Focused tests prove that:

- a forged range extending into a truncated/unreturned suffix is rejected through 18A;
- an equal-by-value replacement of the parent paragraph is rejected through 18A's exact-object identity requirement;
- unsupported text-selection mode or offset unit is rejected before note creation.

## Human interpretation remains separate from source evidence

The result is deliberately named `...NoteRecord`, not `...Evidence`.

The selected range remains source-derived selection evidence. The note records what the caller wrote about that selection.

Attaching the note does not establish:

- relevance or importance;
- factual truth;
- claim support;
- quotation validity;
- citation stability or authority;
- source/publisher authenticity;
- provenance or chain of custody;
- observation time;
- author identity;
- machine interpretation.

18B records human interpretation only.

## Tests

Six focused tests prove:

1. the exact 18A range object is retained, note text is verbatim, and the result is frozen;
2. a whitespace-only selected source range may still receive a human note without semantic reinterpretation;
3. non-string and whitespace-only note values are rejected;
4. unsupported range-selection mode and offset-unit values are rejected;
5. a forged range entering a truncated/unreturned suffix is rejected through the established 18A boundary;
6. an equal-by-value replacement of the parent paragraph is rejected through 18A exact-identity validation.

## Validation

Behavior/public API proof:

- Actions #602 on `25328976800b7c94db6b41fff9e9bafac0d67763` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 checked out exact head `25328976800b7c94db6b41fff9e9bafac0d67763`;
- **304 tests collected / 304 passed in 30.63s**;
- all six focused 18B tests passed alongside the complete established Repository Zero, Chromium, capture, paragraph-selection, paragraph-note durability, exact-range selection, and durable-note relinking stack.

## Explicit non-goals

18B adds no:

- browser acquisition, navigation, scrolling, or control;
- capture-file read or verification;
- source-text expansion;
- substring/fuzzy search;
- semantic passage extraction;
- copied selected-text storage;
- text-range mutation;
- paragraph-note schema generalization;
- generic annotation/note abstraction;
- note editing/deletion/history;
- multiple notes or notebook abstraction;
- tags, questions, claims, categories, or confidence scores;
- persistence of text-range selections or range notes;
- quotation/citation verification;
- source authentication or provenance verification;
- author identity or timestamp inference;
- LLM interpretation or generated notes;
- autonomous research workflow;
- researcher UI.

Those remain separate product questions.

## Decision — D136

**One exact 18A paragraph-text selection may be linked to one immutable caller-authored note record whose text is preserved verbatim. Note creation must require the established 18A selection mode and Unicode code-point offset unit and must re-establish parent/range validity through the existing public 18A selection operation rather than creating a second coordinate/source-validation authority. The resulting note must retain the exact caller-supplied 18A selection object; validation may construct temporary 18A evidence but must not replace the caller's selection or copy the selected source text into a second representation. A non-empty selected source range may contain any already-returned characters, including whitespace or punctuation; Pyxis does not decide whether those characters are semantically meaningful. The note remains human interpretation distinct from page/source evidence and adds no relevance, importance, truth, claim-support, quotation-verification, citation-stability, source-authenticity, provenance, authorship, temporal, machine-interpretation, or browser-control authority.**
