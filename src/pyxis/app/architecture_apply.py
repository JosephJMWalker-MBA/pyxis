from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from pyxis.revisions import canonical_sha256
from pyxis.runtime import run_materialized_workspace

from .apply import ApplyResult, apply_add_split_lines, apply_remove_normalize_text
from .architecture_reconciliation import (
    ArchitectureConsequenceReconciliationPresentation,
    create_architecture_consequence_reconciliation,
)
from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .presentation import WorkspacePresentation
from .preview import ArchitecturePreview
from .preview_presentation import create_architecture_preview_presentation
from .query import query_workspace_presentation


@dataclass(frozen=True, slots=True)
class WorkspaceArchitectureApplyResult:
    """Fresh evidence produced by one governed architectural apply operation."""

    apply: ApplyResult
    run: BuildAndRunResult
    presentation: WorkspacePresentation
    reconciliation: ArchitectureConsequenceReconciliationPresentation


def _apply_workspace_architecture_edit(
    workspace_root: Path,
    preview: ArchitecturePreview,
    current_run: BuildAndRunResult,
    rationale: str,
    text: str,
    *,
    export: WorkspaceExportResult | None,
    apply_builder: Callable[[ArchitecturePreview, Path, str], ApplyResult],
) -> WorkspaceArchitectureApplyResult:
    """Apply one concrete retained preview through shared live-state orchestration."""

    clean_rationale = rationale.strip()
    if not clean_rationale:
        raise ValueError("Architecture rationale is required before apply.")

    root = workspace_root.resolve()
    current_presentation = query_workspace_presentation(
        root,
        run=current_run,
        export=export,
    )
    if (
        canonical_sha256(preview.current_spec)
        != current_presentation.canonical.canonical_sha256
    ):
        raise ValueError("Pending preview does not match current canonical Workspace state.")

    proposed_presentation = create_architecture_preview_presentation(preview)
    applied = apply_builder(
        preview,
        root,
        clean_rationale,
    )
    runtime_result = run_materialized_workspace(
        applied.build.repository,
        root,
        text,
    )
    run = BuildAndRunResult(
        build=applied.build,
        runtime_result=runtime_result,
    )
    presentation = query_workspace_presentation(
        root,
        run=run,
        export=None,
    )
    reconciliation = create_architecture_consequence_reconciliation(
        proposed_presentation,
        applied,
        presentation,
    )

    return WorkspaceArchitectureApplyResult(
        apply=applied,
        run=run,
        presentation=presentation,
        reconciliation=reconciliation,
    )


def apply_workspace_remove_normalize_text(
    workspace_root: Path,
    preview: ArchitecturePreview,
    current_run: BuildAndRunResult,
    rationale: str,
    text: str,
    *,
    export: WorkspaceExportResult | None = None,
) -> WorkspaceArchitectureApplyResult:
    """Apply one retained normalize_text-removal preview and rerun the result.

    The operation consumes the exact typed preview supplied by the application
    controller. Current run/export evidence is preflighted before mutation. The
    existing governed apply path owns revision/canonical/compiler mutation. A
    fresh runtime result and presentation are then produced from the new build.

    Pre-change export evidence is intentionally not carried into the post-apply
    presentation because compiler products and RIR identity have changed.
    """

    return _apply_workspace_architecture_edit(
        workspace_root,
        preview,
        current_run,
        rationale,
        text,
        export=export,
        apply_builder=apply_remove_normalize_text,
    )


def apply_workspace_add_split_lines(
    workspace_root: Path,
    preview: ArchitecturePreview,
    current_run: BuildAndRunResult,
    rationale: str,
    text: str,
    *,
    export: WorkspaceExportResult | None = None,
) -> WorkspaceArchitectureApplyResult:
    """Apply one retained split_lines-addition preview and rerun the result."""

    return _apply_workspace_architecture_edit(
        workspace_root,
        preview,
        current_run,
        rationale,
        text,
        export=export,
        apply_builder=apply_add_split_lines,
    )
