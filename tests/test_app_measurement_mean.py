from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementMeanEvidence,
    ExecutionEnvironmentEvidence,
    MeasurementStageMeanEvidence,
    StageWorkContextMeanEvidence,
    create_build_and_run_measurement_cohort,
    create_build_and_run_measurement_duration_envelope,
    create_build_and_run_measurement_mean,
    create_build_and_run_measurement_median,
    measure_build_and_run_workspace,
    partition_build_and_run_measurement_stage_samples,
    project_build_and_run_measurement_stage_samples,
)
from pyxis.authoring import create_workspace_spec


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def _chain(tmp_path: Path):
    root = tmp_path / "workspace"
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )
    clocks = (
        FakeClock(0.0, 4.0, 5.0, 7.0),
        FakeClock(10.0, 11.5, 12.0, 13.25),
        FakeClock(20.0, 21.0, 22.0, 22.75),
        FakeClock(30.0, 30.75, 31.0, 31.5),
        FakeClock(40.0, 40.5, 41.0, 41.25),
    )
    observations = tuple(
        measure_build_and_run_workspace(
            spec,
            root,
            "same workload",
            clock=clock,
            environment_provider=lambda: environment,
        )
        for clock in clocks
    )
    cohort = create_build_and_run_measurement_cohort(observations)
    samples = project_build_and_run_measurement_stage_samples(cohort)
    partition = partition_build_and_run_measurement_stage_samples(samples)
    envelope = create_build_and_run_measurement_duration_envelope(partition)
    medians = create_build_and_run_measurement_median(envelope)
    return medians, create_build_and_run_measurement_mean(medians)


def test_mean_uses_raw_durations_and_retains_exact_median(tmp_path: Path) -> None:
    medians, means = _chain(tmp_path)
    assert means.median is medians
    assert tuple(stage.stage for stage in means.stages) == ("build", "runtime")
    for source_stage, mean_stage in zip(medians.stages, means.stages, strict=True):
        for source_group, mean_group in zip(source_stage.groups, mean_stage.groups, strict=True):
            assert mean_group.median is source_group

    build_first, build_reused = means.stages[0].groups
    runtime_first, runtime_reused = means.stages[1].groups
    assert build_first.mean_seconds == 4.0
    assert build_reused.mean_seconds == 0.9375
    assert runtime_first.mean_seconds == 2.0
    assert runtime_reused.mean_seconds == 0.6875
    assert build_reused.median.median_seconds == 0.875
    assert runtime_reused.median.median_seconds == 0.625
    assert build_reused.mean_seconds != build_reused.median.median_seconds
    assert runtime_reused.mean_seconds != runtime_reused.median.median_seconds
    assert tuple(field.name for field in fields(means)) == ("median", "stages")
    assert tuple(field.name for field in fields(build_first)) == ("median", "mean_seconds")
    with pytest.raises(FrozenInstanceError):
        build_first.mean_seconds = 0.0


def test_mean_rejects_wrong_value_detached_source_and_stage_order(tmp_path: Path) -> None:
    medians, means = _chain(tmp_path)
    source = medians.stages[0].groups[0]
    with pytest.raises(ValueError, match="mean_seconds"):
        StageWorkContextMeanEvidence(median=source, mean_seconds=-1.0)

    detached = replace(source)
    detached_mean = StageWorkContextMeanEvidence(
        median=detached,
        mean_seconds=means.stages[0].groups[0].mean_seconds,
    )
    with pytest.raises(ValueError, match="exact source median group object"):
        BuildAndRunMeasurementMeanEvidence(
            median=medians,
            stages=(
                MeasurementStageMeanEvidence(
                    stage="build",
                    groups=(detached_mean, means.stages[0].groups[1]),
                ),
                means.stages[1],
            ),
        )
    with pytest.raises(ValueError, match="stage contract"):
        BuildAndRunMeasurementMeanEvidence(
            median=medians,
            stages=(means.stages[1], means.stages[0]),
        )
