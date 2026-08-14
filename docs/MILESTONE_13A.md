# Milestone 13A — Architecture Consequence Trace

**Decision D118 — one proposed architecture edit may expose a read-only, stage-ordered consequence trace assembled only from preview evidence Pyxis already owns.**

## Product question

Can Pyxis let a user follow one proposed architectural decision from requested change through canonical state, RIR, compiler products, and runtime contract without asking the user to mentally stitch those evidence surfaces together?

## Proven shape

`ArchitecturePreviewPresentation` now carries an immutable tuple of exact trace steps. Each step contains only:

- stage,
- action,
- subject kind,
- subject.

The stage order is:

```text
requested architecture change
    ↓
proposed canonical state
    ↓
proposed RIR
    ↓
compiler products
    ↓
runtime contract
```

For the 13A visible proof, adding `split_lines` renders:

```text
add capability: split_lines
    ↓
add capability: split_lines to proposed canonical state
    ↓
add capability: split_lines to proposed RIR
    ↓
add generated/capabilities/split_lines.py
change generated/workspaces/text_lab/main.py
    ↓
add runtime key: split_lines
```

The trace is rendered inside the existing architecture-preview evidence panel and remains explicitly labeled **PROPOSED — NOT APPLIED**.

## Evidence boundary

The trace does not compile, run, persist, mutate canonical state, append a revision, refresh export evidence, acquire measurements, or infer filesystem state.

It projects only facts already validated by the existing architecture preview:

- added/removed capabilities,
- proposed canonical capability state,
- proposed RIR capability state,
- added/changed/removed compiler-product paths,
- added/removed runtime keys.

No AI explanation, causal claim, score, recommendation, semantic impact label, or generated narrative is introduced.

## UI proof

The first visible acceptance proof uses `split_lines` only. Before and after Preview:

- the live `WorkspaceController` run remains the same object,
- existing READY evidence remains current,
- current canonical/RIR/compiler/runtime/revision/export rendering is unchanged,
- source and portable filesystem snapshots are unchanged,
- compiler execution is blocked by the test and never invoked.

The application presentation also produces the same typed trace shape for `normalize_text` removal, proving the trace projection is not tied to addition semantics.

## Validation

Actions #392 passed on implementation head `f8b75582176811d968335e001280942d59ad024e` with all **209 Repository Zero tests passing**.

## Deliberate non-goals

13A does not add:

- post-Apply consequence reconciliation,
- revision-to-preview trace linking,
- actual-vs-predicted comparison,
- generated-source explanation,
- AI interpretation,
- causal attribution beyond the preview's owned structural facts,
- a generic architecture-operation registry or DSL,
- new compiler, runtime, revision, persistence, export, or measurement semantics.

## Next pressure

The next consequence-trace question, if product use justifies it, is whether the same preview trace can be reconciled after Apply with the actual revision/compiler/runtime evidence Pyxis already records. That should be a separate proof rather than silently expanding a preview presentation into post-change authority.
