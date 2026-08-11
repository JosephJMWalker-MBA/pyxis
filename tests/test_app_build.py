from pathlib import Path

from pyxis.app import build_workspace
from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler.materialize import materialize_artifacts
from pyxis.compiler.repository import compile_repository
from pyxis.rir.model import build_repository_ir


def test_build_workspace_matches_manual_pipeline(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "First-run orchestration proof.",
    )

    manual_repository = build_repository_ir(spec)
    manual_artifacts = compile_repository(manual_repository)
    manual_root = tmp_path / "manual"
    manual_paths = materialize_artifacts(manual_artifacts, manual_root)

    built_root = tmp_path / "built"
    result = build_workspace(spec, built_root)

    assert result.repository == manual_repository
    assert result.artifacts == manual_artifacts
    assert tuple(path.relative_to(built_root) for path in result.written_paths) == tuple(
        path.relative_to(manual_root) for path in manual_paths
    )


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
    assert tuple(path.read_text(encoding="utf-8") for path in result.written_paths) == tuple(
        artifact.source for artifact in result.artifacts
    )


def test_build_workspace_does_not_mutate_authored_spec(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Orchestration boundary proof.",
    )
    before = spec.to_canonical_dict()

    build_workspace(spec, tmp_path)

    assert spec.to_canonical_dict() == before
