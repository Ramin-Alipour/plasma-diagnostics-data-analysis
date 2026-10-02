"""Flow-velocity and Mach-number analysis for directional measurements."""
from __future__ import annotations
import numpy as np
from electrostatic_diagnostics.plasma_parameters.derived import ion_sound_speed_m_s


def estimate_flow_velocity(direction_cosines, directional_measurements_m_s):
    """Estimate a 3-D velocity vector by linear least squares.

    Each row of ``direction_cosines`` represents a unit measurement direction,
    and the corresponding measurement approximates its dot product with the
    flow velocity.
    """
    directions = np.asarray(direction_cosines, dtype=float)
    measurements = np.asarray(directional_measurements_m_s, dtype=float)
    if directions.ndim != 2 or directions.shape[1] != 3:
        raise ValueError("direction_cosines must have shape (n_measurements, 3)")
    if measurements.ndim != 1 or measurements.size != directions.shape[0]:
        raise ValueError("directional_measurements_m_s must match the number of directions")
    if directions.shape[0] < 3 or np.any(~np.isfinite(directions)) or np.any(~np.isfinite(measurements)):
        raise ValueError("at least three finite directional measurements are required")
    norms = np.linalg.norm(directions, axis=1)
    if np.any(norms <= 0):
        raise ValueError("direction vectors must be non-zero")
    normalized = directions / norms[:, None]
    velocity, residuals, rank, _ = np.linalg.lstsq(normalized, measurements, rcond=None)
    if rank < 3:
        raise ValueError("direction measurements do not span three independent components")
    return {
        "velocity_m_s": velocity,
        "residuals_m_s": normalized @ velocity - measurements,
        "rank": int(rank),
    }



def calculate_mach_numbers(velocity_m_s, *, electron_temperature_eV, ion_mass_amu, parallel_axis=0):
    """Calculate parallel/perpendicular Mach numbers from a velocity vector.

    The parallel direction is the selected coordinate axis. The sound speed
    uses the cold-ion ion-acoustic expression; finite ion-temperature and more
    detailed sheath models are outside this initial synthetic workflow.
    """
    velocity = np.asarray(velocity_m_s, dtype=float)
    if velocity.shape != (3,) or np.any(~np.isfinite(velocity)):
        raise ValueError("velocity_m_s must contain three finite components")
    if parallel_axis not in (0, 1, 2):
        raise ValueError("parallel_axis must be 0, 1, or 2")
    cs = ion_sound_speed_m_s(electron_temperature_eV, ion_mass_amu)
    v_parallel = float(velocity[parallel_axis])
    perpendicular_components = np.delete(velocity, parallel_axis)
    v_perpendicular = float(np.linalg.norm(perpendicular_components))
    return {
        "sound_speed_m_s": cs,
        "parallel_velocity_m_s": v_parallel,
        "perpendicular_velocity_m_s": v_perpendicular,
        "parallel_mach": v_parallel / cs,
        "perpendicular_mach": v_perpendicular / cs,
    }
