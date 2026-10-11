import numpy as np
import pandas as pd
import pytest

from spectroscopy.line_width_analysis import summarize_line_width_measurements


def test_line_width_summary_reports_descriptive_statistics_without_mutating_input():
    source = pd.DataFrame({
        "ion": ["A", "B", "C"],
        "wavelength_nm": [400.0, 420.0, 440.0],
        "measured_fwhm_nm": [0.04, 0.06, 0.08],
    })
    original = source.copy(deep=True)

    result = summarize_line_width_measurements(source)

    assert result["n_lines"] == 3
    assert result["wavelength_min_nm"] == 400.0
    assert result["wavelength_max_nm"] == 440.0
    assert np.isclose(result["fwhm_mean_nm"], 0.06)
    assert np.isclose(result["fwhm_median_nm"], 0.06)
    assert np.isclose(result["fwhm_sample_sd_nm"], 0.02)
    assert result["fwhm_min_nm"] == 0.04
    assert result["fwhm_max_nm"] == 0.08
    pd.testing.assert_frame_equal(source, original)


@pytest.mark.parametrize(
    "data, message",
    [
        (pd.DataFrame(columns=["wavelength_nm", "measured_fwhm_nm"]), "at least one"),
        (pd.DataFrame({"wavelength_nm": [400.0]}), "missing required columns"),
        (pd.DataFrame({"wavelength_nm": [np.nan], "measured_fwhm_nm": [0.04]}), "finite"),
        (pd.DataFrame({"wavelength_nm": [400.0], "measured_fwhm_nm": [0.0]}), "positive"),
        (pd.DataFrame({"wavelength_nm": [-400.0], "measured_fwhm_nm": [0.04]}), "positive"),
        (pd.DataFrame({"wavelength_nm": ["not-a-number"], "measured_fwhm_nm": [0.04]}), "numeric"),
    ],
)
def test_line_width_summary_rejects_invalid_inputs(data, message):
    with pytest.raises(ValueError, match=message):
        summarize_line_width_measurements(data)


def test_line_width_summary_uses_zero_sample_sd_for_a_single_line():
    result = summarize_line_width_measurements(
        pd.DataFrame({"wavelength_nm": [400.0], "measured_fwhm_nm": [0.04]})
    )
    assert result["n_lines"] == 1
    assert result["fwhm_sample_sd_nm"] == 0.0
