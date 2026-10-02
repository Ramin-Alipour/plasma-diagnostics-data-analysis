import numpy as np
import pandas as pd
from publication_reconstruction.reconstruct import reconstruct_paper2, reconstruct_paper3
from publication_reconstruction.advanced import (
    reconstruct_paper1_full, reconstruct_paper2_modes, reconstruct_hxr_spectrum,
    cross_diagnostic_summary, paper3_bootstrap_uncertainty, paper4_physics_chain,
    paper5_parameterized_scenarios, paper6_pressure_psd,
)
from publication_reconstruction.master_audit import run_master_audit


def test_p01_full_reconstruction_has_reasonable_mean_error():
    df=pd.read_csv('data/publication_reconstruction/paper1_spectroscopy.csv')
    out,_=reconstruct_paper1_full(df, mc=40)
    assert out.uncertainty_eV.gt(0).all()
    assert out.relative_error_pct.abs().mean() < 2.0


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


def test_p05_reported_effects_are_explicit_calibration_targets():
    out=paper5_parameterized_scenarios()
    for pos,radial,stress in [(0,-50,-15),(5,-35,-5)]:
        r=out[(out.position_mm==pos)&(out.bias_V==200)].iloc[0]
        assert np.isclose(r.radial_change_pct,radial)
        assert np.isclose(r.stress_change_pct,stress)


def test_master_audit_all_six_pass():
    summary,_=run_master_audit()
    assert len(summary)==6
    assert set(summary.status)=={'PASS'}
