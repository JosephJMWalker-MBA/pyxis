# Milestone 47E — explicit third-basis epoch fresh re-entry verification

Decision: **D239**  
Issue: **#199**

## Product boundary

47D / D238 explicitly adopts one exact third-root-backed governed session in-process.

47E adds only the already-established product separation between adoption and fresh-process verification:

```text
exact successful 47D adoption
+ explicit prior 37C/37D second-epoch continuation overlay
+ explicit appended-member locators
+ explicit third changed working-set/note/transition/root/edge/declaration locators
→ existing 40A plan
→ public 40A fresh reconstruction
→ bounded three-layer identity comparison
→ locked verification receipt
```

while:

```text
47E verification
!= 40B persistence
!= controller promotion
!= launch-provenance mutation
!= automatic branch selection
!= generic Nth-epoch abstraction
```

The freshly reconstructed 40A controller is proof evidence only. The mounted 47D controller remains active.

## Why 40A is reused directly

40A / D202 already owns exactly the third-epoch reconstruction shape required here:

```text
explicit 37C/37D second-epoch continuation overlay
→ fresh second-epoch continuation reconstruction
→ explicit third-basis appended members
→ explicit third changed working set + note
→ explicit third 33B transition
→ explicit third 34A root
→ explicit third-root-started declaration
→ governed controller
```

47E therefore does not create a competing re-entry plan, persistence format, ancestry schema, or controller type. It supplies a product verification adapter around existing 40A and compares the resulting fresh authority against the exact historical 47D adoption.

40B / D203 remains a later boundary because it writes durable restart configuration only after a 40A result has already been earned.

## Prior art / reuse

Internal precedent is decisive:

- 46E / D232 establishes adoption → explicit fresh-process verification without persistence or promotion;
- 40A / D202 owns third-basis typed re-entry and concrete three-layer ancestry reconstruction;
- 40B / D203 owns later durable third-epoch restart configuration;
- 47D / D238 supplies the exact historical adoption target;
- existing second-epoch authority inspection separates immutable launch provenance from mutable current governed state.

External systems reviewed before implementation include W3C PROV, DVC, and DataLad. They provide mature provenance interchange, versioned reproducibility, and provenance-tracked dataset/workflow reconstruction, but do not demonstrate this exact product authority boundary: proving one exact in-process adopted third-basis governed session by freshly reconstructing its concrete ancestry from caller-explicit current locators while refusing path discovery, launch-provenance mutation, restart persistence, and global current/latest/head authority.

**No end-to-end substitute demonstrated in this review.**

## Exact authority subject

`verify_chromium_research_third_changed_basis_epoch_reentry(...)` requires exactly:

`ChromiumResearchThirdChangedBasisSessionAdoptionResult`

The retained prior second-epoch continuation is reached only through the exact 47D chain:

```text
47D adoption
→ 47C edge
→ 47B root
→ 47A transition
→ retained ChromiumResearchSecondBasisEpochContinuationReentryResult
```

No separately supplied in-memory controller or continuation result can replace that historical product relationship.

## Explicit locator discipline

47E requires every durable location explicitly for the current proof:

1. prior 37C/37D second-epoch continuation overlay;
2. one locator set per appended third-basis working-set member;
3. changed working-set source;
4. changed working-set-note source;
5. third 33B transition source;
6. third 34A root source;
7. first post-third-root 34B edge source;
8. third-root-backed declaration source.

Every Textual path input begins blank.

No locator is copied or inferred from:

- 47A–47D persistence receipts;
- persisted second-epoch launch provenance;
- raw 38F handoff context;
- checkpoint destinations;
- directories or filenames;
- displayed hashes;
- chronology;
- current/latest/head concepts;
- branch ranking.

A raw 38F launch may use an explicitly supplied persisted 37C/37D overlay for proof, but successful verification must not backfill that supplied path into immutable raw launch provenance.

## Three-layer verification

Public 40A freshly reconstructs the prior second-epoch continuation before reconstructing the third basis.

47E then compares the fresh result with the exact historical 47D lineage.

### Retained first-/second-root ancestry

Required equality:

- prior second-epoch continuation governed presentation;
- prior second-epoch continuation terminal edge SHA-256;
- retained first 34A root SHA-256;
- retained second 34A root SHA-256.

### Third-root layer

Required equality:

- third 34A root SHA-256;
- third-root-backed declaration SHA-256;
- first post-third-root endpoint SHA-256;
- governed adopted presentation.

Fresh Python object identity and path equality are deliberately not required. The fresh controller should be a distinct object representing the same exact bounded durable authority relationships.

## Product surface

47E adds dedicated products layered on all four 47D launch families:

- persisted second-epoch continuation launch;
- raw pathless 38F handoff;
- inspectable persisted launch;
- inspectable raw handoff.

The 47E form mounts only after one new exact successful 47D adoption.

Member-specific locator fields reuse the already-supported concrete working-set member families:

- paragraph note: capture + note;
- exact-range note: capture + note;
- comparison note: first capture + second capture + note.

Successful verification locks all locator fields and retains one exact `ChromiumResearchThirdChangedBasisEpochReentryResult`.

## Mounted-state invariants

Before invoking public 40A, the product snapshots:

- `research_controller`;
- `research_session`;
- `research_reentry`;
- retained historical `second_basis_epoch_continuation_reentry`.

Successful verification requires all four to remain object-identical.

Inspectable products additionally require:

- immutable `launch_provenance` object unchanged;
- mutable `current_state` inspection object unchanged.

For raw 38F launch families, `launch_location_context` must remain `None` before and after 47E.

## Textual event ownership

47E owns only:

`verify-research-third-changed-basis-epoch-reentry`

It does not manually call parent `on_button_pressed`. Inherited 47A–47D and earlier product actions remain Textual MRO-dispatched.

The 47E product mixin mounts its verification form only after inherited 47D promotion has completed.

## Falsification coverage

Focused tests prove:

- exact 47D result type required;
- public 40A freshly reconstructs all three distinct root layers;
- fresh controller is distinct from the mounted controller but presents the exact adopted session;
- wrong prior continuation overlay rejects;
- wrong third-root locator rejects;
- no 47E controls before exact 47D adoption;
- every 47E locator input begins blank;
- successful proof leaves mounted governed state object-identical;
- raw 38F immutable launch provenance remains object-identical and pathless;
- raw current inspection state remains object-identical;
- plain 47D products do not silently gain the 47E verification surface;
- product factories reject the wrong authority family.

Repository Zero full-suite CI on Python 3.11–3.14 remains the final executable gate.

## Non-goals

47E does **not** add:

- 40B durable third-epoch restart-overlay persistence;
- automatic relaunch;
- third-epoch checkpoint or handoff;
- fourth evidence-basis crossing;
- generic recursive epoch/ancestry representation;
- new persistence formats;
- new inspection schema;
- CLI flags;
- locator discovery or prefill;
- launch-path backfill;
- current/latest/head/chronology/branch-ranking authority;
- path identity;
- browser reacquisition;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research.

## Next boundary

If 47E is demonstrated, the next distinct question is proof-gated durable third-epoch restart configuration through existing 40B, analogous to 46F after 46E.

That remains separate from 47E. No 40B overlay is written by this milestone.
