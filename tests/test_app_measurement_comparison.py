from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from pyxis.app import (
    ArtifactGenerationStatusComparisonEvidence,
    StageDurationComparisonEvidence,
    compare_build_and_run_measurements,
    measure_build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def _relative_paths(paths: tuple[Path, ...], root: Path) -> tuple[str, ...]:
    return tuple(path.relative_to(root).as_posix() for path in paths)


def test_comparison_reports_literal_timing_and_work_changes_for_identical_rebuild(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Comparison should describe observations without causal interpretation.",
    )
    text = "  hello   world  "

    first = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(0.0, 4.0, 10.0, 12.0),
    )
    second = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(20.0, 21.5, 30.0, 31.75),
    )

    comparison = compare_build_and_run_measurements(first, second)

    assert comparison.stages == (
        StageDurationComparisonEvidence(
            stage="build",
            before_seconds=4.0,
            after_seconds=1.5,
            delta_seconds=-2.5,
        ),
        StageDurationComparisonEvidence(
            stage="runtime",
            before_seconds=2.0,
            after_seconds=1.75,
            delta_seconds=-0.25,
        ),
    )

    assert comparison.build_work.before is first.measurement.build_work
    assert comparison.build_work.after is second.measurement.build_work
    assert comparison.build_work.artifact_statuses == (
        ArtifactGenerationStatusComparisonEvidence(
            path="generated/capabilities/inspect_text.py",
            before_status="new",
            after_status="reused",
        ),
        ArtifactGenerationStatusComparisonEvidence(
            path="generated/capabilities/normalize_text.py",
            before_status="new",
            after_status="reused",
        ),
        ArtifactGenerationStatusComparisonEvidence(
            path="generated/workspaces/text_lab/main.py",
            before_status="new",
            after_status="reused",
        ),
    )

    before_work = comparison.build_work.before
    after_work = comparison.build_work.after
    assert _relative_paths(before_work.written_paths, root) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert before_work.reused_paths == ()
    assert before_work.removed_paths == ()
    assert after_work.written_paths == ()
    assert _relative_paths(after_work.reused_paths, root) == (
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )
    assert after_work.removed_paths == ()

    assert first.result.build.repository == second.result.build.repository
    assert first.result.runtime_result == second.result.runtime_result

    with pytest.raises(FrozenInstanceError):
        comparison.stages[0].delta_seconds = 0.0


def test_comparison_rejects_mismatched_stage_ordering(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Stage comparison must preserve observation ordering.",
    )
    first = measure_build_and_run_workspace(
        spec,
        root,
        "hello world",
        clock=FakeClock(0.0, 1.0, 2.0, 3.0),
    )
    second = measure_build_and_run_workspace(
        spec,
        root,
        "hello world",
        clock=FakeClock(4.0, 5.0, 6.0, 7.0),
    )
    reordered_measurement = replace(
        second.measurement,
        stages=tuple(reversed(second.measurement.stages)),
    )
    reordered = replace(second, measurement=reordered_measurement)

    with pytest.raises(
        ValueError,
        match="Measured cycles must contain the same ordered stages",
    ):
        compare_build_and_run_measurements(first, reordered)
