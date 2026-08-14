from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    export_workspace,
)
from pyxis.authoring import create_workspace_spec, load_workspace_spec
from pyxis.ui import create_workspace_shell
from test_ui_workspace_measurement_mount import _measurement_presentation


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_split_lines_preview_and_apply_proves_second_architecture_operation(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "first line\nsecond line"
    spec = create_workspace_spec(
        "Text Lab",
        "Second concrete architecture operation proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    portable_before = _file_snapshot(portable)

    controller = WorkspaceController(source, run, export=export)
    preview = controller.preview_add_split_lines()
    pending = controller.pending_preview

    assert pending is not None
    assert pending.current_spec == spec
    assert pending.proposed_spec.capabilities == (
        "inspect_text",
        "normalize_text",
        "split_lines",
    )
    assert preview.added_capabilities == ("split_lines",)
    assert preview.removed_capabilities == ()
    assert preview.added_artifact_paths == (
        "generated/capabilities/split_lines.py",
    )
    assert preview.changed_artifact_paths == (
        "generated/workspaces/text_lab/main.py",
    )
    assert preview.removed_artifact_paths == ()
    assert preview.current_runtime_keys == (
        "inspect_text",
        "normalize_text",
    )
    assert preview.proposed_runtime_keys == (
        "inspect_text",
        "normalize_text",
        "split_lines",
    )
    assert preview.added_runtime_keys == ("split_lines",)
    assert preview.removed_runtime_keys == ()
    assert controller.current_run is run
    assert controller.current_export is export

    presentation = controller.apply_pending_add_split_lines(
        "Add line-oriented evidence as a second concrete architecture edit.",
        text,
    )

    assert controller.pending_preview is None
    assert controller.current_run is not run
    assert controller.current_export is None
    assert load_workspace_spec(source) == pending.proposed_spec
    assert presentation.canonical.capabilities == pending.proposed_spec.capabilities
    assert presentation.rir.capabilities == pending.proposed_spec.capabilities
    assert presentation.export is None

    runtime = controller.current_run.runtime_result
    assert tuple(runtime) == (
        "inspect_text",
        "normalize_text",
        "split_lines",
    )
    assert runtime["split_lines"] == {
        "lines": ["first line", "second line"],
        "line_count": 2,
    }

    statuses = {artifact.path: artifact.status for artifact in presentation.artifacts}
    assert statuses["generated/capabilities/inspect_text.py"] == "reused"
    assert statuses["generated/capabilities/normalize_text.py"] == "reused"
    assert statuses["generated/capabilities/split_lines.py"] == "new"
    assert statuses["generated/workspaces/text_lab/main.py"] == "regenerated"

    assert len(presentation.revisions) == 1
    revision = presentation.revisions[0]
    assert revision.operation == "add_capability:split_lines"
    assert revision.rationale == (
        "Add line-oriented evidence as a second concrete architecture edit."
    )
    assert revision.completed is True

    assert (source / "generated/capabilities/split_lines.py").is_file()
    assert _file_snapshot(portable) == portable_before


def test_split_lines_apply_rejects_a_different_pending_architecture_preview(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Concrete apply methods must validate their exact preview.",
    )
    run = build_and_run_workspace(spec, source, text)
    controller = WorkspaceController(source, run)
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview
    before = _file_snapshot(source)

    with pytest.raises(ValueError, match="supported architecture edit"):
        controller.apply_pending_add_split_lines(
            "Do not reinterpret a removal preview as a capability addition.",
            text,
        )

    assert controller.pending_preview is pending
    assert controller.current_run is run
    assert _file_snapshot(source) == before


def test_prechange_measurement_cannot_co_display_after_split_lines_changes_rir(
    tmp_path: Path,
) -> None:
    measurement = _measurement_presentation(tmp_path / "measurement")
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Mean stays attached to median evidence.",
    )
    run = build_and_run_workspace(spec, source, "same workload")
    controller = WorkspaceController(source, run)
    current = controller.preview_add_split_lines()
    assert current.added_runtime_keys == ("split_lines",)

    post_apply = controller.apply_pending_add_split_lines(
        "Change the RIR so the prior measurement snapshot becomes stale.",
        "same workload",
    )

    with pytest.raises(ValueError, match="RIR SHA-256"):
        create_workspace_shell(
            post_apply,
            controller=controller,
            measurement_presentation=measurement,
        )
