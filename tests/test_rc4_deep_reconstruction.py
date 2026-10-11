import numpy as np
import pandas as pd
from publication_reconstruction.reconstruct import load_constraints
from publication_reconstruction.reconstruct import reconstruct_paper2, reconstruct_paper3
from publication_reconstruction.advanced import (
    reconstruct_paper1_full, reconstruct_paper2_modes, reconstruct_hxr_spectrum,
    cross_diagnostic_summary, paper3_bootstrap_uncertainty, paper4_physics_chain,
    paper5_parameterized_scenarios, paper6_pressure_psd,
)
from publication_reconstruction.master_audit import run_master_audit


def test_p01_synthetic_reconstruction_has_uncertainty_but_no_publication_difference():
    df = load_constraints("paper1_spectroscopy.csv")
    out, _ = reconstruct_paper1_full(df, mc=40)
    assert out.uncertainty_eV.gt(0).all()
    assert np.isfinite(out.synthetic_temperature_eV).all()
    assert "relative_difference_pct" not in out.columns
    assert "reported_temperature_eV" not in out.columns


def test_p01_resolution_modes_are_software_paths_not_publication_comparisons():
    df = load_constraints("paper1_spectroscopy.csv")
    original = df.copy(deep=True)
    equation_out, _ = reconstruct_paper1_full(df, mc=10, resolution_mode="equation")
    tabulated_out, _ = reconstruct_paper1_full(df, mc=10, resolution_mode="tabulated")
    expected = np.sqrt(0.03704**2 + (equation_out.wavelength_nm / 1.35e5)**2)
    assert np.allclose(equation_out.model_resolution_fwhm_nm, expected)
    assert np.allclose(equation_out.instrumental_broadening_fwhm_nm, 0.03704)
    assert np.allclose(equation_out.diffraction_broadening_fwhm_nm, equation_out.wavelength_nm / 1.35e5)
    assert np.allclose(tabulated_out.model_resolution_fwhm_nm, df.resolution_fwhm_nm)
    assert "relative_difference_pct" not in equation_out.columns
    assert "reported_temperature_eV" not in equation_out.columns
    pd.testing.assert_frame_equal(df, original)


def test_p01_master_audit_reports_author_data_basis_only():
    summary, details = run_master_audit()
    p01 = summary.loc[summary.paper == "P01"].iloc[0]
    assert p01.status == "AUTHOR DATA BASIS"
    assert p01.metric == "reporting status"
    assert "alternate_model_mean_absolute_relative_difference_pct" not in summary.columns
    assert "relative_difference_pct" not in summary.columns
    assert details["P01"].iloc[0]["synthetic_comparison"] == "WITHDRAWN_NOT_REPORTABLE"
    assert "relative_difference_pct" not in details["P01"].columns


def test_p02_fourier_identification_recovers_m3_without_svd_labeling():
    hxr,_,modes,t,signals=reconstruct_paper2(samples_per_window=12000)
    out=reconstruct_paper2_modes(modes,t,signals)
    m3=out[out.mode_m==3]
    assert m3.reconstructed_fraction_pct.mean() > 85
    assert m3.absolute_error_pct.abs().mean() < 1


def test_p02_hxr_preserves_event_constraints():
    hxr,_,_,t,signals=reconstruct_paper2(samples_per_window=12000)
    spectra=reconstruct_hxr_spectrum(hxr)
    assert [x['reconstructed_count'] for x in spectra] == list(hxr.total_counts.astype(int))
    assert np.allclose([x['reconstructed_event_mean_keV'] for x in spectra], hxr.mean_energy_keV)
    cross=cross_diagnostic_summary(spectra,t,signals)
    assert (cross.m3_dominant_frequency_kHz > 40).all()


def test_p03_bootstrap_uncertainty_is_positive():
    _,t,iu,idn,_,_=reconstruct_paper3()
    mean,unc,_=paper3_bootstrap_uncertainty(iu,idn,n_boot=100)
    assert 0 < mean < 1
    assert unc > 0


def test_p04_transport_chain_hits_reported_constraints():
    for p in (1.9,2.3,2.7):
        d=paper4_physics_chain(p)
        assert np.isclose(d['radial_transport_proxy'],d['reported_radial_transport'])
        assert np.isclose(d['poloidal_transport_proxy'],d['reported_poloidal_transport'])


def test_p05_reported_effects_are_explicit_consistency_check_targets():
    out=paper5_parameterized_scenarios()
    for pos,radial,stress in [(0,-50,-15),(5,-35,-5)]:
        r=out[(out.position_mm==pos)&(out.bias_V==200)].iloc[0]
        assert np.isclose(r.radial_change_pct,radial)
        assert np.isclose(r.stress_change_pct,stress)


def test_static_audit_csvs_match_current_consistency_statuses():
    from pathlib import Path

    summary, _ = run_master_audit()
    root = Path(__file__).resolve().parents[1]
    dynamic = summary.set_index("paper")
    for relative_path in ("audit/MASTER_AUDIT.csv", "audit/RC4_MASTER_AUDIT.csv"):
        static = pd.read_csv(root / relative_path).set_index("paper")
        for paper in ("P04", "P05", "P06"):
            assert static.loc[paper, "status"] == dynamic.loc[paper, "status"]
        assert static.loc["P01", "status"] == "AUTHOR DATA BASIS"
        assert "alternate_model_mean_absolute_relative_difference_pct" not in static.columns
        assert "relative_difference_pct" not in static.columns
        assert np.isclose(float(static.loc["P06", "value"]),
                          float(dynamic.loc["P06", "value"]), atol=1e-3)


def test_master_audit_all_six_completed():
    summary,_=run_master_audit()
    assert len(summary)==6
    assert summary.loc[summary.paper=='P01','status'].iloc[0]=='AUTHOR DATA BASIS'
    assert summary.loc[summary.paper=='P05','status'].iloc[0]=='CONSISTENCY CHECK'
    statuses = summary.set_index('paper')['status']
    assert statuses['P02'] == 'PASS'
    assert statuses['P03'] == 'PASS'
    assert statuses['P04'] == 'CONSISTENCY CHECK'
    assert statuses['P06'] == 'CONSISTENCY CHECK'
