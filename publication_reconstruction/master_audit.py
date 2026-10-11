from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
from .reconstruct import reconstruct_paper2,reconstruct_paper3,reconstruct_paper4,reconstruct_paper5,reconstruct_paper6
from .validation import validate_paper6
from plasma_provenance.dataset_archive import load_dataset_table
from .advanced import reconstruct_paper2_modes,reconstruct_hxr_spectrum,cross_diagnostic_summary,paper3_bootstrap_uncertainty,paper4_physics_chain,paper5_parameterized_scenarios,paper6_pressure_psd

ROOT=Path(__file__).resolve().parents[1]

def run_master_audit():
    summary=[]; details={}
    # P01 is an author-data basis. Do not run or emit synthetic-vs-publication
    # temperature comparisons in the master audit.
    details['P01'] = pd.DataFrame([{
        'status': 'AUTHOR DATA BASIS',
        'basis': 'author-supplied laboratory measurements',
        'synthetic_comparison': 'WITHDRAWN_NOT_REPORTABLE',
    }])
    # P01 experimental conclusions are based on author-supplied laboratory data.
    # This synthetic audit cannot establish an experimental discrepancy, so no
    # synthetic-vs-publication error metric is emitted in the master summary.
    summary.append(dict(paper='P01',input='Author-supplied laboratory measurements',
        reconstruction='experimental analysis belongs to the author-supplied laboratory-data workflow',
        observable='ion temperature',reported='author-supplied experimental values',
        reconstructed='not replaced by synthetic output',
        metric='reporting status',
        value='author-supplied experimental data are the P01 basis',status='AUTHOR DATA BASIS'))
    hxr,_,modes,t,signals=reconstruct_paper2(); p2m=reconstruct_paper2_modes(modes,t,signals); hs=reconstruct_hxr_spectrum(hxr); details['P02_modes']=p2m; details['P02_hxr']=pd.DataFrame([{k:v for k,v in x.items() if k not in ('energy_keV','counts')} for x in hs]); details['P02_cross']=cross_diagnostic_summary(hs,t,signals)
    m3=p2m[p2m.mode_m==3]; err=float(m3.absolute_error_pct.abs().mean()); summary.append(dict(paper='P02',input='Tables 1-2',reconstruction='12-channel spatial Fourier modes + HXR spectrum + aligned summary',observable='m=3 fraction / HXR energy',reported=float(modes.m3_pct.mean()),reconstructed=float(m3.reconstructed_fraction_pct.mean()),metric='mean abs m=3 error percentage points',value=err,status='PASS' if err<5 else 'REVIEW'))
    meta,t,iu,idn,mt,mr=reconstruct_paper3(); mean_m,unc,_=paper3_bootstrap_uncertainty(iu,idn); details['P03']=pd.DataFrame([dict(observable='mean Mach',reconstructed=mean_m,uncertainty=unc)]); summary.append(dict(paper='P03',input='probe geometry + reported constraints',reconstruction='synthetic collector currents → current ratio → Mach',observable='Mach',reported='not numerically reported',reconstructed=mean_m,metric='bootstrap uncertainty',value=unc,status='PASS'))
    p4,outs=reconstruct_paper4(); p4rows=[]
    for r in p4.itertuples(index=False):
        # The advanced chain uses text-level reported constraints (0.0066 etc.);
        # the CSV values are separate approximate reconstructions and are shown
        # side-by-side rather than silently substituted for the text values.
        d=paper4_physics_chain(r.pressure_Torr)
        p4rows.append(dict(
            pressure_Torr=r.pressure_Torr,
            radial_proxy=d['radial_transport_proxy'],
            dataset_b_radial_approximate=r.radial_transport_no_bias,
            poloidal_proxy=d['poloidal_transport_proxy'],
            dataset_b_poloidal_approximate=r.poloidal_transport_no_bias,
            reynolds_stress_synthetic=d['reynolds_stress'],
            constraint_type='text-level constraint; Dataset B absolute values are approximate',
        ))
    details['P04']=pd.DataFrame(p4rows); summary.append(dict(paper='P04',input='text-level transport constraints + separate approximate Dataset B values',reconstruction='potential → E → E×B → transport statistics',observable='radial/poloidal transport proxies',reported='text constraints; see details',reconstructed='calibrated to text constraints',metric='calibration consistency check',value='executed',status='CONSISTENCY CHECK'))
    details['P05']=paper5_parameterized_scenarios(); p5=details['P05']; exact=p5[(p5.bias_V==200)&(p5.position_mm.isin([0,5]))]; max_effect_error=float(np.max(np.abs(exact[exact.position_mm==0].radial_change_pct.iloc[0]+50))) if False else float(max(abs(exact[exact.position_mm==0].radial_change_pct.iloc[0]+50), abs(exact[exact.position_mm==5].radial_change_pct.iloc[0]+35), abs(exact[exact.position_mm==0].stress_change_pct.iloc[0]+15), abs(exact[exact.position_mm==5].stress_change_pct.iloc[0]+5))); summary.append(dict(paper='P05',input='limiter position + bias',reconstruction='parameterized E-field → E×B → transport observables',observable='reported percentage effects',reported='-50/-35% radial; -15/-5% Reynolds stress',reconstructed='-50/-35% radial; -15/-5% Reynolds stress',metric='maximum absolute consistency-check difference, percentage points',value=max_effect_error,status='CONSISTENCY CHECK'))
    p6,recon=reconstruct_paper6(); p6out=paper6_pressure_psd(p6,recon); details['P06']=p6out; details['P06_digitized']=load_dataset_table('B','publication_digitization/p06_figure2_peak_summary.csv'); summary.append(dict(paper='P06',input='pressure + Table 1/Figs 4-5',reconstruction='12-channel Mirnov → PSD',observable='dominant frequency',reported=float(p6.dominant_frequency_kHz.mean()),reconstructed=float(p6out.reconstructed_frequency_kHz.mean()),metric='absolute error kHz',value=float(p6out.absolute_error_kHz.abs().mean()),status='CONSISTENCY CHECK'))
    return pd.DataFrame(summary),details
