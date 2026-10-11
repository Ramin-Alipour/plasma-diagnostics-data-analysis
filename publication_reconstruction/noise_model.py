"""Reproducible noise model for synthetic robustness tests.

This generates synthetic perturbations around publication-derived reference
values. It never modifies the reference array or represents raw IR-T1 data.
"""
from __future__ import annotations

from typing import Literal
import numpy as np
from numpy.typing import ArrayLike, NDArray

ZeroPolicy = Literal["preserve", "scale"]

def add_relative_gaussian_noise(reference: ArrayLike, *, relative_sigma: float = 0.013,
                                seed: int = 20261011, zero_policy: ZeroPolicy = "preserve",
                                zero_scale: float | None = None) -> NDArray[np.float64]:
    """Return a synthetic noisy copy of reference.

    For nonzero x, Gaussian noise has standard deviation relative_sigma*abs(x).
    0.013 means a 1.3% relative standard deviation, not a per-point error cap.
    Zero policy is either preserve (default) or scale; scale requires an explicit
    positive zero_scale in the same units. Input is never mutated.
    """
    values = np.asarray(reference, dtype=np.float64)
    if values.size == 0:
        return values.copy()
    if not np.all(np.isfinite(values)):
        raise ValueError("reference values must all be finite")
    if not np.isfinite(relative_sigma) or relative_sigma < 0:
        raise ValueError("relative_sigma must be finite and non-negative")
    if zero_policy not in ("preserve", "scale"):
        raise ValueError("zero_policy must be preserve or scale")
    if zero_policy == "scale" and (zero_scale is None or not np.isfinite(zero_scale) or zero_scale <= 0):
        raise ValueError("zero_policy=scale requires positive finite zero_scale")
    rng = np.random.default_rng(seed)
    sigma = relative_sigma * np.abs(values)
    if zero_policy == "scale":
        sigma = np.where(values == 0.0, relative_sigma * float(zero_scale), sigma)
    result = values + rng.normal(0.0, sigma, size=values.shape)
    if zero_policy == "preserve":
        result = np.where(values == 0.0, 0.0, result)
    return np.asarray(result, dtype=np.float64)
