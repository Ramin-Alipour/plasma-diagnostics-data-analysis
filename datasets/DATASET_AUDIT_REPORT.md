# IR-T1 Dataset Audit — Summary

**Date:** 2026-10-11

## Provenance
- Dataset A CSV values were not changed. Dataset A and repository-level README documentation clarifies that the supplied laboratory files may include native hardware/acquisition-software outputs.
- Dataset B is publication-derived and remains separate from Dataset A.
- No 1.3% Gaussian-noise assumption or RNG seed is applied to Dataset B.

## P01 spectroscopy
- 15 spectral lines checked against the published Tables VI–VII.
- Restored the table-reported measured widths, resolution widths, Doppler widths, ion masses, and reported temperatures.
- Removed unsupported instrumental/diffraction decomposition columns from the audited CSV.
- Added an equation-derived temperature column; maximum relative difference from the reported Table VII temperatures is 0.177% (printed table values are rounded and/or internally not identical to direct recomputation).

## P02 hard X-ray
- Restored the six Table 1 counts/total-energy pairs: counts = [5, 5, 6, 158, 182, 136]; total energy (keV) = [3301, 2842, 3475, 78458, 80505, 55808].
- Mean energy is explicitly calculated as total energy / counts; arithmetic consistency test: PASS.
- The prior values in the B file did not match the exact Table 1 values despite being labelled exact_table.

## P02 MHD modal table
- Restored all 20 rows to the printed Table 2 values.
- Modal percentage sums range from 99.822% to 101.974% for the transcribed values. No normalization was applied.
- The prior values in the B file did not match the source table despite being labelled exact_table.

## P03 compound probe
- Restored reported precision for Ti/Te = 0.2, edge electron temperature = 14 eV, maximum plasma current = 16 kA, and equal-saturation-current location = 0.5 mm.
- Model equation is kept distinct from reported measurements.

## P04 pressure/transport
- Numeric values are retained as working reconstruction estimates, but row-level provenance is corrected to say absolute E-field/transport entries are approximate and not exact table transcriptions.
- Further source-calibrated digitization is needed before treating those absolute values as quantitative extracted values.

## P05 limiter/transport
- Numerical effects and qualitative statements remain separated; qualitative effects are not converted to fabricated exact percentages.

## P06 pressure/MHD
- Restored the general ranges in Table 1: electron density 0.7–1.5 × 10^13 cm^-3 and electron temperature 150–230 eV.
- Pressure-specific steady-state/frequency entries remain explicitly approximate.
- Preserved the paper's timing inconsistency: discharge time <35 ms versus figure windows including 45–46 ms.

## Release boundary
This report is an audit note, not a claim that all values have been independently revalidated against publisher source files. Keep approximate/digitized values labelled and do not normalize or silently overwrite them.

## P01 reconciliation and interpretation boundary
- Dataset A and Dataset B remain unchanged and separately sourced.
- A separate ledger records 15 value-based correspondences on ion, wavelength, and measured FWHM. Matching values do not establish shared raw-data provenance.
- No corrected/reconciled numeric values are supplied by the ledger.
- The 158.09% result belongs to the conditional printed-equation quadrature sensitivity path; it is not hidden or automatically classified as an experimental error.
- P04/P05/P06 numerical comparisons are consistency checks, not independent validation.
