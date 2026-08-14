# Milestone 12A

D116: a second concrete architectural operation may add `split_lines` through the same preview → rationale → append-only revision → compiler/materializer → runtime → fresh-presentation path without first introducing a generalized architecture-operation model.

`split_lines` is not part of default canonical intent. Its deterministic compiler product exists only when canonical/RIR capability structure explicitly includes it. Preview exposes only consequences justified by that proposed structure: addition of the `split_lines` capability, `generated/capabilities/split_lines.py`, regeneration of the composed Workspace entrypoint, and addition of the `split_lines` runtime key.

Apply consumes the exact retained split-lines preview, requires human rationale and explicit runtime input, records `add_capability:split_lines`, preserves unchanged capability products as `reused`, emits the new capability product as `new`, regenerates the composed Workspace entrypoint, runs the new Workspace, retires pre-change READY, and makes pre-change measurement presentation incoherent by exact RIR identity. The live shell removes that stale measurement snapshot through the already-proven provenance/invalidation rule; it performs no measurement acquisition or re-projection.

The duplicated concrete preview/apply/controller/UI seams are intentional evidence. 12A does not convert them into a generic operation registry, schema, command object, or dynamic editor. Generalization must be justified by comparing the two now-proven concrete operations rather than predicted in advance.

Proof: Actions #373 passed on `d8b6f0ebe9cbb97960b026efc61b4a7b602ca94e`; all 206 Repository Zero tests passed, including application-level add/preview/apply provenance tests and a visible Textual Preview → rationale → Apply → measurement-invalidation acceptance path.

Next: compare the proven `remove_normalize_text` and `add_split_lines` paths. Extract only duplication that is genuinely operation-independent; retain concrete semantics where the two edits differ.
