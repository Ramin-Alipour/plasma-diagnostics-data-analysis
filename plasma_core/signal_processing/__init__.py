"""Reusable, diagnostic-agnostic signal-processing functions."""

from .correlation import autocorrelation, cross_correlation
from .preprocessing import apply_filter, detrend_signal, normalize_signal, remove_offset
from .spectral import compute_fft, compute_psd, frequency_resolution, welch_frequency_resolution

__all__ = [
    "apply_filter",
    "autocorrelation",
    "compute_fft",
    "compute_psd",
    "cross_correlation",
    "detrend_signal",
    "frequency_resolution",
    "normalize_signal",
    "remove_offset",
    "welch_frequency_resolution",
]
