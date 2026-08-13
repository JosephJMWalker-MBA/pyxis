from __future__ import annotations

from dataclasses import dataclass

from .measurement import MeasurementStage
from .measurement_partition import (
    BuildAndRunMeasurementWorkPartitionEvidence,
    StageWorkContextGroupEvidence,
)


@dataclass(frozen=True, slots=True)
class StageWorkContextDurationEnvelopeEvidence:
    """Literal duration bounds for one exact work-context group."""

    group: StageWorkContextGroupEvidence
    sample_count: int
    minimum_seconds: float
    maximum_seconds: float

    def __post_init__(self) -> None:
        durations = tuple(
            observation.duration_seconds for observation in self.group.observations
        )
        expected_count = len(durations)
        expected_minimum = min(durations)
        expected_maximum = max(durations)

        if self.sample_count != expected_count:
            raise ValueError(
                "Duration envelope sample_count must match the source work-context group."
            )
        if self.minimum_seconds != expected_minimum:
            raise ValueError(
                "Duration envelope minimum_seconds must match the source observations."
            )
        if self.maximum_seconds != expected_maximum:
            raise ValueError(
                "Duration envelope maximum_seconds must match the source observations."
            )


@dataclass(frozen=True, slots=True)
class MeasurementStageDurationEnvelopeEvidence:
    """Ordered exact-work duration envelopes for one measurement stage."""

    stage: MeasurementStage
    groups: tuple[StageWorkContextDurationEnvelopeEvidence, ...]

    def __post_init__(self) -> None:
        if not self.groups:
            raise ValueError("Measurement stage duration envelope requires at least one group.")


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementDurationEnvelopeEvidence:
    """First descriptive compression of one exact-work measurement partition."""

    partition: BuildAndRunMeasurementWorkPartitionEvidence
    stages: tuple[MeasurementStageDurationEnvelopeEvidence, ...]

    def __post_init__(self) -> None:
        stage_names = tuple(stage.stage for stage in self.stages)
        partition_stage_names = tuple(stage.stage for stage in self.partition.stages)
        if stage_names != partition_stage_names:
            raise ValueError(
                "Measurement duration envelope must preserve the partition stage contract."
            )

        for source_stage, envelope_stage in zip(
            self.partition.stages,
            self.stages,
            strict=True,
        ):
            if len(source_stage.groups) != len(envelope_stage.groups):
                raise ValueError(
                    "Measurement duration envelope must preserve every work-context group."
                )
            for source_group, envelope_group in zip(
                source_stage.groups,
                envelope_stage.groups,
                strict=True,
            ):
                if envelope_group.group is not source_group:
                    raise ValueError(
                        "Measurement duration envelope must retain the exact source work-context group object."
                    )


def create_build_and_run_measurement_duration_envelope(
    partition: BuildAndRunMeasurementWorkPartitionEvidence,
) -> BuildAndRunMeasurementDurationEnvelopeEvidence:
    """Compute only count/min/max within each exact 11H work-context group.

    Stage order and work-context group order are preserved from the partition. Each
    group summary retains the exact source ``StageWorkContextGroupEvidence`` object.
    No observations are combined across work contexts, and this boundary computes no
    mean, median, variance, standard deviation, confidence interval, quantile, trend,
    semantic label, score, or causal interpretation.
    """

    return BuildAndRunMeasurementDurationEnvelopeEvidence(
        partition=partition,
        stages=tuple(
            MeasurementStageDurationEnvelopeEvidence(
                stage=stage.stage,
                groups=tuple(
                    StageWorkContextDurationEnvelopeEvidence(
                        group=group,
                        sample_count=len(group.observations),
                        minimum_seconds=min(
                            observation.duration_seconds
                            for observation in group.observations
                        ),
                        maximum_seconds=max(
                            observation.duration_seconds
                            for observation in group.observations
                        ),
                    )
                    for group in stage.groups
                ),
            )
            for stage in partition.stages
        ),
    )
