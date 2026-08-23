# Milestone 31B — Standalone Governed Research Shell + Public CLI Entry

Decision: D174

## Product question

31A established that one governed research session can be reconstructed in a fresh
process from explicitly named durable artifacts without directory scanning, digest
discovery, browser reacquisition, or a global head model.

That still left a practical product failure:

```text
pyxis run ...
```

was the only public executable path.

The complete research workflow existed, but a researcher could reach it only by
writing Python orchestration that manually called 31A and then constructed the
research-aware Workspace shell.

31B makes the governed research workflow directly launchable while preserving the
existing authority boundaries.

## Public command

31B adds:

```text
pyxis research-shell --plan <locator-plan.json>
```

The command performs exactly:

```text
explicit locator-plan JSON
→ strict locator-plan decoding
→ established 31A fresh durable re-entry
→ exact returned 29A controller
→ standalone governed ResearchSessionShell
→ Textual run loop
```

The CLI does not reconstruct evidence itself.

The CLI does not fabricate Repository Zero Workspace state.

## Why the shell is standalone

30B's research interaction surface lives inside the research-aware
`WorkspaceShell` wrapper. That co-location is useful when a caller intentionally
supplies both Workspace and research evidence, but the two authority chains remain
independent.

Using that wrapper as the public research launcher would have required the CLI to
manufacture an unrelated Workspace solely to satisfy the shell constructor.

31B rejects that shortcut.

Instead it adds:

```text
pyxis.ui.research_session_shell.ResearchSessionShell
pyxis.ui.research_session_shell.create_research_session_shell(...)
```

The standalone shell contains only:

- the exact declared rationale segment;
- the exact bounded working-set contexts;
- the governed endpoint-revision controls from 29B;
- the governed explicit continuation controls from 30B;
- the transient rollover receipt after a successful explicit continuation.

It contains no Workspace runtime input, architecture preview/apply controls, export
controls, measurement surface, Workspace controller, Workspace presentation, RIR,
or compiler evidence.

Therefore:

```text
standalone research shell
!=
fabricated Workspace provenance
```

## Controller authority remains unchanged

`ResearchSessionShell` accepts exactly one
`ChromiumResearchSessionController`.

Before mounting, it freshly re-presents the controller's retained 26C evidence
through the established 28A presentation function and requires exact agreement with
the controller's retained presentation.

If the controller already retains one successful 29A endpoint write, that result
must still reference the controller's exact retained presentation.

The shell does not become a second controller.

It delegates:

```text
write successor
→ ChromiumResearchSessionController.persist_declared_endpoint_revision(...)
```

and:

```text
explicitly adopt successor
→ rollover_chromium_research_session_to_persisted_successor(...)
```

The same established distinctions remain:

```text
successful write
!=
adoption
```

and:

```text
explicit local continuation
!=
latest/current/canonical head
```

## Repeatable standalone workflow

The standalone shell supports the same repeated governed loop proven in the
Workspace wrapper:

```text
inspect declared rationale + bounded context
→ write exact human successor
→ old declared session remains mounted
→ explicitly choose continuation
→ supply exact successor file + new declaration destination
→ fresh 30A rollover
→ mount returned continuation controller
→ revise again
```

A focused test executes:

```text
v6
→ write v7
→ explicitly roll over to v7
→ write v8
→ explicitly roll over to v8
```

without adding a `latest`, `current_head`, or canonical-head field.

## Locator-plan document

31A's in-memory `ChromiumResearchSessionReentryPlan` is intentionally typed and
caller-owned. A public executable needs a serializable way for the caller to supply
those explicit locations.

31B adds an operational JSON document format:

```text
pyxis.chromium.research_session_reentry_locator_plan.v1
```

and:

```text
load_chromium_research_session_reentry_plan_document(...)
```

The document is deliberately not a research evidence format.

It contains only:

- member family labels;
- capture/note paths for each explicit working-set member;
- exact member order;
- explicit 20B/21B/22B/23B paths;
- explicit predecessor-edge order;
- explicit declared-edge order;
- explicit declaration path.

It contains no SHA-256 identity registry.

It contains no timestamp.

It contains no latest/current/head field.

It contains no branch rank or discovery rule.

Therefore:

```text
locator-plan document
!=
research evidence
!=
identity authority
!=
history index
```

## Strict document shape

The plan decoder requires an exact JSON object shape.

Unknown root keys reject.

Unknown member keys reject.

Duplicate JSON object keys reject.

Supported member kinds are exactly:

```text
paragraph_note
exact_range_note
comparison_note
```

This matters because permissively accepting fields such as:

```text
sha256
latest
head
```

would allow an operational convenience file to gradually become an undocumented
second authority surface.

31B refuses that expansion.

## Relative paths

Relative locator paths are interpreted only relative to the plan document's own
directory.

For example:

```text
research-session.plan.json
capture-a.json
paragraph-note.json
v4-edge.json
v5-edge.json
v6-edge.json
declared-sequence.json
```

may use simple sibling filenames in the plan.

The current working directory is not used to infer those locations.

This is locator convenience only.

Every referenced durable artifact still has to earn its authority again through
31A's established fresh verification/relinking chain.

Thus:

```text
relative path resolution
!=
content identity
```

## Plan loading performs no evidence reads

Loading the locator document reads only the locator document itself.

A focused test successfully decodes a plan whose referenced files do not exist.

Only the later 31A re-entry operation attempts to open and verify the referenced
evidence.

That separation preserves:

```text
configuration parsing
!=
evidence verification
```

and makes it impossible for the plan parser to become a hidden discovery layer.

## CLI remains thin

`pyxis.cli` adds one subcommand but no research-domain reconstruction logic.

The command delegates:

```text
load plan document
→ reenter_chromium_research_session(plan)
→ run standalone shell with result.controller
```

A focused CLI test deliberately replaces the old Workspace build operation with a
function that raises if called. `research-shell` still succeeds through fresh 31A
re-entry, proving that the CLI does not create unrelated Repository Zero state.

## UI dependency remains optional

The package's Textual dependency remains an optional `ui` extra.

31B does not import `pyxis.ui` at CLI module import time.

The UI module is imported only when `research-shell` is actually launched.

Therefore ordinary commands such as:

```text
pyxis run ...
```

do not acquire a new mandatory Textual dependency merely because the research
launcher exists.

If Textual is unavailable, the research-shell path reports the explicit install
hint:

```text
pip install 'pyxis[ui]'
```

## CLI failure behavior

Malformed plan documents, invalid 31A relationships, unreadable durable evidence,
or missing UI support fail before a research shell is treated as successfully
launched.

The command does not fall back to:

- directory scanning;
- filename guesses;
- digest search;
- browser reacquisition;
- an available nearby declaration;
- an inferred newest file;
- a fabricated Workspace.

## Existing co-located shell remains valid

31B does not replace `WorkspaceShell`.

Callers that intentionally want Repository Zero evidence and independently supplied
research evidence in the same UI may continue to use the established research-aware
Workspace wrapper.

The standalone shell simply removes the requirement to invent a Workspace when the
research session is the only intended authority surface.

Therefore:

```text
standalone research shell
!=
co-located Workspace research shell deprecated
```

Both are legitimate surfaces for different explicit caller intents.

## Falsifiability

Focused tests prove:

1. relative-path locator documents decode to the exact 31A plan and reconstruct an equivalent governed session;
2. absolute paths remain explicit locations and require no rewriting;
3. plan parsing does not open or discover referenced artifacts;
4. authority-like unknown root/member fields reject;
5. duplicate keys and unsupported member kinds reject before 31A;
6. the standalone shell mounts the exact controller with no Workspace controls;
7. a standalone endpoint write preserves exact human wording and does not adopt the successor;
8. explicit standalone rollover replaces the research session while leaving the old controller unchanged;
9. the standalone shell repeats the v7/v8 write-rollover loop without head state;
10. a forged controller presentation is rejected before becoming UI authority;
11. the public `research-shell` command performs real locator-plan decoding + 31A re-entry while never calling the Workspace build path;
12. invalid plan input becomes an explicit CLI usage failure before UI launch;
13. `research-shell --help` exposes the single explicit plan entry rather than discovery/head switches;
14. the UI dependency is imported lazily and a missing Textual dependency produces the explicit `pyxis[ui]` install hint.

## Scope

31B changes only:

- new `src/pyxis/app/chromium_research_session_reentry_plan_document.py`;
- new `src/pyxis/ui/research_session_shell.py`;
- package-level UI exports for the standalone shell;
- the existing thin `src/pyxis/cli.py` command router;
- focused locator-plan, standalone-shell, and CLI tests;
- this milestone document.

It does not change:

- 31A durable re-entry semantics;
- 30A/30B rollover semantics;
- 29A/29B endpoint-revision semantics;
- any research evidence persistence format;
- Chromium acquisition;
- Repository Zero compiler/RIR/runtime/export/measurement semantics;
- `pyproject.toml` script entry point;
- README;
- `docs/CURRENT_STATE.md`.

## What successful 31B proves

Successful 31B establishes only:

> A researcher can invoke the installed `pyxis` executable with one strict,
> locator-only JSON plan; Pyxis can freshly reconstruct exactly that chosen durable
> research session through the established 31A authority boundary and launch a
> standalone Textual interaction surface over the returned governed controller,
> including explicit successor writes and explicit continuation rollovers, without
> creating unrelated Workspace provenance or introducing discovery/latest/head
> semantics.

That does not prove source authenticity, complete history, unique succession,
semantic support, citation authority, trusted chronology, or a canonical global
research state.
