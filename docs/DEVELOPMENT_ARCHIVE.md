# Pyxis Development Archive

**Continuity snapshot — 2026-08-13; Repository Zero current through Milestone 11T / D115.**

This is the canonical development-continuity front door. The exact detailed pre-consolidation archive remains preserved in Git history at commit `675f2b5e37b5edb32d17e9e480a4d16246826486`. Nothing from that history was discarded; this file makes the current checkpoint explicit and points back to the accumulated reasoning when deeper context is needed.

Read alongside:

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — current architectural boundaries through 11T;
- [`DECISIONS.md`](DECISIONS.md) — current normative decisions through D115;
- the source tree — the permanent Repository Zero implementation; and
- the milestone files — the narrow proof record for each later step.

---

## 1. What Pyxis is now

Pyxis began as a Python-first browser/research harness: conserve mature Chromium/browser infrastructure and expose Python capability around it rather than rebuilding a browser from scratch.

Repository Zero revealed the more general product thesis:

```text
human architectural intent
    ↓
canonical authoring state
    ↓
Repository Intermediate Representation
    ↓
deterministic compiler
    ↓
inspectable generated implementation
    ↓
runtime
```

The browser/research product remains a foreseeable application. Repository Zero deliberately proves the compiler path first with the tiny `text_lab` Workspace. `inspect_text` and `normalize_text` are controlled test weights, not the product domain.

---

## 2. Durable principles

The principles that repeatedly survived implementation pressure remain:

1. **Conserve mature infrastructure.** Chromium should remain Chromium; Python-first does not mean rebuilding every lower layer.
2. **Keep human intent visible.** A user should be able to trace intended architecture through canonical state, RIR, compiler nodes, files, and runtime behavior.
3. **Canonical state is authoritative.** Generated code is a consequence, never a second source of truth.
4. **Preview before architectural mutation.** Proposed state is distinct from current evidence until governed Apply succeeds.
5. **Rationale is provenance.** Architectural changes require human rationale and append-only revision history.
6. **Compiler evidence beats inference.** Incremental status belongs to the compiler; filesystem integrity may validate materialization but does not become a shadow classifier.
7. **Separate compilation, materialization, runtime, and export.** Runtime does not compile; export packages exact compiler output.
8. **READY is evidence-derived.** A directory on disk is not READY.
9. **Presentation renders owned evidence.** It does not rediscover state or silently acquire missing facts.
10. **UI events cross named application operations.** Textual is downstream of application-owned semantics.
11. **One controller owns live transient state.** Renderer state is not a second product authority.
12. **Measurement observes before interpreting.** Descriptive evidence is allowed; causal or evaluative labels require separately justified evidence.
13. **Exact work evidence stays exact.** Do not rename equality classes into warm/cold/cached/steady-state/outlier concepts without proof.
14. **Restraint is an architectural feature.** A technically possible abstraction or statistic is not automatically a product requirement.

---

## 3. Repository Zero checkpoint before the measurement tail

By the end of Milestone 10, Repository Zero had already proven:

- canonical `WorkspaceSpec → RIR → compiler → materializer → runtime` boundaries;
- append-only revision intent/completion provenance;
- evidence-backed incremental generation and artifact integrity;
- exact-byte export, conventional Python package projection, verified wheel construction, and fresh offline wheel installation/execution;
- framework-independent `WorkspacePresentation` and honest reopening of durable versus transient evidence;
- application-owned runtime rerun, architecture preview, rationale-bearing Apply, and verified export refresh;
- one `WorkspaceController` as the live transient-state authority; and
- the first local Textual Workspace UI covering inspection, runtime, proposed architecture, governed Apply, READY retirement, and verified READY restoration.

That stability made measurement safe to add as observation rather than redesign.

---

## 4. Measurement progression through 11T

Milestones 11A–11J established the measurement spine: observe the established build/run operation; retain exact compiler/materializer work facts; add Repository/Workspace/RIR identity, privacy-preserving workload identity, coarse execution-environment identity, exact-condition cohorts, raw stage samples, exact-work partitioning, count/min/max envelopes, and median.

The exact pre-consolidation architecture, decision record, and development archive at commit `675f2b5e37b5edb32d17e9e480a4d16246826486` contain the detailed reasoning through that point.

The later sequence stayed intentionally narrow:

### 11K — arithmetic mean

Mean was added as a separate immutable layer over the existing median provenance chain, but recomputed independently from raw group durations. The acceptance fixture deliberately made mean differ from median so a detached or copied statistic could not masquerade as evidence.

### 11L — population standard deviation

Population standard deviation describes only the complete exact recorded work-context group. It retains exact 11K mean provenance and makes no inferential claim about a larger population.

### 11M — descriptive summary bundle

The bundle validates that envelope, median, mean, and dispersion belong to one exact source chain. It computes nothing new.

### 11N — read-only measurement presentation

Presentation projects exact summary evidence into a stable read-only shape while preserving stage/group order and exact work provenance. No statistic, semantic work label, score, or causal interpretation is added.

### 11O — Textual renderer

Textual receives an existing presentation and only renders it. Tests explicitly block measurement, compiler, runtime, and re-projection work from the renderer.

### 11P — optional Workspace co-display

The normal Workspace shell may mount an already-supplied measurement presentation. No measurement controls or renderer-owned refresh/acquisition path is introduced.

### 11Q — provenance gate

Co-display requires Repository ID, Workspace ID, and exact RIR SHA-256 to match current Workspace presentation before Textual initialization.

### 11R — live invalidation

Same-RIR and failed operations keep a coherent snapshot. A successful RIR-changing Apply removes it only after the existing governed Apply path succeeds.

### 11S — non-evidence invalidation notice

After stale measurement evidence has already been removed, a fixed transient UI notice may explain why. The notice carries no measurement object/statistics or controls and expires on the next user operation.

### 11T — caller-supplied re-entry

While no measurement snapshot is mounted, a caller may supply an already-produced presentation for the current RIR. The shell applies the existing Repository/Workspace/RIR gate before mutation, mounts the exact object on success, clears the old notice only after successful mount, and rejects mismatches or replacement attempts without changing shell evidence.

No renderer-owned measurement acquisition, re-projection, recomputation, or refresh semantics were introduced.

---

## 5. Why the central documents were consolidated here

`MILESTONE_11K_CONTINUITY.md` records a tooling limitation: the GitHub connector rejected the large whole-file replacements needed to fold later measurement work into the already-large central documents. The project correctly chose not to risk truncating or rewriting history, so 11K–11S accumulated as milestone addenda.

That preservation choice was correct, but by 11S the onboarding path had become split: README still described Milestone 9 as current, ARCHITECTURE stopped its measurement narrative at 11J, DECISIONS stopped at D106, and this archive's header stopped at 11J even though implementation and tests had advanced substantially.

The 11T continuity reconciliation resolves that without discarding history. The exact prior files remain recoverable in Git at commit `675f2b5e37b5edb32d17e9e480a4d16246826486`; their canonical paths are now concise current front doors through 11T and the milestone files remain the detailed later proof trail.

This is a continuity migration, not a historical rewrite.

---

## 6. Current risks and discipline

### Evidence-model complexity

The measurement pipeline is now deep enough that provenance discipline itself creates abstraction cost. Count/min/max, median, mean, population standard deviation, bundle, projection, renderer, co-display, invalidation, notice, and re-entry are all individually justified—but further statistical layers should not be added merely because they are easy to compute.

The descriptive set is sufficient to prove the architecture. New measurement semantics should require a concrete product question.

### Demonstrator-specific operations

`remove_normalize_text` remains an intentionally concrete architecture operation. Do not generalize it into a generic editing framework until a second genuine architecture edit supplies pressure that the current operation shape cannot satisfy.

### Python support claim versus CI proof

The package currently declares Python `>=3.11` while the ordinary workflow proves Python 3.11. This is not a Repository Zero blocker, but future release hardening should either prove another supported interpreter lane or narrow the declared support contract.

### Measurement is still descriptive

Do not turn timing/work correlations into causal claims. Work-context equality is evidence equality, not proof of cache state, warmup, efficiency, waste, normality, or steady state.

---

## 7. Current development checkpoint

Repository Zero now has four completed proof families:

```text
compiler / runtime / revision / export lifecycle
            +
interactive evidence UI
            +
descriptive measurement pipeline
            +
live measurement provenance / invalidation / re-entry
```

The full Repository Zero test workflow passes on the 11T branch.

The next implementation milestone should come from an actual Pyxis product requirement. Do not automatically continue the 11-series by adding another statistic. If the next real pressure is a second architecture operation, broader journey measurement, browser integration, persistence, or another surface, first state the product question and then extend the narrowest permanent boundary that answers it.

---

## 8. Historical map

For the detailed reasoning that produced the current state:

- inspect `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, and `docs/DEVELOPMENT_ARCHIVE.md` at commit `675f2b5e37b5edb32d17e9e480a4d16246826486` for the exact pre-consolidation records;
- read `MILESTONE_11K_CONTINUITY.md` for why the central docs temporarily lagged; and
- read `MILESTONE_11L.md` through `MILESTONE_11T.md` for the narrow later proof trail.

Those records are evidence of how Pyxis arrived here. The canonical front-door documents describe where Pyxis stands now.
