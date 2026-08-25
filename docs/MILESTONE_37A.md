# Milestone 37A — Fresh Re-entry for a Second Evidence-Basis Epoch

Decision: D190

## Product question

The first root-backed restart family proves one changed-evidence-basis epoch whose pre-change session is an ordinary 31A re-entry plan. Through 35D/35E and 36A–36D, that first epoch can also be durably continued and operated from the standalone product.

The established 33A–34B application boundaries can create another changed evidence basis from such a live root-backed continuation because its governed declared endpoint remains an ordinary durable revision edge.

Before 37A, however, fresh-process ancestry had a structural gap:

```text
ChromiumResearchRootBackedSessionReentryPlan
→ prior_session_plan: ChromiumResearchSessionReentryPlan
```

That field can describe only an ordinary 31A pre-change session. Treating an already root-backed continuation as though it were ordinary would flatten away the first basis-change ancestry.

37A asks only:

> Can one explicitly defined second evidence-basis epoch be freshly re-entered above a persisted 35D/35E continuation while preserving the first root-backed ancestry as a separate prior layer?

## Decision

Add one new typed in-memory plan:

```text
ChromiumResearchSecondBasisEpochReentryPlan
```

with exactly:

```text
prior_root_backed_continuation_overlay_source
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

The prior-session anchor is one explicit persisted 35D/35E continuation-overlay location.

The plan does **not** contain:

- an ordinary `ChromiumResearchSessionReentryPlan` pretending to represent the prior root-backed session;
- an embedded `ChromiumResearchRootBackedSessionReentryPlan`;
- an embedded `ChromiumResearchRootBackedSessionContinuationReentryPlan`;
- a recursive second-epoch plan;
- a history/head pointer.

Construction snapshots caller-owned locators only and reads no artifacts.

## Fresh reconstruction

37A performs:

```text
explicit prior 35D/35E overlay
→ existing strict 35D overlay decoder
→ existing fresh root-backed continuation re-entry
→ fresh prior governed controller
→ fresh prior declared endpoint
```

Then:

```text
explicit second-epoch appended-member locators
→ existing member loaders
```

The complete changed-basis member order is derived as:

```text
fresh prior endpoint working-set members
+ caller-ordered freshly loaded appended members
```

That complete sequence is supplied to the existing public 34A root loader together with the explicit second changed working-set, note, transition, and root paths:

```text
fresh prior endpoint
+ second successor_items
+ explicit second 20B / 21B / 33B / 34A locations
→ existing 34A fresh root loader
```

Finally:

```text
fresh second root
+ explicit root-started ordinary edge paths
+ explicit declaration
→ existing 35A / 26C declaration relinking
→ existing governed ChromiumResearchSessionController
```

No second-epoch relationship is accepted merely because a caller supplies a previously loaded controller.

## Result shape

The returned:

```text
ChromiumResearchSecondBasisEpochReentryResult
```

retains separately:

- `plan` — the second-epoch locator plan;
- `prior_continuation_reentry` — the complete fresh 35D/35E first-epoch continuation ancestry;
- `loaded_appended_members` — only the freshly relinked second-epoch additions;
- `successor_items` — fresh prior members followed by those additions;
- `loaded_root` — the freshly reconstructed **second** 34A root;
- `loaded_declaration` — the second root-started declared segment;
- `controller` — the governed session above the second root.

The first root remains reachable through:

```text
result.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
```

while the second root is:

```text
result.loaded_root
```

They are distinct ancestry layers. The later root does not overwrite or redefine the earlier root.

## Identity rules

37A preserves the previously learned distinctions.

### Path remains location

The prior continuation overlay and every second-epoch artifact are caller-supplied locations for the current operation.

Moved artifacts work only when their new locations are explicitly supplied.

A different path alone is not evidence of a different session. A path-distinct but content-identical prior continuation may validly reconstruct the same durable pre-change authority if all explicit relationships verify.

### Python object identity remains non-authoritative

Fresh prior continuation reconstruction creates new Python objects. They need not be the same objects used when the second transition was originally persisted.

Durable record identities and exact relinking relationships establish authority, not `is` across independent loads.

### Presentation remains bounded

37A does not infer whole-history equivalence from the final presentation. It reconstructs the explicitly declared second root-backed segment and separately retains the fresh first-epoch prior continuation.

## Deliberate scope: exactly one second epoch

37A does not claim an arbitrary-depth repeated-basis ancestry model.

Its prior anchor is specifically an existing persisted 35D/35E continuation from the first root-backed epoch. A third basis change would have a pre-change session whose ancestry includes this new second epoch and therefore requires a new explicit design decision.

This limitation is intentional:

```text
proof of one second epoch
!=
proof of unbounded recursive epochs
```

Generalization should occur only after the second-epoch authority structure is proven in isolation.

## No durable 37A overlay yet

37A adds only typed plan creation and fresh re-entry.

It does not add a plan-document/overlay format or persistence checkpoint. That follows the same separation used by 35B before 35C:

```text
fresh typed reconstruction first
→ durable operational configuration later
```

A future milestone may persist the second-epoch locator plan only after proof-gating its relationship to an earned second-epoch session.

## Falsifiability

37A is intended to reject when:

- the explicit prior 35D/35E overlay is missing or malformed;
- the prior continuation cannot freshly reconstruct its first root-backed ancestry;
- an appended member locator cannot freshly relink;
- the second changed working set or note is wrong or tampered;
- the second 33B transition is wrong or tampered;
- the second 34A root is wrong or tampered;
- the declared edge sequence does not relink from the second root;
- the second declaration does not match that explicit sequence.

It must not search for replacement artifacts or infer alternate paths.

Tests also require successful fresh reconstruction above both:

- a persisted first 35D continuation; and
- a cumulative 35E continuation.

They preserve the first and second roots as separate ancestry layers, exercise moved explicit paths, and demonstrate that path-distinct/content-identical prior continuations are not rejected merely because their locations differ.

## Authority still absent

37A does not add:

- a durable second-epoch overlay;
- Textual/UI controls;
- arbitrary repeated basis-change ancestry;
- automatic basis-change creation;
- recursive plan discovery;
- directory scanning;
- digest search;
- predecessor discovery;
- format guessing;
- latest/current/head selection;
- chronology or branch semantics;
- semantic improvement/support judgment;
- truth, source-authenticity, authorship, trusted-time, or citation authority.

## Acceptance statement

A successful 37A establishes only:

> One explicitly defined second evidence-basis epoch can be freshly reconstructed above a persisted 35D/35E root-backed continuation without flattening the first basis-change ancestry into an ordinary session plan. The prior continuation is freshly re-entered from its explicit overlay, the second changed-basis/root region is freshly relinked from that exact durable endpoint, and the second declared session is governed through the existing root-started sequence machinery without discovery or global-head authority.
