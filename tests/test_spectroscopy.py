import numpy as np
import pytest
from spectroscopy.synthetic import generate_synthetic_spectrum
from spectroscopy.calibration.wavelength import calibrate_wavelength
from spectroscopy.line_identification.identification import SpectralLineReference, identify_spectral_lines
from spectroscopy.spectral_fitting.gaussian import fit_gaussian_peak, compute_fwhm
from spectroscopy.doppler_broadening.temperature import doppler_sigma_from_temperature, estimate_doppler_temperature


def test_wavelength_calibration_recovers_linear_mapping():
    pixels = np.array([0., 500., 1000., 1500.])
    wavelengths = 500e-9 + 0.02e-9 * pixels
    result = calibrate_wavelength(pixels, wavelengths, degree=1)
    np.testing.assert_allclose(result.calibrate([250., 750.]), 500e-9 + 0.02e-9*np.array([250.,750.]), rtol=0, atol=1e-20)
    assert result.rms_residual < 1e-20


def test_gaussian_fwhm_relation():
    sigma = 2.0
    assert compute_fwhm(sigma) == pytest.approx(2*np.sqrt(2*np.log(2))*sigma)


def test_synthetic_spectrum_reproducible():
    a = generate_synthetic_spectrum(); b = generate_synthetic_spectrum()
    np.testing.assert_allclose(a.intensity, b.intensity)


def test_line_identification_matches_reference():
    d = generate_synthetic_spectrum(noise_std=0.001)
    ref = SpectralLineReference("Ar", "I", d.line_center, source="synthetic")
    matches = identify_spectral_lines(d.wavelength, d.intensity, [ref], tolerance=0.5e-9, prominence=0.1)
    assert len(matches) == 1


def test_doppler_temperature_round_trip():
    line = 505e-9; temperature = 20.0; mass = 40.0
    sigma = doppler_sigma_from_temperature(line, temperature, mass)
    result = estimate_doppler_temperature(line, sigma, mass)
    assert result["temperature_eV"] == pytest.approx(temperature, rel=1e-12)


def test_known_temperature_validation_from_synthetic_spectrum():
    d = generate_synthetic_spectrum(noise_std=0.0002, baseline_coefficients=(0.0, 0.0))
    half_window = 0.15e-9
    mask = np.abs(d.wavelength - d.line_center) <= half_window
    fit = fit_gaussian_peak(d.wavelength[mask], d.intensity[mask], initial_guess=(1.0, d.line_center, d.doppler_sigma))
    recovered = estimate_doppler_temperature(d.line_center, fit.sigma, d.atomic_mass_amu)
    assert recovered["temperature_eV"] == pytest.approx(d.temperature_eV, rel=0.03)


def test_instrumental_broadening_correction():
    line = 505e-9; temperature = 20.0; mass = 40.0
    sigma_d = doppler_sigma_from_temperature(line, temperature, mass)
    sigma_i = 4e-12
    sigma_obs = np.sqrt(sigma_d**2 + sigma_i**2)
    result = estimate_doppler_temperature(line, sigma_obs, mass, instrumental_sigma=sigma_i)
    assert result["temperature_eV"] == pytest.approx(temperature, rel=1e-12)


def test_instrumental_width_cannot_exceed_observed_width():
    with pytest.raises(ValueError):
        estimate_doppler_temperature(505e-9, 1e-12, 40.0, instrumental_sigma=2e-12)


def test_baseline_subtraction_recovers_linear_baseline():
    from spectroscopy.preprocessing import subtract_baseline
    x = np.linspace(500e-9, 510e-9, 100)
    baseline = 0.2 + 0.3 * np.linspace(-1, 1, 100)
    corrected, fitted, _ = subtract_baseline(x, baseline, degree=1)
    np.testing.assert_allclose(fitted, baseline, rtol=0, atol=1e-12)
    np.testing.assert_allclose(corrected, 0.0, rtol=0, atol=1e-12)
