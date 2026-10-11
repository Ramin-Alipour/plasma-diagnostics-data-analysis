"""Reproducible comparison of Dataset A records with publication-derived Dataset B.

The comparisons are source-overlap checks, not claims of independent experimental
validation. Values in Dataset A are never modified.
"""
from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

from .dataset_archive import load_dataset_table


def _num_equal(left: Any, right: Any, atol: float = 1e-9) -> bool:
    try:
        a, b = float(left), float(right)
    except (TypeError, ValueError):
        return str(left) == str(right)
    return bool(np.isclose(a, b, rtol=0.0, atol=atol, equal_nan=True))


def _matches(a: pd.DataFrame, b: pd.DataFrame, keys: list[str],
             pairs: list[tuple[str, str]], atol: float = 1e-9) -> dict[str, Any]:
    joined = a.merge(b, left_on=keys, right_on=keys, how="inner", suffixes=("_a", "_b"))
    checks = []
    for _, row in joined.iterrows():
        for left_col, right_col in pairs:
            checks.append({
                "key": [row[k] for k in keys],
                "field_a": left_col,
                "field_b": right_col,
                "a": row[left_col],
                "b": row[right_col],
                "match": _num_equal(row[left_col], row[right_col], atol=atol),
            })
    return {
        "matched_rows": int(len(joined)),
        "field_checks": int(len(checks)),
        "equal_fields": int(sum(item["match"] for item in checks)),
        "differences": [item for item in checks if not item["match"]],
    }


def compare_dataset_a_b() -> dict[str, Any]:
    """Compare shared fields in A and B and return machine-readable results."""
    a1 = load_dataset_table("A", "laboratory_measurements/exp1_spectroscopy.csv")
    b1 = load_dataset_table("B", "publication_reconstruction/paper1_spectroscopy.csv")
    p01 = _matches(
        a1, b1, ["ion"],
        [("wavelength_nm", "wavelength_nm"),
         ("measured_fwhm_nm", "measured_fwhm_nm")],
    )

    a2h = load_dataset_table("A", "laboratory_measurements/exp2_hxr.csv")
    b2h = load_dataset_table("B", "publication_reconstruction/paper2_hxr.csv")
    p02_hxr = _matches(
        a2h, b2h, ["time_start_ms", "time_end_ms"],
        [("total_counts", "total_counts"), ("total_energy_keV", "total_energy_keV"),
         ("mean_energy_keV", "mean_energy_keV")],
        atol=1e-6,
    )

    a2m = load_dataset_table("A", "laboratory_measurements/exp2_modes.csv")
    b2m = load_dataset_table("B", "publication_reconstruction/paper2_modes.csv")
    b2m = b2m.rename(columns={"paper_id": "experiment_id"})
    mode_fields = [(f"m{i}_pct", f"m{i}_pct") for i in range(1, 7)]
    mode_fields.append(("edge_safety_factor", "edge_safety_factor"))
    p02_modes = _matches(
        a2m, b2m, ["experiment_id", "time_start_ms", "time_end_ms"], mode_fields
    )

    a3 = load_dataset_table("A", "laboratory_measurements/exp3_compound_probe.csv")
    b3 = load_dataset_table("B", "publication_reconstruction/paper3_compound_probe.csv")
    b3 = b3.rename(columns={"paper_id": "experiment_id"})
    p03 = _matches(a3, b3, ["experiment_id", "quantity"], [("value", "value")])

    a4 = load_dataset_table("A", "laboratory_measurements/exp4_pressure_transport.csv")
    b4 = load_dataset_table("B", "publication_reconstruction/paper4_pressure_transport.csv")
    p04_pairs = [
        ("avg_Er", "avg_Er_reported"), ("avg_Etheta", "avg_Etheta_reported"),
        ("radial_transport_no_bias", "radial_transport_no_bias"),
        ("radial_transport_plus200", "radial_transport_plus200"),
        ("radial_transport_minus200", "radial_transport_minus200"),
        ("poloidal_transport_no_bias", "poloidal_transport_no_bias"),
        ("poloidal_transport_plus200", "poloidal_transport_plus200"),
        ("poloidal_transport_minus200", "poloidal_transport_minus200"),
    ]
    p04 = _matches(a4, b4, ["pressure_Torr"], p04_pairs)

    a5 = load_dataset_table("A", "laboratory_measurements/exp5_limiter_transport.csv")
    b5 = load_dataset_table("B", "publication_reconstruction/paper5_limiter_transport.csv")
    p05_checks = []
    for _, row in a5.iterrows():
        effect = 100.0 * (float(row["biased_value"]) - float(row["baseline_value"])) / float(row["baseline_value"])
        match = b5[
            (b5["limiter_position_mm"] == row["limiter_position_mm"])
            & (b5["quantity"] == row["quantity"])
        ]
        if match.empty:
            p05_checks.append({"position_mm": row["limiter_position_mm"],
                               "quantity": row["quantity"], "a_effect_pct": effect,
                               "b_effect": None, "match": False})
            continue
        reported = str(match.iloc[0]["reported_effect"])
        number = re.search(r"(\d+(?:\.\d+)?)", reported)
        magnitude = float(number.group(1)) if number else None
        # The published wording is a reduction; compare its magnitude with
        # the independently calculated percentage from the A values.
        expected_magnitude = abs(effect)
        p05_checks.append({
            "position_mm": int(row["limiter_position_mm"]),
            "quantity": row["quantity"],
            "a_effect_pct": effect,
            "b_effect": reported,
            "match": magnitude is not None and np.isclose(expected_magnitude, magnitude, atol=0.6),
        })

    a6 = load_dataset_table("A", "laboratory_measurements/exp6_pressure_mhd.csv")
    b6 = load_dataset_table("B", "publication_reconstruction/paper6_pressure_mhd.csv")
    p06_pressure = a6.merge(b6, on="pressure_Torr", suffixes=("_a", "_b"))
    p06_table = []
    for _, row in p06_pressure.iterrows():
        delta = float(row["dominant_frequency_kHz_b"]) - float(row["dominant_frequency_kHz_a"])
        p06_table.append({
            "pressure_Torr": float(row["pressure_Torr"]),
            "a_frequency_kHz": float(row["dominant_frequency_kHz_a"]),
            "b_digitized_frequency_kHz": float(row["dominant_frequency_kHz_b"]),
            "b_minus_a_kHz": delta,
            "interpretation": "approximate cross-source comparison; not independent validation",
        })

    a6_peaks = load_dataset_table("A", "laboratory_signal_analysis/e06_mhd_peak_summary.csv")
    b6_peaks = load_dataset_table("B", "publication_digitization/p06_figure2_peak_summary.csv")
    p06_peaks = a6_peaks.merge(b6_peaks, on=["panel", "pressure_Torr"], suffixes=("_a", "_b"))
    p06_peak_checks = []
    for _, row in p06_peaks.iterrows():
        delta = float(row["peak_frequency_kHz_b"]) - float(row["peak_frequency_kHz_a"])
        axis_uncertainty = float(row["peak_frequency_uncertainty_kHz_b"])
        p06_peak_checks.append({
            "panel": row["panel"],
            "pressure_Torr": float(row["pressure_Torr"]),
            "a_peak_kHz": float(row["peak_frequency_kHz_a"]),
            "b_digitized_peak_kHz": float(row["peak_frequency_kHz_b"]),
            "b_minus_a_kHz": delta,
            "within_stated_axis_calibration_uncertainty": abs(delta) <= axis_uncertainty,
            "uncertainty_note": "published-figure x-axis calibration only; peak-selection uncertainty is not quantified",
        })

    return {
        "P01_spectroscopy": {
            **p01,
            "interpretation": "Published-table overlap; not independent validation.",
        },
        "P02_hard_xray": {
            **p02_hxr,
            "interpretation": "A/B values overlap with P02 Table 1; mean energy in B is derived.",
        },
        "P02_modes": {
            **p02_modes,
            "interpretation": "Exact Table 2 transcription overlap; explicitly not independent validation.",
        },
        "P03_compound_probe": {
            **p03,
            "interpretation": "Shared reported geometry/parameters; additional abstract values are only in B.",
        },
        "P04_pressure_transport": {
            **p04,
            "interpretation": "Source-text comparison; preserve the reported A/B mismatch instead of overwriting either file.",
        },
        "P05_limiter_transport": {
            "checks": p05_checks,
            "field_checks": len(p05_checks),
            "equal_effects": sum(bool(item["match"]) for item in p05_checks),
            "differences": [item for item in p05_checks if not item["match"]],
            "interpretation": "A's supplied values converted to percentage changes and checked against reported B effects.",
        },
        "P06_pressure_mhd": {
            "table_frequency_comparisons": p06_table,
            "digitized_peak_comparisons": p06_peak_checks,
            "interpretation": "Approximate cross-source comparisons; no raw-time PSD is calculated from E06's frequency-domain file.",
        },
    }
