# Milestone 49C — bare relinked selections in in-memory working sets

Decision: **D248**  
Issue: **#220**

## Concrete researcher action

49A–49B establish a complete exact-range lifecycle:

```text
exact 18A selection
→ durable 49A sidecar
→ file-local verification
→ explicit 49B relinking to supplied source evidence
```

That creates a new useful application record:

```text
ChromiumPageResearchLoadedParagraphTextSelectionRecord
```

which represents one exact passage that has been saved and explicitly reattached to source evidence without requiring a per-selection note.

49C answers:

> Can a researcher carry those already-relinked bare passages forward together in the existing human-owned working-set action before deciding what each passage means?

49C answers **yes**, in memory only.

## Why reuse 20A

20A / D143 was deliberately defined as:

```text
caller chooses already-relinked research records
→ preserve exact order and duplicates
→ immutable human-owned working set
```

It does not claim semantic relation, relevance, priority, completeness, truth, support, or citation authority.

The original three supported families were simply the relinked research-record families available when 20A was implemented:

- 17D paragraph note;
- 18D exact-range note;
- 19D comparison note.

49B now establishes a fourth relinked research-record family.

Creating a parallel “selection collection” would repeat 20A's already-proven organizational mechanics solely because the new member has no note.

49C therefore extends the member family rather than duplicating the collection concept.

## External prior art

The W3C Web Annotation Data Model defines ordered Annotation Collections whose annotations can be collected independently of whether they carry textual bodies.

Hypothesis distinguishes private highlights from note-bearing annotations. A highlight anchors a selected passage without requiring comments or tags and remains available for later access.

Zotero likewise permits researchers to create highlights first, then later add one or multiple annotations to notes.

These systems demonstrate the workflow:

```text
select / highlight
→ organize / retain
→ interpret later
```

They do not replace Pyxis's explicit capture identity, durable sidecar, or fail-closed source-relinking boundaries.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse the established 20A working-set action rather than creating a parallel selection-set artifact.**

## In-memory member extension

49C extends:

```python
ChromiumPageResearchWorkingSetItem
```

to admit:

```python
ChromiumPageResearchLoadedParagraphTextSelectionRecord
```

alongside the original three families.

A 20A working set can therefore now contain any caller-chosen ordered mix of:

```text
17D paragraph note
49B bare exact-range selection
18D exact-range note
19D comparison note
```

The working-set mode does not change:

```text
caller_explicit_ordered_relinked_research_working_set
```

## Bare-selection coherence validation

20A still does not reread sidecar files.

For one 49B member, it checks the retained application graph only.

The validator requires the retained verification to be:

```python
ChromiumPageResearchParagraphTextSelectionVerificationEvidence
```

and re-establishes the current 18A selection through:

```python
select_chromium_research_paragraph_text(
    selection.source,
    start_offset=selection.start_offset,
    end_offset=selection.end_offset,
)
```

The reconstructed result must retain the exact existing 17A parent selection and the same:

- text selection mode;
- offset unit;
- start offset;
- end offset;
- derived selected text.

The retained 49A verification must also agree with the nested supplied-source graph on:

- capture format;
- capture bundle SHA-256;
- paragraph selection mode;
- paragraph ordinal;
- text selection mode;
- offset unit;
- start offset;
- end offset.

Digest comparison continues to use constant-time comparison.

## Exact object identity is retained

The working set stores the exact caller-supplied 49B loaded record object.

49C does not replace it with:

- the temporary rebuilt 18A validation result;
- a copied selection;
- a normalized member wrapper;
- a note-bearing substitute.

The organizational action therefore preserves the same exact-member identity rule established by 20A.

## Order and duplicates remain human-owned

A caller may supply:

```text
bare A
note B
bare A
comparison C
```

and the working set retains exactly:

```text
bare A
note B
bare A
comparison C
```

No sort, deduplication, ranking, or inferred relationship occurs.

## No hidden 49A sidecar reread

Once 49B has successfully relinked a selection, 49C relies on the retained verification and reconstructed source graph already held by that loaded record.

The 49A sidecar may be removed after successful 49B relinking and the record remains eligible for 20A membership.

This preserves the long-established Pyxis distinction:

```text
already-loaded application evidence
!=
fresh durable-file verification
```

## Raw 18A selections remain unsupported

49C does not allow a live raw:

```python
ChromiumPageResearchParagraphTextSelectionEvidence
```

to enter 20A directly.

The bare member must first cross 49A durability and 49B explicit relinking.

Thus:

```text
live exact range
!=
relinked durable research record
```

The new member family is the 49B loaded record, not every 18A object.

## The durable 20B v1 boundary remains closed

This is the central compatibility boundary of 49C.

49C does **not** alter:

```text
pyxis.chromium.research_working_set.v1
```

That format still supports only:

```text
paragraph_note
exact_range_note
comparison_note
```

Existing 20B persistence therefore re-establishes the expanded 20A working set, then rejects a bare-selection member when attempting to project it to the established v1 member-reference vocabulary.

No destination file is created.

This is intentional.

```text
20A in-memory membership extension
!=
20B durable schema extension
```

49C refuses to teach old v1 files/readers a new member kind under the same version identifier.

## Downstream durable product remains unchanged

Because 20B v1 remains closed, 49C does not silently widen:

- 20C working-set relinking;
- 21B durable working-set notes;
- durable rationale revision;
- 27C working-set presentation;
- Textual rationale rendering;
- 33A evidence-basis extension;
- restart/checkpoint products;
- changed-basis products.

Those durable/governed surfaces remain constrained by their existing file contracts.

## In-memory composition remains ordinary

A 49C working set is still an ordinary:

```python
ChromiumPageResearchWorkingSetRecord
```

so existing in-memory operations that genuinely depend only on 20A coherence may compose with it.

That does not grant those operations a new durable parent format.

Any later persistence boundary must still prove compatibility explicitly.

## Focused falsification

49C adds tests proving:

1. a 49B bare selection is accepted as a 20A member;
2. mixed bare and note-bearing membership preserves exact caller order;
3. duplicate bare-selection positions are retained;
4. the exact caller-supplied 49B loaded object is retained;
5. selected text remains derived from the loaded source evidence;
6. a deleted 49A sidecar is not reread during 20A creation;
7. a forged retained source digest rejects;
8. a forged retained coordinate rejects;
9. a raw 18A selection remains unsupported;
10. the original 17D/18D/19D tests remain unchanged;
11. existing 20B v1 persistence rejects a bare-selection working set before writing a file.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49C changes only:

- the public in-memory `ChromiumPageResearchWorkingSetItem` union;
- 20A's in-memory coherence dispatch and validation.

It changes no durable format, file reader, browser behavior, CLI, UI, governed session, or existing note/comparison semantics.

Existing three-family working sets remain behaviorally unchanged.

## Expected next boundary

If 49C succeeds, the next separate product question is:

> How should this expanded working-set membership become durable without silently changing `pyxis.chromium.research_working_set.v1`?

That requires an explicit versioning and compatibility review.

A likely candidate is a versioned working-set format that can read old v1 records while representing a new bare-selection member kind, but that decision is not pre-authorized.

The review must inspect impact on:

- 20B persistence and verification;
- 20C relinking;
- 21B durable note parent references;
- 27C presentation;
- Textual rendering;
- old-reader/new-writer compatibility.

## Non-goals

49C adds no:

- new selection-collection artifact;
- 20B format change;
- 20C change;
- working-set v2;
- durable bare-selection membership;
- presentation/UI change;
- rationale persistence change;
- CLI;
- source discovery;
- quote copying;
- fuzzy anchoring;
- ranking;
- semantic clustering;
- citation authority;
- claim-support authority;
- authorship/authenticity/trusted-time authority.

## Acceptance statement

49C permits only this statement:

> An already-relinked 49B bare exact-range selection may participate directly in the existing human-owned in-memory 20A working-set action with the same exact-order, duplicate, exact-object, and retained-coherence guarantees as established members. The existing durable v1 working-set and governed-session boundaries remain unchanged and fail closed rather than silently widening.
