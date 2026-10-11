# IR-T1 source datasets

This directory contains two **separate, non-interchangeable** evidence sets.

## Dataset A — laboratory data
Dataset A contains structured laboratory measurements and signal-analysis outputs associated with IR-T1 experiments. Some fields may originate from the instrument hardware, acquisition software, or downstream processing. They must not be automatically described as values transcribed from publications.

## Dataset B — publication reconstruction
Dataset B contains reconstructions from six published IR-T1 papers (P01–P06), including a selected digitization from P06 Figure 2. It is publication-derived and is **not** Dataset A with synthetic noise added. No 1.3% Gaussian-noise model or random seed applies to Dataset B.

## Provenance rules
- Keep A and B separate; never merge them into a continuous experimental series.
- Preserve source precision and the distinction between exact table transcription, reported ranges/effects, derived values, approximate reconstructions, and digitized points.
- Do not normalize mode percentages or silently change values to satisfy a consistency check.
- A passing software test is not independent physical validation.

## Integrated files
Both Dataset A and Dataset B CSV files, source manifests, and provenance records are included in the repository as separate directories and are checked by regression tests. Dataset A contains laboratory/device/software-origin data; Dataset B contains publication-extracted/reconstructed data. The published `v0.2.0` archive includes this integration and is archived at [Zenodo DOI 10.5281/zenodo.23298822](https://doi.org/10.5281/zenodo.23298822). Later commits on `main` are development updates and are not automatically part of that immutable versioned archive.

The top-level `dataset_inventory.csv` lists the publication-derived Dataset B records; `dataset_a/source_manifest.csv` and `dataset_b/source_manifest.csv` provide the respective file-level manifests for both evidence sets.

## P01 correspondence ledger
The non-destructive correspondence ledger is at `datasets/dataset_audit/p01_reconciliation.csv`. Its 15 matched rows share normalized ion, wavelength, and measured-FWHM values, but this is not proof of shared raw-data provenance. Reconciled numeric values remain blank; neither Dataset A nor Dataset B is overwritten. See `audit/P01_RECONCILIATION.md` and `audit/P01_RESOLUTION_CONSISTENCY.md`.
