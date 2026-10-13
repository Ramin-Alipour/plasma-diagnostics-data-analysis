import numpy as np

from magnetic_diagnostics.svd import compute_svd


def test_noise_free_rotating_mode_has_two_equal_svd_components_and_recovers_m():
    n_channels, n_samples = 12, 1024
    fs_hz, f_hz, m_true = 256_000.0, 12_000.0, 2
    theta = 2 * np.pi * np.arange(n_channels) / n_channels
    time_s = np.arange(n_samples) / fs_hz
    signals = np.cos(
        m_true * theta[:, None] - 2 * np.pi * f_hz * time_s[None, :]
    )

    result = compute_svd(signals, center=True, scale=False)
    np.testing.assert_allclose(
        result.singular_values[0], result.singular_values[1], rtol=1e-12, atol=1e-12
    )
    np.testing.assert_allclose(result.explained_energy[:2], [0.5, 0.5], atol=1e-12)

    # Identify the physical spatial mode independently of the arbitrary SVD basis.
    spatial_coefficients = np.fft.fft(signals, axis=0) / n_channels
    mode_power = np.mean(np.abs(spatial_coefficients) ** 2, axis=1)
    recovered_m = int(np.argmax(mode_power[1:n_channels // 2]) + 1)
    assert recovered_m == m_true

    # reconstruct() returns the centered analysis matrix, not the original offset signal.
    offset_signals = signals + np.arange(n_channels)[:, None]
    centered = compute_svd(offset_signals, center=True, scale=False)
    reconstructed = centered.reconstruct(n_components=2)
    np.testing.assert_allclose(reconstructed.mean(axis=1), 0.0, atol=1e-12)
    assert not np.allclose(reconstructed, offset_signals)


def test_centered_constant_matrix_has_finite_zero_energy_fractions():
    data = np.repeat(np.array([[2.0], [-3.0], [7.5]]), 32, axis=1)
    result = compute_svd(data, center=True, scale=False)
    np.testing.assert_allclose(result.singular_values, 0.0, atol=0.0)
    np.testing.assert_allclose(result.explained_energy, 0.0, atol=0.0)
    np.testing.assert_allclose(result.cumulative_energy, 0.0, atol=0.0)
    assert np.all(np.isfinite(result.explained_energy))
