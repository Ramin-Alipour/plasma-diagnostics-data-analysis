"""Time-domain correlation utilities."""

from __future__ import annotations

import numpy as np

from .validation import as_signal_array, validate_sampling_frequency


def cross_correlation(
    signal_a: np.ndarray | object,
    signal_b: np.ndarray | object,
    sampling_frequency: float,
    *,
    normalize: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute full cross-correlation and return lag in seconds.

    Inputs must be one-dimensional and have equal length. Positive lag means
    A positive returned lag corresponds to the correlation convention used
    here; for a copy of ``signal_a`` delayed in ``signal_b``, the correlation
    peak therefore occurs at a negative lag.
    """
    a = as_signal_array(signal_a)
    b = as_signal_array(signal_b)
    fs = validate_sampling_frequency(sampling_frequency)
    if a.ndim != 1 or b.ndim != 1:
        raise ValueError("cross_correlation currently requires one-dimensional signals")
    if a.size != b.size:
        raise ValueError("signals must have the same number of samples")
    a = a - np.mean(a)
    b = b - np.mean(b)
    correlation = np.correlate(a, b, mode="full")
    if normalize:
        denominator = np.sqrt(np.sum(a**2) * np.sum(b**2))
        if denominator == 0:
            raise ValueError("cannot normalize correlation for a zero-variance signal")
        correlation = correlation / denominator
    lags_samples = np.arange(-(a.size - 1), a.size)
    return lags_samples / fs, correlation


def autocorrelation(signal: np.ndarray | object, *, normalize: bool = True) -> np.ndarray:
    """Compute the non-negative-lag autocorrelation of a one-dimensional signal."""
    array = as_signal_array(signal)
    if array.ndim != 1:
        raise ValueError("autocorrelation currently requires a one-dimensional signal")
    centered = array - np.mean(array)
    result = np.correlate(centered, centered, mode="full")[array.size - 1 :]
    if normalize:
        denominator = result[0]
        if denominator <= 0:
            raise ValueError("cannot normalize autocorrelation of a zero-variance signal")
        result = result / denominator
    return result
