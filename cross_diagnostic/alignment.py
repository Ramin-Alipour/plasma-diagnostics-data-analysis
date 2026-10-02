"""Explicit time-base alignment for cross-diagnostic analysis."""
from __future__ import annotations
import numpy as np
from scipy.signal import resample_poly
from fractions import Fraction
from plasma_core.data_model import TimeSeries


def _validate_target_time(target_time):
    t = np.asarray(target_time, dtype=float)
    if t.ndim != 1 or t.size < 2 or np.any(~np.isfinite(t)) or np.any(np.diff(t) <= 0):
        raise ValueError("target_time must be finite, strictly increasing, and contain at least two samples")
    return t


def interpolate_to_time(signal: TimeSeries, target_time, *, method: str = "linear") -> TimeSeries:
    """Interpolate a time series onto an explicitly supplied time grid.

    This operation does not choose the target grid automatically. Values outside
    the original time interval are rejected rather than extrapolated.
    """
    if method != "linear":
        raise ValueError("method must be 'linear' in the initial implementation")
    target = _validate_target_time(target_time)
    if target[0] < signal.time[0] or target[-1] > signal.time[-1]:
        raise ValueError("target_time must lie within the original time interval")
    data = np.interp(target, signal.time, signal.data)
    fs = signal.sampling_frequency if signal.is_uniformly_sampled else None
    inferred = 1.0 / np.median(np.diff(target))
    metadata = dict(signal.metadata)
    metadata["time_transform"] = "linear_interpolation"
    analysis = dict(signal.analysis_metadata)
    analysis["interpolation_method"] = method
    analysis["target_sampling_frequency_hz"] = float(inferred)
    return TimeSeries(data, target, inferred if np.allclose(np.diff(target), np.diff(target)[0]) else fs,
                      signal.units, signal.name, metadata, analysis, dict(signal.reproducibility))


def resample_time_series(signal: TimeSeries, target_sampling_frequency_hz: float) -> TimeSeries:
    """Resample a uniformly sampled series to an explicit target rate.

    Polyphase resampling is used, providing anti-alias filtering. The output
    starts at the original first sample and uses the target sampling interval.
    """
    target_fs = float(target_sampling_frequency_hz)
    if not np.isfinite(target_fs) or target_fs <= 0:
        raise ValueError("target_sampling_frequency_hz must be positive and finite")
    if not signal.is_uniformly_sampled:
        raise ValueError("resample_time_series requires a uniformly sampled input")
    source_fs = float(signal.inferred_sampling_frequency)
    ratio = Fraction(target_fs / source_fs).limit_denominator(10000)
    data = resample_poly(signal.data, ratio.numerator, ratio.denominator)
    target_time = signal.time[0] + np.arange(data.size) / target_fs
    max_time = signal.time[-1]
    keep = target_time <= max_time + 0.5 / target_fs
    data = data[keep]
    target_time = target_time[keep]
    metadata = dict(signal.metadata)
    metadata["time_transform"] = "polyphase_resampling"
    analysis = dict(signal.analysis_metadata)
    analysis.update({"source_sampling_frequency_hz": source_fs,
                     "target_sampling_frequency_hz": target_fs,
                     "resampling_ratio": [ratio.numerator, ratio.denominator]})
    return TimeSeries(data, target_time, target_fs, signal.units, signal.name, metadata, analysis,
                      dict(signal.reproducibility))


def align_time_series(a: TimeSeries, b: TimeSeries, *, target_sampling_frequency_hz: float | None = None,
                      interpolation_method: str = "linear") -> tuple[TimeSeries, TimeSeries]:
    """Align two scalar time series on their temporal overlap.

    If sampling frequencies differ, an explicit target rate is required. If
    supplied, both signals are resampled to that rate before overlap trimming.
    No implicit resampling is performed.
    """
    if not a.is_uniformly_sampled or not b.is_uniformly_sampled:
        raise ValueError("both signals must be uniformly sampled for alignment")
    fsa = float(a.inferred_sampling_frequency); fsb = float(b.inferred_sampling_frequency)
    if target_sampling_frequency_hz is None:
        if not np.isclose(fsa, fsb, rtol=1e-9, atol=1e-9):
            raise ValueError("sampling frequencies differ; provide target_sampling_frequency_hz explicitly")
        aa, bb = a, b
    else:
        aa = resample_time_series(a, target_sampling_frequency_hz)
        bb = resample_time_series(b, target_sampling_frequency_hz)
    start = max(aa.time[0], bb.time[0]); stop = min(aa.time[-1], bb.time[-1])
    if stop <= start:
        raise ValueError("signals have no overlapping time interval")
    fs = float(aa.inferred_sampling_frequency)
    n = int(np.floor((stop - start) * fs)) + 1
    common_time = start + np.arange(n) / fs
    common_time = common_time[common_time <= stop + 1e-12]
    if common_time.size < 3:
        raise ValueError("overlap contains fewer than three common samples")
    out_a = interpolate_to_time(aa, common_time, method=interpolation_method)
    out_b = interpolate_to_time(bb, common_time, method=interpolation_method)
    for out, source in ((out_a, a), (out_b, b)):
        out.analysis_metadata["alignment"] = {
            "method": "common_time_grid",
            "overlap_start_s": float(start),
            "overlap_end_s": float(common_time[-1]),
            "target_sampling_frequency_hz": fs,
            "source_sampling_frequency_hz": float(source.inferred_sampling_frequency),
            "explicit_resampling_requested": target_sampling_frequency_hz is not None,
        }
    return out_a, out_b
