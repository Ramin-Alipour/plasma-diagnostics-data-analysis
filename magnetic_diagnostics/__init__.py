"""Magnetic-diagnostic analysis workflows."""
from .fft_psd import channel_psd, dominant_frequency
from .wavelet import compute_cwt
from .svd import SVDResult, compute_svd
from .mode_analysis import channel_phase, component_energy, extract_spatial_structure
__all__ = ["channel_phase", "channel_psd", "component_energy", "compute_cwt", "compute_svd", "dominant_frequency", "extract_spatial_structure", "SVDResult"]
