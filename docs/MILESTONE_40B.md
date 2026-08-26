# Milestone 40B — Persisted third evidence-basis epoch re-entry overlay

Status: proposed implementation pending executed test evidence.

Decision: D203

## Question

40A / D202 established one explicit third changed evidence-basis epoch above a freshly reconstructed second-epoch continuation while retaining first-, second-, and third-root ancestry as distinct layers.

40B asks the next narrower question:

> Can that concrete three-root state be represented by a strict locator-only document and independently re-earned after process exit without flattening or generalizing the ancestry model?

The answer may be earned only through fresh reconstruction. The overlay itself is not authority.

## Decision D203

Pyxis may persist one third-basis-epoch re-entry locator overlay whose complete schema is:

```text
format
prior_second_basis_epoch_continuation_overlay_source
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

The format is:

```text
pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1
```

The overlay contains no root hashes, evidence digests, timestamps, chronology, branch identity, or current/latest/head markers.

## Configuration-only decode

`load_chromium_research_third_basis_epoch_reentry_plan_document(...)` reads only the supplied overlay document.

It does not read:

- the referenced 37C/37D second-epoch continuation overlay;
- appended member evidence;
- changed working-set or note records;
- the third transition;
- the third root;
- ordinary third-root edges;
- the declaration.

Therefore successful decode proves only that a locator configuration has the exact required shape.

It does not prove:

- evidence integrity;
- first-root ancestry;
- second-root ancestry;
- third-root ancestry;
- governed state;
- restartability;
- chronology;
- branch identity;
- current/latest/head status.

## Proof-gated persistence

`persist_chromium_research_third_basis_epoch_reentry_plan_document(...)` accepts:

1. one already-earned `ChromiumResearchThirdBasisEpochReentryResult`;
2. one explicitly supplied current location for the prior 37C/37D second-epoch continuation overlay;
3. one explicit no-overwrite destination.

The operation forms a candidate third-epoch plan from the explicit prior-overlay location plus the third-epoch locator layer retained by the earned result.

Before writing any bytes, Pyxis independently calls the public 40A re-entry boundary.

The fresh result must match the earned result at every retained authority layer relevant to the three-root structure.

## Required three-root match

The proof gate compares:

```text
retained first-root durable identity
retained second-root durable identity
selected post-second-epoch continuation presentation
selected post-second-epoch continuation terminal edge identity
third-root durable identity
final third-epoch governed presentation
final third-epoch terminal edge identity
```

A final-controller-only comparison would be insufficient because it could hide divergence in retained ancestry.

The first and second roots are obtained through the freshly reconstructed prior second-epoch continuation. The third root is freshly relinked by 40A.

No Python object identity is durable authority.

## Path discipline

The prior 37C/37D continuation overlay path is location context only.

A path-distinct prior continuation may be accepted when fresh reconstruction proves the same retained first-root identity, retained second-root identity, governed continuation presentation, and terminal endpoint identity.

This does not make the path an identity claim.

No directory scan, path search, moved-file discovery, predecessor discovery, or latest/current/head selection is introduced.

## Strict document behavior

40B requires:

- exactly the declared root keys;
- exactly one supported format value;
- duplicate JSON keys rejected;
- a non-empty appended-member array;
- a non-empty declared-edge array;
- existing shared strict member decoding;
- relative paths resolved only against the overlay parent;
- no-overwrite persistence;
- exact round-trip decode to the candidate typed plan.

Unknown keys are rejected rather than ignored so control-like fields cannot silently enter the overlay.

## Failure behavior

Persistence writes no bytes when fresh reconstruction fails because of:

- missing or malformed prior second-epoch continuation configuration;
- tampered retained first-root ancestry;
- tampered retained second-root ancestry;
- changed prior continuation state;
- tampered third changed-basis artifacts;
- tampered third root;
- incoherent third-root declared segment.

Wrong result and path types fail before authority-bearing reconstruction or write.

An existing destination is never overwritten.

## Integrity discipline

The fresh loaders may compare SHA-256 record identities as established by earlier milestones.

Those identities establish only the integrity / record-identity relationships already defined by those formats.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

The 40B overlay itself stores none of those hashes.

## Why this remains concrete rather than recursive

40B introduces one named persistence boundary for one named three-root result:

- `ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult`
- `ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult`
- `load_chromium_research_third_basis_epoch_reentry_plan_document(...)`
- `persist_chromium_research_third_basis_epoch_reentry_plan_document(...)`

It does not add:

```text
epoch[n]
ancestor_roots[]
recursive_parent_overlay
```

or any generic walker.

The document references one explicitly understood prior 37C/37D continuation representation. Earlier ancestry remains reconstructed by that existing boundary rather than copied into the third-epoch overlay.

## Non-goals

40B does not add:

- an ordinary continuation above the third root;
- cumulative third-root continuation;
- third-epoch CLI launch;
- third-epoch Textual launch;
- three-root authority-inspection UI/report;
- arbitrary-depth lineage schemas;
- recursive ancestry walking;
- generic epoch arrays;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 40B permits only this statement:

> One explicitly earned third evidence-basis epoch can be represented by a strict locator-only overlay and independently re-earned from that overlay while retaining first-, second-, and third-root ancestry as distinct layers. This remains one concrete three-root persistence proof, not arbitrary-depth lineage.
