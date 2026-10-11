# Dataset B — publication reconstruction

Dataset B contains publication-derived tables and selected figure digitization from six IR-T1 papers (P01–P06). It is distinct from Dataset A and is **not** Dataset A with synthetic noise added. The 1.3% relative-noise model applies only to a separate synthetic-data workflow, not to this publication reconstruction.

## Structure

- `publication_reconstruction/`: transcribed or reconstructed tables for P01–P06.
- `publication_digitization/`: the 423-row P06 Figure 2 digitization, peak summary, and digitization decision log.
- `source_manifest.csv`: file-level source basis and Git blob fingerprints checked against exact file bytes by automated tests.
- `column_provenance.csv`: field-level provenance and interpretation.
- `../DATASET_A_B_COMPARISON.md`: shared-field comparison of A and B using the software comparison module.

## Provenance and precision

Keep directly reported values, equation-derived quantities, qualitative effects, approximate figure readings, and digitized estimates distinguishable. Preserve the precision printed in source tables; do not round source values merely to force a uniform number of decimal places, and do not normalize modal percentages to force their sum to 100%.

The P02 Table 2 values in Dataset B coincide with Dataset A's E02 modal table. This is consistent with Dataset A containing the original values underlying the publication and Dataset B transcribing the published table. The overlap is not evidence that either file is synthetic, but the pair is not independent validation.

For P03, the abstract-reported edge potential (44 V), mean parallel Mach number (0.5), approximately zero perpendicular Mach number, and approximate parallel flow velocity (17 km/s) are included in addition to shared geometry/parameter values.

For P04, average radial/poloidal electric-field powers and transport values have been re-transcribed from the paper's Results/Conclusion text at the precision reported by the authors. In particular, the article text gives radial transport at +200 V and 2.3 Torr as -1.1e-3; Dataset A retains its owner-supplied +0.0010 value. This discrepancy is preserved and documented, not forced to match. Maximum-current and steady-state entries remain figure-level estimates.

For P06, steady-state times are stated in the article text; dominant-frequency estimates come from Figure 2 and are rounded to 0.01 kHz. The stored approximately 0.35 kHz uncertainty covers x-axis calibration only, not peak-selection uncertainty, so it does not imply ±0.01 kHz accuracy. The article does not report the 25–26, 35–36, and 45–46 ms analysis windows found in Dataset A; these windows are therefore blank in the publication-derived P06 table rather than copied from A.

The owner reports that E06 in Dataset A came from the diagnostic software, and it remains unchanged pending provenance review. Its frequency/amplitude and pixel-coordinate columns do not establish that it is a raw time-domain waveform; do not treat it as a PSD input without original time-series samples and sampling metadata. Numerical similarity alone does not establish E06's origin, and the owner's declaration is not independent acquisition-log verification.

A passing software test is not independent experimental validation. Do not add synthetic noise to Dataset B or alter source values to manufacture agreement or disagreement.
