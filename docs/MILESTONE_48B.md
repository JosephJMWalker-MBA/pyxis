# Milestone 48B — bounded changed-basis typed-handoff runner mechanics

Decision: **D243**  
Issue: **#208**

## Purpose

48B is a refactor milestone.

48A / D242 extracted only the repeated post-persistence Textual handoff surface mechanics shared by 44H, 46G, and 47G.

A second independently demonstrated repetition remained in the three public product runners:

```text
run concrete source shell
→ None: stop
→ validate concrete typed result
→ create concrete inspectable receiver
→ receiver.run()
→ return same exact handoff object
```

48B privately shares only that procedure.

No new research authority, persistence behavior, receiver product, public runner, or evidence-basis epoch is added.

## Triply-proven basis

The exact runner pattern already existed independently in:

```text
44H
ordinary changed-basis source
→ exact root-backed handoff
→ inspectable root-backed receiver

46G
one-root changed-basis source
→ exact second-basis handoff
→ inspectable second-basis receiver

47G
second-epoch changed-basis source
→ exact third-basis handoff
→ inspectable third-basis receiver
```

Their source signatures and authority semantics differ.

Their orchestration procedure does not.

This satisfies the same three-family reuse threshold used by the bounded 43-series and by 48A.

## Private runner helper

48B adds:

```text
src/pyxis/ui/chromium_research_changed_basis_typed_handoff_runner.py
```

Its only private procedure is:

```python
_run_changed_basis_typed_handoff(
    *,
    run_source,
    validate_handoff,
    invalid_handoff_error,
    create_receiver,
)
```

and the module exports no public authority API:

```python
__all__: list[str] = []
```

## Exact procedure

The helper executes only:

```text
handoff = run_source()

handoff is None
→ return None
→ receiver factory is never called

handoff exists
→ caller-owned validator must accept
→ otherwise raise caller-owned TypeError before receiver construction

valid handoff
→ create_receiver(handoff)
→ receiver.run()
→ return handoff
```

The exact source-returned object is passed to the concrete receiver by object identity and is returned unchanged.

No copy, wrapper, reconstruction, equality substitution, disk reload, or path lookup occurs.

## Concrete source construction stays concrete

48B deliberately does not pass source-factory arguments through the helper.

Each public runner still constructs its own source first.

### 44H

```python
source = create_first_changed_basis_root_backed_handoff_research_session_shell(
    ordinary_reentry,
    appended_items,
)
```

### 46G

```python
source = create_second_changed_basis_epoch_handoff_research_session_shell(
    reentry,
    appended_items,
)
```

### 47G

```python
source = create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
    lineage,
    appended_items,
)
```

Those factories retain their existing concrete input authority.

The helper sees only `source.run`.

## Concrete validation stays concrete

48B reuses the family validators established by 48A.

### 44H

```python
isinstance(value, ChromiumResearchRootBackedSessionReentryResult)
```

with existing runner error:

```text
44H shell returned an invalid root-backed handoff result.
```

### 46G

```python
type(value) is ChromiumResearchSecondBasisEpochReentryResult
```

with existing runner error:

```text
46G shell returned an invalid second-basis-epoch handoff result.
```

### 47G

```python
type(value) is ChromiumResearchThirdBasisEpochReentryResult
```

with existing runner error:

```text
47G shell returned an invalid third-basis-epoch handoff result.
```

48B does not normalize those rules.

## Concrete receiver selection stays concrete

Each runner still supplies its established inspectable receiver factory:

```text
44H → create_inspectable_root_backed_handoff_research_session_shell
46G → create_inspectable_second_basis_epoch_handoff_research_session_shell
47G → create_inspectable_third_basis_epoch_handoff_research_session_shell
```

The helper does not import or know any of those receiver classes.

It only invokes the caller-supplied factory with the exact handoff object and then calls `.run()` on the returned receiver.

## Public API remains unchanged

The public runner names, signatures, annotations, and roles remain:

```python
run_first_changed_basis_root_backed_handoff_research_session_shell(...)

run_second_changed_basis_epoch_handoff_research_session_shell(...)

run_third_changed_basis_epoch_handoff_research_session_shell(...)
```

48B adds no public generic runner.

## Failure ordering remains explicit

The established runner order is preserved:

1. concrete source construction occurs in the public runner;
2. source shell runs;
3. `None` returns immediately;
4. a non-`None` invalid result raises before receiver construction;
5. a valid result reaches the receiver by exact object identity;
6. receiver runs exactly once;
7. the same exact result object is returned.

This matters because invalid or absent handoff authority must never cause receiver launch.

## Focused falsification

48B adds focused tests proving:

- the private runner module exports no public API;
- normal close constructs no receiver;
- invalid results reject before receiver construction;
- caller-owned error text remains authoritative;
- valid handoff reaches the receiver factory by exact object identity;
- receiver `.run()` executes once;
- the helper returns the same exact handoff object;
- all three concrete modules delegate to the same private procedure;
- concrete validators remain distinct functions.

The mature 44H, 46G, and 47G runner tests remain the stronger end-to-end regression authority.

## Compatibility

48B changes no:

- changed-basis source factory;
- source-shell behavior;
- public runner signature;
- public return annotation;
- concrete result type;
- concrete validator;
- receiver factory;
- receiver behavior;
- launch provenance;
- persistence/reconstruction;
- CLI behavior;
- browser behavior.

## Non-goals

48B adds no:

- fourth evidence-basis crossing;
- generic `epoch[n]`;
- source-factory abstraction;
- receiver abstraction;
- public generic runner;
- generic changed-basis superclass;
- persistence abstraction;
- ancestry abstraction;
- path discovery or promotion;
- CLI routing change;
- automatic mode promotion;
- current/latest/head inference;
- chronology or branch authority;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.

## Architectural result

The changed-basis handoff stack is now:

```text
CONCRETE 44H / 46G / 47G PRODUCT AUTHORITY
        ↓
48A private Textual handoff surface mechanics
        ↓
concrete shell.exit exact typed result
        ↓
48B private runner orchestration mechanics
        ↓
CONCRETE inspectable receiver
```

Concrete ancestry semantics remain outside both private helpers.

## Acceptance statement

48B permits only this statement:

> After three concrete changed-basis product runners independently demonstrated the same normal-close, concrete-validation, receiver-run, and exact-object-return procedure, Pyxis may share that procedure privately while keeping source construction, validation semantics, receiver selection, public APIs, ancestry meaning, and all persistence authority concrete.
