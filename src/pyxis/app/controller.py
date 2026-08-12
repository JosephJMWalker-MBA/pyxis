from __future__ import annotations

from pathlib import Path

from .architecture_preview import preview_workspace_remove_normalize_text
from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .operations import rerun_workspace
from .presentation import WorkspacePresentation
from .preview import ArchitecturePreview
from .preview_presentation import ArchitecturePreviewPresentation


class WorkspaceRuntimeController:
    """Application-owned live state for runtime-only Workspace interactions.

    The controller retains transient run evidence between UI operations while
    delegating the actual operation to ``rerun_workspace()``. It owns no
    compiler, runtime, revision, export, persistence, or presentation logic.
    """

    def __init__(
        self,
        workspace_root: Path,
        run: BuildAndRunResult,
        *,
        export: WorkspaceExportResult | None = None,
    ) -> None:
        self._workspace_root = workspace_root.resolve()
        self._run = run
        self._export = export

    @property
    def current_run(self) -> BuildAndRunResult:
        """Return the current transient run evidence retained by the controller."""

        return self._run

    def rerun(self, text: str) -> WorkspacePresentation:
        """Execute one runtime-only rerun and retain its fresh run evidence."""

        result = rerun_workspace(
            self._workspace_root,
            self._run,
            text,
            export=self._export,
        )
        self._run = result.run
        return result.presentation


class WorkspaceArchitecturePreviewController:
    """Application-owned pending state for preview-first architecture changes.

    The controller retains the typed ArchitecturePreview needed by a later
    rationale/apply operation. Its public preview method returns only immutable
    presentation-safe evidence and does not mutate the Workspace.
    """

    def __init__(
        self,
        workspace_root: Path,
        run: BuildAndRunResult,
        *,
        export: WorkspaceExportResult | None = None,
    ) -> None:
        self._workspace_root = workspace_root.resolve()
        self._run = run
        self._export = export
        self._pending_preview: ArchitecturePreview | None = None

    @property
    def pending_preview(self) -> ArchitecturePreview | None:
        """Return the retained typed preview for a later application-owned apply."""

        return self._pending_preview

    def preview_remove_normalize_text(self) -> ArchitecturePreviewPresentation:
        """Create and retain one non-mutating normalize_text removal preview."""

        result = preview_workspace_remove_normalize_text(
            self._workspace_root,
            self._run,
            export=self._export,
        )
        self._pending_preview = result.preview
        return result.presentation
