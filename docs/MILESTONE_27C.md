# Milestone 27C — Read-Only Working-Set Context for One Declared Rationale

Decision: D165

## Product question

27B makes a verified human rationale segment visible in the Pyxis Textual shell.

The next researcher question is not another persistence question:

```text
"I can read this rationale revision.
What exact research evidence was this rationale attached to?"
```

27C answers that question without reacquiring Chromium, rereading durable sidecars, or claiming that any source evidence supports the rationale.

## Public boundary

The new explicit-module API is:

```python
present_chromium_research_revision_edge_working_set_context(
    loaded,
    declared_position=...,
)
```

where `loaded` is one already-loaded coherent 26C declaration/sequence record.

The output is an immutable:

```text
ChromiumPageResearchRationaleWorkingSetPresentation
```

containing:

- the durable declaration identity;
- the selected one-based declared position;
- the selected edge content identity;
- the exact segment-level human rationale text;
- the retained human working-set mode;
- one ordered presentation member for every exact working-set member.

## Why this comes after 27B

27A intentionally omitted source context so the first UI could not accidentally promote rationale text into source evidence.

27B made that rationale visible with the explicit label:

```text
Human-authored rationale — not source evidence
```

Once that boundary is visible, the next useful researcher action is to inspect the evidence context separately.

The direction is now:

```text
26C verified declared segment
→ 27A rationale-segment presentation
→ 27B rationale-segment UI

26C verified declared segment
→ 27C selected-rationale working-set presentation
→ future source-context UI
```

27C does not collapse these two presentation layers.

## Selection authority

The caller supplies exactly one `declared_position`.

That position means only:

> the one-based position inside this exact verified human-declared segment.

It is not:

- a global revision number;
- chronology;
- a latest marker;
- current head;
- semantic rank.

27C first reuses the complete 27A presentation boundary to re-establish the retained declaration/sequence relationship.

Only then does it select the matching loaded edge at the caller-supplied position.

Thus:

```text
declared position
!=
global revision number
```

and:

```text
caller position choice
!=
discovery of a current or preferred revision
```

## Working-set relationship

Every 22A-style rationale revision retains a `revised_note` over the exact same explicit human working set.

27C obtains the working set from the selected edge's reconstructed revised note and revalidates its members through the existing public 20A constructor:

```text
create_chromium_research_working_set(...)
```

This re-establishes the already-loaded member contracts without reading files.

Successful 27C therefore proves only:

> this exact selected human rationale revision is attached to this exact already-loaded explicit human working set.

It does not prove that the sources support the rationale.

## Three evidence families remain distinct

27C supports the three established 20A member families without flattening them.

### Paragraph note

For a 17D paragraph-note member, 27C presents:

- exact member position;
- member kind `paragraph_note`;
- exact human note text;
- source capture format and bundle content identity;
- observed URL;
- paragraph ordinal;
- the already-returned paragraph `text_prefix`;
- whether that paragraph prefix was truncated.

The excerpt kind is explicitly:

```text
returned_paragraph_prefix
```

It is not called a complete paragraph or verified quotation.

### Exact-range note

For an 18D exact-range-note member, 27C presents:

- exact member position;
- member kind `exact_range_note`;
- exact human note text;
- source capture identity and URL;
- paragraph ordinal;
- the exact already-returned selected text;
- Unicode code-point offset unit;
- zero-based half-open start/end offsets;
- parent paragraph truncation fact.

The excerpt kind is:

```text
exact_returned_text_range
```

### Comparison note

For a 19D comparison-note member, 27C preserves one member with two separately labeled source excerpts:

```text
first_selection
second_selection
```

It does not convert the human juxtaposition into a machine similarity, contradiction, corroboration, or support claim.

Thus:

```text
human juxtaposition
!=
machine semantic relationship
```

## Three interpretation layers remain separate

27C intentionally exposes three different kinds of text:

```text
bounded source excerpt
!=
human note on that source selection
!=
human rationale over the working set
```

The source excerpt is never labeled as the rationale.

The member-level note is never labeled as source evidence.

The segment-level rationale is never labeled as a fact or conclusion.

This preserves the existing authority chain:

```text
source evidence
→ human selection
→ human member note
→ human working-set membership
→ human working-set rationale
→ human rationale revision
```

without upgrading any arrow into semantic support.

## Bounded source text stays bounded

Paragraph members expose only the already-returned paragraph prefix.

Exact-range and comparison members expose only exact ranges inside already-returned prefixes.

27C records the parent paragraph's `truncated` fact so future UI can distinguish:

```text
returned prefix is complete
```

from:

```text
returned prefix is bounded and more source text existed
```

27C never expands a truncated prefix.

It performs no Chromium acquisition and no capture-file read.

## Source identity is not source authenticity

Each excerpt carries:

- persisted capture format;
- capture bundle SHA-256 content identity;
- observed URL.

These fields make it possible to distinguish retained source captures and inspect where the evidence was observed.

They do not prove:

- server identity;
- publication authenticity;
- authorship;
- trusted time;
- canonical URL ownership;
- chain of custody;
- truth.

Thus:

```text
capture content identity + observed URL
!=
source authenticity
```

## No file reads after 26C load

After the 26C record is already loaded, the caller may remove:

- all three original member sidecars;
- the 20B working-set sidecar;
- 21B note sidecar;
- 22B revision sidecar;
- 23B continuation sidecar;
- starting 24B edge;
- successor edge files;
- 26B declaration file.

27C still succeeds from the retained coherent application evidence.

Therefore:

```text
current durable-file availability
!=
ability to inspect already-loaded rationale working-set context
```

This is not fresh durable verification.

## No UI yet

27C is a presentation boundary only.

It does not modify the 27B Textual shell.

A future UI milestone may render this presentation once the presentation contract itself is independently tested.

That preserves the same application → presentation → UI separation used by 27A/27B.

## Falsifiability

Focused tests prove:

1. A selected declared rationale presents the exact three-member mixed working set: paragraph note, exact-range note, comparison note.
2. Selecting declared position 1 versus 2 changes the rationale/edge identity but leaves the exact working-set context unchanged.
3. Wrong loaded types, non-integer positions, position 0, and positions outside the declared segment reject.
4. A forged retained declaration order is rejected through the reused 27A coherence boundary before source context is exposed.
5. A forged selected working-set mode is rejected.
6. Capture format, capture digest, observed URL, paragraph ordinal, offsets, and truncation facts remain explicit in the source-excerpt presentation.
7. Presentation succeeds after every durable input file is deleted following successful 26C loading.
8. All presentation records are immutable and intentionally contain no path, timestamp, latest, current-head, truth, support, citation, or source-authenticity field.
9. Human member notes and segment-level rationale remain distinct from bounded source excerpt text.
10. The explicit module is importable without broadening the package root export surface.

## What successful 27C proves

Successful 27C establishes only:

> For one caller-selected declared position inside one already-loaded coherent 26C segment, Pyxis can produce a small immutable read-only presentation of the exact human working set retained by that rationale revision, preserving ordered member type, bounded source text, capture content identity, observed URL, selection coordinates where applicable, exact member-level human notes, and exact segment-level human rationale text.

## What 27C does not prove or do

27C does **not** establish:

- that any source supports the rationale;
- that the rationale accurately interprets the sources;
- that the member notes accurately interpret their selections;
- source authenticity;
- quotation verification against a live page;
- citation authority;
- completeness of a page or paragraph;
- chronology;
- a latest/current revision;
- branch semantics;
- semantic similarity or contradiction;
- machine judgment;
- Workspace provenance;
- file discovery;
- browser acquisition;
- persistence;
- mutation.

The core boundary is:

```text
bounded source evidence
!=
human note
!=
human rationale
!=
semantic support
```

and:

```text
rationale attached to working set
!=
working set proves rationale
```
