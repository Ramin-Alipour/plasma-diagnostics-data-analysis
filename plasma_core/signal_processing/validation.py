"""Validation helpers for common signal-processing workflows."""

from __future__ import annotations

import numpy as np


def as_signal_array(signal: np.ndarray | object) -> np.ndarray:
    """Return a signal-like input as a floating NumPy array.

    ``TimeSeries`` and ``MultichannelTimeSeries`` objects are accepted through
    their ``data`` attribute. The core numerical functions operate on arrays;
    diagnostic-specific data models remain outside the numerical layer.
    """
    if hasattr(signal, "data"):
        signal = getattr(signal, "data")
    array = np.asarray(signal, dtype=float)
    if array.ndim not in (1, 2):
        raise ValueError("signal must be one-dimensional or (channels, time)")
    if array.size == 0:
        raise ValueError("signal must contain at least one sample")
    if not np.all(np.isfinite(array)):
        raise ValueError("signal must contain only finite values")
    return array


def validate_sampling_frequency(sampling_frequency: float) -> float:
    """Validate and return a positive finite sampling frequency in Hz."""
    fs = float(sampling_frequency)
    if not np.isfinite(fs) or fs <= 0:
        raise ValueError("sampling_frequency must be a positive finite value")
    return fs


def validate_axis(axis: int, ndim: int) -> int:
    """Validate an array axis and return its normalized integer value."""
    if not isinstance(axis, (int, np.integer)):
        raise TypeError("axis must be an integer")
    if axis < -ndim or axis >= ndim:
        raise ValueError(f"axis {axis} is out of bounds for an array with {ndim} dimensions")
    return int(axis) % ndim


def validate_cutoff(cutoff: float | tuple[float, float], sampling_frequency: float, filter_type: str) -> None:
    """Validate filter cutoff frequencies against the Nyquist frequency."""
    fs = validate_sampling_frequency(sampling_frequency)
    nyquist = fs / 2.0
    if filter_type in {"lowpass", "highpass"}:
        value = float(cutoff)  # type: ignore[arg-type]
        if not np.isfinite(value) or value <= 0 or value >= nyquist:
            raise ValueError("cutoff must be between 0 and the Nyquist frequency")
    elif filter_type in {"bandpass", "bandstop"}:
        if not isinstance(cutoff, (tuple, list, np.ndarray)) or len(cutoff) != 2:
            raise ValueError("bandpass and bandstop cutoff must contain two frequencies")
        low, high = map(float, cutoff)
        if not (np.isfinite(low) and np.isfinite(high)) or low <= 0 or high <= low or high >= nyquist:
            raise ValueError("band cutoff frequencies must satisfy 0 < low < high < Nyquist")
    else:
        raise ValueError("filter_type must be one of: lowpass, highpass, bandpass, bandstop")
