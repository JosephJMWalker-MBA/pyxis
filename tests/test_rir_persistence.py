import json
from pathlib import Path

import pytest

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.rir import (
    build_repository_ir,
    load_repository_ir,
    persist_repository_ir,
)


def test_persist_repository_ir_writes_deterministic_inspectable_json(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Inspectable RIR persistence proof.",
    )
    repository = build_repository_ir(spec)

    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_path = persist_repository_ir(repository, first_root)
    second_path = persist_repository_ir(repository, second_root)

    assert first_path == first_root.resolve() / "generated/repository.rir.json"
    assert second_path == second_root.resolve() / "generated/repository.rir.json"
    assert first_path.read_text(encoding="utf-8") == second_path.read_text(
        encoding="utf-8"
    )
    assert json.loads(first_path.read_text(encoding="utf-8")) == {
        "schema_version": "0.1",
        "repository_id": "text-lab",
        "workspace": {
            "workspace_id": "text_lab",
            "name": "Text Lab",
            "description": "Inspectable RIR persistence proof.",
            "entrypoint": "main.py",
            "capabilities": ["inspect_text", "normalize_text"],
        },
    }


def test_load_repository_ir_round_trips_persisted_rir(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Persisted RIR loading proof.",
    )
    repository = build_repository_ir(spec)
    persist_repository_ir(repository, tmp_path)

    loaded = load_repository_ir(tmp_path)

    assert loaded == repository


def test_load_repository_ir_rejects_malformed_shape(tmp_path: Path) -> None:
    rir_path = tmp_path / "generated/repository.rir.json"
    rir_path.parent.mkdir(parents=True)
    rir_path.write_text('{"schema_version":"0.1"}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="top-level shape"):
        load_repository_ir(tmp_path)


def test_persist_repository_ir_does_not_mutate_or_compile(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "RIR filesystem boundary proof.",
    )
    repository = build_repository_ir(spec)
    before = repository.to_dict()

    rir_path = persist_repository_ir(repository, tmp_path)

    assert repository.to_dict() == before
    assert tuple(path for path in tmp_path.rglob("*") if path.is_file()) == (rir_path,)
    assert not tuple(tmp_path.rglob("*.py"))
