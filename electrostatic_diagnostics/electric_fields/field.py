"""Electric-field calculation from a one-dimensional electrostatic potential."""
from __future__ import annotations
import numpy as np


def electric_field_from_potential(position_m, potential_V) -> np.ndarray:
    """Compute ``E = -d(phi)/dr`` using a numerical spatial gradient.

    Parameters
    ----------
    position_m:
        Monotonically increasing radial/spatial coordinate in metres.
    potential_V:
        Electrostatic potential ``phi`` in volts.

    Returns
    -------
    numpy.ndarray
        Electric field in V/m (equivalent to N/C).
    """
    r = np.asarray(position_m, dtype=float)
    phi = np.asarray(potential_V, dtype=float)
    if r.ndim != 1 or phi.ndim != 1 or r.size != phi.size:
        raise ValueError("position_m and potential_V must be one-dimensional arrays of equal length")
    if r.size < 2 or np.any(~np.isfinite(r)) or np.any(~np.isfinite(phi)):
        raise ValueError("position and potential must contain finite data and at least two points")
    if np.any(np.diff(r) <= 0):
        raise ValueError("position_m must be strictly increasing")
    return -np.gradient(phi, r)
