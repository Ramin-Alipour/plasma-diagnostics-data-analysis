"""Common preprocessing operations for scientific time-series signals."""

from __future__ import annotations

import numpy as np
from scipy import signal as scipy_signal

from .validation import as_signal_array, validate_cutoff, validate_sampling_frequency


def remove_offset(signal: np.ndarray | object) -> np.ndarray:
    """Remove the mean offset independently from each signal/channel."""
    array = as_signal_array(signal)
    return array - np.mean(array, axis=-1, keepdims=True)


def detrend_signal(signal: np.ndarray | object, *, type: str = "linear") -> np.ndarray:
    """Remove a constant or linear trend along the time axis."""
    array = as_signal_array(signal)
    if type not in {"constant", "linear"}:
        raise ValueError("type must be 'constant' or 'linear'")
    return scipy_signal.detrend(array, axis=-1, type=type)


def normalize_signal(signal: np.ndarray | object, *, method: str = "zscore") -> np.ndarray:
    """Normalize each signal/channel independently along the time axis.

    Supported methods are ``zscore``, ``peak``, and ``rms``. A zero-scale
    signal raises ``ValueError`` rather than silently producing invalid data.
    """
    array = as_signal_array(signal)
    method = method.lower()
    if method == "zscore":
        scale = np.std(array, axis=-1, keepdims=True)
        center = np.mean(array, axis=-1, keepdims=True)
    elif method == "peak":
        center = np.zeros_like(np.mean(array, axis=-1, keepdims=True))
        scale = np.max(np.abs(array), axis=-1, keepdims=True)
    elif method == "rms":
        center = np.zeros_like(np.mean(array, axis=-1, keepdims=True))
        scale = np.sqrt(np.mean(array**2, axis=-1, keepdims=True))
    else:
        raise ValueError("method must be one of: zscore, peak, rms")
    if np.any(scale <= 0) or not np.all(np.isfinite(scale)):
        raise ValueError("cannot normalize a signal with zero or non-finite scale")
    return (array - center) / scale


def apply_filter(
    signal: np.ndarray | object,
    sampling_frequency: float,
    filter_type: str,
    cutoff: float | tuple[float, float],
    *,
    order: int = 4,
) -> np.ndarray:
    """Apply a Butterworth zero-phase filter along the time axis.

    The implementation uses second-order sections with ``sosfiltfilt`` for
    numerically stable offline analysis. It does not represent a real-time
    causal filter.
    """
    array = as_signal_array(signal)
    fs = validate_sampling_frequency(sampling_frequency)
    kind = filter_type.lower().replace("-", "")
    aliases = {"lowpass": "lowpass", "highpass": "highpass", "bandpass": "bandpass", "bandstop": "bandstop"}
    if kind not in aliases:
        raise ValueError("filter_type must be one of: lowpass, highpass, bandpass, bandstop")
    if not isinstance(order, (int, np.integer)) or order < 1:
        raise ValueError("order must be a positive integer")
    validate_cutoff(cutoff, fs, kind)
    normalized = np.asarray(cutoff, dtype=float) / (fs / 2.0)
    sos = scipy_signal.butter(order, normalized, btype=kind, output="sos")
    return scipy_signal.sosfiltfilt(sos, array, axis=-1)
