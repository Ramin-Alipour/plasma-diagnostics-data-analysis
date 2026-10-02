"""Synthetic hard X-ray time-series and count-spectrum generators."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class SyntheticHXRTimeSeries:
    time_s: np.ndarray
    counts: np.ndarray
    components: dict[str, np.ndarray]
    sampling_frequency_hz: float
    metadata: dict

@dataclass(frozen=True)
class SyntheticHXRCountSpectrum:
    energy_keV: np.ndarray
    expected_counts: np.ndarray
    counts: np.ndarray
    components: dict[str, np.ndarray]
    metadata: dict

def _validate_positive(name, value):
    if not np.isfinite(value) or value <= 0: raise ValueError(f"{name} must be positive")

def generate_hxr_time_series(*, sampling_frequency_hz=1_000_000.0, duration_s=0.01,
                              baseline=20.0, mean_amplitude=100.0, modulation_frequency_hz=44_000.0,
                              secondary_frequency_hz=70_000.0, modulation_depth=0.25,
                              burst_centers_s=(0.0035,0.0072), burst_width_s=0.00012,
                              noise_std=4.0, seed=42):
    _validate_positive("sampling_frequency_hz", sampling_frequency_hz); _validate_positive("duration_s", duration_s)
    if modulation_depth < 0 or modulation_depth > 1: raise ValueError("modulation_depth must be in [0, 1]")
    if noise_std < 0: raise ValueError("noise_std must be non-negative")
    n=int(round(sampling_frequency_hz*duration_s)); t=np.arange(n)/sampling_frequency_hz
    slow=mean_amplitude*(1+modulation_depth*np.sin(2*np.pi*modulation_frequency_hz*t))
    coherent=0.18*mean_amplitude*np.sin(2*np.pi*secondary_frequency_hz*t+0.35)
    burst=np.zeros_like(t)
    for c in burst_centers_s: burst += 0.65*mean_amplitude*np.exp(-0.5*((t-c)/burst_width_s)**2)
    expected=np.clip(baseline+slow+coherent+burst, 0, None)
    rng=np.random.default_rng(seed)
    counts=rng.poisson(expected).astype(float)
    # Optional detector/readout contribution represented separately; Gaussian noise is zero by default.
    if noise_std: counts += rng.normal(0, noise_std, n)
    return SyntheticHXRTimeSeries(t, counts, {"baseline":np.full(n,baseline),"modulated":slow,"coherent":coherent,"bursts":burst}, sampling_frequency_hz,
                                  {"data_type":"synthetic","diagnostic":"hard_xray","seed":seed})

def generate_hxr_spectrum(*, energy_min_keV=10.0, energy_max_keV=1000.0, bins=250,
                          background_level=4.0, low_energy_amplitude=140.0, low_energy_scale_keV=120.0,
                          tail_amplitude=35.0, tail_scale_keV=260.0, tail_threshold_keV=180.0, seed=42):
    if bins < 10 or energy_max_keV <= energy_min_keV: raise ValueError("invalid energy-bin configuration")
    if min(background_level, low_energy_amplitude, low_energy_scale_keV, tail_amplitude, tail_scale_keV, tail_threshold_keV) < 0:
        raise ValueError("spectrum parameters must be non-negative")
    edges=np.linspace(energy_min_keV,energy_max_keV,bins+1); e=0.5*(edges[:-1]+edges[1:])
    background=np.full_like(e,background_level)
    low=low_energy_amplitude*np.exp(-e/low_energy_scale_keV)
    tail=tail_amplitude*np.exp(-np.maximum(e-tail_threshold_keV,0)/tail_scale_keV)*(e>=tail_threshold_keV)
    expected=np.clip(background+low+tail,0,None)
    rng=np.random.default_rng(seed); counts=rng.poisson(expected)
    return SyntheticHXRCountSpectrum(e,expected,counts,{"background":background,"low_energy":low,"high_energy_tail":tail},
                                     {"data_type":"synthetic","diagnostic":"hard_xray","spectrum_type":"count_spectrum","noise_model":"poisson","seed":seed})
