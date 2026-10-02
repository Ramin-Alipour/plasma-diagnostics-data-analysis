from __future__ import annotations
import numpy as np
import pandas as pd
from spectroscopy.doppler_broadening.temperature import estimate_doppler_temperature
from magnetic_diagnostics.svd import compute_svd
from magnetic_diagnostics.fft_psd import channel_psd, dominant_frequency
from turbulence_transport.reynolds_stress.analysis import reynolds_stress
from electrostatic_diagnostics.electric_fields.field import electric_field_from_potential


def validate_paper1(df):
    rows=[]
    for r in df.itertuples(index=False):
        obs=r.measured_fwhm_nm/2.354820045
        inst=r.resolution_fwhm_nm/2.354820045
        out=estimate_doppler_temperature(r.wavelength_nm,obs,r.ion_mass_amu,instrumental_sigma=inst)
        err=100*(out['temperature_eV']-r.reported_temperature_eV)/r.reported_temperature_eV
        rows.append({'ion':r.ion,'reported_TeV':r.reported_temperature_eV,'reconstructed_TeV':out['temperature_eV'],'relative_error_pct':err})
    return pd.DataFrame(rows)


def validate_paper2(modes, t, signals):
    results=[]
    fs=1/np.mean(np.diff(t))
    svd=compute_svd(signals,center=True)
    energy=svd.explained_energy
    for _,r in modes.iterrows():
        # The generator places the mode fractions in a short interval. Recompute SVD on it.
        a=np.searchsorted(t,r.time_start_ms/1000); b=np.searchsorted(t,r.time_end_ms/1000)
        e=compute_svd(signals[:,a:b],center=True).explained_energy
        results.append({'time_start_ms':r.time_start_ms,'target_m3_pct':r.m3_pct,'reconstructed_component1_pct':100*e[0]})
    return pd.DataFrame(results),svd


def validate_paper3(i_up,i_down,k=1.7):
    return np.log(i_up/i_down)/k


def validate_reynolds(er,etheta,bt=0.4):
    # For E x B drift components with orthogonal E and toroidal B, v_r~E_theta/B and v_theta~-E_r/B.
    vr=(etheta-np.mean(etheta))/bt
    vp=-(er-np.mean(er))/bt
    return reynolds_stress(vr,vp)


def validate_paper6(signals,t):
    fs=1/np.mean(np.diff(t))
    f,p=channel_psd(signals[0],sampling_frequency=fs)
    return dominant_frequency(f,p), f, p
