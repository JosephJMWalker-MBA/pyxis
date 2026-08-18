# Milestone 19A — Human-Owned Exact-Range Comparison

## Product question

Can a researcher explicitly place two already-valid 18A exact paragraph-text selections together for examination—including selections from two different durable captures—without Pyxis deciding why they belong together or claiming any semantic relationship between them?

19A answers **yes** through one narrow human-owned comparison boundary.

## Why this milestone exists

18A through 18D complete one exact-range annotation cycle:

```text
exact returned paragraph range
    ↓
human-authored note
    ↓
durable range-note sidecar
    ↓
explicit verified relinking
```

That cycle remains source-local. A researcher can point precisely, interpret precisely, persist that human action, and later re-establish attachment coherence, but Pyxis still has no application-level representation for the simpler cross-source act:

```text
"I choose to examine these two exact pieces of evidence together."
```

19A records that act without promoting juxtaposition into interpretation.

## Public API

```python
create_chromium_research_paragraph_text_selection_comparison(
    first_selection,
    second_selection,
)
```

returns:

```python
ChromiumPageResearchParagraphTextSelectionComparisonRecord(
    comparison_mode="caller_explicit_exact_text_range_comparison",
    first_selection=<exact caller-supplied 18A object>,
    second_selection=<exact caller-supplied 18A object>,
)
```

The returned record is frozen and retains both supplied 18A selection objects by exact Python object identity.

## Range validity remains owned by 18A

19A does not create another paragraph/range/source validator.

For each supplied selection it requires the established:

```text
selection_mode = caller_explicit_returned_paragraph_text_range
offset_unit = unicode_code_point
```

and then delegates validation back through:

```python
select_chromium_research_paragraph_text(
    selection.source,
    start_offset=selection.start_offset,
    end_offset=selection.end_offset,
)
```

That re-establishes the existing 17A parent identity, exact source-owned paragraph identity, integer coordinate shape, non-empty half-open range, Unicode code-point unit, and bounded returned-prefix relationship.

The validation result is deliberately discarded. 19A retains the exact caller-supplied 18A object rather than replacing it with a newly-created equal-by-value range.

## Cross-capture comparison is allowed

The two selections may come from:

- the same paragraph;
- different paragraphs in one loaded capture;
- different loaded captures with different durable bundle identities;
- the same exact selection object supplied twice.

19A adds no same-source requirement.

A focused positive proof uses two distinct `ChromiumPageResearchLoadedCaptureEvidence` objects whose retained 16B verification evidence contains different bundle SHA-256 identities. Their exact 18A ranges can still enter one comparison record.

This is the first Pyxis researcher action that can deliberately place exact evidence from two durable source captures into one typed application record.

## Same-selection pairing remains permitted

19A does not reject:

```text
first_selection is second_selection
```

because doing so would introduce a judgment that a self-comparison is meaningless or invalid research behavior.

The comparison boundary records human juxtaposition. It does not decide whether the juxtaposition is useful.

## Tampered selection objects are revalidated

A caller-created 18A-shaped dataclass is not trusted merely because its fields have the expected names.

If a supplied selection retains a 17A parent whose paragraph has been replaced with an equal-by-value but non-source-owned object, the existing 18A identity check rejects it.

Likewise, replacing an otherwise-valid range coordinate with an out-of-bounds value such as:

```text
end_offset = 999
```

is rejected through 18A bounded-range validation.

Therefore:

```text
18A-shaped value
≠
currently valid 18A source relationship
```

and 19A inherits that distinction rather than weakening it.

## What successful comparison creation proves

Successful 19A creation proves only that:

1. the caller explicitly supplied two 18A-shaped selections;
2. each selection uses the established exact-range mode and Unicode offset unit;
3. each selection can be re-established through the existing 18A public boundary against its retained parent/source evidence;
4. Pyxis retained those exact two supplied selection objects in one immutable comparison record.

That is **human-owned juxtaposition**.

It is not evidence that:

- the ranges are similar;
- the ranges are different;
- one contradicts the other;
- one corroborates the other;
- one supports a claim made by the other;
- either is relevant to a research question;
- either source is more reliable;
- either source is authentic;
- either source is true;
- the pairing is useful;
- a quotation or citation is verified;
- any semantic relationship exists between the two ranges.

## Epistemic separation

19A establishes the next explicit distinction:

```text
source evidence
≠
human selection
≠
human juxtaposition
≠
human interpretation
```

The comparison record says who supplied the pairing decision: the caller.

It does not silently convert that decision into a machine conclusion.

## Focused tests

Seven focused tests cover:

1. exact retention of two 18A selections from distinct loaded captures with distinct bundle SHA-256 identities;
2. two ranges from the same paragraph;
3. the same exact selection object supplied on both sides without significance judgment;
4. rejection of non-18A input types;
5. rejection of unsupported range mode or offset unit;
6. reuse of 18A exact-parent identity and bounded-coordinate validation, including equal-by-value paragraph substitution and `end_offset=999` tampering;
7. exposure through the public `pyxis.app` surface.

## Validation

Milestone acceptance requires the complete established Repository Zero/browser/capture/selection/note/durability/relinking suite plus the seven focused 19A tests to pass on every supported Python lane (3.11–3.14) at the final frozen review head.

## Explicit non-goals

19A adds no:

- comparison note or prose interpretation;
- persistence or comparison sidecar;
- comparison relinking;
- automatic source discovery;
- browser acquisition, navigation, or control;
- capture-file read;
- text search or fuzzy matching;
- embedding generation;
- similarity or distance score;
- contradiction or entailment detection;
- corroboration judgment;
- source ranking;
- relevance/confidence scoring;
- claim or support model;
- quotation/citation verification;
- source authentication;
- trusted timestamp or author identity;
- notebook, collection, or generic annotation framework;
- LLM interpretation or generated comparison;
- researcher UI.

## Decision — D139

**Pyxis may record one explicit caller-owned comparison only by retaining two exact caller-supplied 18A paragraph-text selection objects after independently re-establishing each selection through the existing public 18A range-selection boundary. The two selections may originate from the same paragraph, different paragraphs, different verified loaded captures with different durable content identities, or be the same exact selection object supplied twice; 19A must not impose a same-source or significance requirement. Successful creation proves human-owned juxtaposition only. It does not establish similarity, difference, contradiction, corroboration, support, relevance, reliability, authenticity, truth, quotation/citation validity, or any other semantic relationship. 19A performs no browser acquisition, capture reread, persistence, source discovery, automated comparison, claim modeling, or machine interpretation. Source evidence, human selection, human juxtaposition, and human interpretation remain separate authority layers.**
