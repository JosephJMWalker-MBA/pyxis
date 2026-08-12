from __future__ import annotations

from pathlib import Path

from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .operations import rerun_workspace
from .presentation import WorkspacePresentation


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
