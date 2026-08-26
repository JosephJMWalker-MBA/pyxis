# Milestone 40C — First ordinary continuation above persisted third epoch

Status: proposed implementation pending executed test evidence.

Decision: D204

## Question

40A / D202 established one explicit third evidence-basis composition. 40B / D203 gave that concrete three-root state a strict locator-only durable representation.

40C asks the next narrower question:

> Can one persisted third evidence-basis epoch be freshly re-entered and extended by one ordinary restartable continuation without flattening first-, second-, or third-root ancestry?

This milestone proves only the first ordinary continuation above the persisted third epoch. It does not establish repeatable cumulative continuation and does not generalize the lineage representation.

## Decision D204

Pyxis may represent one first ordinary continuation above a persisted 40B third-epoch overlay with a strict locator-only plan containing exactly:

```text
prior_third_basis_epoch_overlay_source
declared_edge_sources
declaration_source
```

Its persisted format is:

```text
pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1
```

The overlay is operational configuration only.

## Fresh reconstruction order

A 40C re-entry performs:

```text
explicit 40B third-epoch overlay
        ↓
strict configuration decode
        ↓
fresh 40A third-epoch re-entry
        ↓
first root re-earned
second root re-earned
third root re-earned
        ↓
explicit ordered ordinary continuation edges
        ↓
explicit declaration
        ↓
governed controller
```

The prior third-epoch Python object is not durable authority. The 40B overlay must be independently decoded and its complete three-root state freshly reconstructed first.

## Direct durable anchor

The continuation plan references the 40B third-epoch overlay directly.

It does not contain:

- a copied 40A plan;
- copied first-, second-, or third-root records;
- nested continuation overlays;
- an epoch array;
- recursive ancestry data;
- current/latest/head fields;
- chronology or branch identity.

This keeps the first post-third-root continuation representation understandable before cumulative continuation is attempted.

## Configuration-only decode

`load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(...)` reads only the supplied 40C JSON document.

It does not open:

- the referenced 40B overlay;
- any first-, second-, or third-root artifact;
- any research evidence;
- any continuation edge;
- the continuation declaration.

Therefore successful decode establishes configuration shape only.

It does not establish evidence integrity, ancestry, restartability, governed state, chronology, branch identity, or a current/latest/head claim.

## Fresh three-root authority

`reenter_chromium_research_third_basis_epoch_continuation(...)` first loads the exact supplied 40B overlay and invokes the public third-epoch re-entry boundary.

Only the freshly reconstructed third-epoch declared endpoint may serve as the predecessor for the ordinary continuation.

The explicitly ordered continuation edge locations are then reconciled with one explicit declaration using the existing declaration loader.

No ambient edge discovery, filename inference, sorting, directory scan, predecessor search, or format guessing occurs.

## Proof-gated first checkpoint

`persist_chromium_research_third_basis_epoch_continuation_checkpoint(...)` accepts:

1. one already-earned third-epoch re-entry result;
2. one already-chosen session rollover;
3. one explicit current 40B overlay location;
4. one explicit successor edge location;
5. one explicit continuation declaration location;
6. one no-overwrite destination.

Before writing any bytes, Pyxis freshly decodes and re-enters the supplied 40B overlay.

The fresh prior must match the earned third-epoch state at all relevant retained layers:

```text
selected prior second-epoch continuation presentation
selected prior second-epoch continuation endpoint identity
first-root identity
second-root identity
third-root identity
third-epoch governed presentation
third-epoch terminal endpoint identity
```

The chosen rollover must also prove that its prior controller corresponds to that earned third-epoch presentation and endpoint.

Finally, the explicit continuation locations are freshly re-entered and must match the chosen rollover's continuation presentation and terminal endpoint identity.

Only then may the 40C overlay be written.

## Path discipline

Paths remain location context, not durable identity.

A path-distinct 40B overlay may be accepted when explicit fresh reconstruction proves the same retained roots, governed third-epoch presentation, and terminal endpoint identity.

No moved path is searched for or discovered automatically.

A missing or wrong explicit location fails even when a correct-looking decoy exists nearby.

## Explicit continuation choice

The ordinary continuation is caller-owned.

40C does not choose among siblings and does not infer which edge is newest, canonical, or preferred.

A rollover representing a different continuation than the supplied successor/declaration pair is rejected.

This preserves the existing rule that presentation of a choice is not authorization to choose it.

## Strict document behavior

The 40C overlay requires:

- exactly four root keys including `format`;
- one supported format value;
- duplicate JSON keys rejected;
- a non-empty ordered `declared_edge_sources` array;
- relative paths resolved only against the overlay parent;
- no-overwrite persistence;
- exact round-trip decode to the candidate typed plan.

Unknown keys are rejected rather than ignored so control-like state cannot silently enter the document.

## Three-root retention

Fresh 40C re-entry must retain three distinct ancestry roots through the fresh prior third-epoch result:

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
... persisted third-epoch segment ...
   ↓
first ordinary post-third continuation
```

The continuation does not replace or flatten any root.

## Failure behavior

40C must fail without writing when:

- the supplied 40B overlay is missing or malformed;
- retained first-root evidence is tampered;
- retained second-root evidence is tampered;
- third-root evidence is tampered;
- the supplied rollover does not belong to the earned third-epoch state;
- the supplied successor/declaration pair describes a different continuation;
- an explicit successor edge is wrong even when a correct decoy exists nearby;
- the destination already exists;
- required input types are wrong.

Failure grants no discovery fallback or authority substitution.

## Integrity discipline

SHA-256 record identities used by existing loaders remain integrity / record-identity facts only.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

The 40C locator overlay stores no root hashes or evidence digests.

## Why this is not cumulative continuation

40C persists exactly one first ordinary continuation above the 40B anchor.

It does not prove that the same overlay form should recursively reference another 40C overlay.

In particular, it does not add:

```text
prior_continuation_overlay_source -> another 40C overlay
```

or a nested overlay chain.

The next milestone may test cumulative continuation while preserving a direct 40B ancestry anchor, analogous to the earlier second-epoch progression, but that behavior is not part of D204.

## Non-goals

40C does not add:

- repeatable cumulative continuation above the third root;
- recursive overlay ancestry;
- generic `epoch[n]` representation;
- arbitrary-depth lineage walking;
- CLI third-epoch launch;
- Textual third-epoch launch;
- three-root authority-inspection product UI/report;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 40C permits only this statement:

> One explicitly persisted third evidence-basis epoch can be freshly re-entered and extended by one restartable ordinary continuation while retaining first-, second-, and third-root ancestry as distinct layers. This proves one first post-third-root continuation only, not cumulative or arbitrary-depth lineage.
