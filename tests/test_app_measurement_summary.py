from dataclasses import fields, replace

import pytest

from pyxis.app.measurement_dispersion import create_build_and_run_measurement_population_standard_deviation
from pyxis.app.measurement_summary import BuildAndRunMeasurementDescriptiveSummaryEvidence, create_build_and_run_measurement_descriptive_summary
from test_app_measurement_mean import _chain


def test_summary_bundle(tmp_path):
    median, mean = _chain(tmp_path)
    envelope = median.envelope
    dispersion = create_build_and_run_measurement_population_standard_deviation(mean)
    summary = create_build_and_run_measurement_descriptive_summary(envelope, median, mean, dispersion)

    assert summary.envelope is envelope
    assert summary.median is median
    assert summary.mean is mean
    assert summary.dispersion is dispersion
    assert tuple(x.name for x in fields(summary)) == ("envelope", "median", "mean", "dispersion")

    for values in (
        (replace(envelope), median, mean, dispersion),
        (envelope, replace(median), mean, dispersion),
        (envelope, median, replace(mean), dispersion),
    ):
        with pytest.raises(ValueError, match="exact"):
            BuildAndRunMeasurementDescriptiveSummaryEvidence(*values)
