# Milestone 34B — Resume Ordinary Revision After Evidence-Basis Change

Decision: D180

## Product question

34A gives the first rationale revision after a changed evidence basis its own durable root.

The next researcher action is ordinary:

> “I revised the rationale once after changing the evidence basis. Now I want to revise it again.”

The problem is that the new lineage must resume ordinary revision behavior **without erasing the fact that it began at a cross-working-set transition**.

34B adds one explicit bridge from the 34A root back into the existing 24B/25A/25B edge lineage.

## Core relationship

```text
33B cross-working-set transition
→ 34A revision root
→ 34B first ordinary 24B edge
→ existing 25A/25B edge revisions
→ existing edge→edge lineage
```

The 34B edge is not a new durable format.

It uses:

```text
pyxis.chromium.research_working_set_note_revision_edge.v1
```

and records the exact 34A root format + root-record SHA-256 as its predecessor identity.

Therefore:

```text
cross-working-set ancestry preserved
+
ordinary edge format resumed
```

does not require treating the transition itself as a normal same-working-set edge.

## Why generic 24C remains unchanged

34A deliberately proved that a loaded root was not accepted by the generic 24C loader.

34B preserves that boundary.

A caller cannot pass a loaded 34A root directly to:

```text
load_chromium_research_working_set_note_revision_edge(...)
```

Instead 34B adds one root-specific bridge loader:

```text
load_chromium_research_session_working_set_transition_revision_root_edge(...)
```

That loader returns the standard:

```text
ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
```

Once that first edge has been loaded, existing ordinary edge APIs can operate on it.

Thus:

```text
34A root
!=
generic 24C predecessor
```

while:

```text
34A root
→ explicit 34B bridge
→ standard loaded 24B edge
```

is now supported.

## In-memory extension

34B adds:

```text
create_chromium_research_session_working_set_transition_revision_root_edge_extension(...)
```

The returned frozen record retains:

- the exact loaded 34A root;
- one public-22A revision whose prior note is exactly the 34A root endpoint note.

The revised note retains the exact changed working-set object.

Exact textual no-ops remain rejected by public 22A.

No files are read at this boundary.

## Durable persistence

34B adds:

```text
persist_chromium_research_session_working_set_transition_revision_root_edge_extension(...)
```

Inputs are deliberately narrow:

```text
extension
root_source
destination
```

Before writing, Pyxis:

1. re-establishes the loaded 34A root in memory;
2. freshly verifies the caller-supplied current root file;
3. requires exact root format + root-record SHA-256 match;
4. writes one existing-format 24B edge naming that root identity as predecessor.

Older 33B transition and evidence-basis files are not reopened.

This follows the local-current-predecessor principle already used by repeated ordinary edges:

```text
fresh current predecessor identity
!=
recursive ancestry replay
```

The 34A root remains the durable ancestry carrier for the earlier basis change.

## Existing 24B verifier

The existing 24B file-local verifier now structurally accepts one additional predecessor format:

```text
pyxis.chromium.research_session_working_set_transition_revision_root.v1
```

That change proves only that an edge file may structurally name a root predecessor.

File-local verification still does not prove that the referenced root exists, is available, or coherently relinks.

Therefore:

```text
supported predecessor format
!=
verified predecessor relationship
```

## Root-specific edge loading

The 34B loader:

1. freshly verifies the 24B edge file;
2. re-establishes the supplied loaded 34A root in memory;
3. requires exact root format + root-record SHA-256 match;
4. reconstructs the edge revision over exactly the root endpoint note;
5. returns the normal loaded-edge record type.

The returned edge retains the exact root object as `predecessor`.

This preserves the local ancestry seam inside the standard edge object.

## Ordinary 25A/25B continuation

Public 25A already consumes a loaded edge, so no 25A semantic change is needed.

25B previously reopened every prior edge through generic 24C. The first post-root edge cannot be reopened that way because its predecessor is a 34A root.

34B therefore adds one narrow dispatch inside 25B:

```text
prior edge predecessor is 34A root
→ reopen prior edge through 34B root-edge loader

otherwise
→ reopen prior edge through existing public 24C
```

After 25B writes the next edge, that new edge's predecessor is an ordinary edge.

From that point onward, the existing edge→edge reopen path applies with no root-specific dispatch.

Thus:

```text
root-specific bridge needed once
!=
new parallel revision system
```

## Sequence authority remains unchanged

34B does not make a 34A root a 26A sequence start.

The generic sequence loader continues to accept only its previously supported starting predecessor categories.

A researcher may first create/load the 34B root-backed edge and then use ordinary edge-based sequence machinery from an edge boundary.

Whether a declared sequence should be allowed to start *at the root itself* remains a separate authority decision.

Therefore:

```text
root-backed ordinary edge support
!=
root-as-sequence-start authority
```

## Path semantics

A moved byte-identical root file remains usable when its new path is supplied explicitly.

No path is persisted as identity.

```text
path = location, not identity
```

continues to hold.

## Human semantics

All revised rationale text remains caller-authored and verbatim.

34B does not infer:

- semantic improvement;
- evidentiary support;
- correctness;
- chronology;
- authorship identity;
- current/latest/canonical head;
- uniqueness of successor;
- complete history.

## Falsifiability

Focused 34B coverage proves:

1. the root-edge extension uses the exact 34A endpoint note;
2. the revised note retains the exact changed working set;
3. exact textual no-ops reject;
4. persistence writes the existing 24B edge format;
5. the durable edge records the exact 34A root format + SHA-256;
6. a wrong current root file rejects without writing;
7. a moved byte-identical root file works only via its explicit new path;
8. edge destination remains no-overwrite;
9. root-specific loading returns the standard loaded-edge type;
10. the loaded first edge retains the exact root object as predecessor;
11. a genuinely different root identity rejects relinking;
12. generic 24C still rejects a root directly;
13. 26A still rejects a root as sequence start;
14. 25A/25B can continue from the first root-backed edge;
15. the next edge can be loaded by ordinary public 24C;
16. a further edge uses the ordinary edge→edge persistence/relink path with no root-specific predecessor.

The focused test module contains 12 collected tests; several tests cover multiple related assertions.

## Scope

34B adds:

- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root_edge_extension.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root_edge_extension_persistence.py`;
- `src/pyxis/app/chromium_research_session_working_set_transition_revision_root_edge_load.py`;
- `tests/test_app_chromium_research_session_working_set_transition_revision_root_edge.py`;
- this milestone document.

34B narrowly modifies:

- `chromium_research_working_set_note_revision_edge_persistence.py` so 24B verification structurally recognizes the 34A root predecessor format;
- `chromium_research_working_set_note_revision_edge_load.py` so standard loaded edges can retain/validate root ancestry internally while generic public 24C still rejects roots directly;
- `chromium_research_working_set_note_revision_edge_extension_persistence.py` so 25B can reopen the first root-backed prior edge through the explicit 34B loader exactly once.

34B does not change:

- 33B transition semantics;
- 34A root persistence or relinking;
- generic 24C public input categories;
- 26A sequence-start categories;
- sequence declarations;
- session adoption;
- rollover/re-entry/restart behavior;
- CLI;
- Textual UI;
- Chromium acquisition;
- Repository Zero;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 34B proves

Successful 34B establishes only:

> From one coherent loaded 34A cross-working-set revision root and its explicitly supplied current durable root file, Pyxis can accept one additional human rationale revision, persist it in the existing 24B edge format with the exact root identity as predecessor, relink it through a dedicated one-time bridge into the standard loaded-edge type, and then resume the existing ordinary edge revision path without erasing the basis-change ancestry or granting sequence/head/semantic authority.
