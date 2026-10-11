# RC4.3 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: P01 dual-mode consistency check; source-internal equation/table discrepancy remains documented**

- Primary P01 table-reproduction mode uses published Table VI Doppler FWHM values with Eq. (16): mean reported temperature 25.313333 eV; mean reproduced temperature 25.314270 eV; mean absolute relative difference **0.042015%**, maximum about 0.177%.
- The separate printed-equation model uses instrumental FWHM 0.03704 nm and diffraction λ/(1.35×10^5), combined in quadrature. Its previous deterministic synthetic-spectrum result was about **158.09%** mean absolute relative difference (mean reconstructed 34.2167 eV vs reported 25.3133 eV). It remains a distinct sensitivity result.
- Table VI resolution values closely track the linear sum while Eq. (3) states quadrature. The source-internal discrepancy is documented; no source values are changed.
- P02 m=3 reconstruction remains within the documented computational threshold; synthetic mode construction is not recovered raw data.
- P03 uncertainty is bootstrap/model sensitivity because the original Mach time series is unavailable.
- P04 keeps text-level transport targets separate from approximate Dataset B values.
- P05 numerical effects are encoded parameterization targets, not independent validation.
- P06 synthetic signals use the text-level approximately 44 kHz target; approximate pressure-specific estimates differ by about 0.628 kHz.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

- Previous CI passed 117 tests on Python 3.11, 3.12, and 3.13: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38129754091
- Dual-mode P01 code and tests require a fresh CI run before this pass can be marked successful.
- Tests establish software consistency, not author intent or independent experimental validation.
- Notebook outputs were cleared after source-path changes; notebooks have not been represented as freshly executed.

## Pass 3 — Release integrity

**Result: NOT RELEASED; scientific caveat remains**

- PR #10 remains open and unmerged.
- No final public release or final archive verification is claimed.
- Static audit tables distinguish primary table reproduction from the alternative equation-model result.
- Keep the source-internal equation/table discrepancy explicit in scientific descriptions.

## Final scientific boundary

RC4.3 does not claim recovered IR-T1 raw shot data, new IR-T1 experiments after 2018, or confidential client datasets. Publication-derived constraints, approximate digitizations, and synthetic measurements remain separate evidence classes.
