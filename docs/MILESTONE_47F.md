# Milestone 47F — persist verified third-basis epoch restart overlay

Decision: **D240**  
Issue: **#201**

## Product boundary

47E / D239 proves that one exact historical 47D third-basis session can be freshly reconstructed through public 40A while leaving the mounted governed session unchanged.

47F adds only the already-established separation between fresh-process proof and durable restart configuration:

```text
exact successful 47E verification
+ explicit current prior 37C/37D second-epoch continuation overlay
+ explicit no-overwrite 40B destination
→ public 40B fresh three-layer proof
→ strict 40B overlay write
→ strict round-trip decode
→ locked persistence receipt
```

while:

```text
47F persistence
!= third-epoch relaunch
!= mounted-controller replacement
!= launch-provenance mutation
!= later third-epoch continuation checkpoint
!= global current/latest/head authority
```

The newly persisted overlay is operational restart configuration for the exact historical 47E proof. Persistence itself does not promote that configuration into the running shell.

## Why public 40B is reused directly

40B / D203 already owns exactly the required third-basis persistence boundary:

```text
earned 40A result
+ explicitly re-supplied current 37C/37D continuation-overlay path
+ explicit no-overwrite destination
→ candidate 40A locator plan
→ independent fresh 40A reconstruction
→ three-root authority comparison
→ strict locator-only overlay write
→ strict round-trip decode
```

47F therefore does not create another persistence format, proof grammar, ancestry container, or writer. It supplies a bounded product adapter around public 40B and retains the exact 47E verification selected by the researcher.

## Prior art / reuse

Internal precedent is decisive:

- 46F / D233 is the exact previous product analogue for persisting one historical fresh-reentry proof without changing mounted state;
- 40B / D203 owns the strict third-basis locator-only overlay format and mandatory fresh three-layer proof;
- 47E / D239 supplies the exact historical fresh 40A result selected for persistence;
- existing second-epoch authority inspection keeps immutable launch provenance distinct from mutable current governed state.

The current external review again considered W3C PROV as a mature provenance-interchange model and the reproducibility/versioning systems reviewed for 47E, including DVC and DataLad. Those systems remain useful conceptual or integration prior art, but they do not replace this exact Pyxis authority boundary: proof-gating one exact historical 40A reconstruction through the established 40B writer while preserving explicit current locator ownership and refusing relaunch, branch promotion, or launch-provenance mutation.

**No end-to-end substitute demonstrated in this review.**

## Exact authority subject

`persist_chromium_research_third_changed_basis_epoch_reentry_overlay(...)` requires exactly:

`ChromiumResearchThirdChangedBasisEpochReentryResult`

The helper passes exactly:

`verification_result.fresh_reentry`

to public `persist_chromium_research_third_basis_epoch_reentry_plan_document(...)`.

The product adapter does not manufacture a replacement 40A result and does not widen 40B's accepted authority family.

## Explicit locator discipline

47F adds exactly two durable path inputs:

1. current prior 37C/37D second-epoch continuation-overlay source;
2. one new no-overwrite 40B third-basis overlay destination.

Both fields begin blank.

The prior continuation overlay must be supplied again even though 47E previously used one. The path retained by the historical 47E plan records where that earlier verification looked. It is not perpetual location authority for a later persistence action.

```text
historical 47E locator
!=
authorized current 47F locator
```

Neither path is inferred or prefilled from:

- the 47E plan;
- persisted second-epoch launch provenance;
- raw 38F handoff context;
- 47A–47E receipts;
- checkpoint destinations;
- directory contents;
- filename conventions;
- displayed hashes;
- chronology;
- branch ranking;
- current/latest/head concepts.

## Public 40B remains authoritative

Public 40B receives the exact earned 47E fresh result plus the explicitly re-supplied prior continuation-overlay source and destination.

It then:

1. forms a candidate third-basis re-entry plan from the newly supplied prior-overlay location plus the earned 47E third-basis locator layer;
2. freshly reconstructs the prior second-epoch continuation;
3. freshly re-earns the retained first- and second-root ancestry;
4. freshly reconstructs the third root and root-backed declared session;
5. compares all three retained root identities plus the governed state around them;
6. writes the strict locator-only overlay without overwrite; and
7. strictly round-trip decodes the persisted document.

47F does not duplicate or weaken those rules.

## Bounded product checks

After public 40B returns, 47F additionally requires:

- `checkpoint.reentry is verification_result.fresh_reentry`;
- the public candidate plan uses the newly supplied prior continuation-overlay location;
- every other third-basis locator field remains equal to the earned 47E plan;
- the mandatory fresh proof matches the earned result on prior second-epoch continuation presentation and endpoint;
- retained first-, second-, and third-root SHA-256 record identities match;
- final governed presentation and endpoint match;
- the persisted path equals the explicit destination; and
- strict loading of the persisted overlay equals the public candidate plan.

Those are bounded product-coherence checks only. They do not add authorship, authenticity, trusted time, chronology, semantic support, or citation authority.

## Historical target semantics

47F persists the exact successful 47E verification that mounted its persistence form.

It does not ask which controller happens to be mounted when persistence later occurs.

A researcher may therefore:

```text
prove exact 47E historical third-basis session
→ ordinarily roll the mounted 47D session forward
→ persist the exact earlier 47E proof through 47F
```

without retargeting the 40B overlay to the later controller.

Across persistence, the shell snapshots and requires unchanged:

- `research_controller`;
- `research_session`;
- `research_reentry`;
- retained `second_basis_epoch_continuation_reentry`.

## Product surface

47F adds dedicated products layered on all four 47E launch families:

- persisted second-epoch continuation launch;
- raw pathless 38F handoff;
- inspectable persisted launch;
- inspectable raw handoff.

The 47F persistence form appears only after one newly successful exact 47E verification.

It displays:

- retained first-root SHA-256;
- retained second-root SHA-256;
- third-root SHA-256;
- declaration SHA-256;
- endpoint SHA-256;
- one negative-authority notice;
- one blank current prior-continuation-overlay input;
- one blank no-overwrite 40B destination input;
- one explicit persistence button;
- one status/receipt surface.

Successful persistence locks both inputs and the button.

No restart or relaunch control is added.

## Inspectable and raw launch behavior

Inspectable persisted/raw 47F products inherit the already-earned second-epoch launch-inspection separation.

Persistence must leave both:

- exact immutable `launch_provenance` object; and
- exact current `current_state` inspection object

unchanged.

A raw 38F launch may use an explicitly supplied persisted 37C/37D continuation overlay as the public 40B ancestry input because 40B freshly proves the durable relationships through it.

That path still does not become launch provenance.

For raw launch products:

```text
launch_location_context == None
```

before and after 47F.

## Textual event ownership

47F owns only:

`persist-research-third-changed-basis-epoch-reentry-overlay`

It does not manually invoke a parent `on_button_pressed`. Inherited 47A–47E actions remain Textual MRO-dispatched.

The 47F mixin overrides the 47E verification workflow only to detect one new exact successful proof and mount the persistence form afterward.

## Falsification coverage

Focused tests cover:

- exact 47E result type;
- exact retained 47E fresh 40A result as public 40B's earned re-entry;
- strict 40B round-trip decode;
- unchanged earned third-basis locator layer except for the newly supplied prior-overlay location;
- wrong prior continuation overlay rejected before destination write;
- existing destination preserved byte-for-byte;
- no 47F controls before successful 47E;
- both persistence inputs blank;
- persistence after a later ordinary mounted rollover still targets the exact historical 47E proof;
- mounted controller/session/re-entry and retained second-epoch continuation unchanged;
- raw 38F launch provenance object unchanged and pathless;
- raw current inspection object unchanged;
- plain 47E product scope isolation.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Non-goals

47F does **not** add:

- third-epoch relaunch;
- automatic promotion from overlay persistence;
- third-epoch continuation checkpoint or handoff;
- fourth evidence-basis crossing;
- generic Nth-epoch persistence;
- recursive ancestry representation;
- new persistence format;
- new inspection schema;
- CLI flag;
- locator discovery or prefill;
- launch-path backfill;
- current/latest/head/chronology/branch-ranking authority;
- path identity;
- browser reacquisition;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research.

## Next boundary

If 47F is demonstrated, the next distinct question is explicit typed handoff into the already-established third-basis-epoch product using the exact mandatory fresh proof earned by public 40B.

Persistence itself must not silently become promotion.

That handoff remains separate from 47F.
