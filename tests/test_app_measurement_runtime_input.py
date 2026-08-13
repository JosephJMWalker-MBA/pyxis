from dataclasses import FrozenInstanceError, fields
import hashlib
from pathlib import Path

import pytest

from pyxis.app import (
    RuntimeInputComparisonEvidence,
    RuntimeInputEvidence,
    compare_build_and_run_measurements,
    measure_build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def test_measurement_records_privacy_preserving_runtime_input_identity(
    tmp_path: Path,
) -> None:
    text = "café ☕"
    encoded = text.encode("utf-8")
    measured = measure_build_and_run_workspace(
        create_workspace_spec(
            "Text Lab",
            "Runtime input identity should not retain raw workload text.",
        ),
        tmp_path / "workspace",
        text,
        clock=FakeClock(0.0, 1.0, 2.0, 3.0),
    )

    runtime_input = measured.measurement.runtime_input

    assert runtime_input == RuntimeInputEvidence(
        sha256=hashlib.sha256(encoded).hexdigest(),
        character_count=6,
        utf8_byte_count=9,
    )
    assert tuple(field.name for field in fields(runtime_input)) == (
        "sha256",
        "character_count",
        "utf8_byte_count",
    )
    assert text not in repr(runtime_input)

    with pytest.raises(FrozenInstanceError):
        runtime_input.character_count = 99


def test_comparison_exposes_input_match_without_rejecting_different_workloads(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Input mismatch should remain explicit descriptive evidence.",
    )
    first_text = "same workload"
    different_text = "different workload ☕"

    first = measure_build_and_run_workspace(
        spec,
        root,
        first_text,
        clock=FakeClock(0.0, 2.0, 4.0, 5.0),
    )
    same = measure_build_and_run_workspace(
        spec,
        root,
        first_text,
        clock=FakeClock(10.0, 11.0, 12.0, 13.0),
    )
    different = measure_build_and_run_workspace(
        spec,
        root,
        different_text,
        clock=FakeClock(20.0, 20.5, 21.0, 23.0),
    )

    same_comparison = compare_build_and_run_measurements(first, same)
    different_comparison = compare_build_and_run_measurements(same, different)

    assert same_comparison.runtime_input == RuntimeInputComparisonEvidence(
        before=first.measurement.runtime_input,
        after=same.measurement.runtime_input,
        matches=True,
    )
    assert same_comparison.runtime_input.before is first.measurement.runtime_input
    assert same_comparison.runtime_input.after is same.measurement.runtime_input

    assert different_comparison.runtime_input == RuntimeInputComparisonEvidence(
        before=same.measurement.runtime_input,
        after=different.measurement.runtime_input,
        matches=False,
    )
    assert different_comparison.runtime_input.before is same.measurement.runtime_input
    assert different_comparison.runtime_input.after is different.measurement.runtime_input
    assert different_comparison.runtime_input.before.sha256 != (
        different_comparison.runtime_input.after.sha256
    )
    assert different_comparison.runtime_input.before.character_count != (
        different_comparison.runtime_input.after.character_count
    )
    assert tuple(stage.stage for stage in different_comparison.stages) == (
        "build",
        "runtime",
    )
    assert len(different_comparison.build_work.artifact_statuses) == 3
    assert first_text not in repr(different_comparison.runtime_input)
    assert different_text not in repr(different_comparison.runtime_input)
