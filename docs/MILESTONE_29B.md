# Milestone 29B — Textual Declared-Endpoint Rationale Revision

Decision: D170

## Product question

29A creates the first application-owned mutation action over one loaded declared research session:

```text
loaded declared segment endpoint
→ explicit human rationale revision
→ explicit current endpoint file
→ explicit destination
→ durable successor
```

28B already displays one complete 28A research session in the normal Pyxis Textual shell.

The remaining researcher friction is therefore direct:

```text
"I inspected the rationale and its bounded working-set evidence in Pyxis.
I decided to revise the rationale at the declared endpoint.
Let me perform that explicit governed write here without pretending the new edge
has already become the displayed session."
```

29B wires the existing 29A controller into the research-aware Textual shell while preserving 29A's central non-adoption rule.

## Mutating shell form

The package-level research-aware shell gains one optional input:

```python
create_workspace_shell(
    workspace,
    research_controller=controller,
)
```

where `controller` is one already-created:

```text
ChromiumResearchSessionController
```

The shell derives its exact displayed research session from:

```text
controller.presentation
```

rather than requiring the caller to separately provide the controller and an equal-looking 28A presentation.

Thus the mutating form has one application authority source.

## Mutually exclusive research input forms

The shell now supports three deliberate forms:

```text
1. research_controller=
   governed declared-endpoint mutation + complete session display

2. research_session=
   complete read-only 28A session display

3. research_presentation= + optional research_working_set_contexts=
   older read-only 27A/27C split display
```

These forms may not be mixed.

In particular:

```text
research_controller
!=
permission to attach an independently supplied presentation or context set
```

This avoids precedence ambiguity and cross-attachment between one controller's loaded evidence and another presentation surface.

## Controller coherence before mount

The UI does not trust `ChromiumResearchSessionController` merely because its Python type matches.

Before mounting mutation controls, 29B:

1. requires the exact 29A controller type;
2. rebuilds the complete 28A presentation from `research_controller.loaded` through the existing public 28A presentation boundary;
3. requires that rebuilt presentation to equal the controller's retained presentation;
4. if the controller already has a successful endpoint revision result, requires that result's `prior_session` to be the exact retained controller presentation;
5. then routes the controller's exact presentation through the same 28B session validation and existing 27D rendering checks.

Thus a forged controller wrapper cannot gain a mutation control merely by carrying plausible-looking fields.

## Explicit endpoint revision controls

29B adds one dedicated Textual control surface below the displayed research session:

```text
Revise declared endpoint rationale

[authority notice]

New human-authored rationale — exact multiline text is preserved
[multiline editor]

Current durable file for the exact declared endpoint
[path input]

No-overwrite destination for the new successor edge
[path input]

[Persist durable successor — displayed session will not advance]

[status / durable-write receipt]
```

The user must explicitly supply all three mutation inputs:

1. revised human wording;
2. current durable location of the exact declared endpoint edge;
3. destination for the new successor edge.

The UI does not infer either path from the durable declaration, retained loaded record, directory contents, or content digest.

## Exact human text

The rationale editor is multiline.

29B passes its text verbatim into 29A.

It performs no trimming, normalization, summarization, semantic diff, or machine rewriting.

Therefore all existing exact-text rules remain owned by 25A / 22A:

- exact whitespace survives;
- multiline wording survives;
- Unicode survives;
- exact textual no-op rejects;
- textual change does not imply semantic improvement.

## Explicit path validation

The UI performs only one convenience check before invoking 29A:

```text
blank predecessor path → reject
blank destination path → reject
```

Nonblank paths are passed explicitly to 29A / 25B.

The existing durable authority still owns whether:

- the predecessor bytes identify the exact loaded declared endpoint;
- the destination parent exists;
- the destination is unused;
- persistence succeeds.

Thus:

```text
path text entered in UI
!=
content identity
```

and:

```text
path = location, not identity
```

remain intact.

## Success receipt

After one successful write the UI displays a receipt containing:

```text
Success — durable successor written; declared session unchanged.
Successor is not adopted/current/head.
Successor edge SHA-256: <content identity>
Destination: <explicit written location>
Reopen and explicitly redeclare before authoring another successor from the UI.
```

The receipt is transient UI state over the exact successful 29A result.

It is not a new durable format, chronology record, declaration, head pointer, or semantic judgment.

## Lock after one successful UI write

A 29A controller deliberately permits explicit successor writes without claiming uniqueness.

The interactive shell takes a narrower safety posture.

After the first successful UI write from this declared session endpoint, 29B disables:

- the rationale editor;
- predecessor-path input;
- destination-path input;
- persistence button.

The researcher is told to reopen and explicitly redeclare before authoring another successor through the UI.

This does **not** prove that no sibling successor exists or may be created elsewhere.

It establishes only:

```text
this mounted UI session
will not casually issue a second successor write
from the same still-unadopted declared endpoint
```

Therefore:

```text
UI lock after successful write
!=
unique successor constraint
```

and:

```text
UI lock
!=
new edge adoption
```

## Already-successful controller state

If a 29A controller is mounted after it has already successfully persisted one endpoint revision, 29B mounts the control surface already locked and displays that retained successful receipt.

It does not offer another write button merely because the Textual shell itself did not perform the earlier persistence.

## Failure behavior

If UI-specific blank-path validation or the delegated 29A operation fails:

- the status area reports the failure;
- the form remains active;
- no false successful receipt is shown;
- the displayed declared session remains unchanged;
- `controller.last_endpoint_revision` remains governed by 29A's existing success-only update rule;
- no destination is overwritten.

A prior successful 29A result remains retained if a later lower-level call outside this locked UI fails, exactly as established by 29A.

## Display remains the prior declared session

This is the central 29B boundary.

After a successful UI write:

```text
shell.research_session
shell.research_presentation
ResearchRevisionEdgeSequenceDetail.presentation
controller.loaded
controller.presentation
controller.declared_endpoint
```

all continue to represent the exact pre-write declared session.

29B does not:

- append the successor to the displayed sequence;
- rewrite the 26B declaration;
- relink a new 26C segment;
- create a new 28A session;
- label the successor latest/current/head;
- infer that the successor should be adopted.

The only new visible state is the durable-write receipt and locked form.

Thus:

```text
successful UI mutation
!=
displayed-session mutation
```

## Workspace independence remains intact

The research controller remains independent of Repository Zero Workspace provenance.

Workspace runtime reruns may update Workspace runtime evidence while retaining the exact same research controller and exact same research session presentation.

Therefore:

```text
Workspace runtime mutation
!=
research mutation
```

and:

```text
same Textual shell
!=
shared provenance chain
```

remain explicit.

## No new persistence or discovery

29B introduces no new persistence schema and performs no:

- browser acquisition;
- directory scan;
- digest search;
- path discovery;
- automatic predecessor location;
- automatic relinking;
- declaration rewriting;
- sequence rewriting;
- chronology inference;
- branch selection;
- head selection;
- semantic support analysis;
- citation validation;
- source-authenticity validation.

The mutation path remains exactly:

```text
Textual explicit inputs
→ 29A controller
→ public 25A
→ public 25B
→ durable successor result
```

## Falsifiability

Focused tests prove:

1. a valid `research_controller=` mounts its exact retained 28A session plus endpoint revision controls;
2. the controller form cannot be mixed with complete-session or split read-only research inputs;
3. the existing read-only `research_session=` form remains control-free;
4. one successful UI write preserves exact multiline/Unicode human wording, writes a durable successor, reports its identity/location, locks the controls, and leaves the exact declared session unadopted;
5. a wrong explicitly supplied predecessor edge rejects without false success or UI lock;
6. blank explicit path input rejects before persistence without false success;
7. an occupied destination preserves existing bytes and leaves the form active;
8. a controller that already has a successful 29A result mounts the UI already locked with that exact receipt;
9. a Repository Zero Workspace runtime rerun preserves the exact research controller and exact research session;
10. a deliberately forged retained controller presentation is rejected before a mutating shell can mount.

## Scope

29B changes only:

- `src/pyxis/ui/chromium_research_endpoint_revision_textual.py`;
- `src/pyxis/ui/research_workspace_shell.py`;
- focused 29B UI tests;
- this milestone document.

It does not change:

- `src/pyxis/ui/workspace_shell.py`;
- 29A controller semantics;
- 28A presentation semantics;
- 27A/27C presentation semantics;
- existing persistence schemas;
- Chromium acquisition;
- Repository Zero compiler/RIR/runtime/export/measurement behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 29B proves

Successful 29B establishes only:

> From one coherent 29A research-session controller, the normal Pyxis Textual shell can display the controller's exact existing complete research-session presentation, accept explicit multiline human rationale wording plus explicit predecessor/destination paths, invoke the existing 29A governed declared-endpoint successor write, display the exact durable-write identity as a non-adoption receipt, and lock that mounted mutation form after one successful write while leaving the displayed declared session unchanged.

## What 29B does not prove or do

29B does **not** establish:

- latest/current revision;
- global or canonical head;
- unique successor;
- absence of sibling successors;
- branch semantics;
- automatic adoption;
- redeclaration;
- sequence extension;
- chronology;
- complete ancestry;
- semantic improvement;
- source authenticity;
- citation authority;
- semantic support;
- Workspace provenance;
- automatic file discovery.

The core boundary is:

```text
explicit UI successor write
→ durable edge + receipt
!=
adopted/current/head displayed research session
```
