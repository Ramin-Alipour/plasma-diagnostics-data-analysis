"""Run the publication-reconstruction validation chain across all six papers."""
from __future__ import annotations
import numpy as np
from core.data_model import TimeSeries
from core.signal_processing import compute_psd
from magnetic_diagnostics.svd import compute_svd
from magnetic_diagnostics.fft_psd import dominant_frequency
from turbulence_transport.reynolds_stress.analysis import reynolds_stress
from electrostatic_diagnostics.electric_fields.field import electric_field_from_potential
from publication_reconstruction.reconstruct import (
    reconstruct_paper1,reconstruct_paper2,reconstruct_paper3,
    reconstruct_paper4,reconstruct_paper5,reconstruct_paper6,
)
from publication_reconstruction.validation import validate_paper1


def run_all():
    report={}
    p1,_=reconstruct_paper1(); v1=validate_paper1(p1)
    report['P01']={'n_lines':len(p1),'max_temperature_relative_error_pct':float(np.max(np.abs(v1.relative_error_pct)))}

    hxr,events,modes,t,mirnov=reconstruct_paper2()
    svd=compute_svd(mirnov,center=True)
    fs=1/np.mean(np.diff(t)); f,p=compute_psd(mirnov[0],fs)
    report['P02']={'hxr_windows':len(events),'mirnov_channels':mirnov.shape[0],'dominant_frequency_kHz':float(dominant_frequency(f,p)/1000),'dominant_svd_energy_pct':float(100*svd.explained_energy[0])}

    meta,t,iup,idown,mt,mr=reconstruct_paper3()
    report['P03']={'samples':len(t),'mach_rmse':float(np.sqrt(np.mean((mt-mr)**2))),'k':1.7}

    _,p4=reconstruct_paper4()
    report['P04']={'pressure_cases':len(p4),'pressure_values_Torr':[x['pressure_Torr'] for x in p4]}

    p5=reconstruct_paper5()
    report['P05']={'limiter_bias_cases':len(p5),'positions_mm':sorted(set(x['position_mm'] for x in p5))}

    _,p6=reconstruct_paper6()
    f6=[]
    for d in p6:
        fs=1/np.mean(np.diff(d['time_s'])); ff,pp=compute_psd(d['mirnov'][0],fs); f6.append(float(dominant_frequency(ff,pp)/1000))
    report['P06']={'pressure_cases':len(p6),'dominant_frequency_kHz':f6,'reported_frequency_kHz':44.0}
    return report
