from __future__ import annotations

from pathlib import Path

from .architecture_apply import apply_workspace_remove_normalize_text
from .architecture_preview import preview_workspace_remove_normalize_text
from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .export_refresh import refresh_workspace_export
from .operations import rerun_workspace
from .presentation import WorkspacePresentation
from .preview import ArchitecturePreview
from .preview_presentation import ArchitecturePreviewPresentation


class WorkspaceController:
    """Single application-owned authority for one live Workspace interaction state.

    The controller owns exactly one current run, one optional current export
    result, and one optional pending architecture preview. It delegates runtime,
    preview, apply, and verified export behavior to the already-proven
    application operations so those operations remain the owners of coherence
    checks and domain effects.
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
    def current_run(self) -> BuildAndRunResult:
        """Return the one current transient run retained for future operations."""

        return self._run

    @property
    def current_export(self) -> WorkspaceExportResult | None:
        """Return READY evidence still valid for the controller's current build."""

        return self._export

    @property
    def pending_preview(self) -> ArchitecturePreview | None:
        """Return the exact proposed architecture retained for a later apply."""

        return self._pending_preview

    def rerun(self, text: str) -> WorkspacePresentation:
        """Rerun the current architecture and advance only live runtime evidence."""

        result = rerun_workspace(
            self._workspace_root,
            self._run,
            text,
            export=self._export,
        )
        self._run = result.run
        return result.presentation

    def preview_remove_normalize_text(self) -> ArchitecturePreviewPresentation:
        """Preview against the same live state used by runtime and later apply."""

        result = preview_workspace_remove_normalize_text(
            self._workspace_root,
            self._run,
            export=self._export,
        )
        self._pending_preview = result.preview
        return result.presentation

    def apply_pending_remove_normalize_text(
        self,
        rationale: str,
        text: str,
    ) -> WorkspacePresentation:
        """Apply the retained preview and advance the one shared live state."""

        preview = self._pending_preview
        if preview is None:
            raise ValueError("No pending architecture preview is available to apply.")

        result = apply_workspace_remove_normalize_text(
            self._workspace_root,
            preview,
            self._run,
            rationale,
            text,
            export=self._export,
        )

        self._run = result.run
        self._export = None
        self._pending_preview = None
        return result.presentation

    def refresh_export(
        self,
        destination_root: Path,
        text: str,
    ) -> WorkspacePresentation:
        """Verify a fresh export of the exact current build and retain READY evidence."""

        result = refresh_workspace_export(
            self._workspace_root,
            self._run,
            destination_root,
            text,
        )
        self._export = result.export
        return result.presentation


class WorkspaceRuntimeController:
    """Application-owned live state for runtime-only Workspace interactions.

    This specialized controller remains for compatibility with the existing
    Textual runtime proof. New combined interaction flows should use
    ``WorkspaceController`` so runtime and architecture operations share one
    live state authority.
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
    """Application-owned state for preview-first architecture changes.

    This specialized controller remains for compatibility with the existing
    Textual preview proof. New combined interaction flows should use
    ``WorkspaceController`` so runtime and architecture operations share one
    live state authority.
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
    def current_run(self) -> BuildAndRunResult:
        """Return the current transient run evidence retained by this controller."""

        return self._run

    @property
    def current_export(self) -> WorkspaceExportResult | None:
        """Return export evidence still valid for the controller's current build."""

        return self._export

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

    def apply_pending_remove_normalize_text(
        self,
        rationale: str,
        text: str,
    ) -> WorkspacePresentation:
        """Apply the exact retained preview and retain fresh post-apply evidence."""

        preview = self._pending_preview
        if preview is None:
            raise ValueError("No pending architecture preview is available to apply.")

        result = apply_workspace_remove_normalize_text(
            self._workspace_root,
            preview,
            self._run,
            rationale,
            text,
            export=self._export,
        )

        self._run = result.run
        self._export = None
        self._pending_preview = None
        return result.presentation
