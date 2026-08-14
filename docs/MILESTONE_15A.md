# Milestone 15A — First Read-Only Chromium Evidence Boundary

**Decision D121 — Browser state remains caller-owned; Pyxis may acquire frozen read-only page evidence from an explicitly supplied Chromium DevTools endpoint, but it does not take browser-control authority.**

## Product question

Can Pyxis connect to an explicitly supplied Chromium session and turn one existing page into typed, immutable application evidence without taking ownership of navigation, automation, or browser state?

15A answers **yes** with one deliberately narrow observation path.

## Boundary

The caller supplies an explicit Chromium DevTools HTTP(S) endpoint. Pyxis does not discover browser processes, profiles, ports, or sessions.

The concrete transport under `pyxis.browser` performs only:

```text
explicit DevTools endpoint
    ↓
GET /json/list
    ↓
existing page targets only
    ↓
exact selected target
    ↓
one fixed Runtime.evaluate read
```

The fixed read acquires only:

- `window.location.href`;
- `document.title`;
- a bounded prefix of `document.body.innerText`;
- the exact Unicode code-point count of that rendered text.

Callers cannot provide JavaScript or arbitrary Chrome DevTools Protocol methods through this boundary.

## Target selection

Target selection is evidence-bearing rather than heuristic.

- If exactly one page target exists, it may be selected implicitly.
- If multiple page targets exist, Pyxis refuses to guess which tab is "current" or "active" and requires an exact `target_id`.
- A supplied `target_id` must match one discovered page target exactly.
- Non-page targets are ignored.

15A does not infer browser focus from `/json/list` ordering or target metadata.

## Application evidence

`pyxis.app.observe_chromium_page()` returns frozen evidence:

```text
ChromiumPageObservationEvidence
├── endpoint
├── target_id
├── url
├── title
└── ChromiumPageContentEvidence
    ├── source = document.body.innerText
    ├── text_prefix
    ├── text_character_count
    ├── text_limit
    └── truncated
```

The application layer owns this evidence contract. Chrome DevTools transport details remain under `pyxis.browser` and are not promoted into application truth.

## Unicode correction discovered during implementation

The first draft used JavaScript `text.length` / `text.slice()`. That would count UTF-16 code units while Python `len()` counts Unicode code points, making astral characters such as emoji capable of producing false truncation evidence.

The fixed browser expression therefore uses `Array.from(text)` for both counting and bounded slicing. The returned count and Python-side prefix length now share the same code-point semantics.

## Real-browser proof

15A does not rely only on mocked transport tests. The ordinary Repository Zero suite launches a disposable headless Chrome/Chromium instance with its own non-default profile, lets the browser publish its DevTools endpoint, discovers the exact fixture page target, and calls the production `observe_chromium_page()` path over the real HTTP/WebSocket DevTools boundary.

The fixture proves exact URL, title, rendered-text prefix, Unicode character count, limit, and truncation evidence.

The integration work exposed three test-harness facts rather than product defects:

1. a page target can become visible before its title/body evidence is ready;
2. browser startup and DevTools endpoint publication can vary enough that a 10-second fixture-startup assumption is not reliable;
3. one installed Chrome process can remain alive without publishing `DevToolsActivePort` even after 30 seconds, while another installed Chromium-family binary is available and healthy.

The fixture therefore synchronizes only its own setup. The browser allocates the debugging port and the test reads `DevToolsActivePort`; test-only readiness polling waits for the known fixture evidence; and if an installed browser binary never publishes any DevTools endpoint, that process is torn down and the next distinct installed Chromium-family binary is tried with a fresh profile. Once a DevTools endpoint exists, target discovery or production-observation failures remain hard failures rather than fallback conditions.

The production observation itself remains one target discovery plus one fixed read. It gains no browser-launch retry, navigation, target activation, page-read retry, or readiness semantics from the integration fixture.

Evidence trail:

- Actions #432 on `1f039148079b875ba706f7f1052b7a1596e1db32` first completed successfully on Python 3.11, 3.12, 3.13, and 3.14 with 221 tests including the real-browser path.
- PR-context Actions #436 on `12b74bdd718764d6a4e035208ee969d74368b155` exposed the third fixture fact on Python 3.12 before production DevTools acquisition was reached; the other three lanes passed.
- PR-context Actions #438 on `16acfa205718576a11102b85d082d0616eff88a2` then completed successfully on all four supported Python lanes. The previously failing Python 3.12 lane collected and passed all 221 tests, including the real-browser integration test.

The real-browser integration test remains part of the ordinary suite rather than a reduced compatibility smoke path or a skipped supported-interpreter lane.

## Dependency boundary

`websocket-client` is introduced only through the optional `browser` dependency group. It is also included in `dev` so the existing multi-version CI matrix exercises the browser transport on every supported Python interpreter.

The Pyxis core still has no required browser dependency.

## Explicit non-goals

15A adds no:

- navigation;
- tab activation;
- clicks or form submission;
- target creation or closure;
- arbitrary CDP command API;
- user-supplied JavaScript execution;
- browser-state persistence;
- page-observation persistence;
- LLM interpretation;
- autonomous research workflow;
- generalized browser abstraction;
- Workspace mutation;
- browser UI.

## Decision

D121 establishes: **Chromium remains the browser and remains caller-owned. Pyxis may observe one explicitly addressable existing page through a concrete read-only boundary and project that observation into immutable application evidence. Selection must be explicit when the browser exposes more than one page, and later browser-control authority must be justified separately rather than inferred from the ability to observe.**
