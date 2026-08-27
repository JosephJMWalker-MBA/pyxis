# Milestone 43C — bounded cumulative visible-promotion kernel

Decision: **D215**

43C is a refactor milestone. It adds no new research authority, persistence authority, ancestry model, or evidence-basis epoch.

## Why this extraction is now justified

Three independently earned cumulative continuation products already proved the same post-proof Textual transition:

- 36C / D188 — root-backed 35D/35E cumulative continuation;
- 38E / D198 — second-basis-epoch 37C/37D cumulative continuation;
- 41D / D209 — third-basis-epoch 40C/40D cumulative continuation.

Their authority checks are intentionally different. Their **visible promotion procedure after those checks succeed** is not.

The repeated sequence is:

```text
concrete checkpoint proof succeeds
        ↓
concrete old form locks
        ↓
exact fresh re-entry/controller retained
        ↓
rebuild presentation from retained loaded evidence
        ↓
require rebuilt presentation == controller presentation
        ↓
validate declared sequence
        ↓
snapshot one working-set context per declared position
        ↓
remove one-hop sequence + locked revision + rollover + concrete form
        ↓
remove stale rollover receipt if present
        ↓
advance live controller/session/presentation/context state
        ↓
clear ordinary rollover/restart state
        ↓
advance concrete typed re-entry + last-checkpoint state
        ↓
mount concrete success receipt + fresh cumulative sequence
        ↓
unlock endpoint revision + mount empty rollover
```

43C extracts only that procedure.

## New private UI procedure

The private module is:

```text
src/pyxis/ui/chromium_research_cumulative_checkpoint_promotion_textual.py
```

Its two private implementation objects are:

```python
_CumulativeCheckpointPromotionSpec
_promote_cumulative_checkpoint_surface(...)
```

The module exports no public authority surface.

## Concrete responsibility remains concrete

The private promotion procedure does **not** decide whether a cumulative checkpoint is valid.

Before it is called, each existing shell still performs its original family-specific work.

### Root-backed 35E

The root-backed shell still owns:

- exact current typed 35D/35E continuation identity;
- exact rollover identity;
- fixed direct 35C anchor preservation;
- terminal edge SHA-256 equality;
- terminal revised-note text equality;
- retained root identity;
- root-backed persistence error wording.

### Second epoch 37D

The second-epoch shell still owns:

- exact current typed 37C/37D continuation identity;
- exact rollover identity;
- direct 37B anchor preservation;
- terminal edge SHA-256 equality;
- terminal revised-note text equality;
- second-epoch anchor presentation and endpoint identity;
- retained first- and second-root identities;
- second-epoch persistence/error wording.

### Third epoch 40D

The third-epoch shell still owns:

- exact current typed 40C/40D continuation identity;
- exact rollover identity;
- direct 40B anchor preservation;
- terminal edge SHA-256 equality;
- terminal revised-note text equality;
- third-epoch anchor presentation and endpoint identity;
- retained first-, second-, and third-root identities;
- third-epoch persistence/error wording.

Those checks are not callbacks inside a generic ancestry engine. They remain concrete code in the concrete shell modules.

## Concrete promotion specs

Each shell supplies one private concrete promotion spec containing only surface facts:

```text
checkpoint-controls selector
checkpoint-controls widget type
success-receipt DOM id
presentation-coherence error text
context-cardinality error text
```

The helper does not interpret those values.

It does not know whether a selector belongs to 35E, 37D, or 40D.

It does not know how many roots exist.

It does not know which anchor field was proved before entry.

## State advancement boundary

The important ordering remains:

```text
proof
→ lock old form
→ validate fresh presentation
→ remove old visible one-hop surface
→ advance current state
→ mount fresh cumulative surface
→ unlock revision
```

Hidden typed state therefore still cannot outrun the visible cumulative presentation.

The concrete shells provide two narrow state callbacks:

```text
advance exact family current re-entry
record exact family checkpoint result
```

The common live research-controller/session/presentation/context fields are advanced by the private procedure at the same transition.

This is mechanical state placement, not ancestry interpretation.

## Paths remain non-authoritative

43C reads no path and carries no path.

All four cumulative path inputs remain owned by the concrete save handlers and the 43B concrete form adapters.

No prior path becomes:

- current authority;
- latest authority;
- head authority;
- durable identity;
- chronology;
- branch membership.

## Relationship to 43A and 43B

The bounded extraction stack is now:

```text
43A / D213
private application procedure for fixed-anchor cumulative extension mechanics

43B / D214
private Textual form mechanics for four blank explicit paths + old-form locking

43C / D215
private post-proof visible cumulative promotion mechanics
```

The concrete families still surround all three kernels with their own earned authority semantics.

This is not an `epoch[n]` architecture.

## Why the whole cumulative shell is not generic

Significant differences remain outside the extracted procedure:

- root-backed cumulative launch directly accepts an exact typed re-entry;
- second- and third-epoch persisted launches retain explicit launch-lineage wrappers;
- second- and third-epoch raw handoff constructors are distinct from persisted launch constructors;
- root/epoch ancestry proofs differ materially;
- first-checkpoint families differ from cumulative families;
- inspection provenance differs by launch family.

Therefore 43C does not introduce a generic cumulative shell superclass or mixin.

## Falsifiability

Focused 43C coverage proves that all three existing concrete promotion methods call the private procedure while supplying:

- the exact concrete `fresh_reentry`;
- the exact concrete checkpoint result;
- the correct concrete promotion spec;
- the concrete success receipt;
- callbacks that update only the family's current typed re-entry and last cumulative checkpoint fields.

The mature mounted UI suites remain the stronger behavioral authority for:

- presentation coherence;
- sequence/context cardinality;
- exact DOM removal and remount behavior;
- rollover receipt removal;
- typed/current-state advancement;
- success receipt visibility;
- revision unlocking;
- repeatable cumulative cycles;
- failure-state preservation.

## Deliberate non-goals

43C adds none of the following:

- checkpoint persistence changes;
- 43A kernel changes;
- 43B form changes;
- save-handler abstraction;
- rollover-mount abstraction;
- CSS abstraction;
- cumulative handoff abstraction;
- constructor abstraction;
- generic shell lineage;
- generic ancestry traversal;
- fourth evidence-basis epoch;
- arbitrary-depth `epoch[n]`;
- recursive continuation-overlay ancestry;
- new durable format;
- CLI behavior;
- discovery or path prefilling;
- global latest/current/head authority;
- chronology or branch authority;
- authorship, authenticity, or trusted-time authority;
- semantic-support or citation authority.

## Result

43C removes one more triply-proven piece of duplicated mechanics while preserving the architectural rule established by the concrete milestones:

> reusable procedure may be shared only after the authority semantics that surround it remain explicit and independently falsifiable.
