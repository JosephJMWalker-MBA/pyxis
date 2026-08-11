from dataclasses import replace

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler.artifacts import compile_inspect_text
from pyxis.rir.model import build_repository_ir


def test_compile_inspect_text_is_deterministic() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Smallest compiler artifact proof.",
    )
    repository = build_repository_ir(spec)

    first = compile_inspect_text(repository)
    second = compile_inspect_text(repository)

    assert first == second
    assert first.path == "generated/capabilities/inspect_text.py"
    assert first.node_sha256 in first.source


def test_compile_inspect_text_consumes_rir_without_mutating_it() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Compiler boundary proof.",
    )
    repository = build_repository_ir(spec)
    before = repository.to_dict()

    artifact = compile_inspect_text(repository)

    assert repository.to_dict() == before
    assert "def execute" in artifact.source
    assert "hashlib.sha256" in artifact.source


def test_compile_inspect_text_rejects_missing_capability() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Capability reference proof.",
    )
    repository = build_repository_ir(spec)
    repository_without_inspect = replace(
        repository,
        workspace=replace(
            repository.workspace,
            capabilities=("normalize_text",),
        ),
    )

    with pytest.raises(ValueError, match="inspect_text"):
        compile_inspect_text(repository_without_inspect)
