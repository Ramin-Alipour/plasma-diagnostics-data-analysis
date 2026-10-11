# P01 resolution and provenance audit

## Decision and provenance

Dataset A and Dataset B remain separate source records. Dataset A is the laboratory/device-side record; Dataset B is a publication-derived transcription/reconstruction. Shared identifiers or matching wavelength/FWHM fields do not make the datasets interchangeable, and neither dataset is to be overwritten by a reconciliation.

**Author-provided provenance statement (not an independently verified repository measurement):** the lead author reports that some numerical values were intentionally presented approximately or differently in the publication to make straightforward copying of the method/technique more difficult, while the underlying original values could be supplied upon request. This statement is recorded as author testimony; it is not inferred from the numerical discrepancy alone.

Any correspondence between the laboratory record and publication record must be an explicit, separately stored reconciliation layer. It must retain (1) original Dataset A values, (2) literal publication values in Dataset B, (3) mapping key and method, (4) any transformed/approximate value, and (5) origin and status of the rationale. No source CSV or source-table value may be silently replaced.

## Resolution equation discrepancy

The paper's Eq. (3) specifies quadrature combination of instrumental and diffraction broadening, while Table VI resolution values around 0.04003–0.04098 nm closely track the linear sum of 0.03704 nm and wavelength/(1.35 × 10^5). The printed equation and table values therefore define distinct analysis paths.

Quadrature combination is physically defensible if the broadening kernels are independent and Gaussian, because variances add. However, the repository does not contain original CCD frames or an independently measured instrumental line-spread function establishing those assumptions for this experiment. The quadrature calculation is a conditional model/sensitivity result, not an independently validated correction.

## Mode A — source-table consistency

This mode compares the paper's listed Eq. (16)-calculated temperatures against its reported temperatures. It does not independently recalculate the listed values.

- Mean reported temperature: 25.313333 eV
- Mean reproduced temperature: 25.314270 eV
- Mean absolute relative difference: **0.042015%**
- Maximum absolute relative difference across 15 rows: about 0.177%

Recalculation from the rounded Table VI Doppler FWHM values gives about 0.13623% mean absolute relative difference. These are source-table consistency checks, not independent experimental validation.

## Mode B — printed-equation quadrature sensitivity

The model uses instrumental FWHM 0.03704 nm, diffraction FWHM λ/(1.35 × 10^5), and the printed quadrature formula. A prior deterministic synthetic-spectrum run yielded about **158.09%** mean absolute relative temperature difference and a mean reconstructed temperature about 34.2167 eV versus the reported mean 25.3133 eV.

This large discrepancy must not be hidden by altering input values or forcing a match. Nor should it automatically be called an experimental error: it is the result of applying a conditional model to publication-derived inputs, whose provenance the lead author has clarified as potentially approximate/different from original laboratory values. The value remains a model-sensitivity result until a traceable reconciliation based on original values is available.

## Reconciliation protocol

1. Preserve Dataset A and Dataset B unchanged.
2. Keep the author-provided provenance statement clearly attributed as such.
3. Any approximate correspondence must live in a separate file/layer and record source row IDs, matching key, original values, transformed value, method, and rationale.
4. Do not derive an adjustment solely to reduce the 158.09% discrepancy. An adjustment is admissible only when grounded in a documented physical relation or a traceable author-supplied correspondence.
5. Do not describe P04/P05/P06 consistency checks as independent validation.
6. Keep the 1.3% relative-noise convention confined to synthetic data generation; it does not modify Dataset B.

The API supports explicit resolution modes: `reconstruct_paper1_full(..., resolution_mode="tabulated")` and `reconstruct_paper1_full(..., resolution_mode="equation")`. These modes remain separate and preserve the publication-derived source rows.
