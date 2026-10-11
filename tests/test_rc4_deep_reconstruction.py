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


def test_p01_full_reconstruction_records_resolution_consistency_difference():
    df=load_constraints('paper1_spectroscopy.csv')
    out,_=reconstruct_paper1_full(df, mc=40)
    assert out.uncertainty_eV.gt(0).all()
    assert out.relative_difference_pct.abs().mean() > 5.0


def test_p01_uses_documented_quadrature_resolution_model_not_table_column():
    df = load_constraints("paper1_spectroscopy.csv")
    out, _ = reconstruct_paper1_full(df, mc=10)
    expected = np.sqrt(0.03704**2 + (out.wavelength_nm / 1.35e5)**2)
    assert np.allclose(out.model_resolution_fwhm_nm, expected)
    assert np.allclose(out.instrumental_broadening_fwhm_nm, 0.03704)
    assert np.allclose(out.diffraction_broadening_fwhm_nm, out.wavelength_nm / 1.35e5)
    assert (out.tabulated_resolution_fwhm_nm - out.model_resolution_fwhm_nm).abs().mean() > 0.001


def test_p01_table_mode_reproduces_reported_temperature_constraints_without_mutating_source():
    df = load_constraints("paper1_spectroscopy.csv")
    original = df.copy(deep=True)
    table_out = run_master_audit()[1]["P01_table_reproduction"]
    equation_out, _ = reconstruct_paper1_full(df, mc=10, resolution_mode="equation")
    tabulated_out, _ = reconstruct_paper1_full(df, mc=10, resolution_mode="tabulated")
    assert table_out.relative_difference_pct.abs().mean() < 0.1
    assert equation_out.relative_difference_pct.abs().mean() > 100
    assert np.allclose(tabulated_out.model_resolution_fwhm_nm, df.resolution_fwhm_nm)
    assert np.allclose(equation_out.model_resolution_fwhm_nm, equation_out.equation_resolution_fwhm_nm)
    pd.testing.assert_frame_equal(df, original)


def test_p01_source_table_values_track_linear_sum_not_printed_quadrature():
    df = load_constraints("paper1_spectroscopy.csv")
    instrumental = 0.03704
    diffraction = df.wavelength_nm / 1.35e5
    quadrature = np.sqrt(instrumental**2 + diffraction**2)
    linear_sum = instrumental + diffraction
    # Source Table VI is preserved as published; this test records its numerical
    # relation to the printed equation instead of silently treating it as equivalent.
    table = df.resolution_fwhm_nm.to_numpy()
    assert np.mean(np.abs(table - linear_sum.to_numpy())) < 1e-4
    assert np.mean(np.abs(table - quadrature.to_numpy())) > 1e-3


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
        for paper in ("P01", "P04", "P05", "P06"):
            assert static.loc[paper, "status"] == dynamic.loc[paper, "status"]
        assert np.isclose(float(static.loc["P01", "value"]),
                          float(dynamic.loc["P01", "value"]), rtol=1e-6)
        assert np.isclose(float(static.loc["P01", "reconstructed"]), float(dynamic.loc["P01", "reconstructed"]), rtol=1e-6), dynamic.loc["P01"].to_dict()
        assert np.isclose(float(static.loc["P06", "value"]),
                          float(dynamic.loc["P06", "value"]), atol=1e-3)


def test_master_audit_all_six_completed():
    summary,_=run_master_audit()
    assert len(summary)==6
    assert summary.loc[summary.paper=='P01','status'].iloc[0]=='CONSISTENCY CHECK'
    assert summary.loc[summary.paper=='P05','status'].iloc[0]=='CONSISTENCY CHECK'
    statuses = summary.set_index('paper')['status']
    assert statuses['P02'] == 'PASS'
    assert statuses['P03'] == 'PASS'
    assert statuses['P04'] == 'CONSISTENCY CHECK'
    assert statuses['P06'] == 'CONSISTENCY CHECK'
