import numpy as np
import pytest

from electrostatic_diagnostics.langmuir_probe.synthetic import (
    LangmuirSyntheticConfig,
    generate_synthetic_langmuir_iv,
)
from electrostatic_diagnostics.langmuir_probe.analysis import (
    estimate_floating_potential,
    fit_langmuir_iv,
)
from electrostatic_diagnostics.electric_fields.field import electric_field_from_potential
from electrostatic_diagnostics.compound_probe.synthetic import generate_synthetic_directional_measurements
from electrostatic_diagnostics.compound_probe.flow import estimate_flow_velocity, calculate_mach_numbers


def test_langmuir_synthetic_is_reproducible():
    a = generate_synthetic_langmuir_iv()
    b = generate_synthetic_langmuir_iv()
    np.testing.assert_allclose(a["current"], b["current"])


def test_floating_potential_zero_crossing():
    voltage = np.array([-1.0, 0.0, 1.0])
    current = np.array([-2.0, 0.0, 2.0])
    assert estimate_floating_potential(voltage, current) == pytest.approx(0.0)


def test_langmuir_model_recovers_known_temperature_and_plasma_potential():
    data = generate_synthetic_langmuir_iv(
        LangmuirSyntheticConfig(noise_std=2e-5, random_seed=42)
    )
    result = fit_langmuir_iv(data["voltage"], data["current"])
    assert result.plasma_potential == pytest.approx(data["plasma_potential"], abs=0.15)
    assert result.electron_temperature_eV == pytest.approx(data["electron_temperature_eV"], rel=0.05)
    vf = estimate_floating_potential(data["voltage"], data["current"])
    assert data["voltage"].min() < vf < data["plasma_potential"]


def test_electric_field_recovers_linear_potential_gradient():
    r = np.linspace(0.0, 0.01, 101)
    phi = 10.0 - 2000.0 * r
    field = electric_field_from_potential(r, phi)
    np.testing.assert_allclose(field, 2000.0, rtol=0, atol=1e-9)


def test_compound_probe_velocity_recovery():
    data = generate_synthetic_directional_measurements()
    result = estimate_flow_velocity(data["directions"], data["measurements_m_s"])
    np.testing.assert_allclose(result["velocity_m_s"][:2], data["true_velocity_m_s"][:2], atol=250.0)
    assert result["rank"] == 3


def test_mach_numbers_are_consistent_with_sound_speed():
    velocity = np.array([17_000.0, 0.0, 0.0])
    result = calculate_mach_numbers(velocity, electron_temperature_eV=6.0, ion_mass_amu=40.0)
    assert result["parallel_mach"] == pytest.approx(velocity[0] / result["sound_speed_m_s"])
    assert result["perpendicular_mach"] == pytest.approx(0.0)


def test_invalid_electric_field_inputs_are_rejected():
    with pytest.raises(ValueError):
        electric_field_from_potential([0.0, 0.0], [1.0, 2.0])
