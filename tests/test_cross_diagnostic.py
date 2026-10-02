import numpy as np
import pytest
from plasma_core.data_model import TimeSeries
from cross_diagnostic.alignment import align_time_series, interpolate_to_time, resample_time_series
from cross_diagnostic.comparison import correlation_coefficient, cross_correlation, spectral_comparison
from cross_diagnostic.metadata import ExperimentalCondition, compare_with_conditions
from cross_diagnostic.synthetic import magnetic_hxr_pair, electrostatic_turbulence_pair
from turbulence_transport.transport_analysis.flux import turbulent_radial_particle_flux


def test_interpolation_and_resampling_are_explicit():
    a = TimeSeries(np.sin(2*np.pi*10*np.arange(100)/1000), np.arange(100)/1000, 1000, "a.u.")
    t = np.arange(20)/200
    out = interpolate_to_time(a, t)
    assert out.n_samples == 20
    res = resample_time_series(a, 500)
    assert np.isclose(res.inferred_sampling_frequency, 500)


def test_alignment_rejects_mismatched_rates_without_target():
    a = TimeSeries(np.arange(100.), np.arange(100)/1000, 1000)
    b = TimeSeries(np.arange(80.), np.arange(80)/800, 800)
    with pytest.raises(ValueError, match="differ"):
        align_time_series(a, b)


def test_alignment_with_explicit_target():
    a = TimeSeries(np.sin(np.arange(100)/10), np.arange(100)/1000, 1000)
    b = TimeSeries(np.sin(np.arange(80)/8), np.arange(80)/800, 800)
    aa, bb = align_time_series(a, b, target_sampling_frequency_hz=400)
    assert aa.n_samples == bb.n_samples
    assert np.allclose(aa.time, bb.time)
    assert aa.analysis_metadata["alignment"]["explicit_resampling_requested"]


def test_comparisons_require_aligned_time_axis():
    t = np.arange(100)/1000
    a = TimeSeries(np.sin(2*np.pi*20*t), t, 1000)
    b = TimeSeries(np.cos(2*np.pi*20*t), t, 1000)
    assert abs(correlation_coefficient(a,b)) < 0.01
    lags, corr, lag, peak = cross_correlation(a,b)
    assert lags.size == 199
    assert np.isfinite(lag) and np.isfinite(peak)
    spec = spectral_comparison(a,b, nperseg=64)
    assert spec["frequency_hz"].shape == spec["psd_a"].shape


def test_conditions_are_separate_from_signals():
    paired = compare_with_conditions([1,2], [ExperimentalCondition({"pressure_Torr":1.9}), ExperimentalCondition({"pressure_Torr":2.3})])
    assert paired[1]["condition"].values["pressure_Torr"] == 2.3


def test_unified_magnetic_hxr_pair():
    mag, hxr = magnetic_hxr_pair()
    ma, xa = align_time_series(mag, hxr, target_sampling_frequency_hz=400_000)
    assert ma.n_samples == xa.n_samples
    assert np.isfinite(correlation_coefficient(ma, xa))
    assert spectral_comparison(ma, xa)["frequency_hz"].size > 1


def test_unified_electrostatic_turbulence_pair():
    potential, density, velocity = electrostatic_turbulence_pair()
    assert potential.n_samples == density.n_samples == velocity.n_samples
    flux = turbulent_radial_particle_flux(density.data, velocity.data)
    assert np.isfinite(flux)
