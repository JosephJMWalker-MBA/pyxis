from dataclasses import replace
import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunResult,
    apply_remove_normalize_text,
    build_and_run_workspace,
    create_workspace_presentation,
    export_workspace,
    preview_remove_normalize_text,
)
from pyxis.authoring import create_workspace_spec
from pyxis.revisions import canonical_sha256, create_revision_event
from pyxis.runtime import run_materialized_workspace


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
presentation_module = importlib.import_module("pyxis.app.presentation")
runtime_loader_module = importlib.import_module("pyxis.runtime.loader")


def test_workspace_presentation_maps_existing_evidence_without_new_io_or_execution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Read-only Workspace presentation contract.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Workspace presentation must not compile.")

    def fail_if_executed(*args, **kwargs):
        raise AssertionError("Workspace presentation must not execute runtime code.")

    def fail_if_path_read(*args, **kwargs):
        raise AssertionError("Workspace presentation must not read the filesystem.")

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
    monkeypatch.setattr(Path, "read_text", fail_if_path_read)
    monkeypatch.setattr(Path, "read_bytes", fail_if_path_read)
    monkeypatch.setattr(Path, "exists", fail_if_path_read)
    monkeypatch.setattr(Path, "is_file", fail_if_path_read)
    monkeypatch.setattr(Path, "is_dir", fail_if_path_read)

    presentation = create_workspace_presentation(
        spec,
        run,
        export=export,
    )

    assert presentation.canonical.workspace_id == spec.workspace_id
    assert presentation.canonical.name == spec.name
    assert presentation.canonical.description == spec.description
    assert presentation.canonical.capabilities == spec.capabilities
    assert presentation.canonical.canonical_sha256 == canonical_sha256(spec)

    assert presentation.rir.repository_id == run.build.repository.repository_id
    assert presentation.rir.workspace_id == spec.workspace_id
    assert presentation.rir.capabilities == spec.capabilities
    assert presentation.rir.rir_sha256 == run.build.manifest.rir_sha256

    expected_manifest = {
        artifact.path: (artifact.node_sha256, artifact.artifact_sha256)
        for artifact in run.build.manifest.artifacts
    }
    assert tuple(artifact.path for artifact in presentation.artifacts) == tuple(
        status.path for status in run.build.generation_statuses
    )
    assert all(artifact.status == "new" for artifact in presentation.artifacts)
    for artifact in presentation.artifacts:
        assert (artifact.node_sha256, artifact.artifact_sha256) == expected_manifest[
            artifact.path
        ]

    assert presentation.runtime_result == run.runtime_result
    assert presentation.runtime_result is not run.runtime_result
    assert presentation.revisions == ()

    assert presentation.export is not None
    assert presentation.export.readiness == "READY"
    assert presentation.export.export_root == portable.resolve()
    assert presentation.export.rir_sha256 == run.build.manifest.rir_sha256
    assert presentation.export.input_sha256 == export.verification.runtime.input_sha256
    assert presentation.export.compiler_product_count == len(run.build.artifacts)


def test_workspace_presentation_preserves_governed_revision_and_removed_status(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Presentation of governed architecture changes.",
    )
    build_and_run_workspace(spec, root, "hello world")
    preview = preview_remove_normalize_text(spec)
    applied = apply_remove_normalize_text(
        preview,
        root,
        "Remove normalization for the presentation contract proof.",
    )
    runtime_result = run_materialized_workspace(
        applied.build.repository,
        root,
        "hello world",
    )
    run = BuildAndRunResult(
        build=applied.build,
        runtime_result=runtime_result,
    )

    presentation = create_workspace_presentation(
        preview.proposed_spec,
        run,
        revision_events=(applied.revision,),
        revision_completions=(applied.completion,),
    )

    removed = next(
        artifact
        for artifact in presentation.artifacts
        if artifact.path == "generated/capabilities/normalize_text.py"
    )
    assert removed.status == "removed"
    assert removed.node_sha256 is None
    assert removed.artifact_sha256 is None

    assert len(presentation.revisions) == 1
    revision = presentation.revisions[0]
    assert revision.revision_id == applied.revision.revision_id
    assert revision.operation == "remove_capability:normalize_text"
    assert revision.rationale == applied.revision.rationale
    assert revision.completed is True
    assert revision.completion_rir_sha256 == applied.completion.rir_sha256
    assert (
        revision.completion_generation_manifest_sha256
        == applied.completion.generation_manifest_sha256
    )
    assert "normalize_text" not in presentation.runtime_result
    assert presentation.export is None


def test_workspace_presentation_keeps_uncompleted_revision_intent_visible(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Incomplete revision evidence remains explicit.",
    )
    run = build_and_run_workspace(spec, root, "hello world")
    proposed = spec.without_capability("normalize_text")
    event = create_revision_event(
        spec,
        proposed,
        "remove_capability:normalize_text",
        "Proposed but not completed.",
    )

    presentation = create_workspace_presentation(
        spec,
        run,
        revision_events=(event,),
    )

    revision = presentation.revisions[0]
    assert revision.completed is False
    assert revision.completion_rir_sha256 is None
    assert revision.completion_generation_manifest_sha256 is None


def test_workspace_presentation_rejects_mismatched_canonical_or_export_evidence(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Presentation evidence coherence.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)

    changed_spec = replace(spec, description="Different canonical description.")
    with pytest.raises(ValueError, match="Canonical Workspace evidence"):
        create_workspace_presentation(changed_spec, run)

    changed_identity = replace(
        export.verification.identity,
        workspace_id="different_workspace",
    )
    changed_verification = replace(
        export.verification,
        identity=changed_identity,
    )
    changed_export = replace(
        export,
        verification=changed_verification,
    )
    with pytest.raises(ValueError, match="different Workspace"):
        create_workspace_presentation(
            spec,
            run,
            export=changed_export,
        )
