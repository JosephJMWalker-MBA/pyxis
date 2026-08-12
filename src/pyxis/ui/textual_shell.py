from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Button, Input, Static

from pyxis.app.controller import WorkspaceController
from pyxis.app.presentation import (
    CompilerArtifactPresentation,
    ExportPresentation,
    RevisionPresentation,
    WorkspacePresentation,
)
from pyxis.app.preview_presentation import ArchitecturePreviewPresentation


def _format_capabilities(capabilities: tuple[str, ...]) -> str:
    if not capabilities:
        return "—"
    return "\n".join(f"- {capability}" for capability in capabilities)


def _format_paths(paths: tuple[str, ...]) -> str:
    if not paths:
        return "—"
    return "\n".join(f"- {path}" for path in paths)


def _format_optional(value: str | None) -> str:
    return value if value is not None else "—"


def _runtime_to_builtin(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            str(key): _runtime_to_builtin(item)
            for key, item in value.items()
        }
    if isinstance(value, tuple):
        return [_runtime_to_builtin(item) for item in value]
    return value


def _format_runtime(presentation: WorkspacePresentation) -> str:
    return json.dumps(
        _runtime_to_builtin(presentation.runtime_result),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _format_artifact(artifact: CompilerArtifactPresentation) -> str:
    return "\n".join(
        (
            f"Path: {artifact.path}",
            f"Status: {artifact.status}",
            f"Node SHA-256: {_format_optional(artifact.node_sha256)}",
            f"Artifact SHA-256: {_format_optional(artifact.artifact_sha256)}",
        )
    )


def _format_artifacts(presentation: WorkspacePresentation) -> str:
    if not presentation.artifacts:
        return "No compiler artifact evidence."
    return "\n\n".join(
        _format_artifact(artifact)
        for artifact in presentation.artifacts
    )


def _format_revision(revision: RevisionPresentation, index: int) -> str:
    return "\n".join(
        (
            f"Revision {index}",
            f"Revision ID: {revision.revision_id}",
            f"Parent revision ID: {_format_optional(revision.parent_revision_id)}",
            f"Operation: {revision.operation}",
            f"Rationale: {revision.rationale}",
            f"Before canonical SHA-256: {revision.before_canonical_sha256}",
            f"After canonical SHA-256: {revision.after_canonical_sha256}",
            f"Completed: {'yes' if revision.completed else 'no'}",
            "Completion RIR SHA-256: "
            f"{_format_optional(revision.completion_rir_sha256)}",
            "Completion generation manifest SHA-256: "
            f"{_format_optional(revision.completion_generation_manifest_sha256)}",
        )
    )


def _format_revisions(presentation: WorkspacePresentation) -> str:
    if not presentation.revisions:
        return "No revision evidence."
    return "\n\n".join(
        _format_revision(revision, index)
        for index, revision in enumerate(presentation.revisions, start=1)
    )


def _format_export(export: ExportPresentation | None) -> str:
    if export is None:
        return "No READY evidence."
    return "\n".join(
        (
            f"Readiness: {export.readiness}",
            f"Export root: {export.export_root}",
            f"RIR SHA-256: {export.rir_sha256}",
            "Generation manifest SHA-256: "
            f"{export.generation_manifest_sha256}",
            f"Verification input SHA-256: {export.input_sha256}",
            f"Compiler product count: {export.compiler_product_count}",
        )
    )


def _format_canonical(presentation: WorkspacePresentation) -> str:
    canonical = presentation.canonical
    return "\n".join(
        (
            f"Workspace ID: {canonical.workspace_id}",
            f"Name: {canonical.name}",
            f"Description: {canonical.description}",
            "Capabilities:",
            _format_capabilities(canonical.capabilities),
            f"Canonical SHA-256: {canonical.canonical_sha256}",
        )
    )


def _format_rir(presentation: WorkspacePresentation) -> str:
    rir = presentation.rir
    return "\n".join(
        (
            f"Schema version: {rir.schema_version}",
            f"Repository ID: {rir.repository_id}",
            f"Workspace ID: {rir.workspace_id}",
            f"Entrypoint: {rir.entrypoint}",
            "Capabilities:",
            _format_capabilities(rir.capabilities),
            f"RIR SHA-256: {rir.rir_sha256}",
        )
    )


def _export_summary(presentation: WorkspacePresentation) -> str:
    return "READY" if presentation.export is not None else "No READY evidence"


def _format_architecture_preview(
    presentation: ArchitecturePreviewPresentation,
) -> str:
    return "\n".join(
        (
            "PROPOSED — NOT APPLIED",
            "",
            f"Current canonical SHA-256: {presentation.current.canonical_sha256}",
            f"Proposed canonical SHA-256: {presentation.proposed.canonical_sha256}",
            "",
            "Current capabilities:",
            _format_capabilities(presentation.current.capabilities),
            "Proposed capabilities:",
            _format_capabilities(presentation.proposed.capabilities),
            "Added capabilities:",
            _format_capabilities(presentation.added_capabilities),
            "Removed capabilities:",
            _format_capabilities(presentation.removed_capabilities),
            "",
            "Added compiler-product paths:",
            _format_paths(presentation.added_artifact_paths),
            "Changed compiler-product paths:",
            _format_paths(presentation.changed_artifact_paths),
            "Removed compiler-product paths:",
            _format_paths(presentation.removed_artifact_paths),
            "",
            "Current runtime keys:",
            _format_capabilities(presentation.current_runtime_keys),
            "Proposed runtime keys:",
            _format_capabilities(presentation.proposed_runtime_keys),
            "Added runtime keys:",
            _format_capabilities(presentation.added_runtime_keys),
            "Removed runtime keys:",
            _format_capabilities(presentation.removed_runtime_keys),
        )
    )


class ArchitecturePreviewDetail(Vertical):
    """Distinct renderer for proposed architecture that has not been applied."""

    def __init__(self) -> None:
        super().__init__(id="architecture-preview")
        self.presentation: ArchitecturePreviewPresentation | None = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Architecture preview — proposed state only",
            id="architecture-preview-title",
            classes="section-title",
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
        self.presentation = presentation
        self.query_one("#architecture-preview-evidence", Static).update(
            _format_architecture_preview(presentation)
        )

    def clear_presentation(self) -> None:
        """Return the proposed-state surface to its explicit empty state."""

        self.presentation = None
        self.query_one("#architecture-preview-evidence", Static).update(
            "No pending architecture preview."
        )


class ArchitectureApplyControls(Vertical):
    """Rationale-bearing controls mounted only for a retained pending preview."""

    def __init__(self) -> None:
        super().__init__(id="architecture-apply-controls")

    def compose(self) -> ComposeResult:
        yield Static(
            "Rationale required before Apply",
            id="architecture-rationale-label",
        )
        yield Input(
            placeholder="Explain why this architecture change should be applied",
            id="architecture-rationale",
        )
        yield Button(
            "Apply removal of normalize_text",
            id="apply-remove-normalize-text",
            variant="warning",
        )
        yield Static(
            "",
            id="architecture-apply-status",
            markup=False,
        )


class ExportRefreshControls(Vertical):
    """Explicit verified-export controls shown only while READY evidence is absent."""

    def __init__(self) -> None:
        super().__init__(id="export-refresh-controls")

    def compose(self) -> ComposeResult:
        yield Static(
            "Verified export destination",
            id="export-destination-label",
        )
        yield Input(
            placeholder="Enter a fresh export destination path",
            id="export-destination",
        )
        yield Button(
            "Export and verify",
            id="refresh-export",
        )
        yield Static(
            "",
            id="export-refresh-status",
            markup=False,
        )


class WorkspaceDetail(VerticalScroll):
    """Complete renderer for one immutable Workspace presentation."""

    def __init__(self, presentation: WorkspacePresentation) -> None:
        super().__init__(id="workspace-detail")
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        presentation = self.presentation
        canonical = presentation.canonical
        rir = presentation.rir

        with Vertical(id="workspace-summary"):
            yield Static("Pyxis Workspace", id="shell-title")
            yield Static(canonical.name, id="workspace-name", markup=False)
            yield Static(
                canonical.description,
                id="workspace-description",
                markup=False,
            )
            yield Static(
                f"Repository: {rir.repository_id}",
                id="repository-identity",
                markup=False,
            )
            yield Static(
                f"Compiler evidence: {len(presentation.artifacts)} artifacts",
                id="compiler-evidence",
                markup=False,
            )
            yield Static(
                f"Revision evidence: {len(presentation.revisions)} events",
                id="revision-evidence",
                markup=False,
            )
            yield Static(
                f"Export evidence: {_export_summary(presentation)}",
                id="export-evidence",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="canonical-section"):
            yield Static("Canonical intent", classes="section-title")
            yield Static(
                _format_canonical(presentation),
                id="canonical-evidence",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="rir-section"):
            yield Static("Repository Intermediate Representation", classes="section-title")
            yield Static(
                _format_rir(presentation),
                id="rir-evidence",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="compiler-section"):
            yield Static("Compiler artifacts", classes="section-title")
            yield Static(
                _format_artifacts(presentation),
                id="compiler-artifacts",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="runtime-section"):
            yield Static("Runtime result", classes="section-title")
            yield Static(
                _format_runtime(presentation),
                id="runtime-result",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="revisions-section"):
            yield Static("Revision timeline", classes="section-title")
            yield Static(
                _format_revisions(presentation),
                id="revision-timeline",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="export-section"):
            yield Static("Export verification", classes="section-title")
            yield Static(
                _format_export(presentation.export),
                id="export-verification",
                classes="evidence-body",
                markup=False,
            )

    def replace_presentation(self, presentation: WorkspacePresentation) -> None:
        """Replace rendered evidence with one fresh application presentation."""

        self.presentation = presentation
        canonical = presentation.canonical
        rir = presentation.rir

        self.query_one("#workspace-name", Static).update(canonical.name)
        self.query_one("#workspace-description", Static).update(canonical.description)
        self.query_one("#repository-identity", Static).update(
            f"Repository: {rir.repository_id}"
        )
        self.query_one("#compiler-evidence", Static).update(
            f"Compiler evidence: {len(presentation.artifacts)} artifacts"
        )
        self.query_one("#revision-evidence", Static).update(
            f"Revision evidence: {len(presentation.revisions)} events"
        )
        self.query_one("#export-evidence", Static).update(
            f"Export evidence: {_export_summary(presentation)}"
        )
        self.query_one("#canonical-evidence", Static).update(
            _format_canonical(presentation)
        )
        self.query_one("#rir-evidence", Static).update(_format_rir(presentation))
        self.query_one("#compiler-artifacts", Static).update(
            _format_artifacts(presentation)
        )
        self.query_one("#runtime-result", Static).update(
            _format_runtime(presentation)
        )
        self.query_one("#revision-timeline", Static).update(
            _format_revisions(presentation)
        )
        self.query_one("#export-verification", Static).update(
            _format_export(presentation.export)
        )


class WorkspaceShell(App[None]):
    """Textual shell over current evidence and one application live-state authority."""

    TITLE = "Pyxis"
    SUB_TITLE = "Workspace evidence"
    CSS = """
    Screen {
        align: center top;
    }

    #runtime-interaction,
    #architecture-preview-interaction,
    #architecture-preview,
    #export-refresh-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $primary;
    }

    #architecture-preview {
        border: double $warning;
    }

    #runtime-input-label,
    #architecture-preview-action-label,
    #architecture-rationale-label,
    #export-destination-label {
        text-style: bold;
        margin-bottom: 1;
    }

    #architecture-apply-controls,
    #export-refresh-slot {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    #architecture-apply-status,
    #export-refresh-status {
        margin-top: 1;
    }

    #workspace-detail {
        width: 94%;
        height: 1fr;
        padding: 1 2 2 2;
    }

    #workspace-summary,
    .evidence-section {
        width: 100%;
        height: auto;
        padding: 1 2;
        margin-bottom: 1;
        border: round $primary;
    }

    #workspace-name,
    .section-title {
        text-style: bold;
    }

    .section-title {
        margin-bottom: 1;
    }

    .evidence-body {
        width: 100%;
        height: auto;
    }
    """

    def __init__(
        self,
        presentation: WorkspacePresentation,
        *,
        controller: WorkspaceController | None = None,
    ) -> None:
        super().__init__()
        self.presentation = presentation
        self.controller = controller

    def compose(self) -> ComposeResult:
        if self.controller is not None:
            with Vertical(id="runtime-interaction"):
                yield Static("Runtime input", id="runtime-input-label")
                yield Input(
                    placeholder="Enter text and press Enter to run",
                    id="runtime-input",
                )
            with Vertical(id="architecture-preview-interaction"):
                yield Static(
                    "Propose architecture change",
                    id="architecture-preview-action-label",
                )
                yield Button(
                    "Preview removal of normalize_text",
                    id="preview-remove-normalize-text",
                )
            yield ArchitecturePreviewDetail()
            with Vertical(id="export-refresh-slot"):
                if self.presentation.export is None:
                    yield ExportRefreshControls()
        yield WorkspaceDetail(self.presentation)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "runtime-input" or self.controller is None:
            return

        presentation = self.controller.rerun(event.value)
        self.presentation = presentation
        self.query_one(WorkspaceDetail).replace_presentation(presentation)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if self.controller is None:
            return

        if event.button.id == "preview-remove-normalize-text":
            presentation = self.controller.preview_remove_normalize_text()
            self.query_one(ArchitecturePreviewDetail).replace_presentation(presentation)

            if len(self.query("#architecture-apply-controls")) == 0:
                container = self.query_one("#architecture-preview-interaction", Vertical)
                await container.mount(ArchitectureApplyControls())
            else:
                self.query_one("#architecture-apply-status", Static).update("")
            return

        if event.button.id == "refresh-export":
            destination_input = self.query_one("#export-destination", Input)
            runtime_input = self.query_one("#runtime-input", Input)
            status = self.query_one("#export-refresh-status", Static)

            try:
                presentation = self.controller.refresh_export(
                    Path(destination_input.value),
                    runtime_input.value,
                )
            except Exception as exc:
                status.update(f"Export failed: {exc}")
                return

            self.presentation = presentation
            self.query_one(WorkspaceDetail).replace_presentation(presentation)
            controls = self.query_one("#export-refresh-controls", ExportRefreshControls)
            await controls.remove()
            return

        if event.button.id != "apply-remove-normalize-text":
            return

        rationale_input = self.query_one("#architecture-rationale", Input)
        runtime_input = self.query_one("#runtime-input", Input)
        status = self.query_one("#architecture-apply-status", Static)

        try:
            presentation = self.controller.apply_pending_remove_normalize_text(
                rationale_input.value,
                runtime_input.value,
            )
        except Exception as exc:
            status.update(f"Apply failed: {exc}")
            return

        self.presentation = presentation
        self.query_one(WorkspaceDetail).replace_presentation(presentation)
        self.query_one(ArchitecturePreviewDetail).clear_presentation()
        controls = self.query_one("#architecture-apply-controls", ArchitectureApplyControls)
        await controls.remove()

        if len(self.query("#export-refresh-controls")) == 0:
            slot = self.query_one("#export-refresh-slot", Vertical)
            await slot.mount(ExportRefreshControls())


def create_workspace_shell(
    presentation: WorkspacePresentation,
    *,
    controller: WorkspaceController | None = None,
) -> WorkspaceShell:
    """Create the local Workspace shell over application-owned evidence/state."""

    return WorkspaceShell(
        presentation,
        controller=controller,
    )
