# Milestone 47G — explicit third-basis epoch typed handoff

Decision: **D241**  
Issue: **#203**

## Product boundary

47F / D240 persists strict 40B restart configuration for one exact historical 47E third-basis fresh-reentry proof.

47G keeps persistence and mode promotion separate:

```text
exact successful 47F persistence
+ explicit human handoff action
→ exact public-40B checkpoint.fresh_reentry
→ pathless third-basis-epoch first-checkpoint receiver
```

while:

```text
47F persistence
!= 47G promotion

saved 40B overlay path
!= 47G in-process launch provenance

47G typed handoff
!= fabricated persisted 41A shell lineage

47G launch
!= current/latest/head selection
```

The just-written 40B overlay remains durable restart configuration. The in-process handoff transfers the exact fresh typed result already earned by public 40B.

## Prior art and reuse

Internal precedent is decisive:

- 46G / D234 established the exact second-basis product seam: persistence and typed handoff are separate acts, and the handoff transfers the persistence gate's mandatory fresh result rather than reloading its saved overlay;
- 41E already proves pathless typed transfer for an established third-epoch continuation;
- `ThirdBasisEpochResearchSessionShell` already owns the first 40C continuation checkpoint boundary;
- `ChromiumResearchThirdBasisEpochShellLineage` remains reserved for an explicitly persisted 40B path that is freshly proved against earned state;
- third-epoch authority inspection already separates immutable launch provenance from mutable current state.

External review considered AWS Step Functions and Azure Durable Task / Durable Functions. They provide mature durable workflow state, restart/redrive, checkpointing, replay, and execution-history semantics. They do not replace this exact Pyxis authority seam: a human-explicit in-process transfer of one already-earned typed three-root result that deliberately refuses to derive launch provenance from a newly persisted restart-document path.

**No end-to-end substitute demonstrated in this review.**

## Narrow active-reentry refactor

Before 47G, the persisted initial third-epoch shell consumed the active typed launch only through:

```python
self.third_basis_epoch_launch_lineage.reentry
```

That made a pathless initial receiver impossible without inventing a fake persisted 41A lineage.

47G separates the two concepts:

```python
self.third_basis_epoch_launch_lineage = lineage
self.third_basis_epoch_reentry = lineage.reentry
```

The 40C checkpoint workflow now consumes:

```python
self.third_basis_epoch_reentry
```

For ordinary persisted 40B launches, both values still point to the same freshly proved launch authority. Persisted behavior is therefore unchanged.

## Pathless initial receiver

`ThirdBasisEpochHandoffResearchSessionShell` accepts exactly:

`ChromiumResearchThirdBasisEpochReentryResult`

It deliberately bypasses the persisted initial-shell constructor and starts with:

```text
third_basis_epoch_launch_lineage = None
third_basis_epoch_handoff_reentry = exact handoff
third_basis_epoch_reentry = exact handoff
last_third_basis_epoch_continuation_checkpoint = None
```

The mounted controller is the exact handed-off controller.

No 40B overlay source is loaded, stored, inferred, copied, or fabricated as launch provenance.

The receiver inherits the established first-checkpoint behavior. After an explicit ordinary rollover, the existing 40C checkpoint surface appears with all durable path fields blank:

- current 40B overlay source;
- successor edge source;
- continuation declaration source;
- no-overwrite 40C destination.

The researcher must supply every location again. Public 40C remains authoritative.

## Exact 47G authority subject

The source product exits only with:

```python
last_third_changed_basis_epoch_reentry_overlay.checkpoint.fresh_reentry
```

That object is the independent fresh 40A reconstruction earned inside public 40B during 47F.

It is deliberately **not**:

```python
last_third_changed_basis_epoch_reentry_verification.fresh_reentry
```

The earlier 47E result was the earned input to public 40B. The later public-40B `fresh_reentry` is the exact post-proof subject of the 47G handoff.

Python object identity is therefore part of the in-process product contract for this handoff seam.

## Explicit choice

Successful 47F persistence does not exit the changed-basis shell.

Only after one new exact 47F success does 47G mount:

- one negative-authority notice; and
- one explicit **Continue with verified third-basis-epoch session** action.

The currently mounted changed-basis session remains untouched until the researcher selects that action.

A failed 47F persistence attempt exposes no 47G handoff.

## Handoff survives loss of the saved locator document

After public 40B succeeds, the exact fresh typed result already exists in memory.

Therefore this sequence is valid:

```text
47F persists 40B overlay
→ public 40B returns exact fresh_reentry
→ saved 40B overlay file becomes unavailable
→ researcher explicitly chooses 47G handoff
→ exact retained fresh_reentry transfers in-process
```

47G does not reload the saved overlay.

The absence of that path after persistence affects later disk-based relaunch, not the already-earned in-process typed authority subject.

## Source families

47G provides dedicated product surfaces for both source families:

- persisted 37C/37D second-epoch continuation launch;
- raw pathless 38F second-epoch continuation handoff.

Inspectable variants remain available for both source families.

The 47G handoff itself is source-family independent because the transferred authority subject is the exact public-40B fresh third-epoch result.

## Runner

`run_third_changed_basis_epoch_handoff_research_session_shell(...)` chains only an explicit returned 47G result into the pathless inspectable third-basis-epoch receiver.

Normal close returns `None` and launches no receiver.

The runner:

- carries no 40B path;
- performs no disk re-entry;
- performs no shell-lineage proof;
- performs no branch selection;
- passes the exact typed result object to the receiver.

## Read-only 47G launch inspection

`inspect_chromium_research_third_basis_epoch_session_in_process_handoff(...)` projects the exact 47G launch without file I/O.

The launch projection records:

```text
launch family: in-process 47G typed third-basis-epoch handoff
launch location context: none
retained first-root SHA-256
retained second-root SHA-256
retained third-root SHA-256
exact launch endpoint SHA-256
```

The current-state projection begins as:

```text
state kind: third-basis-epoch session
state source: in-process 47G handoff
```

After an ordinary rollover, the immutable launch-provenance object remains object-identical. Only current governed state advances.

The displayed hashes remain integrity / record-identity anchors only. They establish no authorship, authenticity, trusted time, chronology, semantic support, or citation authority.

## Textual dispatch rule

47G owns only:

`continue-third-changed-basis-epoch-session`

For all inherited 47A–47F actions, its handler deliberately does not manually call a parent `on_button_pressed`.

Textual continues dispatch through the MRO. This preserves the event-ownership rule established after earlier duplicate-action defects.

## Focused falsification

Focused tests demonstrate:

1. persisted 40B launch lineage remains exact after the active-reentry split;
2. the raw initial receiver retains the exact typed handoff with no launch lineage/path;
3. raw receiver rollover mounts the existing blank 40C checkpoint form;
4. 47G inspection is pathless and preserves the exact launch-provenance object across rollover;
5. no handoff control exists before successful 47F;
6. successful 47F does not automatically exit;
7. explicit 47G returns exactly `47F.checkpoint.fresh_reentry`;
8. the returned object is not the earlier 47E fresh result;
9. the typed handoff remains available after removal of the just-written 40B overlay file;
10. failed no-overwrite 47F persistence exposes no handoff;
11. raw and persisted 47F source families can reach the same exact typed handoff seam;
12. plain 47F products remain scope-isolated;
13. normal runner close launches no receiver;
14. explicit runner handoff is passed object-identically to the pathless inspectable receiver;
15. product factories reject the wrong authority families.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

47G changes no:

- public 40A reconstruction;
- public 40B persistence;
- 40B overlay format;
- persisted 41A lineage proof;
- persisted third-epoch launch inspection semantics;
- existing 41E continuation handoff;
- public 40C or 40D persistence;
- CLI behavior;
- locator interpretation;
- browser behavior.

## Non-goals

47G does **not** add:

- a 40B disk relaunch inside the handoff;
- automatic mode promotion;
- automatic 40C persistence;
- fourth evidence-basis crossing;
- generic Nth-epoch handoff;
- recursive ancestry representation;
- new persistence format;
- new CLI flag;
- locator discovery or prefill;
- launch-path backfill;
- current/latest/head/chronology/branch-ranking authority;
- browser reacquisition;
- semantic-support or citation authority;
- autonomous research.

## Next boundary

After 47G, numerical symmetry is no longer sufficient justification for another milestone.

The next development decision should begin by reviewing the now-established third-basis-epoch first-checkpoint product together with existing 40C/40D continuation machinery, 41E cumulative handoff, and third-epoch inspection surfaces.

Only a concrete missing product seam should justify 47H.
