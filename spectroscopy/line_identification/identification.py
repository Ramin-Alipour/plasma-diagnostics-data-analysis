"""Candidate-based spectral-line identification."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from scipy.signal import find_peaks

@dataclass(frozen=True)
class SpectralLineReference:
    """Reference metadata for a spectral line."""
    species: str
    ionization_stage: str
    rest_wavelength: float
    optional_relative_intensity: float | None = None
    source: str = "synthetic/reference"


def identify_spectral_lines(wavelengths, intensity, reference_lines, *, tolerance, prominence=None, height=None):
    """Identify candidate reference lines near detected spectral peaks.

    This function performs candidate matching only; it is not an atomic database.
    ``wavelengths`` and ``tolerance`` use the same wavelength unit.
    """
    x = np.asarray(wavelengths, dtype=float)
    y = np.asarray(intensity, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size or x.size < 3:
        raise ValueError("wavelengths and intensity must be one-dimensional arrays of equal length")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
        raise ValueError("wavelengths and intensity must be finite")
    if tolerance <= 0 or not np.isfinite(tolerance):
        raise ValueError("tolerance must be positive and finite")
    if len(reference_lines) == 0:
        raise ValueError("reference_lines must not be empty")
    peaks, properties = find_peaks(y, prominence=prominence, height=height)
    detected = x[peaks]
    results = []
    for ref in reference_lines:
        distances = np.abs(detected - ref.rest_wavelength)
        if distances.size:
            j = int(np.argmin(distances))
            if distances[j] <= tolerance:
                results.append({
                    "reference": ref,
                    "detected_wavelength": float(detected[j]),
                    "peak_index": int(peaks[j]),
                    "difference": float(detected[j] - ref.rest_wavelength),
                    "intensity": float(y[peaks[j]]),
                })
    return results
