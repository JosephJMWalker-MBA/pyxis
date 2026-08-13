from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementStageSamplesEvidence,
    ExecutionEnvironmentEvidence,
    MeasurementStageSamplesEvidence,
    StageSampleObservationEvidence,
    create_build_and_run_measurement_cohort,
    measure_build_and_run_workspace,
    project_build_and_run_measurement_stage_samples,
)
from pyxis.authoring import create_workspace_spec


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def test_stage_sample_projection_preserves_raw_order_and_exact_work_context(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Raw stage samples should preserve work context before statistics.",
    )
    environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )
    text = "same workload"

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

    projection = project_build_and_run_measurement_stage_samples(cohort)

    assert projection.condition is cohort.condition
    assert tuple(stage.stage for stage in projection.stages) == ("build", "runtime")

    build_samples, runtime_samples = projection.stages
    assert tuple(sample.duration_seconds for sample in build_samples.observations) == (
        4.0,
        1.5,
        1.0,
    )
    assert tuple(sample.duration_seconds for sample in runtime_samples.observations) == (
        2.0,
        1.0,
        0.75,
    )

    originals = (first, second, third)
    for index, observation in enumerate(originals):
        assert build_samples.observations[index].build_work is observation.measurement.build_work
        assert runtime_samples.observations[index].build_work is observation.measurement.build_work

    assert {entry.status for entry in build_samples.observations[0].build_work.generation_statuses} == {
        "new"
    }
    assert {entry.status for entry in build_samples.observations[1].build_work.generation_statuses} == {
        "reused"
    }
    assert build_samples.observations[0].build_work.written_paths
    assert build_samples.observations[1].build_work.written_paths == ()

    assert tuple(field.name for field in fields(projection)) == ("condition", "stages")
    assert tuple(field.name for field in fields(build_samples)) == ("stage", "observations")
    assert tuple(field.name for field in fields(build_samples.observations[0])) == (
        "duration_seconds",
        "build_work",
    )

    with pytest.raises(FrozenInstanceError):
        build_samples.observations = ()


def test_stage_sample_evidence_rejects_incoherent_direct_construction() -> None:
    sample = StageSampleObservationEvidence(
        duration_seconds=1.0,
        build_work=first_work := __import__("pyxis.app", fromlist=["BuildWorkEvidence"]).BuildWorkEvidence(
            generation_statuses=(),
            written_paths=(),
            reused_paths=(),
            removed_paths=(),
        ),
    )
    build = MeasurementStageSamplesEvidence(stage="build", observations=(sample, sample))
    runtime = MeasurementStageSamplesEvidence(stage="runtime", observations=(sample, sample))

    from pyxis.app import (
        MeasurementCohortConditionEvidence,
        MeasurementSubjectEvidence,
        RuntimeInputEvidence,
    )

    condition = MeasurementCohortConditionEvidence(
        subject=MeasurementSubjectEvidence(
            repository_id="repository",
            workspace_id="workspace",
            rir_sha256="rir",
        ),
        runtime_input=RuntimeInputEvidence(
            sha256="0" * 64,
            character_count=0,
            utf8_byte_count=0,
        ),
        environment=ExecutionEnvironmentEvidence(
            python_implementation="CPython",
            python_version="3.11.9",
            platform_system="Linux",
            platform_machine="x86_64",
        ),
        stages=("build", "runtime"),
    )

    with pytest.raises(ValueError, match="stage contract"):
        BuildAndRunMeasurementStageSamplesEvidence(
            condition=condition,
            stages=(runtime, build),
        )

    short_runtime = MeasurementStageSamplesEvidence(
        stage="runtime",
        observations=(sample, sample, sample),
    )
    with pytest.raises(ValueError, match="same observation count"):
        BuildAndRunMeasurementStageSamplesEvidence(
            condition=condition,
            stages=(build, short_runtime),
        )

    assert sample.build_work is first_work
