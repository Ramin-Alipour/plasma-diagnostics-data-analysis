"""Turbulent momentum-flux (Reynolds-stress) utilities."""
from __future__ import annotations
import numpy as np


def _pair(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or a.size != b.size or a.size < 2:
        raise ValueError("signals must be one-dimensional, equal-length, and contain at least two samples")
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("signals must contain only finite values")
    return a - np.mean(a), b - np.mean(b)


def reynolds_stress(radial_velocity_m_s, poloidal_velocity_m_s) -> float:
    """Return ``<v_tilde_r v_tilde_theta>`` in m²/s²."""
    vr, vt = _pair(radial_velocity_m_s, poloidal_velocity_m_s)
    return float(np.mean(vr * vt))


def reynolds_force(radial_position_m, reynolds_stress_profile_m2_s2):
    """Return ``-d<vr_tilde vtheta_tilde>/dr`` in m/s²."""
    r = np.asarray(radial_position_m, dtype=float)
    stress = np.asarray(reynolds_stress_profile_m2_s2, dtype=float)
    if r.ndim != 1 or stress.ndim != 1 or r.size != stress.size or r.size < 2:
        raise ValueError("position and stress profile must be equal-length one-dimensional arrays")
    if np.any(~np.isfinite(r)) or np.any(~np.isfinite(stress)) or np.any(np.diff(r) <= 0):
        raise ValueError("position and stress must be finite and position strictly increasing")
    return -np.gradient(stress, r)
