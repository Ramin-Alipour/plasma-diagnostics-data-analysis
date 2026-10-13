"""Generate the structured synthetic rotating-mode figure used in the paper.

Run from the repository root with:
    python paper/svd_rotating_mode_example.py

The data are synthetic and are not intended to represent an IR-T1 discharge.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from magnetic_diagnostics.svd import compute_svd

N_CHANNELS = 12
N_SAMPLES = 1024
FS_HZ = 1024.0
F_HZ = 8.0
MODE_NUMBER = 2

theta = 2.0 * np.pi * np.arange(N_CHANNELS) / N_CHANNELS
time_s = np.arange(N_SAMPLES) / FS_HZ
signals = np.cos(MODE_NUMBER * theta[:, None] - 2.0 * np.pi * F_HZ * time_s[None, :])
result = compute_svd(signals, center=True, scale=False)
rank_two = result.reconstruct(n_components=2)
spatial_projection = (2.0 / N_CHANNELS) * (
    np.exp(-1j * MODE_NUMBER * theta)[:, None] * signals
).sum(axis=0)

ratio = result.singular_values[0] / result.singular_values[1]
assert np.isclose(ratio, 1.0, rtol=1e-10)
assert np.allclose(rank_two, signals, atol=1e-10)
assert np.allclose(np.abs(spatial_projection), 1.0, atol=1e-10)

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), constrained_layout=True)
im = axes[0].imshow(signals, aspect="auto", origin="lower",
                    extent=[time_s[0], time_s[-1], 0, N_CHANNELS],
                    cmap="RdBu_r", vmin=-1, vmax=1)
axes[0].set_title("Synthetic rotating mode")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Channel index")
fig.colorbar(im, ax=axes[0], label="Signal (a.u.)")
axes[1].bar([1, 2], result.singular_values[:2] / result.singular_values[0])
axes[1].set_xticks([1, 2], ["1", "2"])
axes[1].set_ylim(0, 1.15)
axes[1].set_xlabel("SVD component")
axes[1].set_ylabel("Singular value / first")
axes[1].set_title(f"Two quadratures (m = {MODE_NUMBER})")
axes[2].plot(theta, signals[:, 0], "o-", label="Constructed")
axes[2].plot(theta, rank_two[:, 0], "x--", label="Rank-2 reconstruction")
axes[2].set_xlabel("Sensor angle (rad)")
axes[2].set_ylabel("Signal at t = 0 (a.u.)")
axes[2].set_title("Spatial profile recovered")
axes[2].legend(frameon=False)
out = Path("figures/SVD_rotating_mode_example.svg")
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, format="svg")
print(f"Saved {out}; leading singular-value ratio = {ratio:.12f}")
