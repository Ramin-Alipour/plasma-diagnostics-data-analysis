"""Continuous Morlet-wavelet analysis for magnetic signals.

The implementation uses SciPy FFT convolution and an analytic complex-Morlet
wavelet, avoiding a diagnostic-specific dependency on a wavelet package.
"""
from __future__ import annotations
import numpy as np
from scipy.signal import fftconvolve
from core.signal_processing.validation import as_signal_array, validate_sampling_frequency

_MORLET_W0 = 6.0


def _scales_from_frequencies(frequencies: np.ndarray, sampling_frequency: float) -> np.ndarray:
    """Convert physical frequencies to Morlet scales using w0=6."""
    dt = 1.0 / sampling_frequency
    return _MORLET_W0 / (2.0 * np.pi * frequencies * dt)


def _morlet_wavelet(scale: float, sampling_period: float, support: float = 5.0) -> np.ndarray:
    """Construct a finite-support L2-normalized complex Morlet wavelet."""
    half_width = max(1, int(np.ceil(support * scale)))
    time = np.arange(-half_width, half_width + 1, dtype=float) * sampling_period
    tau = time / (scale * sampling_period)
    wavelet = np.pi ** (-0.25) * np.exp(1j * _MORLET_W0 * tau) * np.exp(-0.5 * tau**2)
    wavelet /= np.sqrt(scale)
    return wavelet


def _cwt_one(signal: np.ndarray, scales: np.ndarray, sampling_period: float) -> np.ndarray:
    coefficients = np.empty((scales.size, signal.size), dtype=complex)
    for i, scale in enumerate(scales):
        wavelet = _morlet_wavelet(float(scale), sampling_period)
        coefficients[i] = fftconvolve(signal, np.conjugate(wavelet[::-1]), mode="same") * sampling_period
    return coefficients


def compute_cwt(signal, sampling_frequency: float, *, wavelet: str = "morlet", frequencies=None, scales=None):
    """Compute a continuous wavelet transform with Morlet as the default.

    Parameters
    ----------
    signal:
        One-dimensional signal or channels-by-time array.
    sampling_frequency:
        Sampling frequency in Hz.
    wavelet:
        Currently ``"morlet"`` only. The parameter is explicit so additional
        wavelet families can be added without changing the public API.
    frequencies:
        Desired analysis frequencies in Hz. These are converted to Morlet
        scales using the central-frequency relation for ``w0=6``.
    scales:
        Positive Morlet scales. Provide either ``frequencies`` or ``scales``.

    Returns
    -------
    coefficients, frequencies_hz, scales
        Complex CWT coefficients, physical frequencies, and scales. For
        multichannel input coefficients have shape (channels, scales, time).
    """
    array = as_signal_array(signal)
    fs = validate_sampling_frequency(sampling_frequency)
    if wavelet.lower() != "morlet":
        raise ValueError("wavelet must be 'morlet' in the current implementation")
    if frequencies is not None and scales is not None:
        raise ValueError("provide either frequencies or scales, not both")
    if frequencies is None and scales is None:
        frequencies = np.geomspace(max(fs / 1000.0, 1.0), fs / 4.0, 64)
    if frequencies is not None:
        frequencies = np.asarray(frequencies, dtype=float)
        if frequencies.ndim != 1 or frequencies.size == 0 or not np.all(np.isfinite(frequencies)):
            raise ValueError("frequencies must be a finite one-dimensional array")
        if np.any(frequencies <= 0) or np.any(frequencies >= fs / 2):
            raise ValueError("frequencies must be strictly between zero and Nyquist")
        scales = _scales_from_frequencies(frequencies, fs)
    else:
        scales = np.asarray(scales, dtype=float)
        if scales.ndim != 1 or scales.size == 0 or not np.all(np.isfinite(scales)) or np.any(scales <= 0):
            raise ValueError("scales must be a finite positive one-dimensional array")
        frequencies = _MORLET_W0 / (2.0 * np.pi * scales) * fs
        if np.any(frequencies <= 0) or np.any(frequencies >= fs / 2):
            raise ValueError("scales must map to frequencies strictly between zero and Nyquist")

    dt = 1.0 / fs
    if array.ndim == 1:
        coefficients = _cwt_one(array, scales, dt)
    else:
        coefficients = np.stack([_cwt_one(row, scales, dt) for row in array], axis=0)
    return coefficients, np.asarray(frequencies, dtype=float), np.asarray(scales, dtype=float)
