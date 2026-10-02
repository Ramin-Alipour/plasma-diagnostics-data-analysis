import numpy as np
import pytest

from core.data_model import MultichannelTimeSeries, TimeSeries


def test_time_series_accepts_valid_data():
    fs = 1_000.0
    time = np.arange(100) / fs
    signal = np.sin(2 * np.pi * 10 * time)
    ts = TimeSeries(signal, time, sampling_frequency=fs, units="V", name="test")

    assert ts.n_samples == 100
    assert ts.is_uniformly_sampled
    assert ts.inferred_sampling_frequency == pytest.approx(fs)
    ts.validate_sampling_frequency()


def test_multichannel_orientation_and_metadata():
    fs = 10_000.0
    time = np.arange(200) / fs
    data = np.vstack([np.sin(2 * np.pi * 100 * time), np.cos(2 * np.pi * 100 * time)])
    dataset = MultichannelTimeSeries(
        data=data,
        time=time,
        sampling_frequency=fs,
        channel_names=["ch_1", "ch_2"],
        units=["T", "T"],
        metadata={"diagnostic": "synthetic magnetic"},
        reproducibility={"random_seed": 42},
    )

    assert dataset.shape == (2, 200)
    assert dataset.n_channels == 2
    assert dataset.n_samples == 200
    assert dataset.channel_names == ["ch_1", "ch_2"]
    assert dataset.metadata["diagnostic"] == "synthetic magnetic"
    assert dataset.reproducibility["random_seed"] == 42
    dataset.validate_sampling_frequency()


def test_multichannel_channel_accessor():
    time = np.arange(10) / 100.0
    data = np.vstack([np.arange(10), np.arange(10) + 10])
    dataset = MultichannelTimeSeries(data, time, sampling_frequency=100.0, channel_names=["a", "b"], units=["V", "V"])

    channel = dataset.channel(1)
    assert isinstance(channel, TimeSeries)
    assert channel.name == "b"
    np.testing.assert_array_equal(channel.data, data[1])


def test_invalid_time_length_is_rejected():
    with pytest.raises(ValueError, match="same length"):
        TimeSeries(np.zeros(10), np.arange(9), sampling_frequency=1.0)


def test_invalid_multichannel_shape_is_rejected():
    with pytest.raises(ValueError, match=r"shape \(channels, time\)"):
        MultichannelTimeSeries(np.zeros(10), np.arange(10), sampling_frequency=1.0)


def test_invalid_sampling_frequency_is_rejected():
    with pytest.raises(ValueError, match="positive finite"):
        TimeSeries(np.zeros(10), np.arange(10), sampling_frequency=0.0)


def test_inconsistent_sampling_frequency_can_be_detected():
    time = np.arange(100) / 1_000.0
    ts = TimeSeries(np.zeros(100), time, sampling_frequency=900.0)

    with pytest.raises(ValueError, match="inconsistent"):
        ts.validate_sampling_frequency()


def test_nonuniform_time_axis_is_representable_but_not_uniform():
    time = np.array([0.0, 0.001, 0.002, 0.004, 0.005])
    ts = TimeSeries(np.arange(5), time)

    assert not ts.is_uniformly_sampled
    assert ts.inferred_sampling_frequency is None


def test_nan_data_can_represent_missing_samples():
    time = np.arange(5) / 100.0
    ts = TimeSeries(np.array([0.0, np.nan, 1.0, 2.0, 3.0]), time)
    assert np.isnan(ts.data[1])

