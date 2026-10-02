# RC4.2 Three-Pass Audit

## Pass 1 — Scientific consistency

**Result: PASS**

- P01–P06 are explicitly classified by evidence type in `audit/SCIENTIFIC_AUDIT.md` and `audit/SCIENTIFIC_AUDIT_MATRIX.csv`.
- P01 mean relative reconstruction error remains about 0.91%; line-level deviations are retained rather than hidden.
- P02 m=3 reconstruction remains within the documented validation threshold.
- P03 uncertainty is explicitly treated as bootstrap/model sensitivity because the source does not provide the original Mach time series.
- P04 now produces deterministic but pressure-specific intermediate traces; published transport targets remain explicit constraints.
- P05 preserves the distinction between exact reported percentage effects and qualitative cases.
- P06 reproduces the reported dominant frequency near 44 kHz and keeps the source timing inconsistency explicit.
- Provenance contains 55 records.

## Pass 2 — Software and reproducibility

**Result: PASS**

- 96 automated tests passed after the RC4.2 changes.
- Python compilation and import checks passed.
- All 14 unique notebooks executed with zero notebook error outputs and zero unexecuted code cells.
- Notebook execution works without manually setting `PYTHONPATH`; a nested-working-directory execution was also verified.
- Two repeated master-audit runs returned identical summary DataFrames.
- P04 pressure-specific outputs were checked explicitly and are no longer identical by construction.

## Pass 3 — Release integrity

**Result: PASS**

- The release tree was cleaned of Python bytecode/cache artifacts before packaging.
- Archive structure, duplicate names, absolute paths, and forbidden generated artifacts are checked before the final checksum is generated.
- The final archive is extracted into a fresh directory and re-tested before being reported as the release candidate.
- SHA-256 is stored in the accompanying `.sha256` file.

## Final scientific boundary

RC4.2 does not claim recovered IR-T1 raw shot data, new IR-T1 experiments after 2018, or confidential client datasets. It is an evidence-oriented research portfolio connecting historical experimental diagnostics to current reproducible computational capability through publication-grounded reconstruction and explicit scientific boundaries.
