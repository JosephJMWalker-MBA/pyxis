from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementDurationEnvelopeEvidence,
    BuildAndRunMeasurementMedianEvidence,
    BuildAndRunMeasurementWorkPartitionEvidence,
    BuildWorkEvidence,
    ExecutionEnvironmentEvidence,
    MeasurementCohortConditionEvidence,
    MeasurementStageDurationEnvelopeEvidence,
    MeasurementStageMedianEvidence,
    MeasurementStageWorkPartitionEvidence,
    MeasurementSubjectEvidence,
    RuntimeInputEvidence,
    StageSampleObservationEvidence,
    StageWorkContextDurationEnvelopeEvidence,
    StageWorkContextGroupEvidence,
    StageWorkContextMedianEvidence,
    create_build_and_run_measurement_cohort,
    create_build_and_run_measurement_duration_envelope,
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


def test_median_stays_attached_to_exact_duration_envelopes(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Median should remain attached to the exact descriptive envelope.",
    )
    environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )
    text = "same workload"

    observations = tuple(
        measure_build_and_run_workspace(
            spec,
            root,
            text,
            clock=clock,
            environment_provider=lambda: environment,
        )
        for clock in (
            FakeClock(0.0, 4.0, 5.0, 7.0),
            FakeClock(10.0, 11.5, 12.0, 13.0),
            FakeClock(20.0, 21.0, 22.0, 22.75),
            FakeClock(30.0, 30.75, 31.0, 31.5),
            FakeClock(40.0, 40.5, 41.0, 41.25),
        )
    )
    cohort = create_build_and_run_measurement_cohort(observations)
    samples = project_build_and_run_measurement_stage_samples(cohort)
    partition = partition_build_and_run_measurement_stage_samples(samples)
    envelope = create_build_and_run_measurement_duration_envelope(partition)

    medians = create_build_and_run_measurement_median(envelope)

    assert medians.envelope is envelope
    assert tuple(stage.stage for stage in medians.stages) == ("build", "runtime")

    for source_stage, median_stage in zip(envelope.stages, medians.stages, strict=True):
        assert len(source_stage.groups) == len(median_stage.groups)
        for source_group, median_group in zip(
            source_stage.groups,
            median_stage.groups,
            strict=True,
        ):
            assert median_group.envelope is source_group

    build_first, build_reused = medians.stages[0].groups
    runtime_first, runtime_reused = medians.stages[1].groups

    assert build_first.median_seconds == 4.0
    assert build_reused.median_seconds == 0.875
    assert runtime_first.median_seconds == 2.0
    assert runtime_reused.median_seconds == 0.625

    assert build_first.envelope.sample_count == 1
    assert build_reused.envelope.sample_count == 4
    assert runtime_first.envelope.sample_count == 1
    assert runtime_reused.envelope.sample_count == 4

    assert tuple(field.name for field in fields(medians)) == ("envelope", "stages")
    assert tuple(field.name for field in fields(medians.stages[0])) == ("stage", "groups")
    assert tuple(field.name for field in fields(build_first)) == (
        "envelope",
        "median_seconds",
    )

    with pytest.raises(FrozenInstanceError):
        build_first.median_seconds = 0.0


def test_median_evidence_rejects_incorrect_or_detached_source_envelopes() -> None:
    work = BuildWorkEvidence(
        generation_statuses=(),
        written_paths=(),
        reused_paths=(),
        removed_paths=(),
    )
    first = StageSampleObservationEvidence(duration_seconds=2.0, build_work=work)
    second = StageSampleObservationEvidence(duration_seconds=1.0, build_work=work)
    group = StageWorkContextGroupEvidence(
        build_work=work,
        observations=(first, second),
    )
    group_envelope = StageWorkContextDurationEnvelopeEvidence(
        group=group,
        sample_count=2,
        minimum_seconds=1.0,
        maximum_seconds=2.0,
    )

    with pytest.raises(ValueError, match="median_seconds"):
        StageWorkContextMedianEvidence(
            envelope=group_envelope,
            median_seconds=1.0,
        )

    source_median = StageWorkContextMedianEvidence(
        envelope=group_envelope,
        median_seconds=1.5,
    )
    build_partition = MeasurementStageWorkPartitionEvidence(
        stage="build",
        groups=(group,),
    )
    runtime_partition = MeasurementStageWorkPartitionEvidence(
        stage="runtime",
        groups=(group,),
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
    partition = BuildAndRunMeasurementWorkPartitionEvidence(
        condition=condition,
        stages=(build_partition, runtime_partition),
    )
    envelope = BuildAndRunMeasurementDurationEnvelopeEvidence(
        partition=partition,
        stages=(
            MeasurementStageDurationEnvelopeEvidence(
                stage="build",
                groups=(group_envelope,),
            ),
            MeasurementStageDurationEnvelopeEvidence(
                stage="runtime",
                groups=(group_envelope,),
            ),
        ),
    )

    equal_but_distinct_envelope = StageWorkContextDurationEnvelopeEvidence(
        group=group,
        sample_count=2,
        minimum_seconds=1.0,
        maximum_seconds=2.0,
    )
    detached_median = StageWorkContextMedianEvidence(
        envelope=equal_but_distinct_envelope,
        median_seconds=1.5,
    )

    with pytest.raises(ValueError, match="exact source envelope group object"):
        BuildAndRunMeasurementMedianEvidence(
            envelope=envelope,
            stages=(
                MeasurementStageMedianEvidence(
                    stage="build",
                    groups=(detached_median,),
                ),
                MeasurementStageMedianEvidence(
                    stage="runtime",
                    groups=(source_median,),
                ),
            ),
        )

    with pytest.raises(ValueError, match="stage contract"):
        BuildAndRunMeasurementMedianEvidence(
            envelope=envelope,
            stages=(
                MeasurementStageMedianEvidence(
                    stage="runtime",
                    groups=(source_median,),
                ),
                MeasurementStageMedianEvidence(
                    stage="build",
                    groups=(source_median,),
                ),
            ),
        )
