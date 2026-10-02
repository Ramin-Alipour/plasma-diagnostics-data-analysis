"""Pixel-to-wavelength calibration utilities."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class WavelengthCalibrationResult:
    """Polynomial wavelength calibration and reference-line residuals."""
    coefficients: np.ndarray
    degree: int
    reference_pixels: np.ndarray
    reference_wavelengths: np.ndarray
    fitted_wavelengths: np.ndarray
    residuals: np.ndarray

    def calibrate(self, pixels) -> np.ndarray:
        """Convert detector pixel coordinates to wavelength in meters."""
        return np.polyval(self.coefficients, np.asarray(pixels, dtype=float))

    @property
    def rms_residual(self) -> float:
        """Root-mean-square calibration residual in wavelength units."""
        return float(np.sqrt(np.mean(self.residuals ** 2)))


def calibrate_wavelength(pixels, wavelengths, *, degree: int = 1) -> WavelengthCalibrationResult:
    """Fit a polynomial pixel-to-wavelength calibration.

    Parameters
    ----------
    pixels, wavelengths:
        Reference pixel positions and known wavelengths in the same length unit.
    degree:
        Polynomial degree. Degree 1 is the default for the initial workflow.
    """
    p = np.asarray(pixels, dtype=float)
    w = np.asarray(wavelengths, dtype=float)
    if p.ndim != 1 or w.ndim != 1 or p.size != w.size or p.size == 0:
        raise ValueError("pixels and wavelengths must be non-empty one-dimensional arrays of equal length")
    if not np.all(np.isfinite(p)) or not np.all(np.isfinite(w)):
        raise ValueError("reference pixels and wavelengths must be finite")
    if not isinstance(degree, (int, np.integer)) or degree < 1:
        raise ValueError("degree must be a positive integer")
    if p.size < degree + 1:
        raise ValueError("at least degree + 1 reference lines are required")
    if np.unique(p).size != p.size:
        raise ValueError("reference pixels must be unique")
    coefficients = np.polyfit(p, w, degree)
    fitted = np.polyval(coefficients, p)
    return WavelengthCalibrationResult(
        coefficients=np.asarray(coefficients, dtype=float),
        degree=int(degree),
        reference_pixels=p.copy(),
        reference_wavelengths=w.copy(),
        fitted_wavelengths=fitted,
        residuals=w - fitted,
    )
