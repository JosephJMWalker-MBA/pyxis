# Milestone 37D — Cumulative continuation checkpointing above the second basis epoch

## Decision D193

Repeated ordinary continuation above the second evidence-basis epoch must not create recursive continuation-overlay ancestry.

37D therefore reuses the existing 37C overlay format while keeping its 37B ancestry anchor fixed. Each new checkpoint grows one explicit ordered post-second-root edge tuple and persists a new cumulative declaration.

```text
37B second-epoch overlay
        ↓
       E1 → E2 → E3 → ... → En
```

not:

```text
37B → 37C(E1) → 37C(E2) → 37C(E3) → ...
```

No new persistent overlay format is introduced.

## Reused durable format

```text
pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1
```

A cumulative 37C document continues to contain exactly:

```text
format
prior_second_basis_epoch_overlay_source
declared_edge_sources
declaration_source
```

The difference is only that `declared_edge_sources` may now contain the complete caller-ordered continuation segment `(E1, E2, ..., En)` and `declaration_source` names the corresponding cumulative 26B declaration.

## Cumulative checkpoint proof

`persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(...)` accepts:

- the currently earned 37C continuation re-entry;
- one chosen 30A rollover from that current endpoint;
- the explicit current 37C overlay location;
- the explicit chosen successor edge location;
- a no-overwrite cumulative declaration destination;
- a no-overwrite next 37C overlay destination.

Before new durable outputs are created, Pyxis:

1. requires the declaration and overlay destinations to be distinct and unused;
2. decodes the explicitly supplied current 37C overlay;
3. freshly re-enters it;
4. requires the fresh current continuation presentation and terminal edge identity to match the supplied current continuation;
5. requires the fresh second-epoch anchor presentation and terminal edge identity to match;
6. requires the fresh second-root durable identity to match;
7. requires the retained first-root durable identity to match;
8. requires the chosen rollover prior presentation and endpoint identity to match the supplied current continuation;
9. forms the cumulative source tuple by appending the explicit chosen successor to the current overlay's declared edge tuple;
10. freshly relinks that complete edge sequence from the freshly reconstructed 37B second-epoch endpoint;
11. requires the cumulative sequence terminal edge SHA and exact revised human text to match the chosen rollover successor;
12. persists a new cumulative 26B declaration;
13. constructs a new 37C plan using the same fixed 37B overlay anchor, the cumulative edge tuple, and the new declaration;
14. freshly re-enters the new plan;
15. requires terminal durable edge identity and exact final wording to match the chosen rollover;
16. writes the next no-overwrite 37C overlay;
17. round-trip decodes it and requires exact typed-plan equality.

## Terminal equivalence, not presentation equality

A one-hop 30A rollover presents only its chosen continuation segment. A cumulative 37C re-entry intentionally presents all declared post-second-root edges from the fixed 37B anchor.

Therefore:

```text
same chosen terminal continuation
!=
same whole declared-segment presentation
```

37D establishes equivalence to the chosen rollover using:

- terminal durable edge SHA-256 identity; and
- exact final human wording.

It does not incorrectly require the longer cumulative presentation to equal the one-hop rollover presentation.

## Path is still location, not identity

The explicitly supplied current 37C overlay is re-entered and compared by durable ancestry/session relationships. 37D does not require its decoded path-bearing plan to equal the supplied in-memory plan merely because file locations differ.

A path-distinct current 37C configuration may therefore be accepted when it is explicitly supplied and fresh reconstruction proves the same current continuation, second root, and retained first root.

No alternate location is discovered automatically.

## No recursive continuation configuration

The current 37C overlay is input to proof only. It is never stored as the next overlay's ancestry anchor.

The next plan always preserves:

```text
next_plan.prior_second_basis_epoch_overlay_source
==
current_plan.prior_second_basis_epoch_overlay_source
```

That fixed source is the 37B second-epoch overlay.

## Proven behavior

The 37D test surface covers:

- first cumulative extension from a 37C checkpoint;
- a second cumulative extension from an already cumulative 37C checkpoint;
- fixed 37B ancestry anchoring without recursive 37C references;
- longer cumulative presentation with matching chosen terminal endpoint/text;
- unchanged old overlay and one-hop declaration bytes;
- roundtrip through the unchanged 37C loader;
- path-distinct but durably equivalent current 37C configuration;
- rejection of a genuinely different current overlay;
- wrong explicit successor rejection without decoy discovery;
- second-root tamper rejection;
- retained first-root tamper rejection;
- no-overwrite declaration and overlay destinations;
- distinct-output preflight.

## What 37D does not authorize

37D does **not** add:

- a new continuation overlay format;
- recursive continuation overlays;
- CLI or Textual exposure for the second-epoch lineage;
- a third evidence-basis epoch;
- arbitrary-depth repeated basis-change ancestry;
- directory scanning or locator discovery;
- predecessor search;
- format guessing;
- current/latest/head authority;
- chronology or branch semantics;
- semantic-support, truth, authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

After 37D, Pyxis may say only:

> Repeated ordinary continuation above the second evidence-basis epoch can be checkpointed cumulatively without recursive continuation-overlay ancestry. Every next 37C overlay retains the same explicit 37B anchor, declares the complete caller-ordered post-second-root edge tuple, and proves the chosen terminal continuation by durable endpoint identity and exact human wording.
