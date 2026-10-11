"""Descriptive analysis of measured spectral-line widths."""

from __future__ import annotations

import numpy as np
import pandas as pd


def summarize_line_width_measurements(
    data: pd.DataFrame,
    *,
    wavelength_column: str = "wavelength_nm",
    width_column: str = "measured_fwhm_nm",
) -> dict[str, int | float]:
    """Summarize measured line widths without inferring plasma temperature.

    The input is copied through numeric conversion and is never modified.
    Wavelength and FWHM values must be positive, finite, and present. Returned
    statistics describe only the supplied line-level measurements; they do not
    correct for instrumental broadening or establish a physical interpretation.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")
    if data.empty:
        raise ValueError("data must contain at least one line measurement")

    missing = {wavelength_column, width_column}.difference(data.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    try:
        wavelength = pd.to_numeric(data[wavelength_column], errors="raise").to_numpy(dtype=float)
        widths = pd.to_numeric(data[width_column], errors="raise").to_numpy(dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("wavelength and FWHM columns must contain numeric values") from exc

    if not np.isfinite(wavelength).all() or not np.isfinite(widths).all():
        raise ValueError("wavelength and FWHM values must be finite")
    if (wavelength <= 0).any():
        raise ValueError("wavelength values must be positive")
    if (widths <= 0).any():
        raise ValueError("FWHM values must be positive")

    n_lines = int(widths.size)
    return {
        "n_lines": n_lines,
        "wavelength_min_nm": float(np.min(wavelength)),
        "wavelength_max_nm": float(np.max(wavelength)),
        "fwhm_mean_nm": float(np.mean(widths)),
        "fwhm_median_nm": float(np.median(widths)),
        "fwhm_sample_sd_nm": float(np.std(widths, ddof=1)) if n_lines > 1 else 0.0,
        "fwhm_min_nm": float(np.min(widths)),
        "fwhm_max_nm": float(np.max(widths)),
    }
