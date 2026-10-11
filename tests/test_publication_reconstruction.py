from pathlib import Path
import numpy as np
import pandas as pd
from publication_reconstruction.reconstruct import (
    load_constraints, reconstruct_paper1, reconstruct_paper2,
    reconstruct_paper3, reconstruct_paper4, reconstruct_paper5, reconstruct_paper6,
)
from publication_reconstruction.validation import consistency_check_paper1

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


def test_paper1_temperature_comparison_is_consistency_check_not_forced_match():
    v=consistency_check_paper1(reconstruct_paper1()[0])
    assert 'relative_difference_pct' in v.columns
    assert np.max(np.abs(v.relative_difference_pct)) < 0.2


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
