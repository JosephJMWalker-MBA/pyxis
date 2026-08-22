# Milestone 28B — Complete Research Session Textual Input

Decision: D168

## Product question

28A removes application-side presentation ceremony by producing one immutable complete research-session presentation:

```text
28A session
  = 27A declared rationale segment
  + one 27C working-set context for every declared position
```

27D's Textual shell still required callers to split that bundle back apart:

```python
create_workspace_shell(
    workspace,
    research_presentation=session.sequence,
    research_working_set_contexts=session.working_set_contexts,
)
```

28B answers the practical next step:

```text
"I already have one complete read-only research-session presentation.
Display that exact session in Pyxis without unpacking it myself."
```

## Public UI boundary

The existing package-level shell factory now accepts:

```python
create_workspace_shell(
    workspace,
    research_session=session,
)
```

where `session` is an already-produced:

```text
ChromiumPageResearchSessionPresentation
```

The shell retains the exact session object and uses its exact existing subpresentations:

```text
session.sequence
session.working_set_contexts
```

No new research evidence or presentation family is created by the UI.

## Compatibility

The existing split form remains valid:

```python
create_workspace_shell(
    workspace,
    research_presentation=sequence,
    research_working_set_contexts=contexts,
)
```

28B therefore adds a convenience entry point rather than replacing the 27B/27D interface.

The two forms are deliberately mutually exclusive.

A caller may provide either:

```text
complete 28A session
```

or:

```text
27A sequence + zero or more explicit 27C contexts
```

but not both in one invocation.

This prevents precedence ambiguity and accidental cross-attachment of contexts from another presentation surface.

## Session validation before mount

The UI does not trust the outer 28A dataclass by type alone.

Before mounting a complete session, 28B requires:

1. the exact 28A presentation type;
2. the supported complete-session presentation mode;
3. a valid existing 27A sequence presentation;
4. valid existing 27C context presentation shapes;
5. each context to reconcile to the displayed 27A sequence through the existing 27D attachment checks;
6. exactly one context for every declared sequence member.

Thus a forged session wrapper cannot use the convenience API to bypass the established presentation boundaries.

The shell reuses existing validation rather than introducing a second identity algorithm.

## Complete means complete

28A defines a complete research-session presentation as one context per declared position.

28B preserves that contract.

If a forged session contains fewer contexts than sequence members, the shell rejects it before mount.

Therefore:

```text
28A complete session input
!=
partial 27D context input
```

The older split form still permits partial context display because that is an intentional 27D capability.

The distinction is explicit in which input form the caller chooses.

## Rendering remains unchanged

28B does not create a new widget.

After validation, the session is routed through the existing 27D rendering surface:

```text
28A session
  ↓
existing 27A sequence presentation
  +
existing complete 27C context tuple
  ↓
existing ResearchRevisionEdgeSequenceDetail
  ↓
existing inspect/hide controls
```

Therefore all established labels and authority boundaries remain unchanged, including:

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

## Workspace independence remains intact

A complete research session remains independently supplied research presentation evidence.

Passing it through the same Textual shell as Repository Zero Workspace evidence does not create Workspace provenance.

A Workspace runtime rerun retains the exact session object, exact sequence presentation, and exact context presentation objects.

Thus:

```text
Workspace runtime mutation
!=
research-session refresh
```

and:

```text
same shell
!=
shared provenance chain
```

## No new I/O or authority

28B performs no:

- browser acquisition;
- file reads;
- file discovery;
- durable relinking;
- persistence;
- research mutation;
- rationale revision;
- chronology inference;
- latest/current-head selection;
- semantic support analysis;
- citation validation;
- source-authenticity validation.

It consumes presentation records only.

Therefore:

```text
UI convenience
!=
evidence authority
```

## Falsifiability

Focused tests prove:

1. one complete 28A session mounts the full sequence and every context;
2. the shell retains the exact session object and exact subpresentation objects;
3. complete-session input cannot be combined with the split sequence input;
4. complete-session input cannot be combined with split contexts;
5. the wrong session type is rejected;
6. a forged session presentation mode is rejected;
7. incomplete complete-session context coverage is rejected;
8. a forged session context attachment is rejected through existing 27D identity checks;
9. the legacy split 27A/27C form remains supported and produces the same research surface;
10. Workspace runtime rerun preserves the exact complete session and subpresentations.

## Scope

28B changes only:

- `src/pyxis/ui/research_workspace_shell.py`;
- focused 28B UI tests;
- this milestone document.

It does not change:

- `src/pyxis/ui/workspace_shell.py`;
- 28A application semantics;
- 27A or 27C presentation semantics;
- persistence schemas;
- browser acquisition;
- Repository Zero compiler/RIR/runtime/export/measurement behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 28B proves

Successful 28B establishes only:

> The existing Pyxis research-aware Textual shell can consume one complete immutable 28A research-session presentation directly, validate that its existing 27A sequence and complete 27C context set remain presentation-coherent, and render those exact presentation objects through the already-established 27D research UI without caller-side unpacking.

## What 28B does not prove

28B does not establish:

- complete revision history;
- chronology;
- latest/current revision;
- branch semantics;
- source authenticity;
- citation authority;
- semantic support;
- Workspace provenance;
- file discovery;
- fresh durable verification;
- persistence;
- mutation.

The core boundary is:

```text
complete-session UI convenience
!=
stronger research authority
```
