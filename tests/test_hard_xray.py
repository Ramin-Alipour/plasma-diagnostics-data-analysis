import numpy as np
import pytest
from hard_xray.synthetic import generate_hxr_time_series, generate_hxr_spectrum
from hard_xray.signal_analysis.analysis import power_spectrum, burst_features
from hard_xray.spectrum_analysis.spectrum import integrate_energy_band, hardness_ratio, spectral_tail_feature
from hard_xray.xray_mhd_correlation.correlation import correlation_coefficient, cross_correlation, band_power_ratio

def test_time_series_reproducible():
    a=generate_hxr_time_series(); b=generate_hxr_time_series()
    assert np.array_equal(a.counts,b.counts)
    assert a.metadata["data_type"]=="synthetic"

def test_time_series_psd_has_44khz_feature():
    d=generate_hxr_time_series(duration_s=0.02, noise_std=0)
    f,p=power_spectrum(d.counts,d.sampling_frequency_hz)
    peak=f[1:][np.argmax(p[1:])]
    assert abs(peak-44_000) <= d.sampling_frequency_hz/(len(d.counts))

def test_spectrum_poisson_and_tail():
    d=generate_hxr_spectrum(seed=1)
    assert np.all(d.counts>=0)
    assert d.metadata["noise_model"]=="poisson"
    feat=spectral_tail_feature(d.energy_keV,d.counts,180)
    assert 0 <= feat["tail_fraction"] <= 1

def test_known_band_and_hardness():
    e=np.arange(10,101,10); c=np.arange(1,10+1)
    assert integrate_energy_band(e,c,20,60)==2+3+4+5
    assert hardness_ratio(e,c,(10,50),(50,101)) == pytest.approx((5+6+7+8+9+10)/(1+2+3+4))

def test_burst_detection():
    d=generate_hxr_time_series(noise_std=0)
    out=burst_features(d.time_s,d.counts,prominence=20)
    assert len(out["peak_times_s"])>=2

def test_hxr_mhd_correlation_and_lag():
    t=np.arange(2000)/100000.
    m=np.sin(2*np.pi*1000*t)
    h=np.sin(2*np.pi*1000*t)
    assert correlation_coefficient(h,m)>0.99
    l,c=cross_correlation(h,m,100000.)
    assert abs(l[np.argmax(c)]) < 1/100000.

def test_band_power_ratio():
    t=np.arange(5000)/100000.; x=np.sin(2*np.pi*1000*t)+0.2*np.sin(2*np.pi*5000*t)
    assert band_power_ratio(x,100000,(900,1100),(4500,5500)) > 5

def test_invalid_inputs():
    with pytest.raises(ValueError): generate_hxr_spectrum(bins=5)
    with pytest.raises(ValueError): integrate_energy_band([2,1],[1,2],1,2)
    with pytest.raises(ValueError): correlation_coefficient(np.ones(5),np.ones(5))
