# Milestone 42B — deterministic third-epoch authority inspection

Decision: **D212**

Milestone 42B adds deterministic non-interactive authority inspection for the persisted third-epoch entry families already made visible by Milestone 42A.

It is the three-root analogue of Milestone 39B. It does not create a new lineage model, authority source, persisted handoff, or discovery mechanism.

## Product result

`pyxis research-inspect` now accepts four explicit persisted entry families:

```text
37B   --second-basis-epoch-overlay
37C/D --second-basis-epoch-continuation-overlay
40B   --third-basis-epoch-overlay
40C/D --third-basis-epoch-continuation-overlay
```

All four flags occupy one mutually-exclusive parser group.

The new third-epoch routes are:

```text
explicit persisted path
        ↓
strict locator-overlay decode
        ↓
fresh re-entry
        ↓
41A explicit path/result lineage proof
        ↓
42A UI-independent authority projection
        ↓
deterministic JSON serialization
```

No Textual shell is imported or launched by `research-inspect`.

## Stable third-epoch report format

42B introduces:

```text
pyxis.chromium.research_third_basis_epoch_authority_inspection.v1
```

The serialization layer is deliberately separate from the 42A projection implementation. It consumes one already-derived `ThirdBasisEpochAuthorityInspection` and performs no I/O or authority derivation itself.

The document contains:

```text
format
report_role

authority_notice

launch_provenance
    launch_family
    launch_location_context_only
    first_root_sha256
    second_root_sha256
    third_root_sha256
    launch_endpoint_sha256

current_governed_state
    state_kind
    state_source
    endpoint_sha256
    declared_continuation_edge_count
```

Serialization uses stable key ordering, fixed indentation, UTF-8-safe JSON, and exactly one trailing newline.

## Persisted 40B inspection

For `--third-basis-epoch-overlay`, Pyxis:

1. decodes the exact supplied 40B locator overlay;
2. freshly re-enters its complete three-root ancestry;
3. proves the explicit path/result pairing through the existing 41A shell-lineage boundary;
4. derives the same immutable-launch/current-state projection used by the 42A live product;
5. serializes that projection.

The report therefore exposes the three retained root SHA-256 identities, launch endpoint, current endpoint, and explicit launch path as location context only.

## Persisted 40C / 40D inspection

For `--third-basis-epoch-continuation-overlay`, the same flow reconstructs the persisted continuation and proves the 41A continuation path/result pairing before projection.

40C and cumulative 40D intentionally share one report family and one CLI flag because they already share the same typed continuation re-entry family.

The current-state section includes the declared continuation edge count represented by the freshly reconstructed typed plan.

## Raw 41E handoff remains excluded

42A can visibly inspect an exact in-process 41E handoff because the typed re-entry object already exists in memory.

42B does **not** add a CLI representation for that authority family.

A raw 41E handoff has no persistent launch path. Adding a report flag for it would require either inventing a persistent locator or serializing a different authority object, neither of which is earned by this milestone.

So the durable and in-process families remain distinct:

```text
persisted 40C/40D path
→ fresh re-entry
→ 41A path/result proof
→ deterministic report
```

versus:

```text
exact in-process 41E typed re-entry
→ live 42A inspection only
```

## Path and hash semantics

A displayed path remains **launch location context only**. It is not identity and does not mean current, latest, or head.

SHA-256 values remain integrity / record-identity anchors only. They do not establish:

- authorship;
- authenticity;
- trusted time;
- chronology;
- branch authority;
- semantic support;
- citation authority.

The serialized report is not evidence and is not a control-plane object.

## Prior art reused

Milestone 39B / PR #116 is the direct internal precedent.

42B reuses its key product rules:

- explicit persisted input only;
- strict fresh reconstruction before reporting;
- path/result proof before projection;
- shared application projection rather than CLI-side root derivation;
- deterministic JSON plus newline;
- no UI dependency;
- no implicit discovery or handoff serialization.

No end-to-end substitute search was required beyond this repository precedent because 42B extends an existing Pyxis-specific authority/reporting protocol rather than introducing a new commodity subsystem.

## Tests

42B proves:

- persisted 40B serializes deterministically across repeated calls;
- the report contains first-, second-, and third-root identities;
- launch and current endpoint identities are explicit and separate;
- persisted 40C serializes its typed continuation edge count;
- cumulative 40D uses the same continuation report family;
- serializer rejects non-projection input;
- CLI 40C output is byte-for-byte equal to direct serialization of the shared freshly proven 42A projection;
- malformed 40B input fails before report emission;
- third-epoch `research-inspect` works while every `pyxis.ui` / `textual` import is forbidden;
- all four persisted inspection flags remain mutually exclusive;
- no raw handoff, latest, head, directory, automatic selection, format detection, or format-selection flag is exposed.

## Deliberate non-goals

42B does not add:

- persisted 41E handoff serialization;
- fourth evidence-basis epoch support;
- generic or arbitrary-depth `epoch[n]` ancestry;
- latest/current/head selection;
- directory scanning or predecessor discovery;
- format guessing or auto-detection;
- chronology or branch authority;
- path identity;
- authorship, authenticity, or trusted time;
- semantic-support or citation authority;
- mutation, checkpoint, restart, browser, or persistence authority.

## Acceptance statement

Milestone 42B is accepted when one explicitly supplied persisted 40B or 40C/40D overlay can be freshly reconstructed, explicitly path/result-proven through existing 41A semantics, projected through the same UI-independent authority model used by 42A, and emitted as stable deterministic JSON without importing Textual or expanding authority beyond the supplied persisted entry.
