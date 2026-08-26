# Current Frontier — Milestones 37–38

This document is an additive continuation of `CURRENT_FRONTIER_35_36.md`.

It records the verified frontier through Milestone 38F / Decision D199. It is historical orientation, not a current/head pointer, chronology authority, or substitute for Git history and executed CI evidence.

## Starting point

Milestones 35–36 established:

- persisted root-backed session re-entry;
- persisted ordinary continuation above first-root ancestry;
- repeatable cumulative continuation without recursive overlay ancestry;
- standalone CLI/Textual product paths;
- first checkpoint and repeatable checkpointing;
- explicit in-process handoff from first-checkpoint to cumulative mode.

The 37–38 sequence asks whether one **second changed evidence-basis epoch** can be added while preserving the first root as distinct ancestry and while keeping launch, restart, checkpoint, and path authority explicit.

---

## 37A / D190 — second evidence-basis epoch re-entry

Merged via PR #92 at:

`ff80a34b7dd69fc1063cdbf282ed737c0db5b13c`

Introduced one explicit second basis-change epoch above a proven prior root-backed continuation.

The new second root is distinct from the retained first root. The second basis-change plan remains operational configuration only; it is not a recursive history schema.

Core public boundary:

- `create_chromium_research_second_basis_epoch_reentry_plan(...)`
- `reenter_chromium_research_second_basis_epoch(plan)`

Key rule:

```text
second changed-basis root
!= replacement for first root
```

---

## 37B / D191 — persisted second-epoch locator overlay

Merged via PR #94 at:

`877a23f4f6de09b3432937bb72b69d0e927b7e40`

Added the strict locator-only format:

`pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1`

Persistence freshly re-earns the prior first-epoch continuation and both root identities before writing the overlay.

Path-distinct equivalent prior continuation configurations remain acceptable when fresh durable equivalence proves the same ancestry/session.

Loading the overlay remains configuration decoding only.

---

## 37C / D192 — first restartable continuation above second root

Merged via PR #96 at:

`ada3ad744944a19fa571d09214d172162271b070`

Added the first ordinary continuation locator above a persisted second basis epoch:

`pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1`

Fresh reconstruction re-enters the explicit 37B overlay, re-earns both roots, and then relinks the explicit ordinary continuation declaration.

---

## 37D / D193 — cumulative continuation above second root

Merged via PR #98 at:

`519f8d4d487b4e8be93b534dfd6d0994ffad0ea9`

Added repeatable cumulative checkpoint extension while retaining a direct 37B anchor and a cumulative ordered edge declaration.

Good shape:

```text
37B second-epoch overlay
        ↓
       E1 → E2 → E3 → ... → En
```

Rejected shape:

```text
37C overlay → 37D overlay → 37D overlay → ...
```

The continuation overlay family is reused; no recursive overlay format is introduced.

Path-distinct current overlay locations may be accepted only after fresh durable equivalence.

---

## 38A / D194 — public CLI entry families

Merged via PR #100 at:

`bb378d98f970918075ff5cff8dfa0989cf46410b`

Extended `pyxis research-shell` with explicit mutually exclusive entry families:

- `--second-basis-epoch-overlay`
- `--second-basis-epoch-continuation-overlay`

No generic overlay argument, discovery, format guessing, latest/current/head, or ambient directory selection was added.

---

## 38B / D195 — proven second-epoch shell launch lineage

Merged via PR #102 at:

`eb68f2eb5c525216d590e70579a54145fe7584c4`

Exact tested head:

`0447745742e48d8d630088bf2ac62acffc562c62`

Workflow run:

`32904045402`

Python 3.11–3.14 completed successfully.

Added typed wrappers binding one explicit persisted location to a fresh result reconstructed from that location:

- `ChromiumResearchSecondBasisEpochShellLineage`
- `ChromiumResearchSecondBasisEpochContinuationShellLineage`

The retained result is the **freshly reconstructed result from the explicit source**, not the caller object.

A path remains location context, not identity.

---

## 38C / D196 — dedicated second-epoch Textual shells

Merged via PR #104 at:

`d28aa2561128b411e88381d9c163c8ceca98ee97`

Exact tested head:

`8c046b7b0c156ee6f936e65b3c4aa8fe6f237c71`

Workflow run:

`32904938063`

Python 3.11–3.14 completed successfully.

Introduced dedicated shells retaining the exact 38B launch lineage rather than dropping to a controller-only shell.

Ordinary restart-lineage controls remain absent because second-epoch launch lineage is a different authority family.

---

## 38D / D197 — first Textual 37C checkpoint

Merged via PR #106 at:

`aec95c8d89aed2703278b85290df200d8657e6c0`

Exact tested head:

`137567d2f070c5a3dee0c6939ae5535243ae9263`

Workflow run:

`32905729647`

Python 3.11–3.14 completed successfully.

The 37B-backed shell can now perform one explicit 30A rollover and proof-gate a persisted 37C continuation checkpoint.

Checkpoint success keeps further revision locked. It does not automatically change shell modes.

All checkpoint path fields begin blank; the launch overlay path is not silently reused.

---

## 38E / D198 — repeatable cumulative Textual checkpointing

Merged via PR #108. Authoritative `main` merge commit:

`313fd3ce9f4d75e79034e78e6e38ecdf6e47a8fe`

Exact tested branch head:

`440216d6b1ee8d3bded0777d5d851dbca2657adb`

Workflow run:

`32906553606`

Python 3.11–3.14 completed successfully.

The continuation shell now keeps two concepts separate:

- immutable persisted launch lineage;
- mutable current typed continuation.

After a successful cumulative 37D checkpoint, the visible shell promotes to the exact fresh cumulative continuation and unlocks revision for the next cycle.

The direct 37B ancestry anchor remains fixed; cumulative edge declarations grow without recursive continuation-overlay ancestry.

---

## 38F / D199 — explicit in-process handoff into cumulative mode

Merged via PR #110 at:

`2cef86f994c307a3a01520634fce972d6c365301`

Exact tested head:

`c22c52fbb518093265effd8aa13ba5e36011a57c`

Workflow run:

`32976034216`

Python 3.11, 3.12, 3.13, and 3.14 all completed successfully.

38F closes the gap between first-checkpoint mode and cumulative mode without turning checkpoint success into an automatic transition.

The explicit route is:

```text
successful 37C checkpoint
→ explicit Continue in cumulative mode action
→ exact checkpoint.fresh_reentry
→ raw typed cumulative shell
```

The handoff performs:

- no continuation-overlay reload;
- no fabricated 38B path wrapper;
- no saved-path promotion;
- no ordinary restart-lineage promotion.

Normal shell close remains a valid alternative. A later persisted relaunch remains available through the explicit path-proofed CLI route.

### 38F CI cancellation diagnosis

The first PR attempt repeatedly appeared to have GitHub Actions checks "cancelled."

The cancellation was deterministic, not random infrastructure behavior.

Each matrix lane entered `python -m pytest`, reached 73%, and then remained silent until GitHub-hosted Actions terminated the job at almost exactly six hours.

The last completed file was:

`tests/test_cli_second_basis_epoch_cumulative_handoff.py`

The next older CLI test contained a stale lazy-import monkeypatch. 38F had moved the UI factory to `pyxis.ui.second_basis_epoch_cumulative_handoff_shell`, but the stale test still intercepted the older module. The miss caused the test to launch a real interactive Textual application inside CI and wait indefinitely for input.

The fix updated the lazy-import boundary test to intercept the actual current module. The exact corrected head then passed the full 3.11–3.14 matrix.

This establishes a durable testing rule:

> CLI lazy-import/dependency tests must fail fast at the exact current UI adapter boundary. They must never be allowed to fall through into an interactive Textual app during automated tests.

---

# Frontier after 38F

The second basis-change epoch is now usable through both persisted and in-process product paths.

Earned statements include:

- one first root can be retained as distinct ancestry;
- one second changed evidence-basis root can be added above it;
- ordinary continuation can proceed above the second root;
- cumulative continuation can grow without recursive overlay ancestry;
- explicit persisted launch locations can be freshly proven;
- dedicated Textual shells retain typed second-epoch lineage;
- first and repeatable continuation checkpoints are product-accessible;
- first-checkpoint mode can explicitly hand the exact fresh continuation into cumulative mode without disk re-entry.

Not earned:

- third basis-change epoch support;
- arbitrary-depth basis-change schemas;
- generic recursive lineage;
- global latest/current/head authority;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time claims;
- semantic-support or citation authority from integrity hashes.

## Next seam

The next seam is not automatically a third epoch.

Before adding deeper ancestry, the product should make already-earned authority visible enough that a researcher can distinguish:

```text
immutable launch provenance
```

from:

```text
current governed continuation state
```

without allowing displayed paths or hashes to become control-plane authority.

That is Milestone 39A / Decision D200.
