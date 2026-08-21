# Milestone 27D — Textual Inspection of Attached Rationale Working-Set Context

Decision: D166

## Product question

27B made a verified human rationale segment visible in the Pyxis Textual shell.
27C made it possible to produce a bounded read-only presentation of the exact human working set attached to one caller-selected declared rationale position.

The next researcher action is:

```text
"I can see this rationale.
Let me inspect the source context and human notes it was attached to."
```

27D renders already-produced 27C presentations inside the existing research panel and lets the researcher reveal or hide them without changing research evidence.

## Input boundary

The Textual shell still consumes presentation records rather than deep research evidence.

27D accepts:

```text
27A revision-edge sequence presentation
+
zero or more explicit 27C rationale working-set presentations
```

It does **not** accept a 26C loaded evidence graph, browser endpoint, declaration path, edge path, or persistence destination.

Thus:

```text
26C loaded evidence
→ 27C application presentation
→ 27D UI
```

not:

```text
UI
→ deep loaded research evidence
```

## Attachment reconciliation before rendering

A supplied 27C context is accepted only when all of the following match the displayed 27A member at its declared position:

- durable declaration SHA-256;
- declared position;
- edge format;
- edge SHA-256;
- exact human rationale text.

Duplicate context positions are rejected.
A context outside the displayed segment is rejected.
A context cannot be supplied without a research segment.

27D also validates the small 27C rendering contract before mount: supported presentation/working-set mode, supported member families, supported source excerpt roles/kinds, capture identities, paragraph ordinals, truncation flags, and exact-range coordinates.

This is a UI presentation-contract check. It is not fresh durable relinking.

## Researcher interaction

Only rationale members with an explicitly supplied matching 27C presentation receive:

```text
Inspect attached working set
```

The control toggles visibility of that already-produced presentation.

It does not:

- read files;
- reacquire Chromium;
- create a new 27C presentation;
- mutate a working set;
- revise a rationale;
- persist anything;
- discover other revisions;
- select a latest/current head;
- perform semantic analysis.

Therefore:

```text
inspect/hide UI state
!=
research evidence mutation
```

## Rendered authority layers

The expanded detail keeps three text layers visibly distinct:

```text
bounded source excerpt
!=
human note on selected source evidence
!=
human rationale over the working set
```

The attachment notice states explicitly:

```text
Attached human working set. Attachment records what the rationale was authored
about; it does not mean the source evidence proves or supports the rationale.
```

### Paragraph-note member

Renders:

- member position and kind;
- exact human note text;
- capture format and SHA-256 content identity;
- observed URL;
- paragraph ordinal;
- parent paragraph truncation fact;
- exact returned paragraph prefix;
- label: `Bounded returned paragraph prefix — not a verified quotation`.

### Exact-range member

Renders the same source identity facts plus:

- Unicode code-point offset unit;
- zero-based half-open range;
- exact returned selected text;
- label: `Exact returned text range — not a verified quotation`.

### Comparison member

Retains one human comparison note with two separately labeled excerpts:

```text
first_selection
second_selection
```

27D does not infer contradiction, similarity, corroboration, support, or any other machine semantic relationship.

## Workspace independence remains intact

27D continues 27B's cross-spine boundary.

Research rationale and source-context presentations may be displayed alongside Repository Zero Workspace evidence, but no Workspace provenance relationship is asserted.

A Workspace runtime rerun leaves the exact supplied research segment and exact supplied 27C context presentations mounted.

Thus:

```text
same Textual shell
!=
shared provenance chain
```

and:

```text
Workspace runtime change
!=
research-context refresh
```

## Backward compatibility

If no 27C contexts are supplied, the 27B research panel behaves as before and adds no research controls.

Existing callers of:

```python
create_workspace_shell(..., research_presentation=segment)
```

remain valid.

27D adds only the optional argument:

```python
research_working_set_contexts=(...)
```

The mature `src/pyxis/ui/workspace_shell.py` remains unchanged.

## Falsifiability

Focused tests prove:

1. One explicitly supplied context mounts only under its matching declared rationale position and begins collapsed.
2. The inspect control reveals and hides the exact same 27C presentation object.
3. Source excerpt text, member-level human notes, and segment-level rationale remain separate rendered fields.
4. Comparison context preserves two explicit source selections, URLs, and ranges.
5. Contexts without a displayed research segment are rejected.
6. A context naming a different declaration is rejected.
7. A context naming a different edge identity is rejected.
8. A context carrying different rationale text is rejected.
9. Duplicate context positions and forged excerpt shapes are rejected before shell mount.
10. Repository Zero runtime rerun preserves the exact supplied context tuple and exact context presentation objects.

## What successful 27D proves

Successful 27D establishes only:

> Pyxis can render one or more explicitly supplied, presentation-coherent 27C rationale working-set contexts beneath their matching rationale positions in the existing Textual research panel, with researcher-controlled reveal/hide state and explicit separation among bounded source evidence, human source notes, and human rationale text.

## What 27D does not prove or do

27D does **not** establish:

- that any source supports or proves the rationale;
- source authenticity;
- live quotation verification;
- citation authority;
- source completeness;
- chronology;
- latest/current revision semantics;
- branch semantics;
- Workspace provenance;
- semantic similarity/contradiction/corroboration;
- file discovery;
- browser acquisition;
- durable relinking;
- persistence;
- evidence mutation;
- rationale revision.

The core boundaries remain:

```text
rationale attached to working set
!=
working set proves rationale
```

and:

```text
UI visibility state
!=
evidence authority
```
