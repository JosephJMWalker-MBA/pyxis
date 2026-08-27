# Milestone 43A — bounded fixed-anchor cumulative continuation kernel

## Decision D213

Milestones 35E, 37D, and 40D independently proved the same cumulative continuation mechanics above three different concrete ancestry families.

43A extracts only those now-triply-proven mechanics into one private application-layer kernel.

It does **not** generalize Pyxis into an arbitrary-depth evidence-basis epoch model.

This is a refactor milestone, not a new authority milestone.

## Why extraction is justified now

The earlier refusal to create a generic `epoch[n]` abstraction remains correct.

At 40A / D202, the system had not yet earned a claim that evidence-basis ancestry itself was generic. The first, second, and third evidence-basis compositions retained materially different concrete state and proof obligations.

After 40D, however, a narrower repetition has been demonstrated independently three times:

```text
35E
fixed 35C anchor
+ cumulative post-root edge tuple

37D
fixed 37B anchor
+ cumulative post-second-root edge tuple

40D
fixed 40B anchor
+ cumulative post-third-root edge tuple
```

Their ancestry semantics differ.

Their extension procedure does not.

That narrower procedural repetition is the only thing extracted in 43A.

## Shared mechanical kernel

43A adds the private module:

```text
src/pyxis/app/chromium_research_fixed_anchor_cumulative_extension.py
```

Its private entry point executes the procedure already proven separately by 35E, 37D, and 40D:

```text
four explicit paths
→ destination-distinct / no-overwrite preflight
→ strict current overlay decode
→ fresh current re-entry
→ concrete current-state proof callback
→ concrete rollover-prior proof callback
→ append exactly one explicit successor
→ freshly relink the complete cumulative edge sequence
   from the concrete fixed anchor endpoint
→ prove terminal edge SHA-256
→ prove terminal note text
→ persist the cumulative 26B sequence declaration
→ construct the concrete next continuation plan
→ fresh next re-entry
→ concrete next-state proof callback
→ persist concrete continuation overlay
→ round-trip decode exact next plan
```

The kernel does not know:

- how many evidence-basis roots exist;
- what an evidence-basis epoch is;
- how concrete ancestry is represented;
- what durable continuation format a family uses;
- what fixed-anchor field a plan retains;
- how a concrete family proves ancestry equivalence.

Those remain adapter responsibilities inside the existing concrete modules.

## Existing public authority surfaces remain unchanged

The authority-facing functions remain:

```python
persist_chromium_research_root_backed_session_continuation_checkpoint_extension(...)

persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(...)

persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(...)
```

Their existing public result dataclasses and public error classes remain the same.

The private kernel exports nothing through `__all__`.

## Concrete 35E authority remains concrete

The root-backed wrapper still owns and proves:

- the supplied re-entry is the established 35D continuation type;
- the explicit decoded current overlay describes the exact supplied current plan;
- fresh current presentation equality;
- fresh current endpoint identity;
- retained root identity;
- rollover prior presentation and endpoint identity;
- direct anchoring to the retained 35C root-backed overlay;
- fresh cumulative endpoint SHA/text equality with the chosen rollover.

The exact-plan check remains intentionally stricter than the later epoch families.

## Concrete 37D authority remains concrete

The second-basis-epoch wrapper still owns and proves:

- the supplied re-entry is the established 37C continuation type;
- fresh current presentation and endpoint identity;
- second-epoch anchor presentation and endpoint identity;
- retained second-root identity;
- retained first-root identity;
- rollover prior presentation and endpoint identity;
- direct anchoring to the retained 37B overlay;
- fresh cumulative endpoint SHA/text equality with the chosen rollover.

A path-distinct but durably equivalent current continuation overlay remains acceptable only after fresh reconstruction proves that equivalence.

No path-equality authority is introduced.

## Concrete 40D authority remains concrete

The third-basis-epoch wrapper still owns and proves:

- the supplied re-entry is the established 40C continuation type;
- fresh current presentation and endpoint identity;
- third-epoch anchor presentation and endpoint identity;
- retained third-root identity;
- retained second-epoch continuation presentation and endpoint identity;
- retained second-root identity;
- retained first-root identity;
- rollover prior presentation and endpoint identity;
- direct anchoring to the retained 40B overlay;
- fresh cumulative endpoint SHA/text equality with the chosen rollover.

As in 37D, a path-distinct equivalent current overlay is accepted only through fresh durable proof.

## Fixed anchors remain family-specific

43A does not introduce a generic anchor record.

The plans continue to retain their concrete direct anchors:

```text
35E → prior_root_backed_overlay_source
37D → prior_second_basis_epoch_overlay_source
40D → prior_third_basis_epoch_overlay_source
```

A cumulative continuation overlay still does not become the ancestor of the next cumulative overlay.

The cumulative edge tuple grows while the concrete direct anchor remains fixed.

## Error and persistence compatibility

The public wrappers retain their existing error classes and established error wording for:

- current-overlay decode failure;
- fresh current reconstruction failure;
- ancestry mismatch;
- rollover ownership mismatch;
- sequence relink failure;
- terminal SHA mismatch;
- terminal text mismatch;
- fresh next reconstruction failure;
- next endpoint mismatch;
- overlay round-trip failure.

Destination collision and no-overwrite behavior remain unchanged.

No persistence or locator document format changes in 43A.

## Validation strategy

The strongest regression authority remains the existing concrete suites:

```text
test_app_chromium_research_root_backed_session_continuation_checkpoint_extension.py

test_app_chromium_research_second_basis_epoch_continuation_checkpoint_extension.py

test_app_chromium_research_third_basis_epoch_continuation_checkpoint_extension.py
```

Those suites continue to test their concrete ancestry and failure semantics without being rewritten around a generic model.

43A adds one focused parity test that:

- executes all three real extension families;
- proves all three public wrappers pass through the private mechanical kernel;
- proves each next plan retains its original concrete direct anchor;
- proves the kernel itself exposes no public authority surface.

## Deliberate non-authorities

43A does not add:

- a fourth evidence-basis epoch;
- `epoch[n]` or arbitrary-depth ancestry objects;
- recursive ancestry walkers;
- generic root-count logic;
- generic shell lineage;
- generic authority inspection;
- generic persistence formats;
- recursive continuation-overlay ancestry;
- CLI behavior;
- Textual behavior;
- browser or evidence behavior;
- discovery or implicit selection;
- latest/current/head authority;
- chronology or branch authority;
- path identity;
- authorship, authenticity, or trusted-time authority;
- semantic-support or citation authority.

## Architectural result

The resulting boundary is intentionally asymmetric:

```text
CONCRETE AUTHORITY SEMANTICS
35E / 37D / 40D wrappers
        ↓ callbacks
PRIVATE SHARED PROCEDURE
fixed-anchor cumulative extension kernel
        ↓
ESTABLISHED PRIMITIVES
26A relinking + 26B sequence declaration + concrete re-entry/persistence
```

That asymmetry is the point.

Pyxis now reuses what has actually been demonstrated reusable while refusing to claim that concrete evidence-basis ancestry itself is generic.
