import numpy as np
import pytest
from tokamak_workbench.catalog import CATALOG, get_parameter, list_parameters
from tokamak_workbench.physics import beta_local, debye_length_m, doppler_temperature_eV, doppler_velocity_m_s, electron_plasma_frequency_hz, energy_confinement_time_s, electric_field_1d_v_m, greenwald_density_m3, power_spectral_density, svd_decompose

def test_catalog_ids_and_fields():
    ids=[x["id"] for x in CATALOG]
    assert len(ids)==len(set(ids))
    assert all({"id","name","symbol","unit","family","status","formula","limitations"} <= set(x) for x in CATALOG)

def test_lookup():
    assert get_parameter("ti")["symbol"]=="T_i"
    assert list_parameters("spectroscopy")
    with pytest.raises(KeyError): get_parameter("not_a_parameter")

def test_spectroscopy():
    assert doppler_temperature_eV(.01,500,40)>0
    assert doppler_velocity_m_s(.1,500)==pytest.approx(59958.4916,rel=1e-5)
    with pytest.raises(ValueError): doppler_temperature_eV(0,500,40)

def test_derived_quantities():
    assert beta_local(1000,2)>0
    assert debye_length_m(1e19,100)>0
    assert electron_plasma_frequency_hz(1e19)>0
    assert energy_confinement_time_s(1000,500)==pytest.approx(2)
    assert greenwald_density_m3(1,.5)==pytest.approx(1.2732395447e20)

def test_signal_analysis():
    x=np.linspace(0,1,11)
    assert np.allclose(electric_field_1d_v_m(x,2*x),-2)
    f,p=power_spectral_density(np.sin(2*np.pi*10*np.arange(1000)/1000),1000)
    assert len(f)==len(p)
    u,s,vh=svd_decompose(np.arange(20,dtype=float).reshape(2,10))
    assert len(s)==2
