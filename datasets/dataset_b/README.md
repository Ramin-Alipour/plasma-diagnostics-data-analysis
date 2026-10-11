# Dataset B — publication reconstruction

Dataset B contains publication-derived tables and selected digitization from six IR-T1 papers (P01–P06). It is distinct from Dataset A and is **not** Dataset A with synthetic noise added. The 1.3% relative-noise model applies only to a separate synthetic-data workflow, not to this publication reconstruction.

## Structure
- `publication_reconstruction/`: reconstructed/transcribed tables for P01–P06.
- `publication_digitization/`: the complete 423-row P06 Figure 2 digitization, peak summary, and digitization decision log.
- `source_manifest.csv`: file-level source basis and Git blob fingerprints checked against exact file bytes by automated tests.
- `column_provenance.csv`: field-level provenance and interpretation.

## Provenance classes
Keep directly reported values, equation-derived quantities, qualitative effects, approximate reconstruction values, and digitized estimates distinguishable. In particular, P04 absolute E-field/transport values remain approximate; do not cite them as exact table transcriptions. Do not normalize modal percentages to force their sum to 100%.

The owner reports that E06 in Dataset A came from the diagnostic software, and it remains unchanged pending provenance review. Its frequency/amplitude and pixel-coordinate columns do not establish that it is a raw time-domain waveform; do not treat it as a PSD input without the original time-series samples and sampling metadata. Dataset B's P06 digitization is separately derived from the publication figure. Numerical similarity alone does not establish E06's origin, and the owner's declaration is not independent acquisition-log verification.\n\nThe P02 Table 2 values in Dataset B coincide with the values in Dataset A's E02 modal table. This is consistent with Dataset A containing the original measurements underlying the publication and Dataset B transcribing the published table. The overlap is not evidence that either file is synthetic, but it means this pair is not independent validation. Preserve source values and printed precision; do not round source tables to 0.01, normalize mode percentages, or add synthetic noise to Dataset B.\n\nP04 absolute E-field/transport entries and P06 pressure-specific estimates are currently labelled approximate; they have not been verified to ±0.01 accuracy. Figure-derived values require a documented calibration and uncertainty, and should not be described as accurate to 0.01 unless the source resolution supports that claim. A passing software test is not independent experimental validation.
