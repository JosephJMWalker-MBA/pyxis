from pathlib import Path

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler import (
    build_generation_manifest,
    compile_repository,
    materialize_artifacts,
    reconcile_materialized_artifacts,
)
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.rir.model import build_repository_ir


def test_materialize_writes_exact_compiler_artifact_set(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Filesystem materialization proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)

    written = materialize_artifacts(artifacts, tmp_path)

    assert tuple(path.relative_to(tmp_path).as_posix() for path in written) == tuple(
        artifact.path for artifact in artifacts
    )
    for artifact, path in zip(artifacts, written, strict=True):
        assert path.read_text(encoding="utf-8") == artifact.source


def test_materialize_does_not_recompile_or_mutate_artifacts(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Materializer boundary proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    before = artifacts

    materialize_artifacts(artifacts, tmp_path)

    assert artifacts == before
    assert (
        tmp_path / "generated/workspaces/text_lab/main.py"
    ).read_text(encoding="utf-8") == artifacts[-1].source


def test_materialize_rejects_path_escape(tmp_path: Path) -> None:
    unsafe = GeneratedArtifact(
        path="../outside.py",
        source="print('should not be written')\n",
        node_sha256="unsafe",
    )

    with pytest.raises(ValueError, match="relative to the destination"):
        materialize_artifacts((unsafe,), tmp_path)

    assert not (tmp_path.parent / "outside.py").exists()


def test_reconcile_removes_only_stale_manifest_owned_artifacts(
    tmp_path: Path,
) -> None:
    current_spec = create_workspace_spec(
        "Text Lab",
        "Manifest-owned stale artifact proof.",
    )
    current_repository = build_repository_ir(current_spec)
    current_artifacts = compile_repository(current_repository)
    previous_manifest = build_generation_manifest(
        current_repository,
        current_artifacts,
    )
    materialize_artifacts(current_artifacts, tmp_path)

    untracked = tmp_path / "generated/untracked.py"
    untracked.write_text("# not declared by the compiler manifest\n", encoding="utf-8")

    proposed_spec = current_spec.without_capability("normalize_text")
    proposed_repository = build_repository_ir(proposed_spec)
    proposed_artifacts = compile_repository(proposed_repository)

    result = reconcile_materialized_artifacts(
        proposed_artifacts,
        previous_manifest,
        tmp_path,
    )

    assert tuple(path.relative_to(tmp_path).as_posix() for path in result.written_paths) == (
        "generated/capabilities/inspect_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert tuple(path.relative_to(tmp_path).as_posix() for path in result.removed_paths) == (
        "generated/capabilities/normalize_text.py",
    )
    assert not (tmp_path / "generated/capabilities/normalize_text.py").exists()
    assert untracked.read_text(encoding="utf-8") == (
        "# not declared by the compiler manifest\n"
    )
