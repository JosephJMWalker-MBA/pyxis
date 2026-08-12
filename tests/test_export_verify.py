import importlib
import json
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    materialize_export_plan,
    verify_export_identity,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
runtime_loader_module = importlib.import_module("pyxis.runtime.loader")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_export(tmp_path: Path):
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Exported identity verification proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(plan, source, destination)
    return plan, destination


def test_verify_export_identity_reads_exported_evidence_without_compile_or_runtime(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, destination = _build_export(tmp_path)
    before = _file_snapshot(destination)

    def fail_compile(*args, **kwargs):
        raise AssertionError("Export identity verification must not compile.")

    def fail_runtime(*args, **kwargs):
        raise AssertionError("Export identity verification must not execute runtime.")

    monkeypatch.setattr(compiler_repository_module, "compile_repository", fail_compile)
    monkeypatch.setattr(runtime_loader_module, "run_materialized_workspace", fail_runtime)

    result = verify_export_identity(plan, destination)

    assert result.export_root == destination.resolve()
    assert result.repository_id == plan.repository_id
    assert result.workspace_id == plan.workspace_id
    assert result.rir_sha256 == plan.rir_sha256
    assert result.generation_manifest_sha256 == plan.generation_manifest_sha256
    assert tuple(product.path for product in result.compiler_products) == tuple(
        product.path for product in plan.compiler_products
    )
    assert tuple(product.node_sha256 for product in result.compiler_products) == tuple(
        product.node_sha256 for product in plan.compiler_products
    )
    assert tuple(product.artifact_sha256 for product in result.compiler_products) == tuple(
        product.artifact_sha256 for product in plan.compiler_products
    )
    assert not hasattr(result, "ready")
    assert _file_snapshot(destination) == before


def test_verify_export_identity_rejects_post_export_compiler_product_tampering(
    tmp_path: Path,
) -> None:
    plan, destination = _build_export(tmp_path)
    product = plan.compiler_products[0]
    product_path = destination / product.path
    product_path.write_bytes(b"# altered after export materialization\n")
    before = _file_snapshot(destination)

    with pytest.raises(ValueError, match="compiler product identity"):
        verify_export_identity(plan, destination)

    assert _file_snapshot(destination) == before


def test_verify_export_identity_rejects_post_export_rir_tampering(
    tmp_path: Path,
) -> None:
    plan, destination = _build_export(tmp_path)
    rir_path = destination / plan.rir_path
    payload = json.loads(rir_path.read_text(encoding="utf-8"))
    payload["workspace"]["description"] = "Changed only after export."
    rir_path.write_text(
        f"{json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    before = _file_snapshot(destination)

    with pytest.raises(ValueError, match="RIR identity"):
        verify_export_identity(plan, destination)

    assert _file_snapshot(destination) == before


def test_verify_export_identity_rejects_post_export_manifest_tampering(
    tmp_path: Path,
) -> None:
    plan, destination = _build_export(tmp_path)
    manifest_path = destination / plan.generation_manifest_path
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["rir_sha256"] = "changed-after-export"
    manifest_path.write_text(
        f"{json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    before = _file_snapshot(destination)

    with pytest.raises(ValueError, match="generation manifest identity"):
        verify_export_identity(plan, destination)

    assert _file_snapshot(destination) == before


def test_verify_export_identity_requires_all_planned_evidence_files(
    tmp_path: Path,
) -> None:
    plan, destination = _build_export(tmp_path)
    (destination / plan.canonical_path).unlink()

    with pytest.raises(FileNotFoundError, match="Planned exported file"):
        verify_export_identity(plan, destination)
