from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementCohortEvidence,
    ExecutionEnvironmentEvidence,
    create_build_and_run_measurement_cohort,
    measure_build_and_run_workspace,
    preview_remove_normalize_text,
)
from pyxis.authoring import create_workspace_spec


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def _environment() -> ExecutionEnvironmentEvidence:
    return ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )


def test_cohort_retains_ordered_repeated_observations_without_aggregation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Repeated measurements should preserve observations before statistics.",
    )
    text = "same workload"
    environment = _environment()

    first = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(0.0, 4.0, 5.0, 7.0),
        environment_provider=lambda: environment,
    )
    second = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(10.0, 11.5, 12.0, 13.0),
        environment_provider=lambda: environment,
    )
    third = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(20.0, 21.0, 22.0, 22.75),
        environment_provider=lambda: environment,
    )

    cohort = create_build_and_run_measurement_cohort((first, second, third))

    assert cohort.condition.subject is first.measurement.subject
    assert cohort.condition.runtime_input is first.measurement.runtime_input
    assert cohort.condition.environment is first.measurement.environment
    assert cohort.condition.stages == ("build", "runtime")
    assert cohort.observations == (first, second, third)
    assert cohort.observations[0] is first
    assert cohort.observations[1] is second
    assert cohort.observations[2] is third

    assert {entry.status for entry in first.measurement.build_work.generation_statuses} == {
        "new"
    }
    assert {entry.status for entry in second.measurement.build_work.generation_statuses} == {
        "reused"
    }
    assert first.measurement.build_work.written_paths
    assert second.measurement.build_work.written_paths == ()

    assert tuple(field.name for field in fields(cohort)) == (
        "condition",
        "observations",
    )
    assert tuple(field.name for field in fields(cohort.condition)) == (
        "subject",
        "runtime_input",
        "environment",
        "stages",
    )

    with pytest.raises(FrozenInstanceError):
        cohort.observations = ()


def test_cohort_rejects_mixed_measurement_conditions_before_aggregation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Mixed repeated-measurement conditions should be rejected.",
    )
    text = "same workload"
    environment = _environment()

    first = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(0.0, 1.0, 2.0, 3.0),
        environment_provider=lambda: environment,
    )
    second = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(10.0, 11.0, 12.0, 13.0),
        environment_provider=lambda: environment,
    )
    baseline = create_build_and_run_measurement_cohort((first, second))

    different_input = measure_build_and_run_workspace(
        spec,
        root,
        "different workload",
        clock=FakeClock(20.0, 21.0, 22.0, 23.0),
        environment_provider=lambda: environment,
    )
    with pytest.raises(ValueError, match="same runtime input evidence"):
        create_build_and_run_measurement_cohort((first, different_input))

    different_environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.12.4",
        platform_system="Linux",
        platform_machine="arm64",
    )
    environment_changed = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(30.0, 31.0, 32.0, 33.0),
        environment_provider=lambda: different_environment,
    )
    with pytest.raises(ValueError, match="same execution environment evidence"):
        create_build_and_run_measurement_cohort((first, environment_changed))

    changed_spec = preview_remove_normalize_text(spec).proposed_spec
    architecture_changed = measure_build_and_run_workspace(
        changed_spec,
        tmp_path / "changed-architecture",
        text,
        clock=FakeClock(40.0, 41.0, 42.0, 43.0),
        environment_provider=lambda: environment,
    )
    assert architecture_changed.measurement.subject.repository_id == (
        first.measurement.subject.repository_id
    )
    assert architecture_changed.measurement.subject.workspace_id == (
        first.measurement.subject.workspace_id
    )
    assert architecture_changed.measurement.subject.rir_sha256 != (
        first.measurement.subject.rir_sha256
    )
    with pytest.raises(ValueError, match="same Workspace and exact RIR state"):
        create_build_and_run_measurement_cohort((first, architecture_changed))

    unrelated = measure_build_and_run_workspace(
        create_workspace_spec("Other Lab", "A different logical Workspace."),
        tmp_path / "unrelated",
        text,
        clock=FakeClock(50.0, 51.0, 52.0, 53.0),
        environment_provider=lambda: environment,
    )
    with pytest.raises(ValueError, match="same Workspace and exact RIR state"):
        create_build_and_run_measurement_cohort((first, unrelated))

    reversed_measurement = replace(
        second.measurement,
        stages=tuple(reversed(second.measurement.stages)),
    )
    reversed_stages = replace(second, measurement=reversed_measurement)
    with pytest.raises(ValueError, match="stage contract"):
        create_build_and_run_measurement_cohort((first, reversed_stages))

    with pytest.raises(ValueError, match="at least two observations"):
        create_build_and_run_measurement_cohort((first,))

    with pytest.raises(ValueError, match="same runtime input evidence"):
        BuildAndRunMeasurementCohortEvidence(
            condition=baseline.condition,
            observations=(first, different_input),
        )
