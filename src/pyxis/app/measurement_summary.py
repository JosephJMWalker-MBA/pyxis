from dataclasses import dataclass

from .measurement_dispersion import BuildAndRunMeasurementPopulationStandardDeviationEvidence
from .measurement_envelope import BuildAndRunMeasurementDurationEnvelopeEvidence
from .measurement_mean import BuildAndRunMeasurementMeanEvidence
from .measurement_median import BuildAndRunMeasurementMedianEvidence


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementDescriptiveSummaryEvidence:
    envelope: BuildAndRunMeasurementDurationEnvelopeEvidence
    median: BuildAndRunMeasurementMedianEvidence
    mean: BuildAndRunMeasurementMeanEvidence
    dispersion: BuildAndRunMeasurementPopulationStandardDeviationEvidence

    def __post_init__(self) -> None:
        if self.median.envelope is not self.envelope:
            raise ValueError("Summary median must use the exact envelope.")
        if self.mean.median is not self.median:
            raise ValueError("Summary mean must use the exact median.")
        if self.dispersion.mean is not self.mean:
            raise ValueError("Summary dispersion must use the exact mean.")


def create_build_and_run_measurement_descriptive_summary(envelope, median, mean, dispersion):
    """Bundle existing descriptive evidence; compute nothing new."""
    return BuildAndRunMeasurementDescriptiveSummaryEvidence(envelope, median, mean, dispersion)
