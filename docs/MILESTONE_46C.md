# Milestone 46C — explicit first post-second-root edge

Decision: **D230**  
Issue: **#180**

## Product boundary

46B / D229 made one second changed-basis 34A revision root a bounded product action. 46C adds only the next already-proven construction step: one ordinary 34B revision edge whose predecessor is that exact successful 46B root.

```text
exact successful 46B second root
+ new human post-root rationale
+ caller-explicit current root path
+ caller-explicit edge destination
→ one public 34B first post-second-root edge
```

This remains deliberately weaker than a second epoch:

```text
first post-second-root edge
!= sequence declaration
!= second-epoch session
!= second-epoch re-entry/adoption
```

## Reuse decision

No generic repeated-root-edge mechanism was introduced.

46C reuses:

- 44D / D221 as the concrete first changed-basis 34A-root → 34B-edge product pattern;
- the existing public transition-root edge create/persist/load boundaries;
- the existing ordinary edge persistence format;
- the already-demonstrated 37A second-epoch construction, which creates this same 34B bridge from the second 34A root before declaration and re-entry;
- the exact typed `ChromiumResearchSecondChangedBasisRevisionRootResult` supplied by 46B / D229;
- the 45A / D226 persisted-versus-raw launch-provenance distinction without modifying it.

**No end-to-end substitute demonstrated in this review.**

## Application authority

`persist_chromium_research_second_changed_basis_root_edge(...)` requires exactly one `ChromiumResearchSecondChangedBasisRevisionRootResult`.

Before creating the edge, it verifies that the exact 46B result remains internally coherent:

- its freshly loaded root SHA matches its persisted root SHA;
- its freshly loaded human root wording matches its in-memory 46B root wording.

The result retains:

- the exact 46B root result;
- the in-memory public 34B root-edge extension;
- no-overwrite persistence evidence in the existing ordinary edge format;
- one freshly loaded/relinked ordinary edge.

## Explicit locator rule

46C requires only:

1. new human post-root rationale;
2. current durable second-root source;
3. no-overwrite edge destination.

Only the caller-supplied current root file is reopened as durable predecessor evidence.

The earlier second-transition, changed working set, and changed working-set note are not traversed again. No path is copied or inferred from:

- the 46B root receipt;
- 46A/44A receipts;
- persisted 35D/35E launch provenance;
- raw 36D handoff context;
- checkpoint destinations;
- directory contents or filename conventions.

The root output path may be displayed as audit receipt context, but the current-root input begins blank.

## Product surface

`RootBackedContinuationResearchSessionShell` now exposes the 46C form only after a newly successful exact 46B root.

The form starts with:

- blank human rationale;
- blank current second-root source;
- blank edge destination.

A successful edge persistence:

- freshly relinks through public 34B boundaries;
- retains the exact 46B root result;
- locks the 46C form as historical evidence;
- leaves the currently mounted controller unchanged;
- leaves the currently mounted session unchanged;
- leaves the exact retained one-root continuation re-entry unchanged.

It does not expose or create a sequence declaration, second-epoch session, second-epoch re-entry/adoption, or 37B overlay.

## Historical coexistence is intentional

The exact 46B root is durable historical relationship authority. Therefore:

```text
successful 46B second root
+ later continuation of the older one-root branch
→ exact second root remains eligible for its own first local 34B edge
```

The 46C edge form is not marked stale by later one-root rollover. It remains bound to the historical exact 46B result and still requires caller-explicit current-root and destination paths.

This does not select either line as `current`, `latest`, `head`, newer, preferred, or semantically authoritative.

## Launch provenance remains orthogonal

The existing 45A inspection adapters inherit the new edge action without acquiring new launch authority.

- persisted 35D/35E launches retain their exact immutable launch-location context;
- raw 36D in-process handoffs continue to have `launch_location_context=None`;
- successful 46A/46B/46C persistence does not backfill a launch path into a raw handoff;
- neither the second-root path nor the post-root edge destination becomes launch provenance.

## Falsification coverage

Focused 46C tests exercise:

- exact 46B result requirement;
- valid 34B persistence and fresh relink;
- no-op human rationale rejection under the existing public 34B rule;
- moved durable second-root file accepted only through an explicit current path;
- wrong root locator rejection before edge creation completes;
- no edge controls before successful 46B;
- blank rationale/current-root/destination fields after 46B success;
- mounted controller/session/re-entry identity preserved by edge persistence;
- successful edge remaining historical rather than becoming adopted state;
- exact 46C edge authority surviving a later one-root rollover after 46B success;
- persisted launch provenance object identity remaining unchanged;
- raw 36D launch provenance remaining pathless after edge persistence.

## Non-goals

46C does **not** add:

- a second-epoch sequence declaration;
- a second-epoch session;
- second-epoch adoption or re-entry;
- a 37B overlay;
- a new CLI flag;
- a new persistence format;
- changed-basis candidate reset/reconfiguration after rollover;
- launch-path backfill for raw handoffs;
- generic Nth-root/Nth-edge/Nth-epoch abstractions;
- a fourth epoch;
- arbitrary-depth ancestry;
- discovery, prefill, `current`, `latest`, `head`, chronology, or branch-ranking authority;
- path identity, authorship, authenticity, trusted-time, semantic-support, or citation authority;
- browser reacquisition or autonomous research behavior.

## Next boundary

If 46C is demonstrated, the next product question is separate: whether the exact second-root + first-edge chain should be explicitly declared/adopted as the already-existing second-epoch governed session/re-entry product. 46C itself creates no declaration and grants no second-epoch launch authority.
