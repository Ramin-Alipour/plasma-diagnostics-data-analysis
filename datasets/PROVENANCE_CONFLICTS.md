# Dataset A / Dataset B provenance conflict — E06

**Status: unresolved. Do not interpret E06 as a verified raw detector time series.**

The archived file named `dataset_A_fixed/data/laboratory_signal_analysis/e06_mhd_signal.csv` contains 423 rows with `x_pixel`, `y_pixel`, frequency-axis values, and amplitudes. These values match the P06 Figure 2 digitization values in Dataset B after removing publication-specific columns and renaming the experiment identifier. This structure is consistent with figure digitization, not a time-domain raw magnetic-probe waveform.

The file has been preserved in Dataset A's archive path to avoid silently dropping archived content, but its original provenance needs resolution before scientific use.

- Dataset B's `p06_figure2_digitized.csv` remains the explicitly publication-derived, provenance-labeled copy.
- Dataset A's `e06_mhd_signal.csv` must not be described as raw hardware output until independent acquisition records or a separate source file establish that claim.
- No synthetic noise, interpolation, or new measurements were added.
- Software tests record this overlap as a known provenance warning, not as independent experimental corroboration.
