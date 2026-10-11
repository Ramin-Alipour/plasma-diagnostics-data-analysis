# Dataset B — publication reconstruction

Dataset B contains publication-derived tables and selected figure digitization from six IR-T1 papers (P01–P06). It is distinct from Dataset A and is **not** Dataset A with synthetic noise added. The 1.3% relative-noise model applies only to a separate synthetic-data workflow, not to this publication reconstruction.

## Structure

- `publication_reconstruction/`: transcribed or reconstructed tables for P01–P06.
- `publication_digitization/`: the 423-row P06 Figure 2 digitization, peak summary, and digitization decision log.
- `source_manifest.csv`: file-level source basis and Git blob fingerprints checked against exact file bytes by automated tests.
- `column_provenance.csv`: field-level provenance and interpretation.

## Provenance and precision

Keep directly reported values, equation-derived quantities, qualitative effects, approximate figure readings, and digitized estimates distinguishable. Preserve the precision printed in source tables; do not round source values merely to force a uniform number of decimal places, and do not normalize modal percentages to force their sum to 100%.

The P02 Table 2 values in Dataset B coincide with Dataset A's E02 modal table. This is consistent with Dataset A containing the original measurements underlying the publication and Dataset B transcribing the published table. The overlap is not evidence that either file is synthetic, but the pair is not independent validation.

For P04, average radial/poloidal electric-field powers and transport values have been re-transcribed from the paper's Results/Conclusion text at the precision reported by the authors. Maximum-current and steady-state entries remain figure-level estimates. For P06, steady-state times are stated in the article text; dominant-frequency estimates have been aligned with the Figure 2 peak digitization and rounded to 0.01 kHz. Their digitization uncertainty is approximately 0.35 kHz, so two decimal places are numeric formatting, not a claim of ±0.01 kHz accuracy.

The owner reports that E06 in Dataset A came from the diagnostic software, and it remains unchanged pending provenance review. Its frequency/amplitude and pixel-coordinate columns do not establish that it is a raw time-domain waveform; do not treat it as a PSD input without original time-series samples and sampling metadata. Numerical similarity alone does not establish E06's origin, and the owner's declaration is not independent acquisition-log verification.

A passing software test is not independent experimental validation. Do not add synthetic noise to Dataset B or alter source values to manufacture agreement or disagreement.
