import numpy as np
import pytest

from plasma_core.data_model import TimeSeries
from plasma_core.signal_processing import (
    apply_filter,
    autocorrelation,
    compute_fft,
    compute_psd,
    cross_correlation,
    detrend_signal,
    frequency_resolution,
    normalize_signal,
    remove_offset,
    welch_frequency_resolution,
)


FS = 10_000.0
TIME = np.arange(2_000) / FS


def test_remove_offset_works_per_channel():
    data = np.vstack([np.sin(2 * np.pi * 100 * TIME) + 3, np.cos(2 * np.pi * 200 * TIME) - 2])
    result = remove_offset(data)
    np.testing.assert_allclose(np.mean(result, axis=1), 0.0, atol=1e-12)


def test_detrend_removes_linear_trend():
    signal = 0.5 * TIME + np.sin(2 * np.pi * 100 * TIME)
    result = detrend_signal(signal)
    fitted = np.polyfit(TIME, result, 1)
    assert abs(fitted[0]) < 1e-10


def test_normalization_methods():
    signal = np.sin(2 * np.pi * 100 * TIME)
    z = normalize_signal(signal, method="zscore")
    peak = normalize_signal(signal, method="peak")
    rms = normalize_signal(signal, method="rms")
    assert np.mean(z) == pytest.approx(0, abs=1e-12)
    assert np.std(z) == pytest.approx(1, abs=1e-12)
    assert np.max(np.abs(peak)) == pytest.approx(1)
    assert np.sqrt(np.mean(rms**2)) == pytest.approx(1)


def test_normalize_zero_signal_rejected():
    with pytest.raises(ValueError, match="zero or non-finite"):
        normalize_signal(np.zeros(100))


def test_filter_preserves_low_frequency_and_suppresses_high_frequency():
    signal = np.sin(2 * np.pi * 100 * TIME) + np.sin(2 * np.pi * 2_000 * TIME)
    filtered = apply_filter(signal, FS, "lowpass", 500.0)
    f, spectrum = compute_fft(filtered, FS)
    low = np.abs(spectrum[np.argmin(abs(f - 100))])
    high = np.abs(spectrum[np.argmin(abs(f - 2_000))])
    assert low > 10 * high


def test_bandpass_filter_accepts_two_cutoffs():
    signal = np.sin(2 * np.pi * 100 * TIME) + np.sin(2 * np.pi * 2_000 * TIME)
    filtered = apply_filter(signal, FS, "bandpass", (50.0, 500.0))
    f, spectrum = compute_fft(filtered, FS)
    low = np.abs(spectrum[np.argmin(abs(f - 100))])
    high = np.abs(spectrum[np.argmin(abs(f - 2_000))])
    assert low > 10 * high


def test_filter_cutoff_validation():
    with pytest.raises(ValueError, match="Nyquist"):
        apply_filter(np.ones(1000), FS, "lowpass", FS / 2)


def test_fft_returns_expected_frequency_peak():
    frequency = 500.0
    signal = np.sin(2 * np.pi * frequency * TIME)
    f, spectrum = compute_fft(signal, FS)
    peak = f[np.argmax(np.abs(spectrum))]
    assert peak == pytest.approx(frequency)


def test_fft_accepts_time_series_model():
    ts = TimeSeries(np.sin(2 * np.pi * 100 * TIME), TIME, sampling_frequency=FS)
    f, spectrum = compute_fft(ts, FS)
    assert spectrum.shape == f.shape


def test_psd_recovers_known_frequency():
    frequency = 700.0
    signal = np.sin(2 * np.pi * frequency * TIME)
    f, psd = compute_psd(signal, FS, nperseg=1000)
    peak = f[np.argmax(psd)]
    assert peak == pytest.approx(frequency)


def test_periodogram_psd_recovers_known_frequency():
    frequency = 700.0
    signal = np.sin(2 * np.pi * frequency * TIME)
    f, psd = compute_psd(signal, FS, method="periodogram")
    peak = f[np.argmax(psd)]
    assert peak == pytest.approx(frequency)


def test_psd_multichannel_shape():
    data = np.vstack([np.sin(2 * np.pi * 100 * TIME), np.sin(2 * np.pi * 200 * TIME)])
    f, psd = compute_psd(data, FS, nperseg=1000)
    assert psd.shape == (2, f.size)


def test_spectral_resolution():
    assert frequency_resolution(1_000.0, 1_000) == pytest.approx(1.0)
    assert welch_frequency_resolution(1_000.0, 250) == pytest.approx(4.0)


def test_cross_correlation_peak_for_known_shift():
    n = 1000
    t = np.arange(n) / FS
    a = np.sin(2 * np.pi * 100 * t)
    shift = 20
    b = np.zeros_like(a)
    b[shift:] = a[:-shift]
    lags, corr = cross_correlation(a, b, FS)
    peak_lag = lags[np.argmax(corr)]
    assert peak_lag == pytest.approx(-shift / FS)


def test_autocorrelation_is_normalized_at_zero_lag():
    result = autocorrelation(np.sin(2 * np.pi * 100 * TIME))
    assert result[0] == pytest.approx(1.0)


def test_cross_correlation_rejects_mismatched_lengths():
    with pytest.raises(ValueError, match="same number of samples"):
        cross_correlation(np.ones(10), np.ones(11), FS)


def test_psd_rejects_unknown_method():
    with pytest.raises(ValueError, match="periodogram"):
        compute_psd(np.ones(100), FS, method="unknown")


def test_signal_validation_rejects_nan():
    with pytest.raises(ValueError, match="finite"):
        compute_fft(np.array([0.0, np.nan, 1.0]), FS)
