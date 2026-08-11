from dataclasses import replace

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler.repository import compile_repository
from pyxis.rir.model import build_repository_ir


def test_compile_repository_returns_complete_ordered_artifact_set() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Complete compiler result proof.",
    )
    repository = build_repository_ir(spec)

    artifacts = compile_repository(repository)

    assert tuple(artifact.path for artifact in artifacts) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )


def test_compile_repository_is_deterministic_and_non_mutating() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Repository compiler boundary proof.",
    )
    repository = build_repository_ir(spec)
    before = repository.to_dict()

    first = compile_repository(repository)
    second = compile_repository(repository)

    assert first == second
    assert repository.to_dict() == before


def test_compile_repository_respects_rir_capability_order() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Ordered fan-out proof.",
    )
    repository = build_repository_ir(spec)
    reversed_repository = replace(
        repository,
        workspace=replace(
            repository.workspace,
            capabilities=("normalize_text", "inspect_text"),
        ),
    )

    artifacts = compile_repository(reversed_repository)

    assert tuple(artifact.path for artifact in artifacts) == (
        "generated/capabilities/normalize_text.py",
        "generated/capabilities/inspect_text.py",
        "generated/workspaces/text_lab/main.py",
    )


def test_compile_repository_rejects_unknown_capability() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Unknown capability boundary proof.",
    )
    repository = build_repository_ir(spec)
    unknown_repository = replace(
        repository,
        workspace=replace(
            repository.workspace,
            capabilities=("inspect_text", "not_real"),
        ),
    )

    with pytest.raises(ValueError, match="not_real"):
        compile_repository(unknown_repository)
