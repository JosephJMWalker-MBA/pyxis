# Milestone 46D — Explicit second changed-basis session adoption

Decision: **D231**

## Product result

46D productizes the already-proven declaration/adoption boundary after the exact 46C first post-second-root edge.

```text
exact 46C edge
+ explicit current edge path
+ explicit no-overwrite declaration destination
→ root-started declared segment
→ standard governed controller
→ explicit shell-local adoption
```

This is the first 46-series step that intentionally replaces the shell's active governed controller.

It still does **not** create second-epoch fresh-process re-entry or a persisted second-epoch overlay.

## Why declaration and adoption remain one boundary

44E / D222 already establishes the first-root pattern: open the exact root-started sequence, persist/reload its declaration, construct the standard governed controller, then promote that controller only after the explicit action succeeds.

37A's second-epoch construction expects the same durable shape above the second root before fresh-process re-entry.

Splitting declaration from in-process adoption here would manufacture a new product boundary unsupported by the prior implementation evidence.

## Application boundary

`ChromiumResearchSecondChangedBasisSessionAdoptionResult` retains:

- the exact `ChromiumResearchSecondChangedBasisRootEdgeResult`;
- the freshly loaded root-started sequence;
- no-overwrite declaration persistence evidence;
- the freshly reconciled declaration;
- the standard `ChromiumResearchSessionController`.

`adopt_chromium_research_second_changed_basis_governed_session(...)` requires exactly the 46C result plus two caller-explicit durable locators:

- current first post-second-root edge source;
- declaration destination.

The second 34A root is already the exact loaded starting record retained by 46C. Only the explicit current 46C edge file is reopened. The historical edge receipt is not path authority.

## Product boundary

46D uses a dedicated `SecondChangedBasisSessionAdoptionResearchSessionShell` over the reusable 35D/35E/46A–46C continuation shell.

Before adoption, inherited one-root 35E behavior remains unchanged.

After exact 46C success, one adoption form appears with blank:

- edge source;
- declaration destination.

Declaration construction itself cannot mutate the mounted one-root controller/session/re-entry.

After successful explicit promotion:

- the exact newly declared second-root-backed controller becomes active;
- session/presentation/working-set contexts are replaced from that controller;
- completed 46A–46D result objects and receipts remain historical evidence;
- changed-basis candidate authority is cleared;
- pending first-root cumulative-checkpoint controls/receipts are removed;
- the retained first-root continuation re-entry remains ancestry context only.

A later rollover therefore dispatches through the ordinary governed-session rollover path. It cannot manufacture a first-root 35E checkpoint from historical ancestry.

## Inspection behavior

The existing 45A projection already separates immutable launch provenance from mutable current governed state.

Inspectable persisted 35D/35E and raw 36D continuation shells now inherit the 46D product shell.

On adoption:

- `launch_provenance` remains the exact same object;
- only `current_state` advances from the adopted controller;
- persisted launch location remains context only;
- raw 36D launch location remains `None`;
- no second-epoch path or overlay is invented.

No inspection schema change is required.

## Prior art / reuse

46D reuses:

- 44E / D222 for the first-root declaration/adoption product pattern;
- existing root-started sequence load, declaration persistence, and declaration-load boundaries;
- the standard governed controller;
- 37A's established second-root declared-segment shape;
- 45A / D226 generic controller projection for mutable current governed state.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Focused falsification

Coverage proves:

- exact 46C result type is required;
- exact second root and edge identities are retained;
- moved durable edge works only through the explicit supplied path;
- wrong edge locator rejects before declaration write;
- adoption controls appear only after exact 46C success and begin blank;
- declaration construction does not mutate mounted one-root state;
- explicit promotion replaces active governed state with the exact adopted controller;
- changed-basis candidate authority is cleared;
- post-adoption rollover mounts no historical first-root 35E checkpoint;
- persisted and raw 45A launch provenance remains object-identical while current state advances.

## Non-goals

46D does not add:

- second-epoch fresh-process re-entry;
- second-epoch persisted overlay;
- CLI locators;
- a new persistence format;
- a new inspection schema;
- generic Nth-root/adoption/epoch machinery;
- a fourth epoch;
- discovery, prefill, current/latest/head/chronology authority;
- path identity;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- browser reacquisition;
- autonomous research behavior.

## Acceptance

Acceptance requires the exact final PR head to pass Repository Zero on Python 3.11, 3.12, 3.13, and 3.14. Any red result must be treated as evidence and corrected only at the demonstrated boundary before merge.
