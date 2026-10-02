"""Synthetic multichannel magnetic (Mirnov-like) diagnostic data.

The generated signals are deliberately synthetic.  Their parameters are
chosen to provide controlled temporal and spatial structure for later PSD,
wavelet, SVD, and mode-analysis workflows; they are not reconstructions of
IR-T1 experimental data.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from core.data_model import MultichannelTimeSeries


@dataclass(frozen=True)
class MirnovSyntheticConfig:
    """Configuration for a synthetic multichannel magnetic dataset.

    Frequencies are in Hz, duration in seconds, and amplitudes are in the
    arbitrary signal unit declared by ``signal_units``.
    """

    n_channels: int = 12
    sampling_frequency: float = 1_000_000.0
    duration: float = 0.010
    dominant_frequency: float = 44_000.0
    secondary_frequency: float = 70_000.0
    secondary_amplitude_ratio: float = 0.30
    amplitude_modulation_frequency: float = 2_000.0
    amplitude_modulation_depth: float = 0.15
    secondary_modulation_depth: float = 0.10
    noise_std: float = 0.08
    phase_span: float = np.pi / 2.0
    secondary_phase_offset: float = np.pi / 5.0
    channel_amplitude_variation: float = 0.15
    signal_units: str = "a.u."
    random_seed: int = 42

    def validate(self) -> None:
        """Validate configuration parameters before data generation."""
        if self.n_channels < 2:
            raise ValueError("n_channels must be at least 2")
        if not np.isfinite(self.sampling_frequency) or self.sampling_frequency <= 0:
            raise ValueError("sampling_frequency must be positive and finite")
        if not np.isfinite(self.duration) or self.duration <= 0:
            raise ValueError("duration must be positive and finite")
        for name, frequency in (
            ("dominant_frequency", self.dominant_frequency),
            ("secondary_frequency", self.secondary_frequency),
            ("amplitude_modulation_frequency", self.amplitude_modulation_frequency),
        ):
            if not np.isfinite(frequency) or frequency < 0:
                raise ValueError(f"{name} must be non-negative and finite")
        if self.dominant_frequency >= self.sampling_frequency / 2:
            raise ValueError("dominant_frequency must be below the Nyquist frequency")
        if self.secondary_frequency >= self.sampling_frequency / 2:
            raise ValueError("secondary_frequency must be below the Nyquist frequency")
        if self.secondary_amplitude_ratio < 0:
            raise ValueError("secondary_amplitude_ratio must be non-negative")
        if not 0 <= self.amplitude_modulation_depth < 1:
            raise ValueError("amplitude_modulation_depth must be in [0, 1)")
        if not 0 <= self.secondary_modulation_depth < 1:
            raise ValueError("secondary_modulation_depth must be in [0, 1)")
        if self.noise_std < 0 or not np.isfinite(self.noise_std):
            raise ValueError("noise_std must be non-negative and finite")
        if not np.isfinite(self.phase_span):
            raise ValueError("phase_span must be finite")
        if self.channel_amplitude_variation < 0 or not np.isfinite(self.channel_amplitude_variation):
            raise ValueError("channel_amplitude_variation must be non-negative and finite")
        if not isinstance(self.random_seed, (int, np.integer)):
            raise ValueError("random_seed must be an integer")


def generate_synthetic_mirnov_dataset(
    config: MirnovSyntheticConfig | None = None,
) -> MultichannelTimeSeries:
    """Generate a reproducible synthetic Mirnov-like dataset.

    The model combines a dominant oscillation, a secondary oscillation,
    slowly varying amplitudes, controlled channel-to-channel amplitude and
    phase structure, and independent Gaussian measurement noise.

    Returns
    -------
    MultichannelTimeSeries
        Data with shape ``(channels, time)`` and metadata explicitly marking
        the dataset as synthetic.

    Notes
    -----
    The 44 kHz default is motivated by the characteristic frequency range
    reported in the project's IR-T1 scientific reference, but the generated
    dataset is not experimental IR-T1 data and does not reproduce a published
    shot or measurement.
    """
    if config is None:
        config = MirnovSyntheticConfig()
    config.validate()

    n_samples = int(round(config.duration * config.sampling_frequency))
    if n_samples < 2:
        raise ValueError("duration and sampling_frequency must produce at least two samples")

    # Endpoint-excluded time base: exactly n_samples at the requested rate.
    time = np.arange(n_samples, dtype=float) / config.sampling_frequency

    rng = np.random.default_rng(config.random_seed)
    channel_index = np.arange(config.n_channels, dtype=float)
    channel_position = np.linspace(-1.0, 1.0, config.n_channels)

    # Controlled spatial structure: smooth amplitude profile and phase
    # progression across channels, rather than independent random channels.
    primary_amplitudes = 1.0 + config.channel_amplitude_variation * np.cos(
        np.pi * channel_position
    )
    primary_phases = config.phase_span * channel_position
    secondary_phases = primary_phases + config.secondary_phase_offset

    primary_envelope = 1.0 + config.amplitude_modulation_depth * np.sin(
        2.0 * np.pi * config.amplitude_modulation_frequency * time
    )
    secondary_envelope = 1.0 + config.secondary_modulation_depth * np.cos(
        2.0 * np.pi * config.amplitude_modulation_frequency * time
    )

    primary = primary_amplitudes[:, None] * primary_envelope[None, :] * np.sin(
        2.0 * np.pi * config.dominant_frequency * time[None, :] + primary_phases[:, None]
    )
    secondary = (
        config.secondary_amplitude_ratio
        * primary_amplitudes[:, None]
        * secondary_envelope[None, :]
        * np.sin(
            2.0 * np.pi * config.secondary_frequency * time[None, :]
            + secondary_phases[:, None]
        )
    )
    noise = config.noise_std * rng.standard_normal((config.n_channels, n_samples))
    data = primary + secondary + noise

    channel_names = [f"mirnov_{i + 1:02d}" for i in range(config.n_channels)]
    metadata = {
        "data_type": "synthetic",
        "diagnostic": "magnetic",
        "diagnostic_model": "Mirnov-like",
        "synthetic_model": "two_frequency_multichannel_oscillation",
        "scientific_status": "synthetic_demonstration",
        "signal_units": config.signal_units,
        "frequency_components_hz": {
            "dominant": config.dominant_frequency,
            "secondary": config.secondary_frequency,
        },
        "spatial_structure": {
            "amplitude_profile": "smooth_cosine_profile",
            "primary_phase_profile": "linear_across_channels",
            "secondary_phase_offset_rad": config.secondary_phase_offset,
        },
        "note": (
            "Synthetic data for reproducible method development; not original "
            "IR-T1 experimental data and not an experimental reconstruction."
        ),
    }
    analysis_metadata = {
        "generation": {
            "n_channels": config.n_channels,
            "duration_s": config.duration,
            "sampling_frequency_hz": config.sampling_frequency,
            "amplitude_modulation_frequency_hz": config.amplitude_modulation_frequency,
            "amplitude_modulation_depth": config.amplitude_modulation_depth,
            "secondary_modulation_depth": config.secondary_modulation_depth,
            "secondary_amplitude_ratio": config.secondary_amplitude_ratio,
            "noise_std": config.noise_std,
            "phase_span_rad": config.phase_span,
            "channel_amplitude_variation": config.channel_amplitude_variation,
        }
    }
    reproducibility = {
        "random_seed": int(config.random_seed),
        "random_generator": "numpy.random.default_rng",
    }

    return MultichannelTimeSeries(
        data=data,
        time=time,
        sampling_frequency=config.sampling_frequency,
        channel_names=channel_names,
        units=[config.signal_units] * config.n_channels,
        metadata=metadata,
        analysis_metadata=analysis_metadata,
        reproducibility=reproducibility,
    )
