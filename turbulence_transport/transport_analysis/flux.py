"""Synthetic E×B velocity and turbulent particle-flux calculations."""
from __future__ import annotations
import numpy as np


def exb_velocity(electric_field_V_m, magnetic_field_T):
    """Compute ``v_E = E × B / |B|²`` for vector arrays.

    Inputs have shape ``(3, n)`` or ``(3,)`` and use SI units. This is the
    ideal E×B drift only; it is not a model of the total plasma velocity.
    """
    E = np.asarray(electric_field_V_m, dtype=float)
    B = np.asarray(magnetic_field_T, dtype=float)
    if E.shape != B.shape or E.shape[0] != 3 or E.ndim not in (1, 2):
        raise ValueError("electric_field_V_m and magnetic_field_T must have matching shape (3,) or (3, n)")
    if np.any(~np.isfinite(E)) or np.any(~np.isfinite(B)):
        raise ValueError("fields must be finite")
    if E.ndim == 1:
        denom = float(np.dot(B, B))
        if denom == 0:
            raise ValueError("magnetic field magnitude must be non-zero")
        return np.cross(E, B) / denom
    denom = np.sum(B * B, axis=0)
    if np.any(denom == 0):
        raise ValueError("magnetic field magnitude must be non-zero at every sample")
    return np.cross(E.T, B.T).T / denom[None, :]


def fluctuation_flux(quantity_fluctuation, velocity_fluctuation, *, axis=-1) -> float:
    """Return the average turbulent product ``<q_tilde v_tilde>``."""
    q = np.asarray(quantity_fluctuation, dtype=float)
    v = np.asarray(velocity_fluctuation, dtype=float)
    if q.shape != v.shape or q.size < 2 or np.any(~np.isfinite(q)) or np.any(~np.isfinite(v)):
        raise ValueError("fluctuation arrays must be finite and have identical shapes")
    return float(np.mean(q * v, axis=axis)) if q.ndim > 1 else float(np.mean(q * v))


def turbulent_particle_flux(density_m3, velocity_m_s, *, direction="radial") -> float:
    """Return turbulent particle flux ``Gamma=<n_tilde v_tilde>`` in m⁻² s⁻¹.

    ``direction`` is a descriptive label (for example ``"radial"`` or
    ``"poloidal"``); it does not alter the numerical operation.
    """
    if not isinstance(direction, str) or not direction.strip():
        raise ValueError("direction must be a non-empty string")
    n = np.asarray(density_m3, dtype=float)
    vr = np.asarray(velocity_m_s, dtype=float)
    if n.ndim != 1 or vr.ndim != 1 or n.size != vr.size or n.size < 2:
        raise ValueError("density and radial velocity must be equal-length one-dimensional arrays")
    if np.any(~np.isfinite(n)) or np.any(~np.isfinite(vr)):
        raise ValueError("density and velocity must be finite")
    dn = n - np.mean(n)
    dvr = vr - np.mean(vr)
    return float(np.mean(dn * dvr))


def turbulent_radial_particle_flux(density_m3, radial_velocity_m_s) -> float:
    """Return ``Gamma_r=<n_tilde v_tilde_r>`` in m⁻² s⁻¹."""
    return turbulent_particle_flux(density_m3, radial_velocity_m_s, direction="radial")


def turbulent_poloidal_particle_flux(density_m3, poloidal_velocity_m_s) -> float:
    """Return ``Gamma_theta=<n_tilde v_tilde_theta>`` in m⁻² s⁻¹."""
    return turbulent_particle_flux(density_m3, poloidal_velocity_m_s, direction="poloidal")
