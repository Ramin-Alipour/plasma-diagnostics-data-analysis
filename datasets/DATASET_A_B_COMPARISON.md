# Dataset A/B comparison report

**Generated from the source tables and checked by** `plasma_provenance.dataset_comparison.compare_dataset_a_b()` **and** `tests/test_dataset_a_b_comparison.py`.

Dataset A values were not edited. Dataset B values were rechecked against the source publications where the article text/table was available. Equality is recorded, not manufactured. Exact overlap with a publication table is not independent validation.

## Shared-field comparisons

| Source | Comparison performed | Result | Interpretation |
|---|---|---:|---|
| P01 spectroscopy | 15 ion rows × wavelength and measured FWHM | 30/30 equal | The values overlap between the owner-supplied record and P01 Table VI. This is source overlap, not independent validation. |
| P02 hard X-ray | 6 time windows × counts, total energy, mean energy | 18/18 equal within (10^{-5}) keV | Counts and energy are transcribed from P02 Table 1; mean energy in B is derived from the table and rounded. |
| P02 modal table | 20 time windows × 6 modal percentages and edge safety factor | 140/140 equal | B transcribes P02 Table 2 at its printed precision. The exact A/B match is not independent validation and must not be “fixed” by changing values. |
| P03 compound probe | 11 shared geometry/parameter quantities | 11/11 equal | B now also records abstract-reported edge potential (44 V), mean parallel Mach number (0.5), approximately zero perpendicular Mach number, and approximate parallel flow (17 km/s), which are not present in A's shared-field subset. |
| P04 pressure/transport | 3 pressures × 2 average E-field powers and 6 transport values | 23/24 equal | One source discrepancy remains and is preserved below. |
| P05 limiter transport | A-derived percentage changes versus B-reported effects | 4/4 agree to within 0.6 percentage points | The values are related to the same published experiment; do not call this independent validation. |
| P06 pressure/MHD | A frequency field versus B digitized Figure 2 peaks | 3 approximate comparisons | The values differ by +0.51, −3.28, and −0.59 kHz at 1.9, 2.5, and 2.9 Torr, respectively. These are cross-source estimates, not a calibrated validation. |

## P04 discrepancy retained

At 2.3 Torr and +200 V, Dataset A contains `radial_transport_plus200 = +0.0010`. The P04 Results text reports the radial transport decreasing from (1.5\times10^{-3}) to (-1.1\times10^{-3}), so the re-extracted Dataset B value is `-0.0011`.

Neither value was overwritten. The difference is (-0.0021) in the encoded transport units. It is a genuine source/data discrepancy that requires interpretation; it is not evidence that either dataset should be edited to force agreement.

The remaining P04 transport values were re-transcribed from the article text:
- Radial, no bias: 0.0066, 0.0015, 0.0015.
- Radial, +200 V: 0.0043, −0.0011, 0.00036.
- Radial, −200 V: 0.0097, 0.0042, 0.0067.
- Poloidal, no bias: 0.0129, 0.0092, 0.0089.
- Poloidal, +200 V: 0.0161, 0.0197, 0.0103.
- Poloidal, −200 V: 0.0093, 0.0075, 0.0080.

Values are listed in pressure order 1.9, 2.3, and 2.7 Torr. Maximum-current and steady-state entries remain figure estimates.

## P06 peak-level check

The Dataset A diagnostic-output peak summary and the P06 Figure 2 digitization summary differ by approximately +0.258, −0.209, and −0.485 kHz for panels a, b, and c. The last difference exceeds the stored 0.355 kHz **x-axis calibration** uncertainty. That uncertainty does not include the uncertainty of selecting a peak from a broad, noisy spectral envelope, which is not quantified. Therefore, no claim of precise peak-level validation is made.

The P06 publication-derived table no longer carries the 25–26, 35–36, and 45–46 ms analysis windows that appeared in Dataset A: those windows are not reported in the cited paper, and the last interval also exceeds the paper's stated discharge duration. The field is blank in B rather than copied from A.

## E06 limitation

`e06_mhd_signal.csv` remains unchanged. It has pixel-coordinate, frequency, and amplitude columns and does not establish a raw time-domain waveform. The owner-reported diagnostic-software provenance is retained; the possibility of an acquisition/export problem is not presented as a verified fact. No time-domain PSD is computed from this file.

## Reproducibility and scientific boundary

Run `pytest tests/test_dataset_a_b_comparison.py tests/test_publication_reconstruction.py` to exercise the comparison and source-value regression checks. The tests check the corrected P04 values, the deliberately preserved A/B discrepancy, the absence of unreported P06 windows, and the explicit non-independence of exact source-table overlaps.

The comparison is a provenance/consistency audit, not a claim that all values are independent or experimentally validated. Synthetic reconstructions remain a separate third category and use the declared 1.3% relative-noise model only in synthetic outputs.
