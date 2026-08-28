# Current Frontier — Milestones 41–43

> **Continuity status — implementation through Milestone 43E / D217.**  
> **Updated:** 2026-08-27  
> This document is an additive continuation of `CURRENT_FRONTIER_39_40.md`. It is compact orientation, not a current/head pointer, chronology authority, or substitute for implementation, tests, milestone records, Git history, or executed CI evidence.

## Read this after the earlier frontier chain

Recommended compact orientation order:

1. `README.md` — product identity, authority philosophy, Repository Zero, and browser-research foundations.
2. `docs/CURRENT_FRONTIER.md` — Milestones 25B–34B.
3. `docs/CURRENT_FRONTIER_35_36.md` — root-backed restartability and standalone product continuation through 36D / D189.
4. `docs/CURRENT_FRONTIER_37_38.md` — second evidence-basis epoch and product checkpoint/handoff support through 38F / D199.
5. `docs/CURRENT_FRONTIER_39_40.md` — authority inspection plus the concrete third evidence-basis epoch through 40D / D205.
6. `docs/CURRENT_FRONTIER_41_43.md` — third-epoch product parity, three-root authority inspection, and bounded cumulative-mechanics consolidation through 43E / D217.
7. Milestone-specific documents when exact authority, failure, persistence, or acceptance boundaries matter.

The governing continuity rule remains:

```text
implementation + tests + milestone record
> compact continuity summary
> presentation wording
```

If a compact summary conflicts with implementation or milestone evidence, the stronger evidence wins.

## Starting point

40A–40D established one concrete third evidence-basis epoch above an explicitly reconstructed second-epoch continuation. That three-root state became durably restartable and repeatably ordinarily continuable while retaining one direct 40B anchor rather than recursively chaining continuation overlays.

The strongest statement at 40D was intentionally concrete:

```text
first root
   ↓
first-root continuation
   ↓
second root
   ↓
second-root continuation
   ↓
third root
   ↓
repeatable post-third-root continuation
```

It was not a claim that Pyxis supported arbitrary-depth evidence-basis ancestry.

Milestones 41–43 answer two different questions:

1. Can the already-earned concrete third epoch receive the same usable product and inspection surfaces that the second epoch already earned?
2. After root-backed, second-epoch, and third-epoch cumulative continuation have independently demonstrated the same mechanics, which procedures are now safe to share without turning different ancestry semantics into one generic authority model?

The answer through 43E is yes to both, within the bounded rules below.

---

## 41A / D206 — proven third-epoch shell launch lineage

41A establishes the application-layer prerequisite for public third-epoch launch.

One explicit 40B or 40C/40D path is not simply attached to an arbitrary in-memory re-entry. Pyxis strictly decodes the exact supplied overlay, freshly reconstructs it, and matches the complete earned state before returning one proof-carrying launch wrapper.

The two launch families are:

```text
ChromiumResearchThirdBasisEpochShellLineage
ChromiumResearchThirdBasisEpochContinuationShellLineage
```

The wrappers retain:

```text
explicit overlay location context
+
fresh re-entry proven from that location
```

not:

```text
caller object + caller path = authority
```

The 40B proof matches retained second-epoch continuation presentation/endpoint, first-root identity, second-root identity, third-root identity, third-epoch presentation, and terminal endpoint. The 40C/40D continuation proof additionally matches the current continuation before applying the nested three-root proof.

A path remains operational location context only. Path-distinct equivalent overlays are acceptable only after fresh reconstruction proves equivalent earned state.

41A introduces no CLI, UI, persistence, discovery, generic lineage walker, or arbitrary-depth ancestry.

## 41B / D207 — dedicated third-epoch product launch shells

41B consumes only the 41A proof-carrying wrappers and gives the third epoch explicit standalone product entry through `pyxis research-shell`.

The public persisted entry families are:

```text
--third-basis-epoch-overlay
--third-basis-epoch-continuation-overlay
```

Dedicated Textual shells retain the immutable launch lineage while mounting the already-earned governed controller. They do not manufacture an ordinary restart-plan identity from a stronger third-epoch controller.

The persisted launch path therefore becomes:

```text
explicit overlay
→ strict decode
→ fresh re-entry
→ 41A path/result proof
→ dedicated third-epoch shell
```

40D cumulative overlays continue to use the established 40C continuation-overlay family; no separate cumulative persisted launch type is invented.

## 41C / D208 — first explicit 40B → 40C Textual checkpoint

41C brings the first post-third-root continuation checkpoint into the product shell.

After one explicit ordinary rollover, the researcher supplies the existing explicit durable locations needed to persist the first 40C continuation. The UI does not discover, prefill, or infer those locations.

The checkpoint remains a distinct action from the rollover that produced the candidate continuation.

Therefore:

```text
successful rollover
!=
durable continuation checkpoint
```

and the shell advances only after the concrete 40C persistence/proof succeeds.

## 41D / D209 — repeatable cumulative third-epoch checkpointing

41D extends the first checkpoint into the already-proven 40D cumulative mode.

The shell retains two different kinds of state:

```text
immutable persisted launch lineage
!=
mutable current typed continuation
```

Each successful cumulative checkpoint:

- keeps the fixed direct 40B anchor;
- extends only the explicit ordered post-third-root edge tuple;
- proves the fresh next continuation through the established 40D application boundary;
- locks the old checkpoint form;
- visibly promotes the fresh governed state; and
- mounts a fresh explicit checkpoint surface for another cycle.

This makes the concrete three-root product repeatable without recursive continuation-overlay ancestry.

## 41E / D210 — explicit in-process handoff into cumulative mode

41E preserves another distinction:

```text
successful first 40C checkpoint
!=
automatic transition into cumulative mode
```

The researcher must explicitly choose to continue in cumulative mode.

The handoff carries the exact typed `fresh_reentry` already earned by the checkpoint. It does not reload the just-written continuation overlay merely to recreate authority already present in memory.

Because no persisted launch occurred for that cumulative shell, the raw handoff deliberately has no persistent launch path to display or claim.

This is not a shortcut around path proof for persisted launch. It is a separate exact in-process authority family.

---

## 42A / D211 — visible third-epoch authority inspection

42A gives the third epoch a read-only inspection projection without turning presentation into authority.

Its central separation is:

```text
immutable launch provenance
!=
current governed state
```

The projection records, as appropriate:

- persisted launch family or exact in-process handoff family;
- launch location context when a persisted launch actually occurred;
- first-root identity;
- second-root identity;
- third-root identity;
- launch endpoint identity;
- current state kind and source;
- current endpoint identity; and
- continuation edge count for an exact typed continuation.

A later cumulative checkpoint may advance current governed state while launch provenance stays unchanged.

A raw 41E handoff reports no persistent launch location. A later checkpoint path cannot be backfilled into earlier launch provenance.

The projection is read-only. It grants no mutation, restart, checkpoint, discovery, browser, path, chronology, semantic-support, or citation authority.

## 42B / D212 — deterministic non-interactive third-epoch inspection

42B extends `pyxis research-inspect` to persisted third-epoch entry families:

```text
--third-basis-epoch-overlay
--third-basis-epoch-continuation-overlay
```

Each route performs:

```text
explicit persisted path
→ strict decode
→ fresh re-entry
→ 41A path/result proof
→ 42A UI-independent inspection projection
→ deterministic JSON
```

The report format is:

```text
pyxis.chromium.research_third_basis_epoch_authority_inspection.v1
```

The exact in-process 41E handoff is intentionally not exposed through `research-inspect` because it has no persisted launch locator to supply to a fresh process.

The non-interactive path imports no Textual UI and adds no discovery, current/latest/head selection, or stronger path semantics.

By 42B the second and third concrete epochs have product inspection parity, but they remain distinct concrete authority models.

---

## 43A–43E — consolidate only mechanics that earned reuse

Milestone 43 begins after three concrete cumulative families have independently proven repeatable behavior:

```text
35E  root-backed cumulative continuation
37D  second-epoch cumulative continuation
40D  third-epoch cumulative continuation
```

The key architectural observation is:

> Their ancestry semantics differ. Several surrounding procedures do not.

43A–43E extract only those procedures.

### 43A / D213 — fixed-anchor cumulative extension kernel

43A extracts the triply-proven application procedure for cumulative extension into a private kernel.

The shared procedure covers mechanics such as explicit path preflight, strict current-overlay decode, fresh re-entry, appending one explicit successor, relinking the complete cumulative edge sequence from the concrete fixed anchor, terminal identity/text checks, sequence declaration persistence, fresh next re-entry, and overlay round-trip.

Concrete adapters still own:

- root count and ancestry shape;
- current-state and rollover proof;
- concrete fixed-anchor field;
- concrete continuation plan/result types;
- concrete persistence format and public error contract.

There is no generic anchor record and no `epoch[n]` model.

### 43B / D214 — cumulative checkpoint Textual form kernel

43B extracts only the triply-proven four-input checkpoint-form mechanics:

```text
exact current typed continuation
+ exact rollover
→ four blank explicit path fields
→ pending status
→ old-form lock after proven success
```

The concrete root-backed, second-epoch, and third-epoch control types remain public and retain their own types, labels, selectors, error wording, and terminology.

43B explicitly declines to genericize cumulative handoff because the constructor semantics differ across the three families.

### 43C / D215 — visible cumulative promotion kernel

43C extracts the common post-proof visible state transition.

Only after the concrete family proves one cumulative checkpoint does the shared UI procedure rebuild and verify presentation, remove the old one-hop/checkpoint surface, advance common live controller/session state, retain exact family state through narrow callbacks, mount the success receipt and fresh cumulative sequence, and unlock endpoint revision.

Proof remains outside the helper.

This preserves the ordering:

```text
concrete proof
→ lock old form
→ validate fresh presentation
→ visible state promotion
→ fresh cumulative surface
```

Hidden typed state therefore cannot silently outrun the visible governed presentation.

### 43D / D216 — rollover-mount kernel

43D extracts only the shared checkpoint-gating surface transition after the ordinary base shell has already mounted and retained the exact one-hop rollover.

The concrete subclass still explicitly invokes base rollover first. The private helper then verifies the retained rollover, removes stale prior-cycle UI, prevents ordinary restart-plan controls on the cumulative shell, locks revision pending checkpoint, and mounts the concrete cumulative checkpoint form.

The base rollover call remains concrete because it is the authority-bearing point that creates and retains the one-hop continuation.

### 43E / D217 — explicit-path submission through the existing form kernel

43E closes the extraction run at an even narrower seam than a generic save handler.

The existing private 43B form kernel now owns only:

```text
read the four explicit path inputs
→ reject blanks in the established order using caller-owned concrete messages
→ return four exact Path values
```

The concrete save handlers still own, in order:

```text
missing rollover check
→ exact displayed rollover identity
→ exact current typed re-entry identity
→ four-path collection
→ concrete family persistence
→ concrete 35E / 37D / 40D proof
→ old-form lock
→ 43C promotion
```

43E therefore does not create a generic save orchestration layer.

That stopping point is deliberate: the code remaining around the shared path submission increasingly expresses the authority semantics that distinguish the three families.

---

## Architecture after 43E

The cumulative path now has a deliberately asymmetric structure:

```text
CONCRETE AUTHORITY SEMANTICS
root-backed / second epoch / third epoch
        ↓
BOUNDED PRIVATE MECHANICAL KERNELS
43A persistence procedure
43B form mechanics + 43E explicit path submission
43C visible promotion
43D rollover-mount transition
        ↓
ESTABLISHED RESEARCH PRIMITIVES
explicit revisions, declarations, re-entry, persistence
```

This is not an unfinished generic epoch engine.

The concrete authority layers remain valuable because they make different proof obligations visible and falsifiable.

Second- and third-epoch shell-lineage and authority-inspection code still show surface symmetry, but that symmetry carries different earned ancestry obligations:

```text
second epoch
→ retained first root + second root

third epoch
→ retained second-epoch continuation + first root + second root + third root
```

A generic shell-lineage or generic authority-inspection object would therefore do more than remove syntax duplication. It would encode a stronger claim that those ancestry obligations have one already-earned generic meaning. Pyxis has not demonstrated that claim.

## Adjacent prior art reviewed at this frontier

Before considering another ancestry abstraction, three mature adjacent patterns were reviewed:

- **W3C PROV / PROV-O** provides a mature interoperable vocabulary for provenance relationships among entities, activities, and agents.
- **RO-Crate** provides a mature research-object packaging and contextual metadata model built on linked-data conventions.
- **Event sourcing** provides a mature architecture for reconstructing state from an ordered event log and retaining historical state changes.

All three are useful reference points. They solve adjacent interoperability, packaging, or event-history problems that Pyxis should reuse rather than reinvent when those jobs arise.

None is an end-to-end substitute for Pyxis's current research authority contract:

```text
explicit caller-supplied durable locators
+
local fresh reconstruction and proof
+
no ambient discovery
+
no global latest/current/head
+
no chronology inferred merely from available records
```

Importing a generic event log or provenance DAG as the governing model would risk laundering stronger completeness, chronology, traversal, or history assumptions into Pyxis.

Therefore the conclusion of this review is:

> **no end-to-end substitute demonstrated in this review**

This is not a novelty claim. It is a boundary decision about the current product contract.

## Current implemented frontier

The implemented frontier is **Milestone 43E / Decision D217**.

The strongest compact statement currently earned is:

> Pyxis can preserve and productize one concrete three-root changed-evidence-basis lineage through explicit persisted launch, repeatable cumulative continuation, explicit in-process handoff, visible authority inspection, and deterministic non-interactive inspection; and it can share the triply-proven mechanical parts of cumulative continuation across root-backed, second-epoch, and third-epoch families without making their ancestry semantics generic.

That is stronger than the 40D frontier and still narrower than:

> Pyxis supports arbitrary-depth evidence-basis lineage.

The latter remains unproven and intentionally unclaimed.

## Authority boundaries still intentionally absent

Through 43E, Pyxis still does **not** claim or infer:

- a fourth evidence-basis epoch merely by analogy;
- generic `epoch[n]` or arbitrary-depth evidence-basis ancestry;
- a recursive ancestry walker or generic shell lineage;
- generic authority-inspection ancestry semantics;
- recursive continuation-overlay ancestry;
- a global current/latest/head research state;
- complete revision or evidence-basis history;
- unique successor relationships;
- chronology or branch identity from local durable references;
- path identity;
- source discovery from digest or filename matching;
- authorship, authenticity, or trusted time from SHA-256;
- semantic support or citation authority from evidence membership, human notes, or inspection reports; or
- autonomous browser/research authority from any shell, report, or control-plane text.

These absences remain product constraints, not implementation accidents.

## Next decision frontier

43E should end the current extraction series. The remaining cumulative save-handler code is increasingly concrete authority semantics rather than commodity repetition.

The next runtime milestone should begin from a researcher-facing product question instead of from another ancestry-depth proof or code-symmetry exercise.

The strongest candidate is:

> **How should a researcher explicitly say “my evidence basis changed” from inside the product using already-proven concrete authority paths?**

The repository already contains important lower-level application primitives:

```text
33A
exact governed declared endpoint
+ explicit already-relinked additional evidence
+ fresh human rationale
→ prepared changed working set + note

33B
exact old declared endpoint
+ exact prepared changed basis
→ explicit durable cross-working-set transition
```

Those primitives deliberately stop before product UI/CLI adoption, and no standalone Textual surface currently exposes them directly.

That creates several questions that must be answered before implementation:

1. **Additional evidence entry:** how does the researcher explicitly supply already-relinked 17D/18D/19D evidence to the product without adding ambient discovery or autonomous browsing authority?
2. **Explicit preparation vs adoption:** how should the product keep “prepare changed basis” visibly separate from “adopt this transition,” preserving the 33A/33B distinction?
3. **Concrete family ceiling:** how should the product prevent a generic changed-basis action from silently turning a third-epoch session into an unproven fourth epoch?
4. **Interoperability later:** should a future read-only export projection map Pyxis provenance into W3C PROV or RO-Crate for exchange, while remaining strictly downstream of Pyxis authority rather than feeding authority back into it?

The generic ancestry question should remain deferred until a product requirement actually needs arbitrary depth and can state the proof obligations that would make it safe.

Therefore the recommended next runtime direction is productization of **explicit evidence-basis change**, bounded by the concrete authority families already earned—not a fourth epoch and not a generic ancestry engine.

## Continuity rule

For future development sessions:

```text
implementation + tests + milestone record
> compact continuity summary
> presentation wording
```

A future session should orient through this frontier file before inferring work from older status headers in `CURRENT_STATE.md`, `DECISIONS.md`, or the preserved historical narrative.

Pyxis should continue to prefer explicit authority, falsifiable evidence, mature-component reuse, and narrow earned capability over convenient inference.