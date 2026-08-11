import json
from pathlib import Path

from pyxis.authoring import create_workspace_spec, persist_workspace_spec


def test_persist_workspace_spec_writes_only_canonical_authoring_state(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Canonical authoring persistence proof.",
    )

    canonical_path = persist_workspace_spec(spec, tmp_path)

    assert canonical_path == (
        tmp_path.resolve() / "authoring/canonical/workspace.json"
    )
    assert json.loads(canonical_path.read_text(encoding="utf-8")) == {
        "workspace_id": "text_lab",
        "name": "Text Lab",
        "description": "Canonical authoring persistence proof.",
        "capabilities": ["inspect_text", "normalize_text"],
    }
    assert not (tmp_path / "generated").exists()


def test_persist_workspace_spec_is_deterministic_and_non_mutating(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Deterministic canonical persistence proof.",
    )
    before = spec.to_canonical_dict()

    first = persist_workspace_spec(spec, tmp_path / "first")
    second = persist_workspace_spec(spec, tmp_path / "second")

    assert first.read_bytes() == second.read_bytes()
    assert spec.to_canonical_dict() == before
