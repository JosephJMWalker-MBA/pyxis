# Milestone 50J — prove 35D continuation above bare-selection overlay-v2 ancestry

Decision: **D264**  
Issue: **#258**

## Concrete researcher action

50I proves that a persisted first-root bare-selection 35C overlay-v2 can relaunch
into the established root-backed product.

The next ordinary researcher action is:

> Make one governed continuation from that relaunched state, checkpoint it, and
> relaunch that continuation later without losing the bare saved passage in ancestry.

## Reuse review

Existing 35D continuation checkpointing and re-entry already compose through the
public first-root 35C loader.

The checkpoint path is:

```text
earned root-backed re-entry
+ explicit prior 35C overlay path
+ explicit successor edge
+ explicit continuation declaration
→ load prior 35C overlay
→ require exact typed-plan equality
→ fresh 35B reconstruction
→ verify exact rollover relationship
→ persist locator-only 35D overlay-v1
```

Fresh 35D re-entry is:

```text
35D overlay-v1
→ prior_root_backed_overlay_source
→ public 35C loader
→ public 35B reconstruction
→ explicit continuation edge/declaration relink
→ governed continuation controller
```

The 35D document does not encode the member vocabulary of its prior changed-basis
session. It stores only locators for the prior root-backed overlay and the
continuation segment.

Therefore the strongest hypothesis was:

```text
35C overlay-v2 ancestry
does not imply
35D overlay-v2
```

## Decision

50J is **proof-only**.

No production code changes.

No 35D durable-format change.

The existing:

`pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1`

remains sufficient above first-root 35C overlay-v2 ancestry.

## Executable crossing

The focused proof creates a real first-root bare-selection overlay-v2 through the
public 50H path, then freshly reconstructs that root-backed session from the
persisted path.

From the fresh governed controller it performs one ordinary endpoint revision and
the existing explicit 30A rollover.

That exact rollover is then supplied to public 35D checkpoint persistence.

## 35D remains locator-only

The persisted continuation document remains exactly:

```json
{
  "format": "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1",
  "prior_root_backed_overlay_source": "...",
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
- root paths; or
- prior-session plan paths.

The member vocabulary remains owned by the referenced 35C overlay.

## Bare saved passage survives continuation reconstruction

Fresh 35D re-entry first reconstructs the referenced first-root session through the
public 35C loader.

The focused proof establishes that this fresh prior ancestry still contains one real:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

with exact selected text:

`"Bare"`

and no manufactured note object.

That freshly loaded bare member remains present in:

- the fresh root-backed prior working set; and
- the fresh continuation endpoint working set.

Thus ordinary continuation does not erase or reinterpret the saved passage.

## Durable ancestry remains explicit

The 35D overlay points to the exact persisted first-root overlay-v2 path.

It does not inline, migrate, or copy that prior configuration.

Fresh reconstruction therefore remains compositional:

```text
35D continuation locator
→ exact 35C overlay path
→ exact 35C format dispatch
→ exact changed-basis evidence locators
```

## Product relaunch inheritance

No new CLI branch is required.

The existing command:

```text
pyxis research-shell --root-backed-continuation-overlay <35D>
```

loads the historical 35D overlay-v1, reconstructs its v2-backed prior ancestry
through the public 35C loader, proves the existing typed continuation lineage, and
dispatches the established root-backed continuation product.

The focused proof fails if launch falls back to:

- a controller-only product; or
- the non-continuation root-backed shell.

Neither fallback is required.

## Read-only inspection inheritance

The same persisted 35D path is also supplied twice to:

```text
pyxis research-inspect --root-backed-continuation-overlay <35D>
```

Both runs emit byte-identical deterministic JSON.

The result exactly equals the shared continuation authority-inspection projection
and remains:

`read_only_inspection_not_authority`

with launch family:

`persisted 35D/35E root-backed continuation launch`

No new inspection format is introduced.

## Fail-closed ancestry proof

The test tampers with the referenced first-root overlay-v2 after a valid 35D
checkpoint has been written.

The 35D document itself still decodes as locator-only configuration.

Fresh 35D re-entry then fails when it attempts to reconstruct the explicit prior
35C ancestry.

This preserves the established distinction:

```text
configuration shape
!=
reconstructed research authority
```

## Repository Zero proof

The test-only head passed the complete Repository Zero suite on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

without any production-code correction.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

50J changes only:

- one focused continuation proof module;
- this milestone record; and
- compact README continuity.

It does not change:

- 35C persistence/loading;
- 35D persistence/loading;
- continuation formats;
- CLI implementation;
- root-backed product shells;
- authority inspection;
- second-/third-epoch products;
- evidence formats; or
- browser behavior.

## Explicit stop boundary

50J proves only the **first ordinary continuation** above first-root bare-selection
overlay-v2 ancestry.

Do not infer:

- second changed-basis epoch serialization;
- third changed-basis epoch serialization;
- 31B plan-v2;
- automatic locator discovery;
- current/latest/head authority;
- browser highlighting or mutation;
- automatic adoption;
- search or indexing;
- tags;
- export;
- citation authority; or
- semantic interpretation.

Any later changed-basis persistence crossing requires its own researcher-action
review.

## Compact result

After 50J, the first-root bare-passage path is proven through one durable ordinary
continuation and another process boundary:

```text
bare saved passage
→ first-root changed-basis overlay-v2
→ fresh root-backed relaunch
→ ordinary governed endpoint revision
→ 30A rollover
→ unchanged 35D continuation overlay-v1
→ process restart
→ fresh v2-backed prior reconstruction
→ explicit continuation reconciliation
→ established root-backed continuation product
```

The v2 distinction stays exactly where the changed member vocabulary lives.
