"""FFT and power-spectral-density utilities."""

from __future__ import annotations

import numpy as np
from scipy import signal as scipy_signal

from .validation import as_signal_array, validate_sampling_frequency


def compute_fft(
    signal: np.ndarray | object,
    sampling_frequency: float,
    *,
    detrend: str | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute a one-sided real FFT along the time axis.

    Returns
    -------
    frequencies_hz, spectrum
        Frequency bins in Hz and the complex one-sided FFT. For multichannel
        input, the spectrum has shape ``(channels, frequencies)``.
    """
    array = as_signal_array(signal)
    fs = validate_sampling_frequency(sampling_frequency)
    if detrend not in {None, "constant", "linear"}:
        raise ValueError("detrend must be None, 'constant', or 'linear'")
    if detrend is not None:
        array = scipy_signal.detrend(array, axis=-1, type=detrend)
    n = array.shape[-1]
    frequencies = np.fft.rfftfreq(n, d=1.0 / fs)
    spectrum = np.fft.rfft(array, axis=-1)
    return frequencies, spectrum


def compute_psd(
    signal: np.ndarray | object,
    sampling_frequency: float,
    *,
    method: str = "welch",
    window: str = "hann",
    nperseg: int | None = None,
    noverlap: int | None = None,
    detrend: str = "constant",
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate a one-sided power spectral density.

    ``welch`` is the default method. The output uses physical frequency units
    (Hz) and PSD units corresponding to signal-units squared per Hz.
    """
    array = as_signal_array(signal)
    fs = validate_sampling_frequency(sampling_frequency)
    method = method.lower()
    if method not in {"welch", "periodogram"}:
        raise ValueError("method must be one of: welch, periodogram")
    if nperseg is not None and (not isinstance(nperseg, (int, np.integer)) or nperseg < 2):
        raise ValueError("nperseg must be an integer greater than or equal to 2")
    if noverlap is not None and (not isinstance(noverlap, (int, np.integer)) or noverlap < 0):
        raise ValueError("noverlap must be a non-negative integer")
    if method == "welch":
        frequencies, psd = scipy_signal.welch(
            array,
            fs=fs,
            window=window,
            nperseg=nperseg,
            noverlap=noverlap,
            detrend=detrend,
            axis=-1,
            scaling="density",
        )
    else:
        frequencies, psd = scipy_signal.periodogram(
            array,
            fs=fs,
            window=window,
            detrend=detrend,
            axis=-1,
            scaling="density",
        )
    return frequencies, psd


def frequency_resolution(sampling_frequency: float, n_samples: int) -> float:
    """Return the nominal FFT frequency-bin spacing in Hz."""
    fs = validate_sampling_frequency(sampling_frequency)
    if not isinstance(n_samples, (int, np.integer)) or n_samples < 1:
        raise ValueError("n_samples must be a positive integer")
    return fs / int(n_samples)


def welch_frequency_resolution(sampling_frequency: float, nperseg: int) -> float:
    """Return the nominal Welch segment frequency-bin spacing in Hz."""
    fs = validate_sampling_frequency(sampling_frequency)
    if not isinstance(nperseg, (int, np.integer)) or nperseg < 2:
        raise ValueError("nperseg must be an integer greater than or equal to 2")
    return fs / int(nperseg)
