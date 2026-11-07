# Milestone 51E — fresh explicit-path initial-session re-entry

Decision: **D285**  
Issue: **#307**  
Pull request: **#308**

## Research question

51D creates one truthful initial governed-session root from an explicit durable capture,
one saved bare exact-range selection, and one first human rationale.

Its final 21C reopening is a same-process creation proof, however. The saved selection
was already loaded earlier in that command invocation.

51E asks the separate restart question:

> Can Pyxis reconstruct the same initial governed application state using only four
> caller-explicit durable locations, with every content and attachment relationship
> freshly re-earned after the prior process state is gone?

The preceding review in #306 deliberately tried to falsify the need for another
persistence format or locator document before implementation.

## Falsification result — no new durable state is needed

The existing durable artifacts already contain the complete root:

```text
research_capture.v1
+ research_paragraph_text_selection.v1
+ research_working_set.v2
+ research_working_set_note.v2
```

Existing public boundaries already own all necessary integrity and coherence work:

```text
16C capture load
→ 49B exact-range-selection relink
→ 21C working-set-note load
   → existing 20C ordered working-set-member reconciliation
→ 51C initial-session controller
```

Therefore 51E adds application reconstruction only. It introduces no
`initial_session_reentry.v1`, no genesis artifact, no locator document, and no generic
re-entry plan object.

## Public application boundary

51E adds:

`ChromiumResearchInitialSessionReentryResult`

and:

```python
reenter_chromium_research_initial_session(
    *,
    capture_source: Path,
    selection_source: Path,
    working_set_source: Path,
    note_source: Path,
) -> ChromiumResearchInitialSessionReentryResult
```

All four locations must be explicit `pathlib.Path` inputs before any file is loaded.
The function performs no path inference, directory scan, digest search, source
discovery, browser acquisition, or persistence.

## Exact reconstruction order

The implementation remains a thin composition:

1. fresh public 16C loads the explicit durable capture;
2. fresh public 49B verifies and relinks the explicit saved selection against that
   exact loaded capture;
3. fresh public 21C loads the explicit working-set note using exactly the one fresh
   bare-selection member plus the supplied working-set and note paths;
4. 21C delegates working-set verification and ordered member reconciliation to
   unchanged public 20C;
5. the existing 51C `ChromiumResearchInitialSessionController` mounts the exact fresh
   21C root; and
6. one immutable result returns only after the whole chain succeeds.

51E copies none of the verifier, digest, parent-reference, member-reference, or
selection-coordinate rules from those existing boundaries.

## Result semantics

The immutable result retains by identity:

- the fresh 16C loaded capture;
- the fresh 49B loaded bare exact-range selection;
- the fresh 21C loaded working-set-note root; and
- the 51C controller constructed from that exact root.

This result is application reconstruction state only. It is not a durable evidence
artifact, path registry, history index, trusted clock, source-authentication claim,
semantic-support claim, or current/latest/head pointer.

The supplied paths answer only **where the caller asked Pyxis to look**. Existing
verification and relinking answer whether the located bytes earn application
authority again.

## Read-only failure boundary

51E writes nothing.

A wrong but individually valid capture fails when 49B cannot attach the saved
selection to it. A wrong but individually valid saved selection reaches 49B but fails
20C ordered-member reconciliation. Wrong working-set and working-set-note artifacts
fail the existing parent/member identity rules. Malformed or tampered bytes remain
owned by each layer's established integrity verifier.

Focused proof snapshots every supplied input and verifies byte-for-byte preservation
after failed re-entry attempts.

## Loaded state outlives its locator files

After a successful re-entry, the four durable input files may disappear and the
already-mounted 51C presentation remains usable.

That behavior is intentional: the fresh loaders earned the application objects before
the files disappeared. The controller does not continuously treat paths as ambient
authority and does not rediscover or reread them while presenting the mounted root.

## External prior art

The #306 review also checked the July 2026 Model Context Protocol session-state
revision. MCP moved away from implicit protocol-level sessions and recommends explicit
application-owned handles for stateful interactions.

That supports Pyxis's explicit-state direction but does not replace content coherence:
an opaque handle or filesystem location can identify where to look, while Pyxis still
must freshly prove that the capture, selection, working set, and working-set note
satisfy their existing durable identity contracts.

Reference recorded in #306:

- <https://blog.modelcontextprotocol.io/posts/2026-07-28/>

## Executable proof

Executable head:

`496d3e0d78feb03f36fe10e5f60cf2c975f9bbe2`

passed the full Repository Zero matrix on both push and pull-request workflows:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

Push run: **#2109**  
Pull-request run: **#2110**

The focused executable proof demonstrates:

1. a complete v2 initial root is reconstructed from four durable paths without
   passing retained creation-time application objects;
2. the result retains the exact fresh capture, selection, loaded root, and controller
   objects by identity;
3. the 51C presentation preserves the exact human rationale and bare-selection
   excerpt while continuing to expose `human_note_text=None`;
4. the application order is exactly 16C → 49B → 21C → 51C;
5. non-`Path` inputs fail before 16C;
6. a wrong valid capture fails closed;
7. a different valid selection attached to the same capture fails working-set member
   reconciliation;
8. wrong valid working-set and note artifacts fail their existing coherence rules;
9. tampering at each of the four durable layers is rejected through existing
   verification;
10. every caller-supplied file remains byte-for-byte unchanged after each tested
    failure; and
11. a successful mounted presentation remains usable after all four durable inputs are
    deleted.

The full matrix also keeps the established ordinary-session re-entry stack green.

The documentation-complete head must pass the same push and PR matrix before merge.

## Scope

51E adds only:

- one initial-session re-entry application module;
- one focused test module; and
- this milestone record after executable proof.

It changes no existing durable schema or public 16C, 49B, 20C, 21C, or 51C semantics.

It adds no CLI command, Textual UI, locator/configuration persistence, browser action,
revision, continuation, edge, declaration, sequence, ordinary-session adoption, or
current/latest/head model.

## Stop boundary

51E proves only:

```text
four explicit durable locations
→ fresh content/coherence proof
→ mounted 51C initial-session application state
```

The next review should inspect the actual researcher action after fresh reconstruction
before deciding whether direct CLI re-entry, an initial-session Textual surface, or a
persisted locator convenience has earned another boundary.
