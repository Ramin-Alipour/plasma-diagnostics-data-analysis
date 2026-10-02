"""Common cross-diagnostic statistical and spectral comparisons."""
from __future__ import annotations
import numpy as np
from scipy.signal import correlate, welch
from plasma_core.data_model import TimeSeries


def _pair(a: TimeSeries, b: TimeSeries):
    if a.time.size != b.time.size or not np.allclose(a.time, b.time, rtol=1e-9, atol=1e-12):
        raise ValueError("signals must share the same time axis; align them explicitly first")
    x = a.data - np.mean(a.data); y = b.data - np.mean(b.data)
    if np.std(x) == 0 or np.std(y) == 0:
        raise ValueError("signals must have non-zero variance")
    return x, y


def correlation_coefficient(a: TimeSeries, b: TimeSeries) -> float:
    """Return zero-lag Pearson correlation after explicit time alignment."""
    x, y = _pair(a, b)
    return float(np.corrcoef(x, y)[0, 1])


def cross_correlation(a: TimeSeries, b: TimeSeries) -> tuple[np.ndarray, np.ndarray, float, float]:
    """Return normalized cross-correlation and the lag of its maximum.

    Positive lag means the maximum occurs at a positive value of the lag axis;
    it is reported as a temporal offset only and is not interpreted as causality.
    """
    x, y = _pair(a, b)
    fs = a.inferred_sampling_frequency
    if fs is None:
        raise ValueError("cross_correlation requires a uniformly sampled time axis")
    corr = correlate(x, y, mode="full") / np.sqrt(np.sum(x*x) * np.sum(y*y))
    lags = np.arange(-x.size + 1, x.size) / fs
    i = int(np.argmax(np.abs(corr)))
    return lags, corr, float(lags[i]), float(corr[i])


def spectral_comparison(a: TimeSeries, b: TimeSeries, *, method: str = "welch", nperseg: int | None = None):
    """Return comparable PSD estimates for two aligned signals."""
    if method != "welch":
        raise ValueError("method must be 'welch' in the initial implementation")
    _pair(a, b)
    fs = a.inferred_sampling_frequency
    if fs is None:
        raise ValueError("spectral comparison requires a uniformly sampled time axis")
    f_a, p_a = welch(a.data, fs=fs, nperseg=nperseg, scaling="density", detrend="linear")
    f_b, p_b = welch(b.data, fs=fs, nperseg=nperseg, scaling="density", detrend="linear")
    if not np.allclose(f_a, f_b):
        raise ValueError("aligned signals produced different frequency axes")
    return {"frequency_hz": f_a, "psd_a": p_a, "psd_b": p_b, "method": method}
