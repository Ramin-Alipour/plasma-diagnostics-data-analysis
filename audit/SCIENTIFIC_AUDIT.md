# Stage 3 — Scientific Audit (P01–P06)

## Purpose and evidence classes

This audit separates published evidence from reconstructed, synthetic, assumed, and derived quantities. Numerical agreement with values from the same paper is a table-reproduction or consistency check, not independent experimental validation.

- **published** — statement or result described by the source paper.
- **directly_extracted** — value copied from a table or explicit text.
- **reconstructed** — quantity calculated by a documented model.
- **synthetic** — measurement-like data generated because original raw arrays are unavailable.
- **assumed** — modelling choice not uniquely specified by the publication.
- **derived** — mathematically derived from a documented value/model.
- **not_independently_validated** — source lacks data needed for independent experimental validation.

## Paper-by-paper audit

| Paper | Published/direct evidence | Reconstruction | Synthetic/assumed layer | Independent validation boundary | Status |
|---|---|---|---|---|---|
| **P01** | Author-supplied laboratory measurements; publication-derived values separately retained | Author-supplied experimental analysis; synthetic spectrum is test-only | Not applicable to the experimental data basis | Some publication values were intentionally approximate/different to protect sensitive diagnostic know-how | **AUTHOR DATA BASIS** |
| **P02** | HXR counts/energies and 12-channel Mirnov modal percentages from tables | HXR event-energy reconstruction; spatial Fourier mode reconstruction; PSD/SVD summary | event-energy distribution width, sampling, phases, noise, idealized channel geometry | Original HXR detector response and raw Mirnov traces unavailable | PASS; no causal HXR↔MHD claim |
| **P03** | Probe geometry, calibration factor k=1.7, Ti/Te, Te, plasma current, model equation | Synthetic collector-current ratio → Mach number + bootstrap sensitivity | Mach trajectory, current baseline, noise, sampling | No published raw collector-current time series | PASS; model-constrained |
| **P04** | Text-level transport constraints; Dataset B absolute E-field/transport values separately labelled approximate | Synthetic potential → E → E×B → density fluctuation → turbulent-flux chain | potential waveform, phase, noise, B field, density construction | No raw probe traces; absolute CSV values are not exact table transcriptions | CONSISTENCY CHECK |
| **P05** | Limiter positions/bias and explicitly reported percentage/qualitative effects | Parameterized field → E×B → transport scenarios | baseline signals and field-amplitude factors | No raw time series or transfer-function recovery; numerical targets encoded in model | CONSISTENCY CHECK; not independent validation |
| **P06** | Text-level approximately 44 kHz activity, timing windows, plasma ranges; approximate pressure-specific estimates and Figure 2 digitization | Synthetic 12-channel Mirnov PSD + canonical Dataset B figure digitization | channel amplitudes, phases, noise, sampling | Figure peaks and pressure-specific frequencies approximate; source timing inconsistency retained | CONSISTENCY CHECK |

## P01 data provenance and reporting decision

The lead author confirms that the laboratory measurements supplied for P01 are real experimental data. Some publication values were intentionally reported approximately or differently to protect sensitive diagnostic know-how. The legacy synthetic CCD-like spectrum was a software-development scaffold and is not the experimental dataset. Its comparison with publication values is withdrawn from scientific reporting; it is not a reportable experimental discrepancy.



- **Primary table-reproduction mode:** mean reported temperature 25.313333 eV; mean reproduced temperature 25.314270 eV; mean absolute relative difference **0.042015%**; maximum absolute relative difference about 0.177%.
- **Alternative printed-equation model:** previous deterministic synthetic-spectrum audit yielded about **158.09%** mean absolute relative temperature difference and mean reconstructed temperature about 34.2167 eV. This remains visible as a sensitivity result.
- Table VI resolution values closely track the linear sum of 0.03704 nm and λ/(1.35×10^5), while Eq. (3) specifies quadrature. This is a source-internal numerical inconsistency; author intent cannot be inferred from the numbers alone.
- Table reproduction uses directly tabulated Doppler FWHM and Eq. (16); it is not independent validation and does not recover original CCD frames.

## Interpretation rules

1. Reported values are never relabelled as reconstructed measurements.
2. Agreement with constraints from the same paper is a consistency check, not experimental discovery.
3. Synthetic intermediate traces are not original IR-T1 signals.
4. SVD components are not automatically assigned physical MHD mode numbers; P02 uses explicit spatial Fourier construction.
5. P04 Reynolds stress is a synthetic intermediate unless independently constrained by the source.
6. P06 preserves the source timing-window inconsistency.
7. P01 scientific conclusions must use author-supplied laboratory measurements; synthetic test outputs are not reported as experimental results.

## Release boundary

Software CI may pass while scientific limitations remain. No original IR-T1 raw diagnostic arrays are distributed. Dataset A remains laboratory/device-software data; Dataset B remains publication-derived; synthetic data remain a separate evidence class.
