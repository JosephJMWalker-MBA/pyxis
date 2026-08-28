# Pyxis Current Frontier — Milestones 44A through 44G

> **Continuity status — implementation through Milestone 44G / D224.**  
> **Updated:** 2026-08-28  
> This file is an additive continuation of `docs/CURRENT_FRONTIER_41_43.md`. It does not replace milestone records, implementation, tests, executed CI, or the earlier compact frontier documents.

## Read this after `docs/CURRENT_FRONTIER_41_43.md`

Milestones 41–43 closed the concrete third-epoch product loop, added read-only authority inspection, and extracted only the cumulative mechanics independently proven across one-, two-, and three-root continuation families.

The post-43E decision boundary deliberately rejected a fourth evidence-basis epoch or generic `epoch[n]` abstraction. The stronger product question was instead:

> How can a researcher explicitly initiate one changed evidence basis from inside the existing governed product using already-proven concrete authority boundaries?

Milestones 44A–44G answer that question for the first changed-basis path above an ordinary 31A-launched governed session.

## Current first changed-basis product flow

The implemented product path is now:

```text
ordinary governed 31A-backed session
→ 44A prepare changed evidence basis
→ 44B persist explicit 33B cross-working-set transition
→ 44C persist first 34A revision root
→ 44D persist first 34B post-root ordinary edge
→ 44E explicitly adopt the 35A root-backed governed session
→ 44F freshly prove 35B reconstructability
→ 44G persist the verified session as a 35C restart overlay
```

Each arrow is a distinct authority step. The series deliberately does not collapse preparation, transition, root creation, governed-session adoption, fresh reconstruction, or restart persistence into one opaque action.

The resulting 35C overlay is existing root-backed operational configuration. It is not evidence, a global branch pointer, a latest/current/head record, or permission to replace whichever controller the 44-series shell currently has mounted.

---

## 44A / D218 — Explicit Changed-Evidence-Basis Preparation

44A exposes the established 33A preparation boundary from an already-governed research shell.

The caller supplies one or more exact already-loaded/relinked application evidence objects. The researcher can inspect those objects only as candidate appended members, enter a new human rationale, and provide two explicit no-overwrite destinations for the changed working set and changed working-set note.

Persistence delegates to the public 33A boundary.

A successful 44A action proves only:

```text
current declared working set
+ explicit candidate appended evidence
+ explicit human rationale
→ durable prepared changed basis
```

It does not adopt that basis or alter the mounted governed controller.

### Staleness rule

An unadopted endpoint-revision write does not invalidate the prepared candidate because `last_endpoint_revision` is not declared-session authority.

An explicit 30A rollover that replaces the governed controller before preparation persistence makes the old unsaved form stale rather than silently retargeting it.

---

## 44B / D219 — Explicit First Changed-Basis Transition

44B exposes the existing 33B cross-working-set transition only where an exact ordinary `ChromiumResearchSessionReentryResult` proves the shell belongs to the pre-root ordinary launch family.

The action requires:

1. one exact successful 44A preparation;
2. the exact retained ordinary 31A re-entry;
3. explicit current durable source for the declared endpoint;
4. explicit durable sources for the prepared working set and note; and
5. one explicit no-overwrite transition destination.

All locator inputs begin blank.

The product then delegates through existing 33B creation, persistence, and fresh relinking.

Successful 44B persistence leaves the mounted governed session unchanged. The transition is durable historical evidence of an explicit evidence-basis crossing, not adoption of that branch.

---

## 44C / D220 — Explicit First Changed-Basis Revision Root

44C exposes the existing 34A first revision-root boundary from one exact successful 44B transition.

The researcher must author genuinely new rationale text and explicitly supply the five durable locations required by the established 34A boundary:

- prior endpoint edge source;
- changed working-set source;
- changed working-set-note source;
- 33B transition source;
- no-overwrite 34A root destination.

The 44A/44B output paths may be displayed as historical receipt context but are not copied into the inputs or promoted into continuing path authority.

The application helper freshly relinks the transition before persistence and again through the public 34A loader after persistence.

A successful root remains historical changed-basis lineage and does not itself replace the mounted controller.

---

## 44D / D221 — Explicit First Post-Root Ordinary Edge

44D exposes the existing 34B one-time bridge from the first 34A root back into ordinary 24B edge lineage.

Inputs are deliberately narrow:

- genuinely new human rationale;
- explicit current durable 34A root source;
- explicit no-overwrite first-edge destination.

Successful persistence uses the existing ordinary 24B edge format and then freshly reloads the edge through the root-specific 34B boundary.

The product still does not declare a sequence, construct a governed root-backed session, or alter whichever old-basis controller remains mounted.

---

## 44E / D222 — Explicit Changed-Basis Governed-Session Adoption

44E is the first 44-series action that intentionally changes the shell's governed branch.

From one exact successful 44D result, the researcher supplies:

- explicit current durable source for the first post-root edge; and
- explicit no-overwrite destination for the existing-format 26B root-backed declaration.

The exact loaded 34A root retained by the 44D result is already the explicit starting record, so no root path input is added.

The established 35A machinery then performs:

```text
exact loaded 34A root
+ explicit first-edge source
→ fresh root-started 26A sequence
→ existing 26B declaration
→ fresh 26C declaration relink
→ existing ChromiumResearchSessionController
→ explicit shell-local branch adoption
```

After successful adoption, the new 35A controller becomes the shell's governed controller and the ordinary revision/rollover surface is rebuilt over that changed-basis session.

This is shell-local explicit branch adoption only. It creates no global latest/current/head authority.

### No restart authority yet

44E deliberately clears ordinary restart/re-entry authority after adoption.

```text
35A in-process governed-session adoption
!=
35B fresh-process reconstructability
```

---

## 44F / D223 — Explicit Root-Backed Fresh-Process Verification

44F exposes the established 35B reconstruction boundary as a separate verification action after exact 44E adoption.

The exact initial ordinary 31A plan remains retained application state from the launch lineage. All current durable locators required to reconstruct the changed-basis region begin blank and must be explicitly supplied again.

The application helper constructs the exact 35B typed plan and freshly reconstructs the historical 44E root-backed session.

It then proves at minimum that the fresh result retains the exact expected:

- root identity;
- declaration identity;
- declared endpoint identity and rationale; and
- governed presentation.

Successful 44F verification does **not** replace the currently mounted controller and does not write restart configuration.

This remains true if the mounted 44E session has already rolled to a later continuation. 44F verifies the exact historical 44E target selected by the retained product evidence rather than silently retargeting to whatever is currently mounted.

---

## 44G / D224 — Persist Verified Root-Backed Restart Overlay

44G takes one exact successful 44F verification and exposes the established public 35C proof-gated persistence boundary.

Two explicit durable inputs begin blank:

1. current durable source for the matching ordinary 31B v1 plan document; and
2. no-overwrite destination for `pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1`.

Public 35C remains authoritative for:

```text
ordinary 31B decode
→ exact prior-plan equality
→ fresh 35B reconstruction
→ presentation/root/endpoint coherence
→ exclusive no-overwrite overlay write
→ strict round-trip overlay decode
```

44G adds only product-level identity checks against the exact 44F proof and a dedicated Textual persistence surface.

### Historical target semantics

The 44G persistence subject is the exact historical session verified by 44F.

If the mounted shell has subsequently rolled farther, persistence still writes restart configuration for the historical 44E/44F root-backed session while leaving the later mounted controller untouched.

Therefore:

```text
persisted 44G overlay target
!=
implicit claim about currently mounted session
```

44G does not set `research_reentry`, replace `research_controller`, mount generic restart controls, relaunch from the overlay, or checkpoint a later 35D continuation.

### Final validation

PR #167 merged 44G from exact tested head:

```text
eb5599d71a571de4a2d2153059b4f8e8bf69e6e7
```

Repository Zero workflow run `33191039137` passed the complete suite on Python 3.11, 3.12, 3.13, and 3.14.

The final 44G change remained exactly seven files with no workflow/debug-instrumentation changes.

---

## Reuse lessons reinforced by the 44-series

### 1. Productization does not require duplicating lower-level authority

44A–44G repeatedly expose already-proven 33A–35C application boundaries through narrow product wrappers and dedicated Textual surfaces.

The product layer may add exact retained-object and mounted-state coherence checks, but it does not become a second implementation of persistence, relinking, or ancestry proof.

### 2. Prior path use is not continuing path authority

Every durable locator field that matters to the current operation begins blank unless an existing typed in-memory object already provides the required authority directly.

Historical receipt paths may be shown for context, but they are not silently copied, searched, or treated as current.

```text
previously used path
!=
currently authorized locator
```

### 3. Historical durable lineage may coexist with later mounted work

The 44B transition, 44C root, 44D first edge, 44F verification target, and 44G overlay can remain truthful historical records even while the mounted shell continues on another branch or later continuation.

Coexistence does not itself establish chronology, preference, or head authority.

### 4. Explicit adoption is stronger than successful preparation or persistence

The 44-series has two places where user choice must remain especially visible:

- 44E explicitly adopts the changed-basis governed controller;
- a later product boundary must explicitly decide whether a successful 44G result should be handed into the already-proven root-backed session shell.

Neither action is allowed to occur merely because the required durable artifacts exist.

---

## Authority boundaries still intentionally absent

Through 44G, Pyxis still does **not** claim or infer:

- a globally current/latest/canonical research session;
- complete revision history or unique successor relationships;
- chronology from paths, filenames, hashes, or filesystem timestamps;
- branch preference merely because one durable lineage was persisted later;
- durable identity from path equality;
- persistent path authority from a successful prior operation;
- source authenticity, authorship, or trusted time from SHA-256 integrity;
- semantic improvement from changed rationale text;
- evidentiary support merely because human notes are attached to evidence;
- quotation/citation authority from exact source selection alone;
- browser navigation or autonomous interaction authority from read-only observation;
- a generic fourth evidence-basis epoch or recursive `epoch[n]` ancestry model;
- automatic restart/adoption merely because a valid 35C overlay was written.

These remain deliberate product constraints.

## Current decision frontier after 44G

The implemented frontier is **44G / D224**.

The next approved product question is tracked as **44H / D225 in issue #168**:

> After successful 44G persistence, can the researcher explicitly leave the current 44-series shell and continue immediately in the already-proven root-backed product shell using the exact freshly proven in-memory 35C result, without reloading the just-written overlay or treating its path as current/head authority?

The proposed handoff subject is exactly:

```text
44G result.checkpoint.fresh_reentry
```

That object is already a freshly proven `ChromiumResearchRootBackedSessionReentryResult`, which is the existing input accepted by `RootBackedResearchSessionShell`.

The intended distinction follows the already-proven 36D and 41E handoff pattern:

```text
successful persistence
!=
automatic mode change

explicit typed in-process handoff
!=
persistent path authority
```

44H is not yet implemented merely because this continuity document records the decision frontier.

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
