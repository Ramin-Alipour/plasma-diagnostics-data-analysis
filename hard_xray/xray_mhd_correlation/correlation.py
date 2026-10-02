"""Focused HXR–MHD temporal comparison utilities."""
from __future__ import annotations
import numpy as np
from scipy.signal import correlate, butter, sosfiltfilt

def _pair(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    if a.ndim!=1 or b.ndim!=1 or a.size!=b.size or a.size<3 or np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)): raise ValueError("signals must be finite equal-length 1-D arrays")
    return a-a.mean(),b-b.mean()

def correlation_coefficient(hxr,mhd):
    a,b=_pair(hxr,mhd)
    if np.std(a)==0 or np.std(b)==0: raise ValueError("signals must have non-zero variance")
    return float(np.corrcoef(a,b)[0,1])

def cross_correlation(hxr,mhd,sampling_frequency_hz):
    if sampling_frequency_hz<=0: raise ValueError("sampling_frequency_hz must be positive")
    a,b=_pair(hxr,mhd); corr=correlate(a,b,mode="full",method="auto"); corr/=np.sqrt(np.sum(a*a)*np.sum(b*b))
    lags=np.arange(-a.size+1,a.size)/sampling_frequency_hz
    return lags,corr

def band_power_ratio(signal,sampling_frequency_hz,band,reference_band):
    x=np.asarray(signal,dtype=float)
    if x.ndim!=1 or np.any(~np.isfinite(x)) or sampling_frequency_hz<=0: raise ValueError("invalid signal or sampling frequency")
    nyq=sampling_frequency_hz/2
    def bp(b):
        if not (0<b[0]<b[1]<nyq): raise ValueError("frequency band must be inside (0, Nyquist)")
        sos=butter(4,b,btype="bandpass",fs=sampling_frequency_hz,output="sos"); y=sosfiltfilt(sos,x); return float(np.mean(y*y))
    ref=bp(reference_band)
    if ref==0: raise ValueError("reference-band power is zero")
    return bp(band)/ref
