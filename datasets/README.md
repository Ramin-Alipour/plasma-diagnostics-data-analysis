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
Both Dataset A and Dataset B CSV files, source manifests, and provenance records are included in this branch. Dataset A contains laboratory/device/software-origin data; Dataset B contains publication-extracted/reconstructed data. The archives are integrated as separate directories and are checked by regression tests. Do not confuse this branch with a versioned public release.
