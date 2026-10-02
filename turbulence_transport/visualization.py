"""Scientific plotting helpers for turbulence and transport workflows."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_fluctuations(time_s, density_m3, potential_V):
    fig, ax1 = plt.subplots()
    ax1.plot(time_s, density_m3)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Density (m$^{-3}$)")
    ax2 = ax1.twinx()
    ax2.plot(time_s, potential_V)
    ax2.set_ylabel("Electrostatic potential (V)")
    fig.tight_layout()
    return fig, (ax1, ax2)


def plot_parameter_scan(parameter_values, response, parameter_name, response_name="Synthetic response"):
    fig, ax = plt.subplots()
    ax.plot(parameter_values, response, marker="o")
    ax.set_xlabel(parameter_name)
    ax.set_ylabel(response_name)
    ax.set_title("Synthetic parameter scan")
    fig.tight_layout()
    return fig, ax
