"""Derived plasma-parameter utilities used by electrostatic workflows."""
from __future__ import annotations
import numpy as np
from scipy.constants import atomic_mass, e


def ion_sound_speed_m_s(electron_temperature_eV: float, ion_mass_amu: float) -> float:
    """Return the cold-ion ion-acoustic speed ``sqrt(e Te / m_i)``.

    ``electron_temperature_eV`` is in eV and ``ion_mass_amu`` is in atomic
    mass units. The result is in m/s. Finite ion-temperature corrections are
    intentionally outside this initial synthetic workflow.
    """
    if not np.isfinite(electron_temperature_eV) or electron_temperature_eV <= 0:
        raise ValueError("electron_temperature_eV must be positive and finite")
    if not np.isfinite(ion_mass_amu) or ion_mass_amu <= 0:
        raise ValueError("ion_mass_amu must be positive and finite")
    return float(np.sqrt(e * electron_temperature_eV / (ion_mass_amu * atomic_mass)))
