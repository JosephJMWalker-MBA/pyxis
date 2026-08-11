from pathlib import Path

from pyxis.app import build_and_run_workspace, build_workspace
from pyxis.authoring.workspace import create_workspace_spec
from pyxis.runtime.loader import run_materialized_workspace


def test_build_and_run_matches_manual_composition(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "First-run orchestration proof.",
    )
    text = "  hello   world  "

    manual_root = tmp_path / "manual"
    manual_build = build_workspace(spec, manual_root)
    manual_runtime = run_materialized_workspace(
        manual_build.repository,
        manual_root,
        text,
    )

    composed_root = tmp_path / "composed"
    result = build_and_run_workspace(
        spec,
        composed_root,
        text,
    )

    assert result.build.repository == manual_build.repository
    assert result.build.artifacts == manual_build.artifacts
    assert result.runtime_result == manual_runtime


def test_build_and_run_exposes_generated_behavior(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Executable first-run proof.",
    )

    result = build_and_run_workspace(
        spec,
        tmp_path,
        "  hello   world  ",
    )

    assert set(result.runtime_result) == {
        "inspect_text",
        "normalize_text",
    }
    assert result.runtime_result["inspect_text"]["words"] == 2
    assert (
        result.runtime_result["normalize_text"]["normalized_text"]
        == "hello world"
    )


def test_build_and_run_does_not_mutate_authoring_spec(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Orchestration boundary proof.",
    )
    before = spec.to_canonical_dict()

    build_and_run_workspace(
        spec,
        tmp_path,
        "hello world",
    )

    assert spec.to_canonical_dict() == before
