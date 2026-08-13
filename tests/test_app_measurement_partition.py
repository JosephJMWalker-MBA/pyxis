from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from pyxis.app import (
    BuildAndRunMeasurementWorkPartitionEvidence,
    BuildWorkEvidence,
    ExecutionEnvironmentEvidence,
    MeasurementCohortConditionEvidence,
    MeasurementStageWorkPartitionEvidence,
    MeasurementSubjectEvidence,
    RuntimeInputEvidence,
    StageSampleObservationEvidence,
    StageWorkContextGroupEvidence,
    create_build_and_run_measurement_cohort,
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


def test_work_partition_groups_exact_evidence_without_semantic_labels(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Exact work evidence should partition raw samples before statistics.",
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

    assert partition.condition is samples.condition
    assert tuple(stage.stage for stage in partition.stages) == ("build", "runtime")

    for source_stage, partition_stage in zip(samples.stages, partition.stages, strict=True):
        assert len(partition_stage.groups) == 2
        first_group, reused_group = partition_stage.groups

        assert first_group.build_work is source_stage.observations[0].build_work
        assert first_group.observations == (source_stage.observations[0],)
        assert first_group.observations[0] is source_stage.observations[0]

        assert reused_group.build_work is source_stage.observations[1].build_work
        assert reused_group.observations == source_stage.observations[1:]
        for group_observation, source_observation in zip(
            reused_group.observations,
            source_stage.observations[1:],
            strict=True,
        ):
            assert group_observation is source_observation

        assert {entry.status for entry in first_group.build_work.generation_statuses} == {
            "new"
        }
        assert {entry.status for entry in reused_group.build_work.generation_statuses} == {
            "reused"
        }
        assert first_group.build_work.written_paths
        assert reused_group.build_work.written_paths == ()

    assert tuple(field.name for field in fields(partition)) == ("condition", "stages")
    assert tuple(field.name for field in fields(partition.stages[0])) == ("stage", "groups")
    assert tuple(field.name for field in fields(partition.stages[0].groups[0])) == (
        "build_work",
        "observations",
    )

    with pytest.raises(FrozenInstanceError):
        partition.stages = ()


def test_work_partition_evidence_rejects_incoherent_direct_construction() -> None:
    first_work = BuildWorkEvidence(
        generation_statuses=(),
        written_paths=(Path("generated/first.py"),),
        reused_paths=(),
        removed_paths=(),
    )
    second_work = BuildWorkEvidence(
        generation_statuses=(),
        written_paths=(),
        reused_paths=(Path("generated/first.py"),),
        removed_paths=(),
    )
    first_sample = StageSampleObservationEvidence(
        duration_seconds=2.0,
        build_work=first_work,
    )
    second_sample = StageSampleObservationEvidence(
        duration_seconds=1.0,
        build_work=second_work,
    )

    with pytest.raises(ValueError, match="match the group BuildWorkEvidence"):
        StageWorkContextGroupEvidence(
            build_work=first_work,
            observations=(second_sample,),
        )

    first_group = StageWorkContextGroupEvidence(
        build_work=first_work,
        observations=(first_sample,),
    )
    second_group = StageWorkContextGroupEvidence(
        build_work=second_work,
        observations=(second_sample,),
    )
    duplicate_first_group = StageWorkContextGroupEvidence(
        build_work=first_work,
        observations=(first_sample,),
    )

    with pytest.raises(ValueError, match="duplicate equal work contexts"):
        MeasurementStageWorkPartitionEvidence(
            stage="build",
            groups=(first_group, duplicate_first_group),
        )

    build_partition = MeasurementStageWorkPartitionEvidence(
        stage="build",
        groups=(first_group, second_group),
    )
    runtime_partition = MeasurementStageWorkPartitionEvidence(
        stage="runtime",
        groups=(first_group, second_group),
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
        BuildAndRunMeasurementWorkPartitionEvidence(
            condition=condition,
            stages=(runtime_partition, build_partition),
        )

    short_runtime = MeasurementStageWorkPartitionEvidence(
        stage="runtime",
        groups=(
            StageWorkContextGroupEvidence(
                build_work=first_work,
                observations=(first_sample, first_sample),
            ),
            second_group,
        ),
    )
    with pytest.raises(ValueError, match="same observation count"):
        BuildAndRunMeasurementWorkPartitionEvidence(
            condition=condition,
            stages=(build_partition, short_runtime),
        )
