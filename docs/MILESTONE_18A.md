# Milestone 18A — Human-Owned Exact Paragraph Text Selection

## Product question

Can a researcher refine one exact 17A paragraph choice to the exact already-visible characters that matter without Pyxis searching the paragraph, copying source text into a second representation, expanding truncated evidence, or claiming quotation/citation authority?

18A answers **yes** through one pure application boundary.

## Why this is a new phase

17A through 17D established a complete durable paragraph-note lifecycle:

```text
verified durable capture
    ↓
explicit paragraph selection
    ↓
human note
    ↓
durable note sidecar
    ↓
verified relinking
```

That lifecycle deliberately remained paragraph-granular. A researcher can say "this paragraph matters" and attach interpretation, but cannot yet represent "these exact already-visible characters are what I selected."

Adding another persistence mechanism would not answer that product gap. 18A therefore begins a new human-research phase with a narrower selection action rather than extending storage machinery.

## Boundary

```text
ChromiumPageResearchParagraphSelectionEvidence
    ↓
caller supplies start_offset + end_offset
    ↓
validate exact 17A paragraph identity
    ↓
require zero-based half-open range
    ↓
require range wholly inside returned text_prefix
    ↓
ChromiumPageResearchParagraphTextSelectionEvidence
```

Public API:

```python
select_chromium_research_paragraph_text(
    source,
    start_offset=...,
    end_offset=...,
)
```

Result:

```python
ChromiumPageResearchParagraphTextSelectionEvidence(
    selection_mode="caller_explicit_returned_paragraph_text_range",
    offset_unit="unicode_code_point",
    source=<exact supplied 17A selection>,
    start_offset=...,
    end_offset=...,
)
```

## Coordinates, not copied source text

18A intentionally does not store a new selected-text field.

The exact selected text is a derived property:

```python
selection.selected_text
```

which is computed from:

```text
selection.source.paragraph.text_prefix[start_offset:end_offset]
```

The durable/source hierarchy therefore remains inspectable:

```text
16C loaded capture
    ↓
17A exact paragraph object
    ↓
18A exact coordinates
    ↓
derived selected_text
```

The paragraph remains the source-text owner. 18A does not create a second quote-like source representation.

## Unicode coordinate semantics

Offsets are explicitly:

```text
zero-based
half-open [start_offset:end_offset)
Unicode code points
```

The result records:

```text
offset_unit="unicode_code_point"
```

This matches the code-point semantics already established for bounded Chromium text evidence. Python string slicing therefore has the same conceptual unit used by the existing observation contracts, including characters such as emoji.

A focused test selects offsets `1:4` from:

```text
A😀B café
```

and derives exactly:

```text
😀B 
```

without splitting the emoji into surrogate units.

## Caller owns the range

Pyxis does not search for a supplied substring or infer where a phrase begins or ends.

The caller supplies both coordinates explicitly.

18A therefore adds no:

- text matching;
- fuzzy matching;
- occurrence selection;
- semantic passage extraction;
- sentence segmentation;
- relevance ranking;
- model-selected highlights.

The operation records the caller's exact mechanical choice only.

## Bounded evidence remains bounded

18A operates only on the paragraph's already-returned `text_prefix`.

If a paragraph originally contained more characters than were returned, its existing evidence may truthfully contain:

```text
text_prefix="Alpha"
text_character_count=10
truncated=True
```

18A permits selecting the full returned prefix `0:5`.

It refuses `0:6` even though the complete character count says additional text existed. The count is evidence that more text existed; it is not authority to reconstruct or address characters Pyxis did not return.

The operation therefore does not:

- reconnect to Chromium;
- reread the capture file;
- enlarge the prior text limit;
- synthesize the hidden suffix;
- search another capture for the missing text.

## Exact parent identity remains required

The public 17A dataclass is constructible Python state, so 18A does not trust value equality alone.

Before refining a selection it confirms:

- the established 17A selection mode;
- the retained source is a `ChromiumPageResearchLoadedCaptureEvidence`;
- the retained paragraph is `ChromiumPageParagraphEvidence`;
- the paragraph ordinal addresses returned source evidence;
- the selected paragraph is the exact object by identity at that ordinal;
- the paragraph's character-count/limit/truncation facts remain coherent.

A focused test replaces the selected paragraph with an equal-by-value copy and proves 18A rejects it.

## Selection is not quotation verification

The name `selected_text` describes the exact substring of already-returned paragraph evidence at the caller's chosen coordinates.

It does not mean:

- the source publisher is authenticated;
- the paragraph is a faithful representation of some external canonical publication;
- the text remained unchanged after observation;
- the text is suitable as a stable citation;
- the selected range is semantically complete;
- the selection is relevant or important;
- the selection supports a claim;
- the selection is a legally/editorially verified quotation.

18A refines human-choice provenance only.

## Tests

Six focused tests prove:

1. exact 17A source identity is retained and Unicode text is derived from coordinates;
2. `selected_text` is not a stored dataclass field;
3. offsets require exact integers, reject Python booleans, use half-open semantics, and require a non-empty range;
4. an equal-by-value paragraph copy is rejected because exact source identity was lost;
5. an unsupported parent-selection mode is rejected;
6. the full returned prefix of truncated text may be selected but no coordinate may enter the unreturned suffix;
7. coordinates outside complete untruncated returned text fail explicitly.

Several assertions share test functions, so the milestone adds six tests rather than inflating the count artificially.

## Validation

Behavior/public API proof:

- Actions #593 on `c0edfb3dacfde1c5733d3cc35b32766a0d2e883d` passed on Python 3.11, 3.12, 3.13, and 3.14;
- inspected Python 3.11 checked out exact head `c0edfb3dacfde1c5733d3cc35b32766a0d2e883d`;
- **298 tests collected / 298 passed in 38.79s**;
- all six focused 18A tests passed alongside the complete established Repository Zero, Chromium, capture, paragraph-selection, note-persistence, and note-relinking stack.

## Explicit non-goals

18A adds no:

- browser acquisition, navigation, scrolling, or control;
- capture-file read or verification;
- source-text expansion;
- substring search or occurrence matching;
- sentence/semantic passage segmentation;
- copied selected-text storage field;
- quote object or quotation-verification claim;
- citation locator or citation-stability claim;
- relevance/importance/confidence score;
- claim/support semantics;
- note attachment to text-range selections;
- persistence of text-range selections;
- multi-range selection set;
- generic selection registry;
- source authentication or provenance verification;
- timestamp or observation-time inference;
- LLM interpretation or generated highlights;
- researcher UI.

Those remain separate product questions.

## Decision — D135

**One exact 17A paragraph selection may be refined by the caller into one non-empty zero-based half-open Unicode code-point range wholly contained in the paragraph's already-returned `text_prefix`. The refined selection must retain the exact 17A selection object and derive selected text from that source rather than store a second copy of source text. Equal-by-value replacement of the selected paragraph is insufficient; the exact paragraph object retained by the supplied 17A source must remain present. A range may cover the complete returned prefix of truncated paragraph evidence but must not address, reacquire, expand, search for, or synthesize unreturned characters merely because the complete character count says more text existed. Exact range selection records human choice only and adds no relevance, importance, truth, claim-support, quotation-verification, citation-stability, source-authenticity, provenance, temporal, or browser-control authority.**
