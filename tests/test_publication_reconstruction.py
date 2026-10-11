from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from publication_reconstruction.reconstruct import (
    load_constraints, reconstruct_paper1, reconstruct_paper2,
    reconstruct_paper3, reconstruct_paper4, reconstruct_paper5, reconstruct_paper6,
)
from publication_reconstruction.validation import consistency_check_paper1
from publication_reconstruction.synthetic_noise import add_relative_gaussian_noise

DATA=Path(__file__).resolve().parents[1]/'datasets'/'dataset_b'/'publication_reconstruction'


def test_all_six_constraint_files_exist_and_are_nonempty():
    files=['paper1_spectroscopy.csv','paper2_hxr.csv','paper2_modes.csv','paper3_compound_probe.csv','paper4_pressure_transport.csv','paper5_limiter_transport.csv','paper6_pressure_mhd.csv']
    for f in files:
        df=load_constraints(f)
        assert not df.empty


def test_paper1_preserves_source_reported_resolution_values():
    df = load_constraints('paper1_spectroscopy.csv')
    assert df.resolution_fwhm_nm.notna().all()
    assert df.resolution_fwhm_nm.between(0.0400, 0.0411).all()
    assert df.doppler_fwhm_nm.notna().all()


def test_paper1_synthetic_helper_emits_no_publication_discrepancy():
    source = load_constraints("paper1_spectroscopy.csv")
    original = source.copy(deep=True)
    result = consistency_check_paper1(source)
    assert "synthetic_temperature_eV" in result.columns
    assert "reported_TeV" not in result.columns
    assert "relative_difference_pct" not in result.columns
    assert np.isfinite(result["synthetic_temperature_eV"]).all()
    assert result["model_resolution_fwhm_nm"].between(0.0370, 0.0380).all()
    pd.testing.assert_frame_equal(source, original)


def test_reconstructions_are_deterministic():
    a=reconstruct_paper2(seed=22)[3:]
    b=reconstruct_paper2(seed=22)[3:]
    assert np.allclose(a[0],b[0]); assert np.allclose(a[1],b[1])
    a=reconstruct_paper3(seed=22)[1:]
    b=reconstruct_paper3(seed=22)[1:]
    assert np.allclose(a[1],b[1]); assert np.allclose(a[2],b[2])


def test_six_paper_generators_return_data():
    assert len(reconstruct_paper1()[1])==15
    assert len(reconstruct_paper2()[1])==6
    assert len(reconstruct_paper3()[1])==3000
    assert len(reconstruct_paper4()[1])==3
    assert len(reconstruct_paper5())==9
    assert len(reconstruct_paper6()[1])==3


def test_p04_advanced_chain_preserves_text_constraints_separately_from_dataset_b_approximations():
    from publication_reconstruction.advanced import paper4_physics_chain

    constraints = load_constraints("paper4_pressure_transport.csv")
    for row in constraints.itertuples(index=False):
        result = paper4_physics_chain(row.pressure_Torr)
        text_radial = {1.9: 0.0066, 2.3: 0.0015, 2.7: 0.0015}[row.pressure_Torr]
        text_poloidal = {1.9: 0.0129, 2.3: 0.0092, 2.7: 0.0089}[row.pressure_Torr]
        assert result["text_constraint_radial_transport"] == pytest.approx(text_radial)
        assert result["text_constraint_poloidal_transport"] == pytest.approx(text_poloidal)
        assert result["radial_transport_proxy"] == pytest.approx(text_radial)
        assert result["poloidal_transport_proxy"] == pytest.approx(text_poloidal)
        # These are intentionally not overwritten with the separate approximate CSV values.


def test_master_audit_uses_canonical_dataset_b_and_keeps_p04_sources_distinct():
    from publication_reconstruction.master_audit import run_master_audit
    from plasma_provenance.dataset_archive import load_dataset_table

    summary, details = run_master_audit()
    canonical = load_dataset_table("B", "publication_digitization/p06_figure2_peak_summary.csv")
    pd.testing.assert_frame_equal(
        details["P06_digitized"].reset_index(drop=True),
        canonical.reset_index(drop=True),
    )
    assert set(details["P06_digitized"]["panel"]) == {"a", "b", "c"}
    p04 = details["P04"]
    assert {"dataset_b_radial_approximate", "dataset_b_poloidal_approximate",
            "radial_proxy", "poloidal_proxy", "constraint_type"}.issubset(p04.columns)
    assert p04["constraint_type"].str.contains("text-level constraint").all()
    p06_summary = summary.loc[summary["paper"] == "P06"].iloc[0]
    assert p06_summary["status"] == "CONSISTENCY CHECK"


def test_p06_pressure_specific_frequency_estimates_remain_approximate_constraints():
    constraints = load_constraints("paper6_pressure_mhd.csv")
    assert constraints["confidence"].str.contains("digitized_frequency").all()
    # The synthetic signal generator uses the text-reported approximately 44 kHz
    # activity; pressure-specific estimates are not silently treated as exact.
    _, recon = reconstruct_paper6()
    assert all(item["target_frequency_kHz"] == 44.0 for item in recon)



def test_synthetic_relative_noise_is_1_3_percent_and_reproducible():
    reference = np.concatenate([np.full(100_000, 100.0), np.zeros(3), np.array([-50.0])])
    original = reference.copy()
    first = add_relative_gaussian_noise(reference, seed=130)
    second = add_relative_gaussian_noise(reference, seed=130)

    assert np.array_equal(first, second)
    assert np.array_equal(reference, original)  # input is not mutated
    assert np.array_equal(first[-4:-1], np.zeros(3))  # zero references stay zero
    assert np.std(first[:100_000] - reference[:100_000]) == pytest.approx(1.3, rel=0.02)
    assert np.isfinite(first).all()


def test_synthetic_relative_noise_rejects_invalid_inputs():
    import pytest

    with pytest.raises(ValueError, match="finite"):
        add_relative_gaussian_noise([1.0, np.nan], seed=1)
    with pytest.raises(ValueError, match="relative_std"):
        add_relative_gaussian_noise([1.0], relative_std=-0.013, seed=1)



def test_paper1_generator_applies_1_3_percent_relative_noise_to_nonzero_signal():
    _, clean_spectra = reconstruct_paper1(seed=19, relative_noise_std=0.0)
    _, noisy_spectra = reconstruct_paper1(seed=19, relative_noise_std=0.013)
    clean = np.concatenate([entry[2] for entry in clean_spectra])
    noisy = np.concatenate([entry[2] for entry in noisy_spectra])
    mask = clean > 0.1
    relative_residual = (noisy[mask] - clean[mask]) / np.abs(clean[mask])
    assert np.std(relative_residual) == pytest.approx(0.013, rel=0.08)



def _measured_relative_noise_std(clean, noisy):
    clean = np.asarray(clean, dtype=float)
    noisy = np.asarray(noisy, dtype=float)
    mask = np.abs(clean) > 1e-10
    assert mask.sum() > 100
    return float(np.std((noisy[mask] - clean[mask]) / np.abs(clean[mask])))


def test_all_six_reconstruction_generators_apply_shared_relative_noise():
    # Each comparison holds the synthetic model and random seed fixed, changing
    # only the declared measurement-noise standard deviation.
    _, p1_clean = reconstruct_paper1(seed=51, relative_noise_std=0.0)
    _, p1_noisy = reconstruct_paper1(seed=51, relative_noise_std=0.013)
    assert _measured_relative_noise_std(
        np.concatenate([v[2] for v in p1_clean]),
        np.concatenate([v[2] for v in p1_noisy]),
    ) == pytest.approx(0.013, rel=0.10)

    p2_clean = reconstruct_paper2(seed=52, relative_noise_std=0.0)
    p2_noisy = reconstruct_paper2(seed=52, relative_noise_std=0.013)
    assert _measured_relative_noise_std(p2_clean[4], p2_noisy[4]) == pytest.approx(0.013, rel=0.10)

    p3_clean = reconstruct_paper3(seed=53, relative_noise_std=0.0)
    p3_noisy = reconstruct_paper3(seed=53, relative_noise_std=0.013)
    assert _measured_relative_noise_std(p3_clean[2], p3_noisy[2]) == pytest.approx(0.013, rel=0.10)
    assert _measured_relative_noise_std(p3_clean[3], p3_noisy[3]) == pytest.approx(0.013, rel=0.10)

    _, p4_clean = reconstruct_paper4(seed=54, relative_noise_std=0.0)
    _, p4_noisy = reconstruct_paper4(seed=54, relative_noise_std=0.013)
    assert _measured_relative_noise_std(p4_clean[0]["Er_V_m"], p4_noisy[0]["Er_V_m"]) == pytest.approx(0.013, rel=0.10)
    assert _measured_relative_noise_std(p4_clean[0]["radial_transport"], p4_noisy[0]["radial_transport"]) == pytest.approx(0.013, rel=0.10)

    p5_clean = reconstruct_paper5(seed=55, relative_noise_std=0.0)
    p5_noisy = reconstruct_paper5(seed=55, relative_noise_std=0.013)
    assert _measured_relative_noise_std(p5_clean[0]["radial_transport"], p5_noisy[0]["radial_transport"]) == pytest.approx(0.013, rel=0.10)

    _, p6_clean = reconstruct_paper6(seed=56, relative_noise_std=0.0)
    _, p6_noisy = reconstruct_paper6(seed=56, relative_noise_std=0.013)
    assert _measured_relative_noise_std(p6_clean[0]["mirnov"], p6_noisy[0]["mirnov"]) == pytest.approx(0.013, rel=0.10)
