# Pyxis Decision Record

This document captures the implementation decisions proven during prototyping and carried into Repository Zero.

## D063 — Preview-first historical reapply
Historical canonical state is never applied directly. Reapplication previews architectural consequences and creates a new revision.

## D064 — Consolidate into one minimal product
A capability is not part of Pyxis until it participates in the same Workspace, compiler, runtime, and revision path.

## D065 — Independent export
Exported compiler products must run independently of the Pyxis source tree.

## D066 — Verified export
An export is READY only after provenance and runtime verification succeed.

## D067 — Visible READY state
First-run UX should end in a visible readiness state derived from verification evidence.

## D068 — Minimal Workspace creation
First-run Workspace creation begins with only a name and description.

## D069 — Created Workspaces run immediately
The first user-created Workspace must execute the generated entrypoint from its own detail screen.

## D070 — Preview architecture edits before mutation
Preview may derive proposed canonical/RIR states but may not mutate canonical or generated files.

## D071 — Rationale belongs in provenance
Architectural changes require human rationale before compilation and append a revision event.

## D072 — Restore is not rollback
Restoration creates a new intent-bearing revision through the same compiler path; history remains immutable.

## D073 — Preview observable runtime contract
Pyxis may predict runtime capability surfaces that follow directly from canonical structure, without simulating implementation behavior.

## D074 — Consolidate before expanding
Proof-specific surfaces should be removed in favor of one coherent first-run product path.

## D075 — Export is packaging, not compilation
Export packages exact compiler products and must not reinterpret or regenerate implementation.

## D076 — Export belongs in the Workspace journey
A user should reach verified portable output from the same first-run Workspace experience.

## D077 — Conventional package shape
Portable output should resemble a normal Python repository rather than a special Pyxis-only artifact.

## D078 — Self-contained portability proof
The minimum exported repository can be installed and executed without network access or external build dependencies while preserving generated artifact identity.

## Repository Zero rule

New implementation work should extend the permanent vertical slice rather than create another disposable proof repository.
