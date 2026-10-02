import numpy as np
import pytest

from synthetic_data.magnetic.mirnov import (
    MirnovSyntheticConfig,
    generate_synthetic_mirnov_dataset,
)


def test_default_dataset_shape_and_time_base():
    dataset = generate_synthetic_mirnov_dataset()

    assert dataset.shape == (12, 10_000)
    assert dataset.sampling_frequency == pytest.approx(1_000_000.0)
    assert dataset.time[0] == pytest.approx(0.0)
    assert dataset.time[-1] == pytest.approx(0.009999)
    assert dataset.duration == pytest.approx(0.009999)
    dataset.validate_sampling_frequency()


def test_default_dataset_metadata_marks_synthetic_data():
    dataset = generate_synthetic_mirnov_dataset()

    assert dataset.metadata["data_type"] == "synthetic"
    assert dataset.metadata["diagnostic"] == "magnetic"
    assert dataset.metadata["diagnostic_model"] == "Mirnov-like"
    assert dataset.units == ["a.u."] * 12
    assert dataset.channel_names == [f"mirnov_{i:02d}" for i in range(1, 13)]


def test_same_seed_reproduces_identical_data():
    first = generate_synthetic_mirnov_dataset(MirnovSyntheticConfig(random_seed=123))
    second = generate_synthetic_mirnov_dataset(MirnovSyntheticConfig(random_seed=123))

    np.testing.assert_array_equal(first.data, second.data)


def test_different_seed_changes_noise_realization():
    first = generate_synthetic_mirnov_dataset(MirnovSyntheticConfig(random_seed=123))
    second = generate_synthetic_mirnov_dataset(MirnovSyntheticConfig(random_seed=124))

    assert not np.array_equal(first.data, second.data)


def test_channels_have_controlled_spatial_structure():
    dataset = generate_synthetic_mirnov_dataset(
        MirnovSyntheticConfig(noise_std=0.0, secondary_amplitude_ratio=0.0)
    )

    # With no noise and one frequency, channels remain distinct but coherent.
    assert not np.array_equal(dataset.data[0], dataset.data[-1])
    assert np.max(np.abs(dataset.data)) > 0.0


def test_configuration_is_respected():
    config = MirnovSyntheticConfig(
        n_channels=6,
        sampling_frequency=500_000.0,
        duration=0.004,
        dominant_frequency=30_000.0,
        secondary_frequency=60_000.0,
        noise_std=0.02,
        random_seed=7,
    )
    dataset = generate_synthetic_mirnov_dataset(config)

    assert dataset.shape == (6, 2_000)
    assert dataset.metadata["frequency_components_hz"]["dominant"] == 30_000.0
    assert dataset.metadata["frequency_components_hz"]["secondary"] == 60_000.0
    assert dataset.reproducibility["random_seed"] == 7


def test_invalid_frequency_above_nyquist_is_rejected():
    config = MirnovSyntheticConfig(sampling_frequency=100_000.0, dominant_frequency=60_000.0)

    with pytest.raises(ValueError, match="Nyquist"):
        generate_synthetic_mirnov_dataset(config)
