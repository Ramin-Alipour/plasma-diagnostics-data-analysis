# Selective Figure Digitization

> **Archive note:** The canonical release tables and decision log are under `datasets/dataset_b/publication_digitization/`. This top-level directory is retained as a historical workflow snapshot for compatibility; its manifest points to canonical Dataset B outputs. The legacy and canonical CSVs are not numerically identical in all derived peak estimates, so neither version is silently substituted for the other. They are two processing snapshots of the same publication figure, not independent datasets.

Digitization is used only where it adds quantitative information beyond tables/text. Each extracted point is labelled as **digitized from published figure**, never as raw experimental data.

## RC4 completed digitization: P06 Figure 2

Figure 2 of P06 contains three PSD panels for 1.9, 2.5 and 2.9 Torr. The publication describes the MHD activity as concentrated around 40–50 kHz and reports an approximately 44 kHz maximum. RC4 now performs a real pixel-to-axis digitization of the published figure rendering and stores:

- `p06_figure2_digitized.csv` — digitized frequency/amplitude traces with pixel coordinates and calibration uncertainty.
- `p06_figure2_peak_summary.csv` — peak-frequency estimates from a median-smoothed digitized envelope.
- `CALIBRATION.md` — axis calibration and uncertainty conventions.

The legacy snapshot stores peak estimates of approximately 44.06, 41.03 and 46.10 kHz for 1.9, 2.5 and 2.9 Torr, respectively. The current canonical Dataset B snapshot stores approximately 42, 48 and 52 kHz for those panels, with a conservative ±3.1 kHz peak-selection uncertainty and ±0.35 kHz axis-calibration uncertainty. These are different figure-digitization/peak-picking outputs; both are approximate figure-derived estimates, not recovered raw spectra. Neither replaces the paper's text-reported approximately 44 kHz value. The canonical Dataset B manifest points to the current values, while this legacy snapshot is retained for traceability.

For P01–P05, exact tables, equations, reported numerical effects, or defensible non-pixel constraints currently provide stronger evidence than approximate figure digitization, so the release records an explicit `not_digitized` decision rather than manufacturing precision.
