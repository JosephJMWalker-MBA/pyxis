# Milestone 17A — Human-Owned Verified-Capture Passage Selection

## Product question

Can a researcher explicitly select one already-observed paragraph from verified rehydrated Chromium research evidence without Pyxis ranking passages, reacquiring browser state, copying the text into a stronger semantic object, or turning the human choice into a relevance/citation/truth claim?

17A answers **yes** through one narrow application-level selection boundary.

## Why this milestone exists

Milestones 15A–15G established literal read-only browser evidence. 16A composed those evidence families without inventing atomic browser state. 16B made the completed bundle durable. 16C allowed a verified durable capture to re-enter the typed application layer while retaining its file-verification origin.

The next concrete research action is not another observer or storage primitive. It is a human choosing one already-available piece of evidence for attention.

That choice must remain visibly human/caller-owned.

## Boundary

```text
ChromiumPageResearchLoadedCaptureEvidence
    ↓
caller supplies exact 1-based paragraph ordinal
    ↓
validate selection-relevant capture/bundle/paragraph coherence
    ↓
require the paragraph to be inside the already-returned bounded prefix
    ↓
retain exact loaded-capture object
+ retain exact paragraph object
    ↓
frozen ChromiumPageResearchParagraphSelectionEvidence
```

Public API:

```python
select_chromium_research_capture_paragraph(
    source,
    paragraph_ordinal=...
)
```

Result:

```python
ChromiumPageResearchParagraphSelectionEvidence(
    selection_mode="caller_explicit_returned_paragraph_ordinal",
    source=<exact ChromiumPageResearchLoadedCaptureEvidence>,
    paragraph=<exact ChromiumPageParagraphEvidence>,
)
```

## Human ownership

The operation never chooses a paragraph for the caller.

The caller supplies one exact 1-based DOM paragraph ordinal. Pyxis does not:

- rank passages;
- infer importance;
- infer relevance;
- infer support or contradiction;
- choose by authored element ID;
- choose by text similarity;
- choose by heading/section context;
- ask an LLM which paragraph matters.

The resulting `selection_mode` records only that the caller explicitly chose one returned paragraph ordinal.

## Exact evidence identity

17A does not copy selected text into a new quote, excerpt, citation, claim, or normalized passage representation.

The result retains:

- the **exact supplied 16C loaded-capture object** under `source`;
- the **exact already-returned paragraph object** under `paragraph`.

This preserves the upstream acquisition origin and avoids creating another source of truth.

Duplicate authored IDs therefore cannot redirect selection. Two paragraphs may both carry `id="passage"`; ordinal 1 and ordinal 2 remain distinct exact evidence objects.

## Bounded evidence remains bounded

A paragraph collection may report that more paragraphs existed than were returned because the observation was bounded.

If the caller requests an ordinal that is known to exist according to `paragraph_count` but lies outside the returned tuple, 17A refuses the selection.

It does **not**:

- reconnect to Chromium;
- issue another paragraph observation;
- reread the capture file;
- enlarge a prior collection limit;
- synthesize the missing paragraph;
- infer its text from page-level content.

The caller may only select evidence that is already present in the supplied source object.

## Upstream authority remains upstream

17A consumes `ChromiumPageResearchLoadedCaptureEvidence`, the type emitted by the 16C loader.

It does not reopen the capture JSON or rerun the SHA-256 verifier. Selection performs only the coherence checks needed for its own boundary, including:

- supported capture format;
- verification/bundle endpoint, target ID, URL, acquisition mode, and acquisition-order agreement;
- paragraph member endpoint/target/URL coherence;
- established paragraph selector identity;
- paragraph collection count/limit/truncation consistency;
- contiguous returned paragraph ordinals;
- selected paragraph text count/limit/truncation consistency.

This preserves layer ownership: 16B owns durable-file verification, 16C owns full typed rehydration, and 17A owns explicit selection from the already-loaded result.

## Selection is not epistemic promotion

A caller choosing a paragraph means only that the caller chose it.

Selection does not prove:

- relevance;
- importance;
- factual correctness;
- source truth;
- source authenticity;
- quotation validity;
- citation validity;
- citation completeness;
- stable locator identity;
- semantic passage boundaries beyond the existing literal `<p>` evidence;
- support for a claim;
- contradiction of a claim;
- atomic page state;
- browser-control authority.

The selected paragraph retains every limitation it had before selection, including text and collection truncation facts.

## Tests

Focused tests prove:

1. selection returns a frozen record containing the exact source object and exact selected paragraph object;
2. duplicate authored element IDs do not affect exact ordinal selection;
3. an ordinal known only through truncated collection count is refused rather than reacquired;
4. boolean, zero, and out-of-range ordinals are rejected;
5. verification/bundle origin incoherence is rejected;
6. the real public durable chain works as `persist bundle → load capture → select paragraph`, with selection retaining the exact loaded result and exact paragraph object.

## Validation

Implementation/public API proof:

- Actions #556 on `32397e95c22693502004c2228617e03c8ead22f1`: Python 3.11, 3.12, 3.13, and 3.14 all passed;
- inspected Python 3.11 log: **273 collected / 273 passed**, including five focused 17A tests.

Durable-chain composition proof:

- Actions #557 on `9f53a1e38d55624b15f0be3eee7ba7dc0dee06f5`: Python 3.11, 3.12, 3.13, and 3.14 all passed;
- inspected Python 3.11 log: **274 collected / 274 passed in 32.46s**;
- the six 17A tests include the public `persist → load → select` path.

## Explicit non-goals

17A adds no:

- browser acquisition or control;
- navigation, scrolling, activation, clicking, or form submission;
- capture-file read or verification during selection;
- persistence of the selection itself;
- automatic passage recommendation;
- ranking, scoring, search, or relevance inference;
- semantic passage extraction or sentence splitting;
- cross-family semantic joins;
- quotation verification;
- citation formatting or locator stability;
- source verification or provenance authentication;
- claim/argument modeling;
- annotation, note, question, tag, or rationale system;
- multi-selection or selection-set abstraction;
- generic selection registry across evidence families;
- LLM interpretation;
- autonomous research workflow;
- researcher UI.

## Decision — D131

**An explicit caller may select one already-returned paragraph from verified rehydrated Chromium research evidence by exact ordinal, producing a frozen selection that retains the exact loaded-capture evidence object and exact paragraph evidence object. Selection records caller choice only: it does not imply relevance, importance, truth, quotation validity, citation authority, locator stability, source authenticity, or browser-control authority. Evidence outside the bounded returned paragraph prefix must not be reacquired, expanded, or synthesized as a side effect of selection.**
