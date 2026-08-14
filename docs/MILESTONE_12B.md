# Milestone 12B

D117: two proven concrete architecture operations justify private reuse of orchestration that is demonstrably operation-independent, but they do not yet justify a generic architecture-operation model.

The comparison between `remove_normalize_text` and `add_split_lines` found two exact shared application sequences:

1. Workspace preview orchestration: resolve the Workspace root, preflight current run/export evidence, load canonical state, invoke one concrete preview builder, project immutable preview evidence, and verify that canonical identity did not change during assembly.
2. Workspace Apply orchestration: require and normalize rationale, preflight current run/export evidence, verify the retained preview still names current canonical state, invoke one concrete governed Apply function, run the materialized post-change Workspace with explicit runtime input, rebuild current presentation, and intentionally omit pre-change READY evidence.

Those sequences are now represented by private helpers in `architecture_preview.py` and `architecture_apply.py`. The existing named public functions remain the only public architecture-edit application seams.

The comparison did **not** justify generalizing:

- capability-specific proposed canonical mutations or `ArchitectureDelta` facts;
- revision operation identities such as `remove_capability:normalize_text` and `add_capability:split_lines`;
- compiler capability registration or capability source generation;
- `WorkspaceController`'s named operation methods;
- Textual button IDs, copy, rationale controls, or event routing;
- an operation registry, command object/schema, dynamic editor, or architecture DSL.

The lower governed Apply layer had already reached this same boundary through `_apply_previewed_edit`: shared governance is private while concrete operation wrappers supply operation identity and preview validation. 12B extends that proven shape upward only where the second operation demonstrated exact orchestration duplication.

No new public API, canonical field, RIR field, compiler product, runtime behavior, revision semantics, UI behavior, measurement behavior, or persistence path is introduced.

Proof: Actions #380 passed on `4d75b37a03d0bb70de503ac98d78e3e747e61141`; all 206 Repository Zero tests passed.

Next: do not generalize further merely because two operations exist. The next milestone should be driven by the next concrete Pyxis product pressure; a broader architecture-operation abstraction should require additional evidence that the currently concrete controller/UI semantics are obstructing real work.
