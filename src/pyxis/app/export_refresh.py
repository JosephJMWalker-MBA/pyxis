from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .build import BuildAndRunResult
from .export import WorkspaceExportResult, export_workspace
from .presentation import WorkspacePresentation
from .query import query_workspace_presentation


@dataclass(frozen=True, slots=True)
class WorkspaceExportRefreshResult:
    """Fresh READY evidence produced from one current live Workspace build."""

    export: WorkspaceExportResult
    presentation: WorkspacePresentation


def refresh_workspace_export(
    workspace_root: Path,
    current_run: BuildAndRunResult,
    destination_root: Path,
    text: str,
) -> WorkspaceExportRefreshResult:
    """Export and verify the exact current Workspace build into a fresh destination.

    Current live run evidence is preflighted against persisted Workspace state
    before export begins. The existing export orchestration remains the owner of
    planning, exact-byte materialization, and READY verification. This operation
    does not compile, mutate canonical intent, append revisions, or infer READY
    from filesystem presence.
    """

    root = workspace_root.resolve()
    query_workspace_presentation(
        root,
        run=current_run,
        export=None,
    )

    export = export_workspace(
        current_run.build,
        root,
        destination_root,
        text,
    )
    presentation = query_workspace_presentation(
        root,
        run=current_run,
        export=export,
    )

    return WorkspaceExportRefreshResult(
        export=export,
        presentation=presentation,
    )
