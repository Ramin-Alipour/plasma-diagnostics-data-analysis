"""Scientific visualization for electrostatic diagnostics."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_langmuir_iv(voltage, current, *, fitted_current=None, ax=None):
    if ax is None:
        _, ax = plt.subplots()
    ax.plot(np.asarray(voltage), np.asarray(current), label="Synthetic I-V")
    if fitted_current is not None:
        ax.plot(np.asarray(voltage), np.asarray(fitted_current), label="Model fit")
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Probe voltage (V)")
    ax.set_ylabel("Probe current (A)")
    ax.set_title("Langmuir I-V characteristic")
    ax.legend()
    return ax


def plot_potential_and_field(position_m, potential_V, electric_field_V_m, *, ax=None):
    if ax is None:
        _, ax = plt.subplots()
    ax.plot(np.asarray(position_m) * 1e3, np.asarray(potential_V), label="Potential")
    ax.set_xlabel("Position (mm)")
    ax.set_ylabel("Potential (V)")
    ax.set_title("Synthetic electrostatic potential profile")
    ax.legend()
    return ax


def plot_mach_numbers(mach_result, *, ax=None):
    if ax is None:
        _, ax = plt.subplots()
    labels = ["Parallel", "Perpendicular"]
    values = [mach_result["parallel_mach"], mach_result["perpendicular_mach"]]
    ax.bar(labels, values)
    ax.set_ylabel("Mach number")
    ax.set_title("Synthetic compound-probe flow analysis")
    return ax
