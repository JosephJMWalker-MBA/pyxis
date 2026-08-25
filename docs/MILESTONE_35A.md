# Milestone 35A — Root-Backed Declared Session Adoption

Decision: D181

## Product question

34B proves that one ordinary 24B revision edge may explicitly follow a 34A
cross-working-set revision root through one root-specific bridge, after which ordinary
edge-to-edge revision behavior resumes.

34B deliberately leaves one authority ungranted:

```text
34A root
!=
26A sequence start
```

That prevents a changed-evidence-basis lineage from entering the existing durable
26B/26C declared-session machinery even after the first root-backed ordinary edge has
been proven.

35A asks the narrow question:

> Given one exact loaded 34A root and one or more explicit durable ordinary edges whose
> first member was created from that root through 34B, may the researcher explicitly
> declare that root as the starting predecessor of one bounded ordered revision
> segment and use the existing governed session controller from the segment endpoint?

35A answers **yes**, with one narrow dispatch rule.

## Core relationship

```text
33B cross-working-set transition
→ 34A revision root
→ 34B first ordinary edge
→ 35A explicit root-started 26A sequence
→ existing 26B durable declaration
→ existing 26C declaration relinking
→ existing 28A presentation
→ existing 29A governed session controller
→ existing ordinary 29A/30A revision + rollover
```

35A does not create a new sequence format, declaration format, controller type, or
revision format.

## One-time root dispatch

Public 26A now accepts one additional explicit starting-predecessor category:

```text
ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
```

When that category is supplied:

```text
sequence member 0
→ public 34B root-specific edge loader

sequence member 1+
→ existing public 24C loader
```

Thus:

```text
root as explicit sequence start
!=
root as generic 24C predecessor
```

Generic public 24C remains unchanged.

## Durable declaration

The existing 26B declaration format remains:

```text
pyxis.chromium.research_working_set_note_revision_edge_sequence.v1
```

35A allows its starting-predecessor reference to use the already-established 34A root
format:

```text
pyxis.chromium.research_session_working_set_transition_revision_root.v1
```

No root path is persisted. The declaration records only the root format and exact
root-record SHA-256, followed by the ordered standard edge identities.

Before persistence, Pyxis re-establishes the loaded root relationship in memory and
rechecks the retained root verification JSON and self-integrity exactly as 26B already
does for its older starting-predecessor categories.

Therefore:

```text
root content identity recorded
!=
root file discovered
```

and:

```text
root self-integrity
!=
source authentication or chronology
```

## Fresh declaration relinking

Public 26C now accepts the same explicit loaded 34A root as a starting predecessor.

The caller still supplies:

- the already-loaded starting record;
- every edge file in exact order; and
- the declaration file.

26C freshly verifies the declaration, delegates the explicit sequence to public 26A,
and compares the observed root + edge content identities to the durable declaration.

A wrong root cannot relink the first edge merely because its type is supported.

## Governed session adoption

Once the root-started declaration is freshly loaded, no new controller semantics are
needed.

The existing `ChromiumResearchSessionController` consumes the standard loaded 26C
record, and its declared endpoint remains the final ordinary edge in the explicit
segment.

The existing 28A/27A/27C presentation path also remains downstream of that loaded
segment. The presentation may display the 34A root format/content identity as the
segment start, but it does not present the root as a globally current history root.

From that endpoint, ordinary governed behavior resumes unchanged:

```text
29A explicit endpoint revision
→ 25A/25B ordinary edge
→ 30A explicit continuation rollover
```

The successful 35A path therefore enters the existing governed in-process lifecycle
without inventing a changed-basis controller fork.

## What 35A deliberately does not solve

35A does **not** yet extend the 31A/32A/32B fresh-process re-entry-plan schema.

The current 31A plan reconstructs a 23C base and then an optional ordinary edge prefix
before loading a declaration. A 34A root requires additional explicit durable
locators for the 33B changed-basis transition and the 34A root itself.

Smuggling those locators into the old plan would be a separate persistence/orchestration
authority change.

Therefore:

```text
root-backed declared session in current process
!=
fresh-process root-backed re-entry plan
```

That becomes the next explicit product question rather than an implicit side effect of
35A.

## Authority boundaries

35A does not infer or claim:

- global current/latest/canonical head;
- complete history;
- chronology;
- branch identity;
- unique successor;
- semantic improvement;
- evidentiary support for human rationale;
- source authenticity;
- citation authority;
- path identity;
- directory or digest discovery;
- automatic evidence-basis adoption;
- automatic session rollover; or
- fresh-process restartability for the root-backed session.

The researcher explicitly supplies the root and every ordered edge used by 26A/26C.

## Falsifiability

Focused 35A coverage proves:

1. public 26A accepts one exact loaded 34A root as an explicit starting predecessor;
2. the first sequence edge retains that exact root object as predecessor;
3. a first edge from a genuinely different root rejects at sequence position zero;
4. public 26B persists the exact root format + root-record SHA-256 as the starting
   predecessor identity;
5. public 26B still persists only standard 24B edge identities as members;
6. public 26C freshly relinks the root-started declaration from explicit supplied
   evidence;
7. the resulting standard loaded declaration can become an existing 29A governed
   session controller;
8. 28A presentation preserves the root format as the declared segment start without
   adding head semantics;
9. the governed root-backed session can persist another ordinary 29A endpoint revision;
10. existing 30A rollover can explicitly adopt that ordinary successor with no
    root-specific dispatch;
11. no new durable sequence/declaration/controller format is introduced; and
12. generic public 24C remains unchanged.

## Scope

35A modifies only:

- `chromium_research_working_set_note_revision_edge_sequence_load.py`;
- `chromium_research_working_set_note_revision_edge_sequence_persistence.py`;
- `chromium_research_working_set_note_revision_edge_sequence_declaration_load.py`;
- focused 35A tests; and
- this milestone document.

35A does not change:

- 33A preparation semantics;
- 33B transition semantics;
- 34A root creation/persistence/relinking;
- 34B root-edge creation/persistence/relinking;
- generic 24C public inputs;
- sequence/declaration durable formats;
- `ChromiumResearchSessionController` behavior;
- 29A endpoint revision behavior;
- 30A rollover behavior;
- 31A re-entry-plan behavior;
- 32A/32B restart-plan behavior;
- CLI;
- Textual UI;
- Chromium acquisition;
- research-control-plane state; or
- Repository Zero.

## What successful 35A proves

Successful 35A establishes only:

> From one exact already-loaded 34A cross-working-set revision root and one explicit
> ordered list of durable ordinary edge files beginning with the already-earned 34B
> root-backed edge relationship, Pyxis can relink and persist an existing-format
> declared revision segment whose explicit start is that root, freshly reconcile the
> declaration to the same root and edge identities, and enter the existing governed
> in-process research-session controller at the ordinary edge endpoint without
> erasing the evidence-basis-change ancestry or granting global history/head/semantic
> authority.
