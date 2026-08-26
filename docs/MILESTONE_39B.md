# Milestone 39B — Deterministic non-interactive second-epoch authority inspection

Status: proposed implementation pending executed test evidence.

Decision: D201

## Question

39A / D200 made already-earned second-epoch authority visible inside the Textual research product while preserving the distinction:

```text
immutable launch provenance
!= current governed state
```

The projection logic, however, lived next to the Textual widget. That left two product gaps:

1. scripts and operators could not inspect the same authority without launching an interactive UI;
2. adding a second non-interactive renderer risked duplicating root/endpoint derivation and creating two subtly different authority descriptions.

39B asks whether Pyxis can expose one deterministic non-interactive report while keeping exactly one projection model and without turning report output into authority.

## Decision D201

The second-epoch authority description becomes a UI-independent application projection.

Both interactive and non-interactive product surfaces must consume that same projection.

Therefore:

```text
Textual inspection derivation
== non-interactive inspection derivation
```

at the application-model boundary, while:

```text
inspection report
!= evidence
!= control-plane authority
```

## Shared application projection

The new application module is:

`pyxis.app.chromium_research_second_basis_epoch_authority_inspection`

It defines immutable projection records for:

- launch provenance;
- current governed state;
- the combined authority inspection.

It derives those records only from already-proven typed state:

- `ChromiumResearchSecondBasisEpochShellLineage`;
- `ChromiumResearchSecondBasisEpochContinuationShellLineage`;
- exact in-process `ChromiumResearchSecondBasisEpochContinuationReentryResult`.

The projection performs no file reads, writes, overlay loading, path proof, discovery, format guessing, browser operations, mutation, restart, or checkpointing.

## Launch families

The pure projection retains the three 39A launch families:

```text
persisted 37B second-basis-epoch launch
persisted 37C/37D continuation launch
in-process 38F typed continuation handoff
```

A persisted launch may retain its already-proven explicit overlay source as launch location context only.

An in-process handoff retains no path.

No nested plan path is promoted to launch provenance for the handoff family.

## Current-state advancement

The application projection supports pure current-state advancement while retaining the exact immutable launch-provenance object.

Controller-only visible continuation can advance:

- state kind;
- state source;
- current endpoint SHA-256.

Typed continuation advancement can additionally expose the declared continuation edge count.

Typed advancement must re-check the retained first-root and second-root identities against immutable launch provenance. A mismatch fails rather than rewriting the launch description.

## Textual reuse

The 39A Textual panel remains the visible widget, but its constructors and update methods now delegate to the shared application projection.

The widget becomes a renderer/state holder over the application model rather than the place where root and endpoint authority are derived.

Existing 39A launch/current behavior remains unchanged in meaning.

## Non-interactive CLI

39B adds:

```text
pyxis research-inspect
```

with exactly two mutually exclusive persisted entry families:

```text
--second-basis-epoch-overlay <path>
--second-basis-epoch-continuation-overlay <path>
```

Each CLI route uses the already-earned persisted authority chain:

```text
explicit path
→ strict configuration decode
→ fresh re-entry
→ 38B explicit path/result proof
→ shared authority projection
→ deterministic JSON serialization
```

No Textual import or launch occurs.

The CLI deliberately has no in-process-handoff option because 38F handoff authority exists only as an exact typed in-memory result. 39B does not invent durable handoff serialization.

## Deterministic JSON

The report format is:

`pyxis.chromium.research_second_basis_epoch_authority_inspection.v1`

Serialization is deterministic for one exact projection:

- stable field names;
- sorted JSON keys;
- fixed indentation;
- UTF-8 text semantics;
- one trailing newline.

The report includes:

- `report_role = read_only_inspection_not_authority`;
- immutable launch provenance;
- current governed state;
- an explicit negative-authority notice.

Path-distinct equivalent launches may legitimately differ in their `launch_location_context_only` value while retaining matching proven durable identities.

## Negative authority discipline

The report explicitly does not establish:

- evidence status;
- control-plane state;
- current/latest/head selection;
- path identity;
- branch or chronology authority;
- authorship;
- authenticity;
- trusted time;
- semantic support;
- citation authority;
- mutation/restart/checkpoint/browser authority.

SHA-256 values remain integrity / record-identity anchors only.

## Regression rules

39B adds tests requiring:

- deterministic repeated serialization;
- persisted launch path appears only as launch-location context;
- in-process projection has no path;
- current advancement retains the exact launch-provenance object;
- different root ancestry is rejected;
- invalid CLI configuration fails before report emission;
- CLI entry flags remain explicit and mutually exclusive;
- no discovery/latest/head/generic-overlay/handoff flag appears;
- `research-inspect` succeeds even when every `pyxis.ui` and `textual` import is actively forbidden.

## Not added

39B does not add:

- third evidence-basis epoch support;
- arbitrary-depth or recursive lineage schema;
- persistent handoff serialization;
- new persistence formats;
- new checkpoint APIs;
- automatic path reuse;
- evidence/browser behavior;
- mutation authority.

## Acceptance statement

If the executed test suite succeeds, 39B permits only this statement:

> The same already-proven second-epoch authority projection can be inspected interactively or emitted deterministically as non-interactive JSON. Both surfaces distinguish immutable launch provenance from current governed state, and neither report text, paths, nor hashes become a new authority source.
