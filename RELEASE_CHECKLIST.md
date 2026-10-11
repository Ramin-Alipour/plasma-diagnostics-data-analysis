# Historical v0.1.1 Checklist and v0.3.0 Release Gate

> This checklist records the earlier v0.1.1 release state. It is not the checklist for the current release. The current public version is [v0.2.2](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2), archived at [Zenodo DOI 10.5281/zenodo.23300661](https://doi.org/10.5281/zenodo.23300661). The previous [v0.2.1 archive](https://doi.org/10.5281/zenodo.23300345) and earlier [v0.2.0 archive](https://doi.org/10.5281/zenodo.23298822) remain available. In v0.2.0, the early synthetic P01 spectrum comparison was withdrawn from scientific reporting because it was a software-development scaffold, not the experimental dataset.

## Consolidated release gate — v0.3.0

- [x] Package and citation version aligned at 0.3.0 on the release branch
- [x] Changelog includes the spectral-line utility, Dataset A P01 notebook, metadata checks, and release-packaging updates
- [x] README distinguishes the unpublished v0.3.0 candidate from the published v0.2.2 archive
- [x] Metadata test permits a release candidate without inventing a version DOI
- [ ] CI passes on the consolidated release branch
- [ ] Publish GitHub Release tag `v0.3.0`
- [ ] Confirm Zenodo archive and record its actual version-specific DOI
- [ ] Add the confirmed DOI to README and manuscript, then rerun CI
- [ ] Complete SoftwareX template/word-count and author declaration checks

## Historical v0.1.1 checklist — Scientific

- [x] Six publication constraint datasets retained
- [x] P01 full spectral reconstruction
- [x] P02 explicit 12-channel spatial mode identification
- [x] P02 HXR synthetic spectrum and cross-diagnostic summary
- [x] P03 uncertainty/sensitivity
- [x] P04 potential → E → E×B → turbulent-flux chain
- [x] P05 limiter/bias → field → transport parameterization
- [x] P06 pressure-dependent PSD reconstruction
- [x] Selective real figure digitization with calibration/uncertainty
- [x] Provenance schema and records
- [x] P01 Eq. (3)/(11) quadrature-resolution consistency note
- [x] Six-paper master audit
- [x] v0.1.1 master audit with P01/P05 consistency-check status

## Reproducibility

- [x] Automated tests
- [x] Python compilation
- [x] Import smoke test
- [x] All 14 notebooks executed successfully
- [x] Notebook outputs checked for execution errors
- [x] Cache/temp cleanup before release archive
- [x] Archive extraction test
- [x] SHA-256 checksum
- [x] Isolated package-build/install smoke test
- [x] Isolated virtual-environment test using the audited dependency set

## Boundary checks

- [x] Synthetic data never described as recovered raw data
- [x] Figure-derived values labelled as digitized
- [x] Post-2018 confidential/client datasets not fabricated or included
- [x] P06 timing inconsistency preserved and documented
- [x] No physical mode is inferred from SVD component number alone
- [x] Cross-diagnostic comparisons explicitly avoid causal claims
- [x] XRD/SEM/AFM/XPS/TEM activity described as historical and not implemented in this repository
