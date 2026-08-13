from __future__ import annotations

from dataclasses import dataclass

from .measurement import BuildWorkEvidence, MeasurementStage
from .measurement_cohort import MeasurementCohortConditionEvidence
from .measurement_samples import (
    BuildAndRunMeasurementStageSamplesEvidence,
    StageSampleObservationEvidence,
)


@dataclass(frozen=True, slots=True)
class StageWorkContextGroupEvidence:
    """Raw stage samples sharing one exact compiler/materializer work context."""

    build_work: BuildWorkEvidence
    observations: tuple[StageSampleObservationEvidence, ...]

    def __post_init__(self) -> None:
        if not self.observations:
            raise ValueError("Stage work-context group requires at least one observation.")
        if any(observation.build_work != self.build_work for observation in self.observations):
            raise ValueError(
                "Stage work-context group observations must match the group BuildWorkEvidence."
            )


@dataclass(frozen=True, slots=True)
class MeasurementStageWorkPartitionEvidence:
    """First-occurrence-ordered exact work-context groups for one measurement stage."""

    stage: MeasurementStage
    groups: tuple[StageWorkContextGroupEvidence, ...]

    def __post_init__(self) -> None:
        if not self.groups:
            raise ValueError("Measurement stage work partition requires at least one group.")

        if sum(len(group.observations) for group in self.groups) < 2:
            raise ValueError(
                "Measurement stage work partition requires at least two observations."
            )

        for index, group in enumerate(self.groups):
            if any(
                group.build_work == prior.build_work
                for prior in self.groups[:index]
            ):
                raise ValueError(
                    "Measurement stage work partition cannot contain duplicate equal work contexts."
                )


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementWorkPartitionEvidence:
    """Pure exact-work partition of raw samples from one coherent measurement cohort."""

    condition: MeasurementCohortConditionEvidence
    stages: tuple[MeasurementStageWorkPartitionEvidence, ...]

    def __post_init__(self) -> None:
        stage_names = tuple(stage.stage for stage in self.stages)
        if stage_names != self.condition.stages:
            raise ValueError(
                "Measurement work partition must preserve the cohort stage contract."
            )

        observation_counts = {
            sum(len(group.observations) for group in stage.groups)
            for stage in self.stages
        }
        if len(observation_counts) != 1:
            raise ValueError(
                "Measurement work partition must preserve the same observation count for every stage."
            )


def _partition_stage(
    stage: MeasurementStage,
    observations: tuple[StageSampleObservationEvidence, ...],
) -> MeasurementStageWorkPartitionEvidence:
    grouped: list[tuple[BuildWorkEvidence, list[StageSampleObservationEvidence]]] = []

    for observation in observations:
        for build_work, members in grouped:
            if observation.build_work == build_work:
                members.append(observation)
                break
        else:
            grouped.append((observation.build_work, [observation]))

    return MeasurementStageWorkPartitionEvidence(
        stage=stage,
        groups=tuple(
            StageWorkContextGroupEvidence(
                build_work=build_work,
                observations=tuple(members),
            )
            for build_work, members in grouped
        ),
    )


def partition_build_and_run_measurement_stage_samples(
    samples: BuildAndRunMeasurementStageSamplesEvidence,
) -> BuildAndRunMeasurementWorkPartitionEvidence:
    """Partition raw stage samples by exact BuildWorkEvidence equality.

    Group order follows the first occurrence of each exact work-evidence value in
    the stage sample stream. Observation order within a group remains the original
    stage order, and the original ``StageSampleObservationEvidence`` objects are
    retained rather than copied. The first sample in each equality class supplies
    the exact ``BuildWorkEvidence`` object used as that group's key.

    This boundary performs no execution, filesystem access, sorting, aggregation,
    semantic work-state labeling, scoring, or causal interpretation.
    """

    return BuildAndRunMeasurementWorkPartitionEvidence(
        condition=samples.condition,
        stages=tuple(
            _partition_stage(stage.stage, stage.observations)
            for stage in samples.stages
        ),
    )
