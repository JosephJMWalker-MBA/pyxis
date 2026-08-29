# Milestone 46A — explicit second changed-basis transition from one-root continuation

Decision: **D228**

## Question

45A / D226 and 45B / D227 close one-root authority-inspection parity. Existing 37–38 machinery can freshly re-enter and operate an already-created second evidence-basis epoch, while lower-level 33A–34B machinery can construct the records from which that epoch is later re-entered.

The remaining product gap is narrower: a live one-root continuation product that has explicitly opted into 44A preparation cannot yet persist the second 33B cross-working-set transition from its exact typed continuation authority.

46A asks whether Pyxis can expose that one transition without broadening first-crossing authority, inferring durable locators, creating the second root, or introducing a generic repeated-transition abstraction.

## Decision D228

Add one concrete second changed-basis transition boundary to the existing `RootBackedContinuationResearchSessionShell` family.

The product rule is:

```text
exact current ChromiumResearchRootBackedSessionContinuationReentryResult
+
new successful inherited 44A preparation
+
caller-explicit durable 33B locators
→
one persisted + freshly relinked second changed-basis transition
```

while:

```text
second transition
!= second 34A root
!= second-epoch declared session
!= 37A re-entry
!= automatic adoption
```

## Reuse and prior art

46A introduces no new persistence format or transition record format.

It reuses:

- 44A / D218 for opt-in, already-loaded candidate preparation in `ResearchSessionShell` subclasses;
- 44B / D219 for the concrete product pattern of explicit-only transition controls, retryable failure, historical locked success, and stale-on-rollover behavior;
- public 33B transition creation, persistence, and fresh relinking;
- 35D/35E typed root-backed continuation re-entry as the exact one-root ancestry authority;
- 37A's already-proven lower-level construction sequence, which applies existing 33A→33B→34A→34B machinery to one-root continuation state before creating a two-root re-entry plan;
- 45A / D226 for the distinction between persisted continuation launch provenance and raw 36D in-process handoff provenance.

44B remains unchanged and ordinary-reentry-only. 46A is a separate concrete helper rather than a generalized Nth-transition API.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Application boundary

`pyxis.app.chromium_research_second_changed_basis_transition` requires exactly:

```text
ChromiumResearchRootBackedSessionContinuationReentryResult
```

The helper must prove that the supplied controller matches the typed continuation on:

- governed presentation;
- declaration durable identity;
- current declared-endpoint durable identity.

The successful 44A preparation must belong to that exact controller presentation and retain that exact declared endpoint.

The result retains:

- exact controller;
- exact continuation re-entry;
- exact preparation result;
- public in-memory 33B transition;
- public durable transition persistence evidence;
- freshly loaded/relinked transition.

Fresh relinking must identify the exact current predecessor endpoint and exact prepared successor working set and note.

## Explicit locator discipline

Four durable path inputs remain caller-explicit:

```text
prior edge source
prepared working-set source
prepared working-set-note source
transition destination
```

No path is copied or inferred from:

- 44A preparation receipts;
- the continuation re-entry plan;
- a 35D/35E launch overlay;
- a 35E checkpoint destination;
- 45A launch provenance;
- raw 36D handoff state;
- directory contents or filename conventions.

Moved but durably equivalent prepared records work only when their explicit current paths are supplied.

## Product surface

`RootBackedContinuationResearchSessionShell` already inherits optional 44A preparation. 46A does not change its constructor and does not configure a candidate automatically.

When a caller has explicitly configured candidate evidence before mount and a newly successful 44A preparation occurs, the shell mounts exactly one second-transition form.

The form begins with all path fields blank and describes the prepared basis as not yet transitioned or rooted.

On success:

- the exact 33B transition is persisted and freshly relinked;
- the form becomes a locked historical receipt;
- mounted controller, session, and typed continuation re-entry remain unchanged;
- no second root or second-epoch control is mounted.

On retryable failure, the form remains available.

## Candidate and rollover lifecycle

46A preserves the inherited 44A candidate lifecycle rather than adding reconfiguration semantics.

If the shell adopts a different declared session before the transition is saved:

- inherited 44A candidate/preparation state becomes stale under existing rules;
- the 46A transition form is also marked stale and disabled;
- neither surface silently retargets.

A one-hop controller that has advanced beyond the exact retained typed continuation is therefore ineligible for 46A until existing product boundaries establish a new exact authority state. 46A does not add a candidate-reset or post-promotion reconfiguration mechanism.

## Persisted versus raw launch provenance

The existing 45A continuation adapters inherit 46A behavior from the same concrete continuation shell.

For a persisted 35D/35E launch, the immutable proved launch-location context remains unchanged by preparation or second-transition persistence.

For a raw 36D handoff, launch location remains `None` before and after second-transition persistence.

46A does not require, infer, or create a launch overlay path.

## Textual dispatch discipline

The existing continuation shell handles its own concrete button IDs and delegates only unhandled events to the base shell. 46A adds its button to that existing handler rather than introducing a subclass that manually redispatches an already handled inherited event.

This preserves the lesson from prior Textual MRO failures: one user action must schedule one mutation attempt.

## Tests

Focused coverage requires:

- exact continuation result required at the application boundary;
- fresh 33B relink to the exact predecessor and prepared successor basis;
- moved prepared records accepted only via explicit new paths;
- mismatched typed continuation rejected before destination write;
- no transition controls before successful 44A preparation;
- newly successful preparation mounts one blank explicit transition form;
- successful transition leaves mounted controller/session/continuation unchanged;
- rollover stales an unsaved transition rather than retargeting it;
- persisted 45A launch provenance object remains unchanged;
- raw 36D launch path remains absent;
- plain continuation shell without configured candidate gains no transition surface;
- no second-root/adoption/re-entry controls appear from 46A success.

Repository Zero remains the final regression gate across Python 3.11–3.14.

## Non-goals

46A does not add:

- second 34A revision-root creation;
- second 34B post-root edge creation;
- second-epoch adoption or 37A re-entry;
- 37B restart overlay persistence;
- a new CLI flag;
- a new persistence format;
- launch-path serialization for raw handoffs;
- candidate reset/reconfiguration after rollover;
- generic repeated or Nth basis-transition APIs;
- fourth-epoch or arbitrary-depth ancestry;
- discovery, prefill, current/latest/head, chronology, or branch authority;
- path identity;
- authorship, authenticity, or trusted-time authority;
- semantic-support or citation authority;
- browser reacquisition or autonomous research behavior.

## Acceptance statement

If executed tests pass, 46A permits only this statement:

> An exact one-root continuation product with explicitly configured candidate evidence can use inherited 44A preparation and then persist one public 33B second changed-basis transition from caller-explicit durable locators. The transition is freshly relinked to the exact retained continuation endpoint and prepared successor basis, while mounted continuation state and persisted/raw launch-provenance semantics remain unchanged.
