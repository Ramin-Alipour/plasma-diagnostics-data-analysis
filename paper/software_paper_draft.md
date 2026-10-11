# Plasma Diagnostics Data Analysis: A Provenance-Aware Python Framework for Reproducible Diagnostic Workflows

**Author:** Ramin Alipour  
**ORCID:** https://orcid.org/0000-0003-0744-9866

**Intended journal:** SoftwareX (provisional target; formatting and editorial requirements still to be checked).  
**Status:** public repository working draft, not submission-ready. Version `v0.2.1` is published on GitHub and archived on Zenodo with the version-specific DOI [10.5281/zenodo.23300345](https://doi.org/10.5281/zenodo.23300345). The earlier `v0.2.0` version remains archived at [10.5281/zenodo.23298822](https://doi.org/10.5281/zenodo.23298822). This working draft still requires journal-format review and final author/data-scope checks.

### Highlights

- Reusable Python workflows cover spectroscopy, hard-X-ray, magnetic/MHD, electrostatic-probe, and turbulence/transport analysis.
- Provenance records distinguish supplied laboratory/device-software data, publication-derived values, and synthetic test signals.
- Continuous integration tests three Python versions, executes eight reconstruction notebooks, and checks the installed wheel.
- Synthetic consistency checks are explicitly distinguished from independent experimental validation.

## Abstract

Experimental plasma diagnostics combine heterogeneous measurements, calibration and signal-processing steps, derived physical quantities, and interpretation under incomplete access to original acquisition records. Reproducible computational studies must therefore make both the analysis workflow and the provenance of each input explicit. This paper presents *Plasma Diagnostics Data Analysis*, an MIT-licensed Python research-software framework for organizing and exercising analysis workflows spanning optical spectroscopy, hard-X-ray signals, multichannel magnetic fluctuations, electrostatic probes, turbulence and transport, and cross-diagnostic analysis. The repository combines reusable analysis modules with automated tests, executable notebooks, publication-traceability records, and provenance-aware data loaders. Its six-paper IR-T1 reference set motivates controlled computational demonstrations and selected published constraints; synthetic signals are kept distinct from laboratory/device-software records and publication-derived tables. Dataset A contains a limited set of supplied laboratory and diagnostic-software records, whereas Dataset B contains separately documented values extracted or reconstructed from publications. Neither dataset substitutes for the other, and the repository does not claim to recover a complete archive of original IR-T1 shots. At the archived release commit `b3dbd1a145684b314c4d1017cfad19a173e2df9a`, GitHub Actions passed on Python 3.11, 3.12, and 3.13; all eight publication-reconstruction notebooks executed successfully on Python 3.11, and package build/install, compilation, and import checks passed. These checks establish software reproducibility, not independent experimental validation.

**Keywords:** plasma diagnostics; scientific Python; spectroscopy; magnetic fluctuations; hard X-ray; electrostatic probes; turbulence; transport; data provenance; reproducible research software

## 1. Motivation and significance

Plasma-diagnostic research relies on multi-stage transformations: instrument-aware preprocessing, calibration, feature extraction, signal analysis, calculation of physical observables, and comparison with physical expectations or published constraints. When these steps are distributed across scripts and notebooks, it can be difficult to determine which values are measured, which are derived, and which are generated to test an algorithm. This is particularly consequential when original diagnostic arrays are unavailable or published tables and figures provide only partial numerical constraints.

This software was developed as a computational continuation of experimental plasma-diagnostic work associated with the IR-T1 tokamak. Its aim is not to claim new IR-T1 experiments or reproduce original shots that are unavailable in the repository. Instead, it organizes reusable analysis methods and controlled computational demonstrations under a common software and provenance structure.

The design addresses three needs: reusable analysis components that can be called from scripts, tests, and notebooks; explicit separation of laboratory/device-software records, publication-derived data, synthetic signals, assumptions, and derived quantities; and reproducible execution through automated tests, notebook runs, package installation checks, and documented limitations.

## 2. Software description

### 2.1. Architecture

The Python implementation includes reusable modules for:

- optical spectroscopy: wavelength calibration, line identification, Gaussian fitting, and Doppler-broadening calculations;
- magnetic diagnostics: preprocessing, power spectral density (PSD), singular-value decomposition (SVD), wavelet analysis, and spatial Fourier mode identification;
- electrostatic diagnostics and compound-probe analysis;
- hard-X-ray event/spectrum workflows;
- turbulence and transport calculations, including fluctuation statistics, Reynolds stress, E×B-related quantities, and parameter scans;
- cross-diagnostic time alignment and correlation;
- publication reconstruction, provenance records, source manifests, and audit outputs.

The repository includes domain notebooks, eight publication-reconstruction notebooks, tests, package metadata, and audit documentation. Notebooks are executable demonstrations of reusable modules, not the only implementation of the analysis.

### 2.2. Evidence classes

**Dataset A — supplied laboratory/device-software records.** This collection contains a limited set of supplied laboratory measurements and diagnostic-software outputs, including an owner-confirmed E06 MHD-signal export. Source files are retained as supplied. Dataset A is not a complete archive of original IR-T1 raw shots, and the repository does not claim independent access to the original acquisition system.

**Dataset B — publication-derived records.** This collection contains values extracted from, digitized from, or reconstructed on the basis of six IR-T1 publications. Source manifests and field-level provenance distinguish directly reported table/text values from approximate digitizations and reconstructed quantities. Dataset B is not Dataset A with noise added.

**Synthetic data — controlled computational layer.** Synthetic signals exercise algorithms or encode selected constraints. The common relative-noise convention uses Gaussian standard deviation equal to 1.3% of the absolute nonzero reference value; exact zero references remain zero. This convention applies to synthetic signals only and does not alter Dataset A or Dataset B.

P01 has an additional reporting boundary. The lead author supplied real laboratory measurements and confirmed that some published values were intentionally approximate or different to protect sensitive diagnostic know-how. The early synthetic CCD-like spectrum was a software-development scaffold, not the experimental dataset. Synthetic-spectrum comparisons with publication temperatures have therefore been withdrawn from the master audit, regression assertions, and notebook reporting. The synthetic fitting path remains available only as a software-test workflow; it is not used to report a P01 experimental discrepancy.

### 2.3. Publication-grounded workflows

Six publications motivate the initial reference set, but are not treated as substitutes for original raw diagnostic arrays.

| Case | Diagnostic domain | Computational demonstration | Principal limitation |
|---|---|---|---|
| P01 | Optical/CCD spectroscopy and impurities | Synthetic line-fitting code path retained for software testing; laboratory provenance recorded separately | Synthetic-versus-publication temperature comparisons are withdrawn; experimental conclusions require author-supplied laboratory data |
| P02 | Hard X-ray and magnetic/MHD diagnostics | HXR event-energy constraints, synthetic multichannel Mirnov signals, spatial Fourier mode identification, and cross-diagnostic summaries | Original detector response and raw Mirnov time series are not reconstructed |
| P03 | Compound probe and plasma flow | Directional-current model and Mach-number sensitivity analysis | Original collector-current time series unavailable |
| P04 | Pressure-dependent turbulence/transport | Synthetic potential-to-field and transport chains, with text-level constraints separated from approximate Dataset B values | Intermediate traces are synthetic and absolute CSV values are approximate reconstructions |
| P05 | Biased-limiter position and transport | Parameterized synthetic scenarios for control-condition sensitivity | Parameterized effects are consistency targets, not new measurements or independent causal inference |
| P06 | Pressure-dependent magnetic/MHD fluctuations | Synthetic 12-channel signals, PSD analysis, and separately documented figure digitization | Pressure-specific estimates and figure-derived values are approximate; source timing inconsistency is retained as a limitation |

Agreement with a target used to construct a synthetic signal is a computational consistency check, not independent experimental validation. Synthetic traces are not described as recovered measurements.

## 3. Illustrative workflow

A typical analysis proceeds by loading a dataset through the provenance-aware loader, checking its source manifest and field-level provenance, running reusable analysis functions, comparing outputs only with relevant constraints, and executing the associated tests and notebook.

For magnetic/MHD examples, a 12-channel synthetic Mirnov matrix can be projected onto spatial Fourier bases to identify constructed poloidal components; PSD and cross-diagnostic summaries can then be calculated. The model does not equate an SVD component index with a physical poloidal mode number. For turbulence/transport examples, the code separates text-level reported targets from approximate reconstructed values rather than silently substituting one for the other.

For P01, the master audit reports author-supplied laboratory measurements as the experimental data basis. The synthetic fitting routine is exercised only to test software execution, and no synthetic-versus-publication discrepancy metric is produced.

## 4. Software verification

Automated tests check algorithm behavior, deterministic synthetic generation, provenance integrity, data-loader behavior, and selected computational constraints. Continuous integration runs the test suite on Python 3.11, 3.12, and 3.13. The Python 3.11 job additionally executes the eight publication-reconstruction notebooks. All jobs compile Python modules, perform import smoke tests, and build and install a wheel before exercising key data-loading and provenance functions.

On the archived `v0.2.0` release commit `b3dbd1a145684b314c4d1017cfad19a173e2df9a`, CI passed across Python 3.11–3.13; all eight reconstruction notebooks ran on Python 3.11, and compilation, import, and wheel build/install checks passed. See [GitHub Actions run 38143258358](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38143258358).

These checks verify software execution and packaging. They do not independently validate historical IR-T1 measurements, establish author intent, recover unavailable raw shots, or turn synthetic constraints into new experimental findings.

## 5. Limitations

A complete archive of original IR-T1 raw diagnostic shots is not distributed. Dataset A is a limited set of supplied laboratory/device-software records, not a full acquisition archive. Dataset B values derived from figures or reconstructed from incomplete publication information may be approximate and are labelled accordingly. Synthetic waveforms require assumptions about sampling, noise, phases, amplitudes, and model structure that are not uniquely recoverable from a paper. Agreement with a target used to construct a synthetic signal is a consistency check, not independent validation. The repository does not claim new IR-T1 experiments after 2018 or distribution of confidential client datasets.

## 6. Impact

The framework provides a single inspectable software structure for methods commonly split among separate analysis scripts and notebooks. Its primary contribution is the combination of reusable diagnostic-analysis modules with an explicit evidence-provenance model and automated execution checks. This structure helps researchers audit the path from input data to derived quantities, reuse algorithms across related diagnostic problems, and distinguish software correctness from experimental validation.

## 7. Availability and release status

Source repository: [Ramin-Alipour/plasma-diagnostics-data-analysis](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis). License: MIT. The Dataset A/Dataset B integration is included in the published `v0.2.0` release. The archived version-specific record is [Zenodo DOI 10.5281/zenodo.23298822](https://doi.org/10.5281/zenodo.23298822), with its source and Python distribution assets listed on the [GitHub release page](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.0).

## 8. Software metadata

| Item | Description |
|---|---|
| Software name | Plasma Diagnostics Data Analysis |
| Current public version | 0.2.0; version-specific Zenodo archive published |
| Archived release commit | `b3dbd1a145684b314c4d1017cfad19a173e2df9a` (tag `v0.2.0`) |
| Repository | https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis |
| License | MIT |
| Programming language | Python |
| Runtime requirement | Python ≥ 3.11 |
| Core dependencies | NumPy, SciPy, Matplotlib, pandas |
| Development/test dependencies | Jupyter, pytest |
| Verified environment | GitHub Actions on Python 3.11, 3.12, and 3.13; notebook execution on Python 3.11 |
| Installation for the eventual merged version | `python -m pip install -e ".[dev]"` |
| Automated tests | `python -m pytest` |
| Notebook reproduction | Execute the notebooks under `notebooks/publication_reconstruction/` with Jupyter/nbconvert |

The installation and test commands above apply to the released package. Cite the version-specific archive DOI when reporting results obtained with `v0.2.0`.

## 9. Author contributions

Ramin Alipour: conceptualization, software development, data curation and provenance documentation, computational analysis, and manuscript preparation.

## 10. Conclusions

*Plasma Diagnostics Data Analysis* provides a reusable Python framework for plasma-diagnostic signal processing and publication-grounded computational demonstrations. Its central design choice is to make data provenance and scientific limitations explicit alongside reusable algorithms and automated tests. The framework supports reproducible workflows across spectroscopy, magnetic and hard-X-ray diagnostics, electrostatic probes, turbulence/transport, and cross-diagnostic analysis. It does not claim recovery of missing raw IR-T1 shots or independent validation of synthetic reconstructions. Before submission, the draft still requires journal-specific formatting and a final check of author declarations, data permissions, and scope.

## References

1. Alipour, R., Ghoranneviss, M., and Elahi, A. S. (2017). First investigation on plasma impurities of the IR-T1 Tokamak. *AIP Advances*, 7(11), 115303. https://doi.org/10.1063/1.4990869
2. Alipour, R., Ghoranneviss, M., and Elahi, A. S. (2017). Investigation on the Hard X-ray Radiations of the IR-T1 Tokamak Plasma: Electric and Magnetic Perspectives. *Brazilian Journal of Physics*, 47, 567–574. https://doi.org/10.1007/s13538-017-0536-6
3. Alipour, R., Ghoranneviss, M., and Elahi, A. S. (2017). Design and fabrication of a new compound probe for plasma flux measurement in IR-T1 tokamak. *Review of Scientific Instruments*, 88, 093516. https://doi.org/10.1063/1.4994037
4. Alipour, R., Meshkani, S., Elahi, A. S., and Ghoranneviss, M. (2017). Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma. *The European Physical Journal D*, 71, 60. https://doi.org/10.1140/epjd/e2017-70563-6
5. Alipour, R., Ghoranneviss, M., Elahi, A. S., and Meshkani, S. (2017). Effects of the location of a biased limiter on turbulent transport in the IR-T1 tokamak plasma. *The European Physical Journal D*, 71, 228. https://doi.org/10.1140/epjd/e2017-80215-6
6. Alipour, R., and Ghanbari, M. R. (2018). Magnetic evaluation of hydrogen pressure changes on MHD fluctuations in IR-T1 tokamak plasma. *The European Physical Journal D*, 72, 75. https://doi.org/10.1140/epjd/e2018-90033-y

---

## Internal submission checklist (remove before submission)

- [ ] Apply the current SoftwareX manuscript template and verify article-type requirements.
- [x] Confirm the published `v0.2.0` tag, Zenodo archive, and version-specific DOI; do not cite the pre-integration `v0.1.1` archive as the artifact described here.
- [x] CI passed on the exact `v0.2.0` release commit; preserve [the release CI report](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38143258358).
- [ ] Verify references, author metadata, repository citation instructions, and data availability statements.
- [ ] Ensure the final manuscript contains no P01 synthetic-versus-publication discrepancy value and makes no claim of independent experimental validation.
- [ ] Review all Dataset A files and provenance statements for permission and scope before public release.
