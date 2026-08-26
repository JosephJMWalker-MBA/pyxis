# Milestone 40A — Explicit third evidence-basis epoch composition proof

Status: proposed implementation pending executed test evidence.

Decision: D202

## Question

Milestones 37–39 established one second changed evidence-basis epoch, made it restartable and usable through product paths, and then made its authority inspectable without expanding that authority.

The next question is deliberately narrower than arbitrary-depth ancestry:

> Does the explicit basis-change construction compose one more time?

40A tests exactly one third changed evidence-basis epoch above a freshly proven second-epoch continuation.

## Decision D202

Pyxis may reconstruct one third basis-change epoch only from one explicitly supplied persisted 37C/37D second-epoch continuation overlay.

The reconstruction sequence is:

```text
explicit 37C/37D continuation overlay
        ↓
strict configuration decode
        ↓
fresh second-epoch continuation re-entry
        ↓
explicit third-epoch appended members
        ↓
explicit changed working set + note
        ↓
explicit 33B transition
        ↓
explicit third 34A root
        ↓
explicit root-started ordinary declaration
        ↓
governed controller
```

No prior Python object is durable authority. The explicit prior overlay is independently decoded and freshly re-entered before third-epoch state is accepted.

## Plan boundary

`ChromiumResearchThirdBasisEpochReentryPlan` contains only:

```text
prior_second_basis_epoch_continuation_overlay_source
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

It does not contain:

- a nested second-epoch plan;
- an epoch array;
- a recursive ancestry tree;
- copied first- or second-root records;
- a latest/current/head marker;
- chronology or branch state.

The plan is operational configuration only.

## Three retained ancestry layers

A successful reconstruction preserves:

```text
first root
   ↓
... first-root continuation ...
   ↓
second root
   ↓
... second-root continuation ...
   ↓
third root
   ↓
... declared third-root segment ...
```

The first and second roots remain present inside the freshly reconstructed prior second-epoch continuation. The third root is newly relinked from that fresh prior endpoint.

Therefore:

```text
third root != replacement for second root
second root != replacement for first root
```

and 40A must prove all three retained root identities are distinct in the test fixture.

## Fresh prior authority

The prior anchor is one explicit 37C/37D continuation overlay location.

40A performs:

1. strict decode of that exact overlay;
2. fresh second-epoch continuation re-entry through the established public boundary;
3. only then uses the fresh prior controller's declared endpoint as the pre-third-epoch endpoint.

A missing or malformed prior overlay fails before third-epoch reconstruction.

A prior continuation whose durable evidence has been tampered with also fails before the third root can be accepted.

## Third changed evidence basis

Only explicitly supplied appended working-set member locators are loaded.

The successor working-set order is exactly:

```text
fresh prior endpoint members
+
caller-ordered appended third-epoch members
```

The changed working set, changed note, transition, and third root are all supplied by explicit locations and freshly relinked using the existing 33B/34A loader boundary.

No ambient member discovery or directory scan exists.

## Root-started declaration

The ordinary segment above the third root is reconstructed only from:

- the freshly loaded third root;
- explicitly ordered declared edge sources;
- one explicit declaration source.

A wrong declared edge is rejected even if a byte-identical decoy with an obvious name exists nearby.

## Path discipline

Paths are location context, not durable identity.

40A preserves two existing rules:

1. moved artifacts can work only when their new locations are explicitly resupplied;
2. a path-distinct prior 37C/37D configuration may be accepted when fresh reconstruction proves equivalent durable first-root, second-root, presentation, and endpoint relationships.

There is no path-based identity claim and no latest/current/head selection.

## Integrity discipline

SHA-256 values and record relationships establish integrity / record identity within the existing loaders.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

## Why this is not arbitrary-depth lineage

40A intentionally names a concrete third-epoch type:

- `ChromiumResearchThirdBasisEpochReentryPlan`
- `ChromiumResearchThirdBasisEpochReentryResult`
- `create_chromium_research_third_basis_epoch_reentry_plan(...)`
- `reenter_chromium_research_third_basis_epoch(...)`

It does not introduce:

```text
epoch[n]
```

or a generic recursive ancestor collection.

One successful third composition is evidence that the architecture composes one additional time. It is not evidence that an unlimited recursive representation is correct, safe, understandable, or product-ready.

## Failure behavior

40A requires explicit rejection for:

- wrong plan type;
- missing prior second-epoch continuation overlay;
- tampered prior second-epoch continuation evidence;
- appended-member relinking failure;
- tampered or incoherent third root;
- wrong third declared edge/declaration.

Failure must not trigger discovery, path guessing, fallback selection, or authority substitution.

## Non-goals

40A does not add:

- a persisted third-epoch locator overlay;
- third-epoch continuation overlay;
- checkpointing or cumulative continuation above the third root;
- CLI or Textual third-epoch launch;
- third-epoch authority-inspection product UI;
- arbitrary-depth basis-change schemas;
- recursive lineage walking;
- generic epoch arrays;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 40A permits only this statement:

> One explicit third evidence-basis epoch can be freshly reconstructed above an explicitly located, freshly proven second-epoch continuation while retaining the first, second, and third roots as distinct ancestry layers. This proves one additional composition step, not arbitrary-depth recursive lineage.
