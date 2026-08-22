# Milestone 28A — Complete Research Session Presentation

Decision: D167

## Product question

27D makes the verified rationale segment and explicitly supplied working-set contexts usable in the Textual shell.

But preparing that UI still requires caller ceremony:

```text
produce 27A sequence presentation
produce 27C context for position 1
produce 27C context for position 2
...
pass all of them separately
```

The next researcher-facing pressure is therefore not a new evidence claim. It is removal of repeated presentation orchestration.

28A answers:

```text
"I already loaded one coherent 26C declared segment.
Give me the complete read-only presentation surface for that segment in one call."
```

## Public boundary

28A adds the explicit-module API:

```python
present_chromium_research_session(loaded)
```

where `loaded` is one already-loaded coherent 26C declaration/sequence record.

The output is an immutable:

```text
ChromiumPageResearchSessionPresentation
```

containing exactly:

```text
presentation_mode
sequence
working_set_contexts
```

`sequence` is the existing complete 27A presentation.

`working_set_contexts` contains one existing complete 27C presentation for every declared position in the sequence, in declared order.

## No new evidence authority

28A deliberately creates no new source or research evidence type.

Its authority is only composition:

```text
verified 26C loaded evidence
→ existing 27A sequence presentation
→ existing 27C context presentation for each declared position
→ immutable complete session bundle
```

Thus:

```text
presentation aggregation
!=
new evidence authority
```

and:

```text
complete presentation bundle
!=
complete history
```

The bundle does not establish chronology, latest/current head, branch semantics, semantic support, source authenticity, citation authority, or Workspace provenance.

## Complete coverage

28A iterates the exact one-based positions produced by 27A.

For each member, it calls the existing 27C boundary with that exact declared position.

The returned context must reconcile to the 27A member by:

- durable declaration SHA-256;
- declared position;
- edge format;
- edge SHA-256;
- exact human rationale text.

Only after every position succeeds is the session record returned.

Therefore:

```text
partial presentation success
!=
complete research session
```

If a later position is invalid, the call fails rather than returning an incomplete session bundle.

## Human wording remains exact

28A does not rewrite text.

The sequence retains exact human-authored rationale wording from 27A.

Each context retains exact 27C fields including:

- segment-level human rationale text;
- exact member-level human notes;
- bounded paragraph prefixes;
- exact selected text ranges;
- two separately labeled comparison selections;
- capture content identity;
- observed URL;
- paragraph ordinal;
- truncation facts;
- Unicode code-point coordinates where applicable.

The established separation remains:

```text
bounded source evidence
!=
human note on source selection
!=
human rationale over working set
```

and:

```text
rationale attached to working set
!=
working set proves rationale
```

## No file reads

28A starts from already-loaded 26C evidence.

Both 27A and 27C are already in-memory presentation boundaries.

Therefore 28A performs no:

- declaration-file read;
- edge-file read;
- member-sidecar read;
- browser acquisition;
- file discovery.

After successful 26C loading, all related durable inputs may disappear and 28A can still produce the complete session presentation from retained coherent application evidence.

This does not mean fresh durable verification occurred.

## No UI yet

28A is an application-presentation aggregation boundary only.

It does not modify the Textual shell.

A later UI milestone can accept this one bundle instead of requiring callers to pass the sequence and every context separately.

Preserving this split keeps the direction:

```text
26C loaded evidence
→ 28A complete presentation bundle
→ future UI convenience boundary
```

rather than allowing UI code to reach into deep loaded research evidence.

## Falsifiability

Focused tests prove:

1. One call returns the complete two-member declared sequence and two ordered contexts.
2. The returned sequence equals the independently produced existing 27A presentation and the contexts equal independently produced existing 27C presentations.
3. Every context reconciles to the exact matching sequence member by declaration, position, edge identity, and exact rationale text.
4. Exact Unicode, whitespace, multiline rationale text, mixed working-set member kinds, human notes, and bounded source excerpts survive unchanged.
5. Wrong input type rejects.
6. A forged retained declaration is rejected through the reused 27A coherence boundary before a session is returned.
7. A forged later working-set state rejects the whole session instead of yielding partial success.
8. Session presentation still succeeds after all durable inputs are deleted following successful 26C loading.
9. The session record is frozen and contains no path, timestamp, latest, current-head, truth, support, citation, source-authenticity, or Workspace field.
10. The explicit module is importable without broadening the package-root export surface.

## What successful 28A proves

Successful 28A establishes only:

> From one already-loaded coherent 26C declared revision-edge segment, Pyxis can produce one immutable complete read-only presentation bundle containing the exact existing 27A declared rationale segment and one exact existing 27C working-set context for every declared position, with position-by-position presentation coherence and no additional file or browser access.

## What 28A does not prove or do

28A does **not** establish:

- complete revision history;
- chronology;
- latest/current revision;
- branch semantics;
- source authenticity;
- live quotation verification;
- citation authority;
- semantic support;
- semantic similarity, contradiction, or corroboration;
- Workspace provenance;
- file discovery;
- browser acquisition;
- fresh durable relinking;
- persistence;
- mutation;
- UI rendering.

The core boundary is:

```text
complete presentation surface
!=
complete history or stronger evidence
```
