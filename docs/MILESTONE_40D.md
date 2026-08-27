# Milestone 40D — Cumulative continuation above persisted third epoch

Status: proposed implementation pending executed test evidence.

Decision: D205

## Question

40C / D204 established one first restartable ordinary continuation above a persisted 40B third evidence-basis epoch.

40D asks the next narrower question:

> Can that ordinary post-third-root continuation be extended repeatedly while preserving the direct 40B ancestry anchor and all three retained roots, without recursively nesting continuation overlays?

This milestone is about repeatable ordinary continuation above one concrete three-root epoch. It does not generalize evidence-basis lineage depth.

## Decision D205

Pyxis may cumulatively extend a `ChromiumResearchThirdBasisEpochContinuationReentryResult` while continuing to use the existing 40C locator-overlay format:

```text
pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1
```

No new persistent format is introduced.

Each cumulative overlay still contains exactly:

```text
format
prior_third_basis_epoch_overlay_source
declared_edge_sources
declaration_source
```

The ordered edge tuple grows. The direct 40B anchor does not change.

## Direct-anchor rule

The required ancestry shape is:

```text
40B third-epoch overlay
        ↓
third epoch with retained first/second/third roots
        ↓
E1 → E2 → ... → En
```

It is not:

```text
40B
 ↓
40C(E1)
 ↓
40C(E2)
 ↓
40C(E3)
```

A cumulative next plan therefore retains:

```python
next_plan.prior_third_basis_epoch_overlay_source = (
    current_plan.prior_third_basis_epoch_overlay_source
)
```

and extends only:

```python
next_plan.declared_edge_sources = (
    *current_plan.declared_edge_sources,
    explicit_successor_source,
)
```

This prevents recursive continuation-overlay ancestry from becoming an implicit authority model.

## Fresh reconstruction order

`persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(...)` performs:

```text
explicit current 40C overlay
        ↓
strict configuration decode
        ↓
fresh current 40C re-entry
        ↓
fresh direct 40B re-entry
        ↓
first root re-earned
second root re-earned
third root re-earned
        ↓
current continuation matched
        ↓
chosen rollover matched to current endpoint
        ↓
current ordered post-third-root edges
        +
explicit chosen successor edge
        ↓
fresh cumulative relink from third-epoch endpoint
        ↓
new cumulative declaration
        ↓
new 40C-format plan with same direct 40B anchor
        ↓
fresh next re-entry
        ↓
strict next overlay
```

No directory scan, filename inference, sorting, predecessor search, or latest/current/head selection occurs.

## Current-state proof gate

A path supplied as `current_overlay_source` is location context only.

The current overlay is freshly decoded and re-entered before extension. The fresh current result must match the supplied typed continuation at the following layers:

```text
current continuation presentation
current continuation endpoint identity
third-epoch anchor presentation
third-epoch anchor endpoint identity
third-root identity
retained second-epoch continuation presentation
retained second-epoch continuation endpoint identity
second-root identity
first-root identity
```

This prevents a terminal-only comparison from hiding divergence in retained ancestry.

A path-distinct current overlay may be accepted only when this explicit fresh reconstruction proves the same durable governed state.

## Chosen-rollover proof

The supplied rollover must belong to the supplied current continuation.

Its prior controller must match:

```text
current continuation presentation
current continuation endpoint identity
```

The cumulative relinker then appends only the explicitly supplied `successor_edge_source`.

The newly relinked terminal edge must match the chosen rollover successor by:

```text
durable edge-record identity
exact final human note text
```

No sibling choice or successor discovery occurs.

## Why whole-presentation equality changes here

The one-hop rollover controller presents only its declared one-hop continuation.

The cumulative controller presents the complete retained post-third-root sequence:

```text
E1 → E2 → ... → En → En+1
```

Therefore the two whole presentations legitimately differ after cumulative extension.

40D does not force false whole-presentation equality. Instead, it proves that the cumulative result ends at exactly the human-chosen successor through terminal edge identity and exact note text.

This distinction was already necessary for cumulative continuation above the second root and remains necessary here.

## New cumulative declaration

The complete explicit cumulative edge sequence is freshly relinked from the freshly reconstructed third-epoch endpoint.

Only after that succeeds may Pyxis persist a new declaration for the complete sequence.

The declaration destination and next-overlay destination must:

- be explicitly supplied;
- be distinct paths;
- not already exist.

An existing output blocks the operation before the other durable output is written.

## Next-plan reconstruction

The next plan uses the existing 40C type:

`ChromiumResearchThirdBasisEpochContinuationReentryPlan`

It carries:

- the unchanged direct 40B third-epoch overlay location;
- the cumulative ordered edge tuple;
- the newly persisted cumulative declaration location.

The plan is then freshly re-entered through the public 40C re-entry boundary.

The fresh next terminal endpoint must match the chosen rollover continuation by:

```text
durable edge-record identity
exact final human note text
```

Only then may the next 40C overlay be written.

## Repeatability proof

40D is not satisfied merely by extending the first 40C checkpoint once.

The focused tests apply the same extension operation again to the freshly reconstructed cumulative result and its newly persisted overlay.

The second extension must still:

- retain the same direct 40B ancestry anchor;
- preserve all three root identities;
- extend the existing cumulative edge tuple by exactly one chosen successor;
- freshly reconstruct the new terminal state.

This is the distinction between a second special-case hop and a repeatable cumulative continuation mechanism.

## Configuration and authority

The existing 40C loader remains configuration-only.

A successfully decoded cumulative overlay proves only the exact locator shape. It does not by itself prove:

- evidence integrity;
- any root identity;
- restartability;
- governed state;
- chronology;
- branch identity;
- current/latest/head state.

Those facts are re-earned only by the fresh reconstruction path.

## Path discipline

Paths remain operational locations, not durable identity.

40D adds no:

- moved-file search;
- directory discovery;
- predecessor discovery;
- canonical path claim;
- current/latest/head path selection.

A wrong explicit path fails even when a correct-looking artifact exists nearby.

## Integrity discipline

SHA-256 identities used by existing loaders remain integrity / durable record-identity facts only.

They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- semantic support;
- citation authority.

The 40C-format overlay stores no ancestry hashes.

## Failure behavior

40D must fail without creating its new durable outputs when:

- the current 40C overlay cannot be decoded;
- the current 40C overlay cannot freshly re-enter;
- the fresh current state differs from the supplied typed continuation;
- retained first-root evidence is tampered;
- retained second-root evidence is tampered;
- retained third-root evidence is tampered;
- the chosen rollover does not belong to the current continuation;
- the explicitly supplied successor is not the chosen rollover successor;
- the cumulative sequence cannot be relinked;
- the next fresh re-entry does not end at the chosen terminal state;
- either output destination already exists;
- the two output destinations are the same;
- required input types are wrong.

Failure grants no discovery fallback or authority substitution.

## Non-goals

40D does not add:

- recursive continuation-overlay nesting;
- a generic `epoch[n]` representation;
- arbitrary-depth changed-evidence-basis lineage;
- CLI third-epoch launch;
- Textual third-epoch launch;
- three-root authority-inspection UI/report;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support/citation authority.

## Acceptance statement

If the executed full test suite succeeds, 40D permits only this statement:

> One persisted third evidence-basis epoch can retain a direct durable 40B ancestry anchor while an ordinary post-third-root continuation is extended cumulatively across repeated checkpoints, with first-, second-, and third-root ancestry freshly preserved. This proves repeatable cumulative continuation above one concrete three-root epoch, not arbitrary-depth evidence-basis lineage.
