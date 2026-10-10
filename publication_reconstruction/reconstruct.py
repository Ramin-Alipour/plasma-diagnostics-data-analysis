"""Publication-grounded synthetic reconstructions for the six IR-T1 papers.

The functions in this module never claim to recover original raw measurements.
They generate deterministic synthetic/raw-like measurements constrained by
quantities explicitly reported in the publications.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

PACKAGE_DATA = Path(__file__).resolve().parent / "data"
DATA = PACKAGE_DATA / "publication_reconstruction"


def load_constraints(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name)


def reconstruct_paper1():
    df = load_constraints("paper1_spectroscopy.csv")
    # The reconstructed spectra are synthetic; reported constraints are retained.
    return df, df[["wavelength_nm", "reported_temperature_eV"]].copy()


def reconstruct_paper2(seed: int = 2, n: int = 1200):
    df = load_constraints("paper2_hxr.csv")
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 30e-3, n)
    counts = rng.poisson(0.1, size=n)
    for row in df.itertuples(index=False):
        lo, hi = int(row.time_start_ms / 30 * n), int(row.time_end_ms / 30 * n)
        counts[lo:hi] += rng.poisson(max(row.total_counts / max(hi-lo, 1), 0.01), size=max(hi-lo, 0))
    return df, pd.DataFrame({"time_s": t, "counts": counts})


def reconstruct_paper3(seed: int = 3, n: int = 3000):
    df = load_constraints("paper3_compound_probe.csv")
    rng = np.random.default_rng(seed)
    x = np.linspace(-0.01, 0.01, n)
    current = np.exp(-(x / 0.004) ** 2) + 0.02 * rng.normal(size=n)
    return df, pd.DataFrame({"position_m": x, "current_A": current})


def reconstruct_paper4(seed: int = 4, n: int = 3200):
    """Synthetic E-field/transport traces matching publication summary ranges."""
    df = load_constraints("paper4_pressure_transport.csv")
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 32e-3, n)
    outputs = []
    for row in df.itertuples(index=False):
        osc = np.sin(2*np.pi*1200*t) + 0.4*np.sin(2*np.pi*4800*t)
        er = 350*np.sin(2*np.pi*1200*t) + 80*rng.normal(size=n)
        ep = 120*np.sin(2*np.pi*1200*t+0.5) + 40*rng.normal(size=n)
        vr = np.sqrt(abs(row.radial_transport_no_bias))*osc
        vp = np.sqrt(abs(row.poloidal_transport_no_bias))*(0.75*osc + 0.25*np.sin(2*np.pi*2300*t))
        outputs.append(dict(pressure_Torr=row.pressure_Torr, time_s=t, Er_V_m=er, Etheta_V_m=ep,
                            radial_transport=vr, poloidal_transport=vp,
                            target_radial=(row.radial_transport_no_bias,row.radial_transport_plus200,row.radial_transport_minus200),
                            target_poloidal=(row.poloidal_transport_no_bias,row.poloidal_transport_plus200,row.poloidal_transport_minus200)))
    return df, outputs


def reconstruct_paper5(seed: int = 5, n: int = 2000):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 32e-3, n)
    scenarios = []
    for pos in (0, 5, 10):
        for bias in (-200, 0, 200):
            scale = 1.0
            if bias == 200 and pos == 0: scale = 0.50
            elif bias == 200 and pos == 5: scale = 0.65
            elif bias == 200 and pos == 10: scale = 0.95
            elif bias == -200 and pos in (5,10): scale = 1.25
            fluct = 1 + 0.18*np.sin(2*np.pi*700*t) + 0.08*rng.normal(size=n)
            scenarios.append(dict(position_mm=pos,bias_V=bias,time_s=t,radial_transport=np.maximum(0,0.01*scale*fluct),
                                  poloidal_transport=np.maximum(0,0.012*(1+(0.3 if bias==200 else 0))*fluct),target_scale=scale))
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
            temporal=np.sin(2*np.pi*44000*t+0.3*m)
            spatial=np.cos(m*theta)
            x += amp*(0.8 if m==3 else 0.35)*spatial[:,None]*temporal[None,:]
        x += 0.08*rng.normal(size=x.shape)
        out.append(dict(pressure_Torr=row.pressure_Torr,time_s=t,mirnov=x,target_frequency_kHz=44.0,
                        steady_state_ms=row.steady_state_ms,windows_ms=windows))
    return df,out
