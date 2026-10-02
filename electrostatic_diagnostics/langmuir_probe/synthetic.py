"""Controlled synthetic Langmuir I-V characteristics.

The model is a compact, smooth-in-physics approximation intended for
algorithm validation. It is not a full sheath/collection model and does not
represent a reconstruction of IR-T1 probe data.
"""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class LangmuirSyntheticConfig:
    """Parameters for a synthetic single-probe I-V characteristic."""

    voltage_min: float = -25.0
    voltage_max: float = 25.0
    n_points: int = 501
    plasma_potential: float = 8.0
    electron_temperature_eV: float = 6.0
    ion_saturation_current: float = 2.0e-3
    electron_saturation_current: float = 4.0e-3
    noise_std: float = 2.0e-5
    random_seed: int = 42


def _validate_config(config: LangmuirSyntheticConfig) -> None:
    if config.n_points < 20:
        raise ValueError("n_points must be at least 20")
    if not config.voltage_min < config.voltage_max:
        raise ValueError("voltage_min must be smaller than voltage_max")
    if not config.voltage_min < config.plasma_potential < config.voltage_max:
        raise ValueError("plasma_potential must lie inside the voltage range")
    for name in ("electron_temperature_eV", "ion_saturation_current", "electron_saturation_current"):
        if not np.isfinite(getattr(config, name)) or getattr(config, name) <= 0:
            raise ValueError(f"{name} must be positive and finite")
    if not np.isfinite(config.noise_std) or config.noise_std < 0:
        raise ValueError("noise_std must be finite and non-negative")


def langmuir_iv_model(
    voltage: np.ndarray | float,
    ion_saturation_current: float,
    electron_saturation_current: float,
    plasma_potential: float,
    electron_temperature_eV: float,
) -> np.ndarray:
    """Return the synthetic net current for the repository's I-V model.

    Below ``plasma_potential`` the electron current follows an exponential
    retardation law; above it the electron current saturates. Ion current is
    represented by a constant negative saturation current. ``Te`` is in eV,
    so the exponential argument is dimensionless for voltage in volts.
    """
    if electron_temperature_eV <= 0:
        raise ValueError("electron_temperature_eV must be positive")
    voltage = np.asarray(voltage, dtype=float)
    electron_current = np.where(
        voltage < plasma_potential,
        electron_saturation_current * np.exp((voltage - plasma_potential) / electron_temperature_eV),
        electron_saturation_current,
    )
    return electron_current - ion_saturation_current


def generate_synthetic_langmuir_iv(config: LangmuirSyntheticConfig | None = None):
    """Generate a noisy synthetic Langmuir I-V dataset with known parameters."""
    if config is None:
        config = LangmuirSyntheticConfig()
    _validate_config(config)
    voltage = np.linspace(config.voltage_min, config.voltage_max, config.n_points)
    current_clean = langmuir_iv_model(
        voltage,
        config.ion_saturation_current,
        config.electron_saturation_current,
        config.plasma_potential,
        config.electron_temperature_eV,
    )
    rng = np.random.default_rng(config.random_seed)
    current = current_clean + rng.normal(0.0, config.noise_std, size=voltage.size)
    return {
        "voltage": voltage,
        "current": current,
        "current_clean": current_clean,
        "plasma_potential": config.plasma_potential,
        "electron_temperature_eV": config.electron_temperature_eV,
        "ion_saturation_current": config.ion_saturation_current,
        "electron_saturation_current": config.electron_saturation_current,
        "noise_std": config.noise_std,
        "random_seed": config.random_seed,
    }
