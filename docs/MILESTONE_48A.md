# Milestone 48A — bounded changed-basis typed-handoff mechanics

Decision: **D242**  
Issue: **#206**

## Purpose

48A is a refactor milestone.

It extracts only the post-persistence Textual handoff procedure that has now been independently demonstrated by all three complete changed-basis product crossings:

```text
44H — first changed basis → root-backed product
46G — second changed basis → second-basis-epoch product
47G — third changed basis → third-basis-epoch product
```

No new research authority, ancestry model, persistence behavior, receiver, runner, or evidence-basis epoch is added.

## Why extraction is justified now

Before 47G, the changed-basis handoff mechanics had not yet crossed the repository's established three-family reuse threshold.

After 47G, three concrete products independently prove the same procedure:

```text
concrete persistence succeeds
→ exact retained persistence result changes
→ exact checkpoint.fresh_reentry selected
→ concrete family validates exact handoff type
→ duplicate handoff controls forbidden
→ concrete notice mounted
→ concrete explicit button mounted
→ persistence alone still does not promote mode
→ button press revalidates exact retained result
→ shell exits with exact checkpoint.fresh_reentry
```

The ancestry semantics remain different.

The surface procedure does not.

That is the same architectural distinction that justified the bounded 43A–43E cumulative extractions.

## Private helper

48A adds:

```text
src/pyxis/ui/chromium_research_changed_basis_typed_handoff_textual.py
```

The module exports no public authority surface:

```python
__all__: list[str] = []
```

Its private objects are:

```python
_ChangedBasisTypedHandoffSurfaceSpec

_require_changed_basis_checkpoint_fresh_handoff(...)

_mount_changed_basis_typed_handoff_after_new_persistence(...)
```

## Shared mechanics

### Exact checkpoint fresh-result extraction

`_require_changed_basis_checkpoint_fresh_handoff(...)` receives:

- one concrete retained persistence result selected by the caller;
- one concrete surface spec;
- one concrete validation callback.

It performs only:

```text
result must exist
→ handoff = result.checkpoint.fresh_reentry
→ concrete validator must accept handoff
→ return same exact object
```

The helper does not know which concrete result type owns the checkpoint.

It does not select a shell attribute.

It does not infer a receiver.

It does not exit the app.

### New-result gate and control mounting

`_mount_changed_basis_typed_handoff_after_new_persistence(...)` receives the concrete previous and current persistence-result objects.

It performs only:

```text
no current result → no handoff surface
same retained result object → no new handoff surface
new retained result
→ exact checkpoint fresh result validation
→ reject duplicate concrete notice
→ mount concrete notice
→ mount concrete primary button
```

It returns the exact handoff object only as mechanical evidence to the concrete caller.

The concrete shell remains responsible for whether that return value is used.

## Concrete surface specs

Each family keeps one private concrete spec containing only visible/error details already established by that family.

### 44H

The first crossing retains:

- button ID `continue-first-changed-basis-root-backed-session`;
- notice ID `research-first-changed-basis-root-backed-handoff-notice`;
- exact 44G/44H notice wording;
- button label `Continue with verified changed-basis session`;
- exact missing-result error;
- exact invalid-root-backed-result error;
- exact duplicate-control error.

Its validator remains:

```python
isinstance(value, ChromiumResearchRootBackedSessionReentryResult)
```

48A does not strengthen that established rule to exact type equality.

### 46G

The second crossing retains:

- button ID `continue-second-changed-basis-epoch-session`;
- notice ID `research-second-changed-basis-epoch-handoff-notice`;
- exact 46F/46G notice wording;
- button label `Continue with verified second-basis-epoch session`;
- exact existing errors.

Its validator remains:

```python
type(value) is ChromiumResearchSecondBasisEpochReentryResult
```

### 47G

The third crossing retains:

- button ID `continue-third-changed-basis-epoch-session`;
- notice ID `research-third-changed-basis-epoch-handoff-notice`;
- exact 47F/47G notice wording;
- button label `Continue with verified third-basis-epoch session`;
- exact existing errors.

Its validator remains:

```python
type(value) is ChromiumResearchThirdBasisEpochReentryResult
```

## Concrete orchestration remains concrete

48A deliberately leaves these methods inside their existing product modules:

```text
44H
_persist_research_first_changed_basis_root_backed_reentry_overlay

46G
_persist_second_changed_basis_epoch_reentry_overlay

47G
_persist_third_changed_basis_epoch_reentry_overlay
```

Each method still:

1. selects its own exact retained result attribute;
2. invokes its own inherited persistence action;
3. selects that attribute again;
4. delegates only the new-result gate and visible handoff-mount mechanics.

Likewise, each concrete `on_button_pressed` still:

1. owns its exact concrete button ID;
2. selects its exact retained persistence result;
3. delegates only checkpoint-fresh extraction/type validation;
4. calls `self.exit(handoff)` itself.

The private helper therefore never becomes a mode-changing authority surface.

## Why persistence stays concrete

The persistence operations remain materially different:

```text
44G → public 35C root-backed restart overlay
46F → public 37B second-basis restart overlay
47F → public 40B third-basis restart overlay
```

Their locators, result types, ancestry proofs, mounted-state invariants, and persistence formats remain concrete.

48A does not extract any of that orchestration.

## Why runners stay concrete

The three handoff runners also share an apparent shape:

```text
run concrete source shell
→ None or concrete typed result
→ validate
→ run concrete receiver
```

48A leaves them untouched.

Their source-factory signatures and receiver products differ, and runner extraction is not needed to earn the UI reuse implemented here.

A later refactor may consider that repetition only if it can remain useful without obscuring source and receiver authority.

## Textual dispatch remains unchanged

44H, 46G, and 47G continue to own only their exact handoff button events.

They do not manually invoke parent `on_button_pressed` handlers for inherited actions.

Textual MRO dispatch therefore remains unchanged and the earlier duplicate-action defect remains guarded against.

## Focused falsification

48A adds focused kernel tests that prove:

- the helper module exports no public authority API;
- exact `checkpoint.fresh_reentry` object identity is preserved;
- missing retained persistence rejects with concrete wording;
- concrete validator failure rejects before mount;
- identical previous/current result objects mount nothing;
- a newly retained valid result mounts exactly one concrete `Static` notice and one primary `Button`;
- concrete notice/button IDs and labels are retained;
- duplicate notice state rejects before new widgets are mounted;
- all three concrete modules import the same private kernel procedures;
- the established 44H/46G/47G surface contracts remain concrete.

The mature existing 44H, 46G, and 47G suites remain the stronger behavioral regression authority for full end-to-end product handoff.

## Compatibility

48A changes no:

- public application function;
- public result dataclass;
- persistence format;
- persistence function;
- fresh reconstruction;
- checkpoint proof;
- receiver product;
- runner signature;
- launch-lineage type;
- inspection schema;
- CLI flag;
- browser behavior;
- concrete DOM ID;
- concrete button label;
- concrete notice wording;
- concrete established type-validation rule.

## Non-goals

48A adds no:

- fourth evidence-basis crossing;
- generic `epoch[n]`;
- arbitrary-depth ancestry;
- generic changed-basis superclass;
- persistence abstraction;
- reconstruction abstraction;
- runner abstraction;
- receiver abstraction;
- generic launch lineage;
- generic inspection ancestry;
- locator discovery or prefill;
- path promotion;
- global current/latest/head authority;
- chronology or branch authority;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.

## Architectural result

The boundary is intentionally asymmetric:

```text
CONCRETE CHANGED-BASIS AUTHORITY
44H / 46G / 47G modules
        ↓
concrete validator + surface spec
        ↓
PRIVATE SHARED TEXTUAL PROCEDURE
changed-basis typed handoff mechanics
        ↓
CONCRETE shell.exit + runner + receiver
```

The helper knows nothing about root count or evidence-basis ancestry.

That is the point.

## Acceptance statement

48A permits only this statement:

> After three concrete changed-basis product families independently demonstrated the same post-persistence typed-handoff surface procedure, Pyxis may share that procedure privately while keeping all persistence, ancestry, result typing, exit authority, runner orchestration, receiver selection, and public product semantics concrete.
