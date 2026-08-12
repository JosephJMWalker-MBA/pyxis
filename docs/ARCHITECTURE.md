# Pyxis Architecture

## Product thesis

Pyxis turns human architectural intent into executable, inspectable systems through a transparent compiler path.

The minimum proven path is:

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

Changes flow through the same path:

```text
preview proposed canonical state
    ↓
show predicted artifact/runtime consequences
    ↓
record rationale
    ↓
append revision
    ↓
write canonical state
    ↓
compile
    ↓
run changed Workspace
```

## Architectural boundaries

### Canonical state

Canonical authoring data is the authoritative expression of intended architecture.

### RIR

The Repository Intermediate Representation is the normalized compiler input derived from canonical state. It makes architectural relationships inspectable before code generation.

### Generated implementation

Generated files are compiler products. UI actions and export logic must not patch generated implementation directly.

### Revisions

Architectural changes are append-only events carrying human rationale, before/after canonical hashes, and compiler completion evidence.

### Export

Export is packaging, not compilation. It packages existing compiler products and verifies their identity and runtime behavior.

Portable packaging keeps two forms deliberately distinct:

- `generated/` remains the original compiler-product/evidence surface.
- the conventional `src/` package layout is an exact-byte projection of those compiler products plus packaging-only support files.

The current Repository Zero portability proof establishes:

```text
exact compiler products
      ↓
verified portable export
      ↓
conventional src/ projection
      ↓
standalone package runtime without Pyxis
      ↓
standard wheel built with ordinary PEP 517 tooling
      ↓
wheel payload identity verification
      ↓
fresh network-disabled wheel installation
      ↓
installed console execution with matching behavior
```

These proofs must not be collapsed into a stronger claim than the evidence supports:

- **source package → conventional wheel is proven** using ordinary PEP 517 build isolation.
- **verified wheel → fresh offline install → execution is proven** with network access actively blocked.
- **offline source package → wheel construction remains unproven.**

A successful offline wheel installation does not prove that build dependencies for source-to-wheel construction are available offline. Repository Zero should not introduce a bespoke local build backend unless a later explicit decision concludes that the stronger offline source-build proof is required.

## Minimum permanent demonstrator

`examples/text_lab/` should remain the executable architectural specification for the first vertical slice.

Its two initial capabilities are deliberately simple:

- `inspect_text`
- `normalize_text`

They exist to prove the compiler and revision model, not because text utilities are the long-term product domain.

## Deferred concerns

The following remain important but should not expand Repository Zero until the vertical slice is stable:

- browser integration
- broader capability catalog
- provider-neutral AI services
- timing and waste instrumentation
- security permission models
- educational overlays beyond compiler inspection
- deployment integrations
