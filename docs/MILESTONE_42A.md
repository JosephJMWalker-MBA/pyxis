# Milestone 42A — Visible third-epoch authority inspection

Status: proposed implementation pending executed test evidence.

Decision: D211

## Question

Milestones 41A–41E made the concrete three-root operational family usable through:

- proven persisted 40B launch;
- first proof-gated 40C checkpoint;
- repeatable persisted 40C/40D cumulative continuation;
- explicit in-process handoff from the first checkpoint into cumulative mode.

The missing product question is observability.

A researcher needs to be able to see what authority the shell actually retains without a read-only display accidentally becoming a new authority source.

## Decision D211

Pyxis adds a read-only three-root authority inspection projection and renders it in the current third-epoch Textual product shells.

The projection visibly separates:

```text
immutable launch provenance
        !=
current governed state
```

and preserves the existing rule:

```text
path location context
        !=
durable identity or current authority
```

The inspection performs no file reads, overlay reload, path proof, discovery, persistence, restart, checkpoint, browser access, or authority promotion.

## Prior art used

42A deliberately follows the mature second-epoch inspection architecture established by 39A / D200 and refined by 39B / D201.

The reusable pattern is:

```text
already-proven launch/re-entry object
        ↓
UI-independent read-only authority projection
        ↓
Textual renderer
        ↓
inspection-aware shell adapter
```

The second-epoch implementation demonstrated several important boundaries that 42A preserves:

- launch provenance remains immutable while current state advances;
- persisted launch paths are displayed only as location context;
- an in-process typed handoff has no persistent launch path;
- cumulative promotion updates only current typed state;
- a later checkpoint path never backfills into prior launch provenance;
- SHA-256 anchors establish integrity / record identity only.

No external dependency or new subsystem is needed. The mature internal implementation already solves the relevant inspection job; 42A extends that pattern by one concrete root rather than inventing a generalized recursive lineage model.

## Application-side projection

`chromium_research_third_basis_epoch_authority_inspection.py` defines three immutable records:

```text
ThirdBasisEpochLaunchProvenanceInspection
ThirdBasisEpochCurrentGovernedStateInspection
ThirdBasisEpochAuthorityInspection
```

Launch provenance contains:

- launch family;
- launch location context (`Path | None`);
- first-root SHA-256;
- second-root SHA-256;
- third-root SHA-256;
- launch endpoint SHA-256.

Current governed state contains:

- state kind;
- state source;
- current endpoint SHA-256;
- declared continuation edge count when represented as a typed continuation.

The projection is intentionally UI-independent so the meaning of the authority display is not defined by Textual widgets.

## Three explicit launch families

42A supports exactly the already-earned concrete third-epoch launch families.

### Persisted 40B launch

Input authority:

```text
ChromiumResearchThirdBasisEpochShellLineage
```

The projection records the proven 40B overlay location as launch context and extracts all three retained root identities from the freshly proven re-entry.

Initial current state is the third-basis-epoch session itself.

### Persisted 40C/40D continuation launch

Input authority:

```text
ChromiumResearchThirdBasisEpochContinuationShellLineage
```

The projection records the proven continuation overlay location as launch context, the three root identities, the launch endpoint, and the current typed continuation edge count.

### In-process 41E handoff

Input authority:

```text
ChromiumResearchThirdBasisEpochContinuationReentryResult
```

The launch location is explicitly `None`.

The inspection says that there is no persistent launch path because the current process already holds the exact typed continuation freshly earned by the successful 40C checkpoint.

No saved overlay path is inferred or reconstructed from that typed state.

## Advancing current state

### Visible one-hop rollover from 40B

The first-checkpoint product shell may update only the current-state portion after an explicit 30A rollover.

Launch provenance remains the exact same object.

The current state is described as:

```text
visible one-hop continuation
explicit rollover from persisted 40B launch
```

That update does not assert restartability or persisted continuation authority.

### Typed cumulative promotion

A persisted or raw-handoff cumulative shell updates current state only after the existing 41D proof-gated cumulative checkpoint succeeds and promotes its fresh typed continuation.

Before accepting the new projection, the application helper re-checks:

```text
first root  == immutable launch first root
second root == immutable launch second root
third root  == immutable launch third root
```

A mismatch is rejected rather than rendered as a legitimate current state.

The inspection adapter additionally requires the exact immutable launch-provenance object to survive the shell promotion by object identity.

## Textual rendering

`ThirdBasisEpochAuthorityInspectionPanel` renders two visibly separate sections:

```text
Immutable launch provenance
Current governed state
```

The panel shows all three root SHA-256 anchors and the launch/current endpoint anchors.

Its authority notice states that:

- displayed paths are launch location context only;
- no path represents current/latest/head authority;
- SHA-256 anchors do not prove authorship, authenticity, trusted time, chronology, semantic support, or citation authority;
- the panel grants no mutation, restart, checkpoint, discovery, browser, or path authority.

## Product shell adapters

42A adds inspection-aware adapters around the already-earned 41C/41D/41E behavior:

```text
InspectableThirdBasisEpochCumulativeHandoffResearchSessionShell
InspectableThirdBasisEpochContinuationResearchSessionShell
InspectableThirdBasisEpochContinuationHandoffResearchSessionShell
```

The older milestone factories remain valid historical boundaries. The current CLI opts into the inspection-aware adapters.

This is the same additive productization pattern used by 39A.

## CLI boundary

The current `research-shell` launch factories now select the inspection-aware third-epoch adapters for:

- `--third-basis-epoch-overlay`;
- `--third-basis-epoch-continuation-overlay`;
- the exact raw in-process 41E continuation handoff.

The decode, fresh re-entry, 41A path/result proof, checkpoint, and handoff boundaries are unchanged.

`research-inspect` remains second-epoch-only in 42A.

No third-epoch deterministic serialization format or command-line inspection route is added here. That remains the clean 42B seam.

## Failure behavior

The inspection surface never repairs or guesses authority.

A typed continuation whose retained first-, second-, or third-root identity does not match immutable launch provenance is rejected.

A path supplied later for cumulative checkpointing does not alter launch provenance. This is especially important for raw 41E handoff mode, where launch path remains absent even after the researcher explicitly supplies a persisted continuation path for a later checkpoint.

## Authority deliberately not added

42A adds no claim about:

- latest/current/head persisted state;
- branch or chronology authority;
- path identity;
- discovery or format guessing;
- fourth evidence-basis epochs;
- generic `epoch[n]` or arbitrary-depth lineage;
- authorship or authenticity;
- trusted time;
- semantic support;
- citation authority.

No persistence format, checkpoint API, browser layer, or research evidence loader changes.

## Acceptance statement

If the executed test suite succeeds, 42A permits only this statement:

> A researcher launching any currently supported third-epoch product shell can visibly inspect the three retained root identities, immutable launch context, and current governed endpoint/state without the inspection itself reading, proving, mutating, discovering, persisting, or promoting authority. Persisted paths remain location context only, raw 41E handoff retains no launch path, and cumulative promotion may update current state only while all three immutable launch-root identities remain fixed.
