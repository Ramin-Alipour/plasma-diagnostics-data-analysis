"""Basic statistical analysis of plasma turbulence fluctuations."""
from __future__ import annotations
import numpy as np


def _finite_equal_1d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.size != b.size or a.size < 2:
        raise ValueError("signals must be one-dimensional, equal-length, and contain at least two samples")
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("signals must contain only finite values")
    return a, b


def decompose_fluctuation(signal):
    """Return mean and zero-mean fluctuation, ``x = mean(x) + x_tilde``."""
    x = np.asarray(signal, dtype=float)
    if x.ndim != 1 or x.size < 2 or np.any(~np.isfinite(x)):
        raise ValueError("signal must be a finite one-dimensional array with at least two samples")
    mean = float(np.mean(x))
    fluctuation = x - mean
    return {"mean": mean, "fluctuation": fluctuation}


def correlation_coefficient(signal_a, signal_b):
    """Return the Pearson correlation coefficient of two fluctuations/signals."""
    a, b = _finite_equal_1d(signal_a, signal_b)
    a = a - np.mean(a)
    b = b - np.mean(b)
    denom = np.sqrt(np.sum(a**2) * np.sum(b**2))
    if denom == 0:
        raise ValueError("correlation is undefined for a zero-variance signal")
    return float(np.sum(a * b) / denom)


def cross_phase(signal_a, signal_b):
    """Estimate the mean phase difference using the complex cross-spectrum.

    The returned phase is the angle of ``sum(A*conj(B))`` after removal of
    the means. It is a compact synthetic-analysis diagnostic, not a full
    frequency-resolved cross-phase analysis.
    """
    a, b = _finite_equal_1d(signal_a, signal_b)
    a = a - np.mean(a)
    b = b - np.mean(b)
    cross = np.vdot(b, a)
    if abs(cross) == 0:
        raise ValueError("cross phase is undefined for zero cross-power")
    return float(np.angle(cross))
