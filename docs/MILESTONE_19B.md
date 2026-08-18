# Milestone 19B — Human-Owned Comparison Note

## Product question

Can a researcher write one explicit human-authored interpretation over an already-valid 19A exact-range comparison while Pyxis preserves the comparison and the note as separate authority layers?

19B answers **yes** through one narrow comparison-note boundary.

## Why this milestone exists

19A introduced:

```text
exact 18A range A
        \
         → explicit human juxtaposition
        /
exact 18A range B
```

That record says only that the caller chose to examine two exact ranges together. It deliberately does not say why.

19B adds the next researcher-owned action:

```text
source evidence
    ↓
exact selections
    ↓
human juxtaposition
    ↓
human-authored comparison note
```

The note may explain similarity, difference, tension, uncertainty, context, or any other human interpretation, but Pyxis does not adopt that interpretation as source evidence or machine judgment.

## Public API

```python
create_chromium_research_paragraph_text_selection_comparison_note(
    comparison,
    note_text=...,
)
```

returns:

```python
ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord(
    note_mode="caller_authored_note_on_exact_text_range_comparison",
    comparison=<exact caller-supplied 19A object>,
    note_text=<verbatim caller text>,
)
```

The returned record is frozen.

## Exact comparison retention

19B retains the exact `ChromiumPageResearchParagraphTextSelectionComparisonRecord` supplied by the caller.

It does not replace that object with a newly-created equal-by-value comparison after validation.

This is important because runtime ownership remains explicit:

```text
validation result
≠
caller-supplied comparison identity
```

A focused test creates an equal-by-value copy of a valid 19A record, supplies that copy to 19B, and proves that the resulting note retains the copy itself rather than the original object or a third reconstructed object.

## Comparison validity remains owned by 19A

19B does not create a competing comparison validator.

It requires the established 19A comparison mode:

```text
caller_explicit_exact_text_range_comparison
```

and delegates validity back through the public 19A operation:

```python
create_chromium_research_paragraph_text_selection_comparison(
    comparison.first_selection,
    comparison.second_selection,
)
```

19A in turn delegates each exact-range relationship back through 18A.

Therefore 19B inherits, rather than duplicates:

- exact 17A source-owned paragraph identity;
- exact 18A range mode and Unicode code-point coordinates;
- bounded returned-prefix validation;
- the 19A rule that cross-capture pairing is allowed;
- the 19A rule that same-selection pairing is allowed without significance judgment.

## Verbatim human text

`note_text` must be a string containing at least one non-whitespace character.

If accepted, Pyxis stores it exactly as supplied, including:

- leading and trailing whitespace;
- line breaks;
- Unicode;
- punctuation;
- capitalization;
- wording.

Validation may inspect `note_text.strip()` only to reject whitespace-only input. It does not normalize the stored value.

## What the note means

The note is a **human record attached to a human-owned juxtaposition**.

It is not source evidence.

For example, a researcher may write:

```text
These passages appear to frame the same event differently.
```

Pyxis records that sentence as caller-authored interpretation. Pyxis does not thereby establish that the passages actually concern the same event, differ materially, contradict one another, or support any claim.

Likewise, the note may be wrong, speculative, provisional, rhetorical, or incomplete. 19B preserves who supplied the interpretation rather than silently promoting it.

## Tampered comparison relationships remain falsifiable

19B re-establishes the supplied comparison through 19A before attaching the note.

If one nested exact range retains a paragraph replaced by an equal-by-value but non-source-owned object, 18A rejects the chain through the existing identity proof.

If one nested range is changed to an out-of-bounds coordinate such as:

```text
end_offset = 999
```

18A rejects that relationship through bounded returned-evidence validation.

Thus:

```text
comparison-shaped dataclass
≠
currently valid comparison relationship
```

and adding human prose does not weaken that distinction.

## What successful 19B creation proves

Successful creation proves only that:

1. the caller supplied one comparison-shaped 19A record;
2. its comparison mode is the established caller-owned comparison mode;
3. its two nested exact-range selections can be re-established through 19A and 18A;
4. the caller supplied non-whitespace note text;
5. Pyxis retained the exact supplied comparison object and exact supplied note text together in one immutable record.

It does **not** prove:

- that the note is true;
- that the note is relevant;
- that the compared passages are similar;
- that the compared passages differ;
- that either passage contradicts or corroborates the other;
- that either passage supports a claim;
- that either source is authentic or reliable;
- that the researcher is correctly identified;
- when the note was written;
- that the note is a valid quotation or citation;
- that any machine agrees with the interpretation.

## Epistemic separation

19B extends the authority chain without collapsing it:

```text
source evidence
≠
human selection
≠
human juxtaposition
≠
human interpretation
```

The comparison note makes the last layer concrete while preserving the previous three intact.

## Focused tests

Seven focused tests cover:

1. exact comparison-object retention plus verbatim whitespace, Unicode, punctuation, and line breaks;
2. refusal of non-string and whitespace-only note text;
3. refusal of non-19A comparison inputs;
4. refusal of unsupported comparison mode;
5. reuse of 19A/18A parent-identity and bounded-coordinate validation, including equal-by-value paragraph substitution and `end_offset=999` tampering;
6. revalidation without replacement of an equal-by-value but distinct supplied comparison object;
7. exposure through the public `pyxis.app` surface.

## Validation

Behavior/public-API proof:

- draft PR #27 Actions **#643** completed successfully on Python 3.11, 3.12, 3.13, and 3.14 for review head `49689930c145cc63af4874b122b1378cc68c7a53`;
- Python 3.11 collected **332 tests / 332 passed in 38.68s**;
- all seven focused 19B tests passed alongside the complete established Repository Zero/browser/capture/selection/note/durability/relinking/comparison suite;
- the PR-context checkout merged that exact head into current `main` before running the suite, preserving the independent review-context pattern used by prior milestones.

## Explicit non-goals

19B adds no:

- comparison-note persistence or sidecar;
- comparison-note relinking;
- machine-authored comparison prose;
- similarity or distance score;
- contradiction, entailment, or corroboration detection;
- claim or support model;
- relevance or confidence judgment;
- quotation/citation verification;
- source authentication;
- author identity or trusted timestamp;
- automatic source discovery;
- browser acquisition, navigation, or control;
- capture reread;
- embeddings or LLM work;
- notebook, collection, or generic annotation framework;
- researcher UI.

## Decision — D140

**Pyxis may attach one caller-authored note to one caller-owned 19A exact-range comparison only after re-establishing that comparison through the existing public 19A boundary, which in turn preserves 18A range validity. The resulting immutable note record must retain the exact caller-supplied comparison object and the caller's note text verbatim. The note is human interpretation attached to human juxtaposition; it does not become source evidence and does not establish similarity, difference, contradiction, corroboration, support, relevance, reliability, authenticity, truth, quotation/citation validity, author identity, trusted time, or machine agreement. 19B performs no browser acquisition, capture reread, persistence, automated comparison, claim modeling, or LLM interpretation. Source evidence, human selection, human juxtaposition, and human interpretation remain separate authority layers.**
