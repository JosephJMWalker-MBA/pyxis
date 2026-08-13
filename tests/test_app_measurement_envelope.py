from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementDurationEnvelopeEvidence,
    BuildAndRunMeasurementWorkPartitionEvidence,
    BuildWorkEvidence,
    ExecutionEnvironmentEvidence,
    MeasurementCohortConditionEvidence,
    MeasurementStageDurationEnvelopeEvidence,
    MeasurementStageWorkPartitionEvidence,
    MeasurementSubjectEvidence,
    RuntimeInputEvidence,
    StageSampleObservationEvidence,
    StageWorkContextDurationEnvelopeEvidence,
    StageWorkContextGroupEvidence,
    create_build_and_run_measurement_cohort,
    create_build_and_run_measurement_duration_envelope,
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


def test_duration_envelope_compresses_only_within_exact_work_contexts(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Count and observed bounds should remain attached to exact work evidence.",
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
        )
    )
    cohort = create_build_and_run_measurement_cohort(observations)
    samples = project_build_and_run_measurement_stage_samples(cohort)
    partition = partition_build_and_run_measurement_stage_samples(samples)

    envelope = create_build_and_run_measurement_duration_envelope(partition)

    assert envelope.partition is partition
    assert tuple(stage.stage for stage in envelope.stages) == ("build", "runtime")

    for source_stage, envelope_stage in zip(
        partition.stages,
        envelope.stages,
        strict=True,
    ):
        assert tuple(summary.group for summary in envelope_stage.groups) == source_stage.groups
        for source_group, summary in zip(
            source_stage.groups,
            envelope_stage.groups,
            strict=True,
        ):
            assert summary.group is source_group

    build_first, build_reused = envelope.stages[0].groups
    assert (build_first.sample_count, build_first.minimum_seconds, build_first.maximum_seconds) == (
        1,
        4.0,
        4.0,
    )
    assert (
        build_reused.sample_count,
        build_reused.minimum_seconds,
        build_reused.maximum_seconds,
    ) == (3, 0.75, 1.5)

    runtime_first, runtime_reused = envelope.stages[1].groups
    assert (
        runtime_first.sample_count,
        runtime_first.minimum_seconds,
        runtime_first.maximum_seconds,
    ) == (1, 2.0, 2.0)
    assert (
        runtime_reused.sample_count,
        runtime_reused.minimum_seconds,
        runtime_reused.maximum_seconds,
    ) == (3, 0.5, 1.0)

    assert tuple(field.name for field in fields(envelope)) == ("partition", "stages")
    assert tuple(field.name for field in fields(envelope.stages[0])) == ("stage", "groups")
    assert tuple(field.name for field in fields(build_first)) == (
        "group",
        "sample_count",
        "minimum_seconds",
        "maximum_seconds",
    )

    with pytest.raises(FrozenInstanceError):
        build_first.sample_count = 2


def test_duration_envelope_rejects_detached_or_incorrect_compression() -> None:
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

    with pytest.raises(ValueError, match="sample_count"):
        StageWorkContextDurationEnvelopeEvidence(
            group=group,
            sample_count=1,
            minimum_seconds=1.0,
            maximum_seconds=2.0,
        )

    with pytest.raises(ValueError, match="minimum_seconds"):
        StageWorkContextDurationEnvelopeEvidence(
            group=group,
            sample_count=2,
            minimum_seconds=0.5,
            maximum_seconds=2.0,
        )

    with pytest.raises(ValueError, match="maximum_seconds"):
        StageWorkContextDurationEnvelopeEvidence(
            group=group,
            sample_count=2,
            minimum_seconds=1.0,
            maximum_seconds=3.0,
        )

    source_summary = StageWorkContextDurationEnvelopeEvidence(
        group=group,
        sample_count=2,
        minimum_seconds=1.0,
        maximum_seconds=2.0,
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

    equal_but_distinct_group = StageWorkContextGroupEvidence(
        build_work=work,
        observations=(first, second),
    )
    detached_summary = StageWorkContextDurationEnvelopeEvidence(
        group=equal_but_distinct_group,
        sample_count=2,
        minimum_seconds=1.0,
        maximum_seconds=2.0,
    )

    with pytest.raises(ValueError, match="exact source work-context group object"):
        BuildAndRunMeasurementDurationEnvelopeEvidence(
            partition=partition,
            stages=(
                MeasurementStageDurationEnvelopeEvidence(
                    stage="build",
                    groups=(detached_summary,),
                ),
                MeasurementStageDurationEnvelopeEvidence(
                    stage="runtime",
                    groups=(source_summary,),
                ),
            ),
        )

    with pytest.raises(ValueError, match="stage contract"):
        BuildAndRunMeasurementDurationEnvelopeEvidence(
            partition=partition,
            stages=(
                MeasurementStageDurationEnvelopeEvidence(
                    stage="runtime",
                    groups=(source_summary,),
                ),
                MeasurementStageDurationEnvelopeEvidence(
                    stage="build",
                    groups=(source_summary,),
                ),
            ),
        )
