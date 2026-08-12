from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.runtime import run_materialized_workspace

from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .presentation import WorkspacePresentation
from .query import query_workspace_presentation


@dataclass(frozen=True, slots=True)
class WorkspaceRerunResult:
    """Fresh runtime and presentation evidence from one existing Workspace rerun."""

    run: BuildAndRunResult
    presentation: WorkspacePresentation


def rerun_workspace(
    workspace_root: Path,
    run: BuildAndRunResult,
    text: str,
    *,
    export: WorkspaceExportResult | None = None,
) -> WorkspaceRerunResult:
    """Rerun one already-built Workspace and return fresh presentation evidence.

    The supplied live evidence is first checked against the persisted Workspace
    through the existing query boundary. Only then is the already-materialized
    generated entrypoint executed. The existing BuildResult is reused exactly;
    this operation does not compile, classify generation status, materialize,
    mutate revisions, export, or infer readiness.
    """

    root = workspace_root.resolve()

    # Reject stale or mismatched live evidence before generated code executes.
    query_workspace_presentation(
        root,
        run=run,
        export=export,
    )

    runtime_result = run_materialized_workspace(
        run.build.repository,
        root,
        text,
    )
    updated_run = BuildAndRunResult(
        build=run.build,
        runtime_result=runtime_result,
    )
    presentation = query_workspace_presentation(
        root,
        run=updated_run,
        export=export,
    )

    return WorkspaceRerunResult(
        run=updated_run,
        presentation=presentation,
    )
