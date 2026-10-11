# RC4.2 Master Reconstruction Audit

This audit is descriptive and validation-oriented. It does not rank the six papers or assign an overall score.

## Summary

| paper   | input                                     | reconstruction                                                    | observable                  | reported                                 | reconstructed                            | metric                                                | value                  | status   |
|:--------|:------------------------------------------|:------------------------------------------------------------------|:----------------------------|:-----------------------------------------|:-----------------------------------------|:------------------------------------------------------|:-----------------------|:---------|
| P01     | Table VI-VII                              | synthetic CCD-like spectrum → Gaussian fit → Doppler correction   | ion temperature             | 25.313333333333333                       | 25.296146241969705                       | mean relative error %                                 | 0.9081224437964254     | PASS     |
| P02     | Tables 1-2                                | 12-channel spatial Fourier modes + HXR spectrum + aligned summary | m=3 fraction / HXR energy   | 89.10754999999999                        | 88.96495040621258                        | mean abs m=3 error percentage points                  | 0.14627038130091066    | PASS     |
| P03     | probe geometry + reported constraints     | synthetic collector currents → current ratio → Mach               | Mach                        | not numerically reported                 | 0.454929212006573                        | bootstrap uncertainty                                 | 0.002349175536502966   | PASS     |
| P04     | pressure + approximate Dataset B constraints | potential → E → E×B → transport statistics                      | radial/poloidal transport proxies | see approximate constraint table     | calibrated to stored approximate values | calibration consistency check                         | executed               | CONSISTENCY CHECK |
| P05     | limiter position + bias                   | parameterized E-field → E×B → transport observables               | reported percentage effects | -50/-35% radial; -15/-5% Reynolds stress | -50/-35% radial; -15/-5% Reynolds stress | maximum absolute calibration error, percentage points | 1.4210854715202004e-14 | PASS     |
| P06     | pressure + Table 1/Figs 4-5               | 12-channel Mirnov → PSD                                           | dominant frequency          | mean of approximate pressure-specific estimates: 44.307 kHz | 44.010 kHz (synthetic 44 kHz activity) | mean absolute difference from approximate estimates: 0.628 kHz | 0.628 kHz | CONSISTENCY CHECK |

## P04 pressure-specific synthetic intermediate check

| Pressure (Torr) | Radial proxy calibrated to text constraint | Poloidal proxy calibrated to text constraint | Reynolds stress (synthetic) |
|---:|---:|---:|---:|
| 1.9 | 0.0066 | 0.0129 | -48616.8579629 |
| 2.3 | 0.0015 | 0.0092 | -27880.2742437 |
| 2.7 | 0.0015 | 0.0089 | -26060.1514765 |

The P04 advanced chain uses text-level constraints (0.0066/0.0015/0.0015 radial and 0.0129/0.0092/0.0089 poloidal). Dataset B separately stores approximate absolute transport/E-field reconstruction values, not exact table transcriptions; those CSV values are not silently substituted for the text constraints. Intermediate Reynolds-stress values are synthetic model outputs and are not presented as published measurements.

## Scientific boundaries

- Synthetic reconstructions are never represented as recovered raw IR-T1 measurements.
- P01 uses a synthetic CCD-like spectrum and preserves line-level deviations rather than hiding them.
- P02 uses explicit spatial Fourier construction for physical mode-number encoding; SVD component number is not used as a proxy for physical mode number.
- P02 HXR spectra are constrained by published counts/energy information; detector response is not reconstructed.
- P03 Mach is a model-constrained reconstruction with bootstrap sensitivity; the original raw collector-current series is unavailable.
- P04 advanced-chain targets are text-level reported constraints; Dataset B's absolute transport/E-field entries are separate approximate reconstruction values. Intermediate potential/E-field/velocity/density traces are synthetic.
- P05 numerical effects are parameterization targets where explicitly reported; qualitative source statements remain qualitative.
- P06 synthetic Mirnov traces use the text-level approximately 44 kHz activity; pressure-specific frequencies in the constraint table are approximate estimates. Canonical Figure 2 digitization and the legacy processing snapshot are distinct approximate outputs. The source timing inconsistency is preserved.
- Post-2018 continuity is described as scientific/technical computational practice; confidential client datasets and undisclosed experiments are not invented or included.

## Release interpretation

RC4.2 is a release candidate that has completed the planned scientific, software, continuity/evidence, and reproducibility review cycle. A final public release remains distinct from this release candidate.
