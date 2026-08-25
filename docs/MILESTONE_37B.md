# Milestone 37B — Persisted Second-Basis-Epoch Re-entry Overlay

Decision: D191

## Product question

37A / D190 proves that one explicitly defined second evidence-basis epoch can be freshly reconstructed above a persisted 35D/35E root-backed continuation without flattening the first basis-change ancestry into an ordinary session plan.

The 37A plan is still in-memory operational configuration.

37B asks only:

> Can that already-proven second-epoch locator plan be checkpointed as a strict durable restart overlay while preserving both ancestry layers and without upgrading configuration into research evidence or global-head authority?

## Decision

Add one locator-only JSON format:

```text
pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1
```

with exactly:

```text
format
prior_root_backed_continuation_overlay_source
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

This is the durable operational form of the established 37A typed plan.

It does **not** embed:

- an ordinary 31A plan;
- a decoded first-epoch 35B plan;
- a decoded 35D/35E continuation plan;
- another 37A/37B plan;
- a recursive ancestry object;
- a content digest, timestamp, branch identity, or head marker.

## Configuration-only loading

`load_chromium_research_second_basis_epoch_reentry_plan_document()` reads only the 37B overlay document itself.

It does not open:

- the referenced prior 35D/35E continuation overlay;
- appended-member capture or note files;
- the second changed working set or note;
- the second 33B transition;
- the second 34A root;
- the second declared edges or declaration.

Those paths become evidence inputs only when the decoded plan is explicitly passed to the existing public 37A fresh-re-entry boundary.

This separation is intentional:

```text
configuration decode
!=
evidence verification
```

Relative paths are interpreted only relative to the 37B overlay parent. The established 31B locator codec is reused for member families and path encoding rather than creating a second member-locator grammar.

## Proof-gated persistence

`persist_chromium_research_second_basis_epoch_reentry_plan_document()` accepts:

- one already-earned `ChromiumResearchSecondBasisEpochReentryResult`;
- one explicitly supplied current prior 35D/35E continuation-overlay location;
- one no-overwrite destination.

The caller must explicitly supply the prior continuation-overlay location again. The path retained when the 37A result was originally constructed is not silently promoted into perpetual current-location authority.

A candidate 37A plan is built from:

```text
explicit current prior continuation-overlay source
+ earned second-epoch appended-member locators
+ earned second changed working-set/note locators
+ earned second transition/root locators
+ earned second declared-edge/declaration locators
```

The candidate is then freshly reconstructed through:

```text
reenter_chromium_research_second_basis_epoch(candidate_plan)
```

before any overlay bytes are written.

## Two-layer proof requirements

The fresh reconstruction must match the earned result across both ancestry layers.

### Prior first-epoch continuation layer

37B requires:

- prior continuation governed presentation equality;
- prior continuation terminal durable edge identity equality;
- retained first-epoch 34A root durable identity equality.

The fresh prior continuation may consist of newly loaded Python objects at different explicit filesystem locations. Object identity and path equality are not required.

### Second-epoch layer

37B also requires:

- second 34A root durable identity equality;
- final second-epoch governed presentation equality;
- final declared endpoint durable edge identity equality.

Only after both layers agree is the new overlay written.

## Path-distinct prior continuation authority

A prior 35D/35E continuation at a different explicit path may be accepted when fresh reconstruction proves the same durable prior authority.

Thus:

```text
different explicit path
!=
different durable ancestry
```

and:

```text
same path
!=
authority without fresh verification
```

37B does not search for moved overlays. The alternative location must be supplied explicitly by the caller.

## Strict document behavior

The 37B document:

- rejects duplicate JSON object keys;
- rejects missing top-level fields;
- rejects unknown top-level fields;
- rejects unsupported formats;
- rejects malformed member locator shapes through the established locator grammar;
- requires a non-empty appended-member sequence;
- requires a non-empty declared-edge sequence;
- writes with no overwrite;
- round-trip decodes to the exact candidate 37A plan after persistence.

The loader remains useful even when referenced files are temporarily absent because decoding the locator overlay is not evidence re-entry.

## Persistence ordering

37B follows the proof-before-write ordering already established by 35C:

```text
freshly prove candidate ancestry/session
→ attempt no-overwrite overlay write
→ round-trip decode
```

An existing destination therefore does not skip fresh ancestry proof. No-overwrite is a file mutation rule, not an alternative evidence authority path.

## Falsifiability

37B rejects checkpointing when:

- the explicit prior continuation overlay is missing, malformed, or reconstructs different ancestry;
- first-epoch durable ancestry beneath that overlay has been tampered;
- any required second-epoch evidence locator can no longer freshly reconstruct the earned second root/session;
- the fresh prior continuation presentation, endpoint identity, or first-root identity differs;
- the fresh second-root identity differs;
- the fresh second-epoch presentation or endpoint identity differs;
- the destination already exists;
- the persisted overlay does not round-trip to the exact candidate plan.

It does not scan for a replacement prior overlay or substitute a decoy artifact.

## Authority still absent

37B does not add:

- research-evidence status to locator configuration;
- content digests inside the overlay;
- source authenticity, authorship, or trusted time;
- semantic support or truth claims;
- citation authority;
- a global latest/current/canonical head;
- chronology or branch semantics;
- directory scanning or digest discovery;
- predecessor or moved-path discovery;
- format guessing;
- arbitrary-depth basis-change ancestry;
- a third basis-change model;
- CLI launch support for 37B;
- Textual/UI controls for second-epoch creation or checkpointing.

## Acceptance statement

A successful 37B establishes only:

> One proven second evidence-basis epoch can be checkpointed as a strict locator-only restart overlay. The overlay preserves an explicit reference to the prior persisted 35D/35E continuation instead of flattening that ancestry, is written only after fresh reconstruction matches the earned session across both root-backed ancestry layers, and remains operational configuration rather than research evidence or global-head authority.
