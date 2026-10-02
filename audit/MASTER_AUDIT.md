# Master Reconstruction Audit — v0.1.1

This audit is descriptive. P01 and P05 publication-target comparisons are reported as computational consistency checks rather than independent validation.

## Summary

| Paper | Input | Reconstruction | Observable | Reported | Reconstructed / result | Metric | Value | Status |
|---|---|---|---|---:|---:|---|---:|---|
| P01 | Table VI-VII + Eq. (3)/(11) | synthetic CCD-like spectrum → Gaussian fit → quadrature resolution correction | ion temperature | 25.313333333333333 | 34.405310546706396 | mean absolute relative difference % (consistency check) | 160.36474963491762 | CONSISTENCY CHECK |
| P02 | Tables 1-2 | 12-channel spatial Fourier modes + HXR spectrum + aligned summary | m=3 fraction / HXR energy | 89.10754999999999 | 88.96495040621258 | mean abs m=3 error percentage points | 0.14627038130091066 | PASS |
| P03 | probe geometry + reported constraints | synthetic collector currents → current ratio → Mach | Mach | not numerically reported | 0.454929212006573 | bootstrap uncertainty | 0.002349175536502966 | PASS |
| P04 | pressure + reported transport constraints | potential → E → E×B → transport statistics | radial transport proxy | see constraint table | see detail table | physics chain | executed | PASS |
| P05 | limiter position + bias | parameterized E-field → E×B → transport observables | reported percentage effects | -50/-35% radial; -15/-5% Reynolds stress | -50/-35% radial; -15/-5% Reynolds stress | maximum absolute consistency-check difference, percentage points | 1.4210854715202004e-14 | CONSISTENCY CHECK |
| P06 | pressure + Table 1/Figs 4-5 | 12-channel Mirnov → PSD | dominant frequency | 44.0 | 44.00975097656249 | absolute error kHz | 0.009750976562493463 | PASS |

## P01 resolution note

- Instrumental FWHM: 0.03704 nm.
- Diffraction FWHM: λ/(1.35 × 10^5).
- Resolution FWHM: quadrature sum of instrumental and diffraction terms.
- The resulting resolution is approximately 0.0372 nm over the selected lines.
- The reconstructed temperatures are not forced to match the reported Table VII temperatures.
- The comparison is a computational consistency check using synthetic spectra, not independent experimental validation.

## P05 interpretation

- Reported numerical percentage effects are used as explicit construction targets.
- Matching those targets is a round-trip consistency check, not independent experimental validation.

## Scientific boundary

No original IR-T1 raw diagnostic arrays are distributed. Synthetic and reconstructed quantities remain explicitly separated from published experimental measurements.
