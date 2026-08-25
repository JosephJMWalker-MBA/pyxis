# Milestone 36C — Repeatable Cumulative Post-Root Checkpointing in Textual

Decision: D188

## Product question

36B made the first post-root continuation checkpointable from a 35C-launched Textual shell, then deliberately required an explicit relaunch through the saved continuation overlay.

A persisted 35D/35E continuation is already restartable, but before 36C its public CLI launch discarded the typed continuation re-entry lineage and mounted only a controller. The researcher could revise and roll over, but could not invoke the established 35E cumulative checkpoint boundary from the product surface.

36C closes that loop without recursive overlay ancestry:

```text
explicit 35D/35E overlay
→ strict 35D decode
→ fresh typed continuation re-entry
→ dedicated cumulative standalone shell
→ explicit endpoint revision
→ explicit 30A one-hop rollover
→ revision lock
→ blank explicit 35E checkpoint inputs
→ public 35E proof + persistence
→ visible promotion to exact fresh cumulative controller
→ unlock one next endpoint revision
```

## Decision

A continuation launched from `--root-backed-continuation-overlay` retains the exact `ChromiumResearchRootBackedSessionContinuationReentryResult` in a dedicated `RootBackedContinuationResearchSessionShell`.

It is not coerced to ordinary 31A lineage and does not use ordinary 32B restart controls. The 36B first-checkpoint shell remains separate.

## Blank checkpoint inputs every cycle

After each successful 30A rollover, the shell mounts a 35E checkpoint form with four blank explicit inputs:

1. current durable path for the exact 35D/35E overlay describing the pre-rollover cumulative session;
2. current durable path for the exact chosen successor edge;
3. no-overwrite destination for the new cumulative post-root declaration;
4. no-overwrite destination for the next 35D/35E overlay.

The shell does not prefill the overlay used at launch, an overlay written by a previous checkpoint, the successor path used during revision/rollover, or either destination. Past path use is not current-location authority.

The save action delegates only to:

```python
persist_chromium_research_root_backed_session_continuation_checkpoint_extension(...)
```

That application boundary retains the fixed 35C ancestry anchor, freshly relinks the complete ordered post-root edge tuple, verifies the chosen terminal edge by durable identity and exact human wording, persists the new cumulative declaration, freshly reconstructs the next continuation, and only then persists the next overlay.

## Visible cumulative promotion is mandatory

A one-hop 30A continuation presentation and a 35E cumulative presentation are intentionally different shapes.

For example:

```text
current cumulative segment: E2 → E3
30A rollover presentation:  E4
35E fresh presentation:      E2 → E3 → E4
```

Therefore successful checkpointing cannot merely advance hidden restart lineage while leaving the one-hop controller mounted.

36C requires:

```text
successful 35E proof
→ verify fresh terminal edge/root identity against mounted state
→ remove one-hop research surface
→ set typed lineage = result.fresh_reentry
→ set live controller = result.fresh_reentry.controller
→ mount exact fresh cumulative presentation
→ retain a checkpoint receipt
→ unlock next endpoint revision
```

This visible promotion keeps the next rollover's prior-controller presentation coherent with the exact typed continuation lineage required by the next 35E checkpoint.

## Repeatable loop

After promotion, the same shell may repeat:

```text
cumulative En
→ author En+1
→ explicit 30A rollover
→ lock
→ explicit 35E checkpoint
→ fresh cumulative E2..En+1 controller
→ unlock
```

Every new overlay continues to reference the same direct 35C root-backed ancestry overlay. The post-root edge tuple grows cumulatively; no 35D overlay references another 35D overlay.

## CLI handoff

`pyxis research-shell --root-backed-continuation-overlay ...` now passes the exact fresh continuation re-entry result into the dedicated cumulative shell factory.

The other entry families remain unchanged:

- `--plan` retains ordinary 31A/32B behavior;
- `--root-backed-overlay` retains the 36B first-checkpoint 35B shell behavior.

## Preserved authority boundaries

36C does not add:

- ordinary restart-lineage authority to root-backed continuations;
- recursive continuation-overlay traversal;
- path reuse or inference as current-location authority;
- filesystem scanning, digest discovery, or automatic predecessor search;
- plan-family guessing;
- latest/current/head, chronology, or branch semantics;
- semantic-support, authorship, authenticity, or citation authority;
- browser acquisition or research-control-plane state.

## Falsifiability

36C is intended to fail safely when:

- any checkpoint field is blank;
- the explicit current overlay is malformed, wrong, or no longer reconstructs the supplied current continuation;
- a different sibling successor is supplied;
- cumulative declaration and next-overlay destinations collide;
- either no-overwrite destination already exists;
- fresh cumulative terminal edge identity/text does not match the chosen one-hop continuation;
- the fixed 35C ancestry anchor changes;
- the fresh root identity diverges from the retained continuation ancestry.

On failure, the one-hop continuation remains visible and revision remains locked. Typed lineage does not advance.

Moved current overlay or successor files can succeed only when their new current locations are supplied explicitly and the durable relationships still verify.

## Acceptance statement

A successful 36C establishes only:

> A persisted 35D/35E continuation can run a repeatable governed Textual loop in which each explicit rollover is locked until an explicit 35E cumulative checkpoint is freshly proven. On success the shell visibly adopts that exact cumulative controller before further revision is unlocked, while preserving the fixed 35C ancestry anchor without recursive overlays, path inference, or global head/semantic authority.
