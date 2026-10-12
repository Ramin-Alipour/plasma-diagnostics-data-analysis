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
            left_name = f"{left_col}_a" if left_col in a.columns and left_col in b.columns and left_col not in keys else left_col
            right_name = f"{right_col}_b" if right_col in a.columns and right_col in b.columns and right_col not in keys else right_col
            left_value, right_value = row[left_name], row[right_name]
            checks.append({
                "key": [row[k] for k in keys],
                "field_a": left_col,
                "field_b": right_col,
                "a": left_value,
                "b": right_value,
                "match": _num_equal(left_value, right_value, atol=atol),
            })
    return {
        "matched_rows": int(len(joined)),
        "field_checks": int(len(checks)),
        "equal_fields": int(sum(item["match"] for item in checks)),
        "differences": [item for item in checks if not item["match"]],
    }


def _effect_report_check(effect_pct: float, reported: str, atol: float = 0.6) -> dict[str, Any]:
    """Check both direction and magnitude for a numeric effect described in prose."""
    text = str(reported).lower().replace("_", " ")
    direction = "reduction" if "reduc" in text else ("increase" if "increas" in text or "increment" in text else None)
    observed_direction = "increase" if effect_pct > 0 else ("reduction" if effect_pct < 0 else "no_change")
    direction_matches = direction is not None and direction == observed_direction
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]
    magnitude_matches = False
    magnitude_delta = None
    reported_range = None
    if numbers:
        if len(numbers) >= 2 and (" to " in text or "between" in text):
            lo, hi = min(numbers[0], numbers[1]), max(numbers[0], numbers[1])
            reported_range = [lo, hi]
            magnitude_matches = lo - atol <= abs(effect_pct) <= hi + atol
            magnitude_delta = 0.0 if magnitude_matches else (abs(effect_pct) - lo if abs(effect_pct) < lo else abs(effect_pct) - hi)
        else:
            target = numbers[0]
            reported_range = [target, target]
            magnitude_matches = bool(np.isclose(abs(effect_pct), target, rtol=0.0, atol=atol))
            magnitude_delta = 0.0 if magnitude_matches else abs(effect_pct) - target
    return {"reported_direction": direction, "a_direction": observed_direction, "direction_matches": direction_matches, "reported_magnitude_pct": reported_range, "a_magnitude_pct": abs(effect_pct), "magnitude_delta_pct_points": magnitude_delta, "magnitude_matches": magnitude_matches, "match": direction_matches and magnitude_matches}

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
        atol=1e-5,
    )

    a2m = load_dataset_table("A", "laboratory_measurements/exp2_modes.csv")
    b2m = load_dataset_table("B", "publication_reconstruction/paper2_modes.csv")
    b2m = b2m.rename(columns={"paper_id": "experiment_id"})
    mode_fields = [(f"m{i}_pct", f"m{i}_pct") for i in range(1, 7)]
    mode_fields.append(("edge_safety_factor", "edge_safety_factor"))
    p02_modes = _matches(
        a2m, b2m, ["time_start_ms", "time_end_ms"], mode_fields
    )

    a3 = load_dataset_table("A", "laboratory_measurements/exp3_compound_probe.csv")
    b3 = load_dataset_table("B", "publication_reconstruction/paper3_compound_probe.csv")
    b3 = b3.rename(columns={"paper_id": "experiment_id"})
    p03 = _matches(a3, b3, ["quantity"], [("value", "value")])

    a4 = load_dataset_table("A", "laboratory_measurements/exp4_pressure_transport.csv")
    b4 = load_dataset_table("B", "publication_reconstruction/paper4_pressure_transport.csv")
    p04_pairs = [
        ("max_current_kA", "max_current_kA"),
        ("steady_state_ms", "steady_state_ms"),
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
            & (b5["bias_V"] == row["bias_V"])
            & (b5["quantity"] == row["quantity"])
        ]
        if match.empty:
            p05_checks.append({"position_mm": row["limiter_position_mm"],
                               "quantity": row["quantity"], "a_effect_pct": effect,
                               "b_effect": None, "match": False})
            continue
        reported = str(match.iloc[0]["reported_effect"])
        effect_check = _effect_report_check(effect, reported)
        p05_checks.append({
            "position_mm": int(row["limiter_position_mm"]),
            "quantity": row["quantity"],
            "a_effect_pct": effect,
            "b_effect": reported,
            **effect_check,
        })

    a6 = load_dataset_table("A", "laboratory_measurements/exp6_pressure_mhd.csv")
    b6 = load_dataset_table("B", "publication_reconstruction/paper6_pressure_mhd.csv")
    p06_pressure = a6.merge(b6, on="pressure_Torr", suffixes=("_a", "_b"))
    p06_table = []
    for _, row in p06_pressure.iterrows():
        delta = float(row["dominant_frequency_kHz_b"]) - float(row["dominant_frequency_kHz_a"])
        steady_delta = float(row["steady_state_ms_b"]) - float(row["steady_state_ms_a"])
        discharge_bound_match = _num_equal(
            row["discharge_time_max_ms_a"], row["discharge_time_max_ms_b"]
        )
        frequency_uncertainty = float(row["dominant_frequency_uncertainty_kHz"])
        p06_table.append({
            "pressure_Torr": float(row["pressure_Torr"]),
            "a_steady_state_ms": float(row["steady_state_ms_a"]),
            "b_steady_state_ms": float(row["steady_state_ms_b"]),
            "steady_state_b_minus_a_ms": steady_delta,
            "a_discharge_time_upper_bound_ms": float(row["discharge_time_max_ms_a"]),
            "b_discharge_time_upper_bound_ms": float(row["discharge_time_max_ms_b"]),
            "discharge_time_bound_matches": discharge_bound_match,
            "a_frequency_kHz": float(row["dominant_frequency_kHz_a"]),
            "b_digitized_frequency_kHz": float(row["dominant_frequency_kHz_b"]),
            "b_frequency_uncertainty_kHz": frequency_uncertainty,
            "b_minus_a_kHz": delta,
            "within_peak_selection_uncertainty": abs(delta) <= frequency_uncertainty,
            "interpretation": "text-reported timing/bound correspondence plus approximate cross-source frequency comparison; not independent validation",
        })

    a6_peaks = load_dataset_table("A", "laboratory_signal_analysis/e06_mhd_peak_summary.csv")
    b6_peaks = load_dataset_table("B", "publication_digitization/p06_figure2_peak_summary.csv")
    p06_peaks = a6_peaks.merge(b6_peaks, on=["panel", "pressure_Torr"], suffixes=("_a", "_b"))
    p06_peak_checks = []
    for _, row in p06_peaks.iterrows():
        delta = float(row["peak_frequency_kHz_b"]) - float(row["peak_frequency_kHz_a"])
        peak_uncertainty = float(row["peak_frequency_uncertainty_kHz_b"])
        p06_peak_checks.append({
            "panel": row["panel"],
            "pressure_Torr": float(row["pressure_Torr"]),
            "a_peak_kHz": float(row["peak_frequency_kHz_a"]),
            "b_digitized_peak_kHz": float(row["peak_frequency_kHz_b"]),
            "b_minus_a_kHz": delta,
            "within_stated_peak_selection_uncertainty": abs(delta) <= peak_uncertainty,
            "uncertainty_note": "combined axis-calibration and peak-selection uncertainty (~3.1 kHz); not independent validation",
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
            "matching_effects": sum(bool(item["match"]) for item in p05_checks),
            "direction_mismatches": [item for item in p05_checks if not item.get("direction_matches", False)],
            "differences": [item for item in p05_checks if not item["match"]],
            "interpretation": "A's supplied values converted to percentage changes and checked against reported B effects.",
        },
        "P06_pressure_mhd": {
            "table_frequency_comparisons": p06_table,
            "digitized_peak_comparisons": p06_peak_checks,
            "interpretation": "Approximate cross-source comparisons; no raw-time PSD is calculated from E06's frequency-domain file.",
        },
    }
