"""Synthetic directional measurements for compound-probe workflow validation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CompoundProbeSyntheticConfig:
    """Configuration for a linear directional-velocity measurement model."""
    true_velocity_m_s: tuple[float, float, float] = (17_000.0, 2_500.0, 1_000.0)
    noise_std_m_s: float = 100.0
    random_seed: int = 42


def generate_synthetic_directional_measurements(config: CompoundProbeSyntheticConfig | None = None):
    """Generate three non-collinear directional measurements of a flow vector.

    The measurement model is ``u_j = d_j dot v + noise``. It represents a
    controlled computational abstraction of directional probe sensitivity, not
    a reconstruction of the detailed IR-T1 compound-probe transfer function.
    """
    if config is None:
        config = CompoundProbeSyntheticConfig()
    v = np.asarray(config.true_velocity_m_s, dtype=float)
    if v.shape != (3,) or np.any(~np.isfinite(v)):
        raise ValueError("true_velocity_m_s must contain three finite components")
    if config.noise_std_m_s < 0 or not np.isfinite(config.noise_std_m_s):
        raise ValueError("noise_std_m_s must be finite and non-negative")
    directions = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0), 0.0],
    ])
    clean = directions @ v
    rng = np.random.default_rng(config.random_seed)
    measured = clean + rng.normal(0.0, config.noise_std_m_s, size=clean.size)
    return {
        "directions": directions,
        "measurements_m_s": measured,
        "clean_measurements_m_s": clean,
        "true_velocity_m_s": v,
        "noise_std_m_s": config.noise_std_m_s,
        "random_seed": config.random_seed,
    }
