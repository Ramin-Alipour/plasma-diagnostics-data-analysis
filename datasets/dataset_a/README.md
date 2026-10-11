# Dataset A — laboratory/device-linked data

This directory preserves the laboratory dataset as a distinct evidence set. The files are supplied as laboratory/device- and acquisition-software-linked data, as confirmed by the dataset owner. Do not relabel these files as publication transcriptions merely because some values overlap with quantities discussed in papers.

## Structure
- `laboratory_measurements/`: tabular diagnostic measurements and summaries.
- `laboratory_signal_analysis/`: derived signal-analysis outputs and manifest. The full `e06_mhd_signal.csv` source file is still pending upload and must not be treated as present in this branch yet.
- `source_manifest.csv`: source-file inventory.

## Important boundary
Dataset A and Dataset B are separate and must not be merged into a single experimental series. Preserve original precision and provenance. A software test checks data handling or arithmetic; it does not independently validate the physical measurements.
