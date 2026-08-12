from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from pyxis.compiler import repository_ir_sha256
from pyxis.rir import load_repository_ir
from pyxis.runtime import run_materialized_workspace

from .plan import ExportPlan


@dataclass(frozen=True, slots=True)
class ExportRuntimeVerificationResult:
    """Observable evidence that exported runtime behavior matches its source.

    This result records successful behavior equivalence only. It does not verify
    exported artifact identity, installability, or READY state.
    """

    source_root: Path
    export_root: Path
    repository_id: str
    workspace_id: str
    input_sha256: str
    source_result: dict[str, object]
    export_result: dict[str, object]


def verify_export_runtime(
    plan: ExportPlan,
    source_root: Path,
    export_root: Path,
    text: str,
) -> ExportRuntimeVerificationResult:
    """Execute source and exported Workspaces and require equivalent behavior.

    Both Repository IR objects are reloaded from their respective persisted
    trees. Their deterministic identities must match the export plan before
    execution. This function does not compile, write package metadata, verify
    full export identity, or claim READY.
    """

    source = source_root.resolve()
    exported = export_root.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Source Workspace root does not exist: {source}")
    if not exported.is_dir():
        raise FileNotFoundError(f"Export root does not exist: {exported}")
    if (
        source == exported
        or source in exported.parents
        or exported in source.parents
    ):
        raise ValueError("Runtime verification requires separate source and export trees.")

    source_repository = load_repository_ir(source)
    exported_repository = load_repository_ir(exported)

    for label, repository in (
        ("Source", source_repository),
        ("Exported", exported_repository),
    ):
        if repository.repository_id != plan.repository_id:
            raise ValueError(f"{label} Repository identity does not match the export plan.")
        if repository.workspace.workspace_id != plan.workspace_id:
            raise ValueError(f"{label} Workspace identity does not match the export plan.")
        if repository_ir_sha256(repository) != plan.rir_sha256:
            raise ValueError(f"{label} RIR identity does not match the export plan.")

    source_result = run_materialized_workspace(source_repository, source, text)
    export_result = run_materialized_workspace(exported_repository, exported, text)
    if export_result != source_result:
        raise ValueError(
            "Exported runtime behavior does not match the original materialized Workspace."
        )

    return ExportRuntimeVerificationResult(
        source_root=source,
        export_root=exported,
        repository_id=exported_repository.repository_id,
        workspace_id=exported_repository.workspace.workspace_id,
        input_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        source_result=source_result,
        export_result=export_result,
    )
