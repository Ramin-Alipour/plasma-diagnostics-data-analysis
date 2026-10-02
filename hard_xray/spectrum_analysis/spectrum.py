"""Feature extraction from synthetic HXR count spectra."""
from __future__ import annotations
import numpy as np

def _inputs(e,c):
    e=np.asarray(e,dtype=float); c=np.asarray(c,dtype=float)
    if e.ndim!=1 or c.ndim!=1 or e.size!=c.size or e.size<2 or np.any(~np.isfinite(e)) or np.any(~np.isfinite(c)): raise ValueError("energy and counts must be finite 1-D arrays of equal length")
    if np.any(np.diff(e)<=0): raise ValueError("energy axis must be strictly increasing")
    if np.any(c<0): raise ValueError("counts must be non-negative")
    return e,c

def integrate_energy_band(energy_keV, counts, low_keV, high_keV):
    e,c=_inputs(energy_keV,counts)
    if not (low_keV<high_keV): raise ValueError("low_keV must be below high_keV")
    m=(e>=low_keV)&(e<high_keV)
    return int(np.sum(c[m]))

def hardness_ratio(energy_keV, counts, low_band, high_band):
    low=integrate_energy_band(energy_keV,counts,*low_band); high=integrate_energy_band(energy_keV,counts,*high_band)
    if low<=0: raise ValueError("low-energy band contains no counts")
    return float(high/low)

def spectral_tail_feature(energy_keV, counts, threshold_keV):
    e,c=_inputs(energy_keV,counts); m=e>=threshold_keV
    if not np.any(m): raise ValueError("threshold is above energy range")
    return {"threshold_keV":float(threshold_keV),"tail_counts":int(np.sum(c[m])),"tail_fraction":float(np.sum(c[m])/np.sum(c))}
