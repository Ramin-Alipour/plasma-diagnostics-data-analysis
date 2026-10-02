"""Scientific visualizations for cross-diagnostic comparisons."""
from __future__ import annotations
import matplotlib.pyplot as plt


def plot_aligned_signals(a, b):
    fig, ax = plt.subplots()
    ax.plot(a.time, a.data, label=a.name or "A")
    ax.plot(b.time, b.data, label=b.name or "B")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Signal")
    ax.set_title("Aligned cross-diagnostic signals"); ax.legend(); fig.tight_layout()
    return fig, ax


def plot_cross_correlation(lags, correlation):
    fig, ax = plt.subplots()
    ax.plot(lags, correlation)
    ax.set_xlabel("Lag (s)"); ax.set_ylabel("Normalized cross-correlation")
    ax.set_title("Cross-correlation")
    fig.tight_layout(); return fig, ax


def plot_spectral_comparison(result):
    fig, ax = plt.subplots()
    ax.semilogy(result["frequency_hz"], result["psd_a"], label="A")
    ax.semilogy(result["frequency_hz"], result["psd_b"], label="B")
    ax.set_xlabel("Frequency (Hz)"); ax.set_ylabel("PSD")
    ax.set_title("Cross-diagnostic spectral comparison"); ax.legend(); fig.tight_layout()
    return fig, ax
