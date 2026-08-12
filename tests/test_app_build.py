import json
from pathlib import Path

from pyxis.app import build_workspace
from pyxis.authoring import persist_workspace_spec
from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler import (
    build_generation_manifest,
    classify_generation_statuses,
    inspect_materialized_artifact_integrity,
    load_generation_manifest,
    persist_generation_manifest,
    reconcile_materialized_artifacts,
)
from pyxis.compiler.repository import compile_repository
from pyxis.rir import persist_repository_ir
from pyxis.rir.model import build_repository_ir


def _status_pairs(result):
    return tuple((entry.path, entry.status) for entry in result.generation_statuses)


def _relative_paths(paths, root: Path):
    return tuple(path.relative_to(root).as_posix() for path in paths)


def test_build_workspace_matches_manual_pipeline(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "First-run orchestration proof.",
    )

    manual_root = tmp_path / "manual"
    manual_previous_manifest = load_generation_manifest(manual_root)
    manual_existing_integrity = inspect_materialized_artifact_integrity(
        manual_previous_manifest,
        manual_root,
    )
    manual_canonical_path = persist_workspace_spec(spec, manual_root)
    manual_repository = build_repository_ir(spec)
    manual_rir_path = persist_repository_ir(manual_repository, manual_root)
    manual_artifacts = compile_repository(manual_repository)
    manual_manifest = build_generation_manifest(manual_repository, manual_artifacts)
    manual_statuses = classify_generation_statuses(
        manual_artifacts,
        manual_previous_manifest,
        manual_existing_integrity,
    )
    manual_materialization = reconcile_materialized_artifacts(
        manual_artifacts,
        manual_statuses,
        manual_previous_manifest,
        manual_root,
    )
    manual_manifest_path = persist_generation_manifest(manual_manifest, manual_root)

    built_root = tmp_path / "built"
    result = build_workspace(spec, built_root)

    assert result.canonical_path.relative_to(built_root) == (
        manual_canonical_path.relative_to(manual_root)
    )
    assert result.repository == manual_repository
    assert result.rir_path.relative_to(built_root) == manual_rir_path.relative_to(
        manual_root
    )
    assert result.artifacts == manual_artifacts
    assert result.manifest == manual_manifest
    assert result.generation_statuses == manual_statuses
    assert result.manifest_path.relative_to(built_root) == (
        manual_manifest_path.relative_to(manual_root)
    )
    assert tuple(path.relative_to(built_root) for path in result.written_paths) == tuple(
        path.relative_to(manual_root)
        for path in manual_materialization.written_paths
    )
    assert tuple(path.relative_to(built_root) for path in result.reused_paths) == tuple(
        path.relative_to(manual_root)
        for path in manual_materialization.reused_paths
    )
    assert result.removed_paths == manual_materialization.removed_paths == ()


def test_build_workspace_materializes_complete_repository(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Complete first-run build proof.",
    )

    result = build_workspace(spec, tmp_path)

    assert tuple(artifact.path for artifact in result.artifacts) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert all(path.exists() for path in result.written_paths)
    assert tuple(path.read_bytes() for path in result.written_paths) == tuple(
        artifact.source.encode("utf-8") for artifact in result.artifacts
    )
    assert result.reused_paths == ()
    assert result.removed_paths == ()


def test_build_workspace_persists_canonical_state_separately_from_generated(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Canonical and generated filesystem boundary proof.",
    )

    result = build_workspace(spec, tmp_path)

    assert result.canonical_path == (
        tmp_path.resolve() / "authoring/canonical/workspace.json"
    )
    assert result.canonical_path not in result.written_paths
    assert json.loads(result.canonical_path.read_text(encoding="utf-8")) == {
        "workspace_id": "text_lab",
        "name": "Text Lab",
        "description": "Canonical and generated filesystem boundary proof.",
        "capabilities": ["inspect_text", "normalize_text"],
    }
    assert all(
        path.relative_to(tmp_path).parts[0] == "generated"
        for path in result.written_paths
    )


def test_build_workspace_persists_rir_separately_from_compiler_artifacts(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "RIR and compiler artifact boundary proof.",
    )

    result = build_workspace(spec, tmp_path)

    assert result.rir_path == tmp_path.resolve() / "generated/repository.rir.json"
    assert result.rir_path not in result.written_paths
    assert json.loads(result.rir_path.read_text(encoding="utf-8")) == {
        "schema_version": result.repository.schema_version,
        "repository_id": result.repository.repository_id,
        "workspace": {
            "workspace_id": result.repository.workspace.workspace_id,
            "name": result.repository.workspace.name,
            "description": result.repository.workspace.description,
            "entrypoint": result.repository.workspace.entrypoint,
            "capabilities": list(result.repository.workspace.capabilities),
        },
    }
    assert _relative_paths(result.written_paths, tmp_path) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )


def test_build_workspace_persists_manifest_separately_from_compiler_artifacts(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Generation evidence boundary proof.",
    )

    result = build_workspace(spec, tmp_path)

    assert result.manifest_path == (
        tmp_path.resolve() / "generated/generation.manifest.json"
    )
    assert result.manifest_path not in result.written_paths
    assert json.loads(result.manifest_path.read_text(encoding="utf-8")) == (
        result.manifest.to_dict()
    )
    assert set(result.manifest.to_dict()) == {"rir_sha256", "artifacts"}
    assert all(
        set(entry) == {"path", "node_sha256", "artifact_sha256"}
        for entry in result.manifest.to_dict()["artifacts"]
    )
    assert tuple(entry.path for entry in result.manifest.artifacts) == tuple(
        artifact.path for artifact in result.artifacts
    )
    assert _relative_paths(result.written_paths, tmp_path) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )


def test_first_build_reports_new_and_writes_every_artifact(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec("Text Lab", "First-build status proof.")

    result = build_workspace(spec, tmp_path)

    assert _status_pairs(result) == (
        ("generated/capabilities/inspect_text.py", "new"),
        ("generated/capabilities/normalize_text.py", "new"),
        ("generated/workspaces/text_lab/main.py", "new"),
    )
    assert _relative_paths(result.written_paths, tmp_path) == tuple(
        artifact.path for artifact in result.artifacts
    )
    assert result.reused_paths == ()


def test_identical_rebuild_reuses_every_artifact_without_generated_writes(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec("Text Lab", "Identical rebuild status proof.")
    baseline = build_workspace(spec, tmp_path)
    before = {
        artifact.path: (tmp_path / artifact.path).read_bytes()
        for artifact in baseline.artifacts
    }

    result = build_workspace(spec, tmp_path)

    assert tuple(entry.status for entry in result.generation_statuses) == (
        "reused",
        "reused",
        "reused",
    )
    assert result.written_paths == ()
    assert _relative_paths(result.reused_paths, tmp_path) == tuple(
        artifact.path for artifact in result.artifacts
    )
    assert {
        artifact.path: (tmp_path / artifact.path).read_bytes()
        for artifact in result.artifacts
    } == before


def test_tampered_generated_artifact_is_regenerated_while_clean_artifacts_reuse(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec("Text Lab", "Artifact integrity status proof.")
    baseline = build_workspace(spec, tmp_path)
    inspect_path = tmp_path / "generated/capabilities/inspect_text.py"
    inspect_path.write_bytes(b"# manual generated-code edit\n")

    result = build_workspace(spec, tmp_path)

    assert tuple(entry.status for entry in result.generation_statuses) == (
        "regenerated",
        "reused",
        "reused",
    )
    assert _relative_paths(result.written_paths, tmp_path) == (
        "generated/capabilities/inspect_text.py",
    )
    assert _relative_paths(result.reused_paths, tmp_path) == (
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert inspect_path.read_bytes() == baseline.artifacts[0].source.encode("utf-8")


def test_build_workspace_reconciles_removed_compiler_artifact_from_prior_manifest(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Permanent path stale artifact reconciliation proof.",
    )
    build_workspace(spec, tmp_path)

    stale_path = tmp_path / "generated/capabilities/normalize_text.py"
    untracked_path = tmp_path / "generated/untracked.py"
    assert stale_path.is_file()
    untracked_path.write_text("# outside compiler ownership\n", encoding="utf-8")

    proposed_spec = spec.without_capability("normalize_text")
    result = build_workspace(proposed_spec, tmp_path)

    assert _status_pairs(result) == (
        ("generated/capabilities/inspect_text.py", "reused"),
        ("generated/workspaces/text_lab/main.py", "regenerated"),
        ("generated/capabilities/normalize_text.py", "removed"),
    )
    assert _relative_paths(result.written_paths, tmp_path) == (
        "generated/workspaces/text_lab/main.py",
    )
    assert _relative_paths(result.reused_paths, tmp_path) == (
        "generated/capabilities/inspect_text.py",
    )
    assert _relative_paths(result.removed_paths, tmp_path) == (
        "generated/capabilities/normalize_text.py",
    )
    assert not stale_path.exists()
    assert untracked_path.read_text(encoding="utf-8") == "# outside compiler ownership\n"
    assert tuple(artifact.path for artifact in result.artifacts) == (
        "generated/capabilities/inspect_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert tuple(entry.path for entry in result.manifest.artifacts) == (
        "generated/capabilities/inspect_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert json.loads(result.canonical_path.read_text(encoding="utf-8"))[
        "capabilities"
    ] == ["inspect_text"]
    assert json.loads(result.rir_path.read_text(encoding="utf-8"))["workspace"][
        "capabilities"
    ] == ["inspect_text"]


def test_build_workspace_does_not_mutate_authored_spec(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Orchestration boundary proof.",
    )
    before = spec.to_canonical_dict()

    build_workspace(spec, tmp_path)

    assert spec.to_canonical_dict() == before
