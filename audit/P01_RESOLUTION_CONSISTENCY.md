# P01 Resolution Consistency Note

## Status: SOURCE INCONSISTENCY IDENTIFIED; REVIEW ITEM REMAINS OPEN

Source paper: R. Alipour, M. Ghoranneviss, and A. Salar Elahi, “First investigation on plasma impurities of the IR-T1 Tokamak,” *AIP Advances* 7, 115303 (2017), DOI: 10.1063/1.4990869.

The paper gives these relevant statements:
- Eq. (3) defines resolution broadening as the quadrature sum of instrumental and diffraction broadening.
- Eq. (5) and the 5 μm slit calculation give instrumental broadening 0.03704 nm.
- Eq. (11) gives diffraction broadening λ/(1.35 × 10^5).
- Table VI, however, lists resolution values near 0.04003–0.04098 nm.

The tabulated values closely track the **linear sum** of 0.03704 nm and λ/(1.35 × 10^5), not the quadrature sum specified by Eq. (3). For example:

| Wavelength | Diffraction term | Eq. (3) quadrature result | Linear sum | Table VI resolution |
|---:|---:|---:|---:|---:|
| 409.731 nm | ≈0.003035 nm | ≈0.037164 nm | ≈0.040075 nm | 0.04003 nm |
| 537.149 nm | ≈0.003979 nm | ≈0.037253 nm | ≈0.041019 nm | 0.04098 nm |

This is a source-internal numerical inconsistency. The near-match to the linear sum is strong evidence of how the table values were obtained, but it does not establish author intent. The repository should not silently rewrite either the equation or the table.

## Current implementation

The current `advanced.py` and `validation.py` implementations follow the equation as printed:

- instrumental broadening: `Δλ_instrumental = 0.03704 nm`
- diffraction broadening: `Δλ_diffraction = λ / (1.35 × 10^5)`
- resolution: `Δλ_resolution = sqrt(Δλ_instrumental² + Δλ_diffraction²)`
- Doppler width: `Δλ_Doppler = sqrt(Δλ_measured² − Δλ_resolution²)`

The resulting model resolution is approximately 0.0372–0.0373 nm. Table VI's reported resolution values and Table VII's reported temperatures are preserved unchanged as publication evidence.

## Audit consequence

Under the equation-based model, the deterministic master audit gives a mean absolute relative temperature difference of about 158.09% and a reconstructed mean temperature of about 34.2167 eV versus a reported mean of about 25.3133 eV. This large difference is consistent with the identified equation/table discrepancy; it is not evidence that the publication is necessarily wrong or that the reconstructed temperature is an independently measured result.

## Decision and closure

- Keep the equation-based model explicit and preserve the table values separately.
- Keep the audit status **OPEN SCIENTIFIC REVIEW** and describe the result as a source-internal consistency discrepancy.
- Do not substitute the linear sum simply to reproduce Table VI/Table VII, and do not change published source values to force agreement.
- Before closing the issue, record a source-level decision on whether the reconstruction should prioritize the printed equation or the tabulated derived values. If a table-reproduction mode is added, label it separately from the equation-based model and test both against their own documented definitions.
- Recompute static audit tables only if that scientific decision changes the model or reported comparison.

The synthetic Gaussian generation remains a computational round trip based on published measured FWHM values. It is not independent experimental validation and does not recover original CCD frames.
