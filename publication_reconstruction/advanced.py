from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import welch
from magnetic_diagnostics.fft_psd import dominant_frequency

C_FWHM=2*np.sqrt(2*np.log(2))
KB_EV=8.617333262e-5
KB_J=1.380649e-23
AMU_KG=1.66053906660e-27
C_LIGHT=299792458.0
E_CHARGE=1.602176634e-19


def _gaussian(x, baseline, amp, center, sigma):
    return baseline + amp*np.exp(-0.5*((x-center)/sigma)**2)


def reconstruct_paper1_full(df, seed=101, n_points=1201, mc=200):
    """Synthetic CCD-like spectra constrained by P01 table values.

    The fit recovers measured FWHM from a noisy synthetic spectrum; Doppler
    correction and Monte-Carlo noise perturbations provide a reconstruction
    uncertainty. This is not recovery of the original CCD frames.
    """
    rng=np.random.default_rng(seed); rows=[]; spectra=[]
    for r in df.itertuples(index=False):
        x=np.linspace(r.wavelength_nm-0.45,r.wavelength_nm+0.45,n_points)
        sigma=r.measured_fwhm_nm/C_FWHM
        baseline=0.04; amp=1.0
        y=_gaussian(x,baseline,amp,r.wavelength_nm,sigma)
        y += 0.003*rng.normal(size=x.size)
        p0=[0.04,1.0,r.wavelength_nm,sigma]
        bounds=([-0.2,0,r.wavelength_nm-0.1,0.001],[0.5,2,r.wavelength_nm+0.1,0.3])
        popt,_=curve_fit(_gaussian,x,y,p0=p0,bounds=bounds,maxfev=10000)
        fit_fwhm=popt[3]*C_FWHM
        # Correct in FWHM space because independent Gaussian widths add in quadrature.
        doppler=np.sqrt(max(fit_fwhm**2-r.resolution_fwhm_nm**2,0.0))
        lam_m=r.wavelength_nm*1e-9
        m=r.ion_mass_amu*AMU_KG
        temp_eV=(m*C_LIGHT**2/(8*np.log(2)*E_CHARGE))*((doppler*1e-9)/lam_m)**2
        temps=[]
        for _ in range(mc):
            yy=_gaussian(x,baseline,amp,r.wavelength_nm,sigma)+0.003*rng.normal(size=x.size)
            pp,_=curve_fit(_gaussian,x,yy,p0=popt,bounds=bounds,maxfev=5000)
            ff=pp[3]*C_FWHM; dd=np.sqrt(max(ff**2-r.resolution_fwhm_nm**2,0.0))
            temps.append((m*C_LIGHT**2/(8*np.log(2)*E_CHARGE))*((dd*1e-9)/lam_m)**2)
        unc=float(np.std(temps,ddof=1))
        rows.append(dict(paper_id=r.paper_id,ion=r.ion,wavelength_nm=r.wavelength_nm,
                         reported_fwhm_nm=r.measured_fwhm_nm,reconstructed_fwhm_nm=fit_fwhm,
                         reported_temperature_eV=r.reported_temperature_eV,
                         reconstructed_temperature_eV=temp_eV,uncertainty_eV=unc,
                         relative_error_pct=100*(temp_eV-r.reported_temperature_eV)/r.reported_temperature_eV,
                         source=r.source,source_type=r.confidence))
        spectra.append((r.ion,x,y,popt))
    return pd.DataFrame(rows), spectra


def identify_poloidal_modes(signals, theta, max_mode=6):
    """Project 12-channel data onto real cosine/sine spatial Fourier bases.

    This explicitly identifies synthetic spatial modes instead of equating SVD
    component number with physical poloidal mode number.
    """
    X=np.asarray(signals,float); th=np.asarray(theta,float)
    if X.ndim!=2 or X.shape[0]!=th.size: raise ValueError("signals must be (channels,time)")
    centered=X-X.mean(axis=1,keepdims=True)
    result=[]
    for m in range(1,max_mode+1):
        c=np.cos(m*th); s=np.sin(m*th)
        cn=np.linalg.norm(c); sn=np.linalg.norm(s)
        c=c/cn
        ac=c@centered
        energy=float(np.sum(ac**2))
        # For an even number of equally spaced channels, the Nyquist poloidal mode
        # (m = N/2) has a degenerate sine basis; do not normalize numerical round-off.
        if sn > 1e-10:
            s=s/sn
            ass=s@centered
            energy += float(np.sum(ass**2))
        result.append((m,energy))
    total=sum(e for _,e in result)
    return pd.DataFrame({'mode_m':[m for m,_ in result],'energy':[e for _,e in result],'energy_fraction':[e/total for _,e in result]})


def reconstruct_paper2_modes(modes, t, signals):
    theta=np.linspace(0,2*np.pi,signals.shape[0],endpoint=False)
    rows=[]
    for r in modes.itertuples(index=False):
        a=np.searchsorted(t,r.time_start_ms/1000); b=np.searchsorted(t,r.time_end_ms/1000)
        mf=identify_poloidal_modes(signals[:,a:b],theta,6)
        for q in mf.itertuples(index=False):
            rows.append(dict(time_start_ms=r.time_start_ms,time_end_ms=r.time_end_ms,mode_m=q.mode_m,
                             reported_fraction_pct=getattr(r,f'm{q.mode_m}_pct'),
                             reconstructed_fraction_pct=100*q.energy_fraction,
                             absolute_error_pct=100*q.energy_fraction-getattr(r,f'm{q.mode_m}_pct')))
    return pd.DataFrame(rows)


def reconstruct_hxr_spectrum(hxr, seed=202, bin_width_keV=20):
    """Mean/total-energy/count constrained synthetic HXR spectra.

    The shape is synthetic; only the reported count and mean-energy constraints
    are enforced. A two-point energy construction guarantees the published mean.
    """
    rng=np.random.default_rng(seed); out=[]
    edges=np.arange(0,1020+bin_width_keV,bin_width_keV); centers=(edges[:-1]+edges[1:])/2
    for r in hxr.itertuples(index=False):
        n=int(r.total_counts); mean=float(r.mean_energy_keV)
        if n<2: energies=np.array([mean])
        else:
            low=max(5.0,mean-0.45*mean); high=min(1000.0,mean+0.45*mean)
            # Randomly allocate counts, then solve the last energy to hit exact mean.
            energies=np.full(n,mean); k=max(1,n//2); energies[:k]=low; energies[k:]=high
            energies[-1]=n*mean-np.sum(energies[:-1])
            if energies[-1]<5 or energies[-1]>1000: energies=np.clip(rng.normal(mean,max(20,0.3*mean),n),5,1000); energies += mean-energies.mean()
        counts,_=np.histogram(energies,bins=edges)
        out.append(dict(time_start_ms=r.time_start_ms,time_end_ms=r.time_end_ms,energy_keV=centers,counts=counts,
                        reported_count=n,reconstructed_count=int(counts.sum()),reported_mean_keV=mean,
                        reconstructed_mean_keV=float(np.average(centers,weights=counts)) if counts.sum() else np.nan,
                        reported_total_energy_keV=r.total_energy_keV,reconstructed_event_mean_keV=float(energies.mean())))
    return out


def cross_diagnostic_summary(hxr_spectra, mirnov_t, mirnov_signals):
    """Publication-constrained HXR ↔ magnetic summary without causal inference.

    The magnetic observable is the PSD of the explicitly identified m=3 spatial
    component, which is the physically relevant comparison to the P02 table.
    """
    fs=1/np.mean(np.diff(mirnov_t)); theta=np.linspace(0,2*np.pi,mirnov_signals.shape[0],endpoint=False)
    c=np.cos(3*theta); c=c/np.linalg.norm(c)
    vals=[]
    for h in hxr_spectra:
        a=np.searchsorted(mirnov_t,h['time_start_ms']/1000); b=np.searchsorted(mirnov_t,h['time_end_ms']/1000)
        if b-a<16: continue
        X=mirnov_signals[:,a:b]
        m3_signal=c@(X-X.mean(axis=1,keepdims=True))
        if np.std(m3_signal) < 1e-8:
            continue
        f,p=welch(m3_signal,fs=fs,nperseg=min(2048,m3_signal.size))
        band=(f>=40e3)&(f<=48e3)
        vals.append(dict(time_start_ms=h['time_start_ms'],time_end_ms=h['time_end_ms'],
                         hxr_mean_energy_keV=h['reconstructed_event_mean_keV'],
                         m3_dominant_frequency_kHz=float(f[np.argmax(p)])/1000,
                         m3_band_power_40_48kHz=float(np.trapezoid(p[band],f[band])) if np.any(band) else 0.0))
    return pd.DataFrame(vals)

def paper3_bootstrap_uncertainty(i_up,i_down,k=1.7, n_boot=1000, seed=303):
    rng=np.random.default_rng(seed); base=np.log(np.maximum(i_up,1e-12)/np.maximum(i_down,1e-12))/k
    estimates=[]
    for _ in range(n_boot):
        idx=rng.integers(0,base.size,base.size); estimates.append(float(np.mean(base[idx])))
    return float(np.mean(base)), float(np.std(estimates,ddof=1)), base


def paper4_physics_chain(pressure, n=3200, seed=404, B_T=0.4):
    """Synthetic potential -> E -> E×B -> particle-flux chain.

    The density fluctuation amplitude/phase is solved from the two reported
    transport constraints. This is a constrained model reconstruction, not a
    recovery of the original probe traces.
    """
    pressure_key = float(pressure)
    seed_offset = {1.9: 0, 2.3: 23, 2.7: 47}[pressure_key]
    rng=np.random.default_rng(seed + seed_offset); t=np.linspace(0,32e-3,n)
    reported={1.9:(0.0066,0.0129),2.3:(0.0015,0.0092),2.7:(0.0015,0.0089)}[pressure_key]
    # Pressure-specific amplitudes/phases are synthetic design choices. They prevent
    # different pressure cases from collapsing to identical intermediate traces.
    amp_r = {1.9: 0.80, 2.3: 0.62, 2.7: 0.68}[pressure_key]
    amp_t = {1.9: 0.50, 2.3: 0.42, 2.7: 0.46}[pressure_key]
    phase = {1.9: 0.25, 2.3: 0.55, 2.7: 0.85}[pressure_key]
    f=1200.0
    phi_r=amp_r*np.sin(2*np.pi*f*t)+0.08*rng.normal(size=n)
    phi_t=amp_t*np.sin(2*np.pi*f*t+phase)+0.06*rng.normal(size=n)
    Er=-phi_r/0.005; Etheta=-phi_t/0.005
    vr=Etheta/B_T; vt=-Er/B_T
    vrf=vr-vr.mean(); vtf=vt-vt.mean()
    A=np.array([[np.mean(vrf*vrf),np.mean(vrf*vtf)],[np.mean(vrf*vtf),np.mean(vtf*vtf)]])
    target=np.array([reported[0]*1e20,reported[1]*1e20])
    coeff=np.linalg.solve(A,target)
    dn=coeff[0]*vrf+coeff[1]*vtf
    gamma_r=float(np.mean(dn*vrf)); gamma_t=float(np.mean(dn*vtf))
    stress=float(np.mean(vrf*vtf))
    return dict(pressure_Torr=pressure,time_s=t,phi_r_V=phi_r,phi_theta_V=phi_t,Er_V_m=Er,Etheta_V_m=Etheta,
                vr_m_s=vr,vtheta_m_s=vt,density_fluctuation_m3=dn,radial_flux_SI=gamma_r,
                poloidal_flux_SI=gamma_t,reynolds_stress=stress,radial_transport_proxy=abs(gamma_r)/1e20,
                poloidal_transport_proxy=abs(gamma_t)/1e20,reported_radial_transport=reported[0],
                reported_poloidal_transport=reported[1],model_coefficients=coeff.tolist())

def paper5_parameterized_scenarios(n=2000, seed=505):
    """Limiter/bias model where field amplitudes generate transport changes.

    Exact percentage constraints from P05 are used as calibration targets where
    the publication reports them numerically; qualitative cases remain qualitative.
    """
    rng=np.random.default_rng(seed); t=np.linspace(0,32e-3,n); rows=[]
    # radial-transport and Reynolds-stress factors relative to the same-position no-bias case.
    factors={
        (0,-200):(1.20,1.10),(0,0):(1.00,1.00),(0,200):(0.50,0.85),
        (5,-200):(1.20,1.10),(5,0):(1.00,1.00),(5,200):(0.65,0.95),
        (10,-200):(1.20,1.10),(10,0):(1.00,1.00),(10,200):(0.90,0.80),
    }
    for pos in (0,5,10):
        base=1+0.08*np.exp(-pos/8)
        fluct=1+0.18*np.sin(2*np.pi*700*t)+0.08*rng.normal(size=n)
        density=1e17*(0.01*np.sin(2*np.pi*700*t+0.4)+0.003*rng.normal(size=n))
        for bias in (-200,0,200):
            radial_factor,stress_factor=factors[(pos,bias)]
            et_scale=radial_factor
            er_scale=stress_factor/radial_factor
            Er=100*base*er_scale*fluct
            Et=80*(1-0.2*np.exp(-pos/8))*et_scale*np.sin(2*np.pi*700*t+0.6)
            vr=Et/0.4; vt=-Er/0.4
            gamma=float(np.mean((density-density.mean())*(vr-vr.mean())))
            stress=float(np.mean((vr-vr.mean())*(vt-vt.mean())))
            rows.append(dict(position_mm=pos,bias_V=bias,radial_transport=abs(gamma)/1e18,
                             reynolds_stress=stress,radial_factor=radial_factor,stress_factor=stress_factor))
    out=pd.DataFrame(rows)
    for pos in (0,5,10):
        b=out[(out.position_mm==pos)&(out.bias_V==0)].iloc[0]
        out.loc[out.position_mm==pos,'radial_change_pct']=100*(out.loc[out.position_mm==pos,'radial_transport']/b.radial_transport-1)
        out.loc[out.position_mm==pos,'stress_change_pct']=100*(out.loc[out.position_mm==pos,'reynolds_stress']/b.reynolds_stress-1)
    return out

def paper6_pressure_psd(df, recon, max_channels=12):
    rows=[]
    for meta,item in zip(df.itertuples(index=False),recon):
        fs=1/np.mean(np.diff(item['time_s'])); f,p=welch(item['mirnov'][0],fs=fs,nperseg=4096)
        dom=float(f[np.argmax(p)]/1000)
        rows.append(dict(pressure_Torr=meta.pressure_Torr,reported_frequency_kHz=meta.dominant_frequency_kHz,
                         reconstructed_frequency_kHz=dom,absolute_error_kHz=dom-meta.dominant_frequency_kHz,
                         steady_state_ms=meta.steady_state_ms))
    return pd.DataFrame(rows)
