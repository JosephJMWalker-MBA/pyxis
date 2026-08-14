# Pyxis

Pyxis turns software architecture into executable, inspectable systems—connecting human intent to generated code through a transparent compiler, with measurable consequences and portable output.

## Current focus

Repository Zero now has a permanent evidence-bearing vertical slice:

```text
Create Workspace
      ↓
Canonical authoring state
      ↓
RIR
      ↓
Compiler
      ↓
Generated Workspace
      ↓
Run
      ↓
Preview architectural change
      ↓
Trace proposed architectural consequences
      ↓
Record rationale + append-only revision
      ↓
Incremental recompilation
      ↓
Export exact compiler products
      ↓
Verify provenance + runtime behavior
      ↓
Conventional portable source repository
      ↓
Verified wheel
      ↓
Fresh offline installation + execution
```

The first local Textual Workspace UI consumes those application boundaries rather than recreating them. Repository Zero also has a descriptive measurement path over the established build/run operation, with exact subject/workload/environment/work provenance, read-only summary presentation, and live Workspace/RIR provenance rules through Milestone 11T. Two concrete architecture operations now prove both additive and subtractive governed edits, with only demonstrated invariant orchestration shared privately. Milestone 13A adds a preview-only architecture consequence trace that connects requested change → proposed canonical state → proposed RIR → compiler-product consequences → runtime-contract consequences using only already-owned preview evidence.

The first demonstrator remains intentionally small so the entire transformation can be inspected end to end.

## Core principles

- Human intent should remain visible in the implementation path.
- Canonical source is authoritative; generated files are compiler products.
- Architectural changes are previewed before mutation.
- Revisions are append-only and carry rationale.
- Incremental generation is based on compiler evidence, not filesystem inference.
- Export packages existing compiler output rather than regenerating it.
- READY is derived from verification evidence.
- Presentation and UI render application-owned evidence rather than rediscovering product state.
- Measurement observes established operations and remains descriptive rather than causal.
- Portable output should look like a conventional Python repository.
- The smallest demonstrator should remain understandable end to end.
- Pyxis should leave users better Python programmers by making the transformation from architecture to code inspectable.

## Portable output

Repository Zero defines one portable deliverable with two complementary forms:

```text
conventional source repository + verified wheel
```

The source repository preserves the exact compiler products, provenance evidence, and conventional Python package structure. The verified wheel is checked against that source/manifest evidence and is the artifact covered by Pyxis's offline portability guarantee.

The verified wheel has been proven to install and execute in a fresh environment with network access blocked, without Pyxis participating, while reproducing the already-verified Workspace behavior.

Raw source-to-wheel construction remains conventional PEP 517 packaging and may require declared build dependencies to be obtainable. Pyxis does not require the raw source repository to rebuild its wheel while offline.

## Repository Zero

The permanent implementation is organized around explicit boundaries under `src/pyxis/`, including:

```text
src/pyxis/
├── authoring/
├── rir/
├── compiler/
├── runtime/
├── revisions/
├── exporting/
└── app/
```

The permanent reference example is `examples/text_lab/`.

## Project continuity

Start with [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) for the current Repository Zero map through Milestone 13A / D118.

The repository also keeps three complementary detailed records so future development does not depend on chat history:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — architectural boundaries and detailed evolution
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — normative implementation decisions
- [`docs/DEVELOPMENT_ARCHIVE.md`](docs/DEVELOPMENT_ARCHIVE.md) — development history, learned logic, prototype lessons, current gaps, and foreseeable implementation path

Later milestone documents remain the narrow proof trail for changes not safely foldable into the large central files through the current GitHub connector.

## Status

Repository Zero is proven through Milestone 13A / D118: the compiler/runtime/revision/export lifecycle, interactive evidence UI, descriptive measurement pipeline, live measurement provenance/invalidation/re-entry path, two concrete governed architecture operations, shared private architecture orchestration, and preview-only architecture consequence trace all remain inside the permanent vertical slice.

Do not add another statistic, abstraction, or explanatory layer merely because the current architecture makes one possible. The next implementation milestone should answer a concrete product question; for the consequence-trace path, the next candidate is a separate proof that post-Apply actual revision/compiler/runtime evidence can be reconciled with the earlier preview without turning preview evidence into post-change authority.
