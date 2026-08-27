# Milestone 41B — Dedicated third-epoch Textual launch shells

Status: proposed implementation pending executed test evidence.

Decision: D207

## Question

41A / D206 proved an application-layer launch authority for the concrete persisted third evidence-basis epoch: one explicit 40B or 40C/40D overlay location may be carried only when it is bound to the fresh matching three-root re-entry reconstructed from that exact location.

The next product question is deliberately narrower than checkpointing or three-root inspection:

> Can those already-proven 41A launch lineages enter the public `pyxis research-shell` path through dedicated Textual shell types without discarding launch provenance or inventing new persistence, restart, checkpoint, discovery, or authority semantics?

## Decision D207

Pyxis may expose explicit persisted third-epoch launch parity through two dedicated Textual shell types:

```text
ThirdBasisEpochResearchSessionShell
ThirdBasisEpochContinuationResearchSessionShell
```

Each shell accepts only its exact 41A proof-carrying lineage wrapper and mounts:

```text
lineage.reentry.controller
```

through the established `ResearchSessionShell` behavior.

The base shell receives no ordinary `ChromiumResearchSessionReentryResult`.

Therefore:

```text
shell.research_reentry is None
```

and 41B does not manufacture ordinary restart-plan authority from a third-epoch controller.

## Public launch families

`pyxis research-shell` gains two explicit mutually exclusive entry configurations:

```text
--third-basis-epoch-overlay
--third-basis-epoch-continuation-overlay
```

They join the existing explicit ordinary, root-backed, and second-epoch entry families. No discovery or format autodetection is introduced.

### Persisted 40B third epoch

The launch sequence is:

```text
explicit --third-basis-epoch-overlay
        ↓
strict 40B configuration decode
        ↓
fresh 40A third-epoch re-entry
        ↓
41A re-proves exact path/result relationship
        ↓
ChromiumResearchThirdBasisEpochShellLineage
        ↓
ThirdBasisEpochResearchSessionShell
```

### Persisted 40C / cumulative 40D continuation

The launch sequence is:

```text
explicit --third-basis-epoch-continuation-overlay
        ↓
strict 40C-format configuration decode
        ↓
fresh 40C continuation re-entry
        ↓
41A re-proves exact path/result relationship
        ↓
ChromiumResearchThirdBasisEpochContinuationShellLineage
        ↓
ThirdBasisEpochContinuationResearchSessionShell
```

40D deliberately retained the unchanged 40C continuation-overlay format and re-entry family. Therefore cumulative 40D checkpoints launch through the same continuation shell and do not receive a new product type.

## Second reconstruction is deliberate

The CLI first reconstructs the explicit configuration in order to obtain an already-earned typed result.

41A then reconstructs the exact supplied location again and returns the fresh result that has actually proven the path/result pairing.

The dedicated shell receives only the latter.

Therefore:

```text
caller-owned re-entry
+
caller-supplied path
!=
launch authority
```

until the 41A proof succeeds.

## Launch lineage remains launch context

Each shell retains the exact 41A wrapper unchanged:

```text
explicit persisted source
↕ freshly proven relationship
fresh launched re-entry
```

The generic base shell still permits already-earned governed operations such as endpoint revision and explicit rollover.

If those operations move the live in-memory controller, 41B does not rewrite the retained launch lineage.

Therefore:

```text
launch lineage != implicit current persisted lineage
```

and:

```text
live in-memory continuation != proven checkpoint
```

This is the same authority distinction that was proven before second-epoch checkpoint UI was introduced.

## Reuse before invention

41B deliberately reuses the established second-epoch product-launch pattern from 38C rather than creating a new UI architecture.

The new shells are thin lineage-retaining wrappers around `ResearchSessionShell`.

They do not duplicate:

- session presentation;
- endpoint revision controls;
- rollover behavior;
- persistence logic;
- re-entry logic; or
- browser research logic.

The only new product responsibility is retaining the stronger 41A launch provenance while mounting the already-earned governed controller.

## UI authority retained

The dedicated shells expose only the generic governed session surface inherited from `ResearchSessionShell`.

41B adds no:

- ordinary restart-plan controls;
- third-epoch first-checkpoint controls;
- cumulative third-epoch checkpoint controls;
- automatic persistence;
- path prefilling;
- in-process handoff;
- three-root authority-inspection panel.

The focused UI tests also prove that ordinary endpoint revision and rollover may move the live controller while the retained launch wrapper remains unchanged.

## CLI authority

The two new CLI routes must not fall back to:

- the ordinary re-entry-aware shell;
- either root-backed shell family;
- either second-basis-epoch shell family; or
- the generic controller-only shell.

They route only through the dedicated third-epoch shell factories after successful 41A proof.

The optional Textual dependency remains lazily imported. Import failure for Textual must still produce the established `pyxis[ui]` installation guidance rather than making UI a core dependency.

## Inspection remains separate

41B does not extend `pyxis research-inspect`.

Second-epoch authority inspection remains the only currently earned inspection product surface.

Third-epoch launch parity does not imply that a three-root authority projection or report already exists. That requires its own milestone.

## Path discipline

Paths remain explicit operational location context only.

41B adds no:

- directory scan;
- filename inference;
- moved-file search;
- predecessor discovery;
- format guessing;
- path identity;
- current/latest/head path selection.

A path-distinct overlay is usable only if the existing 41A proof freshly reconstructs and matches the earned lineage.

## Integrity discipline

Any SHA-256 identities used by the established re-entry and 41A proof boundaries remain integrity / durable record-identity facts only.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

## Failure behavior

Public launch fails before UI when:

- the explicit 40B or 40C/40D overlay cannot be decoded;
- referenced durable evidence cannot be freshly reconstructed;
- the 41A path/result proof fails;
- the supplied shell lineage is the wrong typed family; or
- the optional UI dependency is unavailable.

Failure grants no discovery fallback, alternate family routing, or controller-only launch.

## Non-goals

41B does not add:

- third-epoch checkpoint controls;
- cumulative third-epoch checkpoint UI;
- automatic checkpoint persistence;
- path prefilling;
- in-process handoff;
- three-root authority-inspection UI or JSON report;
- new persistence formats;
- another evidence-basis epoch;
- generic `epoch[n]` lineage;
- arbitrary-depth ancestry;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 41B permits only this statement:

> Pyxis can launch one explicitly persisted third evidence-basis epoch or post-third-root continuation through `pyxis research-shell` while retaining the exact 41A proof-carrying launch lineage inside a dedicated Textual shell. Cumulative 40D overlays use the same continuation launch family. The shells expose only the already-earned generic governed session surface and add no third-epoch checkpoint, inspection, discovery, or stronger path authority.
