from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from pyxis.compiler import (
    generation_manifest_sha256,
    load_generation_manifest,
    repository_ir_sha256,
)
from pyxis.rir import load_repository_ir

from .plan import ExportPlan


@dataclass(frozen=True, slots=True)
class VerifiedExportCompilerProduct:
    """Identity evidence for one compiler product read from an exported tree."""

    path: str
    node_sha256: str
    artifact_sha256: str


@dataclass(frozen=True, slots=True)
class ExportIdentityVerificationResult:
    """Immutable identity evidence derived independently from exported files.

    This result verifies RIR, generation-manifest, and compiler-product identity.
    It does not execute exported code, verify runtime behavior, or claim READY.
    """

    export_root: Path
    repository_id: str
    workspace_id: str
    rir_sha256: str
    generation_manifest_sha256: str
    compiler_products: tuple[VerifiedExportCompilerProduct, ...]


def _resolve_planned_path(path_value: str, root: Path) -> Path:
    if not path_value:
        raise ValueError("Export verification paths must be non-empty.")

    relative = Path(path_value)
    if relative == Path(".") or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"Export verification path must remain relative: {path_value!r}."
        )

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Export verification path escapes the root: {path_value!r}.")
    return target


def verify_export_identity(
    plan: ExportPlan,
    export_root: Path,
) -> ExportIdentityVerificationResult:
    """Verify exact exported compiler identity without compilation or execution."""

    root = export_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Export root does not exist: {root}")

    evidence_paths = (
        plan.canonical_path,
        plan.rir_path,
        plan.generation_manifest_path,
    )
    product_paths = tuple(product.path for product in plan.compiler_products)
    planned_paths = (*evidence_paths, *product_paths)
    if len(set(planned_paths)) != len(planned_paths):
        raise ValueError("Export verification plan paths must be unique.")

    for path_value in planned_paths:
        target = _resolve_planned_path(path_value, root)
        if not target.is_file():
            raise FileNotFoundError(
                f"Planned exported file does not exist: {path_value!r}."
            )

    repository = load_repository_ir(root)
    if repository.repository_id != plan.repository_id:
        raise ValueError("Exported Repository identity does not match the export plan.")
    if repository.workspace.workspace_id != plan.workspace_id:
        raise ValueError("Exported Workspace identity does not match the export plan.")

    rir_sha256 = repository_ir_sha256(repository)
    if rir_sha256 != plan.rir_sha256:
        raise ValueError("Exported RIR identity does not match the export plan.")

    manifest = load_generation_manifest(root)
    if manifest is None:
        raise FileNotFoundError("Exported generation manifest does not exist.")

    manifest_sha256 = generation_manifest_sha256(manifest)
    if manifest_sha256 != plan.generation_manifest_sha256:
        raise ValueError(
            "Exported generation manifest identity does not match the export plan."
        )
    if manifest.rir_sha256 != rir_sha256:
        raise ValueError("Exported generation manifest does not reference the exported RIR.")

    if len(manifest.artifacts) != len(plan.compiler_products):
        raise ValueError(
            "Exported generation manifest does not cover the planned compiler products."
        )

    verified_products: list[VerifiedExportCompilerProduct] = []
    for product, recorded in zip(
        plan.compiler_products,
        manifest.artifacts,
        strict=True,
    ):
        if (
            recorded.path != product.path
            or recorded.node_sha256 != product.node_sha256
            or recorded.artifact_sha256 != product.artifact_sha256
        ):
            raise ValueError(
                f"Exported generation evidence disagrees with the plan for {product.path!r}."
            )

        product_path = _resolve_planned_path(product.path, root)
        artifact_sha256 = hashlib.sha256(product_path.read_bytes()).hexdigest()
        if artifact_sha256 != product.artifact_sha256:
            raise ValueError(
                f"Exported compiler product identity does not match the plan: "
                f"{product.path!r}."
            )

        verified_products.append(
            VerifiedExportCompilerProduct(
                path=product.path,
                node_sha256=product.node_sha256,
                artifact_sha256=artifact_sha256,
            )
        )

    return ExportIdentityVerificationResult(
        export_root=root,
        repository_id=repository.repository_id,
        workspace_id=repository.workspace.workspace_id,
        rir_sha256=rir_sha256,
        generation_manifest_sha256=manifest_sha256,
        compiler_products=tuple(verified_products),
    )
