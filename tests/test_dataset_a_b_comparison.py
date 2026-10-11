from pathlib import Path

import numpy as np
import pandas as pd

from plasma_provenance.dataset_comparison import compare_dataset_a_b


ROOT = Path(__file__).resolve().parents[1]
DATA_A = ROOT / "datasets" / "dataset_a" / "laboratory_measurements"
DATA_B = ROOT / "datasets" / "dataset_b" / "publication_reconstruction"


def test_p04_reextracted_text_values_and_a_b_discrepancy_are_preserved():
    a = pd.read_csv(DATA_A / "exp4_pressure_transport.csv").set_index("pressure_Torr")
    b = pd.read_csv(DATA_B / "paper4_pressure_transport.csv").set_index("pressure_Torr")

    assert np.allclose(
        b["radial_transport_plus200"].to_numpy(),
        [0.0043, -0.0011, 0.00036],
        rtol=0.0,
        atol=1e-12,
    )
    assert np.allclose(
        b["poloidal_transport_plus200"].to_numpy(),
        [0.0161, 0.0197, 0.0103],
        rtol=0.0,
        atol=1e-12,
    )
    assert np.allclose(
        b["poloidal_transport_minus200"].to_numpy(),
        [0.0093, 0.0075, 0.0080],
        rtol=0.0,
        atol=1e-12,
    )

    # Dataset A remains untouched: the article text says -1.1e-3 at 2.3 Torr.
    assert a.loc[2.3, "radial_transport_plus200"] == 0.0010
    assert b.loc[2.3, "radial_transport_plus200"] == -0.0011


def test_p06_unreported_analysis_windows_are_not_copied_into_dataset_b():
    b = pd.read_csv(DATA_B / "paper6_pressure_mhd.csv")
    assert b["analysis_windows_ms"].isna().all()


def test_software_comparison_reports_source_overlap_and_real_discrepancy():
    result = compare_dataset_a_b()

    assert result["P01_spectroscopy"]["field_checks"] == 30
    assert result["P01_spectroscopy"]["equal_fields"] == 30

    assert result["P02_hard_xray"]["field_checks"] == 18
    assert result["P02_hard_xray"]["equal_fields"] == 18

    assert result["P02_modes"]["matched_rows"] == 20
    assert result["P02_modes"]["field_checks"] == 140
    assert result["P02_modes"]["equal_fields"] == 140
    assert "not independent validation" in result["P02_modes"]["interpretation"]

    assert result["P03_compound_probe"]["field_checks"] == 11
    assert result["P03_compound_probe"]["equal_fields"] == 11

    assert result["P04_pressure_transport"]["field_checks"] == 24
    assert result["P04_pressure_transport"]["equal_fields"] == 23
    discrepancy = result["P04_pressure_transport"]["differences"]
    assert len(discrepancy) == 1
    assert discrepancy[0]["key"] == [2.3]
    assert discrepancy[0]["a"] == 0.0010
    assert discrepancy[0]["b"] == -0.0011

    assert result["P05_limiter_transport"]["field_checks"] == 4
    assert result["P05_limiter_transport"]["equal_effects"] == 4

    p06 = result["P06_pressure_mhd"]
    assert len(p06["table_frequency_comparisons"]) == 3
    assert len(p06["digitized_peak_comparisons"]) == 3
    assert any(
        not row["within_stated_axis_calibration_uncertainty"]
        for row in p06["digitized_peak_comparisons"]
    )
