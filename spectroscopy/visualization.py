"""Scientific visualization for spectroscopy workflows."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_spectrum(wavelengths, intensity, *, ax=None, label="Synthetic spectrum"):
    if ax is None: _, ax = plt.subplots()
    ax.plot(np.asarray(wavelengths) * 1e9, intensity, label=label)
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Intensity (a.u.)"); ax.legend()
    return ax


def plot_calibration_residual(result, *, ax=None):
    if ax is None: _, ax = plt.subplots()
    ax.plot(result.reference_pixels, result.residuals * 1e12, "o")
    ax.axhline(0.0, linewidth=1)
    ax.set_xlabel("Reference pixel"); ax.set_ylabel("Calibration residual (pm)")
    ax.set_title("Wavelength calibration residual")
    return ax


def plot_line_identification(wavelengths, intensity, matches, *, ax=None):
    if ax is None: _, ax = plt.subplots()
    x = np.asarray(wavelengths) * 1e9
    ax.plot(x, intensity, label="Synthetic spectrum")
    for match in matches:
        ax.axvline(match["detected_wavelength"] * 1e9, linestyle="--", label=match["reference"].species)
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Intensity (a.u.)"); ax.set_title("Candidate spectral-line identification")
    ax.legend()
    return ax


def plot_gaussian_fit(wavelengths, intensity, fit_result, *, ax=None):
    if ax is None: _, ax = plt.subplots()
    x = np.asarray(wavelengths) * 1e9
    ax.plot(x, intensity, label="Spectrum")
    ax.plot(x, fit_result.fitted, label="Gaussian fit")
    ax.set_xlabel("Wavelength (nm)"); ax.set_ylabel("Intensity (a.u.)"); ax.set_title("Gaussian spectral-line fit"); ax.legend()
    return ax


def plot_temperature_validation(known_temperature, recovered_temperature, *, ax=None):
    if ax is None: _, ax = plt.subplots()
    ax.bar(["Known", "Recovered"], [known_temperature, recovered_temperature])
    ax.set_ylabel("Ion temperature (eV)"); ax.set_title("Synthetic Doppler-temperature validation")
    return ax
