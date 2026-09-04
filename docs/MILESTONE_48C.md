# Milestone 48C — bounded changed-basis proof-to-persistence mount mechanics

Decision: **D244**  
Issue: **#210**

## Purpose

48C is a refactor milestone.

Three complete changed-basis product crossings independently proved the same Textual transition from one newly retained fresh reconstruction proof into one explicit restart-persistence form:

```text
44F fresh 35B proof → 44G 35C persistence controls
46E fresh 37A proof → 46F 37B persistence controls
47E fresh 40A proof → 47F 40B persistence controls
```

48C privately shares only that mount procedure.

It does not share reconstruction, persistence, path, ancestry, or result semantics.

## Triply-proven procedure

Before 48C, each concrete product performed the same sequence after its inherited verification action:

```text
retain previous verification object
→ run concrete inherited verification
→ read current retained verification object

current is None
or current is previous exact object
→ stop

new exact verification
→ reject existing concrete persistence controls
→ construct concrete controls with exact verification
→ mount controls
```

The three families already had independent behavioral coverage for this gate.

That repetition meets the three-family threshold previously used by Milestones 43A–43E and 48A–48B.

## Private helper

48C adds:

```text
src/pyxis/ui/chromium_research_changed_basis_restart_persistence_textual.py
```

The module exposes no public authority surface:

```python
__all__: list[str] = []
```

Its private objects are:

```python
_ChangedBasisRestartPersistenceMountSpec

_mount_changed_basis_restart_persistence_after_new_verification(...)
```

## Mount spec

The private spec contains only two concrete surface facts:

```text
controls_selector
duplicate_controls_error
```

It contains no persistence format, path, root count, milestone semantics, or result type.

The concrete products retain their existing values.

### 44G

```text
controls:
#research-first-changed-basis-root-backed-reentry-overlay-controls

duplicate error:
44G overlay persistence controls are already mounted.
```

### 46F

```text
controls:
#research-second-changed-basis-epoch-reentry-overlay-controls

duplicate error:
Second-basis re-entry overlay controls are already mounted.
```

### 47F

```text
controls:
#research-third-changed-basis-epoch-reentry-overlay-controls

duplicate error:
Third-basis re-entry overlay controls are already mounted.
```

## Exact-object gate

The helper compares only object identity:

```python
current_verification is previous_verification
```

It never uses structural or value equality as a substitute for one newly retained proof result.

When a new verification exists, the exact same object is passed directly to the concrete controls constructor.

No reconstruction, reload, wrapper, copy, or equality substitution occurs.

## Concrete verification stays concrete

Each product still performs its own inherited verification call.

### 44G

```python
await super()._verify_research_first_changed_basis_root_backed_reentry()
```

The concrete retained field remains:

```python
last_first_changed_basis_root_backed_reentry_verification
```

### 46F

```python
await super()._verify_second_changed_basis_epoch_reentry()
```

The concrete retained field remains:

```python
last_second_changed_basis_epoch_reentry_verification
```

### 47F

```python
await super()._verify_third_changed_basis_epoch_reentry()
```

The concrete retained field remains:

```python
last_third_changed_basis_epoch_reentry_verification
```

48C never invokes or interprets those verification functions.

## Concrete controls stay concrete

Each caller supplies its established constructor:

```text
44G → ResearchFirstChangedBasisRootBackedReentryOverlayControls
46F → ResearchSecondChangedBasisEpochReentryOverlayControls
47F → ResearchThirdChangedBasisEpochReentryOverlayControls
```

Those controls retain their existing:

- verification type checks;
- authority notices;
- summaries;
- blank path inputs;
- button IDs and labels;
- success receipts;
- post-success locking rules.

48C does not create a generic restart-overlay form.

## Persistence remains completely outside 48C

The helper runs before any persistence attempt.

It knows nothing about:

```text
35C root-backed restart overlay
37B second-basis restart overlay
40B third-basis restart overlay
```

It does not read:

- prior-plan paths;
- prior continuation-overlay paths;
- destinations;
- persistence results;
- checkpoint results;
- launch provenance.

The concrete save handlers remain unchanged by this milestone.

## Focused falsification

48C adds focused tests proving:

1. the private helper module exports no public API;
2. `None` current verification mounts nothing;
3. an object-identical previous/current verification mounts nothing;
4. the no-new-result paths never call the controls factory;
5. duplicate controls reject before controls construction;
6. a newly retained exact verification reaches the controls factory by object identity;
7. the exact created controls object is mounted and returned;
8. 44G, 46F, and 47F all import the same private helper;
9. all three retain their exact selectors and duplicate-control wording.

The mature 44G, 46F, and 47F suites remain the stronger end-to-end behavioral authority.

## Compatibility

48C changes no:

- 35B, 37A, or 40A verification;
- verification result type;
- controls class;
- visible wording;
- path input;
- persistence function;
- persistence result type;
- persistence format;
- mounted-state preservation;
- typed handoff;
- runner;
- inspection;
- CLI;
- browser behavior.

## Non-goals

48C adds no:

- persistence abstraction;
- explicit-path collection abstraction;
- save-handler abstraction;
- result-proof abstraction;
- generic restart-persistence controls;
- generic changed-basis superclass;
- fourth evidence-basis epoch;
- generic `epoch[n]`;
- ancestry traversal;
- locator discovery or prefill;
- path promotion;
- global current/latest/head authority;
- chronology or branch authority;
- authorship/authenticity/trusted-time authority;
- semantic-support or citation authority;
- autonomous research behavior.

## Architectural result

The post-proof changed-basis product path now has three bounded private reuse seams:

```text
CONCRETE 44F / 46E / 47E FRESH PROOF
        ↓
48C private proof-to-persistence mount mechanics
        ↓
CONCRETE 44G / 46F / 47F persistence
        ↓
48A private typed-handoff surface mechanics
        ↓
CONCRETE shell.exit
        ↓
48B private typed-handoff runner mechanics
        ↓
CONCRETE receiver
```

At every seam, concrete ancestry and persistence authority remain outside the helper.

## Acceptance statement

48C permits only this statement:

> After three concrete changed-basis products independently demonstrated the same newly-retained-proof gate and persistence-controls mount procedure, Pyxis may share that procedure privately while keeping verification, control typing, persistence, paths, ancestry, and all public product semantics concrete.
