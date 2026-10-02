"""Controlled synthetic spectral-line generation for scientific validation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.constants import atomic_mass, c, e, k

@dataclass(frozen=True)
class SyntheticSpectrum:
    """Synthetic spectrum with known physical generation parameters."""
    pixels: np.ndarray
    wavelength: np.ndarray
    intensity: np.ndarray
    true_wavelength: np.ndarray
    line_center: float
    temperature_eV: float
    atomic_mass_amu: float
    doppler_sigma: float
    instrumental_sigma: float
    baseline: np.ndarray
    random_seed: int


def _doppler_sigma(line_center, temperature_eV, mass_amu):
    mass = mass_amu * atomic_mass
    temperature_J = temperature_eV * e
    return line_center * np.sqrt(temperature_J / (mass * c**2))


def generate_synthetic_spectrum(*, n_pixels=2048, pixel_start=0.0, pixel_end=2047.0,
                                calibration_coefficients=(500e-9, 0.005e-9),
                                line_center=505e-9, amplitude=1.0,
                                temperature_eV=20.0, atomic_mass_amu=40.0,
                                instrumental_sigma=0.0, baseline_coefficients=(0.05, 0.0),
                                noise_std=0.01, seed=42):
    """Generate one Gaussian spectral line with known Doppler temperature.

    ``calibration_coefficients`` are polynomial coefficients in ascending order,
    mapping pixel to wavelength. Baseline coefficients are in the normalized
    pixel coordinate [-1, 1].
    """
    if n_pixels < 16: raise ValueError("n_pixels must be at least 16")
    if noise_std < 0 or not np.isfinite(noise_std): raise ValueError("noise_std must be finite and non-negative")
    if temperature_eV <= 0 or atomic_mass_amu <= 0: raise ValueError("temperature_eV and atomic_mass_amu must be positive")
    pixels = np.linspace(pixel_start, pixel_end, int(n_pixels))
    coeff = np.asarray(calibration_coefficients, dtype=float)
    if coeff.ndim != 1 or coeff.size < 2: raise ValueError("calibration_coefficients must contain at least two terms")
    wavelength = sum(c_i * pixels**i for i, c_i in enumerate(coeff))
    true_wavelength = wavelength.copy()
    sigma_d = _doppler_sigma(line_center, temperature_eV, atomic_mass_amu)
    if instrumental_sigma < 0: raise ValueError("instrumental_sigma must be non-negative")
    sigma_obs = np.sqrt(sigma_d**2 + instrumental_sigma**2)
    xnorm = 2.0 * (pixels - pixels.min()) / (pixels.max() - pixels.min()) - 1.0
    baseline = np.zeros_like(xnorm)
    for power, coefficient in enumerate(baseline_coefficients): baseline += coefficient * xnorm**power
    rng = np.random.default_rng(seed)
    line = amplitude * np.exp(-0.5 * ((wavelength - line_center) / sigma_obs)**2)
    intensity = line + baseline + rng.normal(0.0, noise_std, size=n_pixels)
    return SyntheticSpectrum(pixels, wavelength, intensity, true_wavelength, line_center,
                             temperature_eV, atomic_mass_amu, sigma_d, float(instrumental_sigma),
                             baseline, int(seed))
