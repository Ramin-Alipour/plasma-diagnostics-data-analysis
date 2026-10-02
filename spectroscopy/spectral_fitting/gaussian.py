"""Single-Gaussian spectral-line fitting."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit

@dataclass(frozen=True)
class GaussianFitResult:
    """Parameters and diagnostics for a fitted Gaussian peak."""
    amplitude: float
    center: float
    sigma: float
    amplitude_uncertainty: float
    center_uncertainty: float
    sigma_uncertainty: float
    covariance: np.ndarray
    fitted: np.ndarray
    residuals: np.ndarray

    @property
    def fwhm(self) -> float:
        return compute_fwhm(self.sigma)

    @property
    def reduced_residual_rms(self) -> float:
        return float(np.sqrt(np.mean(self.residuals ** 2)))


def _gaussian(x, amplitude, center, sigma):
    return amplitude * np.exp(-0.5 * ((x - center) / sigma) ** 2)


def compute_fwhm(sigma: float) -> float:
    """Return Gaussian FWHM from standard deviation ``sigma``."""
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be positive and finite")
    return float(2.0 * np.sqrt(2.0 * np.log(2.0)) * sigma)


def fit_gaussian_peak(x, y, *, initial_guess=None, bounds=None) -> GaussianFitResult:
    """Fit a single Gaussian peak without a built-in baseline term.

    Internally the wavelength coordinate is centered and scaled before fitting
    to avoid numerical conditioning problems when wavelengths are expressed in
    SI units such as meters.
    """
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 3:
        raise ValueError("x and y must be one-dimensional arrays of equal length")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("x and y must be finite")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x must be strictly increasing")
    x_ref = float(np.mean(x))
    x_scale = float(np.ptp(x))
    if x_scale <= 0:
        raise ValueError("x must span a non-zero interval")
    if initial_guess is None:
        amplitude = float(np.max(y))
        center = float(x[np.argmax(y)])
        width = max(x_scale / 10.0, np.finfo(float).eps)
        initial_guess = (amplitude, center, width)
    amp0, center0, sigma0 = map(float, initial_guess)
    if sigma0 <= 0 or not np.isfinite(sigma0):
        raise ValueError("initial sigma must be positive and finite")
    z = (x - x_ref) / x_scale
    p0 = (amp0, (center0 - x_ref) / x_scale, sigma0 / x_scale)

    def gaussian_scaled(zcoord, amplitude, center_scaled, sigma_scaled):
        return amplitude * np.exp(-0.5 * ((zcoord - center_scaled) / sigma_scaled) ** 2)

    if bounds is None:
        lower = (-np.inf, (x[0] - x_ref) / x_scale, np.finfo(float).eps / x_scale)
        upper = (np.inf, (x[-1] - x_ref) / x_scale, np.inf)
    else:
        lower_raw, upper_raw = bounds
        lower = (lower_raw[0], (lower_raw[1] - x_ref) / x_scale, lower_raw[2] / x_scale)
        upper = (upper_raw[0], (upper_raw[1] - x_ref) / x_scale, upper_raw[2] / x_scale)

    popt, pcov = curve_fit(gaussian_scaled, z, y, p0=p0, bounds=(lower, upper), maxfev=20000)
    amplitude, center_scaled, sigma_scaled = popt
    center = x_ref + center_scaled * x_scale
    sigma = sigma_scaled * x_scale
    fitted = gaussian_scaled(z, amplitude, center_scaled, sigma_scaled)
    residuals = y - fitted
    cov_transform = np.diag([1.0, x_scale, x_scale])
    covariance = cov_transform @ pcov @ cov_transform
    uncertainties = np.sqrt(np.clip(np.diag(covariance), 0.0, np.inf))
    return GaussianFitResult(
        amplitude=float(amplitude), center=float(center), sigma=float(sigma),
        amplitude_uncertainty=float(uncertainties[0]), center_uncertainty=float(uncertainties[1]),
        sigma_uncertainty=float(uncertainties[2]), covariance=np.asarray(covariance, dtype=float),
        fitted=fitted, residuals=residuals,
    )
