from pathlib import Path

import pytest

from pyxis.app import preview_remove_normalize_text
from pyxis.authoring import create_workspace_spec
from pyxis.compiler import compile_repository, materialize_artifacts
from pyxis.rir import build_repository_ir
from pyxis.runtime import run_materialized_workspace


def test_preview_remove_normalize_text_is_in_memory_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Preview-only architectural edit proof.",
    )
    before = spec.to_canonical_dict()
    monkeypatch.chdir(tmp_path)

    preview = preview_remove_normalize_text(spec)

    assert spec.to_canonical_dict() == before
    assert preview.current_spec is spec
    assert preview.proposed_spec is not spec
    assert preview.proposed_spec.capabilities == ("inspect_text",)
    assert preview.proposed_repository.workspace.capabilities == ("inspect_text",)
    assert preview.delta.added_capabilities == ()
    assert preview.delta.removed_capabilities == ("normalize_text",)
    assert preview.delta.added_artifact_paths == ()
    assert preview.delta.removed_artifact_paths == (
        "generated/capabilities/normalize_text.py",
    )
    assert preview.delta.changed_artifact_paths == (
        "generated/workspaces/text_lab/main.py",
    )
    assert preview.delta.added_runtime_keys == ()
    assert preview.delta.removed_runtime_keys == ("normalize_text",)
    assert not tuple(tmp_path.rglob("*"))


def test_preview_predictions_match_real_compiler_and_runtime(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Preview prediction validation proof.",
    )
    current_repository = build_repository_ir(spec)
    preview = preview_remove_normalize_text(spec)

    current_artifacts = compile_repository(current_repository)
    proposed_artifacts = compile_repository(preview.proposed_repository)
    current_by_path = {artifact.path: artifact for artifact in current_artifacts}
    proposed_by_path = {artifact.path: artifact for artifact in proposed_artifacts}

    actual_removed = tuple(
        path for path in current_by_path if path not in proposed_by_path
    )
    actual_added = tuple(
        path for path in proposed_by_path if path not in current_by_path
    )
    actual_changed = tuple(
        path
        for path in current_by_path
        if path in proposed_by_path and current_by_path[path] != proposed_by_path[path]
    )

    assert actual_removed == preview.delta.removed_artifact_paths
    assert actual_added == preview.delta.added_artifact_paths
    assert actual_changed == preview.delta.changed_artifact_paths

    runtime_root = tmp_path / "runtime"
    materialize_artifacts(proposed_artifacts, runtime_root)
    runtime_result = run_materialized_workspace(
        preview.proposed_repository,
        runtime_root,
        "  hello   world  ",
    )

    assert tuple(runtime_result) == preview.proposed_spec.capabilities
    assert "normalize_text" not in runtime_result


def test_preview_requires_normalize_text_to_be_present() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Invalid duplicate preview proof.",
    )
    inspect_only = spec.without_capability("normalize_text")

    with pytest.raises(ValueError, match="normalize_text"):
        preview_remove_normalize_text(inspect_only)
