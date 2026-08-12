from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.presentation import WorkspacePresentation


class WorkspaceShell(App[None]):
    """Minimal Textual shell over one immutable Workspace presentation.

    The shell renders application-owned evidence only. It does not load a
    Workspace, compile, execute runtime code, query revision files, export, or
    infer READY state.
    """

    TITLE = "Pyxis"
    SUB_TITLE = "Workspace evidence"
    CSS = """
    Screen {
        align: center middle;
    }

    #workspace-shell {
        width: 80%;
        height: auto;
        padding: 1 2;
        border: round $primary;
    }

    #workspace-name {
        text-style: bold;
    }
    """

    def __init__(self, presentation: WorkspacePresentation) -> None:
        super().__init__()
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        presentation = self.presentation
        export_evidence = (
            "READY"
            if presentation.export is not None
            else "No READY evidence"
        )

        with Vertical(id="workspace-shell"):
            yield Static("Pyxis Workspace", id="shell-title")
            yield Static(
                presentation.canonical.name,
                id="workspace-name",
                markup=False,
            )
            yield Static(
                presentation.canonical.description,
                id="workspace-description",
                markup=False,
            )
            yield Static(
                f"Repository: {presentation.rir.repository_id}",
                id="repository-identity",
                markup=False,
            )
            yield Static(
                "Compiler evidence: "
                f"{len(presentation.artifacts)} artifacts",
                id="compiler-evidence",
                markup=False,
            )
            yield Static(
                f"Revision evidence: {len(presentation.revisions)} events",
                id="revision-evidence",
                markup=False,
            )
            yield Static(
                f"Export evidence: {export_evidence}",
                id="export-evidence",
                markup=False,
            )


def create_workspace_shell(presentation: WorkspacePresentation) -> WorkspaceShell:
    """Create the first local UI shell without acquiring or changing evidence."""

    return WorkspaceShell(presentation)
