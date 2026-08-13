from math import sqrt
from pyxis.app.measurement_dispersion import create_build_and_run_measurement_population_standard_deviation as sd
from pyxis.app.measurement_summary import create_build_and_run_measurement_descriptive_summary as bundle
from pyxis.app.measurement_summary_presentation import create_build_and_run_measurement_summary_presentation as project
from test_app_measurement_mean import _chain


def test_projection_values(tmp_path):
    median, mean = _chain(tmp_path)
    envelope = median.envelope
    view = project(bundle(envelope, median, mean, sd(mean)))
    reused = view.stages[0].groups[1]
    assert reused.build_work is envelope.stages[0].groups[1].group.build_work
    assert (reused.sample_count, reused.minimum_seconds, reused.maximum_seconds) == (4, .5, 1.5)
    assert (reused.median_seconds, reused.mean_seconds, reused.population_standard_deviation_seconds) == (.875, .9375, sqrt(.13671875))
