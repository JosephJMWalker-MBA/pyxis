from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.exporting import (
    ExportMaterializationResult,
    ExportVerificationResult,
    build_export_plan,
    materialize_export_plan,
    verify_export,
)

from .build import BuildResult


@dataclass(frozen=True, slots=True)
class WorkspaceExportResult:
    """Observable result of exporting and verifying one existing Workspace build."""

    materialization: ExportMaterializationResult
    verification: ExportVerificationResult


def export_workspace(
    build: BuildResult,
    source_root: Path,
    destination_root: Path,
    text: str,
) -> WorkspaceExportResult:
    """Plan, materialize, and verify portable output from one existing build.

    This is application orchestration only. Export planning owns compiler-product
    identity, export materialization owns exact-byte copying, and export
    verification owns READY evidence. This function does not compile, rebuild,
    reinterpret generated source, add package metadata, or execute a shadow path.
    """

    plan = build_export_plan(
        build.repository,
        build.artifacts,
        build.manifest,
    )
    materialization = materialize_export_plan(
        plan,
        source_root,
        destination_root,
    )
    verification = verify_export(
        plan,
        source_root,
        destination_root,
        text,
    )

    return WorkspaceExportResult(
        materialization=materialization,
        verification=verification,
    )
