# P01 Resolution Consistency and Dual-Mode Reconstruction

## Decision

The primary P01 audit now compares the paper's Eq. (16)-calculated-temperature column against its reported-temperature column. A separate formula recalculation from rounded Doppler widths is also retained, and the printed-equation quadrature model remains available as a sensitivity analysis. No published values are modified.

The paper contains a numerical inconsistency: Eq. (3) specifies quadrature combination of instrumental and diffraction broadening, but Table VI resolution values around 0.04003–0.04098 nm closely track the linear sum of 0.03704 nm and wavelength/(1.35 × 10^5). The equation-based result is not silently discarded.

## Mode A — published-table reproduction (primary audit)

This mode uses the published Table VI Doppler FWHM values and Eq. (16) to reproduce the Table VII temperature calculation.

- Mean reported temperature: 25.313333 eV
- Mean reproduced temperature: 25.314270 eV
- Mean absolute relative difference: **0.042015%**
- Maximum absolute relative difference across 15 rows: about 0.177%

This small residual is a rounded-table reproduction result, not independent experimental validation: the widths and comparison temperatures are reported by the same paper.

## Mode B — printed-equation quadrature model (alternative/sensitivity)

The model uses instrumental FWHM 0.03704 nm, diffraction FWHM λ/(1.35 × 10^5), and the quadrature resolution formula printed in Eq. (3). The previous deterministic synthetic-spectrum audit yielded about **158.09%** mean absolute relative temperature difference and a mean reconstructed temperature about 34.2167 eV versus the reported mean 25.3133 eV.

This value remains visible as the alternative equation-model outcome. It is not the primary table-reproduction metric, but it is not erased.

## Interpretation and safeguards

The two modes answer different questions:
- Table reproduction asks whether the directly tabulated Doppler widths reproduce the temperatures in the same publication.
- The equation model asks what results from applying the printed quadrature formula to measured FWHM values.

The near-match of Table VI to the linear sum is evidence of a source-internal numerical inconsistency, not proof of author intent. No raw CCD frames or independent calibration data are available.

The API supports explicit resolution modes: reconstruct_paper1_full(..., resolution_mode="tabulated") and reconstruct_paper1_full(..., resolution_mode="equation"). The master audit reports table reproduction as its primary comparison and retains the equation-model results separately. Both preserve original Dataset B rows.
