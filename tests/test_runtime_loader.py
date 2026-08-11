from dataclasses import replace
from pathlib import Path

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler import compile_repository, materialize_artifacts
from pyxis.rir.model import build_repository_ir
from pyxis.runtime import run_materialized_workspace


def test_author_compile_materialize_execute_vertical_slice(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Permanent vertical slice proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    materialize_artifacts(artifacts, tmp_path)

    result = run_materialized_workspace(
        repository,
        tmp_path,
        "  hello   world  ",
    )

    assert set(result) == {"inspect_text", "normalize_text"}
    assert result["inspect_text"]["words"] == 2
    assert result["normalize_text"]["normalized_text"] == "hello world"
    assert result["normalize_text"]["changed"] is True


def test_runtime_does_not_modify_materialized_repository(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Runtime side-effect boundary proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    written = materialize_artifacts(artifacts, tmp_path)
    before = {path: path.read_bytes() for path in written}

    run_materialized_workspace(repository, tmp_path, "hello world")

    after = {path: path.read_bytes() for path in written}
    assert after == before


def test_runtime_respects_rir_capability_composition(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Runtime composition proof.",
    )
    repository = build_repository_ir(spec)
    inspect_only = replace(
        repository,
        workspace=replace(
            repository.workspace,
            capabilities=("inspect_text",),
        ),
    )
    artifacts = compile_repository(inspect_only)
    materialize_artifacts(artifacts, tmp_path)

    result = run_materialized_workspace(
        inspect_only,
        tmp_path,
        "hello world",
    )

    assert set(result) == {"inspect_text"}


def test_runtime_requires_materialized_entrypoint(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Missing entrypoint proof.",
    )
    repository = build_repository_ir(spec)

    with pytest.raises(FileNotFoundError, match="entrypoint"):
        run_materialized_workspace(repository, tmp_path, "hello world")
