# Milestone 38A — Public CLI launch for persisted second-basis-epoch sessions

## Decision D194

Persisted second-basis-epoch sessions may be launched from the installed public CLI only through explicit configuration-family options.

38A extends `pyxis research-shell` with two new mutually exclusive entry families:

```text
pyxis research-shell --second-basis-epoch-overlay <37B-overlay.json>
pyxis research-shell --second-basis-epoch-continuation-overlay <37C-or-37D-overlay.json>
```

37D reuses the 37C durable format, so it receives no separate CLI option.

No generic overlay option, format autodetection, directory search, or current/latest/head selection is introduced.

## Complete explicit entry set

After 38A, `research-shell` accepts exactly one of:

```text
--plan
--root-backed-overlay
--root-backed-continuation-overlay
--second-basis-epoch-overlay
--second-basis-epoch-continuation-overlay
```

The argparse mutually exclusive group remains required. Mixing entry families rejects before any plan loading or UI work.

## 37B launch path

```text
explicit --second-basis-epoch-overlay path
→ strict 37B locator-overlay loader
→ existing 37A fresh second-epoch re-entry
→ freshly governed second-epoch controller
→ existing controller-only ResearchSessionShell
```

The CLI does not fabricate an ordinary 31A result, a 35B root-backed result, or another typed lineage wrapper.

## 37C / 37D launch path

```text
explicit --second-basis-epoch-continuation-overlay path
→ strict existing 37C locator-overlay loader
→ existing 37C fresh continuation re-entry
→ freshly governed post-second-root controller
→ existing controller-only ResearchSessionShell
```

A cumulative 37D overlay is simply a valid 37C-format document with a longer explicit edge tuple and cumulative declaration. The CLI does not inspect milestone provenance or guess which producer created it.

## Public launchability is not checkpoint authority

Both new entry families deliberately use:

```text
_run_controller_only_research_session_shell(controller)
```

They do not use:

```text
_run_research_session_shell(...)
_run_root_backed_research_session_shell(...)
_run_root_backed_continuation_research_session_shell(...)
```

The second-epoch application results contain restart lineage, but 38A does not yet define how that lineage is paired with an explicit launch-config path and retained safely inside Textual for future checkpoint operations.

Therefore:

```text
public launchability
!=
permission to use an older checkpoint-aware shell lineage
```

and:

```text
freshly reconstructed controller
!=
implicitly authorized restart-checkpoint state
```

## No format autodetection

The caller selects the configuration family explicitly.

Pyxis does not:

- inspect a JSON `format` field to choose a loader;
- try loaders until one succeeds;
- scan a directory for plausible overlays;
- infer the newest configuration;
- select a head or branch;
- convert one lineage family into another.

This keeps entry authority at the caller/tool boundary rather than inside opaque launch heuristics.

## Proven CLI behavior

The 38A focused CLI tests use actual durable fixtures to prove:

- a persisted 37B overlay launches through `--second-basis-epoch-overlay`;
- a persisted first 37C continuation launches through `--second-basis-epoch-continuation-overlay`;
- a cumulative 37D overlay launches through that same continuation family;
- all three route only through the controller-only shell boundary;
- none builds Repository Zero / Workspace state;
- malformed 37B and 37C-family overlays reject before UI launch;
- new entry families remain mutually exclusive with ordinary and first-root families;
- CLI help exposes every explicit family;
- help exposes no `--latest`, `--head`, `--directory`, `--auto`, generic `--overlay`, format-detection, or format-selection authority.

Existing ordinary, 35C, and 35D/35E launch behavior remains unchanged.

## What 38A does not authorize

38A does **not** add:

- second-epoch Textual checkpoint controls;
- a second-epoch launch-lineage proof wrapper;
- in-process handoff from a 37B shell into a 37C/37D checkpoint-aware shell;
- automatic promotion between 37B and 37C configuration families;
- new persistence formats;
- a third evidence-basis epoch;
- format autodetection;
- path discovery;
- current/latest/head authority;
- chronology or branch semantics;
- semantic-support, truth, authorship, authenticity, trusted-time, or citation authority.

## Acceptance statement

After 38A, Pyxis may say only:

> Persisted 37B second-epoch sessions and 37C/37D continuation sessions can be explicitly launched from the public `research-shell` command. Each configuration is strictly decoded and freshly re-entered through its established application boundary, then mounted through the controller-only shell without inventing checkpoint lineage, discovery, format autodetection, or global-head authority.
