# Dataset B — publication reconstruction

Dataset B contains publication-derived tables and selected digitization from six IR-T1 papers (P01–P06). It is distinct from Dataset A and is **not** Dataset A with synthetic noise added. The 1.3% relative-noise model applies only to a separate synthetic-data workflow, not to this publication reconstruction.

## Structure
- `publication_reconstruction/`: reconstructed/transcribed tables for P01–P06.
- `publication_digitization/`: the complete 423-row P06 Figure 2 digitization, peak summary, and digitization decision log.
- `source_manifest.csv`: file-level source basis and Git blob fingerprints checked against exact file bytes by automated tests.
- `column_provenance.csv`: field-level provenance and interpretation.

## Provenance classes
Keep directly reported values, equation-derived quantities, qualitative effects, approximate reconstruction values, and digitized estimates distinguishable. In particular, P04 absolute E-field/transport values remain approximate; do not cite them as exact table transcriptions. Do not normalize modal percentages to force their sum to 100%.

E06 in Dataset A is owner-confirmed output from the diagnostic's own software and is preserved as supplied. Dataset B's P06 digitization is separately derived from the publication figure. Numerical similarity does not override the owner's source declaration and must not be used to reclassify Dataset A. A passing software test is not independent experimental validation.
