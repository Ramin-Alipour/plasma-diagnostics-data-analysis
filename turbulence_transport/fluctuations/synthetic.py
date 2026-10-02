"""Controlled synthetic turbulence-like fluctuation signals."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TurbulenceSyntheticConfig:
    """Configuration for coupled density and potential fluctuations."""
    sampling_frequency_hz: float = 200_000.0
    duration_s: float = 0.02
    dominant_frequency_hz: float = 12_000.0
    secondary_frequency_hz: float = 27_000.0
    density_mean_m3: float = 1.0e18
    density_fluctuation_fraction: float = 0.08
    potential_mean_v: float = 5.0
    potential_fluctuation_v: float = 1.0
    phase_density_rad: float = 0.55
    phase_potential_rad: float = 0.0
    noise_fraction: float = 0.01
    random_seed: int = 42


def generate_synthetic_fluctuations(config: TurbulenceSyntheticConfig | None = None):
    """Generate synthetic density and electrostatic-potential fluctuations.

    The signals share controlled frequencies and phase relationships. They are
    intended for reproducible transport-method demonstrations, not measured data.
    """
    if config is None:
        config = TurbulenceSyntheticConfig()
    for name in ("sampling_frequency_hz", "duration_s", "dominant_frequency_hz", "secondary_frequency_hz"):
        if not np.isfinite(getattr(config, name)) or getattr(config, name) <= 0:
            raise ValueError(f"{name} must be positive and finite")
    if config.duration_s * config.sampling_frequency_hz < 20:
        raise ValueError("configuration must contain at least 20 samples")
    if config.density_mean_m3 <= 0 or config.potential_mean_v <= 0:
        raise ValueError("mean density and potential must be positive")
    if config.density_fluctuation_fraction < 0 or config.potential_fluctuation_v < 0 or config.noise_fraction < 0:
        raise ValueError("fluctuation amplitudes and noise_fraction must be non-negative")
    n = int(round(config.duration_s * config.sampling_frequency_hz))
    time_s = np.arange(n) / config.sampling_frequency_hz
    rng = np.random.default_rng(config.random_seed)
    envelope = 1.0 + 0.25 * np.sin(2 * np.pi * 500.0 * time_s)
    base = np.sin(2 * np.pi * config.dominant_frequency_hz * time_s)
    secondary = 0.35 * np.sin(2 * np.pi * config.secondary_frequency_hz * time_s + 0.3)
    density_fluctuation = config.density_mean_m3 * config.density_fluctuation_fraction * envelope * (
        base + secondary
    )
    potential_fluctuation = config.potential_fluctuation_v * envelope * (
        np.sin(2 * np.pi * config.dominant_frequency_hz * time_s + config.phase_potential_rad)
        + 0.35 * np.sin(2 * np.pi * config.secondary_frequency_hz * time_s + 0.3)
    )
    density = config.density_mean_m3 + density_fluctuation + rng.normal(
        0.0, config.noise_fraction * config.density_mean_m3, n
    )
    potential = config.potential_mean_v + potential_fluctuation + rng.normal(
        0.0, config.noise_fraction * config.potential_fluctuation_v, n
    )
    return {
        "time_s": time_s,
        "density_m3": density,
        "potential_V": potential,
        "density_fluctuation_m3": density - np.mean(density),
        "potential_fluctuation_V": potential - np.mean(potential),
        "sampling_frequency_hz": config.sampling_frequency_hz,
        "config": config,
        "data_type": "synthetic",
    }
