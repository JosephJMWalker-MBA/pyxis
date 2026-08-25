# Milestone 36A — Public CLI Launch for Persisted Root-Backed Research Sessions

Decision: D186

## Product question

35C–35E make changed-evidence-basis research sessions durable and restartable at the
application/configuration layer, but the installed `pyxis research-shell` entry point
still accepts only the ordinary 31B/v1 locator plan.

36A asks:

> Can the installed CLI explicitly launch either a persisted 35C root-backed session
> or a persisted 35D/35E post-root continuation without guessing the configuration
> family or fabricating ordinary 32B restart lineage?

36A answers **yes** through explicit mutually exclusive entry options.

## Public entry forms

The established ordinary form remains:

```text
pyxis research-shell --plan <ordinary-v1-plan.json>
```

36A adds:

```text
pyxis research-shell --root-backed-overlay <35c-overlay.json>
pyxis research-shell --root-backed-continuation-overlay <35d-overlay.json>
```

35E requires no additional CLI option because D185 intentionally reuses the unchanged
35D continuation-overlay format.

The three options are mutually exclusive and exactly one is required. Pyxis does not
inspect an arbitrary JSON file and guess its plan family.

## Delegation boundaries

The ordinary path remains unchanged:

```text
explicit ordinary plan
→ existing 31B document loader
→ public 31A fresh re-entry
→ existing re-entry-aware ResearchSessionShell
```

The 35C path is:

```text
explicit 35C overlay
→ existing strict 35C loader
→ public 35B fresh root-backed re-entry
→ existing governed controller
→ controller-only ResearchSessionShell
```

The 35D/35E path is:

```text
explicit 35D-family continuation overlay
→ existing strict 35D loader
→ public 35D fresh continuation re-entry
→ existing governed controller
→ controller-only ResearchSessionShell
```

No Repository Zero Workspace build path is invoked by any `research-shell` entry.

## Why root-backed launches are controller-only

The existing standalone shell has two distinct modes:

- controller-only mode; and
- ordinary re-entry-aware mode carrying an exact `ChromiumResearchSessionReentryResult`.

Only the second mode has earned the ordinary 32B restart-checkpoint lineage contract.
A 35B or 35D result is not an ordinary 31A result and must not be coerced into one.

Therefore 36A launches root-backed sessions in controller-only mode.

That mode retains the existing governed controller interactions, including inspection,
explicit endpoint revision, and explicit rollover behavior already owned by the shell,
but it does not mount ordinary 32B restart-checkpoint controls.

Thus:

```text
public launchability
!=
ordinary restart-lineage authority
```

A later milestone may explicitly connect the shell to the 35C/35D/35E checkpoint
boundaries.

## Lazy UI dependency

Textual remains an optional dependency and is imported only when a research shell is
actually launched. Both the ordinary re-entry-aware runner and the new controller-only
runner share the same lazy factory-loading boundary and the same installation hint.

## Authority boundaries

36A does not infer or claim:

- plan-family autodetection;
- filesystem discovery;
- directory scanning;
- digest-based lookup;
- path identity;
- a global current/latest/canonical head;
- chronology or branch identity;
- unique successor;
- semantic improvement or evidentiary support;
- source authenticity, authorship, or citation authority;
- ordinary 32B restart lineage for root-backed sessions;
- browser navigation or autonomous acquisition.

Paths remain caller-supplied locations. Configuration-family selection remains a
caller-owned CLI choice.

## Falsifiability

Focused 36A coverage proves:

1. the existing ordinary `--plan` path still freshly re-enters and launches the exact
   ordinary re-entry-aware session;
2. an explicit 35C overlay freshly reconstructs its root-backed governed controller
   and uses only the controller-only shell runner;
3. an explicit 35D overlay freshly reconstructs its continuation controller through
   the existing 35D boundary;
4. a 35E-generated cumulative overlay launches through the same unchanged 35D family;
5. controller-only shell launch passes no ordinary `reentry=` lineage argument;
6. invalid ordinary and root-backed configuration rejects before Textual launch;
7. exactly one entry family is required and mixed entry options reject at argument
   parsing;
8. help exposes only explicit entry families and no latest/head/directory/auto entry;
9. the optional UI dependency remains lazily imported for both launch modes; and
10. research-shell launch does not invoke Workspace build orchestration.

## Scope

36A changes only:

- `src/pyxis/cli.py`;
- `tests/test_cli.py`; and
- this milestone document.

36A does not change:

- the 31A/31B ordinary plan format;
- 32A/32B ordinary restart behavior;
- 35B typed root-backed re-entry;
- the 35C overlay format;
- the 35D overlay format;
- 35E cumulative checkpoint semantics;
- `ResearchSessionShell` implementation;
- Repository Zero;
- Chromium acquisition; or
- research-control-plane state.

## What successful 36A proves

Successful 36A establishes only:

> From one explicitly selected ordinary plan, 35C root-backed overlay, or 35D/35E
> continuation overlay, the installed `pyxis research-shell` command can freshly
> reconstruct the corresponding governed session through the already-earned
> application boundary and launch the existing standalone shell without discovery,
> plan-family guessing, fabricated ordinary restart lineage, or global
> head/semantic authority.
