"""SVD decomposition using the repository-wide channels x time convention."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from core.data_model import MultichannelTimeSeries
from core.signal_processing.validation import as_signal_array

@dataclass(frozen=True)
class SVDResult:
    """SVD result for X with shape (channels, time)."""
    u: np.ndarray
    singular_values: np.ndarray
    vt: np.ndarray
    centered: bool
    scaled: bool
    matrix_orientation: str = "channels_by_time"

    @property
    def temporal_components(self) -> np.ndarray:
        """Return singular-value-weighted temporal coefficients Sigma V^T."""
        return self.singular_values[:, None] * self.vt

    @property
    def explained_energy(self) -> np.ndarray:
        """Fraction of squared-singular-value energy per component."""
        energy = self.singular_values ** 2
        return energy / np.sum(energy)

    @property
    def cumulative_energy(self) -> np.ndarray:
        return np.cumsum(self.explained_energy)

    def reconstruct(self, n_components: int | None = None) -> np.ndarray:
        """Reconstruct the centered/scaled analysis matrix."""
        k = self.singular_values.size if n_components is None else int(n_components)
        if k < 1 or k > self.singular_values.size:
            raise ValueError("n_components must be between 1 and the number of components")
        return (self.u[:, :k] * self.singular_values[:k]) @ self.vt[:k, :]


def compute_svd(data: MultichannelTimeSeries | np.ndarray, *, center: bool = True, scale: bool = False) -> SVDResult:
    """Compute SVD of a channels-by-time magnetic data matrix.

    Centering removes each channel mean. Scaling is optional and disabled by
    default because channel amplitude contains information for spatial analysis.
    """
    array = data.data if isinstance(data, MultichannelTimeSeries) else as_signal_array(data)
    if array.ndim != 2:
        raise ValueError("SVD requires a two-dimensional channels-by-time array")
    matrix = np.array(array, dtype=float, copy=True)
    if not np.all(np.isfinite(matrix)):
        raise ValueError("SVD input must contain only finite values")
    if center:
        matrix -= np.mean(matrix, axis=1, keepdims=True)
    if scale:
        std = np.std(matrix, axis=1, keepdims=True)
        if np.any(std <= 0) or not np.all(np.isfinite(std)):
            raise ValueError("cannot scale a zero-variance channel")
        matrix /= std
    u, s, vt = np.linalg.svd(matrix, full_matrices=False)
    return SVDResult(u=u, singular_values=s, vt=vt, centered=center, scaled=scale)
