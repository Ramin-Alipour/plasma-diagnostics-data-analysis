"""Temporal analysis for synthetic HXR signals."""
from __future__ import annotations
import numpy as np
from scipy.signal import periodogram, find_peaks

def _arr(x):
    a=np.asarray(x,dtype=float)
    if a.ndim!=1 or a.size<2 or np.any(~np.isfinite(a)): raise ValueError("signal must be a finite 1-D array")
    return a

def integrated_intensity(counts, time_s=None):
    c=_arr(counts)
    return float(np.mean(c)) if time_s is None else float(np.trapz(c,np.asarray(time_s,dtype=float)))

def high_energy_band_fraction(energy_keV, counts, threshold_keV):
    e=_arr(energy_keV); c=_arr(counts)
    if e.size!=c.size or threshold_keV<e.min() or threshold_keV>e.max(): raise ValueError("invalid energy/count inputs")
    total=np.sum(c)
    return float(np.sum(c[e>=threshold_keV])/total) if total>0 else 0.0

def burst_features(time_s, counts, *, prominence=None):
    t=_arr(time_s); c=_arr(counts)
    if t.size!=c.size: raise ValueError("time and counts must have same length")
    baseline=np.median(c); y=c-baseline
    p=prominence if prominence is not None else max(1.0,2*np.std(y))
    idx,_=find_peaks(y,prominence=p)
    return {"peak_indices":idx,"peak_times_s":t[idx],"peak_values":c[idx],"baseline":float(baseline)}

def power_spectrum(counts, sampling_frequency_hz):
    c=_arr(counts)
    if sampling_frequency_hz<=0: raise ValueError("sampling_frequency_hz must be positive")
    f,p=periodogram(c,fs=sampling_frequency_hz,scaling="density",detrend="linear")
    return f,p
