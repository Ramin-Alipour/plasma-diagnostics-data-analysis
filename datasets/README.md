# IR-T1 source datasets

This directory is being added to the repository as two **separate, non-interchangeable** evidence sets.

## Dataset A — laboratory data
Dataset A contains structured laboratory measurements and signal-analysis outputs associated with IR-T1 experiments. Some fields may originate from the instrument hardware, acquisition software, or downstream processing. They must not be automatically described as values transcribed from publications.

## Dataset B — publication reconstruction
Dataset B contains reconstructions from six published IR-T1 papers (P01–P06), including a selected digitization from P06 Figure 2. It is publication-derived and is **not** Dataset A with synthetic noise added. No 1.3% Gaussian-noise model or random seed applies to Dataset B.

## Provenance rules
- Keep A and B separate; never merge them into a continuous experimental series.
- Preserve source precision and the distinction between exact table transcription, reported ranges/effects, derived values, approximate reconstructions, and digitized points.
- Do not normalize mode percentages or silently change values to satisfy a consistency check.
- A passing software test is not independent physical validation.

## Current staged files
- `dataset_inventory.csv`: file-level provenance inventory for the publication-reconstruction set.
- `DATASET_AUDIT_REPORT.md`: current audit findings and unresolved checks.
- Source archives are intended to be stored under `source/` so the original file structure can be preserved before software integration. This branch is a staging PR; do not release or cite it as a versioned data release until the dataset archives and integration tests are present.
