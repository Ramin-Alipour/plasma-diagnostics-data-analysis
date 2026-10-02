"""Ion-temperature estimation from Gaussian Doppler broadening."""
from __future__ import annotations
import numpy as np
from scipy.constants import atomic_mass, c, e, k


def _validate_positive(name, value):
    if not np.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite")


def doppler_sigma_from_temperature(line_center, temperature_eV, atomic_mass_amu):
    """Return Gaussian Doppler sigma in the wavelength unit of ``line_center``.

    The model assumes a Maxwellian thermal velocity distribution and a Gaussian
    Doppler profile. The returned sigma is the standard deviation of the
    wavelength Gaussian, not the conventional 1/e half-width.
    """
    _validate_positive("line_center", line_center)
    _validate_positive("temperature_eV", temperature_eV)
    _validate_positive("atomic_mass_amu", atomic_mass_amu)
    mass = atomic_mass_amu * atomic_mass
    temperature_J = temperature_eV * e
    return float(line_center * np.sqrt(k * (temperature_J / k) / (mass * c**2)))


def estimate_doppler_temperature(line_center, observed_sigma, atomic_mass_amu, *, instrumental_sigma=0.0):
    """Estimate ion temperature from Gaussian Doppler broadening.

    Parameters are in one consistent wavelength unit except ``atomic_mass_amu``.
    For Gaussian widths, independent Gaussian instrumental broadening is removed
    in quadrature. The returned temperature is in eV.
    """
    _validate_positive("line_center", line_center)
    _validate_positive("observed_sigma", observed_sigma)
    _validate_positive("atomic_mass_amu", atomic_mass_amu)
    if not np.isfinite(instrumental_sigma) or instrumental_sigma < 0:
        raise ValueError("instrumental_sigma must be finite and non-negative")
    if instrumental_sigma > observed_sigma:
        raise ValueError("instrumental_sigma cannot exceed observed_sigma")
    sigma_doppler = float(np.sqrt(observed_sigma**2 - instrumental_sigma**2))
    mass = atomic_mass_amu * atomic_mass
    temperature_J = mass * c**2 * (sigma_doppler / line_center)**2
    temperature_eV = temperature_J / e
    temperature_K = temperature_J / k
    return {
        "temperature_eV": float(temperature_eV),
        "temperature_K": float(temperature_K),
        "doppler_sigma": sigma_doppler,
        "observed_sigma": float(observed_sigma),
        "instrumental_sigma": float(instrumental_sigma),
    }
