from __future__ import annotations

from dataclasses import dataclass
from statistics import median

from .measurement import MeasurementStage
from .measurement_envelope import (
    BuildAndRunMeasurementDurationEnvelopeEvidence,
    StageWorkContextDurationEnvelopeEvidence,
)


@dataclass(frozen=True, slots=True)
class StageWorkContextMedianEvidence:
    """Median duration for one exact 11I work-context envelope."""

    envelope: StageWorkContextDurationEnvelopeEvidence
    median_seconds: float

    def __post_init__(self) -> None:
        expected = float(
            median(
                observation.duration_seconds
                for observation in self.envelope.group.observations
            )
        )
        if self.median_seconds != expected:
            raise ValueError(
                "Work-context median_seconds must match the exact source envelope observations."
            )


@dataclass(frozen=True, slots=True)
class MeasurementStageMedianEvidence:
    """Ordered medians for the exact work-context envelopes of one stage."""

    stage: MeasurementStage
    groups: tuple[StageWorkContextMedianEvidence, ...]

    def __post_init__(self) -> None:
        if not self.groups:
            raise ValueError("Measurement stage median evidence requires at least one group.")


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementMedianEvidence:
    """Median-only central-tendency evidence over one exact 11I envelope."""

    envelope: BuildAndRunMeasurementDurationEnvelopeEvidence
    stages: tuple[MeasurementStageMedianEvidence, ...]

    def __post_init__(self) -> None:
        stage_names = tuple(stage.stage for stage in self.stages)
        envelope_stage_names = tuple(stage.stage for stage in self.envelope.stages)
        if stage_names != envelope_stage_names:
            raise ValueError(
                "Measurement median evidence must preserve the source envelope stage contract."
            )

        for source_stage, median_stage in zip(
            self.envelope.stages,
            self.stages,
            strict=True,
        ):
            if len(source_stage.groups) != len(median_stage.groups):
                raise ValueError(
                    "Measurement median evidence must preserve every source envelope group."
                )
            for source_group, median_group in zip(
                source_stage.groups,
                median_stage.groups,
                strict=True,
            ):
                if median_group.envelope is not source_group:
                    raise ValueError(
                        "Measurement median evidence must retain the exact source envelope group object."
                    )


def create_build_and_run_measurement_median(
    envelope: BuildAndRunMeasurementDurationEnvelopeEvidence,
) -> BuildAndRunMeasurementMedianEvidence:
    """Compute median only within each exact 11I work-context envelope.

    Stage and work-context ordering are preserved. Every median retains the exact
    source ``StageWorkContextDurationEnvelopeEvidence`` object, and the top-level
    result retains the exact 11I envelope. This boundary computes no mean,
    dispersion, additional quantile, semantic label, score, or causal interpretation.
    """

    return BuildAndRunMeasurementMedianEvidence(
        envelope=envelope,
        stages=tuple(
            MeasurementStageMedianEvidence(
                stage=stage.stage,
                groups=tuple(
                    StageWorkContextMedianEvidence(
                        envelope=group,
                        median_seconds=float(
                            median(
                                observation.duration_seconds
                                for observation in group.group.observations
                            )
                        ),
                    )
                    for group in stage.groups
                ),
            )
            for stage in envelope.stages
        ),
    )
