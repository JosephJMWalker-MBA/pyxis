# Milestone 43B — bounded cumulative checkpoint Textual kernel

## Decision D214

Milestones 36C, 38E, and 41D independently proved the same cumulative-checkpoint **form mechanics** above three different concrete continuation families.

43B extracts only those triply-proven Textual mechanics into one private UI-layer kernel.

It does **not** generalize root/epoch ancestry, checkpoint persistence, shell promotion, or cumulative handoff authority.

This is a refactor milestone, not a new authority milestone.

## Frontier review

43A deliberately ended by re-reviewing the frontier instead of assuming a fourth evidence-basis epoch.

Two plausible reuse candidates were compared.

### Explicit cumulative handoff — not extracted

36D, 38F, and 41E share an important authority rule:

```text
successful first checkpoint
!= automatic mode transition

explicit Continue in cumulative mode
→ exact checkpoint.fresh_reentry only
```

But the constructor semantics are not actually triply identical.

The root-backed cumulative shell already accepts the exact typed continuation re-entry directly for both persisted and in-process entry. Second- and third-epoch persisted continuation shells instead require their concrete launch-lineage wrappers, so 38F and 41E needed distinct raw handoff shells that deliberately bypass those persisted-launch constructors.

Collapsing those differences now would risk turning a shared authority principle into a false shared constructor model.

43B therefore leaves cumulative handoff untouched.

### Cumulative checkpoint forms — extracted

The form mechanics are independently identical in 36C / D188, 38E / D198, and 41D / D209:

```text
exact typed current continuation
+ exact explicit rollover
        ↓
revision remains locked
        ↓
four blank explicit path roles
        ↓
concrete persistence/proof owned by shell
        ↓
exact current-reentry identity retained
+ exact rollover identity retained
        ↓
old form disables inputs + save button
+ displays concrete success receipt
        ↓
concrete shell owns visible promotion
```

Those mechanics are the 43B extraction boundary.

## Private kernel

43B adds:

```text
src/pyxis/ui/chromium_research_cumulative_checkpoint_textual.py
```

Its private surface contains:

```text
_CumulativeCheckpointTextualSpec
_CumulativeCheckpointTextualControls
```

and exports nothing through `__all__`.

The private base owns only:

1. composition of the established title / authority notice / candidate receipt surface;
2. composition of exactly four initially blank `Input` widgets;
3. composition of one save button and one pending-status surface;
4. exact current-reentry object identity comparison after a concrete result is supplied;
5. exact rollover object identity comparison;
6. disabling those four old inputs and the old save button after success;
7. replacing the old status text with the concrete family's supplied success receipt.

The base knows no root count, evidence-basis epoch, milestone number, durable format, anchor field, persistence API, or ancestry proof.

## Concrete authority remains concrete

The existing public controls remain the caller-facing types:

```text
RootBackedResearchSessionCumulativeCheckpointControls
SecondBasisEpochResearchSessionCumulativeCheckpointControls
ThirdBasisEpochResearchSessionCumulativeCheckpointControls
```

Each concrete module still owns:

- its exact current re-entry type check;
- its exact result type check;
- its exact rollover type check;
- all DOM IDs and selectors;
- all labels and placeholders;
- its authority notice;
- its candidate receipt;
- its success receipt;
- its exact error wording;
- its root/epoch terminology.

No shell imports or selectors need to change.

## What does not move

43B deliberately does not move any shell behavior.

The root-backed, second-epoch, and third-epoch cumulative shells still own:

- reading the four explicit paths;
- calling their concrete application persistence boundary;
- root/epoch ancestry verification;
- terminal SHA/text verification;
- failure-state retention;
- cumulative controller promotion;
- clearing one-hop rollover state;
- revision unlocking after visible promotion.

The 43A application kernel and the 43B Textual kernel therefore solve two different proven repetitions:

```text
43A
application-layer cumulative extension mechanics

43B
UI-layer cumulative checkpoint form mechanics
```

Neither claims generic ancestry semantics.

## Falsifiability

43B adds focused structural coverage proving that:

- all three public controls subclass the same private Textual mechanical base;
- all three use the private compose implementation;
- all three concrete `lock_after_success` methods delegate result handling to the private lock mechanic while supplying their concrete result type and concrete error wording;
- every concrete form specification still contains exactly four distinct explicit path roles;
- the shared module exports no public authority surface.

The mature 36C, 38E, and 41D interaction suites remain the behavioral regression authority. They continue to prove the real mounted controls, blank inputs, selectors, persistence flows, failure locking, receipts, visible promotion, and repeatable cycles.

## Preserved non-authorities

43B adds no authority to infer or select:

- a current overlay path;
- a successor edge path;
- a declaration destination;
- an overlay destination;
- latest/current/head state;
- chronology or branch meaning;
- path identity;
- authorship or authenticity;
- trusted time;
- semantic support or citation authority.

All four durable locations remain explicit user-supplied operational context each cycle.

## Not generalized

43B does not add:

- a fourth evidence-basis epoch;
- `epoch[n]`;
- arbitrary-depth ancestry;
- a generic root/epoch schema;
- a generic checkpoint persistence API;
- generic shell lineage;
- a generic cumulative handoff constructor;
- a shell-promotion kernel;
- a new durable format;
- CLI behavior;
- browser or evidence behavior.

## Result

The implementation now reuses two procedures that have each independently earned reuse:

```text
cumulative persistence mechanics  → private 43A application kernel
cumulative form mechanics         → private 43B Textual kernel
```

while preserving the concrete authority models that make the root-backed, second-epoch, and third-epoch families meaningfully different.
