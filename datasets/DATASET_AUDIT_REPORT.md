# IR-T1 Dataset Audit — Summary

**Audit date:** 2026-10-11  
**Working branch:** `audit/reextract-dataset-b-20261011`

## Dataset categories

- **Dataset A:** owner-supplied laboratory/device/software records. Its scientific values were not edited in this audit.
- **Dataset B:** values transcribed or reconstructed from the six cited IR-T1 papers and selected figure digitization.
- **Synthetic outputs:** a separate, deterministic software-test workflow. The 1.3% relative-noise model applies to these synthetic outputs, not to Dataset B's publication-reference tables.

## Source re-extraction and corrections

### P01 spectroscopy
- Checked the 15 spectral lines against Tables VI–VII in the source PDF.
- Table-reported measured widths, resolution widths, Doppler widths, ion masses, and reported temperatures are preserved at source precision.
- Equation-derived temperatures remain clearly labelled as derived quantities; they are not presented as separate published measurements.

### P02 hard X-ray and modal table
- The six Table 1 counts/total-energy pairs are transcribed as published: counts = [5, 5, 6, 158, 182, 136]; total energy (keV) = [3301, 2842, 3475, 78458, 80505, 55808].
- Mean energy is derived as total energy / counts.
- All 20 rows of Table 2 are transcribed at printed precision. The exact match between A's E02 modal table and B's Table 2 transcription is retained because the source publication contains those values. It is not independent validation and is not a reason to alter either file.

### P03 compound probe
- Shared reported geometry/parameter values are preserved.
- Added the abstract-reported edge plasma potential (44 V), mean parallel Mach number (0.5), approximately zero perpendicular Mach number, and approximate parallel flow velocity (17 km/s).
- The Mach relation is kept separate as a model equation.

### P04 pressure/transport — corrected from article text
- Re-transcribed average radial/poloidal electric-field powers and transport values from the Results/Conclusion text.
- Correct radial transport under +200 V at 2.3 Torr is **−1.1 × 10⁻³**, not +0.36 × 10⁻³. The latter belongs to +200 V at 2.7 Torr.
- Correct poloidal transport under +200 V is [0.0161, 0.0197, 0.0103]; under −200 V it is [0.0093, 0.0075, 0.0080], ordered by 1.9, 2.3, and 2.7 Torr.
- Dataset A's +0.0010 value at 2.3 Torr remains unchanged. The source/data discrepancy is documented rather than concealed.
- The Results text reports maximum currents of about 20/22/22 kA and steady-state times of 12/11/10 ms; these are text-reported values, not figure estimates. The current values retain the paper's approximate wording.

### P05 limiter/transport — rechecked against Results and Conclusion
- The edge +200 V radial-transport reduction (~50%), the 5 mm +200 V radial-transport reduction (~35%), and the edge/5 mm Reynolds-stress reductions (15%/5%) are retained as the article's specific Results values.
- Corrected two earlier qualitative encodings: at 10 mm, Reynolds stress is described as showing wild fluctuations and a dramatic **increase** under applied voltages, not a reduction; at 5 mm with −200 V, the article says the bias was not effective in decreasing radial transport, rather than explicitly quantifying an increase.
- Added conclusion-level ranges separately: radial electric field +20–30%, poloidal electric field −30–40%, poloidal transport +25–35%, radial transport −35–45%, and Reynolds stress −5–10% for the 5 mm, +200 V case. The conclusion-level ranges are not silently substituted for the narrower figure/result statements.
- The four shared A-derived percentage checks remain a consistency check on related data, not independent validation.

### P06 pressure/MHD
- Table 1 general ranges are retained: electron density 0.7–1.5 × 10¹³ cm⁻³ and electron temperature 150–230 eV.
- Steady-state times 30.4, 28.5, and 27.8 ms are taken from article text.
- Figure 2 dominant-frequency values remain digitized estimates, not exact published numbers. The stored ~0.35 kHz value describes x-axis calibration uncertainty only; peak-selection uncertainty is not quantified.
- The 25–26, 35–36, and 45–46 ms analysis windows were removed from the publication-derived P06 table because they are not reported in the paper. The 45–46 ms interval also exceeds the article's stated discharge duration (<35 ms). The synthetic generator may still use these as synthetic workflow windows, but they are not labelled publication data.

## Software A/B comparison

The new `plasma_provenance.dataset_comparison.compare_dataset_a_b()` workflow compares shared fields without changing Dataset A. Its regression test records the results:
- P01: 30/30 shared wavelength/width checks equal.
- P02 HXR: 18/18 shared-field checks equal within the stated numerical tolerance.
- P02 modes: 140/140 shared numeric values equal; explicitly not independent validation.
- P03: 11/11 shared parameter checks equal.
- P04: 29/30 checks equal after including shared maximum-current and steady-state fields; the 2.3 Torr radial +200 V discrepancy remains visible.
- P05: 4/4 A-derived percentage effects agree with the reported B effects within the test tolerance.
- P06: all three shared steady-state times and the discharge-time upper bound match between A and B; pressure-specific frequencies and E06 peak-summary/figure-digitization values are compared as approximate estimates. The 2.9 Torr peak-summary difference exceeds the stored x-axis calibration uncertainty, which does not include peak-selection uncertainty.

See [DATASET_A_B_COMPARISON.md](DATASET_A_B_COMPARISON.md) for the full comparison table and discrepancy details.

## E06 provenance boundary

The owner confirms that `datasets/dataset_a/laboratory_signal_analysis/e06_mhd_signal.csv` came from the diagnostic software, and the file remains unchanged. Its columns (`x_pixel`, `y_pixel`, `frequency_kHz`, `amplitude`) do not establish that it is a raw time-domain waveform. A possible acquisition/export/processing problem remains a hypothesis, not a verified explanation. No time-domain PSD is computed from this file without a valid waveform and sampling metadata.

## Release boundary

This branch contains source corrections, an A/B comparison module, and regression tests. **CI status:** An earlier commit on this branch passed GitHub Actions across Python 3.11, 3.12, and 3.13. The subsequent P05 extraction corrections have new regression tests and must be judged by the latest workflow run before this branch is treated as validated. Dataset A was not edited; no tag was changed and no release was published.
