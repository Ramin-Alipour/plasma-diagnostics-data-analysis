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

def test_p05_reextraction_preserves_article_direction_and_conclusion_ranges():
    b = pd.read_csv(DATA_B / "paper5_limiter_transport.csv")

    def effect(position, bias, quantity):
        rows = b[
            (b["limiter_position_mm"] == position)
            & (b["bias_V"] == bias)
            & (b["quantity"] == quantity)
        ]
        assert len(rows) == 1
        return rows.iloc[0]["reported_effect"]

    # The article reports a dramatic increment at 10 mm, not a reduction.
    assert effect(10, 200, "reynolds_stress") == "dramatic_increment_with_wild_fluctuations"
    assert effect(10, -200, "reynolds_stress") == "dramatic_increment_with_wild_fluctuations"
    # At 5 mm and -200 V, the article says the reduction was ineffective;
    # it does not quantify an increase.
    assert effect(5, -200, "radial_turbulent_transport") == "not_effective_in_decreasing_transport"

    expected_ranges = {
        "radial_electric_field": "increased_about_20_to_30_percent",
        "poloidal_electric_field": "reduced_about_30_to_40_percent",
        "poloidal_turbulent_transport_conclusion_range": "increased_about_25_to_35_percent",
        "radial_turbulent_transport_conclusion_range": "reduced_about_35_to_45_percent",
        "reynolds_stress_conclusion_range": "reduced_about_5_to_10_percent",
    }
    for quantity, expected in expected_ranges.items():
        assert effect(5, 200, quantity) == expected
