# v0.1.0-rc4.2 — Scientific Audit and Reproducibility Candidate

RC4.2 follows the RC4 deep-reconstruction candidate and closes the next scientific/reproducibility review cycle.

## Stage 3 — Scientific Audit

- Added `audit/SCIENTIFIC_AUDIT.md` with explicit evidence classes and paper-by-paper boundaries.
- Added `audit/SCIENTIFIC_AUDIT_MATRIX.csv` for machine-readable traceability.
- Preserved the distinction between published evidence, directly extracted values, reconstructed observables, synthetic inputs, assumptions, derived quantities, and quantities not independently validated.

## Stage 4 — Scientific Continuity Layer

The release exposes the 2006–2026 trajectory through `research_continuity/README.md`, `PORTFOLIO.md`, `POST_2018_ACTIVITY.md`, and `EVIDENCE_MAP.md`, while avoiding claims of undisclosed post-2018 plasma experiments.

## Stage 5 — Evidence Map

The evidence map links historical diagnostic capabilities to executable computational artifacts and states the boundary for each capability.

## Stage 6 — Corrections and validation

- P04 pressure cases now use deterministic pressure-specific synthetic intermediate traces instead of identical traces for all pressures. Published transport targets remain explicit constraints.
- Notebook imports now locate the repository root automatically, eliminating the need to set `PYTHONPATH` for normal `nbconvert` execution.
- Version metadata is `0.1.0-rc4.2`.
- Provenance count is corrected to the actual 55 records.
- All notebooks are re-executed after the changes; tests, archive integrity, import/compile checks, provenance checks, and master-audit determinism are revalidated before release packaging.

## Boundary

RC4.2 remains a release candidate. It does not contain original IR-T1 raw shot data or confidential client data and does not claim exact recovery of either.
