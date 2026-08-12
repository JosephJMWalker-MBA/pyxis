from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .plan import ExportPlan
from .runtime import ExportRuntimeVerificationResult, verify_export_runtime
from .verify import ExportIdentityVerificationResult, verify_export_identity


ExportReadiness = Literal["READY"]


@dataclass(frozen=True, slots=True)
class ExportVerificationResult:
    """Evidence-backed export verification from identity and runtime proofs.

    READY is derived only after both existing verification paths succeed for the
    same export tree, Repository, and Workspace. This result does not compile,
    package, install, or add verification files to either tree.
    """

    readiness: ExportReadiness
    identity: ExportIdentityVerificationResult
    runtime: ExportRuntimeVerificationResult


def verify_export(
    plan: ExportPlan,
    source_root: Path,
    export_root: Path,
    text: str,
) -> ExportVerificationResult:
    """Derive READY only from successful identity and runtime verification."""

    identity = verify_export_identity(plan, export_root)
    runtime = verify_export_runtime(plan, source_root, export_root, text)

    if identity.export_root != runtime.export_root:
        raise RuntimeError("Export verification evidence refers to different export roots.")
    if identity.repository_id != runtime.repository_id:
        raise RuntimeError("Export verification evidence refers to different Repositories.")
    if identity.workspace_id != runtime.workspace_id:
        raise RuntimeError("Export verification evidence refers to different Workspaces.")

    return ExportVerificationResult(
        readiness="READY",
        identity=identity,
        runtime=runtime,
    )
