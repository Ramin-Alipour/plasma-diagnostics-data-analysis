"""Unit-explicit calculations for selected tokamak observables."""
import numpy as np
from scipy import signal
C = 299792458.0
KB = 1.380649e-23
E_CHARGE = 1.602176634e-19
EPS0 = 8.8541878128e-12
ME = 9.1093837139e-31
MU0 = 1.25663706212e-6
AMU = 1.66053906660e-27

def doppler_temperature_eV(fwhm_nm, wavelength_nm, mass_amu):
    """Thermal Gaussian Doppler temperature in eV; correct instrumental width first."""
    if min(fwhm_nm, wavelength_nm, mass_amu) <= 0:
        raise ValueError("FWHM, wavelength and mass must be positive.")
    temp_joule = mass_amu*AMU*C**2/(8*np.log(2))*(fwhm_nm/wavelength_nm)**2
    return float(temp_joule/E_CHARGE)

def doppler_velocity_m_s(delta_lambda_nm, rest_wavelength_nm):
    """Non-relativistic line-of-sight velocity from calibrated wavelength shift."""
    if rest_wavelength_nm <= 0: raise ValueError("Rest wavelength must be positive.")
    return float(C*delta_lambda_nm/rest_wavelength_nm)

def electric_field_1d_v_m(x_m, potential_v):
    """E=-dV/dx, with x strictly increasing."""
    x, v = np.asarray(x_m,float), np.asarray(potential_v,float)
    if x.ndim != 1 or v.ndim != 1 or x.size != v.size or x.size < 2: raise ValueError("Expected equal-length 1D arrays.")
    if np.any(np.diff(x) <= 0): raise ValueError("Coordinates must increase strictly.")
    return -np.gradient(v,x)

def exb_velocity_m_s(electric_field_v_m, magnetic_field_t):
    """Vector E×B drift; last axis of each vector must have 3 components."""
    e, b = np.asarray(electric_field_v_m,float), np.asarray(magnetic_field_t,float)
    if e.shape[-1] != 3 or b.shape[-1] != 3: raise ValueError("E and B must have three components.")
    b2 = np.sum(b*b,axis=-1,keepdims=True)
    if np.any(b2 == 0): raise ValueError("B must be nonzero.")
    return np.cross(e,b)/b2

def beta_local(pressure_pa, magnetic_field_t):
    if pressure_pa < 0 or magnetic_field_t == 0: raise ValueError("Pressure must be >=0 and B nonzero.")
    return float(pressure_pa/(magnetic_field_t**2/(2*MU0)))

def energy_confinement_time_s(stored_energy_j, net_loss_power_w):
    """tau_E=W/P_loss; caller must define P_loss consistently."""
    if stored_energy_j < 0 or net_loss_power_w <= 0: raise ValueError("W>=0 and P_loss>0 required.")
    return float(stored_energy_j/net_loss_power_w)

def debye_length_m(ne_m3, te_eV):
    """Classical electron Debye length; Te supplied in eV."""
    if ne_m3 <= 0 or te_eV <= 0: raise ValueError("Density and temperature must be positive.")
    return float(np.sqrt(EPS0*te_eV/(ne_m3*E_CHARGE)))

def electron_plasma_frequency_hz(ne_m3):
    """Electron plasma frequency in Hz (cycles/s)."""
    if ne_m3 <= 0: raise ValueError("Density must be positive.")
    return float(np.sqrt(ne_m3*E_CHARGE**2/(EPS0*ME))/(2*np.pi))

def greenwald_density_m3(ip_ma, minor_radius_m):
    if ip_ma <= 0 or minor_radius_m <= 0: raise ValueError("Ip and minor radius must be positive.")
    return float(ip_ma/(np.pi*minor_radius_m**2)*1e20)

def power_spectral_density(values, sampling_hz, nperseg=None):
    """Welch PSD; returns frequency in Hz and PSD in input-unit squared/Hz."""
    x = np.asarray(values,float)
    if x.ndim != 1 or x.size < 4 or sampling_hz <= 0: raise ValueError("Need a 1D signal with >=4 samples and positive sampling rate.")
    if nperseg is None: nperseg = min(1024,x.size)
    return signal.welch(x,fs=sampling_hz,nperseg=min(int(nperseg),x.size),detrend="constant")

def normalized_cross_correlation(x,y):
    """Demeaned full-lag cross-correlation normalized by global Euclidean norms."""
    x,y = np.asarray(x,float),np.asarray(y,float)
    if x.ndim != 1 or y.ndim != 1 or not x.size or not y.size: raise ValueError("Inputs must be nonempty 1D arrays.")
    x,y = x-x.mean(),y-y.mean()
    den = np.linalg.norm(x)*np.linalg.norm(y)
    if den == 0: raise ValueError("Undefined for constant signals.")
    return signal.correlation_lags(x.size,y.size,mode="full"), signal.correlate(x,y,mode="full")/den

def svd_decompose(channel_by_time_matrix, center=True):
    """SVD of channels × time matrix; returns U, singular values and Vh."""
    x = np.asarray(channel_by_time_matrix,float)
    if x.ndim != 2 or min(x.shape) < 1 or not np.all(np.isfinite(x)): raise ValueError("Expected finite nonempty 2D matrix.")
    if center: x = x-x.mean(axis=1,keepdims=True)
    return np.linalg.svd(x,full_matrices=False)
