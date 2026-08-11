# Pyxis Development Archive

**Continuity snapshot — 2026-08-11**

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

---

## 5. Prototype decision sequence that led here

The numbered prototype decisions capture the narrowing process.

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

The prototype successfully demonstrated clean, network-disabled installation while preserving generated artifact identity.

`DECISIONS.md` remains the compact normative record; this archive records why those decisions emerged.

---

## 6. Transition to Repository Zero

After D078, the architecture had survived a sufficiently strong chain:

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

The permanent repository has been populated incrementally rather than through one bulk import of prototype code.

That was intentional. Prototype code proved ideas; Repository Zero should contain only the implementation that still deserves to exist.

### 7.1 Authoring

`src/pyxis/authoring/workspace.py`

`WorkspaceSpec` is a frozen canonical intent object created from the minimum first-run inputs:

- name
- description

It derives a stable Workspace ID and currently references the two demonstrator capabilities.

Boundary: no compiler or runtime behavior belongs here.

### 7.2 RIR

`src/pyxis/rir/model.py`

`WorkspaceSpec` deterministically lowers into `RepositoryIR` / `WorkspaceIR`.

Boundary: RIR is derived compiler-facing structure. It does not contain generated source or execute behavior.

### 7.3 Compiler artifact generation

`src/pyxis/compiler/artifacts.py`

The compiler currently emits deterministic artifacts for:

- `generated/capabilities/inspect_text.py`
- `generated/capabilities/normalize_text.py`
- `generated/workspaces/<workspace_id>/main.py`

Each artifact carries a deterministic node SHA-256 identity.

### 7.4 Repository compiler

`src/pyxis/compiler/repository.py`

`compile_repository(repository)` converts one RIR into one ordered immutable artifact tuple.

Unknown capabilities fail explicitly.

Boundary: compilation remains pure and performs no filesystem writes.

### 7.5 Materialization

`src/pyxis/compiler/materialize.py`

`materialize_artifacts(artifacts, destination_root)` is the first filesystem boundary.

It writes only already-compiled artifact source to already-declared relative paths and rejects path escapes.

Boundary: materialization does not compile, inspect canonical state, or execute generated code.

### 7.6 Runtime

`src/pyxis/runtime/loader.py`

`run_materialized_workspace(repository, repository_root, text)` locates the generated Workspace entrypoint from the RIR and executes it.

Boundary: runtime does not compile or write.

### 7.7 Application orchestration

`src/pyxis/app/build.py`

`build_workspace(spec, destination_root)` composes:

```text
build_repository_ir
      ↓
compile_repository
      ↓
materialize_artifacts
```

It returns a frozen `BuildResult` containing the RIR, generated artifacts, and written paths.

`build_and_run_workspace(spec, destination_root, text)` then composes:

```text
build_workspace
      ↓
run_materialized_workspace
```

This is the current complete permanent vertical slice.

---

## 8. Proof status: an important distinction

Two different kinds of evidence exist and should not be conflated.

### Prototype proofs

The pre-Repository-Zero prototypes were actually executed during development. Their smoke tests and targeted tests were used to discover several of the lessons above, including incremental waste, revision behavior, portability, and clean installation.

### Current GitHub Repository Zero

The permanent repository has been authored through the GitHub connector in small commits. Tests have been written to specify the intended boundaries, but this connector session does not execute the repository test suite.

Therefore:

> Do not claim the current Repository Zero suite is passing until it has been run in a real checkout or CI environment.

One of the earliest next actions should be to establish that executable verification.

---

## 9. Known gaps in the permanent implementation

The current vertical slice executes, conceptually, through all permanent layers, but several pieces proven in prototypes have not yet been migrated.

### 9.1 Canonical authoring is not yet persisted as a repository artifact

`WorkspaceSpec` currently exists as an in-memory canonical object during the build path.

The first real user-created Workspace should persist its authoritative authoring state, likely under a path similar to:

```text
authoring/canonical/workspace.json
```

The exact format should remain small and deterministic.

### 9.2 RIR is not yet serialized into the generated repository

Inspectability improves substantially when the normalized compiler input can be examined alongside generated code.

A permanent form similar to:

```text
generated/repository.rir.json
```

should be restored from the prototype architecture.

### 9.3 Generation manifest / artifact integrity is not yet permanent

The prototypes proved semantic fingerprints, artifact hashes, and incremental status. Repository Zero has node hashes but not yet the full manifest/reconciliation layer.

### 9.4 Revision history has not yet been migrated

Append-only rationale-bearing revision events, canonical snapshots, preview-first change, restore, and reapply remain proven prototype behavior but are not yet in the permanent code.

### 9.5 Export has not yet been migrated

The export architecture is well proven, but Repository Zero should reintroduce it only after the permanent build path, serialization, manifest, and tests are stable.

### 9.6 User-facing first-run command is not yet connected

The next interface should call the existing orchestration rather than creating a second implementation path.

### 9.7 `examples/text_lab/` has not yet become the permanent executable specification

The example should eventually be committed as the smallest repository whose expected canonical state, RIR, generated artifacts, runtime behavior, and later revision behavior can be inspected end to end.

---

## 10. Foreseeable implementation path

The order matters. The purpose is to keep proving the same architecture under increasing product realism, not to add breadth prematurely.

### Milestone 1 — Verify Repository Zero in an executable environment

Run the full current test suite in a checkout or CI.

Fix real integration errors before adding architecture.

Do not infer correctness from the fact that individual files look coherent.

### Milestone 2 — Persist the first Workspace's canonical state

Make first-run creation produce a real Workspace directory with authoritative authoring data.

Target conceptual shape:

```text
<workspace>/
├── authoring/
│   └── canonical/
│       └── workspace.json
└── generated/
```

Keep name + description as the first-run inputs.

### Milestone 3 — Persist RIR and a minimal generation manifest

The compiler path should leave inspectable evidence of what it consumed and what it produced.

Initial manifest concerns:

- RIR hash
- artifact path
- node fingerprint
- artifact hash

Do not add incremental optimization until this evidence exists cleanly.

### Milestone 4 — Connect the first real CLI

The CLI should remain a thin interface over application orchestration.

A first useful command should be able to:

```text
name + description + destination + sample text
      ↓
create canonical Workspace
      ↓
build
      ↓
run
      ↓
show observable result
```

The CLI must not contain compiler behavior.

### Milestone 5 — Commit `examples/text_lab/`

Turn the demonstrator into a permanent executable architectural specification rather than another disposable fixture.

A change to Pyxis that breaks the reference path should be immediately visible.

### Milestone 6 — Restore preview-first architectural editing

Begin with one edit only: remove `normalize_text`.

The permanent flow should reproduce the successful prototype:

```text
current canonical state
      ↓
derive proposed state in memory
      ↓
show capability + artifact consequences
      ↓
no mutation yet
```

### Milestone 7 — Restore rationale-bearing append-only revisions

Apply should require rationale, append revision provenance, write canonical state, compile, and record completion.

Then add restore through the same path.

### Milestone 8 — Restore incremental generation

Once the manifest and revision path are stable, reintroduce node-level reuse.

Reuse requires both:

- unchanged semantic fingerprint
- unchanged artifact integrity hash

Compiler status should again become visible evidence.

### Milestone 9 — Restore export as packaging

Package the exact current compiler products into an independently runnable repository.

Verification should establish RIR/artifact identity and runtime behavior before READY.

### Milestone 10 — First local Workspace UI

Only after the CLI and permanent path are stable should the UI become the primary first-run surface.

The UI should orchestrate existing product APIs rather than absorb architecture.

### Milestone 11 — Measurement

Reintroduce time and waste accounting once there is a stable user journey worth measuring.

The Execution Ledger can then evolve from real observations rather than imagined fields.

### Milestone 12 — Browser/research capabilities

After the compiler/product spine is stable, return to the original browser/research purpose.

Chromium remains the browser. Pyxis adds inspectable Python capabilities, evidence, provenance, permissions, and workflows around it.

---

## 11. What should remain deferred

Do not let the existence of archived ideas create pressure to implement them immediately.

Until the first permanent Workspace lifecycle is solid, defer:

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

Repository Zero should stay small enough to understand end to end.

---

## 12. Failure modes to watch for

### Generated-code editing

If a feature fixes architecture by editing generated Python directly, it is almost certainly violating the model.

### UI inference replacing compiler evidence

Do not reconstruct compiler state from timestamps, Git diffs, or file existence when the compiler can state it directly.

### Shadow implementations

Preview, export, CLI, UI, and education layers must not quietly reimplement capability logic.

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

If those answers are unclear, the feature is probably ahead of the architecture.

---

## 14. Handoff guidance for a future development session

A future session should not begin by asking, “What should Pyxis be?”

That question has been explored enough for the minimum slice.

Begin instead with:

> What is the next smallest implementation that makes the permanent `WorkspaceSpec → RIR → compiler → materializer → runtime` path more real while preserving its boundaries?

Read the current code before modifying it.

Continue in small commits.

Do not bulk-import the old prototype repositories.

Migrate only the behavior whose architectural value is still understood.

When a prototype lesson and current code disagree, reproduce the contradiction with a test before redesigning the architecture.

---

## 15. Current continuity sentence

At this snapshot, Pyxis has moved from architectural proof into a permanent minimal reference implementation. The core path exists in source as distinct authoring, RIR, compiler, materialization, runtime, and orchestration layers. The immediate challenge is no longer inventing the architecture; it is making that path persist its own canonical/RIR evidence, execute under real CI, and become the first genuinely usable Workspace workflow without allowing interface convenience to collapse the boundaries that made the architecture valuable.
