# Stage 3 — Scientific Audit (P01–P06)

## Purpose

This audit separates what is directly supported by the six publications from what is reconstructed, synthetic, assumed, or derived by this repository. A numerical comparison is treated as a consistency check of an encoded publication constraint, not as recovery of the original IR-T1 shot. Independent validation is claimed only where the source provides sufficient information for it.

## Evidence classes

- **published** — scientific statement or experimental result described by the source paper.
- **directly_extracted** — numerical value/range copied from a table or explicit textual statement.
- **reconstructed** — quantity calculated by applying a documented model or analysis method to reconstructed/synthetic inputs.
- **synthetic** — measurement-like data generated because the original raw array is unavailable.
- **assumed** — modelling or numerical choice not uniquely specified by the publication.
- **derived** — mathematically derived from an already documented value/model.
- **not_independently_validated** — repository quantity for which the publication does not provide enough information for an independent experimental validation.

## Paper-by-paper audit

| Paper | Published/direct evidence | Reconstruction | Synthetic/assumed layer | Independent validation boundary | Status |
|---|---|---|---|---|---|
| **P01** | Spectral lines, measured widths, published resolution model, reported ion temperatures | Synthetic CCD-like spectra → Gaussian fit → Eq. (3)/(11) quadrature resolution correction → Ti | amplitude, noise realization, pixel grid, spectral-window construction | Original CCD pixels, detector response, acquisition noise and complete calibration cannot be recovered; corrected resolution yields line-level temperature differences from the reported values | CONSISTENCY CHECK; see `audit/P01_RESOLUTION_CONSISTENCY.md` |
| **P02** | HXR counts/energies and 12-channel Mirnov modal percentages from tables | HXR event-energy reconstruction; spatial Fourier mode reconstruction; PSD/SVD summary | event-energy distribution width, sampling, phases, tiny noise, channel geometry idealization | Original HXR detector response and raw Mirnov traces unavailable | PASS; no causal HXR↔MHD claim |
| **P03** | Probe geometry, calibration factor k=1.7, Ti/Te, Te, plasma current, model equation | Synthetic collector-current ratio → Mach number + bootstrap sensitivity | Mach trajectory, current baseline, noise, sampling | No published raw collector-current time series; reconstructed Mach is not a recovered shot | PASS; model-constrained |
| **P04** | Pressures 1.9/2.3/2.7 Torr and reported transport constraints; bias cases reported in source | Synthetic potential → E → E×B → density fluctuation → turbulent-flux chain | potential waveform, phase, noise, B field, density construction; pressure-specific traces are synthetic | Reynolds-stress intermediate values are not claimed as published measurements; no raw probe traces | PASS; constrained model reconstruction |
| **P05** | Limiter positions/bias and explicitly reported percentage/qualitative effects | Parameterized field → E×B → transport observable scenarios | baseline signals and field-amplitude factors; qualitative cases are not converted into exact published numbers | No raw time series or transfer-function recovery | PASS; effect constraints remain attributed to publication |
| **P06** | 1.9/2.5/2.9 Torr, 44 kHz activity, timing windows, plasma parameters; Figure 2 digitization | Synthetic 12-channel Mirnov PSD + calibrated figure digitization | channel amplitudes, phases, noise, sampling | Figure digitization is an independent approximate extraction, not raw-data recovery; source timing inconsistency is preserved | PASS with timing limitation explicitly retained |

## Scientific interpretation rules

1. A `reported` number is never relabeled as a reconstructed measurement.
2. A reconstructed value that matches a reported target is described as a **consistency check**, not experimental discovery. A round-trip construction is not independent validation.
3. Synthetic intermediate traces are not presented as original IR-T1 signals.
4. Mathematical SVD components are not automatically assigned physical MHD mode numbers; P02 uses explicitly constructed spatial Fourier patterns because the publication reports mode-energy fractions.
5. P04 Reynolds stress is treated as a synthetic intermediate unless independently constrained by the source; only the published transport targets are used as quantitative calibration constraints.
6. P06 preserves the source paper's reported timing-window inconsistency rather than silently correcting it.

## Known numerical validation observations

- P01 uses the paper's stated quadrature resolution model. The corrected resolution is approximately 0.0372 nm across the selected lines; the resulting temperatures, especially for narrow metal lines, differ materially from the reported Table VII values. The repository records this as a consistency check rather than forcing agreement.
- P02 m=3 reconstruction is validated against the publication's tabulated modal fractions.
- P03 reports a reconstructed Mach number with bootstrap uncertainty because the source does not provide a numerical time-series Mach value for direct recovery.
- P04 exactly targets the published transport constraints by construction; this is a calibration/constraint test, not an independent measurement validation.
- P05 uses the explicitly reported numerical percentage effects as parameterization targets; matching them is a round-trip consistency check, not independent validation, and qualitative source statements remain qualitative.
- P06 recovers the reported dominant frequency near 44 kHz and separately stores calibrated Figure 2 digitization.

## Release decision from Stage 3

The scientific layer is acceptable for a release candidate **only with the above boundaries stated explicitly**. No paper is represented as an exact raw-data reproduction. The principal corrective action identified by this audit was P04's identical intermediate pressure traces and the documentation/provenance-count/version inconsistencies; these are corrected in RC4.2.
