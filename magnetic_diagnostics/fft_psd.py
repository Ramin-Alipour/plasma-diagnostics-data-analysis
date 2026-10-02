"""Magnetic-specific frequency-domain analysis built on the common core."""
from __future__ import annotations
import numpy as np
from core.data_model import MultichannelTimeSeries
from core.signal_processing import compute_psd

def channel_psd(data: MultichannelTimeSeries | np.ndarray, sampling_frequency: float | None = None, **kwargs):
    """Compute PSD for synchronized magnetic channels without changing orientation."""
    if isinstance(data, MultichannelTimeSeries):
        fs = data.sampling_frequency if sampling_frequency is None else sampling_frequency
        if fs is None:
            raise ValueError("sampling_frequency is required when it is not stored in the data model")
        return compute_psd(data.data, fs, **kwargs)
    if sampling_frequency is None:
        raise ValueError("sampling_frequency is required for array input")
    return compute_psd(data, sampling_frequency, **kwargs)

def dominant_frequency(frequencies: np.ndarray, psd: np.ndarray) -> np.ndarray:
    """Return the frequency of maximum PSD for each channel."""
    f = np.asarray(frequencies, dtype=float); p = np.asarray(psd, dtype=float)
    if f.ndim != 1 or p.ndim not in (1, 2) or p.shape[-1] != f.size:
        raise ValueError("frequencies must be 1D and PSD must be 1D or channels x frequency")
    if not np.all(np.isfinite(f)) or not np.all(np.isfinite(p)):
        raise ValueError("frequencies and PSD must be finite")
    return f[np.argmax(p, axis=-1)]
