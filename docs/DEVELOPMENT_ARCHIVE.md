# Pyxis Development Archive

**Continuity snapshot — 2026-08-11; Repository Zero status updated through Milestone 9N on 2026-08-12**

This document preserves the reasoning that produced Pyxis, not just the current code. It exists so a future development session can continue from the accumulated lessons instead of rediscovering them or flattening the project into a generic code generator.

It should be read alongside:

- `ARCHITECTURE.md` — current architectural boundaries
- `DECISIONS.md` — implementation decisions already treated as constraints
- the source tree — the permanent Repository Zero implementation

---

## 1. What Pyxis became

Pyxis began as a Python-first browser/research harness: keep Chromium for the mature browser work it already does well, then expose Python capabilities around it instead of rebuilding a browser from scratch.

That starting point produced a broader engineering thesis:

> Python already provides enormous capability. Pyxis should conserve effort by composing existing strengths, make the transformations visible, and measure the cost of getting from intent to execution.

During prototyping, the center of gravity became clearer. The strongest reusable idea was not any one browser feature. It was the transparent path from human architectural intent to executable software:

```text
human intent
    ↓
canonical authoring state
    ↓
Repository Intermediate Representation (RIR)
    ↓
compiler
    ↓
generated implementation
    ↓
runtime
```

The browser/research product remains a foreseeable application of that architecture, but Repository Zero deliberately proves the compiler path first with a tiny `text_lab` Workspace.

`inspect_text` and `normalize_text` are not the product domain. They are controlled test weights for the architecture.

---

## 2. Product principles that survived implementation pressure

These principles repeatedly survived real implementation tests and should be treated as durable unless contrary evidence appears.

### 2.1 Chromium should remain Chromium

Pyxis should not spend engineering effort recreating mature browser infrastructure. Browser integration should eventually compose with Chromium rather than replace it.

### 2.2 Python-first does not mean Python-only ideology

Python is the preferred orchestration and capability language because of its ecosystem, readability, and usefulness as an educational surface. The deeper rule is to use mature tools rather than rebuild them unnecessarily.

### 2.3 Human intent must remain visible

A user should be able to trace:

```text
I asked for this
      ↓
Pyxis represented it this way
      ↓
therefore these compiler nodes exist
      ↓
therefore these files exist
      ↓
therefore this runtime behavior exists
```

If the system cannot explain that path, it is drifting away from the original value proposition.

### 2.4 Canonical source is authoritative

Generated code is a consequence, not a second source of truth.

UI actions, restore actions, export actions, and educational lessons must not patch generated files to simulate architectural change.

### 2.5 The compiler should be inspectable and deterministic

The same canonical state should lower to the same RIR and the same RIR should produce the same compiler products.

This is necessary for explanation, provenance, caching, waste measurement, testing, and safe revision behavior.

### 2.6 Evidence beats inference

Whenever the compiler already knows what happened, the UI should render that fact rather than infer it from Git, timestamps, filesystem shape, or heuristics.

Examples include artifact statuses such as `new`, `reused`, `regenerated`, and `removed`.

### 2.7 Changes should be previewed before mutation

Architectural edits should first produce a proposed canonical/RIR state and show their consequences.

Preview may derive and compare. It may not mutate.

### 2.8 Human rationale is part of provenance

A structural diff explains *what* changed. It does not explain *why*.

Architectural revisions therefore need an intent-bearing rationale before compilation.

### 2.9 History is append-only

Restore is not rollback. Reapply is not history rewriting.

Returning to an earlier architecture should create a new revision whose state happens to match an earlier state. The intervening history remains intact.

### 2.10 Export is packaging, not compilation

Portable output must package the exact compiler products that already ran inside Pyxis.

Export must not regenerate, reinterpret, or patch implementation.

### 2.11 READY is evidence-derived

A UI may show READY only because verification evidence says the output is ready, not because files happen to exist.

### 2.12 Pyxis should teach by being inspectable

The educational opportunity is not a tutorial bolted onto a code generator.

A transparent compiler lets users learn Python and software architecture by observing real consequences of real changes.

---

## 3. The broad architecture explored before Repository Zero

Before the current minimum slice was chosen, a larger architecture was developed. It is intentionally archived here so it is not lost, while remaining deferred until the core path is stable.

### Capability Cards

Capabilities were described by explicit purpose, inputs, and outputs rather than hidden ad hoc functions.

### Execution Graphs

Runtime work was modeled as explicit graph structure rather than opaque orchestration.

### Observation Pipeline

A recurring pipeline was defined as:

```text
Acquire → Assess → Observe → Normalize → Correlate → Present
```

This came from browser/research and OCR work where preserving what was observed separately from what was concluded proved important.

### Immutable Evidence Objects

Evidence should carry provenance, confidence, timestamps, spatial relationships where relevant, and stable identity.

### Rule Engine and Finding Objects

Rules consume evidence and produce findings. Rules do not mutate the evidence they inspect.

### Workspace Sessions

A Workspace session was envisioned as a timeline of snapshots, permissions, metrics, evidence references, and outputs.

### Explicit state machines

Mutable entities should have declared lifecycle transitions rather than informal status changes.

### Capability Test Harness

Capabilities should eventually ship with fixture, contract, security, and performance tests.

### Service Registry / dependency injection

External services and model providers should remain replaceable rather than being hardwired into capability logic.

### Capability Lifecycle

The explored lifecycle was:

```text
Proposed
→ Designed
→ Scaffolded
→ Implemented
→ Verified
→ Certified
→ Stable
→ Deprecated
→ Archived
```

### Planning Graph separate from Execution Graph

The plan for what should happen and the record of what did happen are different objects and should not be collapsed.

### Execution Ledger

Time, resource use, cache behavior, service calls, and avoidable work were intended to become machine-accounted evidence rather than vague performance impressions.

### Bootstrap Specification

A declarative bootstrap document was explored as the source for repository generation.

### Capability Registry

Capabilities should eventually be explicit registry entries rather than discovered implicitly from filesystem shape.

### Canonical Repository Layout

A larger repository organization was explored around Governance, Knowledge, Runtime, Capabilities, Interfaces, Quality, and Documentation.

### Capability Composition Specification

Atomic capabilities and declarative workflows should be separable.

### Canonical Data Model

The larger data model considered Identity, Configuration, Planning, Execution, Evidence, Evaluation, Artifacts, and Governance.

### Repository Constitution

A highest-level governance document was envisioned to declare architectural rules that lower-level generators may not violate.

None of these concepts are discarded. They are intentionally downstream of Repository Zero.

---

## 4. What implementation taught us

The most valuable lessons did not come from naming abstractions. They came from repeatedly forcing the architecture through small executable proofs.

### 4.1 A lesson must change canonical state, not fake generated output

The first useful educational proof removed `normalize_text` from canonical architecture and let the compiler propagate the consequence.

This established a durable rule:

> Educational lessons must invoke the real architecture path.

Otherwise the learner is being shown theater rather than the system.

### 4.2 Performance metrics need a human journey

Timing and waste became useful only when attached to a concrete workflow such as first compile → first run → guided edit → recompile.

Abstract compiler benchmarks did not explain whether the product was wasting the user's time.

### 4.3 Full-tree regeneration created measurable waste

A guided change that removed one capability exposed unnecessary regeneration of unaffected code.

That led to node-level semantic fingerprints and artifact integrity checks.

The important rule was not simply “cache files.” It was:

> Reuse is valid only when the semantic node is unchanged *and* the existing generated artifact still matches the compiler's recorded artifact hash.

This prevents a manually altered generated file from being silently accepted as reusable compiler output.

### 4.4 Incremental status belongs to the compiler contract

`new`, `reused`, `regenerated`, and `removed` are not UI guesses. They are compiler facts.

The UI should display compiler explanations directly.

### 4.5 Restoration must pass through current intent

Restoring `normalize_text` by recovering an old generated file would have violated the architecture.

The correct path is current canonical intent → RIR → compiler → new generated artifact.

This distinction became the foundation for safe revision history.

### 4.6 Git is useful but not sufficient provenance

Git can record file changes. It does not inherently capture the user's architectural rationale, proposed state, compiler consequence, or runtime consequence in the product model.

Pyxis therefore explored its own append-only revision events while still expecting Git to remain useful repository infrastructure.

### 4.7 Reapply is state reproduction, not rollback

A prior canonical state can be selected and reproduced as a new revision.

That preserves the full path:

```text
remove → restore → reapply
```

rather than pretending the middle event never happened.

### 4.8 Preview can predict structure, but should not invent a shadow runtime

Pyxis can safely predict observable behavior that follows directly from canonical structure—for example, which capability result keys will exist.

It should not simulate generated implementation details in a parallel “preview runtime.”

### 4.9 Consolidation became more valuable than new abstractions

A series of small proofs eventually created a new risk: fragmentation.

The response was to stop creating one-off demonstrators and require each proven concept to participate in one coherent first-run path.

This was the transition from prototypes to Repository Zero.

### 4.10 Portability became a compiler-ownership test

If an exported Workspace can run independently while preserving the same RIR identity and artifact hashes, that is evidence that implementation truly belongs to the compiler products rather than hidden Pyxis runtime magic.

### 4.11 Packaging exposed an honest environment constraint

An early clean-install proof failed because the target virtual environment did not contain `setuptools`.

The lesson was important: do not weaken acceptance criteria or claim success around infrastructure gaps.

The prototype was eventually made self-contained enough to prove a network-disabled clean installation using a tiny local standard-library build backend.

That proof is useful history, but Repository Zero should still prefer conventional tooling where it is available rather than making bespoke packaging infrastructure part of the core product prematurely.

Repository Zero later separated source-build evidence from installation evidence. A conventional source package builds a standard wheel using ordinary PEP 517 build isolation when build dependencies are obtainable. The verified wheel can then be installed and executed in a fresh virtual environment while network access is actively blocked. Because installation consumes a prebuilt wheel, Setuptools is not needed during that installation proof.

Milestone 9M tested the stronger source-build condition directly. The exact planned package bytes were copied into a disposable build context, normal PEP 517 build isolation was preserved, index/network access was disabled, and no vendored dependency, fallback backend, or workaround was supplied. The build failed before producing a wheel because the isolated environment could not resolve `setuptools>=77.0.3`.

Milestone 9N then resolved the requirement rather than changing packaging: offline rebuilding from raw source is not part of the Repository Zero portable contract. The portable deliverable is the conventional source repository plus the already-verified wheel. Offline guarantees attach to installation and execution of that verified wheel.

---

## 5. Prototype and Repository Zero decision sequence

The numbered decisions capture the narrowing process.

### D055 — Guided Architectural Delta
Teach by modifying canonical architecture and letting the compiler expose consequences.

### D056 — Local Learning and Waste Report
Attach timing and waste to a user journey rather than abstract compiler throughput.

### D057 — Node-Level Incremental Generation
Reuse generated output only when semantic fingerprints and artifact integrity both agree.

### D058 — Visible Incremental Compilation
Expose compiler-derived artifact statuses and explanations to the user.

### D059 — Safe Capability Restoration
Restore from current canonical intent rather than deleted generated files.

### D060 — Append-Only Canonical Revision Events
Record operation, rationale, before/after hashes, chain identity, and compiler completion.

### D061 — Workspace Revision Timeline
Combine human rationale with compiler and runtime consequences in one history view.

### D062 — Reapply Canonical State as a New Revision
Reproduce prior state without rewriting history.

### D063 — Preview-First Reapply
Historical state may not be reapplied without first showing its architectural delta.

### D064 — Consolidated Minimal Product
A feature is not part of the product until it participates in the same first-run path.

### D065 — Installable CLI and Independent Export
Portable compiler products should execute independently from the Pyxis source tree.

### D066 — Verified Export
Export becomes READY only after provenance and runtime verification.

### D067 — Visible READY State
Readiness in the interface must come from verification evidence.

### D068 — Real Workspace Creation
First-run authoring should begin with only Workspace name and description.

### D069 — Created Workspace Runs Immediately
A newly created Workspace should quickly reach observable generated behavior.

### D070 — Preview Architectural Edits Before Compilation
Derive proposed state in memory and prohibit mutation until Apply.

### D071 — Architecture Changes Require Rationale + Provenance
A compiler diff does not explain intent; rationale belongs in the revision record.

### D072 — Reversible Change Uses the Same Path
Restoration is another forward revision, not rollback.

### D073 — Preview Includes Predicted Runtime Contract
Predict only runtime surfaces directly implied by canonical structure.

### D074 — Consolidate the First-Run Product Before Adding Features
The architectural risk shifted from insufficient proof to fragmented proofs.

### D075 — Export Is a Consequence of the Product Path
Export packages existing compiler products rather than introducing a parallel generator.

### D076 — First Run Ends With Export
Portability becomes part of the same Workspace journey.

### D077 — Package-Ready Repository
Portable output should look conventional to another Python developer.

### D078 — Self-Contained Install Proof
The prototype demonstrated clean, network-disabled installation while preserving generated artifact identity.

### D079 — Separate Source-Build and Wheel-Install Portability Proofs
Repository Zero separated conventional source-to-wheel construction from verified-wheel installation/execution.

### D080 — Reproduce a Portability Constraint Before Choosing Its Remedy
Repository Zero reproduced the offline PEP 517 build-dependency failure before deciding whether it deserved a solution.

### D081 — Portable Deliverable Is Conventional Source Plus a Verified Wheel
Repository Zero resolved D078 in favor of the smallest proven product contract. Offline installation/execution of the verified wheel is required; offline rebuilding from raw source is not.

`DECISIONS.md` remains the compact normative record; this archive records why those decisions emerged.

---

## 6. Transition to Repository Zero

After D078, the architecture had survived a sufficiently strong prototype chain:

```text
author
  ↓
represent
  ↓
compile
  ↓
execute
  ↓
alter
  ↓
recompile
  ↓
export
  ↓
install elsewhere
  ↓
execute again
```

At that point, further disposable proof repositories had diminishing value.

The development mandate changed from:

> prove that the architecture could work

into:

> construct the permanent reference implementation from the proven architecture

This transition is important. Future work should not restart broad architectural exploration unless Repository Zero reveals a real contradiction.

---

## 7. Current Repository Zero implementation

Repository Zero has now carried the architecture through the permanent path rather than merely preserving prototype intent.

### 7.1 Authoring and canonical persistence

`WorkspaceSpec` remains the authoritative intent object. Workspace builds persist deterministic canonical state under `authoring/canonical/workspace.json` and reload it without deriving truth from generated code.

### 7.2 RIR persistence

Canonical state lowers deterministically into `RepositoryIR` / `WorkspaceIR`, persisted as `generated/repository.rir.json`. A strict read-only loader reconstructs typed RIR for later verification and runtime use.

### 7.3 Compiler products and generation evidence

The compiler emits deterministic `GeneratedArtifact` values for the `text_lab` capabilities and Workspace entrypoint. The generation manifest records RIR identity plus artifact paths, semantic node hashes, and artifact hashes.

Generation status is compiler evidence: `new`, `reused`, `regenerated`, or `removed`.

### 7.4 Incremental materialization

Materialization reconciles current compiler products against prior manifest ownership. Reused artifacts are not rewritten; regenerated/new artifacts are written; removed artifacts are deleted only when the prior manifest established compiler ownership.

Filesystem discovery does not substitute for compiler evidence.

### 7.5 Revision provenance

Architectural change follows preview → rationale → append-only revision → canonical mutation → compiler completion. Removal and restoration of `normalize_text` both use the same current-intent path; restore is a forward revision, not rollback.

### 7.6 Runtime

`run_materialized_workspace()` executes generated implementation from the materialized tree and does not compile or write. Runtime suppresses bytecode-cache writes so the repository boundary remains read-only in observable filesystem terms.

### 7.7 Verified export

Export follows the permanent application path:

```text
existing BuildResult
      ↓
ExportPlan
      ↓
exact-byte portable materialization
      ↓
exported RIR / manifest / artifact identity verification
      ↓
source ↔ export runtime equivalence
      ↓
READY
```

READY is derived only after identity and runtime evidence succeed for the same export tree, Repository, and Workspace.

### 7.8 Conventional source projection

The verified export projects compiler products byte-for-byte into a conventional `src/` package layout. Packaging support files remain a distinct ownership class.

The materialized `src/` package executes in a fresh subprocess with Pyxis unavailable and reproduces the already-verified Workspace behavior.

### 7.9 Standard wheel and offline installation

The conventional source package builds a standard wheel using ordinary PEP 517 tooling when its declared build dependencies are obtainable. Wheel inspection verifies that compiler-product bytes inside the archive still match their recorded hashes and that no Pyxis package has leaked into the payload.

The verified wheel installs into a fresh virtual environment with index access disabled, dependencies disabled, network resolution/connections blocked, user/system site leakage excluded, and Pyxis imports rejected. The installed console command reproduces verified package behavior.

### 7.10 Portable deliverable contract

Milestone 9N defines the permanent Repository Zero portable deliverable as:

```text
conventional source repository + verified wheel
```

The source form preserves inspectability, provenance, exact compiler-product relationships, and conventional Python packaging. The wheel form is the verified offline-installable execution artifact.

Offline source-to-wheel construction was characterized in 9M and fails because normal PEP 517 isolation cannot resolve `setuptools>=77.0.3` without an available index/build dependency. Under D081 that is an accepted source-build limitation, not an unresolved Repository Zero defect.

No local backend, vendored Setuptools, or weakened build isolation is required to close Milestone 9.

### 7.11 Application surfaces

The CLI remains a thin interface over application orchestration. `examples/text_lab/` is the permanent executable specification for the minimum Workspace. Export has a thin application-level orchestration seam over the proven build/export APIs.

---

## 8. Proof status

Repository Zero is exercised by GitHub Actions on Python 3.11. The development sequence repeatedly ran the complete pytest suite after each narrow step.

The portability suite has executed real conventional wheel builds, independent source-layout runtime checks, fresh virtual-environment creation, network-blocked local-wheel installation, execution of the installed console command, and explicit offline source-build characterization.

The permanent rule remains:

> Never broaden a claim beyond the exact condition that was executed and verified.

D081 follows that rule. It chooses the product boundary already supported by evidence instead of inventing infrastructure to satisfy a stronger condition for which Repository Zero has no demonstrated need.

---

## 9. Milestone 9 closure

Milestone 9 — export as packaging — is complete for Repository Zero.

The proven chain is:

```text
exact compiler products
      ↓
verified portable export
      ↓
conventional source projection
      ↓
independent source-layout runtime
      ↓
standard wheel
      ↓
wheel payload identity verification
      ↓
fresh offline wheel installation
      ↓
installed execution with matching behavior
```

The deliverable is source plus verified wheel. Offline rebuilding from raw source is outside the Milestone 9 acceptance contract.

The 9M failure remains useful characterization evidence because it prevents future developers from accidentally claiming that conventional source builds are network-independent. It should not trigger a packaging redesign unless a future real product use case explicitly requires offline source reconstruction.

---

## 10. Foreseeable implementation path

The original milestone order proved useful:

- Milestone 1 — executable CI: complete.
- Milestone 2 — canonical persistence: complete.
- Milestone 3 — RIR + generation evidence: complete.
- Milestone 4 — thin CLI: complete.
- Milestone 5 — permanent `examples/text_lab/`: complete.
- Milestone 6 — preview-first architectural edit: complete.
- Milestone 7 — rationale-bearing append-only revisions and restoration: complete.
- Milestone 8 — evidence-backed incremental generation: complete.
- Milestone 9 — verified export, conventional source, verified wheel, and offline installed execution: complete.

### Milestone 10 — First local Workspace UI

The next major product step is the first local Workspace UI.

It must orchestrate the existing application boundaries rather than absorb compiler, revision, export, or packaging behavior. The UI should make the already-proven evidence chain visible rather than create a second implementation path.

A good first slice should remain small: create/open the permanent `text_lab`-style Workspace, show canonical/RIR/compiler evidence, run it, show READY/export evidence, and expose existing preview/revision operations through application APIs.

### Milestone 11 — Measurement

Reintroduce time and waste accounting once there is a stable user journey worth measuring.

The Execution Ledger can then evolve from real observations rather than imagined fields.

### Milestone 12 — Browser/research capabilities

After the compiler/product spine and first-run journey are stable, return to the original browser/research purpose.

Chromium remains the browser. Pyxis adds inspectable Python capabilities, evidence, provenance, permissions, and workflows around it.

---

## 11. What should remain deferred

Do not let archived ideas create pressure to implement them immediately.

Until the first permanent Workspace UI and lifecycle are solid, defer:

- broad capability marketplaces/catalogs
- model-provider abstractions beyond a real need
- autonomous agent permission systems
- browser replacement work
- complex visual editors
- branching/merge semantics for revision history
- distributed execution
- deployment platforms
- broad plugin systems
- premature optimization
- large schema/generalized ontology work
- bespoke offline source-build infrastructure without a demonstrated requirement

Repository Zero should stay small enough to understand end to end.

---

## 12. Failure modes to watch for

### Generated-code editing

If a feature fixes architecture by editing generated Python directly, it is almost certainly violating the model.

### UI inference replacing compiler evidence

Do not reconstruct compiler state from timestamps, Git diffs, or file existence when the compiler can state it directly.

### Shadow implementations

Preview, export, CLI, UI, education, and packaging layers must not quietly reimplement capability logic.

### Filesystem discovery becoming architecture

A capability should eventually exist because canonical/registry state declares it, not because a Python file happens to be in a directory.

### Abstraction ahead of pressure

The project produced its best progress when abstractions were introduced only after a small proof exposed the need.

### Prototype accumulation

Do not return to producing many disconnected demonstration repositories. Extend the permanent vertical slice.

### Treating text utilities as the product

`inspect_text` and `normalize_text` are intentionally boring. Their purpose is to make architectural consequences obvious.

### Treating Git as the entire product history model

Git is repository history. Pyxis revision provenance has different product semantics and should remain explicit.

### Claiming verification that did not run

Preserve the distinction between designed tests and executed tests.

### Collapsing build and install evidence

A verified wheel that installs offline does not imply the source repository can build a wheel offline. Keep those facts distinct even though D081 does not require the latter.

### Solving a non-requirement

Do not add a custom backend, vendor toolchain dependencies, or weaken conventional build behavior solely because 9M reproduced an offline source-build failure. A characterized limitation is not automatically a product defect.

---

## 13. A useful test for every new feature

Before adding something, ask:

1. What canonical intent does this represent?
2. Does it need to exist in the RIR?
3. Which compiler product changes because of it?
4. Can the consequence be predicted before mutation?
5. What provenance explains why it changed?
6. Does runtime consume generated implementation rather than a shadow path?
7. Can export preserve the exact compiler result?
8. Can a user inspect enough of this transformation to learn from it?
9. Can we measure whether the implementation wastes work?
10. Is this feature required by the current vertical slice, or are we expanding too early?
11. If portability is involved, which exact boundary is being claimed: source build, portable source, verified wheel, wheel installation, or installed execution?
12. Is a proposed workaround solving a demonstrated product requirement or merely removing an observed constraint?

If those answers are unclear, the feature is probably ahead of the architecture.

---

## 14. Handoff guidance for a future development session

A future session should not begin by asking, “What should Pyxis be?”

That question has been explored enough for the minimum slice.

Begin instead with:

> What is the next smallest implementation that makes the permanent `WorkspaceSpec → RIR → compiler → materializer → runtime → verified export` path more usable while preserving its boundaries?

Read the current code before modifying it.

Continue in small commits.

Do not bulk-import the old prototype repositories.

Migrate only behavior whose architectural value is still understood.

When a prototype lesson and current code disagree, reproduce the contradiction with a test before redesigning architecture.

For packaging, Milestone 9 is closed. The portable contract is conventional source plus a verified wheel, and the offline guarantee applies to installing/executing that wheel. Do not reopen offline source-build machinery unless a new real requirement explicitly demands it.

The next major work should therefore move into Milestone 10: make the existing permanent Workspace lifecycle visible and usable through a local UI without creating a shadow product path.

---

## 15. Current continuity sentence

At the 2026-08-12 Milestone 9N closure, Pyxis has a permanent evidence-bearing path from canonical Workspace intent through RIR, deterministic/incremental compiler products, read-only runtime, append-only revisions, exact-byte verified export, conventional package projection, independent package execution, standard wheel construction, and fresh network-disabled installation/execution of the verified wheel with matching behavior. The portable deliverable is now explicitly **conventional source repository + verified wheel**. The stronger offline raw-source rebuild condition was tested, failed at ordinary Setuptools dependency resolution, and intentionally excluded from the Repository Zero acceptance contract. Milestone 9 is closed; the foreseeable next major step is the first local Workspace UI built strictly on the existing application boundaries.
