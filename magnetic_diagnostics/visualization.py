"""Scientific plotting helpers for magnetic-diagnostic workflows."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_multichannel_signals(time, data, *, channel_names=None, max_channels=12, title="Synthetic magnetic signals"):
    """Plot synchronized channels against time in seconds."""
    t = np.asarray(time); x = np.asarray(data)
    fig, ax = plt.subplots(figsize=(10, 6))
    n = min(x.shape[0], max_channels)
    for i in range(n):
        label = channel_names[i] if channel_names is not None else f"channel_{i}"
        ax.plot(t, x[i], label=label)
    ax.set_xlabel("Time [s]"); ax.set_ylabel("Signal [a.u.]"); ax.set_title(title); ax.legend(ncol=2)
    fig.tight_layout(); return fig, ax


def plot_psd(frequencies, psd, *, channel_names=None, title="Magnetic-channel PSD"):
    """Plot PSD for one or multiple channels."""
    f = np.asarray(frequencies); p = np.asarray(psd)
    fig, ax = plt.subplots(figsize=(10, 5))
    if p.ndim == 1: p = p[None, :]
    for i, row in enumerate(p):
        label = channel_names[i] if channel_names is not None else f"channel_{i}"
        ax.semilogy(f, row, label=label)
    ax.set_xlabel("Frequency [Hz]"); ax.set_ylabel("PSD [signal²/Hz]"); ax.set_title(title); ax.legend(ncol=2)
    fig.tight_layout(); return fig, ax


def plot_wavelet_scalogram(time, frequencies, coefficients, *, channel=0, title=None):
    """Plot wavelet power versus time and frequency for one channel."""
    c = np.asarray(coefficients)
    if c.ndim == 3: c = c[channel]
    power = np.abs(c) ** 2
    fig, ax = plt.subplots(figsize=(10, 5))
    mesh = ax.pcolormesh(time, frequencies, power, shading="auto")
    ax.set_yscale("log"); ax.set_xlabel("Time [s]"); ax.set_ylabel("Frequency [Hz]")
    ax.set_title(title or f"Wavelet scalogram — channel {channel}")
    fig.colorbar(mesh, ax=ax, label="Wavelet power [a.u.]" ); fig.tight_layout(); return fig, ax


def plot_singular_values(singular_values, *, title="Singular-value spectrum"):
    s = np.asarray(singular_values)
    fig, ax = plt.subplots(figsize=(8, 5)); ax.semilogy(np.arange(1, s.size + 1), s, "o-")
    ax.set_xlabel("Component"); ax.set_ylabel("Singular value [a.u.]"); ax.set_title(title); fig.tight_layout(); return fig, ax


def plot_temporal_components(time, temporal_components, *, n_components=3, title="Principal temporal components"):
    c = np.asarray(temporal_components)
    fig, ax = plt.subplots(figsize=(10, 6))
    for i in range(min(n_components, c.shape[0])): ax.plot(time, c[i], label=f"component {i + 1}")
    ax.set_xlabel("Time [s]"); ax.set_ylabel("Temporal coefficient [a.u.]"); ax.set_title(title); ax.legend(); fig.tight_layout(); return fig, ax


def plot_spatial_structures(channel_names, u, *, n_components=3, title="SVD channel structures"):
    arr = np.asarray(u)
    x = np.arange(arr.shape[0]); fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(min(n_components, arr.shape[1])): ax.plot(x, arr[:, i], "o-", label=f"component {i + 1}")
    ax.set_xticks(x); ax.set_xticklabels(channel_names, rotation=45, ha="right"); ax.set_xlabel("Channel"); ax.set_ylabel("Spatial coefficient [a.u.]"); ax.set_title(title); ax.legend(); fig.tight_layout(); return fig, ax


def plot_svd_energy(singular_values, *, title="SVD explained energy"):
    s = np.asarray(singular_values, dtype=float); frac = s**2 / np.sum(s**2); cumulative = np.cumsum(frac)
    fig, ax = plt.subplots(figsize=(8, 5)); x = np.arange(1, s.size + 1)
    ax.plot(x, frac, "o-", label="Component")
    ax.plot(x, cumulative, "s--", label="Cumulative")
    ax.set_xlabel("Component"); ax.set_ylabel("Energy fraction"); ax.set_ylim(0, 1.05); ax.set_title(title); ax.legend(); fig.tight_layout(); return fig, ax
