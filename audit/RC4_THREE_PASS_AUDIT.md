# RC4.2 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: OPEN SCIENTIFIC REVIEW — P01 RESOLUTION INTERPRETATION UNRESOLVED**

- P01 mean absolute relative temperature difference is about 158.09% in the current deterministic audit run using the repository's present quadrature-resolution interpretation. The same source table contains resolution values near 0.0400–0.0410 nm while the model gives about 0.0372 nm. This source/model discrepancy is open; code tests do not determine which interpretation is physically correct. See `audit/P01_RESOLUTION_CONSISTENCY.md`.
- P02 m=3 reconstruction remains within the documented computational threshold; the synthetic mode construction is not recovered raw data.
- P03 uncertainty is a bootstrap/model-sensitivity result because the source does not provide the original Mach time series.
- P04 keeps text-level transport targets separate from approximate absolute values in Dataset B; intermediate traces are synthetic.
- P05 numerical percentage effects are encoded parameterization targets, so agreement is a consistency check rather than independent validation.
- P06 synthetic signals use the text-level approximately 44 kHz target; comparison with approximate pressure-specific estimates has a mean absolute difference of about 0.628 kHz. Figure digitization remains a separate approximate result.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

**Result: PASS ON THE TESTED COMMIT**

- The latest reported full CI run passed 116 tests on Python 3.11, 3.12, and 3.13, including compilation, import checks, and installed-wheel smoke tests: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38128766220
- Audit-table synchronization, P01 formula-implementation, and canonical notebook-path regression tests are included in that run.
- These tests establish software/repository consistency only; they do not close the P01 scientific interpretation.
- Notebook outputs were cleared after changing source paths; notebooks have not been represented as freshly executed in this pass.

## Pass 3 — Release integrity

**Result: NOT RELEASED; SCIENTIFIC REVIEW OPEN**

- PR #10 remains open and unmerged.
- No final public release or final archive verification is claimed in this audit.
- Static audit tables and scientific narratives distinguish consistency checks from independent validation.
- Do not describe the repository as scientifically release-ready until P01's equation/table discrepancy has been reconciled against the original source.

## Final scientific boundary

RC4.2 does not claim recovered IR-T1 raw shot data, new IR-T1 experiments after 2018, or confidential client datasets. Publication-derived constraints, approximate digitizations, and synthetic measurements remain separate evidence classes.
