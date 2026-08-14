from dataclasses import FrozenInstanceError
import importlib
from pathlib import Path

import pytest

from pyxis.app import WorkspaceController, build_and_run_workspace
from pyxis.authoring import create_workspace_spec


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _trace_tuples(presentation):
    return tuple(
        (step.stage, step.action, step.subject_kind, step.subject)
        for step in presentation.consequence_trace
    )


def test_split_lines_preview_projects_exact_consequence_trace_without_work(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Preview consequence trace proof.",
    )
    run = build_and_run_workspace(spec, source, "first line\nsecond line")
    before = _file_snapshot(source)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Consequence trace presentation must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    controller = WorkspaceController(source, run)
    presentation = controller.preview_add_split_lines()

    assert _trace_tuples(presentation) == (
        ("requested_architecture_change", "add", "capability", "split_lines"),
        ("proposed_canonical", "add", "capability", "split_lines"),
        ("proposed_rir", "add", "capability", "split_lines"),
        (
            "compiler_product",
            "add",
            "artifact_path",
            "generated/capabilities/split_lines.py",
        ),
        (
            "compiler_product",
            "change",
            "artifact_path",
            "generated/workspaces/text_lab/main.py",
        ),
        ("runtime_contract", "add", "runtime_key", "split_lines"),
    )
    assert controller.current_run is run
    assert controller.current_export is None
    assert _file_snapshot(source) == before

    with pytest.raises(FrozenInstanceError):
        presentation.consequence_trace[0].subject = "other"  # type: ignore[misc]


def test_remove_preview_uses_same_trace_shape_with_remove_actions(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Removal consequence trace proof.",
    )
    run = build_and_run_workspace(spec, source, "hello world")
    controller = WorkspaceController(source, run)

    presentation = controller.preview_remove_normalize_text()

    assert _trace_tuples(presentation) == (
        (
            "requested_architecture_change",
            "remove",
            "capability",
            "normalize_text",
        ),
        ("proposed_canonical", "remove", "capability", "normalize_text"),
        ("proposed_rir", "remove", "capability", "normalize_text"),
        (
            "compiler_product",
            "change",
            "artifact_path",
            "generated/workspaces/text_lab/main.py",
        ),
        (
            "compiler_product",
            "remove",
            "artifact_path",
            "generated/capabilities/normalize_text.py",
        ),
        ("runtime_contract", "remove", "runtime_key", "normalize_text"),
    )
