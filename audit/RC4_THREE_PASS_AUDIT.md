# RC4.2 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: P01 SOURCE-INTERNAL DISCREPANCY IDENTIFIED; REVIEW REMAINS OPEN**

- P01's paper states a quadrature resolution formula in Eq. (3), with instrumental FWHM 0.03704 nm and diffraction λ/(1.35×10^5). That yields about 0.03716–0.03725 nm for the selected wavelength range.
- Table VI instead lists about 0.04003–0.04098 nm, values that closely track the linear sum of instrumental and diffraction terms. The current equation-based model gives about 158.09% mean absolute relative temperature difference (reconstructed mean 34.2167 eV vs reported mean 25.3133 eV). The table/equation mismatch is documented; neither source values nor reported temperatures are altered to force agreement. See `audit/P01_RESOLUTION_CONSISTENCY.md` and issue #11.
- P02 m=3 reconstruction remains within the documented computational threshold; the synthetic mode construction is not recovered raw data.
- P03 uncertainty is a bootstrap/model-sensitivity result because the source does not provide the original Mach time series.
- P04 keeps text-level transport targets separate from approximate absolute values in Dataset B; intermediate traces are synthetic.
- P05 numerical percentage effects are encoded parameterization targets, so agreement is a consistency check rather than independent validation.
- P06 synthetic signals use the text-level approximately 44 kHz target; comparison with approximate pressure-specific estimates has a mean absolute difference of about 0.628 kHz. Figure digitization remains a separate approximate result.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

**Result: PASS ON THE TESTED COMMIT**

- The latest previously completed full CI run passed 116 tests on Python 3.11, 3.12, and 3.13, including compilation, import checks, and installed-wheel smoke tests: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38128766220
- Audit-table synchronization, equation-implementation, and canonical notebook-path regression tests were included in that run.
- These tests establish software/repository consistency only; they do not adjudicate the paper's equation/table discrepancy.
- Notebook outputs were cleared after changing source paths; notebooks have not been represented as freshly executed in this pass.

## Pass 3 — Release integrity

**Result: NOT RELEASED; SCIENTIFIC REVIEW OPEN**

- PR #10 remains open and unmerged.
- No final public release or final archive verification is claimed in this audit.
- Static audit tables and scientific narratives distinguish consistency checks from independent validation.
- The P01 model/table discrepancy must remain explicit in any release notes and scientific description.

## Final scientific boundary

RC4.2 does not claim recovered IR-T1 raw shot data, new IR-T1 experiments after 2018, or confidential client datasets. Publication-derived constraints, approximate digitizations, and synthetic measurements remain separate evidence classes.
