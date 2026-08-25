# Milestone 35B — Explicit Fresh-Process Re-entry for Root-Backed Declared Sessions

Decision: D182

## Product question

35A lets one exact loaded 34A root become the explicit start of an existing-format
26A/26B/26C declared segment. That segment can enter the existing governed 29A
controller and resume ordinary revision/rollover behavior.

35A deliberately stops at the in-process boundary.

The existing 31A re-entry plan can freshly reconstruct an ordinary declared session,
but it has no locator shape for the changed-basis ancestry introduced by:

```text
33B transition
→ 34A root
→ 35A root-started declaration
```

35B asks:

> Given one explicit ordinary 31A plan for the pre-change session, plus explicit
> locators for the added evidence and changed-basis/root/declaration artifacts, can
> Pyxis freshly reconstruct the same root-backed governed session after process exit
> without discovery or ancestry erasure?

35B answers **yes** through a separate typed locator plan.

## Why 35B does not widen the 31A v1 plan

The established 31A document format is:

```text
pyxis.chromium.research_session_reentry_locator_plan.v1
```

Its semantics describe one ordinary 20B/21B/22B/23B base, optional ordinary 24C edge
prefix, and one declared edge segment.

A root-backed session requires qualitatively different durable locators:

- a changed 20B working set;
- a changed 21B note;
- a 33B cross-working-set transition; and
- a 34A root.

Adding those keys silently to the v1 plan would change an existing operational
configuration contract and blur ordinary versus basis-crossing re-entry.

35B therefore introduces only a typed in-memory plan:

```text
ChromiumResearchRootBackedSessionReentryPlan
```

No new persisted plan document, CLI syntax, or Textual input is added.

## Plan shape

The plan contains:

```text
prior_session_plan
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

`prior_session_plan` is the complete existing 31A plan for the ordinary governed
session that owned the pre-change declared endpoint.

The new plan deliberately carries only the **appended** member locators for the
changed evidence basis. It does not duplicate locators for the prior working-set
members.

## Fresh reconstruction chain

35B performs:

```text
explicit prior 31A plan
→ public 31A fresh ordinary session re-entry
→ exact fresh prior declared endpoint

explicit appended member locators
→ existing 17D/18D/19D relinking

fresh prior working-set members
+ explicit freshly relinked appended members
→ exact ordered successor member tuple

prior endpoint
+ successor members
+ changed 20B/21B paths
+ 33B transition path
+ 34A root path
→ public 34A fresh root loader

fresh loaded 34A root
+ explicit 35A ordinary edge paths
+ explicit 26B declaration path
→ public 26C/35A declaration relinking

fresh standard loaded declaration
→ existing ChromiumResearchSessionController
```

No history is discovered from the filesystem.

## Prior endpoint path reuse

The public 34A loader requires an explicit `prior_edge_source`.

35B uses:

```text
prior_reentry.controller.declared_endpoint.verification.path
```

This is not ambient path discovery. That path was reached through the exact
caller-owned 31A plan and freshly verified during the same 35B operation.

Therefore:

```text
path retained by fresh explicit re-entry evidence
!=
filesystem search or digest discovery
```

The old prior edge path does not need to be redundantly copied into the 35B plan.

## Changed member ordering

The complete successor membership is reconstructed mechanically as:

```text
fresh prior endpoint working-set members
+
fresh explicitly supplied appended members
```

Prior members remain first. Appended members retain exact caller order and intentional
duplicates.

35B does not deduplicate, rank, classify, or infer semantic relation.

## Fresh 33B and 34A proof

35B does not reconstruct the changed basis from the declaration alone.

It delegates to the public 34A loader, which itself freshly verifies and relinks the
33B transition through:

- the exact prior endpoint;
- the complete ordered successor member tuple;
- the changed 20B working-set file;
- the changed 21B note file;
- the 33B transition file; and
- the 34A root file.

Thus the root-backed declaration cannot erase or bypass the evidence-basis change.

## Governed controller restoration

After the root is freshly loaded, public 26C/35A reconciles the explicit root-started
edge sequence with the durable declaration.

The result is the existing standard loaded declaration type, so 35B constructs the
existing `ChromiumResearchSessionController` without adding a parallel controller.

Ordinary governed endpoint revision behavior is therefore available immediately after
fresh re-entry.

## Plan creation remains read-free

`create_chromium_research_root_backed_session_reentry_plan()` validates only typed
locator structure and explicit ordering.

It does not require referenced files to exist and performs no evidence verification.

As with 31A:

```text
plan construction
!=
re-entry proof
```

Only `reenter_chromium_research_root_backed_session()` reads and verifies artifacts.

## Authority boundaries

35B does not infer or claim:

- a global current/latest/canonical head;
- complete history;
- chronology;
- branch identity;
- unique successor;
- semantic improvement;
- evidentiary support for human rationale;
- relevance or completeness from working-set membership;
- source authenticity;
- citation authority;
- path identity;
- directory scanning;
- digest-based discovery;
- browser reacquisition;
- autonomous research;
- persisted root-backed restart-plan semantics; or
- CLI/Textual authority for the new plan.

## Falsifiability

Focused 35B coverage proves:

1. typed plan construction succeeds from locator structure even when changed-basis
   paths do not exist;
2. fresh 35B re-entry independently reconstructs the prior ordinary 31A session;
3. appended evidence is freshly relinked from explicit capture/note locators;
4. successor membership is exactly fresh prior members followed by explicit appended
   members;
5. the public 34A loader freshly reconstructs the exact 33B transition + 34A root;
6. the loaded transition prior endpoint is the exact freshly reconstructed prior
   declared endpoint;
7. public 26C/35A freshly reconstructs the root-started declaration;
8. the resulting existing controller exposes the root format as the declared segment
   start while retaining an ordinary edge as the declared endpoint;
9. a wrong appended member locator rejects against the durable changed basis;
10. tampered root bytes reject before declaration adoption;
11. a wrong explicit declared edge is not replaced by an obvious decoy file;
12. the freshly reconstructed controller can immediately perform an ordinary governed
    endpoint revision; and
13. already-loaded 35B application evidence remains usable after its changed-basis
    durable locators are removed.

## Scope

35B adds only:

- `src/pyxis/app/chromium_research_root_backed_session_reentry.py`;
- `tests/test_app_chromium_research_root_backed_session_reentry.py`; and
- this milestone document.

35B does not change:

- the existing 31A plan type;
- the 31A v1 plan document;
- 32A continuation-plan construction;
- 32B restart-plan checkpointing;
- 33A/33B semantics;
- 34A/34B semantics;
- 35A sequence/declaration semantics;
- generic 24C;
- durable research formats;
- CLI;
- Textual UI;
- Chromium acquisition;
- research-control-plane state; or
- Repository Zero.

## What successful 35B proves

Successful 35B establishes only:

> From one explicit caller-owned ordinary 31A prior-session plan, one or more explicit
> appended-member locators, and explicit changed 20B/21B, 33B transition, 34A root,
> 35A edge-sequence, and 26B declaration paths, Pyxis can freshly reconstruct the
> pre-change governed session, exact changed-basis ancestry, root-started declared
> segment, and existing governed controller in a new process without filesystem
> discovery, ancestry erasure, or global head/chronology/semantic authority.
