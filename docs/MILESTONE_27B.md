# Milestone 27B — Independent Research Segment Textual Panel

Decision: D164

## Product question

After 27A produces a small read-only presentation of one coherent verified research-rationale segment, what is the next actual researcher need?

The researcher needs to see that presentation inside Pyxis without writing Python inspection code.

27B answers the narrow question:

```text
"I already have one 27A research presentation.
Show it in the existing Pyxis Textual experience,
without changing what the evidence means."
```

## New authority problem discovered before UI integration

The Repository Zero Workspace spine and the Chromium research spine are related parts of Pyxis, but 27A does not contain any field proving that one research segment belongs to one current Workspace.

Therefore silently placing a research segment under a heading such as:

```text
Workspace research
```

would invent a cross-spine provenance relationship.

27B refuses to do that.

The new rendered panel states explicitly:

```text
Independently supplied research evidence.
Displayed alongside Workspace evidence;
no association with this Workspace is asserted.
```

Thus:

```text
UI co-location
!=
Workspace provenance
```

and:

```text
same Pyxis shell
!=
shared authority chain
```

## Architecture

27B keeps the existing normal Workspace shell implementation unchanged.

Instead it adds one thin additive wrapper:

```text
existing pyxis.ui.workspace_shell.WorkspaceShell
                  ↓ subclassed by
pyxis.ui.research_workspace_shell.WorkspaceShell
```

The package-level exports:

```python
from pyxis.ui import WorkspaceShell, create_workspace_shell
```

now point to the additive wrapper.

The wrapper preserves the complete existing normal shell behavior and adds only one optional argument:

```python
research_presentation=
    ChromiumPageResearchRevisionEdgeSequencePresentation | None
```

The existing `workspace_shell.py` is not edited.

## Read-only research widget

The new explicit UI module is:

```text
pyxis.ui.chromium_research_revision_edge_sequence_textual
```

with:

```python
ResearchRevisionEdgeSequenceDetail
```

The widget consumes exactly one already-produced 27A presentation object.

It does not consume:

- a 26C loaded evidence graph;
- a declaration path;
- an edge path;
- a Chromium endpoint;
- a Workspace controller;
- a persistence destination;
- an LLM.

Therefore the UI direction remains:

```text
26C loaded evidence
→ 27A read-only presentation
→ 27B Textual rendering
```

not:

```text
UI
→ deep research evidence internals
```

## Rendered information

The panel renders only fields already present in 27A:

- durable declaration format and SHA-256 identity;
- starting-record format and SHA-256 identity;
- each one-based declared position;
- each edge format and SHA-256 identity;
- exact human-authored rationale text.

The note label is explicitly:

```text
Human-authored rationale — not source evidence
```

The position label is explicitly:

```text
Declared position N — not a global revision number
```

27B does not rename those fields into stronger concepts.

## Exact human wording

The panel uses Textual `Static(..., markup=False)` for human-authored rationale.

Strings such as:

```text
"  v5 exact human wording 😀  "
```

and:

```text
"v6 exact human wording\nStill tentative."
```

are supplied directly from 27A without trimming, Markdown interpretation, summarization, or normalization.

Thus:

```text
rendering human rationale
!=
editing human rationale
!=
interpreting human rationale
```

## No controls

The research detail mounts no:

- `Button`;
- `Input`;
- apply action;
- refresh action;
- browser action;
- save action;
- revision action.

The researcher can inspect the segment but cannot mutate research evidence through 27B.

Existing Workspace controls remain exactly the existing controls.

Thus:

```text
read-only presentation in UI
!=
research mutation authority
```

## Workspace operations do not refresh research evidence

A supplied 27A presentation is already an in-memory read-only evidence view.

If the user reruns the current Repository Zero Workspace runtime, 27B does not:

- reacquire browser evidence;
- reload research files;
- regenerate the research presentation;
- remove it merely because Workspace runtime state changed.

The exact supplied 27A object remains mounted.

This is safe only because the panel explicitly states that no Workspace association is asserted.

Therefore:

```text
Workspace runtime change
!=
research presentation invalidation
```

within this independent-display boundary.

## Deliberate contrast with measurement evidence

Pyxis measurement presentations already contain explicit Repository/Workspace/RIR subject identity, so the normal Workspace shell can reject or remove a measurement snapshot whose provenance no longer matches the current Workspace.

27A research presentations contain no equivalent Workspace provenance field.

27B does not pretend otherwise.

The two surfaces therefore have intentionally different behavior:

```text
measurement presentation
+ explicit Workspace/RIR provenance
→ provenance coherence enforcement
```

versus:

```text
27A research presentation
+ no Workspace provenance claim
→ independent display with explicit notice
```

This is not inconsistency. It is evidence-sensitive authority.

## Why the normal shell file remains untouched

`src/pyxis/ui/workspace_shell.py` already owns mature behavior for:

- Workspace runtime interaction;
- architecture preview and Apply;
- consequence trace;
- architecture reconciliation;
- measurement snapshot provenance/removal;
- export refresh.

27B has no reason to rewrite those behaviors.

A thin subclass lets the new surface compose with the existing shell while minimizing regression risk.

Thus:

```text
new display capability
!=
permission to restructure mature shell behavior
```

## Package-level compatibility

The public package-level names remain:

```python
pyxis.ui.WorkspaceShell
pyxis.ui.create_workspace_shell
```

Callers that do not provide `research_presentation` retain the existing visual path.

Callers may opt into 27B with:

```python
create_workspace_shell(
    workspace_presentation,
    research_presentation=research_presentation,
)
```

The dedicated research widget is not added to `pyxis.ui.__all__` in this milestone.

## Presentation-shape checks at the UI boundary

27B consumes 27A rather than recreating 27A validation.

It still performs small rendering-contract checks before mounting:

- exact 27A presentation type;
- supported presentation mode;
- supported sequence mode;
- non-empty members;
- contiguous one-based declared positions;
- supported edge format.

These checks prevent a forged or manually assembled presentation-shaped object from silently producing misleading labels.

They do not re-open files or inspect deep 26C evidence.

Therefore:

```text
UI rendering contract check
!=
27A evidence reconstruction
!=
fresh durable verification
```

## Falsifiability proof 1 — no research supplied

If `research_presentation=None`, no research detail is mounted.

27B does not invent an empty research history surface.

## Falsifiability proof 2 — wrong object type

Supplying an arbitrary object as `research_presentation` fails before the shell runs.

Thus:

```text
optional UI slot
!=
accept arbitrary display data
```

## Falsifiability proof 3 — forged declaration positions

Take a valid 27A presentation and replace the first member's:

```text
declared_position = 1
```

with:

```text
declared_position = 2
```

while leaving the rest unchanged.

27B rejects it rather than displaying two position-2 members or silently renumbering them.

Thus:

```text
UI order formatting
!=
authority to repair presentation evidence
```

## Falsifiability proof 4 — no hidden mutation controls

The focused tests query the research detail and require zero `Button` and zero `Input` widgets.

They also require the surrounding normal Workspace shell controls to remain unchanged.

## Falsifiability proof 5 — Workspace rerun does not replace research evidence

With one exact research presentation mounted, submit a different Workspace runtime input.

The Workspace presentation changes.

The research detail retains the exact same 27A presentation object and exact human rationale text.

This demonstrates that 27B does not silently regenerate research evidence during unrelated Workspace operations.

## Falsifiability proof 6 — different Workspaces may display the same research presentation

The focused tests construct two different Workspace identities and pass the exact same 27A presentation to both shells.

Both are accepted.

This is deliberate evidence that 27B makes no hidden Workspace-provenance assertion.

The rendered independence notice is therefore not merely explanatory copy; it describes the actual program contract.

## Language boundary

The panel deliberately avoids:

- `Latest`;
- `Current head`;
- `Revision 1` / `Revision 2` labels;
- chronology claims;
- truth/support labels.

It uses only:

```text
Declared position 1
Declared position 2
...
```

and explicitly says these are not global revision numbers.

## What successful 27B proves

Successful 27B establishes only:

> One already-produced coherent 27A revision-edge-sequence presentation can be rendered read-only inside the package-level Pyxis Textual shell as independently supplied research evidence, preserving exact declaration/member identities, exact declared positions, and exact human-authored rationale text while making no Workspace-provenance, chronology, head, source-support, or semantic-authority claim.

## What 27B does not prove or do

27B does **not** establish:

- that the research segment belongs to the current Workspace;
- that it is the latest research segment;
- that it is complete;
- that it is canonical history;
- that its declared positions are global revision numbers;
- chronology;
- branch or merge semantics;
- source truth;
- citation authority;
- semantic improvement;
- LLM interpretation;
- browser acquisition;
- file verification;
- research persistence;
- research mutation;
- research discovery;
- digest-to-path navigation.

## Authority boundary

The milestone preserves:

```text
verified loaded evidence
!=
27A presentation
!=
27B UI rendering
!=
Workspace provenance
!=
semantic authority
```

and adds the specific cross-spine rule:

```text
co-location
!=
association
```

## Scope summary

27B changes only the UI composition boundary:

1. one new read-only research detail module;
2. one new additive Workspace-shell wrapper;
3. one tiny package-level export reroute;
4. ten focused UI tests;
5. this milestone document / D164.

It makes no changes to:

- `src/pyxis/ui/workspace_shell.py`;
- 27A presentation semantics;
- 26A–26C relinking/persistence;
- browser acquisition;
- Repository Zero canonical/RIR/compiler/runtime behavior;
- measurement semantics;
- export semantics;
- README;
- `docs/CURRENT_STATE.md`.
