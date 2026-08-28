# Milestone 44B — Explicit first changed-basis transition surface

Decision: **D219**

## Product boundary

44A proved that a researcher can prepare a changed evidence basis without adopting it.

44B exposes the next already-proven authority boundary, 33B / D178, only for the first basis crossing from ordinary pre-root lineage.

```text
ordinary 31A re-entry
+ successful 44A / 33A prepared changed basis
+ explicit durable locators
→ explicit 33B cross-working-set transition
→ canonical no-overwrite transition record
→ fresh explicit 33B relink
```

44B stops there.

It does not create the 34A first revision root and does not construct a 35A root-backed declared session.

## Why ordinary 31A re-entry is required

The product needs a concrete reason to know that this is the first evidence-basis crossing rather than an arbitrary later transition.

`ChromiumResearchSessionReentryResult` is that reason.

The ordinary 31A re-entry schema can reconstruct only the established pre-root continuation/ordinary-edge lineage. Root-backed ancestry and later evidence-basis families use distinct typed re-entry products.

44B therefore requires the exact ordinary re-entry family rather than inferring eligibility from:

- shell class names;
- path names;
- file locations;
- sequence length;
- timestamps;
- revision counts;
- root counts;
- generic `epoch[n]` state.

This preserves the rule:

```text
mechanical similarity to a later basis crossing
!=
product authority to expose a generic transition-again action
```

## Concrete shell instead of base-shell widening

The frontier review initially considered adding a conditional hook to `ResearchSessionShell`.

Implementation review found a stronger boundary: a dedicated
`FirstChangedBasisResearchSessionShell`.

The concrete shell:

1. requires an exact ordinary `ChromiumResearchSessionReentryResult` at construction;
2. uses that re-entry's governed controller;
3. configures inherited 44A candidate evidence explicitly;
4. inherits the mature 44A preparation UI;
5. mounts 44B transition controls only after 44A succeeds; and
6. never becomes a superclass of root-backed or later epoch shells.

Therefore no mature `ResearchSessionShell`, root-backed shell, second-epoch shell, or third-epoch shell implementation is modified by 44B.

## Bounded application result

44B adds:

```text
ChromiumResearchFirstChangedBasisTransitionResult
```

which retains:

- the exact mounted controller;
- the exact ordinary 31A re-entry;
- the exact successful 33A/44A preparation;
- the in-memory 33B transition;
- the durable 33B transition persistence evidence; and
- one fresh 33B loaded/relinked transition.

The application helper requires four explicit `Path` values:

```text
prior endpoint edge source
prepared working-set source
prepared working-set-note source
transition destination
```

No locator is copied automatically from the 44A receipt.

That deliberate repetition preserves moved-file support: a durable prepared file may move and still be accepted only when the caller explicitly supplies its new location and the existing 20C/21C/33B integrity relationships re-establish the same content identity.

## Visible transition state

Before transition persistence the UI shows:

```text
PREPARED CHANGED BASIS — NOT YET TRANSITIONED / NOT ROOTED
```

The 44A working-set and note identities plus their original output locations are shown as receipts only.

All four 44B locator inputs begin blank.

The UI does not prefill, discover, infer, scan, search, or remember a replacement locator.

## Successful transition remains outside the mounted session

A successful 44B save proves one explicit durable 33B transition and one fresh relink of it.

The receipt shows:

- transition SHA-256;
- transition destination;
- successor working-set SHA-256; and
- successor working-set-note SHA-256.

It also states that:

```text
transition persisted
!=
mounted governed session advanced
!=
revision root created
!=
root-backed session created
!=
epoch created
!=
current/latest/head selected
```

The exact mounted controller and session remain unchanged.

## Unadopted revision does not stale 44B

33B already proves that the controller's last successful 29A endpoint write is not prior-transition authority.

Therefore an unadopted endpoint revision may occur after 44A preparation without invalidating the 44B form.

The transition still starts from the exact declared endpoint retained by the prepared basis.

## Adopted rollover stales unsaved transition

A successful 30A rollover replaces the mounted governed controller.

The dedicated 44B shell intercepts that boundary and marks any unsaved transition form stale before delegating to the mature base rollover behavior.

The stale form is disabled and says that it will not silently retarget.

If a transition already succeeded, its receipt remains a historical truth and `mark_stale()` is intentionally a no-op.

## Why 44B does not create the first root

34A requires an additional explicit human-authored rationale revision over the changed working-set note.

35A then requires an ordinary edge after that root before a root-backed declared revision sequence can become a governed session controller.

Those are distinct human states:

```text
prepared rationale
→ explicit basis transition
→ first revised rationale after crossing
→ next ordinary rationale edge after root
→ declared root-backed governed session
```

A one-click product action would have to copy, invent, or silently reuse one or more of those rationale states.

44B refuses to manufacture human reasoning for product convenience.

## Prior art / reuse

Internal prior art is decisive for this product slice:

- 31A proves explicit ordinary pre-root re-entry;
- 33B proves the transition object, persistence format, and fresh explicit relinking;
- 44A proves candidate/prepared-basis presentation and staleness behavior;
- 29A/30A prove successful write is distinct from explicit session adoption;
- 34A and 35A prove why later root/session state must remain separate.

The broader external provenance review from the 43E/44A frontier remains applicable. 44B introduces no new provenance model, graph engine, browser subsystem, or persistence framework.

Conclusion: **no end-to-end substitute demonstrated in this review**.

## Falsifiability

Focused 44B coverage proves:

1. the application helper requires exactly `ChromiumResearchSessionReentryResult`;
2. the re-entry must describe the mounted controller presentation/declaration/endpoint;
3. the exact 44A preparation must belong to that controller and exact declared endpoint;
4. transition persistence delegates to the established 33B object and persistence boundaries;
5. the newly persisted transition is freshly loaded/relinked before success is returned;
6. explicit moved working-set/note files work only through supplied new paths;
7. the concrete shell mounts no transition controls before 44A succeeds;
8. successful 44A preparation mounts one 44B form;
9. all four transition locator inputs begin blank;
10. exact prepared working-set/note identities remain visible as receipts only;
11. successful transition locks the form;
12. successful transition leaves the mounted controller/session/declared endpoint unchanged;
13. an unadopted 29A write does not stale the 44B form;
14. a 30A rollover stales/disables an unsaved 44B form;
15. no 34A root or 35A adoption control is mounted; and
16. an ordinary 44A shell without the concrete 44B product surface never gains transition controls.

Existing 33B tests remain the deeper authority for transition-integrity failures and wrong durable inputs. Existing shell suites remain regression authority for mature product behavior.

## Non-authorities

44B adds no:

- 34A revision-root creation;
- 35A root-backed declared-session adoption;
- fourth evidence-basis epoch;
- generic `epoch[n]`;
- arbitrary-depth ancestry;
- generic transition-again product action;
- new transition format;
- new working-set/note format;
- locator discovery;
- digest search;
- CLI transition locator syntax;
- browser acquisition/navigation;
- chronology or branch authority;
- current/latest/head authority;
- path identity;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.

## Acceptance statement

If the complete supported test matrix succeeds, 44B permits only this statement:

> Pyxis can expose and durably persist the first explicit changed-evidence-basis transition from a concretely proven ordinary pre-root research lineage, freshly relink that transition from four caller-supplied durable locators, and keep the mounted governed session unchanged while refusing to manufacture the later revision-root or root-backed-session reasoning states.
