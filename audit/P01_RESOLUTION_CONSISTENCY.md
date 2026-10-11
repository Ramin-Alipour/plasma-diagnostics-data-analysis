# P01 Resolution Consistency Note

## Status: OPEN — source-level scientific review required

The current reconstruction implements the repository's present transcription of the P01 resolution equations:

- instrumental broadening used by the code: `Δλ_instrumental = 0.03704 nm`
- total ruling number used by the code: `N = 1.35 × 10^5`
- diffraction term: `Δλ_diffraction = λ / N`
- model resolution: `Δλ_resolution = sqrt(Δλ_instrumental² + Δλ_diffraction²)`
- Doppler width: `Δλ_Doppler = sqrt(Δλ_measured² − Δλ_resolution²)`

This calculation gives a resolution near 0.0372 nm over the selected 410–537 nm lines. However, the same Dataset B table records resolution values near 0.0400–0.0410 nm. That mismatch is scientifically material and means the equation transcription, meaning of the quoted 0.03704 nm instrumental value, slit-width conditions, and table's resolution column must be reconciled against the original paper before the reconstruction can be called scientifically resolved.

## What the code currently does — and does not establish

- `advanced.py` and `validation.py` consistently implement the quadrature expression above.
- The tabulated resolution values remain preserved as source evidence and are emitted separately from the model-derived values.
- The implementation and its tests establish software consistency with the selected formula; they do **not** establish that this interpretation fully reproduces the paper's resolution calibration.
- Do not overwrite the published resolution values, reported temperatures, or Dataset B source records to force agreement.

## Observed consequence

Under the current model-derived resolution, the deterministic master audit gives a mean absolute relative temperature difference of about 158.09% and a reconstructed mean temperature of about 34.2167 eV versus a reported mean of about 25.3133 eV. Treat this as an **open source/model consistency discrepancy**, not as evidence that the paper is wrong or that the current model is definitively correct.

## Required scientific closure

Before a scientific release claim, compare the original paper's equations and definitions with the exact Table VI entries and verify:

1. whether 0.03704 nm is the complete instrumental FWHM for the same slit and measurement conditions used in Table VI;
2. whether the diffraction term is exactly λ/N with N = 1.35 × 10^5 in the same width convention;
3. whether the tabulated resolution contains additional broadening/calibration contributions or uses a different convention;
4. whether measured, instrumental, resolution, and Doppler widths are all FWHM quantities and are combined in the stated way.

Until those points are resolved from the source, report both the table values and the model-derived values separately and retain P01 as **OPEN SCIENTIFIC REVIEW**.

The synthetic Gaussian generation remains a computational round trip: it is generated from published measured FWHM values, fitted back, and corrected with the current candidate resolution model. It is not independent experimental validation and does not recover original CCD frames.
