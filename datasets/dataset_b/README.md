# Dataset B — publication reconstruction

Dataset B contains publication-derived tables and selected digitization from six IR-T1 papers (P01–P06). It is distinct from Dataset A and is **not** Dataset A with synthetic noise added. The 1.3% relative-noise model applies only to a separate synthetic-data workflow, not to this publication reconstruction.

## Structure
- `publication_reconstruction/`: reconstructed/transcribed tables for P01–P06.
- `publication_digitization/`: digitization manifest and peak summary. The full `p06_figure2_digitized.csv` point-level file is still pending upload and must not be treated as present in this branch yet.
- `source_manifest.csv`: file-level source basis.
- `column_provenance.csv`: field-level provenance and interpretation.

## Provenance classes
Keep directly reported values, equation-derived quantities, qualitative effects, approximate reconstruction values, and digitized estimates distinguishable. In particular, P04 absolute E-field/transport values remain approximate; do not cite them as exact table transcriptions. Do not normalize modal percentages to force their sum to 100%.

A passing software test is not independent experimental validation.
