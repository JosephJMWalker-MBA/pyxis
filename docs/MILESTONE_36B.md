# Milestone 36B — Textual First Checkpoint From Persisted Root-Backed Ancestry

Decision: D187

## Product question

Milestones 35B–35E made the changed-evidence-basis lineage durable at the application/configuration layer, and 36A made those persisted sessions launchable from the installed CLI. But 36A deliberately launched 35C root-backed sessions in controller-only Textual mode, so the first post-root rollover could not be checkpointed from the product surface.

36B adds the smallest missing UI authority:

```text
explicit 35C overlay
→ public 35C decode
→ public 35B fresh re-entry
→ dedicated root-backed standalone shell
→ explicit endpoint revision
→ explicit 30A rollover
→ revision lock
→ blank explicit 35D checkpoint inputs
→ public 35D fresh proof + no-overwrite overlay
```

## Decision

A 35C-launched root-backed session retains its exact typed `ChromiumResearchRootBackedSessionReentryResult` in a dedicated `RootBackedResearchSessionShell` subclass.

The ordinary `ResearchSessionShell` remains unchanged and continues to own only its established controller-only and exact ordinary 31A/32B modes.

The root-backed shell does not construct, coerce, or imitate `ChromiumResearchSessionReentryResult`.

## Explicit path discipline

After one successful 30A rollover, the root-backed shell mounts a dedicated 35D checkpoint form with four blank inputs:

1. current durable path for the exact 35C overlay;
2. current durable path for the chosen successor edge;
3. current durable path for the one-hop continuation declaration;
4. no-overwrite destination for the new 35D continuation overlay.

The shell does not prefill the launch-time 35C overlay path or reuse the paths entered during rollover. A previously used or displayed path remains a location, not continuing location authority.

The save action delegates only to:

```python
persist_chromium_research_root_backed_session_continuation_checkpoint(...)
```

Therefore the application layer, not Textual, freshly proves the explicit 35C ancestry, the chosen successor/declaration relationship, the retained 34A root identity, and the resulting continuation before the overlay is written.

## Revision lock

Immediately after rollover, endpoint revision is locked until checkpoint handling.

Unlike ordinary 32B, a successful 36B checkpoint deliberately does **not** unlock another in-process revision. The successful receipt directs the researcher to relaunch the saved overlay explicitly:

```text
pyxis research-shell --root-backed-continuation-overlay <saved-overlay>
```

This is intentional:

```text
successful first 35D checkpoint
!= automatic promotion to 35E cumulative checkpoint mode
```

Repeated post-root continuation checkpointing requires a distinct typed 35D/35E re-entry lineage and remains the next authority decision.

## CLI handoff

`pyxis research-shell --root-backed-overlay ...` now retains the exact fresh 35B result and passes it to the dedicated root-backed shell factory.

The other two entry families remain unchanged in 36B:

- `--plan` continues to pass the exact ordinary 31A result into the established re-entry-aware shell;
- `--root-backed-continuation-overlay` continues to launch its freshly reconstructed controller in controller-only mode until the separate cumulative-checkpoint UI boundary is authorized.

## Preserved authority boundaries

36B does not add:

- ordinary 32A/32B authority to root-backed sessions;
- 35E cumulative checkpointing;
- recursive continuation-overlay references;
- path inference or path reuse as current-location authority;
- filesystem scanning or digest discovery;
- automatic plan-family detection;
- latest/current/head, chronology, or branch semantics;
- semantic-support, authorship, authenticity, or citation authority;
- browser acquisition or research-control-plane state.

## Falsifiability

36B is intended to fail safely when:

- any one of the four explicit checkpoint paths is blank;
- the explicit current 35C ancestry has been tampered with;
- a different sibling successor is supplied;
- the requested 35D overlay destination already exists;
- the checkpoint result does not retain the exact supplied root-backed lineage and rollover;
- the freshly reconstructed continuation endpoint/root identities do not match the mounted session.

Successful checkpointing with files that have moved is valid only when the researcher supplies their new explicit current locations and the durable content relationships still verify.

## Acceptance statement

A successful 36B establishes only:

> A root-backed session freshly launched from one explicit 35C overlay can revise and explicitly roll over in Textual, then use blank caller-supplied current locations to freshly prove and persist its first 35D continuation overlay. Ordinary restart authority is not reused, paths are not inferred, and the shell does not silently enter repeated 35E checkpoint mode.
