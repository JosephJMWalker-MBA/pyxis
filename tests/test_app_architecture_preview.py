from dataclasses import FrozenInstanceError, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceArchitecturePreviewController,
    build_and_run_workspace,
    build_workspace,
    export_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.revisions import canonical_sha256


architecture_preview_module = importlib.import_module("pyxis.app.architecture_preview")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_architecture_preview_controller_retains_typed_preview_without_mutation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Application-owned architecture preview presentation proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    current_presentation = query_workspace_presentation(
        source,
        run=run,
        export=export,
    )
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Architecture preview presentation must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    controller = WorkspaceArchitecturePreviewController(
        source,
        run,
        export=export,
    )
    presentation = controller.preview_remove_normalize_text()
    pending = controller.pending_preview

    assert pending is not None
    assert pending.current_spec == spec
    assert pending.proposed_spec.capabilities == ("inspect_text",)
    assert presentation.current.workspace_id == spec.workspace_id
    assert presentation.current.name == spec.name
    assert presentation.current.description == spec.description
    assert presentation.current.capabilities == spec.capabilities
    assert presentation.current.canonical_sha256 == canonical_sha256(spec)
    assert presentation.proposed.workspace_id == spec.workspace_id
    assert presentation.proposed.capabilities == ("inspect_text",)
    assert presentation.proposed.canonical_sha256 == canonical_sha256(
        pending.proposed_spec
    )
    assert presentation.proposed.canonical_sha256 != presentation.current.canonical_sha256

    assert presentation.added_capabilities == ()
    assert presentation.removed_capabilities == ("normalize_text",)
    assert presentation.added_artifact_paths == ()
    assert presentation.changed_artifact_paths == (
        "generated/workspaces/text_lab/main.py",
    )
    assert presentation.removed_artifact_paths == (
        "generated/capabilities/normalize_text.py",
    )
    assert presentation.current_runtime_keys == (
        "inspect_text",
        "normalize_text",
    )
    assert presentation.proposed_runtime_keys == ("inspect_text",)
    assert presentation.added_runtime_keys == ()
    assert presentation.removed_runtime_keys == ("normalize_text",)

    with pytest.raises(FrozenInstanceError):
        presentation.removed_capabilities = ()  # type: ignore[misc]

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before

    # Preview does not invalidate the live run or READY evidence because no
    # canonical/compiler/runtime/export state changed.
    after = query_workspace_presentation(
        source,
        run=run,
        export=export,
    )
    assert after == current_presentation


def test_architecture_preview_rejects_stale_live_evidence_before_preview(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Stale evidence must fail before architecture preview.",
    )
    stale_run = build_and_run_workspace(spec, source, "first input")

    changed_spec = replace(
        spec,
        description="Persisted canonical intent changed after the live run.",
    )
    build_workspace(changed_spec, source)

    def fail_if_preview_runs(*args, **kwargs):
        raise AssertionError("Stale live evidence must fail before preview creation.")

    monkeypatch.setattr(
        architecture_preview_module,
        "preview_remove_normalize_text",
        fail_if_preview_runs,
    )

    controller = WorkspaceArchitecturePreviewController(source, stale_run)
    with pytest.raises(ValueError, match="persisted Workspace RIR"):
        controller.preview_remove_normalize_text()

    assert controller.pending_preview is None
