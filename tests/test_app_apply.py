import importlib
import json
from pathlib import Path

import pytest

from pyxis.app import (
    apply_remove_normalize_text,
    build_workspace,
    preview_remove_normalize_text,
)
from pyxis.authoring import (
    create_workspace_spec,
    load_workspace_spec,
    persist_workspace_spec,
)


apply_module = importlib.import_module("pyxis.app.apply")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_apply_remove_normalize_text_records_rationale_then_builds_proposed_state(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "First real architecture Apply proof.",
    )
    build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)

    result = apply_remove_normalize_text(
        preview,
        tmp_path,
        "Remove normalization after reviewing the predicted consequences.",
    )

    assert result.revision.operation == "remove_capability:normalize_text"
    assert result.revision.rationale == (
        "Remove normalization after reviewing the predicted consequences."
    )
    assert result.revision.parent_revision_id is None
    assert result.revision_log_path == tmp_path.resolve() / "revisions/events.jsonl"
    assert [
        json.loads(line)
        for line in result.revision_log_path.read_text(encoding="utf-8").splitlines()
    ] == [result.revision.to_dict()]

    assert load_workspace_spec(tmp_path) == preview.proposed_spec
    assert result.build.repository == preview.proposed_repository
    assert tuple(path.relative_to(tmp_path).as_posix() for path in result.build.removed_paths) == (
        "generated/capabilities/normalize_text.py",
    )
    assert not (tmp_path / "generated/capabilities/normalize_text.py").exists()
    assert (tmp_path / "generated/capabilities/inspect_text.py").is_file()
    assert (tmp_path / "generated/workspaces/text_lab/main.py").is_file()
    assert tuple(entry.path for entry in result.build.manifest.artifacts) == (
        "generated/capabilities/inspect_text.py",
        "generated/workspaces/text_lab/main.py",
    )


def test_apply_requires_rationale_before_any_mutation(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Apply rationale boundary proof.",
    )
    build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)
    before = _file_snapshot(tmp_path)

    with pytest.raises(ValueError, match="rationale"):
        apply_remove_normalize_text(preview, tmp_path, "   ")

    assert _file_snapshot(tmp_path) == before
    assert not (tmp_path / "revisions/events.jsonl").exists()


def test_apply_rejects_stale_preview_without_mutation(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Stale preview guard proof.",
    )
    build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)

    persist_workspace_spec(preview.proposed_spec, tmp_path)
    before = _file_snapshot(tmp_path)

    with pytest.raises(ValueError, match="no longer matches"):
        apply_remove_normalize_text(
            preview,
            tmp_path,
            "This stale preview must not be applied.",
        )

    assert _file_snapshot(tmp_path) == before
    assert not (tmp_path / "revisions/events.jsonl").exists()


def test_apply_appends_revision_before_delegating_build(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Apply ordering proof.",
    )
    build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)
    build_sentinel = object()

    def fake_build_workspace(proposed_spec, destination_root):
        log_path = destination_root.resolve() / "revisions/events.jsonl"
        assert log_path.is_file()
        entries = [
            json.loads(line)
            for line in log_path.read_text(encoding="utf-8").splitlines()
        ]
        assert len(entries) == 1
        assert entries[0]["rationale"] == "Record intent before canonical mutation."
        assert proposed_spec == preview.proposed_spec
        return build_sentinel

    monkeypatch.setattr(apply_module, "build_workspace", fake_build_workspace)

    result = apply_remove_normalize_text(
        preview,
        tmp_path,
        "Record intent before canonical mutation.",
    )

    assert result.build is build_sentinel
    assert load_workspace_spec(tmp_path) == spec
