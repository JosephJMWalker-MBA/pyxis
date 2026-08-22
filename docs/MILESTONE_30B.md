# Milestone 30B — Textual Explicit Continuation-Session Rollover

Decision: D172

## Product question

29B lets a researcher inspect one declared research session and persist one explicit successor rationale from the declared endpoint.

30A then established the application-level adoption boundary:

```text
old declared endpoint
+ explicitly chosen successful successor result
+ explicit durable successor path
+ explicit new declaration destination
→ new verified declared continuation session
→ new research controller
```

The remaining product friction is now direct:

```text
"I wrote this successor in the Pyxis shell.
I want to keep working from this exact successor.
Let me explicitly continue from it here."
```

30B wires 30A into the research-aware Textual shell without introducing automatic head selection, path discovery, or Workspace provenance coupling.

## Research UI flow

The controller-backed research surface now has two separate mutation stages:

```text
1. Revise declared endpoint rationale
   → 29A durable successor write
   → old displayed session remains unchanged

2. Continue from persisted successor
   → explicit successor path
   → explicit new declaration destination
   → 30A rollover
   → mount returned continuation controller
```

The separation is intentional.

A successful write is still not adoption.

A successful rollover is an explicit local continuation choice, not a global head claim.

## New Textual control surface

30B adds:

```text
pyxis.ui.chromium_research_session_rollover_textual
```

with:

```text
ResearchSessionRolloverControls
ROLLOVER_AUTHORITY_NOTICE
rollover_success_receipt(...)
```

The rollover controls display:

```text
Continue from persisted successor

[authority notice]

Displayed successor identity

Durable file for this exact displayed successor
[path input]

No-overwrite destination for the new continuation declaration
[path input]

[Continue from this successor — create new declared session]

[status]
```

## Disabled until there is a concrete successor

When a controller has no successful endpoint revision:

- successor-path input is disabled;
- declaration-destination input is disabled;
- rollover button is disabled;
- no successor is implied or discovered.

After a successful 29B write, the exact returned 29A result becomes the displayed rollover candidate and those controls become active.

A controller mounted with an already-retained successful 29A result likewise displays that result as the candidate.

## Explicit candidate choice

30A deliberately does not use `controller.last_endpoint_revision` as continuation authority.

30B preserves that distinction at the interaction boundary.

The UI may display one retained successful receipt because that is the only successor receipt this mounted controller surface exposes. Pressing:

```text
Continue from this successor
```

is the explicit user choice of that exact displayed result.

The control copy states that sibling successors, if any, are not discovered or enumerated.

Therefore:

```text
displayed retained result
+ explicit Continue action
→ chosen 30A result
```

but:

```text
controller bookkeeping order
!=
automatic continuation authority
```

## Paths remain explicit

30B intentionally leaves both rollover path inputs blank even though the prior persistence result contains its original write destination.

The user supplies:

1. the durable file location that should now be reopened as the chosen successor;
2. the destination for the new continuation declaration.

Pyxis does not prefill or infer either path.

This preserves:

```text
path = location, not identity
```

and allows moved identical successor bytes to remain usable from a new explicitly supplied location.

## Delegation to 30A

The Textual shell does not implement rollover semantics itself.

It delegates exactly:

```text
rollover_chromium_research_session_to_persisted_successor(
    prior_controller,
    displayed_chosen_revision,
    successor_edge_source=explicit_path,
    declaration_destination=explicit_path,
)
```

30A remains responsible for:

- selected-result coherence;
- fresh successor relinking;
- content-identity matching;
- exact human-text matching;
- new one-edge 26B declaration persistence;
- fresh 26C declaration relinking;
- construction of the new continuation controller.

30B adds no research persistence format.

## Successful UI adoption

Only after 30A returns successfully does 30B replace the mounted research surface.

The shell updates only:

```text
research_controller
research_session
research_presentation
research_working_set_contexts
last_research_rollover
```

The old research widgets are removed and replaced with:

1. a transient rollover receipt;
2. the exact new 28A continuation presentation;
3. a fresh unlocked 29B endpoint-revision form for the new endpoint;
4. a fresh disabled rollover form awaiting the next durable successor.

The Repository Zero Workspace presentation/controller remains untouched.

## Visible rollover receipt

A successful rollover produces a transient UI receipt containing:

- exact selected successor SHA-256;
- exact new declaration SHA-256;
- explicit new declaration path;
- a statement that the mounted research session now represents this explicit continuation;
- a statement that this is not a global latest/current/head claim.

The receipt is not a durable authority record.

The durable authority remains the new 26B declaration freshly re-established through 26C and retained by the new controller.

## Old session remains intact

30B mounts the new continuation controller but does not mutate the old controller or old declaration.

The 30A result retains the exact old controller and exact selected revision result.

Thus:

```text
shell now displaying continuation controller
!=
old controller mutated
```

and:

```text
local UI adoption
!=
global revision authority
```

## Failure behavior

Before 30A, blank path inputs reject with a UI status message.

If 30A rejects because the explicit successor file is wrong, a sibling does not match the displayed chosen result, or the declaration destination already exists:

- the old research controller remains mounted;
- the old presentation remains mounted;
- no false rollover receipt appears;
- the rollover controls remain active;
- existing destination bytes remain untouched under existing no-overwrite semantics.

## Read-only forms remain read-only

The existing shell forms remain distinct:

```text
research_session=
research_presentation= + optional contexts
```

These read-only forms mount no endpoint mutation controls and no rollover controls.

Only:

```text
research_controller=
```

can expose the governed write/rollover loop.

## Workspace independence

A successful research rollover does not modify Repository Zero Workspace state.

Likewise, a later Workspace runtime rerun does not replace the newly adopted research continuation controller.

Therefore:

```text
research continuation adoption
!=
Workspace mutation
```

and:

```text
same Textual shell
!=
shared provenance chain
```

remain explicit.

## Repeatable governed loop

30B makes the existing architecture usable as a repeated researcher workflow:

```text
inspect declared rationale + bounded context
→ write explicit successor
→ explicitly continue from that successor
→ inspect new declared continuation
→ write next explicit successor
→ explicitly continue again
```

For example:

```text
v6 declared endpoint
→ write v7
→ explicitly roll over to one-edge declaration v6 → v7
→ write v8
→ explicitly roll over to one-edge declaration v7 → v8
```

At no point does Pyxis require or assert:

- latest;
- current global revision;
- canonical head;
- complete history;
- unique successor;
- branch ranking.

## Falsifiability

Focused tests prove:

1. rollover controls begin disabled when no successful successor exists and infer no paths;
2. one successful 29B UI write enables the exact returned successor as the rollover candidate while keeping path fields blank;
3. one successful rollover replaces only the research surface with the exact 30A continuation controller and leaves the old controller/declaration unchanged;
4. moved identical successor bytes can be explicitly selected from a new location;
5. a different valid sibling successor file rejects when it does not match the displayed chosen result;
6. blank rollover paths reject before 30A without state change;
7. an occupied declaration destination remains no-overwrite and leaves the old session mounted;
8. read-only research forms remain free of both mutation and rollover controls;
9. a Workspace runtime rerun after research rollover preserves the exact newly adopted research continuation;
10. the UI can repeat the write → rollover cycle through a second successor without introducing latest/head state.

## Scope

30B changes only:

- new `src/pyxis/ui/chromium_research_session_rollover_textual.py`;
- research-aware `src/pyxis/ui/research_workspace_shell.py`;
- one endpoint-success receipt sentence in `chromium_research_endpoint_revision_textual.py`;
- its corresponding legacy UI assertion;
- focused 30B interaction tests;
- this milestone document.

It does not change:

- `src/pyxis/ui/workspace_shell.py`;
- 30A rollover semantics;
- 29A controller semantics;
- any research persistence schema;
- Chromium acquisition;
- LLM behavior;
- Repository Zero compiler/RIR/runtime/export/measurement semantics;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 30B proves

Successful 30B establishes only:

> From one controller-backed research session with one explicitly displayed successful successor receipt, the Pyxis Textual shell can require explicit successor/declaration paths, delegate the exact displayed successor choice to the existing 30A rollover boundary, and only after fresh 30A success replace the mounted research surface with the returned declared continuation controller while leaving the old controller, old declaration, and Repository Zero Workspace state unchanged.

That does not prove global chronology, complete history, unique succession, semantic improvement, or a canonical/current/latest head.
