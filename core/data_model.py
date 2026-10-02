"""Common scientific data models for time-series diagnostic data.

The repository-wide convention for multichannel time-series data is
``(channels, time)``.  The classes in this module are intentionally
agnostic to any particular diagnostic so that spectroscopy, magnetic,
electrostatic, turbulence/transport, and hard-X-ray workflows can share the
same basic data contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class TimeSeries:
    """Represent one uniformly or non-uniformly sampled scalar time series.

    Parameters
    ----------
    data:
        One-dimensional numerical samples.
    time:
        One-dimensional time axis with the same length as ``data``.
    sampling_frequency:
        Sampling frequency in Hz.  Required for workflows that assume a
        uniform sampling rate, but stored explicitly when known.
    units:
        Physical unit of ``data``.  Use a descriptive string such as ``"V"``
        or ``"a.u."``.  The time axis is assumed to be expressed in seconds.
    name:
        Optional signal name.
    metadata:
        General scientific metadata.  Diagnostic-specific information may be
        stored here without coupling the core model to a specific diagnostic.
    analysis_metadata:
        Parameters or provenance associated with an analysis step.
    reproducibility:
        Reproducibility information such as a random seed or generator
        configuration when relevant.
    """

    data: np.ndarray
    time: np.ndarray
    sampling_frequency: float | None = None
    units: str = ""
    name: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    analysis_metadata: dict[str, Any] = field(default_factory=dict)
    reproducibility: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.data = np.asarray(self.data, dtype=float)
        self.time = np.asarray(self.time, dtype=float)
        self.metadata = dict(self.metadata)
        self.analysis_metadata = dict(self.analysis_metadata)
        self.reproducibility = dict(self.reproducibility)
        self._validate()

    def _validate(self) -> None:
        if self.data.ndim != 1:
            raise ValueError("data must be a one-dimensional array")
        if self.time.ndim != 1:
            raise ValueError("time must be a one-dimensional array")
        if self.data.size == 0:
            raise ValueError("data must contain at least one sample")
        if self.time.size != self.data.size:
            raise ValueError("time and data must have the same length")
        if np.any(np.isinf(self.data)):
            raise ValueError("data must not contain infinite values")
        if not np.all(np.isfinite(self.time)):
            raise ValueError("time must contain only finite values")
        if self.time.size > 1 and np.any(np.diff(self.time) <= 0):
            raise ValueError("time must be strictly increasing")
        if self.sampling_frequency is not None:
            if not np.isfinite(self.sampling_frequency) or self.sampling_frequency <= 0:
                raise ValueError("sampling_frequency must be a positive finite value")

    @property
    def n_samples(self) -> int:
        """Number of samples in the time series."""
        return self.data.size

    @property
    def duration(self) -> float:
        """Elapsed duration represented by the time axis, in seconds."""
        if self.n_samples < 2:
            return 0.0
        return float(self.time[-1] - self.time[0])

    @property
    def inferred_sampling_frequency(self) -> float | None:
        """Infer the sampling frequency when the time axis is uniform.

        Returns ``None`` for a single-sample series or a non-uniform time axis.
        """
        if self.n_samples < 2:
            return None
        dt = np.diff(self.time)
        reference = float(np.median(dt))
        if not np.allclose(dt, reference, rtol=1e-9, atol=1e-15):
            return None
        return 1.0 / reference

    @property
    def is_uniformly_sampled(self) -> bool:
        """Whether the time axis has a constant sample interval."""
        return self.inferred_sampling_frequency is not None

    def validate_sampling_frequency(self, *, rtol: float = 1e-6, atol: float = 1e-12) -> None:
        """Validate stored sampling frequency against a uniform time axis.

        Raises
        ------
        ValueError
            If the time axis is not uniformly sampled or the stored sampling
            frequency is inconsistent with the time axis.
        """
        if self.sampling_frequency is None:
            raise ValueError("sampling_frequency is not defined")
        inferred = self.inferred_sampling_frequency
        if inferred is None:
            raise ValueError("time axis is not uniformly sampled")
        if not np.isclose(self.sampling_frequency, inferred, rtol=rtol, atol=atol):
            raise ValueError(
                "sampling_frequency is inconsistent with the time axis: "
                f"stored={self.sampling_frequency:g} Hz, inferred={inferred:g} Hz"
            )


@dataclass
class MultichannelTimeSeries:
    """Represent multiple synchronized time-series channels.

    The required repository-wide orientation is ``(channels, time)``.

    The common time-axis convention is seconds, so ``sampling_frequency`` is
    expressed in Hz.
    ``channel_names`` and ``units`` are aligned with the first dimension.
    """

    data: np.ndarray
    time: np.ndarray
    sampling_frequency: float | None = None
    channel_names: list[str] = field(default_factory=list)
    units: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    analysis_metadata: dict[str, Any] = field(default_factory=dict)
    reproducibility: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.data = np.asarray(self.data, dtype=float)
        self.time = np.asarray(self.time, dtype=float)
        self.channel_names = list(self.channel_names)
        self.units = list(self.units)
        self.metadata = dict(self.metadata)
        self.analysis_metadata = dict(self.analysis_metadata)
        self.reproducibility = dict(self.reproducibility)
        self._validate()

    def _validate(self) -> None:
        if self.data.ndim != 2:
            raise ValueError("data must be a two-dimensional array with shape (channels, time)")
        if self.data.shape[0] == 0 or self.data.shape[1] == 0:
            raise ValueError("data must contain at least one channel and one sample")
        if self.time.ndim != 1:
            raise ValueError("time must be a one-dimensional array")
        if self.data.shape[1] != self.time.size:
            raise ValueError("data.shape[1] must equal len(time)")
        if np.any(np.isinf(self.data)):
            raise ValueError("data must not contain infinite values")
        if not np.all(np.isfinite(self.time)):
            raise ValueError("time must contain only finite values")
        if self.time.size > 1 and np.any(np.diff(self.time) <= 0):
            raise ValueError("time must be strictly increasing")
        if self.sampling_frequency is not None:
            if not np.isfinite(self.sampling_frequency) or self.sampling_frequency <= 0:
                raise ValueError("sampling_frequency must be a positive finite value")
        n_channels = self.data.shape[0]
        if self.channel_names and len(self.channel_names) != n_channels:
            raise ValueError("channel_names length must match the number of channels")
        if self.units and len(self.units) != n_channels:
            raise ValueError("units length must match the number of channels")

        if not self.channel_names:
            self.channel_names = [f"channel_{i}" for i in range(n_channels)]
        if not self.units:
            self.units = ["" for _ in range(n_channels)]

    @property
    def n_channels(self) -> int:
        """Number of channels."""
        return self.data.shape[0]

    @property
    def n_samples(self) -> int:
        """Number of time samples per channel."""
        return self.data.shape[1]

    @property
    def shape(self) -> tuple[int, int]:
        """Data shape as ``(channels, time)``."""
        return self.data.shape

    @property
    def duration(self) -> float:
        """Elapsed duration represented by the time axis, in seconds."""
        if self.n_samples < 2:
            return 0.0
        return float(self.time[-1] - self.time[0])

    @property
    def inferred_sampling_frequency(self) -> float | None:
        """Infer sampling frequency when all channels share a uniform time axis."""
        if self.n_samples < 2:
            return None
        dt = np.diff(self.time)
        reference = float(np.median(dt))
        if not np.allclose(dt, reference, rtol=1e-9, atol=1e-15):
            return None
        return 1.0 / reference

    @property
    def is_uniformly_sampled(self) -> bool:
        """Whether the shared time axis has a constant sample interval."""
        return self.inferred_sampling_frequency is not None

    def validate_sampling_frequency(self, *, rtol: float = 1e-6, atol: float = 1e-12) -> None:
        """Validate stored sampling frequency against the shared time axis."""
        if self.sampling_frequency is None:
            raise ValueError("sampling_frequency is not defined")
        inferred = self.inferred_sampling_frequency
        if inferred is None:
            raise ValueError("time axis is not uniformly sampled")
        if not np.isclose(self.sampling_frequency, inferred, rtol=rtol, atol=atol):
            raise ValueError(
                "sampling_frequency is inconsistent with the time axis: "
                f"stored={self.sampling_frequency:g} Hz, inferred={inferred:g} Hz"
            )

    def channel(self, index: int) -> TimeSeries:
        """Return one channel as a :class:`TimeSeries` object."""
        return TimeSeries(
            data=self.data[index],
            time=self.time,
            sampling_frequency=self.sampling_frequency,
            units=self.units[index],
            name=self.channel_names[index],
            metadata={**self.metadata, "channel_index": index},
            analysis_metadata=dict(self.analysis_metadata),
            reproducibility=dict(self.reproducibility),
        )
