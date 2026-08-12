import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunResult,
    apply_remove_normalize_text,
    build_and_run_workspace,
    export_workspace,
    preview_remove_normalize_text,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.runtime import run_materialized_workspace


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
runtime_loader_module = importlib.import_module("pyxis.runtime.loader")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_query_workspace_presentation_assembles_persisted_and_live_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Existing Workspace presentation query proof.",
    )
    build_and_run_workspace(spec, root, text)
    preview = preview_remove_normalize_text(spec)
    applied = apply_remove_normalize_text(
        preview,
        root,
        "Remove normalization so persisted revision evidence is queryable.",
    )
    runtime_result = run_materialized_workspace(
        applied.build.repository,
        root,
        text,
    )
    run = BuildAndRunResult(build=applied.build, runtime_result=runtime_result)
    export = export_workspace(applied.build, root, portable, text)
    source_before = _file_snapshot(root)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Workspace presentation query must not compile.")

    def fail_if_executed(*args, **kwargs):
        raise AssertionError("Workspace presentation query must not execute runtime code.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )
    monkeypatch.setattr(
        runtime_loader_module,
        "run_materialized_workspace",
        fail_if_executed,
    )

    presentation = query_workspace_presentation(
        root,
        run=run,
        export=export,
    )

    assert presentation.canonical.workspace_id == preview.proposed_spec.workspace_id
    assert presentation.canonical.capabilities == preview.proposed_spec.capabilities
    assert presentation.rir.rir_sha256 == applied.build.manifest.rir_sha256
    assert presentation.runtime_result == runtime_result

    removed = next(
        artifact
        for artifact in presentation.artifacts
        if artifact.path == "generated/capabilities/normalize_text.py"
    )
    assert removed.status == "removed"
    assert removed.node_sha256 is None
    assert removed.artifact_sha256 is None

    assert len(presentation.revisions) == 1
    assert presentation.revisions[0].revision_id == applied.revision.revision_id
    assert presentation.revisions[0].completed is True
    assert presentation.export is not None
    assert presentation.export.readiness == "READY"
    assert presentation.export.export_root == portable.resolve()
    assert _file_snapshot(root) == source_before


def test_query_workspace_presentation_requires_live_run_evidence(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Persisted files cannot recreate transient runtime evidence.",
    )
    build_and_run_workspace(spec, root, "hello world")

    assert (root / "generated/generation.manifest.json").is_file()
    assert (root / "generated/repository.rir.json").is_file()
    assert tuple((root / "generated").rglob("*.py"))

    with pytest.raises(ValueError, match="transient"):
        query_workspace_presentation(root)


def test_query_workspace_presentation_does_not_infer_ready_from_export_files(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "READY remains supplied verification evidence only.",
    )
    run = build_and_run_workspace(spec, root, text)
    export_workspace(run.build, root, portable, text)

    assert portable.is_dir()
    presentation = query_workspace_presentation(root, run=run)
    assert presentation.export is None


def test_query_workspace_presentation_rejects_stale_run_evidence(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Stale transient evidence must not be combined with current persistence.",
    )
    stale_run = build_and_run_workspace(spec, root, "hello world")
    preview = preview_remove_normalize_text(spec)
    apply_remove_normalize_text(
        preview,
        root,
        "Change the persisted Workspace after the earlier run evidence.",
    )

    with pytest.raises(ValueError, match="persisted Workspace RIR"):
        query_workspace_presentation(root, run=stale_run)


def test_query_workspace_presentation_rejects_export_from_other_source_root(
    tmp_path: Path,
) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Physical source identity remains explicit for export evidence.",
    )
    first_run = build_and_run_workspace(spec, first_root, text)
    second_run = build_and_run_workspace(spec, second_root, text)
    export = export_workspace(first_run.build, first_root, portable, text)

    with pytest.raises(ValueError, match="different source Workspace"):
        query_workspace_presentation(
            second_root,
            run=second_run,
            export=export,
        )
