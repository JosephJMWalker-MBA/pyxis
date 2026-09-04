# Milestone 48D — bounded changed-basis restart-persistence path submission

Decision: **D245**  
Issue: **#212**

## Purpose

48D is a refactor milestone.

Three complete changed-basis restart-persistence products independently proved the same
two-field path submission mechanics:

```text
44G
explicit ordinary 31B plan source
+ explicit no-overwrite 35C destination

46F
explicit current 35D/35E continuation-overlay source
+ explicit no-overwrite 37B destination

47F
explicit current 37C/37D second-epoch continuation-overlay source
+ explicit no-overwrite 40B destination
```

48D privately shares only:

```text
read both exact input values
→ source blank check first
→ destination blank check second
→ Path(exact original source value)
→ Path(exact original destination value)
→ return two concrete paths to caller
```

No persistence, path discovery, normalization, ancestry, or authority semantics move into
the helper.

## Prior-art basis

The repository already established this exact reuse boundary in 43E / D217 for cumulative
continuation checkpoint forms:

> share only ordered path reading, blank validation, and exact Path conversion after three
> concrete families independently demonstrate the same procedure.

48D applies that rule to the three changed-basis restart-persistence products.

A broader path-form framework would be larger than the repeated procedure and would risk
hiding path meaning. Internal bounded extraction remains the smaller reuse boundary.

**No end-to-end substitute demonstrated in this review.**

## Private path specification

48D extends:

```text
src/pyxis/ui/chromium_research_changed_basis_restart_persistence_textual.py
```

with:

```python
_ChangedBasisRestartPersistencePathSpec(
    source_selector,
    destination_selector,
    missing_source_error,
    missing_destination_error,
)
```

The spec contains only concrete selectors and existing concrete blank-error wording.

It contains no:

- path meaning;
- root count;
- milestone meaning;
- persistence type;
- persistence keyword;
- persistence format;
- reconstruction rule.

The module still exports no public API.

## Private path submission

48D also adds:

```python
_ChangedBasisRestartPersistencePathSubmission(
    source: Path,
    destination: Path,
)
```

and:

```python
_collect_changed_basis_restart_persistence_path_submission(...)
```

The helper queries both concrete selectors as Textual `Input` widgets and preserves
the existing validation order.

## Ordered blank validation

The procedure remains:

```text
query source
query destination

source.value.strip() is empty
→ update concrete status with concrete source error
→ return None

destination.value.strip() is empty
→ update concrete status with concrete destination error
→ return None

otherwise
→ return exact Path conversion for both values
```

A blank source therefore wins over an also-blank destination exactly as before.

Whitespace-only values remain blank.

## Exact entered-value rule

`.strip()` is used only as the blank predicate.

Successful conversion uses:

```python
Path(source.value)
Path(destination.value)
```

not:

```python
Path(source.value.strip())
Path(destination.value.strip())
```

The helper therefore does not:

- trim;
- normalize;
- resolve;
- canonicalize;
- discover;
- compare;
- reinterpret;
- infer path identity.

If the caller enters leading or trailing spaces in a nonblank path, those exact characters
remain part of the `Path` value supplied to concrete persistence.

## Concrete 44G path semantics remain concrete

44G retains this exact mapping:

```text
source selector:
#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source

source meaning:
explicit ordinary 31B plan-document path

destination selector:
#research-first-changed-basis-root-backed-reentry-overlay-destination

destination meaning:
explicit no-overwrite 35C overlay destination
```

The concrete save handler still calls:

```python
persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
    verification,
    prior_session_plan_source=paths.source,
    destination=paths.destination,
)
```

The helper does not know the `prior_session_plan_source` keyword.

## Concrete 46F path semantics remain concrete

46F retains:

```text
source selector:
#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source

source meaning:
explicit current 35D/35E continuation-overlay path

destination selector:
#research-second-changed-basis-epoch-reentry-overlay-destination

destination meaning:
explicit no-overwrite 37B destination
```

The concrete save handler still maps:

```python
prior_root_backed_continuation_overlay_source=paths.source
destination=paths.destination
```

The helper does not know first-root continuation ancestry.

## Concrete 47F path semantics remain concrete

47F retains:

```text
source selector:
#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source

source meaning:
explicit current 37C/37D second-epoch continuation-overlay path

destination selector:
#research-third-changed-basis-epoch-reentry-overlay-destination

destination meaning:
explicit no-overwrite 40B destination
```

The concrete save handler still maps:

```python
prior_second_basis_epoch_continuation_overlay_source=paths.source
destination=paths.destination
```

The helper does not know second-epoch continuation ancestry.

## Persistence authority remains outside 48D

All three concrete handlers continue to own:

1. controls lookup;
2. exact verification/form ownership check;
3. concrete status surface;
4. mounted governed-state snapshot;
5. retained historical continuation snapshot where applicable;
6. exact persistence function;
7. exact persistence keyword mapping;
8. concrete exception handling;
9. proof that the result retains the exact verification;
10. mounted-state preservation proof;
11. concrete retained result field;
12. concrete controls locking and success receipt.

48D therefore does not become a save-handler abstraction.

## Existing no-overwrite behavior remains concrete

The destination path is only collected.

No overwrite check is added to the helper.

35C, 37B, and 40B continue to own their respective no-overwrite persistence behavior.

The helper does not touch the filesystem.

## Focused falsification

48D adds focused tests proving:

1. the private module still exports no public authority API;
2. whitespace-only source is blank;
3. source blank failure occurs before destination failure;
4. destination blank failure occurs only after a nonblank source;
5. successful collection returns `Path` objects from the exact unstripped entered strings;
6. the status surface remains unchanged on successful collection;
7. all three concrete persistence modules import the same private collector;
8. all three retain their exact selectors and existing blank-error wording.

The mature 44G, 46F, and 47F UI suites remain the stronger end-to-end proof that each
returned path reaches its established concrete persistence keyword and produces the same
persistence semantics.

## Compatibility

48D changes no:

- Textual input ID;
- input placeholder;
- blank-validation order;
- blank-error wording;
- successful `Path` conversion behavior;
- verification result;
- persistence function;
- persistence keyword meaning;
- persistence format;
- no-overwrite behavior;
- result-retention proof;
- mounted-state proof;
- handoff;
- runner;
- receiver;
- inspection;
- CLI;
- browser behavior.

## Non-goals

48D adds no:

- path discovery;
- path prefilling;
- path normalization;
- path resolution;
- path identity;
- generic path form;
- persistence abstraction;
- save-handler abstraction;
- result-proof abstraction;
- mounted-state abstraction;
- generic restart-overlay model;
- generic changed-basis superclass;
- fourth evidence-basis epoch;
- generic `epoch[n]`;
- ancestry traversal;
- current/latest/head inference;
- chronology or branch authority;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.

## Architectural result

The changed-basis proof/persistence/handoff path now contains four bounded private
mechanical seams:

```text
CONCRETE 44F / 46E / 47E FRESH PROOF
        ↓
48C private new-proof → persistence-controls mount
        ↓
48D private explicit two-path submission
        ↓
CONCRETE 44G / 46F / 47F persistence + proof
        ↓
48A private typed-handoff surface mechanics
        ↓
CONCRETE shell.exit
        ↓
48B private handoff runner mechanics
        ↓
CONCRETE receiver
```

Concrete authority remains on both sides of every helper.

## Acceptance statement

48D permits only this statement:

> After three concrete changed-basis restart-persistence products independently
> demonstrated the same two-input reading, ordered blank validation, and exact
> `Path` conversion procedure, Pyxis may share that procedure privately while
> keeping all path meaning, persistence, proof, ancestry, mounted-state invariants,
> and public product semantics concrete.
