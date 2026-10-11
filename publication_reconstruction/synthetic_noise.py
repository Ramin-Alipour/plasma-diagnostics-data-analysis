"""Relative Gaussian noise model for synthetic six-paper reconstruction data.

This utility is for newly generated synthetic arrays only. It must not be
applied to Dataset A laboratory/software outputs or Dataset B publication-derived
constraint tables.

For each nonzero reference value x, the additive Gaussian noise has
standard deviation 0.013 * abs(x) by default. A zero reference has no defined
relative scale, so zero entries are preserved exactly rather than introducing
an undocumented absolute noise floor.
"""
from __future__ import annotations

import numpy as np


DEFAULT_RELATIVE_NOISE_STD = 0.013


def add_relative_gaussian_noise(
    reference_values,
    *,
    relative_std: float = DEFAULT_RELATIVE_NOISE_STD,
    seed: int | None = None,
) -> np.ndarray:
    """Return a noisy copy with sigma_i = relative_std * abs(reference_i).

    Zero-valued reference entries are treated separately and remain zero.
    The input is not mutated. A seed makes the noise realization reproducible.
    """
    reference = np.asarray(reference_values, dtype=float)
    if not np.isfinite(reference).all():
        raise ValueError("reference_values must contain only finite values")
    if not np.isfinite(relative_std) or relative_std < 0:
        raise ValueError("relative_std must be finite and non-negative")

    rng = np.random.default_rng(seed)
    sigma = relative_std * np.abs(reference)
    noise = rng.normal(loc=0.0, scale=sigma, size=reference.shape)
    noise = np.where(reference == 0.0, 0.0, noise)
    return reference + noise
