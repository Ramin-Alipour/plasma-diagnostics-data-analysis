# RC4.2 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: OPEN CONSISTENCY CHECKS; P01 NEEDS SCIENTIFIC REVIEW**

- P01 mean absolute relative temperature difference is about 160.36% under the documented quadrature-resolution calculation. This discrepancy is retained as an open scientific-review item, not a pass.
- P02 m=3 reconstruction remains within the documented computational threshold; the synthetic mode construction is not recovered raw data.
- P03 uncertainty is a bootstrap/model-sensitivity result because the source does not provide the original Mach time series.
- P04 keeps text-level transport targets separate from approximate absolute values in Dataset B; intermediate traces are synthetic.
- P05 numerical percentage effects are encoded parameterization targets, so agreement is a consistency check rather than independent validation.
- P06 synthetic signals use the text-level approximately 44 kHz target; comparison with approximate pressure-specific estimates has a mean absolute difference of about 0.628 kHz. Figure digitization remains a separate approximate result.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

**Result: CURRENT HEAD CI PENDING**

- The last completed full CI run passed 113 tests on Python 3.11, 3.12, and 3.13, including compilation, import checks, and installed-wheel smoke tests: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38127009047
- Audit-table synchronization and notebook-path regression tests were added afterward. Their CI result must be checked before treating the current head as verified.
- Notebook outputs were cleared after changing source paths; notebooks have not been represented as freshly executed in this pass.

## Pass 3 — Release integrity

**Result: NOT RELEASED**

- PR #10 remains open and unmerged.
- No final public release or final archive verification is claimed in this audit.
- Static audit tables and scientific narratives distinguish consistency checks from independent validation.

## Final scientific boundary

RC4.2 does not claim recovered IR-T1 raw shot data, new IR-T1 experiments after 2018, or confidential client datasets. Publication-derived constraints, approximate digitizations, and synthetic measurements remain separate evidence classes.
