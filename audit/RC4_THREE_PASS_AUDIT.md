# RC4.3 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: P01 analysis uses author-supplied experimental data; synthetic-spectrum comparison withdrawn from reporting**

- The lead author confirms the P01 laboratory measurements supplied to the project are real experimental data. Some publication values were intentionally approximate/different to protect sensitive diagnostic know-how.
- The early synthetic CCD-like spectrum was a software-development scaffold, not experimental data. Its comparison with publication values is withdrawn; no such discrepancy is reported as an experimental result.

- P03 uncertainty is bootstrap/model sensitivity because the original Mach time series is unavailable.
- P04 keeps text-level transport targets separate from approximate Dataset B values.
- P05 numerical effects are encoded parameterization targets, not independent validation.
- P06 synthetic signals use the text-level approximately 44 kHz target; approximate pressure-specific estimates differ by about 0.628 kHz.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

- Previous CI passed 117 tests on Python 3.11, 3.12, and 3.13: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38129754091
- The legacy synthetic-mode code is retained for software regression tests only; its outputs are excluded from P01 scientific results.
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
