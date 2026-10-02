"""Publication-grounded synthetic reconstructions for the six IR-T1 papers.

The functions in this module never claim to recover original raw measurements.
They generate deterministic synthetic/raw-like measurements constrained by
quantities explicitly reported in the publications.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "publication_reconstruction"


def load_constraints(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name)


def reconstruct_paper1(seed: int = 1):
    """Synthetic spectra constrained by the reported wavelength/FWHM/Ti table."""
    df = load_constraints("paper1_spectroscopy.csv")
    rng = np.random.default_rng(seed)
    spectra = []
    for row in df.itertuples(index=False):
        x = np.linspace(row.wavelength_nm - 0.35, row.wavelength_nm + 0.35, 401)
        sigma = row.measured_fwhm_nm / 2.354820045
        amp = 1.0 + 0.05 * rng.normal()
        y = amp * np.exp(-0.5 * ((x-row.wavelength_nm)/sigma)**2)
        y += 0.015 * rng.normal(size=x.size)
        spectra.append((row.ion, x, y, row.measured_fwhm_nm, row.resolution_fwhm_nm))
    return df, spectra


def reconstruct_paper2(seed: int = 2, samples_per_window: int = 12000):
    """Reconstruct HXR event energies and 12-channel mode-controlled Mirnov data."""
    hxr = load_constraints("paper2_hxr.csv")
    rng = np.random.default_rng(seed)
    hxr_events = []
    # A truncated normal is used only to match count and reported mean; the
    # width is an explicit synthetic assumption, not a recovered spectrum.
    widths = np.array([180, 180, 180, 190, 210, 230.])
    for row, width in zip(hxr.itertuples(index=False), widths):
        e = rng.normal(row.mean_energy_keV, width, int(row.total_counts))
        e = np.clip(e, 5, 1000)
        e += row.mean_energy_keV - e.mean()
        e = np.clip(e, 5, 1000)
        e += row.mean_energy_keV - e.mean()
        hxr_events.append((row.time_start_ms, row.time_end_ms, e))

    modes = load_constraints("paper2_modes.csv")
    t = np.linspace(0, 32e-3, samples_per_window)
    signals = np.zeros((12, t.size))
    # Orthogonal spatial Fourier patterns are used so the target mode-energy
    # fractions are directly encoded in the synthetic measurement.
    theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for _, row in modes.iterrows():
        start = int(np.searchsorted(t, row.time_start_ms/1000))
        end = int(np.searchsorted(t, row.time_end_ms/1000))
        tt = t[start:end]
        if tt.size < 2: continue
        segment = np.zeros((12, tt.size))
        fractions = np.array([row[f"m{i}_pct"] for i in range(1,7)]) / 100.0
        mode_freqs = {1:11_000, 2:22_000, 3:44_000, 4:55_000, 5:66_000, 6:77_000}
        for m, frac in enumerate(fractions, start=1):
            spatial = np.cos(m*theta)
            temporal = np.sin(2*np.pi*mode_freqs[m]*tt)
            segment += np.sqrt(max(frac,0.0)) * spatial[:,None] * temporal[None,:]
        # Tiny numerical noise prevents an unrealistically perfect matrix while
        # preserving the publication-reported modal energy fractions.
        segment += 1e-7 * rng.normal(size=segment.shape)
        signals[:, start:end] = segment
    return hxr, hxr_events, modes, t, signals


def reconstruct_paper3(seed: int = 3, n: int = 3000):
    """Synthetic compound-probe saturation currents constrained by the paper."""
    meta = load_constraints("paper3_compound_probe.csv")
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 30e-3, n)
    # Synthetic Mach trajectory: not reported numerically in the paper.
    mach_true = 0.45 + 0.18*np.sin(2*np.pi*140*t) + 0.04*np.sin(2*np.pi*700*t)
    k = 1.7
    base = 1.0
    ratio = np.exp(k*mach_true)
    i_down = base*(1+0.03*np.sin(2*np.pi*30*t))
    i_up = i_down*ratio
    i_up *= 1 + 0.01*rng.normal(size=n)
    i_down *= 1 + 0.01*rng.normal(size=n)
    mach_recovered = np.log(np.maximum(i_up,1e-12)/np.maximum(i_down,1e-12))/k
    return meta, t, i_up, i_down, mach_true, mach_recovered


def reconstruct_paper4(seed: int = 4, n: int = 3200):
    """Synthetic E-field/transport traces matching publication summary ranges."""
    df = load_constraints("paper4_pressure_transport.csv")
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 32e-3, n)
    outputs = []
    for row in df.itertuples(index=False):
        # E-field traces are generated from a target transport proxy. The exact
        # shape is synthetic; only the reported summary ranges are constrained.
        base_r = row.radial_transport_no_bias
        base_p = row.poloidal_transport_no_bias
        osc = np.sin(2*np.pi*1_200*t) + 0.4*np.sin(2*np.pi*4_800*t)
        er = 350*np.sin(2*np.pi*1_200*t) + 80*rng.normal(size=n)
        ep = 120*np.sin(2*np.pi*1_200*t+0.5) + 40*rng.normal(size=n)
        # Scale velocity-like synthetic fluctuations to reported transport levels.
        vr = np.sqrt(abs(base_r))*osc
        vp = np.sqrt(abs(base_p))*(0.75*osc + 0.25*np.sin(2*np.pi*2_300*t))
        outputs.append(dict(pressure_Torr=row.pressure_Torr, time_s=t, Er_V_m=er, Etheta_V_m=ep,
                            radial_transport=vr, poloidal_transport=vp,
                            target_radial=(row.radial_transport_no_bias,row.radial_transport_plus200,row.radial_transport_minus200),
                            target_poloidal=(row.poloidal_transport_no_bias,row.poloidal_transport_plus200,row.poloidal_transport_minus200)))
    return df, outputs


def reconstruct_paper5(seed: int = 5, n: int = 2000):
    """Synthetic limiter-position/bias traces constrained by reported effects."""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 32e-3, n)
    scenarios = []
    for pos in (0,5,10):
        for bias in (-200,0,200):
            scale = 1.0
            if bias == 200 and pos == 0: scale = 0.50
            elif bias == 200 and pos == 5: scale = 0.65
            elif bias == 200 and pos == 10: scale = 0.95
            elif bias == -200 and pos in (5,10): scale = 1.25
            fluct = 1 + 0.18*np.sin(2*np.pi*700*t) + 0.08*rng.normal(size=n)
            radial = np.maximum(0, 0.01*scale*fluct)
            poloidal = np.maximum(0, 0.012*(1 + (0.3 if bias==200 else 0))*fluct)
            scenarios.append(dict(position_mm=pos, bias_V=bias, time_s=t, radial_transport=radial,
                                  poloidal_transport=poloidal, target_scale=scale))
    return scenarios


def reconstruct_paper6(seed: int = 6, samples_per_window: int = 5000):
    """Synthetic 12-Mirnov datasets for the three reported hydrogen pressures."""
    df = load_constraints("paper6_pressure_mhd.csv")
    rng = np.random.default_rng(seed)
    theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
    windows = [(25,26),(35,36),(45,46)]
    out=[]
    for row in df.itertuples(index=False):
        t=np.linspace(0,50e-3,samples_per_window)
        x=np.zeros((12,t.size))
        amp={1.9:1.0,2.5:0.65,2.9:1.15}[row.pressure_Torr]
        for m in (1,2,3):
            temporal=np.sin(2*np.pi*44_000*t + 0.3*m)
            spatial=np.cos(m*theta)
            x += amp*(0.8 if m==3 else 0.35)*spatial[:,None]*temporal[None,:]
        x += 0.08*rng.normal(size=x.shape)
        out.append(dict(pressure_Torr=row.pressure_Torr,time_s=t,mirnov=x,target_frequency_kHz=44.0,
                        steady_state_ms=row.steady_state_ms,windows_ms=windows))
    return df,out
