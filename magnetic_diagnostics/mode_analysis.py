"""Mathematical coherent-structure analysis; no automatic physical mode labeling."""
from __future__ import annotations
import numpy as np

def component_energy(singular_values):
    """Return fractional squared-singular-value energy."""
    s = np.asarray(singular_values, dtype=float)
    if s.ndim != 1 or s.size == 0 or not np.all(np.isfinite(s)) or np.any(s < 0):
        raise ValueError("singular_values must be a finite non-negative 1D array")
    total = np.sum(s**2)
    if total <= 0:
        raise ValueError("singular_values must contain non-zero energy")
    return s**2 / total

def extract_spatial_structure(u, component: int = 0):
    """Return one SVD left-singular-vector spatial/channel structure."""
    arr = np.asarray(u, dtype=float)
    if arr.ndim != 2 or component < 0 or component >= arr.shape[1]:
        raise ValueError("u must be 2D and component must index an available SVD component")
    return arr[:, component].copy()

def channel_phase(data, frequency: float, sampling_frequency: float):
    """Estimate channel phase at a requested frequency using complex FFT bins.

    This is a signal-processing diagnostic, not an automatic MHD mode identifier.
    """
    from plasma_core.signal_processing import compute_fft
    f, spectrum = compute_fft(data, sampling_frequency)
    idx = int(np.argmin(np.abs(f - frequency)))
    return f[idx], np.angle(spectrum[..., idx])
