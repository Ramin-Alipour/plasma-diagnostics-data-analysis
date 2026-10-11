# Dataset A — laboratory/device-linked archive

This directory preserves the owner-supplied Dataset A files separately from publication reconstructions. The archive contains tabular diagnostic measurements and an E06 file whose provenance is unresolved.

## Structure
- `laboratory_measurements/`: tabular diagnostic measurements and summaries.
- `laboratory_signal_analysis/`: E06 archived table and analysis summary.
- `source_manifest.csv`: source-file inventory.

## Important provenance warning
The E06 file `laboratory_signal_analysis/e06_mhd_signal.csv` has 423 rows of pixel coordinates, frequency-axis values, and amplitudes that duplicate P06 Figure 2 digitization in Dataset B. It is preserved to avoid dropping archived content, but it must **not** be treated as verified raw hardware output. See `../PROVENANCE_CONFLICTS.md`.

Dataset A and Dataset B must not be merged into one experimental series. A passing arithmetic or software test does not independently validate physical measurements.
