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
| **P01** | Spectral lines, measured widths, printed quadrature equation, tabulated resolution and reported ion temperatures | Synthetic CCD-like spectra → Gaussian fit → equation-based quadrature correction → Ti | amplitude, noise realization, pixel grid, spectral-window construction | Original CCD pixels, detector response, acquisition noise and complete calibration cannot be recovered; the printed equation and Table VI resolution values are internally inconsistent | **OPEN SCIENTIFIC REVIEW**; see `audit/P01_RESOLUTION_CONSISTENCY.md` |
| **P02** | HXR counts/energies and 12-channel Mirnov modal percentages from tables | HXR event-energy reconstruction; spatial Fourier mode reconstruction; PSD/SVD summary | event-energy distribution width, sampling, phases, tiny noise, channel geometry idealization | Original HXR detector response and raw Mirnov traces unavailable | PASS; no causal HXR↔MHD claim |
| **P03** | Probe geometry, calibration factor k=1.7, Ti/Te, Te, plasma current, model equation | Synthetic collector-current ratio → Mach number + bootstrap sensitivity | Mach trajectory, current baseline, noise, sampling | No published raw collector-current time series; reconstructed Mach is not a recovered shot | PASS; model-constrained |
| **P04** | Text-level transport constraints; Dataset B absolute E-field/transport values are separately labelled approximate | Synthetic potential → E → E×B → density fluctuation → turbulent-flux chain | potential waveform, phase, noise, B field, density construction; pressure-specific traces are synthetic | No raw probe traces; absolute CSV values are not exact table transcriptions | CONSISTENCY CHECK; text-level calibration |
| **P05** | Limiter positions/bias and explicitly reported percentage/qualitative effects | Parameterized field → E×B → transport observable scenarios | baseline signals and field-amplitude factors; qualitative cases are not converted into exact published numbers | No raw time series or transfer-function recovery; numerical targets are encoded in the model | CONSISTENCY CHECK; not independent validation |
| **P06** | Text-level approximately 44 kHz activity, timing windows, plasma ranges; approximate pressure-specific estimates and Figure 2 digitization | Synthetic 12-channel Mirnov PSD + canonical Dataset B figure digitization | channel amplitudes, phases, noise, sampling | Figure peaks and pressure-specific frequencies are approximate, not raw PSD data; source timing inconsistency is preserved | CONSISTENCY CHECK with timing limitation explicitly retained |

## Scientific interpretation rules

1. A `reported` number is never relabeled as a reconstructed measurement.
2. A reconstructed value that matches a reported target is described as a **consistency check**, not experimental discovery. A round-trip construction is not independent validation.
3. Synthetic intermediate traces are not presented as original IR-T1 signals.
4. Mathematical SVD components are not automatically assigned physical MHD mode numbers; P02 uses explicitly constructed spatial Fourier patterns because the publication reports mode-energy fractions.
5. P04 Reynolds stress is treated as a synthetic intermediate unless independently constrained by the source; only the published transport targets are used as quantitative calibration constraints.
6. P06 preserves the source paper's reported timing-window inconsistency rather than silently correcting it.

## Known numerical validation observations

- **P01:** The source paper (Alipour et al., *AIP Advances* 7, 115303 (2017), DOI 10.1063/1.4990869) states a quadrature resolution formula in Eq. (3). With instrumental FWHM 0.03704 nm and diffraction λ/(1.35×10^5), it yields about 0.03716–0.03725 nm. Table VI instead gives 0.04003–0.04098 nm, numerically close to the linear sum. This source-internal discrepancy is documented in `audit/P01_RESOLUTION_CONSISTENCY.md`; the code follows the printed equation and preserves the table values unchanged. The deterministic equation-based audit reports about 158.09% mean absolute relative temperature difference (reconstructed mean 34.2167 eV vs reported mean 25.3133 eV). This is an open source/model consistency item, not independent experimental validation.
- **P02:** m=3 reconstruction is checked against the publication's tabulated modal fractions; the synthetic spatial basis is constructed, not raw data.
- **P03:** reconstructed Mach number and bootstrap uncertainty are model-derived because the source does not provide a numerical time-series Mach value for direct recovery.
- **P04:** the advanced chain targets text-level transport constraints by construction; Dataset B's absolute transport/E-field values are separate approximate reconstructions.
- **P05:** numerical percentage effects are parameterization targets; matching them is a round-trip consistency check, not independent validation.
- **P06:** synthetic signals use the text-level approximately 44 kHz activity as a consistency check; pressure-specific estimates and Figure 2 digitization are approximate and separate.

## Release decision

Software tests can pass while a source-level scientific discrepancy remains. Keep P01's equation/table inconsistency explicit in all scientific descriptions and release notes. No original IR-T1 raw diagnostic arrays are distributed. Dataset A remains laboratory/device-software data; Dataset B remains publication-derived; synthetic data remain a third, separate evidence class.
