# Milestone 27A — Read-Only Presentation of a Verified Declared Revision-Edge Segment

Decision: D163

## Product question

After 26C can freshly reopen one durable human-declared revision-edge segment, what is the next actual researcher need?

The researcher needs to inspect what they reopened.

Until 27A, the Chromium research spine exposes rich typed application evidence, but a UI would have to understand deep 23C/24C/26A/26B/26C objects directly in order to show it.

That would couple presentation code to authority-bearing evidence internals and make it too easy for UI formatting to accidentally invent stronger claims such as:

- "latest revision";
- "current rationale";
- "revision 7";
- canonical history;
- chronological order;
- semantic improvement;
- source-supported truth.

27A introduces a deliberately small read-only presentation boundary instead.

The narrow question is:

```text
"I have one coherent 26C loaded declaration.
Show me the exact segment I declared and reopened,
without changing what that evidence means."
```

## Why presentation comes before UI

Pyxis already follows an application-presentation-UI separation for Repository Zero.

The Textual shell consumes `WorkspacePresentation` rather than reaching directly into compiler, canonical-authoring, revision-log, and export internals.

The Chromium research surface should follow the same rule.

Therefore 27A is not yet a new Textual screen.

It establishes the presentation contract that a future UI may render.

This keeps the authority chain explicit:

```text
26C loaded evidence
→ 27A read-only presentation
→ future renderer
```

not:

```text
UI reaches through evidence internals
→ UI invents interpretation
```

## Public API

The new explicit-module API is:

```python
present_chromium_research_working_set_note_revision_edge_sequence_declaration(
    loaded,
)
```

with immutable presentation records:

```python
ChromiumPageResearchRevisionEdgeSequencePresentation
ChromiumPageResearchRevisionEdgeSequenceMemberPresentation
```

The module lives at:

```text
pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation
```

27A does not broaden the `pyxis.app` root export surface.

## Presentation shape

The top-level presentation contains only:

```text
presentation_mode
declaration_format
declaration_record_sha256
sequence_mode
starting_record_format
starting_record_sha256
members
```

Each member contains only:

```text
declared_position
edge_format
edge_record_sha256
note_text
```

There is intentionally no:

- filesystem path;
- URL;
- browser page content;
- timestamp;
- revision number;
- latest marker;
- current-head marker;
- branch label;
- semantic score;
- source-support claim;
- citation claim;
- truth value.

## `declared_position` is not a revision number

The presentation uses one-based `declared_position` because the researcher needs a stable display order for the exact human-declared segment.

For example:

```text
declared position 1
declared position 2
declared position 3
```

This means only:

> member position inside this exact verified declaration.

It does not mean:

```text
revision 1
revision 2
revision 3
```

and it does not establish global chronology.

The sequence may start in the middle of a longer history.

Other sibling edges may exist.

The declaration may be only one human-selected segment.

Thus:

```text
declared position
!=
global revision number
!=
chronology
!=
current head
```

## Human text remains human text

Each presentation member exposes the exact `note_text` retained by the freshly relinked edge revision.

Leading and trailing whitespace, line breaks, Unicode, punctuation, and wording are preserved exactly.

27A does not summarize or normalize that text.

It does not label it as:

- fact;
- claim support;
- citation;
- source evidence;
- correct interpretation;
- machine conclusion.

The authority boundary remains:

```text
source evidence
!=
human working-set membership
!=
human rationale
!=
human revision
!=
presentation of that revision
```

## Presentation is not trusted by outer dataclass shape alone

27A does not simply accept any object whose Python type is:

```text
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
```

Before presenting anything it re-establishes the retained in-memory coherence already earned by the 26A/26B/26C boundaries.

It checks:

1. the retained 26B declaration format;
2. the retained sequence mode;
3. the loaded 26A sequence mode;
4. the live in-memory sequence through the existing 26B `_validate_live_sequence(...)` boundary;
5. the starting predecessor content identity against the retained declaration;
6. exact member count;
7. every member content identity position by position;
8. exact reconstructed human note text against the retained edge verification text.

Thus:

```text
outer loaded-record type
!=
coherent presentation evidence
```

## Reusing the 26B in-memory validation boundary

27A deliberately reuses the same retained sequence validation that 26B used before persistence.

That existing boundary re-establishes:

- exact predecessor-object chaining;
- bounded local 24C relationship coherence;
- retained 23B/24B canonical-document self-integrity;
- content identities derived from those retained canonical documents.

This avoids inventing a second presentation-specific identity algorithm.

Therefore:

```text
write-time retained identity interpretation
=
presentation-time retained identity interpretation
```

within the already-established bounded application evidence.

## No filesystem reads

27A performs no file I/O.

After a successful 26C load, the caller may remove:

- the 26B declaration file;
- all supplied 24B edge files;
- the starting edge file;
- the 23B continuation file;
- the 22B revision file;
- the 21B note file;
- the 20B working-set file;
- member sidecars.

27A still succeeds from the already-loaded coherent application evidence.

Thus:

```text
current durable-file availability
!=
ability to present already-loaded verified application evidence
```

This is not fresh verification.

It is a read-only view over already-loaded evidence.

## No browser reads

27A does not connect to Chromium.

It does not reacquire:

- page text;
- paragraph evidence;
- URLs;
- headings;
- links;
- tables;
- metadata;
- lists.

The research evidence that ultimately motivated the working set remains elsewhere in the already-loaded object graph.

27A exposes only the declared revision segment and exact human rationale text.

## No source-content promotion

27A intentionally does not copy source excerpts into the presentation.

A researcher seeing a rationale revision is not automatically seeing the underlying source evidence that informed it.

That separation matters:

```text
human rationale presentation
!=
source quotation presentation
!=
citation authority
```

A future source-evidence view can be built through its own explicit presentation boundary if product pressure requires it.

## Falsifiability proof 1 — forged retained starting identity

Take a valid 26C loaded declaration record.

Replace only the retained declaration's starting content digest with another syntactically valid SHA-256.

Do not change the actual loaded starting predecessor.

27A rejects presentation because the observed in-memory starting content identity no longer matches the retained declaration.

Therefore:

```text
loaded declaration wrapper
+
forged retained identity
!=
presentable coherent evidence
```

## Falsifiability proof 2 — forged retained declaration order

Take a valid two-member 26C record.

Reverse only the retained declaration references while keeping the actual loaded sequence unchanged.

27A rejects member 0 identity mismatch.

It does not reorder either side.

Thus:

```text
same identities
+
different retained declaration order
!=
same presentation evidence
```

## Falsifiability proof 3 — forged loaded sequence order

Take a valid 26C record.

Reverse the loaded edge objects themselves while keeping the declaration unchanged.

The existing live-sequence validation rejects the first broken predecessor relationship.

27A does not display the forged tuple merely because every element has a valid edge type.

Thus:

```text
tuple of valid-looking edge objects
!=
coherent loaded declared sequence
```

## Falsifiability proof 4 — forged displayed note text

Take one valid loaded edge.

Replace the reconstructed revised-note text in memory while leaving the retained verified edge text unchanged.

27A rejects presentation.

This prevents UI-facing text from drifting away from the exact human wording already re-established by the edge evidence.

Therefore:

```text
mutable-looking reconstructed display value
!=
authority to change presented human wording
```

## Exact-text preservation proof

The focused tests preserve and present strings including:

```text
"  v5 exact human wording 😀  "
```

and:

```text
"v6 exact human wording\nStill tentative."
```

without trimming, normalization, summarization, or Unicode loss.

This earns only the claim:

> the presentation preserves the exact already-loaded human-authored text.

It does not earn any semantic claim about that text.

## Starting at a 23C continuation remains supported

26A, 26B, and 26C allow a declared segment to start from either:

- an already-loaded 23C continuation; or
- an already-loaded 24C revision edge.

27A preserves both.

The top-level presentation records the exact starting record format and content digest.

It does not attempt to normalize both families into a synthetic "revision number."

## Immutable presentation records

Both presentation dataclasses are frozen and slot-backed.

The focused tests assert that mutation fails.

The field surface is also tested exactly so accidental additions such as:

```text
path
latest
current_head
timestamp
```

cannot silently enter the presentation contract.

## What successful 27A proves

Successful 27A establishes only:

> One already-loaded coherent 26C declaration/sequence relationship can be transformed into a small immutable read-only presentation containing the exact declaration identity, exact starting content identity, exact declared member identities and positions, and exact already-loaded human-authored revised-note wording.

It does not prove:

- complete history;
- canonical history;
- chronology;
- current head;
- newest revision;
- unique branch;
- semantic improvement;
- correctness of human interpretation;
- source support;
- citation authority;
- source authenticity;
- trusted authorship;
- trusted timestamps.

## Authority boundary after 27A

The browser/research spine can now be stated as:

```text
browser evidence
→ durable capture
→ human selection
→ human interpretation
→ working set
→ human rationale
→ explicit human revision edges
→ durable general revision edges
→ explicit ordered segment
→ durable human segment declaration
→ verified declaration relinking
→ read-only presentation
```

The new boundary is:

```text
verified loaded evidence
!=
read-only presentation
!=
UI rendering
!=
semantic authority
```

## What 27A deliberately does not do

27A does not add:

- a Textual research screen;
- shell navigation;
- research-file picker;
- directory scanning;
- content-address discovery;
- browser acquisition;
- source excerpt rendering;
- working-set member rendering;
- edit controls;
- revision controls;
- persistence;
- export;
- LLM analysis;
- search;
- chronology;
- head selection;
- branch interpretation.

Those capabilities require separate product pressure and separate authority decisions.

## Next product pressure

Once 27A exists, the next concrete researcher question is finally UI-shaped:

```text
"Can I see this verified declared rationale segment inside Pyxis's existing Textual shell?"
```

A future milestone can render the 27A presentation without teaching the UI how to understand deep research evidence internals.

That is now an earned UI boundary rather than architecture gardening.
