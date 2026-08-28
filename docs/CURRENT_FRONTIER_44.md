# Pyxis Current Frontier — Milestones 44A through 44H

> **Continuity status — implementation through Milestone 44H / D225.**  
> **Updated:** 2026-08-28  
> This file is an additive continuation of `docs/CURRENT_FRONTIER_41_43.md`. It does not replace milestone records, implementation, tests, executed CI, or earlier compact frontier documents.

## Read this after `docs/CURRENT_FRONTIER_41_43.md`

Milestones 41–43 closed the concrete third-epoch product loop, added read-only authority inspection, and extracted only cumulative mechanics independently proven across one-, two-, and three-root continuation families.

The post-43E boundary deliberately rejected a fourth evidence-basis epoch or generic `epoch[n]` abstraction. The stronger product question was:

> How can a researcher explicitly initiate one changed evidence basis from inside the existing governed product using already-proven concrete authority boundaries?

Milestones 44A–44H now answer that question end to end for the first changed-basis path above one ordinary 31A-launched governed session.

## Completed first changed-basis product flow

```text
ordinary governed 31A-backed session
→ 44A prepare changed evidence basis
→ 44B persist explicit 33B cross-working-set transition
→ 44C persist first 34A revision root
→ 44D persist first 34B post-root ordinary edge
→ 44E explicitly adopt the 35A root-backed governed session
→ 44F freshly prove 35B reconstructability
→ 44G persist the verified historical session as a 35C restart overlay
→ 44H explicitly hand the exact fresh 35C proof into the established root-backed product
```

Every arrow is a separate authority step. Preparation, transition, root creation, governed-session adoption, fresh reconstruction, durable restart configuration, and product handoff are not collapsed into one opaque action.

---

## 44A / D218 — Explicit changed-evidence-basis preparation

44A exposes the established 33A preparation boundary from an already-governed research shell.

The caller supplies exact already-loaded/relinked application evidence as candidate appended members. The researcher supplies a genuinely new rationale plus explicit no-overwrite destinations for the changed working set and changed working-set note.

Successful 44A proves only:

```text
current declared working set
+ explicit candidate evidence
+ explicit human rationale
→ durable prepared changed basis
```

It does not adopt the basis or alter the mounted governed controller.

An unadopted endpoint-revision write does not stale the candidate. An explicit rollover that replaces the governed controller before persistence does stale the old form rather than silently retargeting it.

---

## 44B / D219 — Explicit first changed-basis transition

44B exposes the established 33B cross-working-set transition only where an exact ordinary `ChromiumResearchSessionReentryResult` proves the shell belongs to the pre-root ordinary launch family.

The transition consumes one exact successful 44A preparation plus explicit current durable sources for the declared endpoint and prepared changed-basis artifacts and one explicit no-overwrite transition destination.

All locator inputs begin blank.

Successful 44B persistence leaves the mounted governed session unchanged. The transition is durable historical evidence of an explicit crossing, not adoption of that branch.

---

## 44C / D220 — Explicit first changed-basis revision root

44C exposes the established 34A first revision-root boundary from one exact successful 44B transition.

The researcher supplies genuinely new rationale and five explicit durable locations: prior endpoint edge, changed working set, changed working-set note, 33B transition, and no-overwrite 34A root destination.

Historical receipt paths may be shown for context but are not copied into current locator fields.

The transition is freshly relinked before root persistence and the new root is freshly reopened through the public 34A boundary before success.

A successful root remains historical lineage and does not replace the mounted controller.

---

## 44D / D221 — Explicit first post-root ordinary edge

44D exposes the established 34B one-time bridge from the first 34A root back into ordinary 24B edge lineage.

Inputs are deliberately narrow:

- genuinely new human rationale;
- explicit current 34A root source;
- explicit no-overwrite first-edge destination.

The persisted record remains the established 24B edge format and is freshly reopened through the root-specific 34B loader.

44D does not declare a sequence, adopt a root-backed controller, or alter whichever old-basis controller is mounted.

---

## 44E / D222 — Explicit changed-basis governed-session adoption

44E is the first 44-series action that intentionally changes the shell's governed branch.

From one exact successful 44D result, the researcher supplies an explicit current first-edge source and an explicit no-overwrite existing-format 26B declaration destination.

The exact loaded 34A root retained by 44D is already the explicit starting record, so no root path is invented.

The established 35A machinery performs:

```text
exact loaded 34A root
+ explicit first-edge source
→ fresh root-started sequence
→ existing 26B declaration
→ fresh declaration relink
→ existing ChromiumResearchSessionController
→ explicit shell-local branch adoption
```

After successful adoption, the root-backed controller becomes the shell's governed controller. This is shell-local user-authorized adoption, not a global latest/current/head claim.

44E deliberately creates no fresh-process restart authority.

---

## 44F / D223 — Explicit root-backed fresh-process verification

44F exposes the established 35B reconstruction boundary as a separate action after exact 44E adoption.

The retained initial ordinary 31A plan remains typed application state. Every current durable locator required for the changed-basis region begins blank and must be explicitly supplied again.

44F builds the exact 35B typed plan, freshly reconstructs the historical 44E root-backed session, and proves the expected root, declaration, endpoint, rationale, and governed presentation.

Successful verification does not replace the currently mounted controller and writes no restart configuration.

If the mounted 44E session has already rolled farther, 44F still verifies the exact historical 44E target rather than silently retargeting to the newer mounted continuation.

---

## 44G / D224 — Persist verified root-backed restart overlay

44G consumes one exact successful 44F verification and exposes the established public 35C proof-gated persistence boundary.

Two explicit durable inputs begin blank:

1. current durable source for the matching ordinary 31B plan document;
2. no-overwrite destination for `pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1`.

Public 35C remains authoritative for:

```text
ordinary 31B decode
→ exact prior-plan equality
→ mandatory fresh 35B reconstruction
→ presentation/root/endpoint coherence
→ no-overwrite overlay write
→ strict round-trip overlay decode
```

44G adds only product-level coherence checks and a dedicated persistence surface.

### Historical-target rule

44G persists the exact historical session selected by 44F, even if the 44-series shell currently mounts a later continuation. Persistence leaves that later mounted state untouched.

```text
successful 44G persistence
!=
mounted-session replacement
```

PR #167 merged the final 44G head `eb5599d71a571de4a2d2153059b4f8e8bf69e6e7`. Repository Zero run `33191039137` passed Python 3.11, 3.12, 3.13, and 3.14.

---

## 44H / D225 — Explicit in-process handoff into the proven root-backed product

44H closes the remaining product seam after 44G.

Successful 44G persistence contains two distinct fresh-process objects:

```text
44F verification_result.fresh_reentry
→ retained as 35C checkpoint.reentry

35C mandatory fresh reconstruction
→ checkpoint.fresh_reentry
```

The exact 44H handoff subject is the latter:

```text
last_first_changed_basis_root_backed_reentry_overlay
    .checkpoint
    .fresh_reentry
```

It is **not**:

- the 35C overlay path;
- the earlier 44F fresh object merely because it represents equivalent durable state;
- whatever controller happens to be mounted;
- a newly reloaded object reconstructed from path text.

### Explicit user choice

Successful persistence alone does not change mode.

Only after one exact successful 44G persistence does the dedicated 44H shell reveal one explicit action:

```text
Continue with verified changed-basis session
```

Pressing that action exits the shell with the exact retained `checkpoint.fresh_reentry` object. Normal close returns no handoff.

### Bounded product runner

44H also closes the product loop rather than stopping at a typed return value:

```text
run 44H shell
→ None on normal close: stop
→ exact ChromiumResearchRootBackedSessionReentryResult on explicit handoff
→ validate typed result
→ pass same object directly to existing RootBackedResearchSessionShell
→ run existing receiver
```

No overlay path is supplied to the runner. No persistence, decode, path proof, discovery, or restart reconstruction occurs during the in-process transition.

Deleting the just-written overlay after successful 44G persistence does not prevent the typed handoff because the transferred authority is the already-earned 35C fresh proof object.

### Historical-target rule remains intact

If the 44-series shell mounts a later continuation, 44G still proves/persists the historical target and 44H still returns that exact historical 35C fresh result only when the researcher explicitly chooses it.

The button press is the branch-changing authority. No latest/current/preferred branch is inferred.

PR #170 merged exact tested head `22797074c211eb4e6a718b2d7960c946be92e50d` as merge commit `d34b4e0baf3e0b822927a8adec7b7de0e7f68677`. Repository Zero run `33207716371` passed the complete suite on Python 3.11, 3.12, 3.13, and 3.14.

---

## Reuse lessons reinforced by 44A–44H

### Productization does not duplicate lower-level authority

The 44-series repeatedly exposes already-proven 33A–35C application boundaries through narrow product wrappers and dedicated UI surfaces. Product code may enforce retained-object and mounted-state coherence but does not become a second persistence/relinking implementation.

### Prior path use is not continuing path authority

Every durable locator relevant to a new operation begins blank unless exact typed application state already carries the necessary authority.

```text
previously used path
!=
currently authorized locator
```

44H makes the inverse equally explicit:

```text
exact typed in-process proof
!=
persistent path authority
```

### Historical durable lineage may coexist with later mounted work

44B transition, 44C root, 44D first edge, 44F verification target, 44G overlay, and the 44H handoff target may remain truthful historical relationships even while another controller is currently mounted.

Coexistence does not establish chronology, preference, or head authority.

### Explicit adoption and handoff remain user-owned boundaries

44E explicitly adopts the new root-backed governed controller.

44H separately and explicitly chooses whether to leave the current 44-series shell for the freshly proven 35C root-backed product.

Neither action is authorized merely because the necessary durable artifacts exist.

---

## Authority boundaries still intentionally absent

Through 44H, Pyxis still does **not** claim or infer:

- a globally current/latest/canonical research session;
- complete revision history or unique successor relationships;
- chronology from paths, filenames, hashes, or filesystem timestamps;
- branch preference merely because one durable lineage was persisted later;
- durable identity from path equality;
- persistent path authority from a prior operation or typed in-process handoff;
- source authenticity, authorship, or trusted time from SHA-256 integrity;
- semantic improvement from changed rationale text;
- evidentiary support merely because human notes are attached to evidence;
- quotation/citation authority from exact source selection alone;
- browser navigation or autonomous interaction authority from read-only observation;
- a generic fourth evidence-basis epoch or recursive `epoch[n]` ancestry model;
- automatic restart/adoption from valid persistence;
- one-root launch-provenance/current-state inspection parity merely because second/third epoch inspection exists.

These remain deliberate product constraints.

## Current implemented frontier after 44H

The 44-series is complete through **44H / D225**.

Its strongest compact statement is:

> From one ordinary 31A-backed governed research session and exact already-loaded candidate evidence, Pyxis can explicitly prepare a changed evidence basis, persist the crossing and first root-backed lineage, explicitly adopt that governed branch, freshly verify and persist restartability, and—only on a separate explicit user action—transfer the exact fresh 35C proof into the established root-backed product without reloading or promoting the overlay path.

That statement does **not** imply arbitrary-depth evidence-basis productization.

## Next decision frontier — 45A / D226

Issue #171 tracks the next separate product question:

> Can already-earned one-root authority become visibly inspectable across persisted 35C/35D/35E launches and in-process 44H/36D handoffs, while keeping immutable launch provenance separate from mutable current governed state and without inventing persistent paths for in-process launches?

This boundary is chosen before productizing a second changed evidence basis because the root-backed product now has four legitimate launch families while lacking the launch-provenance/current-state observability already proven for second and third epochs.

45A is explicitly **not** implemented merely because this continuity document records the approved decision frontier.

It is also not a generic authority-inspection abstraction and does not authorize another evidence-basis epoch.

## Continuity rule

For future development sessions:

```text
implementation + executed tests + milestone record
> compact frontier continuity summary
> README/current-status wording
```

Read the compact chain in order:

1. `docs/CURRENT_FRONTIER.md`
2. `docs/CURRENT_FRONTIER_35_36.md`
3. `docs/CURRENT_FRONTIER_37_38.md`
4. `docs/CURRENT_FRONTIER_39_40.md`
5. `docs/CURRENT_FRONTIER_41_43.md`
6. this file, `docs/CURRENT_FRONTIER_44.md`

If a compact summary conflicts with implementation, tests, executed CI, or a milestone-specific record, inspect the stronger evidence before changing behavior.
