# Milestone 50E — prove bare-passage changed-basis shell adoption

Decision: **D259**  
Issue: **#246**

## Purpose

50A–50D progressively established that one bare exact-range selection can be:

```text
saved without interpretation
→ retained in working_set.v2
→ presented without a fake note
→ preserved through changed-basis preparation
→ referenced by transition-v1
→ rooted by root-v1
→ bridged through edge-v1
→ continued through ordinary edge lineage
```

50E asks whether the already-existing first changed-basis product surface actually inherits those capabilities.

The milestone begins with no production-code change.

## Concrete researcher action

The researcher starts from one ordinary governed session and one already-loaded bare exact-range selection.

The actual product path is:

```text
ordinary governed session
+ exact bare selection candidate
→ 44A prepare changed basis
→ 44B persist/relink transition
→ 44C persist/relink root
→ 44D persist/relink first post-root edge
→ 44E explicitly adopt changed-basis governed session
→ ordinary governed revision remains available
```

This is the first proof in the 50-series that the bare-passage state crosses the complete existing first changed-basis shell workflow rather than only application/persistence boundaries.

## Why this is proof-only

The existing 44B–44E wrappers consume exact typed results:

- 44B consumes the exact 33A preparation;
- 44C consumes the exact 44B transition result;
- 44D consumes the exact 44C root result;
- 44E consumes the exact 44D edge result.

None independently declares a working-set/note version.

Likewise 35A adoption starts from the exact loaded root-v1 and explicit first edge-v1 source. It persists/relinks the existing root-started sequence declaration and constructs the existing governed controller.

Therefore no production defect was demonstrated by static review.

The correct next action is executable falsification of that inherited behavior.

## Executable product crossing

The 50E test creates one real loaded bare exact-range selection and supplies it as the changed-basis candidate to:

`create_first_changed_basis_session_adoption_research_session_shell(...)`

The bare member sidecar is removed before durable preparation.

The test then drives the real Textual controls through the existing helper path used by the historical 44A–44D product tests.

### Candidate state

Before persistence, the candidate surface must show:

```text
Candidate member 1: exact_range_selection
Human note: none attached — saved source passage only
```

and must not display Python `None` as human content.

### 44A

Existing changed-basis preparation must produce:

```text
research_working_set.v2
+
research_working_set_note.v2
```

The exact bare loaded object must be the appended member.

### 44B

The existing first-transition UI must persist and freshly relink:

`research_session_working_set_transition.v1`

### 44C

The existing first-root UI must persist and freshly relink:

`research_session_working_set_transition_revision_root.v1`

### 44D

The existing first-root-edge UI must persist and freshly relink:

`research_working_set_note_revision_edge.v1`

and the edge endpoint working set must still retain the exact bare selection object.

### 44E / 35A

Only after explicit adoption must the shell replace its active governed controller.

The existing 35A path must persist/relink:

`research_working_set_note_revision_edge_sequence.v1`

with the exact root-v1 start and exact first edge-v1.

The adopted controller's declared endpoint must be the exact 44D edge.

Its working set must still contain the exact bare selection object.

The governed presentation must still visibly represent that member as an `exact_range_selection` with no human note attached.

## Post-adoption ordinary action

After explicit adoption the test performs one ordinary governed endpoint revision through the existing controls.

This demonstrates that adopting the v2-backed changed basis does not create a product dead end.

It does not itself adopt that new successor; the established ordinary session semantics remain unchanged.

## Sidecar boundary

The bare selection sidecar is deleted before 44A persistence.

The complete shell crossing succeeds from already-loaded application evidence plus the explicit durable files created by each stage.

No browser reacquisition or member-sidecar discovery is introduced.

## Authority boundaries

50E does not strengthen the semantics of any artifact.

The crossing remains:

```text
explicit candidate
→ prepared changed basis
→ explicit transition
→ explicit human root revision
→ explicit ordinary edge
→ explicit shell-local adoption
```

No stage implies source support, citation validity, chronology, global branch authority, or automatic adoption.

## Stop boundary: 35B

50E proves only in-process 35A adoption.

It does not prove that a new process can reconstruct and launch the v2-backed root-started session through the later 35B restart/re-entry product.

That remains a separate researcher-action review.

Likewise 50E does not propagate the v2-backed changed basis through second or third changed-basis epoch products merely because their architecture is related.

## Production-code result

If Repository Zero passes, **50E changes no production code**.

That is a positive architectural result:

> The existing first changed-basis product surface already consumes the generalized application contracts earned by 50B–50D without requiring version-specific UI or product branching.

## Focused falsification

50E proves:

1. the candidate is the exact bare loaded selection;
2. note absence is rendered explicitly and not as `None`;
3. the sidecar may be deleted before 44A persistence;
4. 44A selects working-set/note v2;
5. 44B remains transition-v1;
6. 44C remains root-v1;
7. 44D remains edge-v1;
8. 44E remains sequence-declaration v1;
9. the active controller does not change before explicit adoption;
10. explicit adoption replaces the active controller with the exact changed-basis controller;
11. the adopted endpoint is the exact 44D edge;
12. the adopted endpoint retains the exact bare selection object;
13. the governed UI still renders the bare member as source evidence without a human note;
14. ordinary governed revision remains available after adoption;
15. no bare member sidecar is rediscovered.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50E adds no:

- production application code;
- production UI code;
- durable format;
- automatic adoption;
- 35B fresh-process re-entry proof;
- second/third epoch propagation;
- browser selection creation;
- browser mutation;
- source discovery;
- search/tags/export;
- chronology/current/latest/head authority;
- citation or semantic-support authority.

## Acceptance statement

50E permits only this statement:

> The existing first changed-basis product surface can carry one explicitly supplied bare saved passage from candidate preparation through transition-v1, root-v1, edge-v1, and explicit in-process governed-session adoption while preserving exact member identity and note absence, without any production-code or durable-format change.
