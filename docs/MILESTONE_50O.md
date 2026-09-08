# Milestone 50O — prove 37C continuation above second-basis bare overlay-v2 ancestry

Decision: **D269**  
Issue: **#268**

## Concrete researcher action

50N proves that a persisted second-basis bare-selection 37B overlay-v2 can relaunch
through the established second-basis product.

The next ordinary researcher action is:

> Make one governed continuation from that relaunched state, checkpoint it, and
> relaunch that continuation later without copying or losing either bare saved
> passage in ancestry.

## Reuse review

Existing public 37C continuation checkpointing and re-entry already compose through
one explicit prior 37B path.

The checkpoint path is:

```text
earned second-basis re-entry
+ explicit prior 37B overlay path
+ explicit successor edge
+ explicit continuation declaration
→ public 37B loader
→ fresh public 37A reconstruction
→ verify retained prior continuation/root ancestry
→ verify second-root and second-epoch presentation/endpoint
→ verify exact rollover relationship
→ persist locator-only 37C overlay-v1
```

Fresh 37C re-entry is:

```text
37C overlay-v1
→ prior_second_basis_epoch_overlay_source
→ public 37B version dispatch
→ public 37A reconstruction
→ explicit continuation edge/declaration relink
→ governed continuation controller
```

The 37C document does not encode the member vocabulary of its prior second changed
basis.

It stores only:

- the explicit prior 37B overlay location;
- the explicitly ordered continuation edge locations; and
- the explicit continuation declaration location.

Therefore the strongest hypothesis was:

```text
37B overlay-v2 ancestry
does not imply
37C overlay-v2
```

This is the second-epoch analogue of the 50J result above first-root overlay-v2
ancestry.

## Decision

50O is **proof-only**.

No production-code changes.

No 37C durable-format change.

The existing:

`pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1`

remains sufficient above second-basis 37B overlay-v2 ancestry.

## Executable crossing

The focused proof creates the complete real bare-selection ancestry rather than a
simplified fixture:

```text
first-root bare saved passage
→ first-root overlay-v2
→ ordinary first-root continuation
→ cumulative first-root continuation
→ second bare saved passage
→ second changed basis
→ second root
→ explicit adoption
→ 46E / 37A fresh proof
→ 46F / 37B overlay-v2
```

The persisted 37B overlay is freshly decoded and reconstructed, then bound to one
persisted-path second-epoch lineage.

From that fresh governed controller, the proof performs one ordinary endpoint
revision and explicit rollover.

That exact rollover is supplied to public 37C checkpoint persistence.

## 37C remains locator-only v1

The new continuation document remains exactly:

```json
{
  "format": "pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1",
  "prior_second_basis_epoch_overlay_source": "...",
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

The bare-selection member vocabulary remains owned by the referenced 37B overlay-v2.

## Both bare saved passages survive continuation reconstruction

Fresh 37C reconstruction first resolves its explicit 37B ancestry through the public
version-aware loader.

The retained first-root ancestry still contains one real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

with selected text:

`"Bare"`

and no manufactured note.

The second changed-basis layer contains a distinct real loaded bare selection with
the same exact selected text and no manufactured note.

The second bare member remains the exact loaded member used by:

- the freshly reconstructed second-root successor working set;
- the freshly reconstructed second-basis endpoint working set; and
- the ordinary 37C continuation endpoint working set.

Thus ordinary continuation above the second epoch neither erases nor reinterprets the
saved passage.

## Durable ancestry remains explicit

The 37C overlay points directly to the exact persisted 37B overlay-v2.

It does not point to the current 37C overlay recursively, flatten the second epoch, or
inline the 37B member locators.

Fresh reconstruction therefore remains compositional:

```text
37C continuation locator
→ exact 37B overlay path
→ exact 37B v1/v2 format dispatch
→ exact two-basis research locators
→ explicit continuation reconciliation
```

## Root and endpoint continuity

The proof mechanically retains:

- the exact first-root identity inside nested ancestry;
- the exact second-root record SHA-256;
- the exact second-basis terminal edge identity; and
- the exact chosen continuation terminal edge identity.

Those digests remain record/content identity anchors only. They do not establish
authorship, trusted time, chronology, semantic support, or citation authority.

## Existing first-checkpoint product inherits the proof

50O drives the real inspectable second-basis first-checkpoint product from a persisted
37B overlay-v2 launch.

The ordinary endpoint revision and rollover expose the historical 37C form.

The researcher supplies all four durable locations explicitly:

- current 37B overlay-v2 path;
- successor edge path;
- continuation declaration path; and
- no-overwrite 37C destination.

The unchanged product succeeds through public 37C.

Successful persistence:

- retains the exact persisted 37B launch lineage;
- does not replace immutable launch provenance;
- leaves the visible one-hop controller mounted; and
- returns a separately fresh 37C reconstruction as proof.

No overlay-v2-specific product control is added.

## Persisted continuation relaunch inheritance

No new CLI branch is required.

The exact persisted continuation is supplied to:

```text
pyxis research-shell --second-basis-epoch-continuation-overlay <37C-v1>
```

The existing CLI:

1. loads the strict 37C overlay-v1;
2. reconstructs its referenced 37B overlay-v2 through the public loader;
3. relinks the explicit continuation;
4. proves persisted second-epoch continuation lineage; and
5. dispatches the established dedicated second-basis continuation product.

The focused proof rejects fallback to controller-only, initial second-epoch, or
root-backed continuation products.

## Read-only inspection inheritance

The same 37C path is supplied twice to:

```text
pyxis research-inspect --second-basis-epoch-continuation-overlay <37C-v1>
```

Both runs emit byte-identical deterministic JSON.

The output exactly equals the established shared second-basis continuation inspection
projection.

It remains:

`pyxis.chromium.research_second_basis_epoch_authority_inspection.v1`

with role:

`read_only_inspection_not_authority`

and launch family:

`persisted 37C/37D continuation launch`

The 37C path is launch-location context only.

No new inspection format or version branch is introduced.

## Fail-closed ancestry reconstruction

After a valid 37C checkpoint is written, the proof tampers with the explicitly
referenced 37B overlay-v2.

The 37C document itself still strictly decodes as locator-only configuration.

Fresh 37C re-entry then fails when it attempts to decode and re-prove the referenced
37B ancestry.

This preserves:

```text
configuration shape
!=
reconstructed research authority
```

and proves that the continuation does not silently cache, flatten, or bypass the
second-basis anchor.

## Repository Zero proof

Test-only head:

`aacb355cbf62fb158a12c04aeef65196bfcbdcdf`

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

50O changes only:

- one focused second-basis continuation proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- 37B persistence/loading;
- public 37A reconstruction;
- 37C persistence/loading;
- continuation formats;
- CLI implementation;
- second-basis product shells;
- authority inspection;
- evidence formats;
- third-basis products; or
- browser behavior.

## Explicit stop boundary

50O proves only the **first ordinary persisted continuation** above v2-backed
second-basis ancestry.

Do not infer:

- 37D cumulative continuation above that ancestry;
- third-basis bare persistence;
- third-basis bare relaunch;
- generic nested version propagation;
- automatic path discovery;
- current/latest/head authority;
- browser highlighting or mutation;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

Any cumulative 37D reuse above this v2-backed second-basis anchor requires its own
concrete researcher-action review.

## Compact result

After 50O, the nested bare-passage lineage is proven through one durable ordinary
continuation above the second changed basis:

```text
first-root bare cumulative ancestry
→ second-basis bare overlay-v2
→ fresh persisted second-epoch launch
→ ordinary governed endpoint revision
→ explicit rollover
→ unchanged 37C continuation overlay-v1
→ process restart
→ public 37B v2 ancestry reconstruction
→ explicit continuation reconciliation
→ established second-basis continuation product
```

The v2 distinction remains exactly at the durable boundary that owns the expanded
bare-selection member vocabulary.
