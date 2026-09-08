# Milestone 50T — prove unchanged 40C continuation above third-basis overlay-v2 ancestry

Decision: **D274**  
Issue: **#278**

## Concrete researcher action

50S proves that a real third-basis overlay-v2 can survive an actual persisted restart
through the established public 40B → public 40A → 41A launch stack.

The next ordinary researcher action is:

> Make one governed continuation from that restarted third-basis session, checkpoint
> it, and prove the existing 40C restart configuration remains sufficient without
> copying or re-versioning the third-basis bare-selection vocabulary.

## Reuse review

Existing public 40C is already locator-only.

Its durable document contains exactly:

```text
format
prior_third_basis_epoch_overlay_source
declared_edge_sources
declaration_source
```

It owns no third-basis member vocabulary.

Fresh 40C re-entry explicitly opens the referenced 40B overlay through the public
version-aware loader, freshly reconstructs the complete third-basis epoch through
unchanged public 40A, then reconciles the explicit continuation edge/declaration above
that freshly proven endpoint.

Therefore the strongest hypothesis was:

```text
40B overlay-v2 ancestry
does not imply
40C overlay-v2
```

This is the third-epoch analogue of the already-proven 50O result above second-basis
overlay-v2 ancestry.

## Decision

50T is **proof-only**.

No production-code changes.

No 40C durable-format change.

The existing:

`pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1`

remains sufficient above a third-basis 40B overlay-v2 anchor.

## Full retained ancestry

The focused proof starts from the complete nested bare-selection history:

```text
first-root bare saved passage
→ first-root overlay-v2
→ first-root ordinary continuation
→ first-root cumulative continuation
→ second-basis bare saved passage
→ second-basis 37B overlay-v2
→ second-epoch ordinary 37C-v1 continuation
→ second-epoch cumulative 37D / 37C-v1
→ third bare saved passage
→ 44A
→ 47A transition
→ 47B third root
→ 47C first edge
→ 47D adoption
→ 47E / public 40A fresh proof
→ 47F / public 40B overlay-v2
→ persisted restart through 50S / 41A
```

From that freshly restarted state, the proof makes one ordinary governed endpoint
revision and explicit rollover.

## 40C remains locator-only v1

That exact rollover is checkpointed through unchanged public 40C.

The resulting document remains exactly:

```json
{
  "format": "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1",
  "prior_third_basis_epoch_overlay_source": "...",
  "declared_edge_sources": ["..."],
  "declaration_source": "..."
}
```

The proof rejects accidental duplication of:

- `appended_working_set_members`;
- `exact_range_selection`;
- `capture_source`;
- `selection_source`;
- changed working-set/note paths;
- transition paths; or
- root paths.

The bare-selection member vocabulary remains owned only by the directly referenced
40B overlay-v2.

## Mandatory fresh proof remains intact

Public 40C checkpoint persistence first decodes and freshly reconstructs the explicit
prior 40B overlay.

It then mechanically compares:

- retained second-epoch continuation presentation;
- retained second-epoch continuation endpoint;
- first-root identity;
- second-root identity;
- third-root identity;
- third-basis presentation;
- third-basis endpoint; and
- exact chosen rollover relationship.

Only after those checks succeed does 40C write the locator overlay.

No version-specific exception is introduced.

## All three bare passages survive continuation reconstruction

Strict round-trip decode of the written 40C-v1 document reconstructs its explicit
40B-v2 anchor through the public loader.

The retained first-root bare saved passage survives as a real no-note loaded exact
selection.

The retained second-basis bare saved passage survives as a distinct real no-note
loaded exact selection.

The third-basis bare saved passage also survives as a real no-note loaded exact
selection.

That third bare object remains the same loaded object retained in:

- the freshly reconstructed third-root successor working set; and
- the freshly reconstructed post-third-root continuation endpoint working set.

No note is manufactured at any layer.

## Root and endpoint continuity

The proof mechanically retains exact:

- first-root identity;
- second-root identity;
- third-root identity; and
- continuation terminal edge identity.

These digests remain record/content identity anchors only. They do not establish
authorship, trusted time, chronology, semantic support, or citation authority.

## Existing first-checkpoint Textual product inherits the proof

50T drives the real inspectable third-basis first-checkpoint product from a persisted
40B-v2 launch.

Before rollover, no 40C form exists.

After explicit rollover, the existing 40C checkpoint form mounts with all durable
locator inputs blank.

The researcher explicitly supplies:

- prior 40B overlay-v2 path;
- successor edge path;
- continuation declaration path; and
- no-overwrite 40C destination.

Successful checkpointing:

- leaves the exact persisted 40B launch lineage mounted;
- preserves the immutable launch-provenance object and original 40B-v2 path;
- leaves the visible one-hop controller mounted; and
- retains the fresh checkpoint result separately as proof.

No v2-specific product control is added.

## Persisted continuation relaunch inheritance

No new CLI branch is required.

The exact persisted continuation is supplied to:

```text
pyxis research-shell --third-basis-epoch-continuation-overlay <40C-v1>
```

The existing CLI:

1. loads the strict 40C overlay-v1;
2. reconstructs its referenced 40B-v2 through the public version-aware loader;
3. freshly reconstructs the complete three-basis epoch;
4. reconciles the explicit continuation declaration;
5. proves persisted third-basis continuation lineage; and
6. dispatches the established dedicated third-basis continuation product.

The focused proof rejects fallback to Workspace, ordinary research-session,
root-backed, root-backed-continuation, controller-only, second-basis,
second-basis-continuation, or initial third-basis products.

## Read-only inspection inheritance

The same 40C-v1 path is supplied twice to:

```text
pyxis research-inspect --third-basis-epoch-continuation-overlay <40C-v1>
```

Both runs emit byte-identical deterministic JSON equal to the established shared
third-basis continuation authority-inspection projection.

The report remains:

`pyxis.chromium.research_third_basis_epoch_authority_inspection.v1`

with role:

`read_only_inspection_not_authority`

and launch family:

`persisted 40C/40D continuation launch`

The 40C path is launch-location context only.

The current governed-state projection reports exactly one declared continuation edge.

## Fail-closed ancestry reconstruction

After a valid 40C checkpoint is written, the proof tampers with the explicitly
referenced 40B overlay-v2.

The 40C document itself still strictly decodes as locator-only configuration.

Fresh 40C re-entry then fails when it attempts to decode and reconstruct the explicit
prior 40B ancestry.

Thus:

```text
valid locator configuration
!=
freshly reconstructed research authority
```

remains mechanically enforced.

## Repository Zero proof

Test-only head:

`5bf6474c31f6f17ab00f0cb53910e9f140c45273`

passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

with no production-code correction.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50T changes only:

- one focused third-basis continuation proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- public 40A;
- public 40B v1/v2;
- 41A lineage;
- 40C persistence/loading;
- CLI implementation;
- third-basis product classes;
- authority inspection;
- 40D cumulative extension;
- first-/second-basis formats;
- browser behavior; or
- semantic interpretation.

## Explicit stop boundary

50T proves only the first ordinary persisted continuation above v2-backed third-basis
ancestry.

Do not infer:

- 40D cumulative continuation above that ancestry;
- 47G in-process handoff compatibility with a v2 47F result;
- fourth-basis bare persistence;
- fourth-basis relaunch;
- arbitrary Nth-basis version propagation;
- automatic path discovery;
- latest/current/head authority;
- browser mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

The next researcher-action review should test unchanged 40D cumulative reuse above the
same fixed 40B-v2 anchor before considering a fourth changed-basis crossing.

## Compact result

After 50T:

```text
three-bare third-basis 40B overlay-v2
→ persisted restart
→ ordinary governed endpoint revision
→ explicit rollover
→ unchanged public 40C overlay-v1
→ fresh continuation reconstruction through the same 40B-v2 anchor
→ established third-basis continuation product
→ unchanged deterministic inspection-v1
```

Version expansion remains local to the durable boundary that actually owns the
expanded locator vocabulary.
