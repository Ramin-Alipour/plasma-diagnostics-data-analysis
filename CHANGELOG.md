# Changelog

## [Unreleased]

These are source-tree changes on `main` after the published v0.2.2 snapshot. They do not create a new release or modify the existing v0.2.2 tag/Zenodo archive.

- Clarified P06 peak-frequency wording so the manuscript, comparison code, and tests consistently describe ±3.1 kHz as an approximate combined axis-calibration/peak-selection uncertainty, not a statistical confidence interval.
- Clarified that the 1.3% relative-noise test and the turbulence generator's 1% default are workflow-specific settings, not a package-wide convention.
- Added a deterministic rotating-mode SVD demonstration, a figure, and regression tests for mode recovery and centered reconstruction behavior.
- Made zero-energy SVD results return finite zero energy fractions rather than undefined `0/0` values, with a regression test.
- Added and clarified `DATA_TERMS.md`: Dataset A is the author's own laboratory data; the document distinguishes its reuse terms from the MIT software license without implying third-party ownership or a known permission barrier.
- Expanded the SoftwareX draft's comparison with PlasmaPy/OMFIT/MDSplus, stated Doppler-model limitations, and updated/verified references for line broadening, probe diagnostics, and SVD-based MHD analysis.
- Clarified that current `main` source edits and their CI results are distinct from the immutable v0.2.2 Zenodo archive.

## [0.2.2] — 2026-10-11

- Added a reusable summary utility for supplied spectral-line wavelength/FWHM measurements, with numeric validation and no unsupported temperature inference.
- Added an executable P01 notebook that analyzes Dataset A laboratory line-width measurements directly and keeps Dataset B and synthetic software-test workflows separate.
- Added automated checks that keep the project version, citation metadata, changelog, README release entry, and DOI references aligned.
- Generalized release packaging to run tests, build a wheel and source distribution, create a source ZIP and SHA-256 manifest, and attach the assets to published releases.

- Published v0.2.2 with aligned package and citation metadata and the Zenodo concept DOI for version-independent project citation.
- Updated the README release and citation sections to identify v0.2.2 and its version-specific DOI.
- Preserved Dataset A and Dataset B source files and their recorded integrity fingerprints; no source-data values were changed for this metadata update.
- Maintained the distinction between laboratory/device-software-origin records, publication-derived reconstructions, and synthetic software-test data.
- No independent experimental-validation claim is introduced by this metadata update.

## [0.2.1] — 2026-10-11

- Added Git blob fingerprints for all files listed in the Dataset A and Dataset B source manifests.
- Added an automated byte-integrity regression test that detects unreviewed edits to manifested source files.
- Documented that all 18 manifested data files remain byte-identical to the published `v0.2.0` archive.
- Clarified P01 synthetic-spectrum reporting boundaries and removed duplicated audit text.
- Updated the software-paper draft and audit documentation to reflect the published DOI and current development status.

## [0.2.0] — 2026-10-11

- Integrated Dataset A laboratory/device-software records and Dataset B publication-derived reconstructions as distinct evidence classes, with provenance manifests and regression coverage.
- Removed P01 synthetic-spectrum versus publication-temperature discrepancy from reportable scientific outputs; retained synthetic fitting as a software test only.
- Clarified that synthetic 1.3% relative noise applies only to nonzero reference values in the synthetic workflow; source datasets remain unchanged.
- Added a SoftwareX-oriented manuscript working draft. The GitHub release is published and archived on Zenodo with version DOI 10.5281/zenodo.23298822.


## [0.1.1] — 2026-10-02

- Corrected P01 spectral-resolution reconstruction to use the publication's quadrature resolution model (Eq. 3/11) and documented the resulting temperature discrepancy as a computational consistency check.
- Historical note: this release documented a temperature comparison from the synthetic CCD-like spectrum. In v0.2.0 that comparison was withdrawn from scientific reporting because the spectrum was a software-development scaffold, not the P01 experimental dataset; it is not a reportable experimental discrepancy.
- Renamed generic `core/` and `provenance/` packages to `plasma_core/` and `plasma_provenance/` and added `pyproject.toml` for standard installation.
- Removed the empty section from `requirements.txt` and moved RC4/RC4.2 release notes/checklist artifacts into `archive/release_candidates/`.
- Reframed P01/P05 publication-target comparisons as consistency checks rather than independent validation.
- Corrected the post-2018 activity statement so XRD/SEM/AFM/XPS/TEM work is identified as historical professional activity not implemented in this repository.
- Re-executed notebooks and tests after the release-correction pass.

## [0.1.0] — 2026-10-02

- Promoted the audited RC4.2 repository state to the final v0.1.0 portfolio-ready release baseline.
- Finalized repository navigation, P01–P06 publication traceability, scientific evidence boundaries, provenance, reconstruction notebooks, figures, and automated validation.
- Preserved the RC4.2 archive and audit records as the historical pre-release snapshot.

## [0.1.0-rc4.2] — 2026-10-01

- Completed the Stage 3 scientific audit for P01–P06 with explicit evidence classes and reconstruction boundaries.
- Added the Scientific Continuity Layer and Evidence Map as release-audited portfolio artifacts.
- Added a machine-readable scientific-audit matrix covering published, directly extracted, reconstructed, synthetic, assumed, derived, and not-independently-validated quantities.
- Fixed P04 synthetic pressure cases so intermediate traces are deterministic but pressure-specific rather than identical by construction; reported transport targets remain explicit constraints.
- Added notebook repository-root bootstrapping so notebooks can be executed with `nbconvert` without manually setting `PYTHONPATH`.
- Corrected release metadata to `0.1.0-rc4.2` and corrected the provenance-record count from 52 to the actual 55 records.
- Re-executed notebooks and revalidated tests, provenance, archive integrity, and master-audit determinism.


## [0.1.0-rc4] — 2026-10-01

- Added a scientific-continuity layer covering the 2006–2026 trajectory while explicitly separating professional-history context from executable repository evidence.
- Added research portfolio, post-2018 activity statement, evidence map, and machine-readable evidence records.
- Added a reusable modern plasma diagnostic pipeline manifest spanning measurement input, preprocessing, calibration, feature extraction, time-frequency/spatial analysis, observables, uncertainty, validation, and publication comparison.
- Added structured provenance schema and 55 traceable publication/reconstruction records.
- Upgraded P01 to a noisy synthetic CCD-like spectrum → Gaussian fitting → instrumental/Doppler correction → Monte-Carlo uncertainty workflow.
- Upgraded P02 to explicit spatial Fourier mode identification for the 12-channel synthetic Mirnov data, separate HXR spectrum reconstruction, and a non-causal HXR↔m=3 magnetic summary.
- Added P03 bootstrap uncertainty for reconstructed Mach number.
- Upgraded P04 to a potential → electric-field → E×B → turbulent particle-flux chain constrained by reported pressure-dependent transport quantities.
- Upgraded P05 to a limiter-position/bias field-amplitude parameterization that reproduces the explicitly reported -50/-35% radial-transport and -15/-5% Reynolds-stress effects as consistency-check targets.
- Added selective real pixel-to-axis digitization of P06 Figure 2 with calibration and uncertainty metadata.
- Added P01/P02/P04/P06 flagship figures and a central `00_six_paper_reconstruction_audit.ipynb`.
- Added RC4 master audit CSV/Markdown outputs and release-cleanup policy.
- Preserved the boundary that no raw IR-T1 shot data or confidential client data are claimed or distributed.

## [0.1.0-rc3] — 2026-10-01

- Added publication-grounded reconstruction study for six IR-T1 peer-reviewed papers.
- Added extracted numerical constraint datasets with explicit provenance/confidence classes.
- Added deterministic synthetic/raw-like reconstruction generators and six per-paper notebooks.
- Added quantitative reconstruction validation and publication-reported comparison targets.
- Added reconstruction audit and dedicated tests.
- Explicitly document that reconstructed datasets are synthetic and do not recover original raw measurements.


## [0.1.0-rc1] — 2026-10-01

### Added

- Continuous-integration workflow covering dependency installation, automated tests, Python compilation, and import smoke testing.
- Publication-to-project scientific traceability in `PUBLICATION_TRACEABILITY.md`.
- Explicit mapping between the six IR-T1 reference publications and repository modules, notebooks, tests, and synthetic validation workflows.

### Documentation

- Updated `README.md` to identify Section 12 as the release and scientific-traceability audit stage.
- Linked the publication traceability document from `README.md` and `SCIENTIFIC_REFERENCE.md`.
- Preserved the distinction between published experimental evidence and synthetic/methodological computational demonstrations.

### Release / reproducibility

- Notebook execution remains outside CI and is part of the release audit.
- No original IR-T1 raw experimental data are added.
- No DOI is asserted without an actual repository release/DOI record.
- No `CONTRIBUTING.md` is added at this stage.
