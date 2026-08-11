# Pyxis

Pyxis turns software architecture into executable, inspectable systems—connecting human intent to generated code through a transparent compiler, with measurable consequences and portable output.

## Current focus

Pyxis is moving from architectural proof into a real reference implementation. The first vertical slice is intentionally small:

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
Record rationale + revision
      ↓
Recompile
      ↓
Export exact compiler products
      ↓
Verify portable output
```

## Core principles

- Human intent should remain visible in the implementation path.
- Canonical source is authoritative; generated files are compiler products.
- Architectural changes are previewed before mutation.
- Revisions are append-only and carry rationale.
- Export packages existing compiler output rather than regenerating it.
- The smallest demonstrator should be understandable end to end.
- Pyxis should leave users better Python programmers by making the transformation from architecture to code inspectable.

## Repository Zero

The initial repository target is the proven vertical slice rather than the full long-term platform. Early modules will center on:

```text
src/pyxis/
├── authoring/
├── rir/
├── compiler/
├── runtime/
├── revisions/
├── export/
└── app/
```

The permanent reference example will be `examples/text_lab/`.

## Project continuity

The repository keeps three complementary records so future development does not depend on chat history:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — current architectural boundaries
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — compact normative decision record
- [`docs/DEVELOPMENT_ARCHIVE.md`](docs/DEVELOPMENT_ARCHIVE.md) — development history, learned logic, prototype lessons, current gaps, and foreseeable implementation path

## Status

Architecture proof complete for the minimum slice. Repository construction is now underway through the permanent `WorkspaceSpec → RIR → compiler → materializer → runtime` path.
