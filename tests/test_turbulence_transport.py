import numpy as np
import pytest

from turbulence_transport.fluctuations import (
    TurbulenceSyntheticConfig,
    correlation_coefficient,
    decompose_fluctuation,
    generate_synthetic_fluctuations,
)
from turbulence_transport.reynolds_stress import reynolds_force, reynolds_stress
from turbulence_transport.transport_analysis import (
    exb_velocity,
    parameter_scan,
    turbulent_particle_flux,
)


def test_synthetic_fluctuations_are_reproducible():
    a = generate_synthetic_fluctuations()
    b = generate_synthetic_fluctuations()
    np.testing.assert_allclose(a["density_m3"], b["density_m3"])
    np.testing.assert_allclose(a["potential_V"], b["potential_V"])


def test_mean_fluctuation_decomposition_reconstructs_signal():
    x = np.array([1.0, 2.0, 4.0, 5.0])
    result = decompose_fluctuation(x)
    np.testing.assert_allclose(result["mean"] + result["fluctuation"], x)
    assert np.mean(result["fluctuation"]) == pytest.approx(0.0)


def test_correlation_of_identical_signals_is_one():
    x = np.sin(np.linspace(0, 4 * np.pi, 1000))
    assert correlation_coefficient(x, x) == pytest.approx(1.0)


def test_reynolds_stress_known_case():
    x = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
    vr = 3.0 * np.sin(x)
    vt = 2.0 * np.sin(x)
    assert reynolds_stress(vr, vt) == pytest.approx(3.0, abs=1e-3)


def test_reynolds_stress_phase_quadrature_is_near_zero():
    x = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
    assert reynolds_stress(np.sin(x), np.cos(x)) == pytest.approx(0.0, abs=1e-3)


def test_reynolds_force_from_linear_profile():
    r = np.linspace(0.0, 0.01, 101)
    stress = 2.0 + 50.0 * r
    np.testing.assert_allclose(reynolds_force(r, stress), -50.0, atol=1e-9)


def test_exb_velocity_cartesian_identity_case():
    E = np.array([0.0, 100.0, 0.0])
    B = np.array([0.0, 0.0, 2.0])
    v = exb_velocity(E, B)
    np.testing.assert_allclose(v, [50.0, 0.0, 0.0])


def test_exb_velocity_time_series_shape():
    E = np.zeros((3, 10))
    E[1] = 20.0
    B = np.zeros((3, 10))
    B[2] = 2.0
    v = exb_velocity(E, B)
    assert v.shape == (3, 10)
    np.testing.assert_allclose(v[0], 10.0)


def test_turbulent_particle_flux_known_case():
    x = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
    density = 1e18 + 2e16 * np.sin(x)
    velocity = 3e3 * np.sin(x)
    expected = 0.5 * 2e16 * 3e3
    assert turbulent_particle_flux(density, velocity) == pytest.approx(expected, rel=1e-3)


def test_parameter_scan_is_explicitly_synthetic():
    result = parameter_scan([1.0, 2.0, 3.0], "pressure", baseline_response=2.0, sensitivity=0.5)
    np.testing.assert_allclose(result["response"], [2.0, 3.0, 4.0])
    assert result["data_type"] == "synthetic"
    assert result["model"] == "linear_sensitivity"


def test_invalid_zero_magnetic_field_is_rejected():
    with pytest.raises(ValueError):
        exb_velocity([1.0, 0.0, 0.0], [0.0, 0.0, 0.0])


def test_directional_particle_flux_wrappers_are_consistent():
    from turbulence_transport import turbulent_radial_particle_flux, turbulent_poloidal_particle_flux
    x = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
    density = 1e18 + 2e16 * np.sin(x)
    velocity = 3e3 * np.sin(x)
    expected = 0.5 * 2e16 * 3e3
    assert turbulent_radial_particle_flux(density, velocity) == pytest.approx(expected, rel=1e-3)
    assert turbulent_poloidal_particle_flux(density, velocity) == pytest.approx(expected, rel=1e-3)
