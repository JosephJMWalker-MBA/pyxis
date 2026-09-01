# Milestone 47A — Explicit third changed-basis transition

> **Decision:** D235  
> **Issue:** #190  
> **Base frontier:** completed 46A–46G second changed-basis product flow

## Product result

47A exposes one additional concrete public 33B crossing from an exact governed second-basis-epoch continuation.

```text
exact current ChromiumResearchSecondBasisEpochContinuationReentryResult
+ explicit successful generic 44A preparation for that exact controller
+ caller-explicit current durable locators
→ one public 33B third changed-basis transition
→ public no-overwrite transition persistence
→ fresh public 33B relink
```

The transition remains historical evidence. Persistence does not change the mounted governed controller, current second-epoch continuation, launch provenance, or product mode.

```text
47A transition
!= third 34A revision root
!= post-third-root edge
!= third-epoch declared session
!= 40A fresh re-entry
!= 40B restart overlay
!= automatic third-epoch adoption
!= arbitrary-depth epoch abstraction
```

## Why 47A is a separate frontier

46G completed the second changed-basis product seam. Its exact typed handoff enters a second-basis-epoch product that already owns:

```text
37C first continuation checkpoint
→ explicit 38F in-process cumulative-mode handoff
→ repeatable 37D cumulative checkpointing
```

No further 46-series runtime seam was demonstrated.

The next distinct job is initiation of a third changed evidence basis from an exact active second-epoch continuation. Lower-level 40-series code already proves that a complete third epoch can later be reconstructed above persisted 37C/37D ancestry, but that machinery begins from durable third-transition/root artifacts. It does not create the product-side third crossing.

## Prior art and reuse

### Internal Pyxis prior art

47A deliberately reuses:

- generic 44A changed-basis preparation from `ResearchSessionShell`;
- 46A / D228 as the exact concrete product precedent for a later 33B crossing;
- public 33B transition creation, persistence, and fresh loading;
- exact current `ChromiumResearchSecondBasisEpochContinuationReentryResult` retained by 37C/37D and raw 38F continuation products;
- existing second-epoch authority inspection for immutable launch provenance versus mutable governed state;
- lower-level 40-series third-epoch reconstruction as evidence that this concrete ancestry shape is coherent, without treating 40A as the product crossing itself.

No generic `transition[n]`, `epoch[n]`, recursive ancestry container, or arbitrary-depth product abstraction is introduced.

### External prior art reviewed before implementation

The decision review considered W3C PROV, DVC, DataLad, and Renku. Those systems provide mature provenance, dataset versioning, workflow dependency, experiment, and reproducibility capabilities. They remain useful conceptual or integration prior art.

The review did not demonstrate an end-to-end substitute for this exact Pyxis authority job: a human-authorized evidence-basis crossing from one active governed second-epoch continuation, preserving exact retained ancestry, requiring caller-owned durable locators, and refusing ambient current/latest/head selection.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Exact application authority

`persist_chromium_research_third_changed_basis_transition(...)` requires exactly:

```text
ChromiumResearchSecondBasisEpochContinuationReentryResult
```

The supplied continuation must retain the supplied controller by exact object identity:

```text
continuation_reentry.controller is controller
```

Structural or presentation equivalence is intentionally insufficient for this in-process action. Focused tests freshly reconstruct an equivalent second-epoch continuation and prove rejection because its controller is a different object.

The successful 44A preparation must also belong to the supplied controller:

```text
prepared.prior_session == controller.presentation
prepared.prior_endpoint is controller.declared_endpoint
```

Foreign-session and forged-endpoint preparations are rejected before transition persistence.

## Public 33B remains authoritative

47A does not implement a new transition record or persistence format.

The application adapter calls the existing public boundaries:

```text
create_chromium_research_session_working_set_transition
persist_chromium_research_session_working_set_transition
load_chromium_research_session_working_set_transition
```

After persistence, 47A adds only bounded coherence checks:

- persistence retains the exact in-memory transition object;
- fresh loaded transition SHA matches persisted transition SHA;
- fresh predecessor endpoint identity matches the exact supplied controller endpoint;
- fresh successor working-set SHA matches the exact preparation persistence;
- fresh successor note SHA matches the exact preparation persistence.

## Explicit locator discipline

The 47A UI mounts four blank fields only after one new successful 44A preparation:

1. current prior endpoint edge source;
2. current prepared working-set source;
3. current prepared working-set-note source;
4. no-overwrite third-transition destination.

Preparation receipts are displayed only as context. They are not copied into the fields.

Focused tests move the prepared working-set and note artifacts after 44A and prove that 47A succeeds only when the caller explicitly supplies the new current locations.

Wrong prior-edge, working-set, or note locators reject without a successful destination. Existing transition destinations remain untouched under no-overwrite failure.

```text
previous successful path
!= continuing locator authority
```

## Dedicated product surfaces

47A does not widen the established second-epoch continuation shells automatically.

Four concrete factories are provided:

- path-proofed persisted 37C/37D continuation product;
- exact pathless raw 38F continuation-handoff product;
- inspectable persisted product;
- inspectable raw handoff product.

All four reuse one private 47A-specific behavior mixin. The mixin is not a generic Nth-epoch abstraction; it only avoids duplicating the exact third-transition UI orchestration across the two already-distinct launch families.

The plain established second-epoch continuation shell still performs generic 44A preparation without gaining a 47A transition form.

## Staleness and historical authority

Before persistence, 47A is bound to the exact controller/endpoint that owned the successful 44A preparation.

If an explicit rollover changes the mounted second-epoch controller before the third transition is saved:

```text
unsaved 47A form → stale and locked
```

It is never silently retargeted.

After successful transition persistence, the relationship changes:

```text
successful 47A result → durable historical transition authority
```

A later second-epoch rollover may advance the mounted controller, but the exact retained 47A result remains unchanged and its successful form does not become stale.

## Launch-provenance preservation

47A persistence does not alter launch provenance or current governed state.

For a persisted 37C/37D launch:

- the exact inspection `launch_provenance` object remains object-identical;
- its explicit launch location context remains unchanged;
- inspection current state remains unchanged by 47A persistence.

For a raw 38F handoff:

- the exact inspection `launch_provenance` object remains object-identical;
- launch location context remains `None`;
- the exact raw handoff re-entry remains retained;
- inspection current state remains unchanged by 47A persistence.

No path is fabricated for the in-process launch family.

## Focused falsification coverage

47A tests cover:

- valid exact-type application persistence and fresh public 33B relink;
- wrong continuation type rejection;
- structurally equivalent freshly reconstructed controller rejection by object identity;
- foreign-session preparation rejection;
- forged exact-endpoint preparation rejection;
- moved preparation artifacts accepted only through caller-supplied current paths;
- wrong prior-edge / working-set / note locator rejection;
- no-overwrite destination preservation;
- UI absence before successful 44A preparation;
- four blank transition locator inputs after preparation;
- successful transition persistence without mounted-state adoption;
- unsaved transition staleness after branch-changing rollover;
- persisted transition survival as historical authority after later rollover;
- persisted launch-provenance object identity preservation;
- raw 38F pathlessness and launch-provenance object identity preservation;
- plain second-epoch continuation products do not acquire 47A implicitly;
- product factories reject the wrong authority family.

## Explicit non-goals

47A introduces no:

- third 34A revision root;
- first post-third-root ordinary edge;
- third-epoch declared-session adoption;
- 40A fresh-process reconstruction;
- 40B restart overlay;
- third-epoch typed handoff;
- fourth evidence-basis epoch;
- generic Nth transition/epoch abstraction;
- recursive ancestry schema;
- CLI flag or existing CLI lifecycle change;
- persistence-format change;
- locator discovery or prefill;
- directory scanning or predecessor discovery;
- global current/latest/head selection;
- chronology or path-identity authority;
- browser reacquisition;
- semantic-support or citation authority;
- autonomous research.

## Validation gate

The implementation is accepted only after Repository Zero passes the complete suite on Python 3.11, 3.12, 3.13, and 3.14 against one exact PR head.

Executable implementation, focused tests, and executed CI remain stronger authority than this milestone summary.
