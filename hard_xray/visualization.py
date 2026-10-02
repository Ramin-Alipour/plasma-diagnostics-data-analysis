"""Scientific visualization helpers for HXR workflows."""
from __future__ import annotations
import matplotlib.pyplot as plt

def plot_hxr_time_series(time_s,counts,ax=None):
    if ax is None: _,ax=plt.subplots()
    ax.plot(time_s,counts); ax.set_xlabel("Time (s)"); ax.set_ylabel("HXR counts (a.u.)"); ax.set_title("Synthetic hard X-ray time series"); ax.grid(True,alpha=0.25); return ax

def plot_hxr_spectrum(energy_keV,counts,ax=None):
    if ax is None: _,ax=plt.subplots()
    ax.step(energy_keV,counts,where="mid"); ax.set_xlabel("Energy (keV)"); ax.set_ylabel("Counts"); ax.set_title("Synthetic HXR count spectrum"); ax.grid(True,alpha=0.25); return ax

def plot_power_spectrum(frequency_hz,power,ax=None):
    if ax is None: _,ax=plt.subplots()
    ax.semilogy(frequency_hz,power); ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("PSD (counts²/Hz)"); ax.set_title("HXR power spectral density"); ax.grid(True,alpha=0.25); return ax

def plot_hxr_mhd_correlation(lags_s,corr,ax=None):
    if ax is None: _,ax=plt.subplots()
    ax.plot(lags_s,corr); ax.axvline(0,ls="--"); ax.set_xlabel("Lag (s)"); ax.set_ylabel("Normalized cross-correlation"); ax.set_title("Synthetic HXR–MHD cross-correlation"); ax.grid(True,alpha=0.25); return ax
