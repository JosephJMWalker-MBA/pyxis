# Milestone 10C — First Local UI Framework Evaluation

**Decision date:** 2026-08-12

## Question

Which current UI technology should render the first local Pyxis Workspace surface without weakening the boundaries already established by D082 and D083?

The first UI needs to:

- remain Python-first;
- run locally on the Repository Zero development platforms;
- consume `WorkspacePresentation` rather than repository files;
- keep compiler/runtime/revision/export operations outside the renderer;
- support deterministic automated testing in the existing pytest/CI path;
- provide enough layout and interaction capability for an evidence-oriented Workspace interface; and
- avoid introducing infrastructure for deployment targets that Repository Zero does not yet require.

## Considered frameworks

### Textual — selected

Textual provides a Python application/widget model, cross-platform local terminal execution, CSS-like layout/styling, and a dedicated headless `App.run_test()` / `Pilot` testing path. It can also be served in a browser, but browser serving is not required for the first local UI.

For Repository Zero this is the smallest framework that satisfies the current interaction and testing needs while allowing the renderer to remain a thin consumer of immutable application evidence.

### NiceGUI — not selected for the first slice

NiceGUI is Python-first from the application author's perspective and has strong testing support, but its runtime is a local web application: FastAPI on the backend with Vue/Quasar and socket.io communication to the browser/client. That is a reasonable architecture for a future graphical web surface, but it adds a server/browser protocol boundary that the first evidence UI does not currently need.

### PySide6 / Qt — not selected for the first slice

PySide6 provides the official Python bindings for Qt and a mature native desktop widget/model-view ecosystem. It is capable enough for a sophisticated desktop application, but it introduces a substantially larger compiled, platform-specific Qt dependency and licensing/deployment surface before Repository Zero has demonstrated a need for native desktop integration.

### Streamlit — not selected

Streamlit is highly productive for Python data applications and has a native app-testing framework. Its core interaction model, however, reruns the application script from top to bottom when widgets change. That execution model is poorly aligned with Pyxis's explicit application-operation boundaries, where UI events should invoke named application operations and then render returned evidence rather than implicitly rerun a whole UI script.

### Flet — not selected for the first slice

Flet offers Python-authored desktop, web, and mobile interfaces backed by Flutter. Its integration-test path provisions and builds a Flutter test host so tests exercise the app as shipped. That is valuable when desktop/mobile packaging is itself a requirement, but it adds a build/runtime toolchain that the first local Workspace evidence UI does not need.

## Decision

Use **Textual** for the first local Workspace UI.

The dependency remains optional (`pyxis[ui]`). The compiler/runtime core stays dependency-free. The development extra includes Textual and `pytest-asyncio` only so Repository Zero CI can exercise the UI boundary.

The first proof is deliberately not a Workspace product screen. `WorkspaceShell` accepts one existing immutable `WorkspacePresentation` and renders a minimal identity/evidence summary. It receives no Workspace path and owns no application operation.

## Revisit conditions

D084 should be reconsidered only when a demonstrated product requirement exceeds the first local UI boundary—for example:

- rich browser-native visualization is materially limited by Textual;
- direct Chromium/browser embedding becomes part of the Workspace UI itself;
- native desktop OS integration becomes necessary;
- mobile becomes an actual supported product target; or
- accessibility/interaction requirements cannot be met by the selected renderer.

A future renderer may change without changing D082/D083: `WorkspacePresentation` and application-owned operations remain the product boundary regardless of UI technology.

## Sources consulted

- Textual documentation: https://textual.textualize.io/
- Textual PyPI project: https://pypi.org/project/textual/
- NiceGUI documentation: https://nicegui.io/documentation/
- NiceGUI PyPI project: https://pypi.org/project/nicegui/
- Qt for Python documentation: https://doc.qt.io/qtforpython-6/
- Streamlit application model and testing documentation: https://docs.streamlit.io/
- Flet documentation and integration-testing guide: https://flet.dev/docs/
