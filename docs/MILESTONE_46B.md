# Milestone 46B — explicit second changed-basis revision root

Decision: **D229**  
Issue: **#178**

## Product boundary

46A / D228 made one second changed-basis 33B transition a bounded live product action from exact one-root continuation authority. 46B adds only the next already-proven construction step: one human-authored 34A revision root over that exact successful 46A transition.

```text
exact successful 46A second transition
+ new human root rationale
+ caller-explicit durable locators
→ one public 34A second changed-basis revision root
```

This remains deliberately weaker than a second epoch:

```text
second 34A root
!= first 34B post-root edge
!= second-epoch declaration
!= second-epoch session/re-entry/adoption
```

## Reuse decision

No generic repeated-root mechanism was introduced.

46B reuses:

- 44C / D220 as the concrete first changed-basis product pattern;
- the existing public 34A transition-revision-root create/persist/load boundaries;
- the already-demonstrated 37A lower-level second-epoch construction, which applies those same 34A primitives to a second 33B transition before creating 34B/declaration/re-entry artifacts;
- the exact typed `ChromiumResearchSecondChangedBasisTransitionResult` supplied by 46A / D228;
- the 45A / D226 persisted-versus-raw launch-provenance distinction without modifying it.

**No end-to-end substitute demonstrated in this review.**

## Application authority

`persist_chromium_research_second_changed_basis_revision_root(...)` requires exactly one `ChromiumResearchSecondChangedBasisTransitionResult`.

Before creating the root, it verifies that the transition result remains internally coherent:

- its freshly loaded transition SHA matches its persisted 33B transition SHA;
- its loaded prior endpoint identity matches the exact endpoint retained by the 46A transition controller;
- its loaded successor working-set SHA matches the exact successful 44A preparation receipt;
- its loaded successor working-set-note SHA matches the exact successful 44A preparation receipt.

The result retains:

- the exact 46A transition result;
- the in-memory public 34A root;
- no-overwrite root persistence evidence;
- one freshly loaded/relinked 34A root.

## Explicit locator rule

All durable paths remain caller supplied:

1. prior endpoint edge source;
2. changed working-set source;
3. changed working-set-note source;
4. second changed-basis transition source;
5. root destination.

The new human root rationale is also explicit.

No locator is copied or inferred from:

- the 46A transition persistence receipt;
- the 44A preparation receipts;
- a persisted 35D/35E launch path;
- a raw 36D in-process handoff;
- a checkpoint destination;
- directory contents, naming conventions, or ambient state.

Receipt paths may be displayed for audit context, but the input controls remain blank.

## Product surface

`RootBackedContinuationResearchSessionShell` now exposes the 46B form only after a newly successful exact 46A transition.

The form starts with:

- blank human rationale;
- blank prior-edge source;
- blank changed working-set source;
- blank changed-note source;
- blank second-transition source;
- blank root destination.

A successful root persistence:

- freshly relinks through public 34A boundaries;
- retains the exact 46A transition result;
- locks the 46B form as historical evidence;
- leaves the currently mounted controller unchanged;
- leaves the currently mounted session unchanged;
- leaves the exact retained one-root continuation re-entry unchanged.

It does not expose or create a 34B edge, second-epoch declaration, second-epoch adoption, 37A re-entry, or 37B overlay.

## Historical coexistence is intentional

46A and 46B have different rollover behavior because they hold different authority states.

Before 46A persistence:

```text
prepared candidate + unsaved second transition form
+ adopted one-root rollover
→ transition form becomes stale
```

That prevents silent retargeting.

After 46A persistence:

```text
exact durable second transition
+ later continuation of the older one-root branch
→ exact second transition remains eligible for its own 34A root
```

The 46B root form is therefore **not** marked stale by later one-root rollover. It remains bound to the historical exact 46A result and still requires the caller to provide explicit durable locators.

This coexistence does not select either line as `current`, `latest`, `head`, newer, preferred, or semantically authoritative.

## Launch provenance remains orthogonal

The existing 45A inspection adapters inherit the new product action without acquiring new launch authority.

- persisted 35D/35E launches retain their exact immutable launch-location context;
- raw 36D in-process handoffs continue to have `launch_location_context=None`;
- successful 46A or 46B persistence does not backfill a launch path into a raw handoff;
- no root destination becomes launch provenance.

## Falsification coverage

Focused 46B tests exercise:

- exact 46A result requirement;
- valid 34A persistence and fresh relink;
- no-op human rationale rejection under the existing public 34A rule;
- moved durable working-set/note/transition files accepted only through explicit current paths;
- wrong transition locator rejection before root creation completes;
- no root controls before successful 46A;
- blank rationale and five blank locator fields after 46A success;
- mounted controller/session/re-entry identity preserved by root persistence;
- successful root remaining historical rather than becoming adopted state;
- exact 46B root authority surviving a later one-root rollover after 46A success;
- persisted launch provenance object identity remaining unchanged;
- raw 36D launch provenance remaining pathless after root persistence.

## Non-goals

46B does **not** add:

- the second 34B post-root edge;
- a second-epoch declaration;
- second-epoch adoption or re-entry;
- a 37B overlay;
- a new CLI flag;
- a new persistence format;
- changed-basis candidate reset/reconfiguration after rollover;
- launch-path backfill for raw handoffs;
- generic Nth-root/Nth-epoch abstractions;
- a fourth epoch;
- arbitrary-depth ancestry;
- discovery, prefill, `current`, `latest`, `head`, chronology, or branch-ranking authority;
- path identity, authorship, authenticity, trusted-time, semantic-support, or citation authority;
- browser reacquisition or autonomous research behavior.

## Next boundary

If 46B is demonstrated, the next creation question is separate: whether one exact successful 46B second root should receive its first public 34B post-root edge as a bounded product action. That is not implied by root persistence itself.
