# Milestone 20C — Verified Research Working-Set Relinking

## Product question

Can Pyxis take one durable 20B working-set sidecar and re-establish its exact ordered membership against caller-supplied already-loaded research records, without searching for members, rereading their individual sidecars, reordering them, or inferring why they belong together?

20C answers **yes**.

## Why this milestone exists

20A created an in-memory human-owned working set:

```text
loaded member A
loaded member B
loaded member A
      ↓
explicit caller membership + order
      ↓
20A working set
```

20B then made that organizational action durable using only member identities:

```text
member kind
member sidecar format
member record SHA-256
```

But 20B intentionally could not prove that those persisted member identities matched any particular loaded research records.

Its principal falsifiability proof demonstrated that a working-set file can remain internally valid after a member digest is replaced with another structurally valid digest and the outer working-set digest is recomputed.

20C adds the missing authority boundary:

```text
20B sidecar path
      ↓
fresh 20B verification
      ↓
caller-supplied complete ordered loaded-member sequence
      ↓
20A in-memory coherence re-established
      ↓
position-by-position durable identity match
      ↓
new loaded working-set record
```

## Public module API

```python
load_chromium_research_working_set(
    items,
    working_set_source,
)
```

returns:

```python
ChromiumPageResearchLoadedWorkingSetRecord(
    verification=<fresh 20B verification>,
    working_set=<new 20A working set over exact supplied members>,
)
```

Mismatch failures use:

```python
ChromiumResearchWorkingSetMemberMismatchError
```

The API is exposed through:

```python
pyxis.app.chromium_research_working_set_load
```

20C does not broaden the `pyxis.app` root re-export surface.

## The caller supplies the complete member sequence

20C performs no member discovery.

The caller must explicitly provide every loaded member expected to occupy the durable working set, in the exact intended order.

Pyxis does not search by:

- member record SHA-256;
- member sidecar path;
- source capture digest;
- URL;
- paragraph ordinal;
- selected text;
- human note text;
- note type similarity;
- semantic similarity;
- temporal proximity.

This preserves agency and keeps digest equality from becoming a hidden search mechanism.

## Order remains part of the human organizational action

If the durable working set records:

```text
A, B, A
```

then the supplied sequence must match:

```text
A, B, A
```

Supplying:

```text
B, A, A
```

fails even when it contains the same loaded objects.

20C does not sort, normalize, auto-swap, or deduplicate.

Thus:

```text
same multiset of members
≠
same human organizational action
```

and:

```text
member order
=
recorded organizational provenance
```

Order still does not imply importance, causal direction, or semantic priority.

## The working-set sidecar is always freshly verified

`load_chromium_research_working_set(...)` accepts a sidecar path, not a prebuilt 20B verification object.

It always calls:

```python
verify_chromium_research_working_set(...)
```

before relinking.

This preserves the established distinction between caller-supplied location and verified durable file evidence.

The working-set sidecar may be moved to another filesystem path before 20C loading because path is location, not durable content identity.

## 20A remains the owner of in-memory member coherence

20C does not reproduce the 17B/18B/19B validation chains.

After fresh 20B sidecar verification and member-count agreement, it calls:

```python
create_chromium_research_working_set(supplied_items)
```

That public 20A boundary re-establishes the supported members' existing in-memory coherence.

Therefore 20C inherits the rule that an outer loaded-record type is not enough. A supplied member whose retained verification facts no longer agree with its nested reconstructed note/source graph is rejected before durable member identity can be accepted.

## Durable member identity is matched position by position

For each verified 20B member reference and the supplied loaded record occupying the same position, 20C compares exactly:

```text
member kind
member sidecar format
member record SHA-256
```

The supported mappings remain the explicit 20A/20B families:

```text
paragraph_note
  → pyxis.chromium.research_paragraph_note.v1

exact_range_note
  → pyxis.chromium.research_paragraph_text_selection_note.v1

comparison_note
  → pyxis.chromium.research_paragraph_text_selection_comparison_note.v1
```

SHA-256 comparison is used only as the durable member-record identity already established by the individual member sidecar layers.

It does not authenticate the member or its source.

## Exact supplied loaded members are retained

20C does not reconstruct the individual 17D/18D/19D member records from their sidecars.

Instead, after successful identity matching, it returns a newly created 20A working set whose tuple contains the exact caller-supplied loaded member objects.

Thus:

```text
persisted runtime object identity
≠
durable identity
```

but:

```text
successful 20C relinking
→ new 20A working-set object
→ exact supplied loaded members retained within it
```

The original pre-persistence 20A working-set object is not claimed to survive disk.

## Individual member sidecars are not reread

20C operates on already-loaded member records.

It does not call the 17D, 18D, or 19D loaders again and does not reread the member paths retained by those records.

A researcher may therefore:

1. successfully relink individual members earlier;
2. create and persist a 20A/20B working set;
3. lose or move the individual member sidecar files;
4. still use those already-loaded member records to relink the 20B working-set sidecar during the current application lifetime.

This proves:

```text
working-set member identity coherence
≠
fresh member-sidecar verification
```

and:

```text
current member-file availability
≠
already-loaded member evidence
```

20C does not claim that a missing member sidecar can later be recovered.

## Falsifiability proof: the 20B-valid wrong digest fails here

20B intentionally permits the following file-local state:

```text
persisted member digest changed to valid 64-hex value
      ↓
working-set record SHA-256 recomputed
      ↓
canonical JSON rewritten
      ↓
20B verification succeeds
```

20C then receives the actual caller-supplied loaded member.

Its retained member sidecar record SHA-256 does not equal the falsified persisted reference.

Therefore 20C fails with:

```text
ChromiumResearchWorkingSetMemberMismatchError
```

This is the principal 20C authority proof.

It demonstrates:

```text
20B file integrity
≠
member identity correctness
```

while:

```text
20C successful positional match
=
verified durable member identity coherence
relative to the supplied loaded records
```

## Member count is exact

A durable working set with two members cannot be relinked against one supplied member or three supplied members.

20C rejects missing or extra supplied members before creating the final loaded working-set record.

This prevents partial relinking from being silently represented as the original human-owned grouping.

## What successful 20C loading proves

Successful 20C loading proves only that:

1. the caller supplied a working-set sidecar path whose bytes freshly satisfy 20B canonical structure and self-integrity;
2. the caller supplied exactly as many already-loaded research records as the sidecar contains member references;
3. those supplied records pass the established 20A in-memory coherence boundary;
4. each supplied record's explicit member family, retained sidecar format, and retained sidecar record SHA-256 match the durable reference in the same position;
5. the resulting new 20A working-set record preserves the exact supplied loaded objects, order, and duplicates.

This is **ordered durable working-set membership coherence relative to caller-supplied loaded records**.

## What successful 20C loading does not prove

20C does **not** prove:

- that any individual member sidecar currently exists;
- that any member sidecar would freshly verify now;
- that any member source is authentic, reliable, or true;
- that a human note is correct;
- that the working-set members are topically or semantically related;
- that member order represents importance or priority;
- that duplicates are meaningful;
- that the working set is complete or representative;
- quotation or citation validity;
- claim support, contradiction, corroboration, or entailment;
- authorship or trusted time;
- chain of custody;
- machine agreement;
- browser freshness or current page state.

Relinking restores an organizational reference relationship. It does not upgrade semantic or evidentiary authority.

## Focused tests

Eight focused tests cover:

1. successful mixed-family relinking after moving the working-set sidecar, with exact supplied object identity and order retained in the new 20A record;
2. intentional duplicate-member positions preserved;
3. successful relinking after all individual member sidecar files are deleted, proving no hidden member-file reread;
4. rejection of the same supplied member objects in a different order;
5. rejection of the recomputed, 20B-valid wrong member digest against the actual supplied loaded member;
6. rejection of missing or extra supplied members;
7. delegation to 20A for in-memory loaded-record coherence rejection;
8. public importability through the explicit 20C module.

## Explicit non-goals

20C adds no:

- member discovery;
- digest-based member search;
- automatic member-file lookup;
- fresh 17D/18D/19D member relinking;
- notebook database;
- title, folder, label, tag, or taxonomy system;
- search or filtering;
- sorting, ranking, or deduplication;
- semantic clustering;
- similarity scoring;
- contradiction, corroboration, entailment, or claim-support detection;
- source authentication;
- quotation or citation verification;
- authorship or trusted timestamps;
- revision history;
- embeddings or LLM interpretation;
- browser acquisition, navigation, or control;
- researcher UI.

## Decision — D145

**Pyxis may load one durable 20B research working-set sidecar only by freshly verifying the caller-supplied working-set path and matching its complete ordered member-reference sequence against a complete caller-supplied ordered sequence of already-loaded 17D paragraph-note, 18D exact-range-note, or 19D comparison-note records. The supplied sequence must first pass the established public 20A in-memory coherence boundary, after which each position must match the verified sidecar's explicit member kind, established member-sidecar format, and member sidecar record SHA-256. Pyxis must not discover members, search by digest, reorder, auto-swap, deduplicate, reread individual member sidecars, or treat path location as durable identity. The returned loaded working-set record may contain a newly reconstructed 20A working set retaining the exact caller-supplied loaded member objects and fresh 20B verification evidence. A recomputed canonical 20B sidecar containing a structurally valid but wrong member digest must continue to pass 20B verification and must fail 20C relinking against the actual supplied loaded member. Successful 20C loading proves only ordered durable working-set membership coherence relative to those supplied loaded records; it does not establish fresh member-file availability or verification, semantic relationship, priority, completeness, source authenticity, reliability, truth, note correctness, quotation/citation validity, authorship, trusted time, chain of custody, or machine agreement. Working-set file integrity, member identity coherence, individual member freshness, human organizational membership, and semantic relationship remain separate authority layers.**
