"""Analysis functions for synthetic and generic Langmuir I-V data."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.optimize import curve_fit

from .synthetic import langmuir_iv_model


@dataclass(frozen=True)
class LangmuirFitResult:
    """Result of fitting the repository's explicit synthetic I-V model."""

    ion_saturation_current: float
    electron_saturation_current: float
    plasma_potential: float
    electron_temperature_eV: float
    parameter_uncertainties: dict[str, float]
    fitted_current: np.ndarray
    residuals: np.ndarray
    covariance: np.ndarray


def estimate_floating_potential(voltage, current) -> float:
    """Estimate floating potential from a zero crossing of net current.

    Linear interpolation is used between the two samples bracketing the
    selected zero crossing. If multiple crossings exist, the crossing closest
    to the center of the voltage range is used.
    """
    voltage = np.asarray(voltage, dtype=float)
    current = np.asarray(current, dtype=float)
    if voltage.ndim != 1 or current.ndim != 1 or voltage.size != current.size:
        raise ValueError("voltage and current must be one-dimensional arrays of equal length")
    if voltage.size < 2 or np.any(~np.isfinite(voltage)) or np.any(~np.isfinite(current)):
        raise ValueError("voltage and current must contain finite data and at least two samples")
    if np.any(np.diff(voltage) <= 0):
        raise ValueError("voltage must be strictly increasing")

    exact = np.flatnonzero(current == 0.0)
    if exact.size:
        center = 0.5 * (voltage[0] + voltage[-1])
        return float(voltage[exact[np.argmin(np.abs(voltage[exact] - center))]])

    crossings = np.flatnonzero(current[:-1] * current[1:] < 0.0)
    if crossings.size == 0:
        raise ValueError("no current zero crossing found in the supplied voltage range")
    center = 0.5 * (voltage[0] + voltage[-1])
    candidates = []
    for i in crossings:
        v0, v1 = voltage[i], voltage[i + 1]
        i0, i1 = current[i], current[i + 1]
        vf = v0 - i0 * (v1 - v0) / (i1 - i0)
        candidates.append(vf)
    return float(candidates[int(np.argmin(np.abs(np.asarray(candidates) - center)))])


def fit_langmuir_iv(voltage, current) -> LangmuirFitResult:
    """Fit the explicit synthetic Langmuir model and recover ``Te`` and ``Vp``.

    This is intentionally a model-based validation workflow. It should not be
    interpreted as a universal Langmuir-probe reduction method for arbitrary
    experimental I-V characteristics.
    """
    voltage = np.asarray(voltage, dtype=float)
    current = np.asarray(current, dtype=float)
    if voltage.ndim != 1 or current.ndim != 1 or voltage.size != current.size:
        raise ValueError("voltage and current must be one-dimensional arrays of equal length")
    if voltage.size < 10 or np.any(~np.isfinite(voltage)) or np.any(~np.isfinite(current)):
        raise ValueError("voltage and current must contain finite data")
    if np.any(np.diff(voltage) <= 0):
        raise ValueError("voltage must be strictly increasing")

    n_edge = max(3, voltage.size // 10)
    ion_guess = max(1e-12, -float(np.median(current[:n_edge])))
    electron_guess = max(1e-12, float(np.max(current) + ion_guess))
    derivative = np.gradient(current, voltage)
    vp_guess = float(voltage[np.argmax(derivative)])
    te_guess = max((voltage[-1] - voltage[0]) / 10.0, 0.5)

    lower = [0.0, 0.0, voltage[0], 1e-6]
    upper = [np.inf, np.inf, voltage[-1], max(voltage[-1] - voltage[0], 1.0) * 2.0]
    popt, pcov = curve_fit(
        langmuir_iv_model,
        voltage,
        current,
        p0=[ion_guess, electron_guess, vp_guess, te_guess],
        bounds=(lower, upper),
        maxfev=20000,
    )
    fitted = langmuir_iv_model(voltage, *popt)
    names = ["ion_saturation_current", "electron_saturation_current", "plasma_potential", "electron_temperature_eV"]
    uncertainties = {name: float(np.sqrt(max(pcov[i, i], 0.0))) for i, name in enumerate(names)}
    return LangmuirFitResult(
        ion_saturation_current=float(popt[0]),
        electron_saturation_current=float(popt[1]),
        plasma_potential=float(popt[2]),
        electron_temperature_eV=float(popt[3]),
        parameter_uncertainties=uncertainties,
        fitted_current=fitted,
        residuals=current - fitted,
        covariance=pcov,
    )
