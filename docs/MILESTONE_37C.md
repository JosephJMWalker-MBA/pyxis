# Milestone 37C — First restartable continuation above a persisted second basis epoch

## Decision D192

A persisted second evidence-basis epoch may be followed by one explicitly chosen ordinary continuation without flattening either basis-change epoch.

37C therefore introduces a locator-only continuation overlay whose prior-session anchor is one explicit persisted 37B overlay. Fresh continuation re-entry must first re-earn the complete 37B second epoch—including its retained first root-backed continuation—and only then reconcile the explicitly supplied ordinary continuation edge sequence and declaration through the existing declaration loader.

The 37C overlay is operational restart configuration. It is not research evidence, a history index, a head pointer, chronology, or branch state.

## Durable format

```text
pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1
```

Exact fields:

```text
format
prior_second_basis_epoch_overlay_source
declared_edge_sources
declaration_source
```

No ordinary 31A plan, 35B plan, 35D/35E plan, 37A plan, research digest, timestamp, or head state is embedded.

## Fresh reconstruction

```text
explicit 37B overlay source
→ strict existing 37B configuration loader
→ existing 37A fresh second-epoch re-entry
→ fresh second-epoch governed endpoint

fresh endpoint
+ explicit continuation edge paths
+ explicit declaration source
→ existing 26C declaration relinking
→ standard governed controller
```

The returned `ChromiumResearchSecondBasisEpochContinuationReentryResult` retains the complete fresh `ChromiumResearchSecondBasisEpochReentryResult`. Through that result, both the first basis-change root and the second basis-change root remain separately inspectable.

## Checkpoint proof

`persist_chromium_research_second_basis_epoch_continuation_checkpoint(...)` accepts:

- one already-earned `ChromiumResearchSecondBasisEpochReentryResult`;
- one chosen `ChromiumResearchSessionRolloverResult`;
- the explicit current 37B overlay location;
- the explicit chosen successor edge location;
- the explicit one-hop continuation declaration location;
- one no-overwrite 37C overlay destination.

Before any 37C bytes are written, Pyxis:

1. decodes the explicitly supplied 37B overlay;
2. freshly re-enters its complete second basis-change epoch;
3. requires the fresh retained prior continuation presentation and terminal edge identity to match the earned ancestry;
4. requires the retained first-root durable identity to match;
5. requires the second-root durable identity to match;
6. requires the second-epoch governed presentation and terminal edge identity to match;
7. requires the chosen rollover's prior controller presentation and endpoint identity to match the earned second epoch;
8. constructs a one-hop 37C continuation plan from the explicit 37B overlay, successor edge, and declaration locations;
9. freshly re-enters that candidate continuation;
10. requires its presentation and terminal durable edge identity to match the chosen rollover;
11. writes the strict no-overwrite 37C overlay;
12. round-trip decodes it and requires exact typed-plan equality.

## Path is location, not identity

37C deliberately does not require the decoded 37B plan to equal the already-earned 37A plan merely because path fields differ.

A path-distinct 37B overlay may be used when it is explicitly supplied and fresh reconstruction proves the same durable ancestry/session authority. No alternate path is discovered automatically.

This preserves the later authority correction already established in the root-backed lineage:

```text
different filesystem location != different durable session identity
```

## Configuration decoding remains non-evidentiary

Loading a 37C overlay reads only the overlay document. It does not open the referenced 37B overlay and does not verify research evidence.

Therefore:

```text
successful overlay decode != successful session re-entry
```

The referenced ancestry earns authority only when fresh re-entry is explicitly invoked.

## Proven behavior

The 37C test surface covers:

- strict locator-only serialization;
- exact typed-plan roundtrip;
- fresh continuation reconstruction above a persisted second epoch;
- retention of both basis-change ancestry layers;
- second-root tamper rejection before checkpoint write;
- retained first-root tamper rejection before checkpoint write;
- path-distinct but durably equivalent explicit 37B overlay acceptance;
- rejection of a different chosen continuation;
- rejection of a wrong explicit successor without searching for a nearby decoy;
- configuration-only overlay decoding while the referenced 37B overlay is unavailable;
- no-overwrite;
- duplicate, missing, unknown, and empty-edge configuration rejection;
- absence of digest/head/chronology/semantic-authority fields.

## What 37C does not authorize

37C does **not** add:

- cumulative repeated continuation checkpointing above the second root;
- CLI launch of 37B or 37C overlays;
- Textual controls for second-epoch lineage;
- a third evidence-basis epoch;
- arbitrary-depth repeated basis-change ancestry;
- recursive continuation-overlay parent chains;
- directory scanning or path discovery;
- predecessor search;
- format guessing;
- current/latest/head authority;
- chronology or branch semantics;
- semantic-support, truth, authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

After 37C, Pyxis may say only:

> One explicitly chosen first ordinary continuation above a persisted second evidence-basis epoch can be checkpointed and freshly reconstructed without flattening either basis-change epoch. The prior 37B ancestry is re-earned from its explicit locator, the continuation is reconciled through the existing declaration machinery, and the resulting overlay remains locator-only operational configuration rather than evidence or global-head state.
