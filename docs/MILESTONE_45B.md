# Milestone 45B — deterministic one-root authority inspection report

Decision: **D227**

## Question

45A / D226 made already-earned one-root root-backed authority visibly inspectable across persisted and exact in-process product entry families while preserving:

```text
immutable launch provenance
!=
mutable current governed state
```

The remaining parity gap is non-interactive inspection. Persisted second- and third-epoch entry families already support deterministic `pyxis research-inspect` reports, while persisted one-root 35C and 35D/35E launches did not.

45B asks whether Pyxis can emit the exact same already-proven one-root authority projection outside Textual without inventing a durable representation for raw 44H/36D handoffs and without turning report output into authority.

## Decision D227

Add deterministic persisted-only one-root authority inspection using the exact 45A application projection and path/result proof wrappers.

The product rule is:

```text
live 45A projection derivation
==
non-interactive 45B projection derivation
```

while:

```text
inspection report
!= evidence
!= control-plane authority
```

## Reused boundaries

45B introduces no new lineage, persistence, restart, checkpoint, browser, or research subsystem.

Direct internal precedent is decisive:

- 39B / D201 — deterministic second-epoch inspection over the same application projection used by the live product;
- 42B / D212 — deterministic third-epoch parity with a separate serializer consuming an already-derived projection;
- 45A / D226 — concrete one-root persisted launch-lineage proof plus UI-independent authority projection.

45B therefore follows the 42B shape: one separate deterministic serializer over an already-derived 45A projection.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Persisted entry families

`pyxis research-inspect` gains exactly two additional mutually exclusive persisted entry flags:

```text
--root-backed-overlay <path>
--root-backed-continuation-overlay <path>
```

Persisted 35C follows:

```text
explicit path
→ strict 35C overlay decode
→ fresh root-backed re-entry
→ 45A explicit path/result proof
→ 45A shared authority projection
→ deterministic JSON serialization
```

Persisted 35D/35E follows:

```text
explicit continuation path
→ strict continuation overlay decode
→ fresh continuation re-entry
→ 45A continuation path/result proof
→ 45A shared authority projection
→ deterministic JSON serialization
```

No CLI-side root, endpoint, or provenance derivation is introduced.

## Raw handoffs remain live-only

45B deliberately exposes no report flag for:

- raw in-process 44H root-backed handoff;
- raw in-process 36D continuation handoff.

Those authority families exist only as exact typed in-memory results and deliberately have no persistent launch path. 45B does not serialize those objects, infer a checkpoint destination, or backfill a prior 44G/35D path merely to make them reportable.

## Stable report format

45B adds:

```text
pyxis.chromium.research_root_backed_session_authority_inspection.v1
```

The deterministic document contains:

```text
format
report_role

authority_notice

launch_provenance
    launch_family
    launch_location_context_only
    root_sha256
    launch_endpoint_sha256

current_governed_state
    state_kind
    state_source
    endpoint_sha256
    declared_continuation_edge_count
```

Serialization uses:

- stable field names;
- sorted JSON keys;
- fixed indentation;
- UTF-8-safe text;
- exactly one trailing newline.

The serializer performs no file I/O, path proof, re-entry, discovery, mutation, checkpointing, restart, browser access, or authority derivation.

## Path and hash semantics

A displayed path is launch-location context only. It is not identity and does not mean current, latest, or head.

Path-distinct but durably equivalent explicitly supplied launch configurations may therefore produce matching durable identities while differing in `launch_location_context_only`.

SHA-256 values remain integrity / durable-record identity anchors only. They do not establish authorship, authenticity, trusted time, chronology, branch authority, semantic support, or citation authority.

## Negative authority discipline

The report explicitly remains:

```text
read_only_inspection_not_authority
```

It does not establish:

- evidence status;
- mutation or control-plane authority;
- checkpoint or restart authority;
- browser authority;
- discovery or automatic selection;
- current/latest/head authority;
- chronology or branch authority;
- path identity;
- authorship, authenticity, or trusted time;
- semantic-support or citation authority.

## Regression rules

45B requires focused coverage proving:

- persisted 35C serializes deterministically from the shared 45A projection;
- exact proved launch path, root SHA, launch endpoint, and current endpoint are emitted;
- persisted 35D exposes the exact typed continuation-edge count;
- cumulative 35E uses the same existing continuation flag and report family;
- repeated serialization is byte-for-byte identical;
- path-distinct but durably equivalent explicit 35C launches may differ only in launch-location context;
- serializer rejects non-projection input;
- CLI continuation output is byte-for-byte equal to direct serialization of the same freshly proven 45A projection;
- malformed one-root persisted input fails before report emission;
- one-root `research-inspect` succeeds while every `pyxis.ui` / `textual` import is actively forbidden;
- all six persisted `research-inspect` flags remain mutually exclusive;
- existing second- and third-epoch report routes remain unchanged;
- no raw handoff, latest, head, directory, auto-detection, or format-selection flag is exposed.

## Non-goals

45B does not add:

- durable serialization of raw 44H or 36D handoffs;
- a new checkpoint, restart, or persistence API;
- second changed-basis productization;
- a fourth evidence-basis epoch;
- generic `epoch[n]` or arbitrary-depth ancestry;
- a generic authority-report schema across all epoch families;
- discovery or path prefill;
- latest/current/head selection;
- chronology or branch authority;
- path identity;
- authorship/authenticity/trusted-time authority;
- semantic-support/citation authority;
- browser reacquisition;
- autonomous research behavior.

## Acceptance statement

If executed tests pass, 45B permits only this statement:

> An explicitly supplied persisted 35C or 35D/35E one-root launch can be freshly reconstructed, path/result-proven through existing 45A semantics, projected through the same UI-independent authority model used by the live product, and emitted as stable deterministic JSON without importing Textual or expanding authority beyond the supplied persisted entry.
