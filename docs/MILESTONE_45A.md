# Milestone 45A — Visible One-Root Authority Inspection Parity

Decision: D226

## Product question

44H / D225 completes the first changed-basis product loop by explicitly handing an exact freshly proven 35C root-backed re-entry into the established root-backed product.

That exposes an older observability asymmetry:

- second- and third-epoch products visibly separate immutable launch provenance from mutable governed state;
- one-root products do not;
- persisted 35C and 35D/35E CLI launches have an explicit caller-supplied launch path;
- 44H and 36D in-process typed handoffs correctly have no persistent launch path.

45A asks whether already-earned one-root authority can become visibly inspectable without changing the authority itself.

45A answers **yes**.

The governing distinction is:

```text
immutable root-backed launch provenance
!=
mutable current governed state
```

## Internal prior art and reuse

Internal prior art is decisive:

- 39A / D200 established visible second-epoch authority inspection;
- 39B / D201 separated its UI-independent projection from rendering;
- 42A / D211 proved the same pattern through three-root products, including raw in-process launch families with no path;
- persisted second-/third-epoch launch-lineage wrappers prove an explicit path by fresh reconstruction rather than treating path equality as identity;
- 36D / D189 and 44H / D225 prove that typed in-process handoff does not create persistent path authority.

45A therefore instantiates that proven pattern concretely for one-root authority. It does not introduce a generic ancestry/epoch inspection abstraction or a new external subsystem.

Conclusion remains:

> **no end-to-end substitute demonstrated in this review**

## Four exact launch families

45A supports exactly four already-earned entry families.

### Persisted 35C root-backed launch

The caller supplies the exact 35C overlay path.

Pyxis strictly decodes that path, freshly reconstructs root-backed state, and requires the fresh result to match the already-earned result on:

- governed presentation;
- declared endpoint durable SHA-256; and
- retained 34A root SHA-256.

Only then is the explicit resolved path retained as launch location context.

### In-process 44H root-backed handoff

44H supplies an exact `ChromiumResearchRootBackedSessionReentryResult`.

No persistent launch path exists in that transition. The inspection projection therefore records `None` and visibly says that no persistent launch path exists.

The earlier 44G destination is not backfilled.

### Persisted 35D/35E continuation launch

The caller supplies the exact root-backed continuation overlay path.

Pyxis strictly decodes and freshly reconstructs continuation state, then requires matching:

- governed continuation presentation;
- declared endpoint durable SHA-256;
- retained prior root-backed presentation/endpoint; and
- retained 34A root SHA-256.

Only then is the explicit resolved continuation path retained as launch context.

### In-process 36D continuation handoff

36D supplies an exact `ChromiumResearchRootBackedSessionContinuationReentryResult`.

No persistent launch path exists. The inspection projection therefore records no path, and later checkpoint destinations never retroactively become launch provenance.

## Proof-carrying persisted launch wrappers

45A adds two concrete frozen launch-lineage types:

```text
ChromiumResearchRootBackedSessionShellLineage
ChromiumResearchRootBackedSessionContinuationShellLineage
```

Each contains exactly:

```text
overlay_source
fresh reentry reconstructed from that explicit source
```

The wrapper does not carry latest/current/head, checkpoint selection, chronology, discovery, semantic support, or path-identity claims.

A moved but durably equivalent explicit source may be valid after fresh proof. Path equality itself is never authority.

## UI-independent inspection projection

45A adds one application-owned frozen projection with two parts.

### Immutable launch provenance

- launch family;
- `Path | None` launch location context;
- retained 34A root SHA-256;
- launch endpoint SHA-256.

### Current governed state

- state kind;
- state source;
- current endpoint SHA-256;
- declared continuation-edge count when represented by an exact typed continuation.

The projection performs no file I/O, persistence, restart, checkpoint, mutation, browser work, discovery, or authority selection.

## Current-state advancement

A first-checkpoint root-backed shell may roll over to one visible post-root continuation.

That updates only the current governed-state projection. The launch-provenance object remains the exact same object.

A cumulative continuation shell may later complete a successful 35E checkpoint promotion.

Before the projection accepts the fresh typed continuation, its retained root SHA-256 must equal immutable launch provenance. The current endpoint and declared continuation-edge count may then advance while launch provenance remains unchanged.

A rollover awaiting 35E proof does not itself fabricate a new typed cumulative continuation projection.

## Textual adapters

45A adds inspection-aware subclasses around mature root-backed product shells rather than changing their checkpoint authority:

- persisted 35C first-checkpoint shell;
- raw 44H first-checkpoint shell;
- persisted 35D/35E cumulative continuation shell;
- raw 36D cumulative continuation shell.

The panel only renders the application projection and performs no file read or independent proof.

Existing 35D and 35E controls, persistence APIs, button IDs, locking rules, and promotion behavior remain owned by their established shells.

## Product routing

Existing product routes now preserve the launch distinction explicitly.

```text
research-shell --root-backed-overlay PATH
→ strict load/re-entry
→ prove PATH against fresh matching 35C state
→ persisted inspectable root-backed shell
→ optional explicit 36D typed handoff
→ raw inspectable continuation shell with no path
```

```text
research-shell --root-backed-continuation-overlay PATH
→ strict load/re-entry
→ prove PATH against fresh matching 35D/35E state
→ persisted inspectable continuation shell
```

The bounded 44H runner now passes its exact typed handoff into the raw inspectable root-backed receiver, which records no persistent path.

No new CLI flag is introduced.

## Falsifiability

Focused coverage proves at minimum:

1. an explicit persisted 35C path is retained only through fresh matching reconstruction;
2. a path-distinct but durably equivalent 35C configuration can be accepted when explicitly supplied and freshly proven;
3. different or tampered persisted 35C state rejects before lineage is returned;
4. persisted launch wrappers contain only explicit source plus fresh typed result;
5. raw 44H launch visibly carries no persistent path;
6. persisted 35D/35E and raw 36D launches preserve their distinct path semantics;
7. persisted CLI routes pass proof-carrying lineage objects into inspection-aware shells;
8. a raw root-backed re-entry is rejected at the persisted-shell runner boundary;
9. explicit 36D handoff does not reload a continuation overlay;
10. normal close does not implicitly enter cumulative mode;
11. rollover preserves the exact launch-provenance object while current endpoint/state advances;
12. successful 35E promotion preserves the exact launch-provenance object while typed current state and edge count advance;
13. a continuation from a different retained root is rejected by the projection; and
14. the authority notice remains explicitly read-only and negative about evidence, mutation, discovery, latest/current/head, authorship, authenticity, trusted time, semantic support, and citation authority.

## Scope

45A changes only:

- one concrete one-root launch-lineage application module;
- one concrete one-root authority-inspection application module;
- one Textual inspection renderer;
- one additive root-backed inspection-adapter module;
- narrow `pyxis.ui` exports;
- existing one-root CLI orchestration;
- the bounded 44H receiving factory;
- focused application, UI, and routing tests; and
- this milestone record.

45A does not alter the existing 35B/35C/35D/35E persistence formats or proof boundaries.

## Non-goals

No deterministic one-root `research-inspect` JSON report yet, no new CLI locator flag, no new persistence format, no automatic restart or mode promotion, no second changed-basis productization, no fourth evidence-basis epoch, no generic `epoch[n]`, no generic authority-inspection superclass/model, no arbitrary-depth ancestry, no path discovery or prefill, no latest/current/head selection, no chronology or branch authority, no path identity, no authorship/authenticity/trusted-time authority, no semantic-support or citation authority, no browser reacquisition, and no autonomous research behavior.

## What successful 45A proves

Successful 45A establishes only:

> Already-earned one-root root-backed authority can carry visible, immutable launch provenance across persisted and in-process product entry families while current governed state continues to move through established rollover and checkpoint behavior. Explicit persisted launch paths survive only as proof-bound launch context, raw typed handoffs visibly carry no persistent path, and neither representation creates discovery, path identity, restart, latest/current/head, or new research authority.
