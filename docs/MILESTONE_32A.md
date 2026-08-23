# Milestone 32A — Explicit Continuation Re-entry Plan

Decision: D175

## Product question

31B made the governed research workflow directly launchable:

```text
pyxis research-shell --plan research-session.plan.json
```

Inside that standalone shell, the researcher can now complete the full governed
interaction loop:

```text
inspect
→ revise declared endpoint
→ persist successor
→ explicitly choose continuation
→ create new declaration
→ mount new continuation session
```

That exposed the next real workflow failure.

After a successful continuation rollover, the locator plan used to launch the
process still describes the **prior** declared session.

If the researcher exits immediately, the new continuation is durable, but the
researcher does not yet have a proven launch plan for it.

Before 32A, recovering that new continuation after process exit required manually
rewriting the 31B locator JSON.

32A closes that gap at the application boundary.

## Core distinction

A successful 30A rollover proves:

```text
chosen prior declared endpoint
+
explicit chosen successor edge
+
new one-edge declaration
→
new governed continuation controller
```

It does **not** prove that an existing 31B locator plan can reopen that continuation.

Therefore:

```text
chosen continuation
!=
restartable continuation
```

32A earns the second state explicitly.

## New public module

32A adds:

```text
pyxis.app.chromium_research_session_continuation_reentry_plan
```

with:

```text
ChromiumResearchSessionContinuationReentryPlanResult
ChromiumResearchSessionContinuationReentryPlanError
persist_chromium_research_session_continuation_reentry_plan(...)
```

The operation accepts:

```text
one prior 31A re-entry result
+
one explicit 30A rollover result
+
current explicit successor-edge location
+
current explicit continuation-declaration location
+
explicit no-overwrite destination for the next locator plan
```

No path is discovered.

No newest declaration is selected.

No sibling successor is enumerated.

## Why the prior re-entry result matters

The prior 31A result retains the exact caller-owned locator lineage that successfully
reconstructed the prior session.

That includes:

```text
working-set member capture/note locations
20B working-set location
21B working-set-note location
22B revision location
23B continuation location
ordered predecessor-edge locations
ordered declared-edge locations
prior declaration location
```

32A does not recreate those paths by inspecting loaded evidence.

It starts from the explicit locator plan the caller previously supplied.

Thus:

```text
loaded evidence
!=
permission to invent historical file locations
```

## Continuation locator transformation

Suppose the prior launch plan represents:

```text
23C base
→ v4
→ declaration start
→ v5
→ v6
```

with:

```text
starting_predecessor_edge_sources = [v4]
declared_edge_sources = [v5, v6]
```

The researcher explicitly writes and adopts:

```text
v6 → v7
```

30A creates a new declaration whose starting predecessor is exact v6 and whose sole
declared member is exact v7.

The next restart plan therefore becomes:

```text
starting_predecessor_edge_sources = [v4, v5, v6]
declared_edge_sources = [v7]
declaration_source = new v7 declaration
```

That transformation is structural, not semantic.

The old declared segment moves into the explicit path sequence required to
reconstruct the new declaration's starting predecessor.

The new declared segment contains only the explicitly chosen successor.

Therefore:

```text
prior declared member
→ predecessor locator for the new declaration
```

means only:

> this path is now needed to rebuild the new declaration's explicit starting
> predecessor from the durable 23C base.

It does not mean that Pyxis discovered a complete history.

## No history upgrade

The generated plan remains a locator plan.

It does not become:

- a revision graph;
- a complete ancestry manifest;
- a branch index;
- a chronology;
- a latest pointer;
- a canonical-head record;
- an evidence-strength record.

The transformation proves only enough explicit ordered locations to reconstruct the
chosen continuation declaration from the same durable base.

Thus:

```text
longer explicit predecessor locator sequence
!=
complete history
```

## Current locations are explicit again

30A requires the caller to supply the successor edge and continuation declaration
locations during rollover.

Those files may later move.

32A therefore does not assume that the paths retained during 30A remain current.

The caller supplies again:

```text
successor_edge_source
continuation_declaration_source
```

These are current locations only.

If the exact durable bytes have moved, the caller can supply the new locations.

A focused test performs:

```text
successful rollover
→ move successor edge
→ move continuation declaration
→ supply both new locations to 32A
→ fresh restart proof succeeds
```

Therefore the established rule survives:

```text
path = location, not identity
```

## No stale-path privilege

The inverse is equally important.

A path remembered by an earlier operation is not privileged simply because Pyxis
used it once.

If the caller supplies a path that no longer contains the required bytes, fresh
re-entry fails.

32A does not search nearby locations for a replacement.

## Fresh proof before write

32A does not persist the transformed locator document immediately.

It first constructs the next in-memory 31A plan and runs:

```text
reenter_chromium_research_session(next_plan)
```

That fresh re-entry must succeed from durable bytes.

Then the newly reconstructed complete research-session presentation must equal the
already-earned 30A continuation presentation.

The freshly reconstructed declared endpoint digest must also equal the chosen
continuation endpoint digest.

Only after those checks pass may the locator document be written.

Therefore:

```text
path-list transformation looked plausible
!=
restart plan accepted
```

Instead:

```text
explicit transformed locations
+
fresh 31A reconstruction
+
exact continuation presentation agreement
→
eligible locator-plan persistence
```

## Failure occurs before plan persistence

If any required durable artifact has changed since the prior process state was
established, fresh 31A re-entry rejects before the new plan document is written.

A focused test performs:

```text
successful prior re-entry
→ successful v7 rollover
→ tamper prior v5 durable edge
→ request continuation restart plan
→ fresh re-entry fails
→ no plan document is created
```

This is intentional.

The fact that an earlier process once accepted v5 does not make its later bytes
acceptable for restart.

Thus:

```text
prior successful loaded state
!=
future restart authority
```

## Wrong sibling rejection

The researcher may create multiple valid successors from the same prior endpoint
through lower-level programmatic use.

32A does not choose among them.

If rollover selected successor A but the caller supplies successor B when building
the restart plan, the fresh declaration reconciliation fails.

No locator plan is written.

Therefore:

```text
valid sibling successor
!=
chosen continuation successor
```

## Wrong or stale declaration rejection

Likewise, a valid older declaration cannot substitute for the explicit continuation
declaration created by 30A.

The transformed plan is freshly reconciled through the established 26C boundary.

A stale declaration therefore rejects even when all referenced edges are themselves
valid durable records.

## Equivalent prior re-entry objects

Process restart naturally creates new Python objects.

32A therefore does not require the prior 31A controller object and the 30A
`prior_controller` object to be the same object instance.

It requires exact declared-session coherence:

```text
complete presentation equality
+
declaration content identity equality
+
declared endpoint content identity equality
```

A focused test freshly re-enters the same prior durable plan twice, performs rollover
from one controller, and successfully creates the continuation restart plan using
the other equivalent re-entry result.

This preserves:

```text
Python object identity
!=
durable research-session identity
```

while still rejecting a locator lineage for a genuinely different declared session.

## Repeatable restart lineage

32A is designed to compose across multiple explicit continuation choices.

Example:

```text
launch plan for v5,v6
→ explicit rollover to v7
→ persist v7 restart plan
→ explicit rollover from live v7 to v8
→ persist v8 restart plan
```

The second generated plan has:

```text
starting predecessor paths
=
original predecessor paths
+ original declared paths
+ v7
```

and:

```text
declared paths = [v8]
```

A focused test proves this repeated transformation while the live controller and
freshly reconstructed restart controller remain distinct but presentation-coherent.

No global head is introduced.

## Locator-plan document persistence

31B added strict decoding of:

```text
pyxis.chromium.research_session_reentry_locator_plan.v1
```

32A adds the matching no-overwrite writer:

```text
persist_chromium_research_session_reentry_plan_document(...)
```

The persisted document retains the exact 31B schema.

No new fields are added.

It still contains only:

- member family labels;
- explicit source locations;
- explicit ordering;
- the locator-plan format marker.

It still contains no:

```text
sha256
latest
current_head
canonical_head
timestamp
complete_history
```

## Plan-document write is no-overwrite

Locator plans describe explicit researcher choices.

32A does not silently replace an older launch plan.

The destination is created with no-overwrite semantics.

If it already exists, persistence fails and the previous bytes remain untouched.

This keeps old operational choices inspectable rather than silently mutating their
meaning.

## Relative path serialization

The writer may serialize a path relative to the plan document only when the target
is inside the document directory tree.

For example:

```text
session/
  research.plan.json
  capture-a.json
  v7-edge.json
  v7-declaration.json
```

can use simple descendant-relative paths.

If an artifact lives outside the plan directory tree, Pyxis writes its explicit
absolute location instead.

Pyxis does not synthesize parent traversal such as:

```text
../../somewhere/file.json
```

This is an operational clarity rule only.

It creates no stronger identity claim.

## Plan persistence does not verify evidence

The generic document writer itself performs no evidence reads.

It validates only that the supplied object is a structurally valid 31A locator plan
and writes the strict 31B JSON shape.

A focused test persists and reloads a valid locator plan whose referenced files do
not exist.

That is correct because:

```text
plan serialization
!=
evidence verification
```

The higher-level 32A continuation operation is the boundary that deliberately runs
fresh 31A verification before using that writer.

## Separation of responsibilities

The resulting architecture is:

```text
31B plan document loader/writer
    operational serialization only

31A re-entry
    fresh durable verification/relinking authority

30A rollover
    explicit continuation adoption authority

32A continuation-plan operation
    explicit lineage transformation
    + fresh 31A proof
    + no-overwrite operational persistence
```

No layer takes over another layer's authority.

## Falsifiability

Focused tests prove:

1. a locator-only plan document can be persisted and loaded back to the exact plan;
2. descendant paths may be serialized relatively without synthetic `..` traversal;
3. plan document persistence is no-overwrite;
4. the persisted document contains no identity/head/chronology registry fields;
5. generic plan persistence does not read referenced research artifacts;
6. a forged plan structure rejects before document creation;
7. one successful 30A rollover becomes a freshly verified restart plan whose fresh presentation equals the chosen continuation;
8. the old declared-edge paths move into the new explicit predecessor path order exactly;
9. all source-evidence/member locator choices remain unchanged;
10. moved successor and declaration files work only when their new locations are explicitly supplied;
11. a wrong sibling successor rejects before plan write;
12. a wrong or stale declaration rejects before plan write;
13. tampered prior durable lineage rejects even after rollover had previously succeeded;
14. an existing plan destination is never overwritten;
15. an equivalent fresh prior re-entry object can supply the locator lineage without Python object-identity privilege;
16. a mismatched prior declared session rejects;
17. repeated v7 then v8 rollovers produce a repeatable explicit restart-locator lineage without global-head state.

## Scope

32A changes only:

- `src/pyxis/app/chromium_research_session_reentry_plan_document.py` to add strict no-overwrite persistence;
- new `src/pyxis/app/chromium_research_session_continuation_reentry_plan.py`;
- focused application tests for both boundaries;
- this milestone document.

32A does not change:

- 31A evidence re-entry semantics;
- 31B CLI launch semantics;
- 31B standalone shell behavior;
- 30A/30B continuation declaration semantics;
- 29A/29B endpoint revision semantics;
- any research evidence persistence format;
- Chromium acquisition;
- Repository Zero Workspace behavior;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 32A proves

Successful 32A establishes only:

> Given one explicit prior re-entry locator lineage and one already-earned explicit
> continuation rollover, Pyxis can accept current explicit locations for the chosen
> successor and continuation declaration, transform the prior locator lineage into
> the exact next re-entry plan, freshly prove that plan reconstructs the same chosen
> continuation session, and persist a new no-overwrite locator-only launch document.

It does not prove complete history, chronology, source authenticity, semantic
support, citation authority, branch uniqueness, latest/current/head status, or a
canonical global research state.

## Next product pressure

Once 32A is earned, the standalone shell can safely expose one explicit post-rollover
action:

```text
Save restart plan for this continuation
```

That future UI step should require an explicit destination and should use the exact
31A re-entry result that launched the current lineage plus the exact 30A rollover
result just chosen.

The UI should not silently overwrite the launch plan and should not infer a default
"current session" file.
