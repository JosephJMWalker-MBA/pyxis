import importlib
import json
from pathlib import Path
from types import SimpleNamespace

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
from pyxis.compiler import generation_manifest_sha256


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

    assert result.completion.revision_id == result.revision.revision_id
    assert result.completion.after_canonical_sha256 == (
        result.revision.after_canonical_sha256
    )
    assert result.completion.rir_sha256 == result.build.manifest.rir_sha256
    assert result.completion.generation_manifest_sha256 == (
        generation_manifest_sha256(result.build.manifest)
    )
    assert result.completion_log_path == (
        tmp_path.resolve() / "revisions/completions.jsonl"
    )
    assert [
        json.loads(line)
        for line in result.completion_log_path.read_text(encoding="utf-8").splitlines()
    ] == [result.completion.to_dict()]


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
    assert not (tmp_path / "revisions/completions.jsonl").exists()


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
    assert not (tmp_path / "revisions/completions.jsonl").exists()


def test_apply_appends_revision_before_build_and_completion_after_build(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Apply ordering proof.",
    )
    baseline = build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)

    def fake_build_workspace(proposed_spec, destination_root):
        revision_log_path = destination_root.resolve() / "revisions/events.jsonl"
        completion_log_path = destination_root.resolve() / "revisions/completions.jsonl"
        assert revision_log_path.is_file()
        assert not completion_log_path.exists()
        entries = [
            json.loads(line)
            for line in revision_log_path.read_text(encoding="utf-8").splitlines()
        ]
        assert len(entries) == 1
        assert entries[0]["rationale"] == "Record intent before canonical mutation."
        assert proposed_spec == preview.proposed_spec
        return SimpleNamespace(manifest=baseline.manifest)

    monkeypatch.setattr(apply_module, "build_workspace", fake_build_workspace)

    result = apply_remove_normalize_text(
        preview,
        tmp_path,
        "Record intent before canonical mutation.",
    )

    assert result.completion_log_path.is_file()
    assert load_workspace_spec(tmp_path) == spec


def test_apply_build_failure_records_intent_without_completion(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Failed Apply completion boundary proof.",
    )
    build_workspace(spec, tmp_path)
    preview = preview_remove_normalize_text(spec)

    def fail_build_workspace(proposed_spec, destination_root):
        assert proposed_spec == preview.proposed_spec
        assert (destination_root / "revisions/events.jsonl").is_file()
        assert not (destination_root / "revisions/completions.jsonl").exists()
        raise RuntimeError("simulated build failure")

    monkeypatch.setattr(apply_module, "build_workspace", fail_build_workspace)

    with pytest.raises(RuntimeError, match="simulated build failure"):
        apply_remove_normalize_text(
            preview,
            tmp_path,
            "Preserve attempted intent even if the build fails.",
        )

    revision_log_path = tmp_path / "revisions/events.jsonl"
    assert revision_log_path.is_file()
    assert len(revision_log_path.read_text(encoding="utf-8").splitlines()) == 1
    assert not (tmp_path / "revisions/completions.jsonl").exists()
    assert load_workspace_spec(tmp_path) == spec
