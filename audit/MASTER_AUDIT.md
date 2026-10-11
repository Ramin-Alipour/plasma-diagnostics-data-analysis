# Master Reconstruction Audit — v0.1.2

This audit distinguishes table reproduction from model sensitivity. Agreement with values derived from the same publication is not independent experimental validation.

## Summary

| Paper | Input | Reconstruction | Observable | Reported | Reconstructed / result | Metric | Value | Status |
|---|---|---|---|---:|---:|---|---:|---|
| P01 | listed Eq. (16)-calculated temperature vs reported temperature | source-table consistency comparison; separate rounded-width recalculation and equation-model sensitivity | ion temperature | 25.313333333333333 | 25.31427027333333 | mean absolute relative difference % (source-table consistency comparison) | 0.04201537799902157 | CONSISTENCY CHECK |
| P02 | Tables 1-2 | 12-channel spatial Fourier modes + HXR spectrum + aligned summary | m=3 fraction / HXR energy | 89.10755 | 88.96495040621258 | mean abs m=3 error percentage points | 0.14627038130091066 | PASS |
| P03 | probe geometry + reported constraints | synthetic collector currents → current ratio → Mach | Mach | not numerically reported | 0.454929212006573 | bootstrap uncertainty | 0.002349175536502966 | PASS |
| P04 | text-level constraints + separate approximate Dataset B values | potential → E → E×B → transport statistics | radial/poloidal transport proxies | text constraints; see details | calibrated to text constraints | calibration consistency check | executed | CONSISTENCY CHECK |
| P05 | limiter position + bias | parameterized E-field → E×B → transport observables | reported percentage effects | -50/-35% radial; -15/-5% Reynolds stress | -50/-35% radial; -15/-5% Reynolds stress | maximum absolute consistency-check difference, percentage points | 1.4210854715202004e-14 | CONSISTENCY CHECK |
| P06 | pressure + Table 1/Figs 4-5 | 12-channel Mirnov → PSD | dominant frequency | mean of approximate pressure-specific estimates: 44.307 kHz | 44.00975097656249 | mean absolute difference from approximate estimates, kHz | 0.627964 | CONSISTENCY CHECK |

## P01: two explicitly separate analyses

- **Primary table-reproduction comparison:** published Table VI Doppler FWHM values and Eq. (16). Mean reported temperature 25.313333 eV; mean reproduced temperature 25.314270 eV; mean absolute relative difference 0.042015%.
- **Alternative printed-equation model:** synthetic CCD-like spectra with the printed Eq. (3)/(11) quadrature correction. Its previous result was about 158.09% mean absolute relative difference (mean reconstructed temperature about 34.2167 eV). This result remains recorded separately.
- Table VI resolution values closely track the linear sum while Eq. (3) specifies quadrature. Both interpretations remain explicit; neither source values nor temperatures are altered to force agreement.
- Table reproduction is not independent validation and does not recover original CCD frames.

## Scientific boundary

No original IR-T1 raw diagnostic arrays are distributed. Dataset A laboratory/device-software data, Dataset B publication-derived data, and synthetic data remain separate evidence classes.
