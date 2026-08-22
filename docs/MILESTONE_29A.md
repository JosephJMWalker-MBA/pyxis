# Milestone 29A — Research Session Declared-Endpoint Revision Controller

Decision: D169

## Product question

28B makes one complete verified research-session presentation directly usable in the Textual shell.

The next practical researcher action is no longer another read-only presentation concern:

```text
"I inspected the bounded evidence and rationale in this declared session.
I want to revise the rationale I am actually continuing from."
```

The already-proven mutation path exists below the session surface:

```text
25A explicit human extension from one loaded general edge
→
25B durable successor in the existing general edge format
```

But a researcher currently has to leave the session abstraction, manually extract the intended loaded edge, invoke 25A, then invoke 25B.

29A adds a narrow application-owned controller for that real workflow.

## Why only the declared endpoint

A loaded 26C segment may contain multiple ordered edge members.

29A deliberately permits revision only from:

```text
the final edge in that explicit caller-declared segment
```

This is called the **declared endpoint**.

It is not called:

- latest revision;
- current revision;
- global head;
- canonical head;
- unique successor location.

Allowing an interior member to be revised through the session controller would silently create a sibling successor relative to later members and would force Pyxis to define branch-selection semantics that have not been earned.

Thus:

```text
declared segment endpoint
!=
global history head
```

and:

```text
interior displayed rationale
!=
authority to branch through the session controller
```

## Public application boundary

29A adds the explicit module:

```text
pyxis.app.chromium_research_session_controller
```

with:

```python
ChromiumResearchSessionController(loaded)
```

where `loaded` is one already-loaded coherent 26C declaration/sequence record.

Construction first reuses the complete 28A presentation boundary.

The controller retains exactly:

```text
loaded
presentation
declared_endpoint
last_endpoint_revision
```

`loaded` is the exact caller-supplied 26C object.

`presentation` is one exact complete 28A session presentation produced from it.

`declared_endpoint` is the exact final loaded edge object in `loaded.sequence.edges`.

`last_endpoint_revision` is initially `None` and becomes the exact result of the most recent **successful** endpoint persistence operation.

## Explicit endpoint revision operation

The controller adds:

```python
persist_declared_endpoint_revision(
    revised_note_text,
    prior_edge_source=...,
    destination=...,
)
```

The caller must explicitly provide:

1. the new human-authored rationale text;
2. the durable file location for the exact declared endpoint edge;
3. the destination for the new successor edge.

29A then composes existing public boundaries:

```text
controller.declared_endpoint
→ public 25A extension
→ public 25B fresh durable predecessor reopening + no-overwrite write
→ endpoint revision persistence result
```

No new persistence schema is introduced.

The successor remains the existing:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

format.

## Result evidence

Successful persistence returns immutable:

```text
ChromiumResearchSessionEndpointRevisionPersistenceResult
```

containing only:

```text
prior_session
extension
persistence
```

`prior_session` is the exact retained 28A presentation.

`extension` is the exact public-25A extension.

`persistence` is the exact public-25B durable write evidence.

The result intentionally has no field for:

- current;
- latest;
- current head;
- adopted revision;
- chronology;
- semantic improvement.

## Persisted successor is not adopted session state

This is the central 29A authority boundary.

After a successful write:

```text
controller.loaded
controller.presentation
controller.declared_endpoint
```

remain the exact same objects as before the write.

The newly persisted successor is **not** automatically appended to the loaded 26C sequence.

The 26B durable declaration is **not** rewritten.

The complete 28A presentation is **not** regenerated to include the successor.

Therefore:

```text
durable successor exists
!=
successor is adopted into declared session
```

and:

```text
successful human revision write
!=
current/head selection
```

A later explicit boundary would be required to relink, redeclare, or otherwise adopt that successor into a newly asserted session state.

## Fresh immediate-predecessor requirement remains intact

29A does not weaken 25B.

The caller must supply the durable file for the exact declared endpoint retained by the controller.

25B freshly reopens that file against the already-loaded predecessor object and requires its content identity to match the extension's retained endpoint before writing the successor.

Thus:

```text
loaded endpoint object
!=
authority to persist successor without current endpoint file
```

Path remains location, not identity.

A byte-identical endpoint file may be moved and explicitly supplied from another path.

A wrong explicitly supplied edge file rejects.

## Older durable ancestry may be absent

29A inherits the established 25B bounded-durability property.

Once 26C is loaded, older working-set, note, revision, continuation, declaration, and earlier edge files may be deleted.

For this operation, Pyxis requires only:

```text
already-loaded coherent application evidence
+
current durable file for the declared endpoint
+
new destination
```

This does not prove whole ancestry still exists durably.

## Exact human wording

29A delegates revision semantics to public 25A / 22A.

Therefore:

- exact whitespace is preserved;
- Unicode is preserved;
- multiline wording is preserved;
- exact no-op revision is rejected;
- semantic improvement is not inferred.

Thus:

```text
textual change
!=
semantic improvement
```

## Failure state

The controller records `last_endpoint_revision` only after public 25B succeeds.

If 25A or 25B rejects:

- no false successful result is retained;
- a previous successful result, if one exists, remains retained;
- the declared session itself is unchanged.

No-overwrite destination behavior remains owned by 25B.

## No UI mutation yet

29A is an application/controller milestone.

It does not add an edit box or Save button to Textual.

This keeps the direction explicit:

```text
loaded 26C evidence
→ 29A controller
→ existing 28A presentation
→ existing 28B shell input
```

with a separate explicit mutation path:

```text
29A controller
→ 25A
→ 25B
→ durable successor result
```

A later UI milestone may wire a researcher action to this controller, but should not allow presentation-only objects to mutate deep evidence directly.

## Falsifiability

Focused tests prove:

1. controller construction retains the exact 26C loaded object and a complete 28A presentation;
2. `declared_endpoint` is exactly the final edge in the explicit declared sequence;
3. a valid endpoint revision composes 25A and 25B, preserves exact human wording, and the successor can be freshly reopened through 24C;
4. a wrong explicitly supplied endpoint file rejects without false controller success;
5. moving the same endpoint bytes to another explicit path still works, proving path is location rather than identity;
6. exact no-op revision and occupied destination both reject without false success or overwrite;
7. older durable ancestry and declaration files may disappear while the already-loaded state plus exact endpoint file still permit the operation;
8. successful persistence does not mutate/adopt the successor into the loaded declaration, presentation, or declared endpoint;
9. a later failed write does not erase the controller's previously retained successful persistence result;
10. wrong-type or forged loaded state rejects before the controller becomes an application authority;
11. the result surface adds no current/latest/head/adoption field and the explicit module remains importable without package-root broadening.

## What successful 29A proves

Successful 29A establishes only:

> From one already-loaded coherent declared research session, Pyxis can identify the exact final member of that explicit segment and, when the caller supplies new human wording, the exact current durable file for that endpoint, and a destination, compose the existing 25A and 25B boundaries to write one durable successor while retaining the original declared session unchanged.

## What 29A does not prove or do

29A does **not** establish:

- latest/current revision;
- global history head;
- unique successor;
- branch semantics;
- automatic adoption of the successor;
- declaration rewriting;
- sequence rewriting;
- chronology;
- complete ancestry;
- semantic improvement;
- source authenticity;
- citation authority;
- semantic support;
- browser acquisition;
- file discovery;
- digest search;
- directory scanning;
- recursive history traversal;
- Textual mutation controls.

The core boundary is:

```text
declared endpoint
→ explicit durable successor
!=
adopted/current/head session state
```
