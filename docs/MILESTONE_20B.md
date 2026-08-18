# Milestone 20B — Durable Research Working Set

## Product question

Can Pyxis make one already-created 20A human-owned research working set durable while preserving exact caller order and duplicates, without copying the members' source evidence or human notes and without rereading the individual member sidecars?

20B answers **yes**.

## Why this milestone exists

20A lets the researcher say:

```text
"carry these already-relinked pieces forward together"
```

but the resulting working set is only an in-memory application record.

20B adds the next narrow durability boundary:

```text
20A working set
      ↓
re-establish 20A in-memory coherence
      ↓
project each member to durable member identity only
      ↓
canonical ordered working-set record
      ↓
SHA-256 self-integrity
      ↓
exclusive-create working-set sidecar
```

The new sidecar persists the researcher's organizational choice. It does not create a notebook database, discover members, reopen source captures, or strengthen the evidence represented by any member.

## Durable member identity is intentionally minimal

Each working-set entry stores exactly:

```text
member kind
member sidecar format
member sidecar record SHA-256
```

For example:

```json
{
  "member_kind": "exact_range_note",
  "member_format": "pyxis.chromium.research_paragraph_text_selection_note.v1",
  "member_record_sha256": "..."
}
```

20B deliberately does **not** copy into the working-set file:

- selected source text;
- paragraph ordinals;
- exact-range coordinates;
- source capture format or bundle SHA-256;
- comparison coordinates;
- human note text;
- browser URLs or target IDs;
- source-capture paths;
- member-sidecar paths;
- loaded application object graphs.

The individual member sidecars already own those durable representations.

Thus:

```text
working-set durability
≠
second serialization of member evidence
```

## Supported member families remain explicit

20B inherits exactly the three member families established by 20A:

1. 17D relinked paragraph note;
2. 18D relinked exact-range note;
3. 19D relinked comparison note.

Their durable identities map to:

```text
paragraph_note
  → pyxis.chromium.research_paragraph_note.v1

exact_range_note
  → pyxis.chromium.research_paragraph_text_selection_note.v1

comparison_note
  → pyxis.chromium.research_paragraph_text_selection_comparison_note.v1
```

20B does not introduce a generic annotation protocol or an open-ended member registry.

## Public module API

```python
persist_chromium_research_working_set(
    working_set,
    destination,
)
```

returns:

```python
ChromiumPageResearchWorkingSetPersistenceEvidence(
    path=...,
    working_set_format="pyxis.chromium.research_working_set.v1",
    working_set_record_sha256=...,
    byte_count=...,
    working_set=<exact supplied 20A object>,
)
```

and:

```python
verify_chromium_research_working_set(source)
```

returns file-local verification evidence containing the explicit working-set mode and an ordered tuple of `ChromiumPageResearchWorkingSetMemberReference` values.

The 20B API is exposed through the package module:

```python
pyxis.app.chromium_research_working_set_persistence
```

20B does not broaden `pyxis.app` root re-exports as part of this milestone.

## Order and duplicates survive persistence

20A established that order and duplicate membership belong to the researcher.

20B preserves that exact sequence mechanically.

If the working set is:

```text
comparison C
paragraph A
comparison C
```

the durable record remains:

```text
comparison C
paragraph A
comparison C
```

No sorting or deduplication occurs.

The working-set file therefore records organizational provenance, not priority or semantic structure.

## Persistence reuses 20A rather than creating a second validator

Before serialization, 20B calls the established 20A constructor over the supplied working-set items.

This re-establishes the member families' existing in-memory coherence through the already-owned 17B/18B/19B chains.

20B then checks only the additional durable identity facts that it needs to serialize:

- each member's retained sidecar format must match its explicit member family;
- each retained member record SHA-256 must have the established lowercase 64-hex shape.

20B does not reproduce the 17D/18D/19D relinking logic.

## Member files are not reread

20B deliberately does not reopen any individual member sidecar.

A researcher may therefore:

1. successfully relink member records through 17D, 18D, or 19D;
2. create a 20A working set;
3. lose or move the individual sidecar files;
4. still persist the working set using the durable member identities retained by those loaded application records.

This means:

```text
current member-sidecar availability
≠
retained durable member identity
```

and:

```text
20B persistence
≠
fresh member-file verification
```

This is not a claim that the missing member file can later be recovered or relinked.

## Deterministic no-overwrite canonical JSON

20B follows the established durability pattern:

- UTF-8 JSON;
- sorted object keys;
- compact separators;
- no NaN values;
- exactly one trailing newline;
- SHA-256 over the canonical `working_set_record` bytes;
- exclusive-create destination semantics.

A second write to the same path fails rather than silently replacing the first working-set artifact.

The SHA-256 is self-integrity evidence only.

It is not authentication, authorship, trusted time, chain of custody, provenance verification, or evidence that the referenced members are available.

## File verification remains file-local

`verify_chromium_research_working_set(...)` reads only the working-set sidecar.

It validates:

- the exact top-level format;
- working-set mode;
- non-empty ordered member list;
- explicit supported member kind;
- exact member format corresponding to that kind;
- valid SHA-256 shape for every member identity;
- the working-set record digest;
- canonical file bytes.

It does not search for or read any referenced member sidecar.

It therefore cannot establish whether the persisted member identities identify the intended loaded research records.

## Falsifiability proof: self-consistent wrong member digest remains file-valid

The principal 20B authority test intentionally changes one persisted member reference so that:

```text
member_record_sha256 = ffffffffff...ffff
```

while preserving a valid 64-character lowercase hexadecimal shape.

The test then recomputes the working-set record SHA-256 and rewrites canonical JSON.

20B verification **must succeed**.

That behavior is intentional because the file is now internally self-consistent.

But nothing in 20B has supplied the referenced loaded member record with which to compare that digest.

Therefore:

```text
working-set file integrity
≠
member identity correctness
```

and:

```text
20B verification
≠
member relinking
```

A later explicit relinking boundary must earn the authority to compare persisted member identities against caller-supplied loaded records.

## What successful persistence proves

Successful 20B persistence proves only that:

1. the caller supplied one established 20A working-set record;
2. its current member graph passes the established 20A in-memory coherence boundary;
3. every member retains a supported durable member sidecar format and a structurally valid record SHA-256;
4. the researcher-selected working-set order and duplicates were serialized exactly;
5. a canonical no-overwrite working-set artifact was created whose recorded SHA-256 matches its working-set record.

It proves a durable representation of the human organizational action.

## What successful persistence or verification does not prove

20B does **not** prove:

- that any referenced member sidecar currently exists;
- that any referenced member sidecar remains unchanged;
- that a member can be freshly relinked;
- that a member digest identifies the intended loaded record;
- that the members are semantically related;
- that order represents importance;
- that duplicates are meaningful;
- that the set is complete or representative;
- source authenticity, reliability, or truth;
- human-note correctness;
- quotation/citation validity;
- authorship or trusted time;
- chain of custody;
- machine agreement.

Persistence preserves the organizational record. It does not upgrade its authority.

## Focused tests

Eight focused tests cover:

1. minimal ordered member-identity serialization with no copied human note/source fields;
2. order and duplicate preservation through verification;
3. successful persistence after individual member sidecars have been deleted;
4. rejection of an invalid retained member record SHA-256 before persistence;
5. rejection of a member-reference mutation when the working-set digest is not recomputed;
6. acceptance of a structurally valid wrong member digest after recomputing the working-set digest, proving file integrity is not member relinking;
7. exclusive-create no-overwrite behavior;
8. public importability through the explicit persistence module.

## Explicit non-goals

20B adds no:

- working-set relinking;
- member discovery;
- automatic member-file lookup by digest;
- notebook database;
- folder/tag/label taxonomy;
- search or filtering;
- sorting, ranking, or deduplication;
- semantic clustering;
- note/source mutation;
- revision history;
- claim modeling;
- source authentication;
- citation or quotation verification;
- embeddings or LLM interpretation;
- browser acquisition or control;
- researcher UI.

## Decision — D144

**Pyxis may persist one already-created 20A human-owned research working set as deterministic no-overwrite canonical JSON containing only the established working-set mode plus the exact ordered sequence of durable member identities, where each member identity consists solely of an explicit supported member kind, its corresponding established member-sidecar format, and the member sidecar's retained record SHA-256. Persistence must re-establish 20A in-memory coherence through the existing public boundary and validate the retained member format/digest shape, while never rereading member sidecars, copying their source/note representations, sorting, deduplicating, discovering, ranking, or interpreting members. Working-set verification remains file-local and may prove only canonical structure and SHA-256 self-integrity. A self-consistent file whose member digest has been replaced by another valid-looking digest must remain 20B-valid after the working-set digest is recomputed, because member identity correctness requires a separate future relinking boundary with caller-supplied member evidence. Working-set durability, member availability, member identity correctness, and semantic relationship remain separate authority layers.**
