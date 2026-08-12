from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring import load_workspace_spec

from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .preview import ArchitecturePreview, preview_remove_normalize_text
from .preview_presentation import (
    ArchitecturePreviewPresentation,
    create_architecture_preview_presentation,
)
from .query import query_workspace_presentation


@dataclass(frozen=True, slots=True)
class WorkspaceArchitecturePreviewResult:
    """Typed pending preview plus immutable presentation-safe preview evidence."""

    preview: ArchitecturePreview
    presentation: ArchitecturePreviewPresentation


def preview_workspace_remove_normalize_text(
    workspace_root: Path,
    run: BuildAndRunResult,
    *,
    export: WorkspaceExportResult | None = None,
) -> WorkspaceArchitecturePreviewResult:
    """Preview normalize_text removal for one coherent existing Workspace.

    Current live run/export evidence is preflighted through the existing query
    boundary before canonical intent is loaded for the in-memory preview. The
    operation performs no canonical write, compilation, runtime execution,
    revision append, export, or readiness mutation.
    """

    root = workspace_root.resolve()
    current_presentation = query_workspace_presentation(
        root,
        run=run,
        export=export,
    )
    spec = load_workspace_spec(root)
    preview = preview_remove_normalize_text(spec)
    presentation = create_architecture_preview_presentation(preview)

    if (
        presentation.current.canonical_sha256
        != current_presentation.canonical.canonical_sha256
    ):
        raise RuntimeError(
            "Canonical Workspace state changed while architecture preview was being assembled."
        )

    return WorkspaceArchitecturePreviewResult(
        preview=preview,
        presentation=presentation,
    )
