# Milestone 20A — Human-Owned Research Working Set

## Product question

Can a researcher explicitly carry forward several already-relinked Pyxis research records together, in a chosen order, without Pyxis inferring that the records are semantically related, deduplicating them, ranking them, or rereading their sidecar files?

20A answers **yes**.

## Why this milestone exists

Milestones 17D, 18D, and 19D can each reopen one durable human research action into typed application evidence:

```text
17D  relinked paragraph note
18D  relinked exact-range note
19D  relinked comparison note
```

Those records are individually useful, but Pyxis had no bounded way for the researcher to say:

```text
"carry these pieces forward together"
```

without immediately introducing a notebook database, tags, search, ranking, or semantic grouping.

20A adds only that explicit organizational action:

```text
relinked record A
relinked record B
relinked record C
        ↓
caller chooses membership + order
        ↓
immutable research working set
```

The working set is human-owned organization over existing evidence. It is not new source evidence and it is not an inferred relationship among the members.

## Public API

```python
create_chromium_research_working_set(items)
```

returns:

```python
ChromiumPageResearchWorkingSetRecord(
    working_set_mode="caller_explicit_ordered_relinked_research_working_set",
    items=(...),
)
```

The public item type is:

```python
ChromiumPageResearchWorkingSetItem
```

and currently admits exactly three established loaded-record families:

- `ChromiumPageResearchLoadedParagraphNoteRecord` from 17D;
- `ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord` from 18D;
- `ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord` from 19D.

20A does not accept raw captures, raw paragraph selections, raw exact ranges, 17B/18B/19B live notes, arbitrary objects, or a generic annotation protocol.

## Membership is explicit, ordered, and non-empty

The caller supplies the records to carry forward.

Pyxis does not discover members from:

- source digest;
- source path;
- URL;
- page title;
- selected text;
- note text;
- semantic similarity;
- shared capture identity;
- temporal proximity.

At least one item is required.

The supplied iterable is snapshotted into an immutable tuple. Therefore later mutation of a caller-owned list cannot silently change the working set.

## Order belongs to the researcher

20A preserves exact caller order.

If the caller supplies:

```text
B, A, C
```

the working set remains:

```text
B, A, C
```

Pyxis does not sort by source, note type, digest, URL, creation path, text, or any inferred importance.

Order is provenance of the researcher's organizational action, not evidence that the first item is more important than later items.

## Duplicates remain duplicates

20A deliberately permits the same exact loaded record object to appear more than once.

For example:

```text
A, A
```

remains:

```text
A, A
```

Pyxis does not infer that repetition is accidental, redundant, or meaningless.

Thus:

```text
value repetition
≠
authority to deduplicate
```

## Exact supplied member identity is retained

The working-set tuple contains the exact loaded record objects supplied by the caller.

20A does not rebuild those objects into normalized copies or collapse the three existing record families into one generic representation.

The only new object is the immutable tuple that freezes membership and order.

## In-memory coherence is re-established without sidecar rereads

20A is downstream of successful relinking.

It does not call the 17D, 18D, or 19D loader again and does not reread any sidecar path.

Instead, each supported member has its current in-memory relationships re-established through the already-owned public human-action boundaries:

```text
17D loaded paragraph note
    ↓
17B note constructor

18D loaded exact-range note
    ↓
18B note constructor
    ↓
18A range validation through the existing chain

19D loaded comparison note
    ↓
19B note constructor
    ↓
19A comparison validation
    ↓
18A validation on both ranges
```

20A then checks that the loaded record's retained verification facts agree with the nested source/selection/note objects already present in memory.

For the relevant record family this includes the established fields such as:

- source capture format and bundle SHA-256;
- paragraph ordinal and selection mode;
- Unicode exact-range mode/unit/start/end coordinates;
- comparison mode and ordered first/second source references;
- note mode and verbatim note text.

No new lower-level selection or comparison validator is introduced.

## Sidecar availability is not required after successful relinking

A central 20A proof is that a successfully loaded 17D, 18D, or 19D record remains eligible for a working set even if its sidecar file is subsequently absent from the filesystem.

This is intentional.

The loaded application record already contains the verification evidence that authorized its earlier relinking plus the reconstructed human-action graph.

20A groups that existing application evidence. It does not claim to freshly verify the file.

Therefore:

```text
current sidecar availability
≠
already-loaded application evidence
```

and:

```text
20A in-memory coherence check
≠
17D/18D/19D fresh relinking
```

If a caller needs fresh file verification and source relinking, the established loader boundary remains the authority for that operation.

## Falsifiability proof: loaded type alone is not enough

20A does not accept a supported dataclass merely because its outer Python type matches.

For example, if an exact-range loaded record is copied with a verification object whose retained `note_text` no longer matches the nested 18B note, working-set creation fails.

Likewise, if a loaded comparison note's retained first source bundle SHA-256 no longer matches the first reconstructed comparison selection's source capture identity, working-set creation fails.

This proves that 20A is not just a heterogeneous tuple wrapper.

It requires the supported in-memory loaded record to remain coherent with the evidence graph it claims to contain.

## What successful working-set creation proves

Successful 20A creation proves only that:

1. the caller supplied a non-empty ordered iterable;
2. every member is one of the three explicitly supported loaded research-record families;
3. each member's established in-memory human-action contract can be re-established through existing public constructors;
4. each member's retained verification facts agree with its nested reconstructed source/selection/note objects;
5. the resulting immutable tuple preserves the caller's membership order and duplicate choices.

It proves an explicit **human-owned working-set membership record** over coherent loaded application evidence.

## What successful creation does not prove

20A does **not** prove:

- that the members are topically related;
- that the members support or contradict one another;
- that any member is relevant, important, representative, or complete;
- that duplicates are meaningful;
- that order represents priority;
- that any source is authentic, reliable, or true;
- that any human note is correct;
- that any citation or quotation is valid;
- that the original sidecar files still exist or remain unchanged;
- that fresh relinking would succeed now;
- authorship, trusted time, or chain of custody;
- machine agreement or interpretation.

Working-set membership is researcher provenance, not semantic authority.

## Focused tests

Seven focused tests cover:

1. mixed 17D/18D/19D membership with exact supplied object identity and caller order preserved;
2. caller-sequence snapshotting plus deliberate duplicate-member preservation;
3. successful working-set creation after the three already-loaded sidecar files are deleted, proving no hidden reread;
4. rejection of an in-memory exact-range verification/note mismatch;
5. rejection of an in-memory comparison source-reference mismatch;
6. rejection of empty sets and non-relinked live note records;
7. public `pyxis.app` exposure.

## Explicit non-goals

20A adds no:

- working-set persistence;
- working-set relinking;
- notebook database;
- collection discovery;
- automatic source discovery;
- title, label, tag, folder, or taxonomy system;
- search or filtering;
- sorting or ranking;
- deduplication;
- source or note mutation;
- note revision history;
- semantic clustering;
- similarity scoring;
- contradiction, entailment, corroboration, or claim-support detection;
- quotation/citation verification;
- source authentication;
- authorship or trusted timestamps;
- embeddings or LLM work;
- browser acquisition, navigation, or control;
- researcher UI.

## Decision — D143

**Pyxis may create one immutable human-owned research working set from a non-empty caller-supplied ordered iterable containing only the established 17D relinked paragraph-note, 18D relinked exact-range-note, and 19D relinked comparison-note record families. The working set must snapshot caller membership into an immutable tuple while retaining each exact supplied loaded record object, preserving caller order and intentional duplicates without sorting, ranking, discovery, deduplication, or semantic inference. Membership validation must re-establish each member's in-memory human-action contract through the existing public 17B, 18B, or 19B constructor chain and require the retained verification facts to agree with the nested reconstructed source/selection/note objects, but it must not reread sidecar files or pretend to perform fresh 17D/18D/19D relinking. A previously relinked record may therefore remain eligible even when its sidecar path no longer exists, while an in-memory verification/note or verification/source mismatch must be rejected. Successful creation proves only explicit working-set membership over coherent loaded application evidence; it does not establish semantic relation, relevance, priority, completeness, source authenticity, reliability, truth, note correctness, quotation/citation validity, authorship, trusted time, chain of custody, or machine agreement. Loaded evidence, human organizational membership, and semantic relationship remain separate authority layers.**
