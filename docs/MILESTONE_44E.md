# Milestone 44E — Explicit Changed-Basis Governed-Session Adoption

Decision: D222

## Product question

44D completes one durable local changed-basis lineage:

```text
33B transition
→ 34A changed-basis revision root
→ 34B first ordinary edge
```

That lineage may coexist with continued work on the old-basis governed session. Nothing
through 44D selects either branch as the shell's governed controller.

35A / D181 already proved the next narrow authority boundary at the application layer:

```text
exact loaded 34A root
+ explicit ordered edge files beginning with the 34B bridge
→ root-started 26A sequence
→ existing 26B durable declaration
→ fresh 26C declaration relink
→ existing 29A governed controller
```

44E productizes that exact boundary.

## Decision

44E adds one explicit action:

> Adopt this exact changed-basis root + first-edge lineage as this shell's governed
> research session.

The action is deliberately different from 44A–44D. Those milestones create historical
artifacts while leaving the mounted governed controller unchanged. 44E is the first
step that intentionally replaces the shell's active controller.

```text
44A prepare
44B transition
44C root
44D first ordinary edge
44E explicit shell-local adoption
```

## Two explicit durable locators

44E asks for exactly two paths, both blank by default:

1. the current durable file for the exact first post-root edge;
2. the no-overwrite destination for the root-backed sequence declaration.

There is intentionally no root path input.

The 34A root is already the exact loaded application record retained through the
44C/44D product result. 35A uses that object as the explicit sequence starting record.
Asking for another root path would add a persistence/re-entry question that 35A does
not require.

The 44D edge output path is displayed only as location receipt context. It is never
copied into the input, searched, discovered by digest, or treated as current authority.
A moved-but-identical edge works only when the researcher supplies its new path.

## Bounded application composition

`chromium_research_first_changed_basis_session_adoption.py` composes only existing
proven boundaries:

```text
ChromiumResearchFirstChangedBasisRootEdgeResult
→ load_chromium_research_working_set_note_revision_edge_sequence
→ persist_chromium_research_working_set_note_revision_edge_sequence
→ load_chromium_research_working_set_note_revision_edge_sequence_declaration
→ ChromiumResearchSessionController
```

The returned `ChromiumResearchFirstChangedBasisSessionAdoptionResult` retains:

- the exact 44D edge result;
- the freshly root-started 26A sequence;
- the existing-format 26B declaration persistence evidence;
- the freshly reconciled 26C declaration;
- the ordinary governed controller.

The application boundary checks that the retained 44D root and edge identities remain
coherent, that the explicit edge source freshly reconstructs the exact 44D edge, and
that the final controller endpoint is that same edge identity and human wording.

## No new durable format

The declaration remains:

```text
pyxis.chromium.research_working_set_note_revision_edge_sequence.v1
```

Its starting predecessor is the existing 34A root format + exact root-record SHA-256.
Its member is the existing 24B edge format + exact first-edge SHA-256.

The declaration contains no filesystem paths, timestamps, branch labels, revision
numbers, current/head flags, or semantic judgments.

## Dedicated shell boundary

`FirstChangedBasisSessionAdoptionResearchSessionShell` subclasses only the dedicated
44D shell.

Existing base, root-backed, second-epoch, and third-epoch shells are unchanged. Later
lineage families therefore do not acquire a generic branch-adoption action by class
symmetry.

44E controls mount only after a newly successful exact 44D edge result.

The controls show:

- exact root identity;
- exact first-edge identity;
- exact first-edge human rationale;
- historical edge output location as receipt context;
- two blank explicit durable-locator inputs;
- an adoption button whose text says that the active governed branch will change.

## Proof before promotion

44E constructs the entire 35A result before changing shell state.

```text
old controller remains mounted
→ build fresh 26A sequence
→ persist 26B declaration
→ fresh 26C relink
→ construct existing controller
→ verify exact 44D endpoint identity
→ lock adoption receipt
→ promote shell state
```

Any evidence/persistence/relink failure therefore leaves the mounted old-basis
controller unchanged.

## Shell-local branch adoption

Successful promotion removes only the currently active governed-session widgets:

- sequence detail;
- endpoint revision controls;
- rollover controls;
- any ordinary restart-plan controls left by the old branch;
- any old rollover success receipt.

It preserves the locked 44A–44E artifact forms as historical receipts.

Then it sets:

```text
research_controller = adopted 35A controller
research_session = adopted controller presentation
research_presentation = adopted sequence presentation
research_working_set_contexts = adopted contexts
research_reentry = None
last_research_rollover = None
last_research_restart_plan = None
```

and mounts fresh ordinary sequence, endpoint-revision, and rollover controls.

The changed-basis candidate's live binding to the old controller is cleared. Completed
preparation/transition/root/edge/adoption result objects remain historical evidence.

## Meaning of adoption

44E means only:

> For this running shell, the researcher explicitly selected this freshly declared
> root-backed segment as the governed session from which future explicit mutations
> will operate.

It does not mean:

```text
shell-local governed controller
=
global current branch
```

and it does not mean:

```text
explicit adoption
=
chronologically latest history
```

The old-basis branch remains durable history and may have continued before adoption.
44E does not erase, invalidate, rank, or globally supersede it.

## Branch coexistence before adoption

A key falsification case is:

```text
persist changed-basis transition/root/first edge
→ continue old-basis session through ordinary 30A rollover
→ later explicitly adopt changed-basis lineage through 44E
```

This is permitted because the changed-basis artifacts are durable historical
relationships independent of the shell's then-mounted old-basis controller.

The 44E button press is the explicit shell-local selection event. Nothing before it
silently retargets the changed-basis lineage to the old continuation or vice versa.

## Ordinary work resumes after adoption

35A already proves that the adopted controller is an ordinary
`ChromiumResearchSessionController` at a standard 24B edge endpoint.

Therefore after 44E:

```text
29A explicit endpoint revision
→ 25A/25B ordinary successor persistence
→ 30A explicit rollover
```

works unchanged.

No root-specific mutation fork is introduced after adoption.

## No fresh-process restart authority

35A deliberately stops before 35B.

44E therefore clears the ordinary re-entry lineage inherited from the old-basis shell
and sets `research_reentry = None` for the adopted session.

It does not create or infer a `ChromiumResearchRootBackedSessionReentryResult`, and it
does not mount restart-plan controls after adoption or after a subsequent ordinary
rollover.

```text
35A / 44E governed session adoption
!=
35B root-backed fresh-process re-entry
```

Restartability remains the next separate authority question.

## Prior art and reuse

Internal prior art is sufficient and decisive for this bounded product step:

- 35A / D181 owns root-started sequence dispatch, existing declaration persistence,
  fresh declaration reconciliation, and ordinary governed-controller construction;
- 44D / D221 supplies the exact first changed-basis edge product result;
- `ResearchSessionShell` owns ordinary governed sequence/revision/rollover UI behavior;
- 35B remains the distinct fresh-process root-backed re-entry boundary.

The broader external provenance review recorded before 44A remains applicable. 44E
introduces no new provenance model or external subsystem.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Falsifiability

Focused 44E coverage proves:

1. the application boundary creates an existing-format root-backed 26B declaration;
2. the declaration names the exact 34A root identity and exact 44D edge identity;
3. 26C freshly reconciles the declaration against the explicit supplied edge path;
4. a moved-but-identical edge works only through its explicit new path;
5. a wrong edge source rejects before declaration write;
6. the 44E form appears only after exact 44D success;
7. both path inputs begin blank and no root locator exists;
8. candidate root/edge identities and rationale are visible without current/head claims;
9. failed UI adoption leaves the mounted controller unchanged and the form unlocked;
10. successful adoption replaces the active governed controller and session surface;
11. the new controller endpoint is the exact 44D first edge;
12. the adoption form locks and retains a truthful receipt;
13. ordinary endpoint revision and 30A rollover work after adoption;
14. an old-basis rollover before adoption does not invalidate the 44D lineage;
15. successful adoption clears old re-entry/restart authority;
16. no restart-plan controls appear for the adopted root-backed session;
17. the plain 44D shell never gains 44E controls; and
18. mature root-backed and later-epoch shells remain unchanged.

## Non-goals

44E does not add:

- 35B fresh-process root-backed re-entry;
- 35C/35D root-backed checkpoint persistence;
- a fourth evidence-basis epoch;
- generic `epoch[n]` machinery;
- arbitrary-depth ancestry traversal;
- a generic branch selector;
- automatic changed-basis adoption;
- path discovery or digest search;
- chronology or global current/latest/head authority;
- path identity;
- authorship, authenticity, or trusted-time authority;
- semantic-support or citation authority; or
- autonomous research behavior.

## What successful 44E proves

Successful 44E establishes only:

> From one exact successful first changed-basis root-edge product result and one
> researcher-supplied current edge path, Pyxis can freshly reconstruct the existing
> 35A root-started segment, persist and freshly reconcile the existing declaration
> format, construct the existing governed controller at the exact 44D edge endpoint,
> and explicitly promote that controller as this running shell's governed session
> without inventing fresh-process restart authority or any global branch/head claim.
