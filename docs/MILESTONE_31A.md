# Milestone 31A — Explicit Durable Research-Session Re-entry

Decision: D173

## Product question

Milestones 29A through 30B complete a governed in-process research loop:

```text
inspect
→ revise declared endpoint
→ persist successor
→ explicitly adopt one successor into a new declaration
→ continue researching
```

That loop still leaves one practical failure:

```text
"I close Pyxis.
I come back tomorrow.
Can I reconstruct the governed research session from durable evidence without hand-building the entire object graph again?"
```

Before 31A, the answer is effectively no at the application boundary.

The durable research files exist, but 26C intentionally requires an already-loaded starting predecessor. Reconstructing that predecessor from a fresh process requires the caller to manually compose the earlier public loaders all the way down to durable captures and human-note sidecars.

31A adds one explicit application orchestration boundary for that fresh-process re-entry.

## Core transition

31A accepts one caller-owned locator plan:

```text
explicit capture + note locations for each working-set member
+
explicit 20B working-set location
+
explicit 21B note location
+
explicit 22B revision location
+
explicit 23B continuation location
+
explicit ordered predecessor-edge locations, possibly empty
+
explicit ordered declared-edge locations
+
explicit 26B declaration location
```

and composes the already-established public boundaries:

```text
16C capture rehydration
→ 17D / 18D / 19D member relinking
→ 23C continuation relinking
→ repeated 24C predecessor-edge relinking
→ 26C declared-segment reconciliation
→ 29A research-session controller
```

The result is a fresh governed research-session controller created without Chromium, directory scanning, digest discovery, or an inferred head.

## New public module

31A adds:

```text
pyxis.app.chromium_research_session_reentry
```

with explicit locator records for the three working-set member families:

```text
ChromiumResearchParagraphNoteReentryLocator
ChromiumResearchExactRangeNoteReentryLocator
ChromiumResearchComparisonNoteReentryLocator
```

plus:

```text
ChromiumResearchSessionReentryPlan
ChromiumResearchSessionReentryResult
ChromiumResearchSessionReentryError
create_chromium_research_session_reentry_plan(...)
reenter_chromium_research_session(...)
```

The module remains explicit rather than broadening the package root.

## The plan stores locations, not evidence identities

The re-entry plan deliberately stores **no SHA-256 digests**.

It stores only:

- durable file locations;
- working-set member family through the typed locator record;
- explicit working-set member order;
- explicit predecessor-edge order;
- explicit declared-edge order.

That is intentional.

The plan is an operational navigation aid, not a second content-identity registry.

Therefore:

```text
re-entry plan path
!=
research evidence identity
```

and:

```text
re-entry plan contents
!=
verification authority
```

Every referenced durable artifact must prove itself again through the established verification and relinking functions.

## Why paths are permitted here

Earlier research persistence deliberately avoided storing paths as durable identity.

31A does not reverse that rule.

A path is useful for a fresh process because the process must be told where the caller currently believes a file is located.

The authority distinction remains:

```text
path = caller-supplied locator
content digest = durable identity evidence inside established artifacts
fresh relinking = application authority to reopen the relationship
```

A moved file therefore remains valid when the caller supplies its new location and its content still satisfies the durable identity relationships.

## Working-set member re-entry

The plan represents each human-selected working-set member explicitly.

### Paragraph-note member

```text
capture_source
note_source
```

31A performs:

```text
16C load durable capture
→ 17D load paragraph note against that exact loaded capture
```

### Exact-range-note member

```text
capture_source
note_source
```

31A performs:

```text
16C load durable capture
→ 18D load exact-range note against that exact loaded capture
```

### Comparison-note member

```text
first_capture_source
second_capture_source
note_source
```

31A preserves source order and performs:

```text
16C load first durable capture
+ 16C load second durable capture
→ 19D load ordered comparison note
```

31A does not swap, search, deduplicate, rank, or semantically compare those sources.

## Fresh verification is required

Re-entry does not trust prior application objects.

Every durable capture and sidecar is freshly reopened from its explicit current path.

This matters across process boundaries.

For example:

```text
process A successfully loaded paragraph-note evidence
→ file later changes or is corrupted
→ process B runs 31A
→ fresh verification rejects
```

The fact that process A once accepted an earlier byte sequence is not authority for process B.

Thus:

```text
previously loaded state
!=
fresh durable re-entry authority
```

## Fresh 23C base reconstruction

After all caller-ordered working-set members are freshly relinked, 31A delegates to public 23C with explicit:

```text
loaded members
working_set_source
prior_note_source
prior_revision_source
continuation_source
```

The existing 20B/21B/22B/23B references re-establish the exact durable working-set and rationale-continuation relationships.

The re-entry plan does not copy those identities.

If the caller supplies the right files in the wrong working-set order, the durable working-set relationships reject.

## Explicit reconstruction of the declaration start

A 26B declaration stores the content identity of its starting predecessor, but deliberately does not store a path to that predecessor.

31A therefore accepts:

```text
starting_predecessor_edge_sources
```

as an explicit ordered tuple.

The freshly loaded 23C continuation is the base.

Each supplied edge is folded in exact order through public 24C:

```text
fresh 23C
→ explicit edge 0
→ explicit edge 1
→ ...
→ explicit declaration starting predecessor
```

The tuple may be empty.

That supports a declaration whose starting predecessor is the 23C continuation itself.

If the declaration instead starts at a later 24C edge and the caller omits that edge, 31A does not search nearby files or use content digests to discover it.

## No predecessor discovery

31A explicitly does not:

- scan a directory;
- search by SHA-256;
- inspect filenames for likely predecessors;
- recursively discover an ancestry chain;
- look for a file beside the declaration;
- infer ordering from timestamps;
- infer ordering from filenames;
- inspect a sibling edge and decide it is preferred.

A test places an exact copy of the required predecessor edge at an obvious nearby filename while deliberately omitting that location from the plan.

Re-entry still fails.

Thus:

```text
available file nearby
!=
caller-selected predecessor
```

## Fresh 26C declaration reconciliation

After the exact declaration starting predecessor has been reconstructed, 31A delegates to public 26C using:

```text
fresh starting predecessor
+
explicit ordered declared-edge paths
+
explicit declaration path
```

26C remains responsible for exact declaration identity/order reconciliation.

31A does not duplicate that logic.

A wrong declared-edge order therefore rejects even if every individual file is valid.

## New governed controller

Only after fresh 26C succeeds does 31A construct:

```text
ChromiumResearchSessionController(loaded_declaration)
```

This reuses the existing 29A controller validation and presentation construction.

The resulting controller is a new in-memory governed session.

It is not automatically current outside this explicit re-entry operation.

## Equivalent presentation, distinct application objects

When every durable byte sequence is unchanged and the caller supplies the same explicit ordering, fresh re-entry should reconstruct an equivalent 28A presentation.

But the objects are newly created:

```text
old loaded declaration object
!=
new loaded declaration object
```

and:

```text
old controller object
!=
new controller object
```

while:

```text
old complete presentation
==
new complete presentation
```

for the same durable evidence.

That is the intended restart property.

## Moved artifacts remain valid

31A tests moving every durable file used by one session into new locations.

The caller then constructs a new plan containing those new paths.

Fresh re-entry succeeds because the durable cross-record content identities still agree.

Therefore:

```text
same old path
!=
required identity
```

and the established rule remains:

```text
path = location, not identity
```

## Loaded state can outlive the re-entry sources

After 31A has successfully reconstructed the controller, the durable source files may disappear and the already-loaded presentation remains usable under the previously established in-memory boundaries.

That does not mean the files still exist.

It means only:

```text
fresh verification happened before successful re-entry
→ application now retains the resulting loaded evidence
```

A later fresh process would again require durable inputs.

## No browser reacquisition

31A starts from durable capture files.

It does not accept a Chromium endpoint, page target, URL to navigate, or browser control object.

The durable capture remains rehydrated 16C evidence, not a new live observation.

Thus:

```text
fresh process re-entry
!=
fresh browser observation
```

## No semantic authority upgrade

Restarting a session does not strengthen any research claim.

The established distinctions survive the process boundary:

```text
source evidence
!=
human selection
!=
human source note
!=
working-set membership
!=
human rationale
!=
semantic support
```

Likewise:

```text
reconstructed session
!=
source authentication
!=
citation authority
!=
claim truth
```

## No latest/head authority

Neither `ChromiumResearchSessionReentryPlan` nor `ChromiumResearchSessionReentryResult` contains fields for:

```text
latest
current
head
canonical_head
complete_history
chronology
```

The caller chooses one exact durable declaration and exact explicit paths required to re-establish it.

Successful re-entry proves only that this chosen declaration can be freshly reconstructed.

It does not compare that declaration with other declarations or successors.

## Why this comes before a CLI command

The installed `pyxis` executable currently exposes only the Repository Zero `run` command.

The research-aware Textual shell is mature, but a CLI cannot responsibly launch it until Pyxis first owns a clean fresh-process application boundary for reconstructing the research controller.

31A establishes that boundary first.

A later milestone can serialize or parse the operational locator plan and connect it to a public shell command without placing relinking logic in `cli.py`.

This preserves the architecture:

```text
CLI parses caller intent
→ application owns re-entry semantics
→ UI consumes application controller
```

rather than:

```text
CLI reimplements research evidence loading
```

## Falsifiability

Focused tests prove:

1. one real durable session built from persisted 16B captures can be freshly reconstructed into a distinct controller with an equivalent complete presentation;
2. changing a sidecar after prior successful loading causes fresh 31A re-entry to reject instead of trusting the old loaded state;
3. moving every durable artifact and explicitly supplying all new locations succeeds;
4. pairing one human-note sidecar with the wrong explicit capture rejects at that exact working-set member;
5. supplying the correct member files in the wrong working-set order rejects through the durable 20B/21B/22B/23B relationships;
6. omitting a required starting-predecessor edge fails even when an identical obvious decoy file is present nearby, proving no discovery;
7. reversing the declared-edge order rejects through fresh 26C reconciliation;
8. a declaration may validly start directly at the freshly reconstructed 23C continuation with zero predecessor-edge locators;
9. after successful re-entry, the loaded controller presentation remains usable after all re-entry source files disappear;
10. plan construction snapshots generator inputs and rejects treating one bare `Path` as an implicit edge-path sequence;
11. plan/result surfaces contain no latest/current/head/discovery authority fields and the module remains explicit.

## Scope

31A adds only:

- `src/pyxis/app/chromium_research_session_reentry.py`;
- focused fresh-process durable re-entry tests;
- this `docs/MILESTONE_31A.md` / D173 document.

31A does not change:

- the Textual UI;
- `pyxis.cli`;
- any research persistence format;
- any existing loader semantics;
- Chromium acquisition;
- 29A mutation semantics;
- 30A rollover semantics;
- 30B UI rollover semantics;
- Repository Zero compiler/RIR/runtime/export/measurement semantics;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 31A proves

Successful 31A establishes only:

> Given one explicit caller-owned plan of current durable file locations and exact ordering sufficient to reconstruct the working-set members, 23C rationale-continuation base, any 24C edges required to reach the chosen declaration start, and the exact declared segment, Pyxis can freshly verify and relink those artifacts through its existing public boundaries and return a new governed research-session controller whose complete presentation is equivalent to the chosen durable session, without Chromium acquisition, path discovery, automatic ancestry traversal, global-head selection, or semantic authority expansion.

That is the minimum earned boundary needed before the complete research shell can become a real fresh-process public command.
