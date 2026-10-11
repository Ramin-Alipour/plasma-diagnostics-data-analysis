# RC4.3 Master Reconstruction Audit

This is a software reconstruction/consistency audit, not a claim of independent experimental validation. Dataset A, publication-derived Dataset B, and synthetic outputs are separate evidence classes. Dataset A values were not edited in the source-re-extraction branch.

## Synthetic reconstruction summary

| Paper | Input basis | Computational workflow | Observable | Interpretation |
|---|---|---|---|---|
| P01 | Owner-supplied experimental measurements plus source-table constraints | Experimental data are the scientific basis; synthetic spectrum is test-only | Ion temperature | No synthetic-spectrum discrepancy is reported as an experimental result. |
| P02 | P02 Tables 1–2 | HXR spectrum and spatial Fourier-mode reconstruction | Modal fractions / HXR energy | Numerical reconstruction is a software consistency check. Exact A/B overlap with Table 2 is not independent validation. |
| P03 | Reported probe geometry and parameters | Synthetic collector currents → current ratio → Mach estimate | Mach number | Model-constrained reconstruction; original raw collector-current series is not in the archive. |
| P04 | Article-text transport constraints | Potential → electric field → E×B → transport statistics | Radial/poloidal transport proxies | Text constraints and source-derived table values remain explicit; A/B discrepancy is retained. |
| P05 | Reported limiter position, bias, and percentage effects | Parameterized E-field → E×B → transport observables | Reported percentage effects | Consistency check against published effects; not independent validation. |
| P06 | General Table 1 ranges, text-reported steady-state times, and digitized Figure 2 | Synthetic 12-channel Mirnov signals → PSD | Dominant frequency | Synthetic target is approximately 44 kHz. Figure-derived pressure-specific estimates remain approximate; peak-selection uncertainty is not quantified. |

## Dataset A/B comparison results

The reproducible implementation is `plasma_provenance.dataset_comparison.compare_dataset_a_b()`. Regression assertions are in `tests/test_dataset_a_b_comparison.py`.

| Source | Shared-field result | Boundary |
|---|---:|---|
| P01 spectroscopy | 30/30 equal | Published-table overlap, not independent validation. |
| P02 HXR | 18/18 equal within (10^{-5}) keV | Table 1 transcription; mean energy in B is derived. |
| P02 modes | 140/140 equal | Exact Table 2 transcription overlap, not independent validation. |
| P03 compound probe | 11/11 equal | B additionally records abstract-reported potential and flow values. |
| P04 pressure/transport | 23/24 equal | At 2.3 Torr, +200 V: A = +0.0010; article-text B = −0.0011. Neither value is overwritten. |
| P05 limiter transport | 4/4 reported effects agree within test tolerance | Same-experiment consistency check. |
| P06 MHD | 3 pressure-frequency and 3 peak-summary comparisons | Approximate A/B comparisons; at least one peak difference exceeds stored x-axis calibration uncertainty. |

## Source corrections in this branch

- P03: added abstract-reported edge potential (44 V), mean parallel Mach number (0.5), approximately zero perpendicular Mach number, and approximate parallel flow (17 km/s).
- P04: corrected radial transport at +200 V and 2.3 Torr to −1.1 × 10⁻³; corrected the pressure ordering of the poloidal transport values.
- P06: removed the unreported 25–26, 35–36, and 45–46 ms windows from publication-derived constraints. The synthetic generator may use these as workflow windows, but they are not claimed to be reported in the paper.
- Added `datasets/DATASET_A_B_COMPARISON.md` with the comparison detail and interpretation limits.

## P01 and source integrity

P01 scientific analysis is based on the owner-supplied laboratory measurements. The legacy synthetic CCD-like spectrum was a software-development scaffold, not the experimental dataset; its comparison against publication-derived values is withdrawn from scientific reporting.

Source values in Dataset B are not modified to conceal technique, create artificial differences, or force agreement with Dataset A. Table values retain published precision. Figure-derived values retain their uncertainty and are not presented as exact measurements.

## E06 limitation

The owner reports that `datasets/dataset_a/laboratory_signal_analysis/e06_mhd_signal.csv` came from the diagnostic software; its values remain unchanged. The file's pixel-coordinate/frequency/amplitude columns do not establish a raw time-domain waveform. A possible acquisition/export issue remains a hypothesis. No time-domain PSD is computed from this file without a valid waveform and sampling metadata.

## Release status

RC4.3 remains a release candidate. GitHub Actions run 834 passed across Python 3.11, 3.12, and 3.13. No tag was changed, no release was published, and no pull request was merged.
