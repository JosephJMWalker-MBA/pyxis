# Current Frontier — Milestones 39–40

> **Continuity status — implementation through Milestone 40D / D205.**  
> **Updated:** 2026-08-26  
> This document is an additive continuation of `CURRENT_FRONTIER_37_38.md`. It is compact orientation, not a current/head pointer, chronology authority, or substitute for implementation, tests, milestone records, Git history, or executed CI evidence.

## Read this after the earlier frontier chain

Recommended compact orientation order:

1. `README.md` — product identity, authority philosophy, Repository Zero, and browser-research foundations.
2. `docs/CURRENT_FRONTIER.md` — Milestones 25B–34B.
3. `docs/CURRENT_FRONTIER_35_36.md` — root-backed restartability and standalone product continuation through 36D / D189.
4. `docs/CURRENT_FRONTIER_37_38.md` — second evidence-basis epoch and product checkpoint/handoff support through 38F / D199.
5. `docs/CURRENT_FRONTIER_39_40.md` — authority inspection plus the concrete third evidence-basis epoch through 40D / D205.
6. Milestone-specific documents when exact authority, failure, persistence, or acceptance boundaries matter.

The governing continuity rule remains:

```text
implementation + tests + milestone record
> compact continuity summary
> presentation wording
```

If a compact summary conflicts with the implementation or milestone evidence, the stronger evidence wins.

## Starting point

Milestones 37–38 established one second changed evidence-basis epoch while retaining the first root as distinct ancestry. That second epoch became:

- durably restartable;
- ordinarily continuable;
- repeatably cumulatively continuable without recursive continuation-overlay ancestry;
- directly launchable through explicit CLI/Textual entry families;
- checkpointable from the product shell; and
- explicitly handoff-capable from first-checkpoint mode into cumulative mode.

Milestones 39–40 then answer two different questions in sequence:

1. Can already-earned second-epoch authority be made inspectable without turning presentation into authority?
2. Does the explicit evidence-basis-change construction compose one additional concrete time, and can that three-root state become restartable and repeatedly continuable?

The answer through 40D is yes, within the explicit boundaries below.

---

## 39A / D200 — visible second-epoch authority inspection

39A adds a read-only inspection surface over authority that already exists.

Its central distinction is:

```text
immutable launch provenance
!= current governed state
```

The inspection surface can show:

- launch family;
- persisted launch location when a persisted launch actually occurred;
- retained first-root identity;
- retained second-root identity;
- launch endpoint identity;
- current state kind;
- current endpoint identity; and
- current continuation edge count when the current state is an exact typed continuation.

Launch provenance remains fixed while current governed state may advance through already-earned rollover or cumulative-promotion behavior.

A displayed path remains launch location context only. An in-process handoff has no persistent launch path, and a later checkpoint path must not be backfilled into earlier launch provenance.

The Textual inspection panel adds no file reads, writes, discovery, checkpoint authority, restart authority, browser authority, or current/latest/head semantics.

---

## 39B / D201 — deterministic non-interactive authority inspection

39B moves second-epoch authority derivation into one UI-independent application projection shared by both interactive and non-interactive surfaces.

Therefore:

```text
Textual inspection derivation
== non-interactive inspection derivation
```

at the application-model boundary.

The public non-interactive entry is:

```text
pyxis research-inspect
```

with explicit mutually exclusive persisted entry families for:

- a second-basis-epoch overlay; or
- a second-basis-epoch continuation overlay.

Each route performs explicit configuration decode, fresh re-entry, explicit path/result proof, shared projection, and deterministic JSON serialization.

The report format is:

```text
pyxis.chromium.research_second_basis_epoch_authority_inspection.v1
```

The report is read-only inspection, not evidence or control-plane state. Report text, paths, and SHA-256 values do not become mutation, restart, branch, chronology, latest/current/head, authorship, authenticity, trusted-time, semantic-support, or citation authority.

39B deliberately does not invent persistence for the exact in-process 38F handoff.

---

## 40A / D202 — explicit third evidence-basis epoch composition

40A asks only whether the already-proven basis-change construction composes one additional concrete time.

One explicit persisted 37C/37D second-epoch continuation is freshly reconstructed, then used as the exact pre-third-epoch anchor for:

```text
explicit appended working-set members
→ explicit changed working set + note
→ explicit 33B transition
→ explicit third 34A root
→ explicit root-started ordinary declaration
→ governed controller
```

A successful result retains three distinct ancestry layers:

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
third-root declared segment
```

The first and second roots are freshly re-earned through the explicitly supplied prior second-epoch continuation. The third root is freshly relinked above that proven endpoint.

40A intentionally uses concrete third-epoch types. It does not introduce `epoch[n]`, a recursive ancestry tree, a generic lineage walker, or an arbitrary-depth claim.

---

## 40B / D203 — persisted third-epoch re-entry overlay

40B makes the concrete three-root state durably restartable through:

```text
pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1
```

The overlay is strict locator-only operational configuration. It stores explicit locations for the prior second-epoch continuation plus the third-epoch changed-basis layer and root-started declared segment.

Loading the overlay proves only configuration shape.

Persistence is proof-gated: before bytes are written, Pyxis independently invokes the public 40A re-entry path and freshly matches all retained authority layers relevant to the three-root structure, including:

- retained first-root identity;
- retained second-root identity;
- selected post-second-epoch continuation presentation and endpoint;
- third-root identity; and
- final third-epoch governed presentation and endpoint.

Paths remain locations, not durable identity. No discovery, path search, chronology, branch, or latest/current/head semantics are added.

---

## 40C / D204 — first ordinary continuation above persisted third epoch

40C adds one restartable ordinary continuation above an explicitly persisted 40B third-epoch overlay.

Its continuation format is:

```text
pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1
```

with one direct 40B ancestry anchor plus one explicitly ordered continuation edge sequence and declaration.

Fresh re-entry follows:

```text
explicit 40B overlay
→ strict configuration decode
→ fresh third-epoch re-entry
→ first root re-earned
→ second root re-earned
→ third root re-earned
→ explicit ordinary continuation edges
→ explicit declaration
→ governed controller
```

The chosen continuation remains caller-owned. Pyxis does not discover siblings, select a preferred successor, infer chronology, or designate a head.

40C proves only the first ordinary continuation above the persisted third epoch.

---

## 40D / D205 — repeatable cumulative continuation above persisted third epoch

40D closes the concrete three-root continuation loop by making post-third-root continuation repeatable while preserving one fixed direct durable third-epoch anchor.

The required shape is:

```text
40B third-epoch overlay
        ↓
retained first root
retained second root
retained third root
        ↓
E1 → E2 → ... → En
```

The rejected shape is recursive continuation-overlay ancestry:

```text
40B
 ↓
40C(E1)
 ↓
40C(E2)
 ↓
40C(E3)
```

40D reuses the existing 40C continuation-overlay format. Each cumulative extension keeps:

```text
prior_third_basis_epoch_overlay_source = unchanged direct 40B anchor
```

and extends only the explicitly ordered post-third-root edge tuple.

Every cumulative extension freshly:

1. decodes and re-enters the current 40C overlay;
2. re-enters the direct 40B anchor;
3. re-earns first-, second-, and third-root ancestry;
4. matches the supplied current governed state;
5. matches the explicitly chosen rollover;
6. appends exactly one explicitly supplied successor edge;
7. relinks the complete cumulative sequence from the third-epoch endpoint;
8. persists a new cumulative declaration;
9. builds a next plan with the same direct 40B anchor; and
10. freshly re-enters and verifies the chosen terminal state before writing the next overlay.

Whole-presentation equality is deliberately not required between a one-hop rollover and a cumulative declaration because the cumulative presentation legitimately contains more retained edges. Terminal equivalence is proven through durable terminal edge identity plus exact final human note text.

The focused 40D tests repeat the extension operation again from a freshly persisted cumulative checkpoint. That distinguishes a repeatable mechanism from another one-off special case.

## Current implemented frontier

The implemented frontier is **Milestone 40D / Decision D205**.

The strongest compact statement currently earned is:

> One persisted third evidence-basis epoch can retain a direct durable 40B ancestry anchor while ordinary post-third-root continuation is extended cumulatively across repeated checkpoints, with first-, second-, and third-root ancestry freshly preserved.

That statement is intentionally narrower than:

> Pyxis supports arbitrary-depth evidence-basis lineage.

The latter has not been demonstrated.

The latest 40D pull request reports the exact-head test matrix passing across Python 3.11, 3.12, 3.13, and 3.14, with 984/984 tests passing on the Python 3.11 lane.

## Authority boundaries still intentionally absent

Through 40D, Pyxis still does **not** claim or infer:

- arbitrary-depth or generic `epoch[n]` evidence-basis lineage;
- recursive continuation-overlay ancestry;
- a global current/latest/head research state;
- complete revision history;
- branch identity or chronology from local durable references;
- path identity;
- source discovery from digest or filename matching;
- authorship, authenticity, or trusted time from SHA-256 identity;
- semantic support or citation authority from human notes, selections, or inspection reports;
- third-epoch CLI/Textual launch;
- three-root authority-inspection UI/report; or
- autonomous research authority from any existing shell or report surface.

These are product constraints, not accidental omissions.

## Next decision frontier

40D creates several structurally available directions, but authorizes none automatically.

Candidate next product questions include:

- Should the already-proven third epoch gain explicit CLI/Textual product launch parity with the second epoch?
- Should the shared authority-inspection model be extended to three retained roots before another basis-change composition is attempted?
- Should Pyxis test a fourth concrete evidence-basis epoch before considering a generic representation?
- Has the repeated concrete pattern now produced enough evidence to design a bounded generic ancestry model, and what proof obligations would prevent that abstraction from laundering authority?
- Should the research-control-plane design work become the next runtime frontier instead of extending lineage depth?

The next milestone should begin by choosing one explicit product question rather than treating implementation convenience or visible symmetry as authorization.