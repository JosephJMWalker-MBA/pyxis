from dataclasses import replace
import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    compare_build_and_run_measurements,
    measure_build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


measurement_module = importlib.import_module("pyxis.app.measurement")


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def test_subject_identity_allows_same_workspace_across_architectural_states(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Subject identity should distinguish Workspace identity from RIR state.",
    )
    first = measure_build_and_run_workspace(
        spec,
        root,
        "hello world",
        clock=FakeClock(0.0, 2.0, 4.0, 5.0),
    )
    second = measure_build_and_run_workspace(
        spec.without_capability("normalize_text"),
        root,
        "hello world",
        clock=FakeClock(10.0, 11.0, 12.0, 13.5),
    )

    first_subject = first.measurement.subject
    second_subject = second.measurement.subject

    assert first_subject.repository_id == first.result.build.repository.repository_id
    assert first_subject.workspace_id == first.result.build.repository.workspace.workspace_id
    assert first_subject.rir_sha256 == first.result.build.manifest.rir_sha256
    assert second_subject.repository_id == second.result.build.repository.repository_id
    assert second_subject.workspace_id == second.result.build.repository.workspace.workspace_id
    assert second_subject.rir_sha256 == second.result.build.manifest.rir_sha256

    assert first_subject.repository_id == second_subject.repository_id
    assert first_subject.workspace_id == second_subject.workspace_id
    assert first_subject.rir_sha256 != second_subject.rir_sha256

    comparison = compare_build_and_run_measurements(first, second)

    assert comparison.subject.before is first_subject
    assert comparison.subject.after is second_subject
    assert comparison.subject.before.rir_sha256 != comparison.subject.after.rir_sha256
    assert tuple(stage.stage for stage in comparison.stages) == ("build", "runtime")
    assert set(second.result.runtime_result) == {"inspect_text"}


def test_comparison_rejects_unrelated_workspace_before_timing_deltas(
    tmp_path: Path,
    monkeypatch,
) -> None:
    first = measure_build_and_run_workspace(
        create_workspace_spec("First Lab", "First measurement subject."),
        tmp_path / "first",
        "hello",
        clock=FakeClock(0.0, 1.0, 2.0, 3.0),
    )
    second = measure_build_and_run_workspace(
        create_workspace_spec("Second Lab", "Second measurement subject."),
        tmp_path / "second",
        "hello",
        clock=FakeClock(4.0, 5.0, 6.0, 7.0),
    )

    def fail_if_delta_is_constructed(*args, **kwargs):
        raise AssertionError("Timing deltas must not be constructed for unrelated subjects.")

    monkeypatch.setattr(
        measurement_module,
        "StageDurationComparisonEvidence",
        fail_if_delta_is_constructed,
    )

    with pytest.raises(
        ValueError,
        match="Measured cycles must describe the same Workspace subject",
    ):
        compare_build_and_run_measurements(first, second)


def test_comparison_rejects_subject_evidence_that_disagrees_with_build(
    tmp_path: Path,
) -> None:
    measured = measure_build_and_run_workspace(
        create_workspace_spec("Text Lab", "Subject evidence must remain coherent."),
        tmp_path / "workspace",
        "hello",
        clock=FakeClock(0.0, 1.0, 2.0, 3.0),
    )
    tampered_subject = replace(
        measured.measurement.subject,
        rir_sha256="0" * 64,
    )
    tampered = replace(
        measured,
        measurement=replace(measured.measurement, subject=tampered_subject),
    )

    with pytest.raises(
        ValueError,
        match="Measurement subject evidence does not match its BuildResult identity",
    ):
        compare_build_and_run_measurements(tampered, measured)
