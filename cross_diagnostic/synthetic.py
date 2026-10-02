"""Synthetic paired signals for the unified cross-diagnostic workflow."""
from __future__ import annotations
import numpy as np
from core.data_model import TimeSeries
from hard_xray.synthetic import generate_hxr_time_series
from synthetic_data.magnetic.mirnov import generate_synthetic_mirnov_dataset
from turbulence_transport.fluctuations.synthetic import generate_synthetic_fluctuations


def magnetic_hxr_pair():
    """Return a synthetic Mirnov-like aggregate and HXR signal with different rates."""
    mag = generate_synthetic_mirnov_dataset()
    magnetic = TimeSeries(np.mean(mag.data, axis=0), mag.time, mag.sampling_frequency,
                          "a.u.", "magnetic_fluctuation", {"data_type":"synthetic","diagnostic":"magnetic"},
                          {}, dict(mag.reproducibility))
    hxr = generate_hxr_time_series(sampling_frequency_hz=800_000.0, duration_s=0.01, modulation_frequency_hz=44_000.0)
    xray = TimeSeries(hxr.counts, hxr.time_s, hxr.sampling_frequency_hz, "counts", "hxr_counts", hxr.metadata)
    return magnetic, xray


def electrostatic_turbulence_pair():
    """Return synthetic electrostatic potential and turbulence-density signals.

    The radial velocity is a controlled synthetic velocity fluctuation derived
    from a phase-shifted common oscillatory component; it is not an experimental
    measurement or an inferred IR-T1 quantity.
    """
    d = generate_synthetic_fluctuations()
    potential = TimeSeries(d["potential_fluctuation_V"], d["time_s"], d["sampling_frequency_hz"],
                           "V", "electrostatic_potential_fluctuation", {"data_type":"synthetic","diagnostic":"electrostatic"})
    density = TimeSeries(d["density_fluctuation_m3"], d["time_s"], d["sampling_frequency_hz"],
                         "m^-3", "density_fluctuation", {"data_type":"synthetic","diagnostic":"turbulence"})
    phase = 0.8
    velocity = 1.5e3 * (np.sin(2*np.pi*12_000*d["time_s"] + phase) + 0.35*np.sin(2*np.pi*27_000*d["time_s"] + 0.3 + phase))
    velocity += np.random.default_rng(42).normal(0, 60.0, d["time_s"].size)
    v = TimeSeries(velocity, d["time_s"], d["sampling_frequency_hz"], "m/s", "radial_velocity_fluctuation",
                   {"data_type":"synthetic","diagnostic":"turbulence","velocity_model":"controlled_synthetic"})
    return potential, density, v
