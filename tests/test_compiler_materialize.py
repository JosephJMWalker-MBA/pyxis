from pathlib import Path

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler import compile_repository, materialize_artifacts
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
