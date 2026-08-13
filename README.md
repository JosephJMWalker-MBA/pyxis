# Pyxis

Pyxis turns software architecture into executable, inspectable systems—connecting human intent to generated code through a transparent compiler, with measurable consequences and portable output.

## Current state

Repository Zero is proven through **Milestone 11T**.

The permanent product path is:

```text
human intent
    ↓
canonical WorkspaceSpec
    ↓
Repository Intermediate Representation (RIR)
    ↓
deterministic compiler
    ↓
compiler-owned generation evidence
    ↓
materialized generated implementation
    ↓
runtime
    ↓
application-owned presentation / operations
    ↓
local Textual Workspace UI
```

Architectural changes remain governed by preview → rationale → append-only revision → canonical mutation → compiler/materializer → runtime. Export packages the exact compiler products and establishes READY only through verification evidence.

Repository Zero also has a descriptive measurement path over the established build/run operation. It preserves exact Workspace/RIR/workload/environment/work-context provenance through raw samples, count/min/max, median, mean, population standard deviation, a provenance-checked summary, read-only presentation, and optional live Workspace co-display. Measurement remains observational: it does not infer causation, efficiency, waste, cache state, warmup state, or performance quality.

Milestones 11Q–11T prove the live provenance rule: a supplied measurement snapshot may be displayed only when Repository ID, Workspace ID, and exact RIR SHA-256 match current Workspace evidence; a successful RIR-changing Apply removes the now-incoherent snapshot; the resulting notice is transient UI status rather than evidence; and an already-produced current-RIR presentation may later re-enter through the same provenance gate without renderer-owned acquisition or refresh semantics.

## Core principles

- Canonical authoring state is authoritative; generated files are compiler products.
- Human intent and architectural consequences must remain inspectable.
- Preview precedes architectural mutation.
- Human rationale belongs in append-only revision provenance.
- Incremental generation uses compiler evidence plus artifact integrity, not filesystem inference.
- Runtime does not compile; orchestration composes established layers.
- Export is packaging, not compilation, and READY is evidence-derived.
- Presentation renders owned evidence; it does not rediscover product state.
- UI actions cross named application-owned operation boundaries.
- One application-owned controller is the live transient-state authority.
- Measurement observes established operations and remains descriptive rather than causal.
- Different exact work contexts are not renamed into inferred states such as warm, cached, steady-state, or outlier.
- Repository Zero stays deliberately small until a concrete product need justifies widening a boundary.

## Repository Zero reference domain

The permanent reference Workspace remains `examples/text_lab/` with the intentionally simple `inspect_text` and `normalize_text` capabilities. They are controlled test weights for the architecture, not the long-term Pyxis product domain.

## Portable output

The portable deliverable remains:

```text
conventional source repository + verified wheel
```

The source form preserves inspectability and exact compiler-product provenance. The verified wheel is the artifact covered by the offline installation/execution guarantee. Raw source-to-wheel construction may require declared PEP 517 build dependencies to be obtainable; Repository Zero does not require rebuilding the wheel from source while offline.

## Project continuity

Start here, then read these canonical records in order:

1. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — current boundaries through 11T.
2. [`docs/DECISIONS.md`](docs/DECISIONS.md) — current normative decision record through D115.
3. [`docs/DEVELOPMENT_ARCHIVE.md`](docs/DEVELOPMENT_ARCHIVE.md) — current development continuity and historical map.

The exact pre-consolidation versions of these records remain preserved in Git history at commit `675f2b5e37b5edb32d17e9e480a4d16246826486`. Milestone documents remain the immutable narrow proof trail for the steps that produced the current architecture.

## Status

Repository Zero now has a proven compiler/runtime/export lifecycle, a proven interactive evidence UI, a descriptive measurement pipeline, and live measurement provenance/invalidation/re-entry semantics. The next work should be driven by a concrete product requirement rather than by adding statistics or generalized abstractions for their own sake.
