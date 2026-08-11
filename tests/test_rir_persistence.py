import json
from pathlib import Path

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.rir import build_repository_ir, persist_repository_ir


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
