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

D081 defines the permanent Repository Zero interpretation of this requirement: the offline guarantee applies to the verified wheel included with the portable deliverable, not to rebuilding that wheel from source while offline.

## D079 — Separate source-build and wheel-install portability proofs
Repository Zero must treat source-to-wheel construction and wheel installation as separate evidence boundaries.

The permanent proof establishes that a conventional source package can build a standard wheel using ordinary PEP 517 tooling when its build dependencies are obtainable, and that a verified prebuilt wheel can then be installed and executed in a fresh environment with network access blocked and without Pyxis participating.

Milestone 9M separately tested the stronger source-build condition without altering the package shape: normal PEP 517 build isolation was preserved, network/index access was disabled, no build dependencies were vendored or injected, and no fallback backend was provided. Under those conditions the current source package fails before wheel construction because the isolated build environment cannot resolve its declared `setuptools>=77.0.3` requirement.

The successful offline wheel-install proof therefore remains distinct from the reproduced offline source-build failure.

## D080 — Reproduce a portability constraint before choosing its remedy
The 9M failure establishes that the stronger interpretation of D078—raw exported source must construct its wheel with no network or externally available build dependency—is **not satisfied by the current conventional package**.

That evidence does not select a solution. Repository Zero must not reintroduce the prototype's local build backend, vendor Setuptools, disable normal build isolation, or otherwise change packaging merely to make the test green. First decide whether offline source-to-wheel construction is actually a required product property. Only then should a remedy be evaluated against the existing constraints: exact compiler-product identity, conventional portable shape where possible, and export remaining packaging rather than compilation.

## D081 — Portable deliverable is conventional source plus a verified wheel
Repository Zero resolves the D078 scope question in favor of the smallest proven product contract.

A portable Pyxis Workspace consists of:

- the conventional source repository containing the exact compiler products and inspectable provenance evidence; and
- a verified wheel built from that source projection whose compiler-product payload identity has been checked against the same evidence.

The portability guarantee is that the **verified wheel can be installed and executed in a fresh environment without network access, external build dependencies, or Pyxis participation while preserving the proven Workspace behavior**.

Rebuilding the wheel from raw source while offline is not a Repository Zero product requirement. Conventional source builds may use ordinary PEP 517 build isolation and may require their declared build dependencies to be obtainable.

The Milestone 9M offline source-build failure remains valuable characterization evidence, but it is an accepted limitation of the source form under this contract rather than a defect requiring a bespoke backend. Repository Zero will not vendor build tooling, weaken normal build isolation, or reintroduce the prototype local backend solely to eliminate that limitation.

This decision closes the Milestone 9 packaging requirement. Future packaging work must be driven by a new demonstrated product need rather than by the stronger D078 interpretation that D081 has now explicitly declined.

## D082 — Workspace presentation is an application-owned evidence adapter
A user interface must consume a read-only Workspace presentation contract assembled from evidence Pyxis already owns. The presentation layer may validate that supplied evidence belongs to the same Workspace, but it may not load or scan repository files, compile, execute runtime code, export, infer compiler status, or synthesize readiness.

Canonical identity must come from authoritative `WorkspaceSpec`, not copied RIR fields. RIR identity and compiler artifact status come from existing build/manifest evidence. Runtime output comes from an existing run result. Revision presentation preserves append-only event intent separately from optional compiler completion evidence. Export presentation exists only when actual `READY` verification evidence is supplied.

The presentation contract itself must remain read-only. Runtime mappings/sequences are recursively exposed as immutable values so a UI cannot mutate application evidence through the view model. A `removed` artifact status must not invent current hashes that no longer exist in the current generation manifest.

This boundary is framework-independent. A future UI renders the contract; it does not become a second query, compiler, runtime, revision, or verification implementation.

## D083 — Existing Workspace queries separate durable and transient evidence
An application query for an existing Workspace may reload only evidence that has an owning persistence boundary: canonical `WorkspaceSpec`, persisted RIR, generation manifest, and append-only revision event/completion history.

Runtime output and generation statuses remain transient evidence. The existence of generated files, a manifest, or an RIR does not permit the query layer to recreate `BuildAndRunResult`, infer `new`/`reused`/`regenerated`/`removed`, or execute the Workspace automatically. A caller must supply the current `BuildAndRunResult`, and it must agree with the persisted RIR and generation manifest before presentation is assembled.

Export readiness is transient verification evidence under the current Repository Zero model. A portable directory on disk does not imply `READY`. Export presentation may be included only when the actual `WorkspaceExportResult` is supplied, refers to the queried source Workspace, and remains coherent with its verified export root.

Revision history is durable evidence and therefore gains typed read-only loaders owned by the revisions persistence layer. The application query consumes those loaders rather than parsing JSONL itself.

This decision keeps reopening an existing Workspace honest: durable facts can be recovered after process loss; transient facts must be rerun or explicitly retained rather than reconstructed heuristically.

## Repository Zero rule

New implementation work should extend the permanent vertical slice rather than create another disposable proof repository.
