# Dataset A/B comparison report

**Comparison workflow:** `plasma_provenance.dataset_comparison.compare_dataset_a_b()`; regression checks: `tests/test_dataset_a_b_comparison.py`.

Dataset A values were not edited. Dataset B values were rechecked against source publications where article text or tables were available. The report below gives numerical differences (Δ = B − A) wherever both datasets contain comparable values. Exact source-table overlap is not independent validation.

## Shared-field comparisons

| Source | Comparison performed | Numerical difference (Δ = B − A) | Interpretation |
|---|---|---|---|
| P01 spectroscopy | 15 ion rows × wavelength and measured FWHM | Wavelength: Δ = 0 nm for 15/15 rows; measured FWHM: Δ = 0 nm for 15/15 rows | Exact overlap with P01 Table VI at stored precision; source overlap, not independent validation. |
| P02 hard X-ray | 6 time windows × counts, total energy, mean energy | Counts: Δ = 0 for 6/6; total energy: Δ = 0 keV for 6/6; mean energy Δ(B−A): 0, 0, +0.0000033, −0.0000003, −0.0000048, −0.0000012 keV | Counts and total energy are transcribed from P02 Table 1; mean energy in B is derived and rounded. |
| P02 modal table | 20 time windows × 6 modal percentages and edge safety factor | Δ = 0 at stored precision across 140/140 numeric fields | B transcribes P02 Table 2. This source overlap is not independent validation and does not justify altering either dataset. |
| P03 compound probe | 11 shared geometry/parameter quantities | Δ = 0 at stored precision for 11/11 shared values | B also records abstract-reported edge potential (44 V), mean parallel Mach number (0.5), approximately zero perpendicular Mach number, and approximate parallel flow (17 km/s); these B-only fields have no A counterpart for a numerical Δ. |
| P04 pressure/transport | 3 pressures × current, steady-state time, 2 average E-field powers, and 6 transport values | 29 fields: Δ = 0 at stored precision; radial transport at 2.3 Torr, +200 V: Δ = −0.0021 | The one discrepancy is retained and detailed below. |
| P05 limiter transport | A-derived signed percentage changes versus B-reported direction and magnitude | A changes: −50.00%, −35.00%, −15.00%, −5.00%; magnitude residuals: 0.00 percentage points for all four | All four signed changes indicate reductions and all four B descriptions report reductions. The test rejects wrong-direction effects even when absolute magnitudes match. This is not independent validation. |
| P06 pressure/MHD | Shared steady-state times and discharge-time upper bound, plus A frequency versus re-digitized B Figure 2 peaks | Steady-state times: Δ = 0 ms for 3/3; discharge upper bound: Δ = 0 ms; frequency Δ(B−A): −1.8, +3.9, +5.8 kHz at 1.9, 2.5, 2.9 Torr | The +3.9 and +5.8 kHz differences exceed the conservative ±3.1 kHz peak-selection uncertainty. The article's general 40–50 kHz PSD band and approximate 44 kHz wavelet result are stored separately; the 2.9 Torr digitized estimate (~52 kHz) is retained with uncertainty, not forced to match. These are approximate cross-source comparisons, not independent validation. |

## P05 signed numerical comparison

The signed percentage change is calculated as \(100\,(\text{biased}-\text{baseline})/\text{baseline}\). Negative values mean reduction. The numerical checks are:

| Position | Quantity | Dataset A baseline | Dataset A biased | A change | Dataset B description | Magnitude residual |
|---:|---|---:|---:|---:|---|---:|
| 0 mm | Radial turbulent transport | 0.00660 | 0.00330 | −50.00% | Reduction about 50% | 0.00 percentage points |
| 5 mm | Radial turbulent transport | 0.00660 | 0.00429 | −35.00% | Reduction almost 35% | 0.00 percentage points |
| 0 mm | Reynolds stress | 0.012900 | 0.010965 | −15.00% | Reduction about 15% | 0.00 percentage points |
| 5 mm | Reynolds stress | 0.012900 | 0.012255 | −5.00% | Reduction about 5% | 0.00 percentage points |

The automated comparison checks the sign separately from the magnitude. A positive signed change paired with a reported reduction, or a negative signed change paired with a reported increase, fails even if the absolute percentages agree. The source text uses approximate language, so the 0.00 residuals mean agreement at the precision encoded in the A values and B descriptions—not independent experimental validation.

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

Values are listed in pressure order 1.9, 2.3, and 2.7 Torr. Maximum currents of about 20/22/22 kA and steady-state times of 12/11/10 ms are reported in the Results text; these are not figure estimates.

## P05 source re-extraction corrections

A closer pass through P05 Results (Figs. 5–7) corrected two misleading qualitative labels in the previous B table: at 10 mm, Reynolds stress is described as showing wild fluctuations and a dramatic **increase** under the applied external voltages, not a reduction; at 5 mm with −200 V, the article says the bias was not effective in decreasing radial transport, rather than explicitly quantifying an increase. The table now preserves the article's distinction between numerical effects (about 50%, almost 35%, 15%, and 5%), conclusion-level ranges (20–30%, 30–40%, 25–35%, 35–45%, and 5–10%), and qualitative figure descriptions. The four shared A-derived signed changes remain −50%, −35%, −15%, and −5%; the added B-only rows are not treated as independent validation.

## P06 signal-analysis peak-summary check

The Dataset A signal-analysis peak summary (`e06_mhd_peak_summary.csv`) and the **canonical Dataset B** P06 Figure 2 digitization (`datasets/dataset_b/publication_digitization/p06_figure2_peak_summary.csv`) differ by Δ(B−A) = **−2.056, +6.974, and +5.901 kHz** for panels a, b, and c, respectively. Only panel a falls within the conservative ±3.1 kHz peak-selection uncertainty; panels b and c exceed it. The ±0.35 kHz axis-calibration uncertainty is only one component and must not be substituted for the combined peak-selection uncertainty. The old top-level `data/publication_digitization/` files are a historical processing snapshot and are not the canonical Dataset B values. No claim of precise peak-level validation is made.

The P06 publication-derived table no longer carries the 25–26, 35–36, and 45–46 ms analysis windows that appeared in Dataset A: those windows are not reported in the cited paper, and the last interval also exceeds the paper's stated discharge duration. The field is blank in B rather than copied from A. The software comparison reports Δ = 0 ms for the three steady-state times (30.4, 28.5, 27.8 ms) and for the stated <35 ms discharge-time upper bound; the frequency values remain approximate and differ.

## E06 limitation

`e06_mhd_signal.csv` remains unchanged. It has pixel-coordinate, frequency, and amplitude columns and does not establish a raw time-domain waveform. The owner-reported diagnostic-software provenance is retained; the possibility of an acquisition/export problem is not presented as a verified fact. No time-domain PSD is computed from this file.

## Reproducibility and scientific boundary

Run `pytest tests/test_dataset_a_b_comparison.py tests/test_publication_reconstruction.py` to exercise the comparison and source-value regression checks. The tests check the corrected P04 values, the deliberately preserved A/B discrepancy, the absence of unreported P06 windows, and the explicit non-independence of exact source-table overlaps.

The comparison is a provenance/consistency audit, not a claim that all values are independent or experimentally validated. Synthetic reconstructions remain a separate third category and use the declared 1.3% relative-noise model only in synthetic outputs.
