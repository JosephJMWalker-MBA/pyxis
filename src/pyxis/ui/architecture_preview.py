from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.preview_presentation import ArchitecturePreviewPresentation


def _format_values(values: tuple[str, ...]) -> str:
    if not values:
        return "—"
    return "\n".join(f"- {value}" for value in values)


def _format_preview(presentation: ArchitecturePreviewPresentation) -> str:
    return "\n".join(
        (
            "Status: PROPOSED — NOT APPLIED",
            "",
            "Current canonical",
            f"Workspace ID: {presentation.current.workspace_id}",
            f"Name: {presentation.current.name}",
            f"Description: {presentation.current.description}",
            "Capabilities:",
            _format_values(presentation.current.capabilities),
            f"Canonical SHA-256: {presentation.current.canonical_sha256}",
            "",
            "Proposed canonical",
            f"Workspace ID: {presentation.proposed.workspace_id}",
            f"Name: {presentation.proposed.name}",
            f"Description: {presentation.proposed.description}",
            "Capabilities:",
            _format_values(presentation.proposed.capabilities),
            f"Canonical SHA-256: {presentation.proposed.canonical_sha256}",
            "",
            "Capability delta",
            "Added:",
            _format_values(presentation.added_capabilities),
            "Removed:",
            _format_values(presentation.removed_capabilities),
            "",
            "Predicted compiler-product consequences",
            "Added paths:",
            _format_values(presentation.added_artifact_paths),
            "Changed paths:",
            _format_values(presentation.changed_artifact_paths),
            "Removed paths:",
            _format_values(presentation.removed_artifact_paths),
            "",
            "Observable runtime-key contract",
            "Current keys:",
            _format_values(presentation.current_runtime_keys),
            "Proposed keys:",
            _format_values(presentation.proposed_runtime_keys),
            "Added keys:",
            _format_values(presentation.added_runtime_keys),
            "Removed keys:",
            _format_values(presentation.removed_runtime_keys),
        )
    )


class ArchitecturePreviewDetail(Vertical):
    """Renderer for proposed architecture evidence that is not current state."""

    def __init__(self) -> None:
        super().__init__(id="architecture-preview-detail")
        self.presentation: ArchitecturePreviewPresentation | None = None

    def compose(self) -> ComposeResult:
        yield Static(
            "PROPOSED ARCHITECTURE — NOT APPLIED",
            id="architecture-preview-title",
            classes="section-title",
            markup=False,
        )
        yield Static(
            "No pending architecture preview.",
            id="architecture-preview-evidence",
            classes="evidence-body",
            markup=False,
        )

    def replace_presentation(
        self,
        presentation: ArchitecturePreviewPresentation,
    ) -> None:
        """Replace only proposed-preview display state from application evidence."""

        self.presentation = presentation
        self.query_one("#architecture-preview-evidence", Static).update(
            _format_preview(presentation)
        )
