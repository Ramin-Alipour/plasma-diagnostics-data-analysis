"""Spectral preprocessing utilities."""
from __future__ import annotations
import numpy as np


def subtract_baseline(wavelengths, intensity, *, degree: int = 1, mask=None):
    """Fit and subtract a polynomial baseline from a spectrum."""
    x = np.asarray(wavelengths, dtype=float); y = np.asarray(intensity, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < degree + 1:
        raise ValueError("wavelengths and intensity must be one-dimensional arrays of compatible length")
    if degree < 0 or not isinstance(degree, (int, np.integer)):
        raise ValueError("degree must be a non-negative integer")
    use = np.ones(x.size, dtype=bool) if mask is None else np.asarray(mask, dtype=bool)
    if use.shape != x.shape or np.count_nonzero(use) < degree + 1:
        raise ValueError("mask must select enough samples for the requested baseline degree")
    coeff = np.polyfit(x[use], y[use], int(degree))
    baseline = np.polyval(coeff, x)
    return y - baseline, baseline, coeff
