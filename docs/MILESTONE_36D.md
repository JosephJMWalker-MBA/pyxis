# Milestone 36D — Explicit In-Process Handoff to Cumulative Mode

Decision: D189

## Product question

36B can freshly checkpoint the first ordinary continuation above a root-backed 35C session through the established 35D persistence boundary. 36C can then operate a persisted 35D/35E continuation as a repeatable cumulative Textual loop.

Before 36D, moving between those two proven product surfaces required closing the 36B shell and explicitly relaunching the newly written continuation overlay.

The 35D checkpoint result already contains the exact freshly reconstructed typed continuation required by 36C:

```text
successful 35D checkpoint
→ ChromiumResearchRootBackedSessionContinuationCheckpointResult
→ result.fresh_reentry
→ valid 36C shell input
```

36D therefore closes only the in-process product seam. It adds no new durable format, loader, checkpoint algorithm, or path authority.

## Decision

After a successful 35D checkpoint, the 36B shell remains revision-locked and exposes one explicit researcher action:

```text
Continue in cumulative mode
```

The action does not exist before successful checkpoint proof. It is not mounted after rollover alone and is not mounted after a failed checkpoint attempt.

Selecting it performs only:

```text
exact retained successful 35D checkpoint
→ exact checkpoint.fresh_reentry object
→ exit first-checkpoint Textual app with that typed result
→ CLI validates the returned result type
→ launch existing 36C cumulative shell with the same exact object
```

No continuation overlay is reloaded during this transition. No plan is reconstructed from path text, and no filesystem search or inference occurs.

## Explicit user agency

Successful checkpointing does not automatically change shell families.

The researcher may:

- explicitly choose `Continue in cumulative mode`; or
- close the first-checkpoint shell and later relaunch the saved continuation overlay through the already-supported `--root-backed-continuation-overlay` path.

A normal close returns no typed continuation handoff and the CLI does not launch 36C.

Thus:

```text
successful persistence != automatic mode transition
```

and:

```text
explicit in-process typed handoff != persistent current-path authority
```

## Path authority remains blank in 36C

36D transfers live typed application state, not a claim that any path used during 35D remains the current location of an artifact.

The newly launched 36C shell starts from the exact proven continuation result and initially shows no checkpoint form. After its next explicit rollover, the existing 36C behavior mounts four blank 35E checkpoint inputs again.

The handoff therefore does not prefill or preserve as authority:

- the 35C overlay path used by the first checkpoint;
- the successor edge path used by the first checkpoint;
- the one-hop declaration path;
- the newly written 35D overlay path;
- any future cumulative declaration or overlay destination.

## CLI behavior

For `pyxis research-shell --root-backed-overlay ...`:

```text
fresh 35B re-entry
→ run 36B first-checkpoint shell
→ shell returns None
   → command ends normally

or

→ shell returns exact typed 35D continuation re-entry
   → validate ChromiumResearchRootBackedSessionContinuationReentryResult
   → run existing 36C cumulative shell with that exact object
```

An unexpected non-`None`, non-typed return is rejected rather than interpreted or coerced.

The other public launch paths remain unchanged:

- `--plan` retains ordinary 31A/32B behavior;
- `--root-backed-continuation-overlay` retains direct 36C fresh persisted re-entry behavior.

## Preserved authority boundaries

36D does not add:

- a new durable re-entry format;
- a new checkpoint or persistence boundary;
- automatic 35E persistence;
- automatic mode promotion after 35D save;
- reload of the saved continuation overlay during handoff;
- path carry-forward, path inference, or directory scanning;
- digest discovery or automatic predecessor search;
- plan-family guessing;
- latest/current/head, chronology, branch, or filesystem-order semantics;
- semantic-support, authorship, authenticity, or citation authority;
- browser navigation, acquisition, or research-control-plane escalation.

## Falsifiability

36D is intended to fail safely when:

- no successful 35D checkpoint exists;
- a 35D checkpoint attempt fails;
- the researcher closes the 36B shell without choosing the handoff action;
- the 36B app returns an unexpected untyped object instead of `None` or a valid continuation re-entry;
- the exact retained checkpoint result is not available to supply the handoff.

In those cases the CLI does not silently launch cumulative mode.

The handoff is intended to be proven by tests that require:

- absence of the handoff control before successful checkpointing;
- absence after failed checkpointing;
- success-only mounting of the explicit handoff control;
- return of the exact retained `checkpoint.fresh_reentry` object;
- no continuation-overlay loader call during the in-process transition;
- no cumulative launch after a normal close;
- rejection of an invalid app return type.

## Acceptance statement

A successful 36D establishes only:

> After the first root-backed continuation has been freshly checkpointed through 35D, the researcher may explicitly transfer that exact in-memory typed continuation result into the already-proven 36C cumulative shell within the same `research-shell` command. The transition reloads no continuation file, infers no current path, and does not occur automatically without the researcher choosing it.
