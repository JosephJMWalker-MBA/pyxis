from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.compiler import (
    build_generation_manifest,
    compile_repository,
    generation_manifest_sha256,
)
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.exporting import build_export_plan
from pyxis.rir import build_repository_ir


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_export_plan_is_pure_and_identifies_exact_compiler_products(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Pure export planning proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)
    monkeypatch.chdir(tmp_path)

    plan = build_export_plan(repository, artifacts, manifest)

    assert plan.repository_id == repository.repository_id
    assert plan.workspace_id == repository.workspace.workspace_id
    assert plan.rir_sha256 == manifest.rir_sha256
    assert plan.generation_manifest_sha256 == generation_manifest_sha256(manifest)
    assert plan.canonical_path == "authoring/canonical/workspace.json"
    assert plan.rir_path == "generated/repository.rir.json"
    assert plan.generation_manifest_path == "generated/generation.manifest.json"
    assert tuple(product.path for product in plan.compiler_products) == tuple(
        artifact.path for artifact in artifacts
    )
    assert tuple(product.node_sha256 for product in plan.compiler_products) == tuple(
        artifact.node_sha256 for artifact in artifacts
    )
    assert tuple(product.artifact_sha256 for product in plan.compiler_products) == tuple(
        entry.artifact_sha256 for entry in manifest.artifacts
    )
    assert not tuple(tmp_path.rglob("*"))


def test_export_plan_matches_permanent_build_without_mutating_workspace(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Permanent build export-plan proof.",
    )
    build = build_workspace(spec, tmp_path)
    before = _file_snapshot(tmp_path)

    plan = build_export_plan(build.repository, build.artifacts, build.manifest)

    assert tuple(product.path for product in plan.compiler_products) == tuple(
        artifact.path for artifact in build.artifacts
    )
    assert {
        plan.canonical_path,
        plan.rir_path,
        plan.generation_manifest_path,
    } == {
        build.canonical_path.relative_to(tmp_path).as_posix(),
        build.rir_path.relative_to(tmp_path).as_posix(),
        build.manifest_path.relative_to(tmp_path).as_posix(),
    }
    assert _file_snapshot(tmp_path) == before


def test_export_plan_rejects_manifest_from_different_rir() -> None:
    original_spec = create_workspace_spec(
        "Text Lab",
        "Original export RIR proof.",
    )
    original_repository = build_repository_ir(original_spec)
    artifacts = compile_repository(original_repository)
    manifest = build_generation_manifest(original_repository, artifacts)

    different_repository = build_repository_ir(
        create_workspace_spec(
            "Text Lab",
            "Different canonical description changes RIR identity.",
        )
    )

    with pytest.raises(ValueError, match="current Repository RIR"):
        build_export_plan(different_repository, artifacts, manifest)


def test_export_plan_rejects_compiler_product_integrity_mismatch() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Export artifact integrity proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)

    tampered = (
        GeneratedArtifact(
            path=artifacts[0].path,
            source=f"{artifacts[0].source}# not the recorded compiler product\n",
            node_sha256=artifacts[0].node_sha256,
        ),
        *artifacts[1:],
    )

    with pytest.raises(ValueError, match="artifact integrity mismatch"):
        build_export_plan(repository, tampered, manifest)
