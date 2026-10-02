# Selective Figure Digitization

Digitization is used only where it adds quantitative information beyond tables/text. Each extracted point is labelled as **digitized from published figure**, never as raw experimental data.

## RC4 completed digitization: P06 Figure 2

Figure 2 of P06 contains three PSD panels for 1.9, 2.5 and 2.9 Torr. The publication describes the MHD activity as concentrated around 40–50 kHz and reports an approximately 44 kHz maximum. RC4 now performs a real pixel-to-axis digitization of the published figure rendering and stores:

- `p06_figure2_digitized.csv` — digitized frequency/amplitude traces with pixel coordinates and calibration uncertainty.
- `p06_figure2_peak_summary.csv` — peak-frequency estimates from a median-smoothed digitized envelope.
- `CALIBRATION.md` — axis calibration and uncertainty conventions.

The digitized peak estimates are approximately 44.06, 41.03 and 46.10 kHz for 1.9, 2.5 and 2.9 Torr, respectively. They should be read as figure-derived estimates, not as recovered raw spectra and not as replacements for the paper's text-reported approximately 44 kHz value.

For P01–P05, exact tables, equations, reported numerical effects, or defensible non-pixel constraints currently provide stronger evidence than approximate figure digitization, so the release records an explicit `not_digitized` decision rather than manufacturing precision.
