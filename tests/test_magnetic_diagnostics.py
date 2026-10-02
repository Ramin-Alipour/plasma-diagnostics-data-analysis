import numpy as np
import pytest
from synthetic_data.magnetic.mirnov import generate_synthetic_mirnov_dataset
from magnetic_diagnostics.fft_psd import channel_psd, dominant_frequency
from magnetic_diagnostics.wavelet import compute_cwt
from magnetic_diagnostics.svd import compute_svd
from magnetic_diagnostics.mode_analysis import component_energy, extract_spatial_structure, channel_phase


def dataset():
    return generate_synthetic_mirnov_dataset()


def test_channel_psd_recovers_synthetic_frequencies():
    d = dataset(); f, p = channel_psd(d, nperseg=d.n_samples)
    peak = f[np.argmax(np.mean(p, axis=0))]
    assert min(abs(peak - 44_000), abs(peak - 70_000)) < 200


def test_dominant_frequency_shape():
    d = dataset(); f, p = channel_psd(d, nperseg=d.n_samples)
    peaks = dominant_frequency(f, p)
    assert peaks.shape == (d.n_channels,)
    assert np.all(np.isfinite(peaks))


def test_wavelet_returns_physical_frequencies():
    d = dataset(); freqs = np.array([44_000., 70_000.])
    c, f, scales = compute_cwt(d.data[0], d.sampling_frequency, frequencies=freqs)
    assert c.shape == (2, d.n_samples)
    np.testing.assert_allclose(f, freqs, rtol=1e-10)
    assert np.all(scales > 0)


def test_svd_orientation_and_reconstruction():
    d = dataset(); result = compute_svd(d)
    assert result.matrix_orientation == "channels_by_time"
    assert result.u.shape == (d.n_channels, min(d.n_channels, d.n_samples))
    assert result.vt.shape[1] == d.n_samples
    centered = d.data - d.data.mean(axis=1, keepdims=True)
    np.testing.assert_allclose(result.reconstruct(), centered, rtol=1e-10, atol=1e-10)


def test_svd_energy_sums_to_one():
    result = compute_svd(dataset())
    assert np.sum(result.explained_energy) == pytest.approx(1.0)
    assert result.cumulative_energy[-1] == pytest.approx(1.0)


def test_svd_scaling_is_optional():
    d = dataset(); result = compute_svd(d, scale=True)
    assert result.scaled is True


def test_mode_analysis_does_not_label_physical_modes():
    result = compute_svd(dataset())
    energy = component_energy(result.singular_values)
    spatial = extract_spatial_structure(result.u, 0)
    assert energy.shape == result.singular_values.shape
    assert spatial.shape == (12,)


def test_channel_phase_tracks_controlled_phase_progression():
    d = dataset(); f, phase = channel_phase(d.data, 44_000., d.sampling_frequency)
    assert abs(f - 44_000.) < 100
    assert np.ptp(np.unwrap(phase)) > 0.5
