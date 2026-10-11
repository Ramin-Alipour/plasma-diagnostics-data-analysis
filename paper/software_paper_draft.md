# Plasma Diagnostics Data Analysis: A Provenance-Aware Python Framework for Reproducible Diagnostic Workflows

**Author:** Ramin Alipour  
**ORCID:** https://orcid.org/0000-0003-0744-9866  
**Corresponding author:** alipour_r@ymail.com

## Abstract

Experimental plasma diagnostics produce heterogeneous signals and spectra that require calibration, preprocessing, feature extraction, and quantitative interpretation. Reusable analysis software is most useful when these transformations can be inspected and when the evidential status of every input is explicit. *Plasma Diagnostics Data Analysis* is an open-source Python framework for spectroscopy, hard-X-ray signals, magnetic fluctuations, electrostatic probes, turbulence and transport, and cross-diagnostic analysis. It combines reusable modules with executable notebooks, automated tests, source manifests, and field-level provenance records. Six IR-T1 publications motivate computational examples without being treated as substitutes for unavailable original diagnostic arrays. Dataset A contains supplied laboratory and diagnostic-software records; Dataset B contains separately documented values transcribed, digitized, or reconstructed from publications; synthetic signals form a third category used for controlled demonstrations and software tests. These categories remain separate. The version-specific v0.2.2 archive is available from GitHub and Zenodo. Continuous integration on Python 3.11–3.13 tests the code, runs the reconstruction notebooks on Python 3.11, and builds and tests an installed wheel. These checks support reproducible software execution, not independent validation of historical experimental results.

**Keywords:** plasma diagnostics; scientific software; Python; spectroscopy; magnetic fluctuations; signal processing; data provenance

## 1. Motivation and significance

Plasma-diagnostic analysis often spans several transformations: preprocessing, calibration, feature extraction, signal analysis, calculation of physical observables, and comparison with experimental or published constraints. When these steps are distributed across individual scripts and notebooks, it can be difficult to trace a result back to its inputs or to distinguish measured values from derived quantities and synthetic test signals.

*Plasma Diagnostics Data Analysis* organizes selected analysis workflows associated with experimental IR-T1 tokamak research into reusable Python modules. The software covers optical/Doppler spectroscopy and impurity analysis [1], hard-X-ray observations [2], compound-probe measurements [3], pressure-dependent turbulent transport [4], biased-limiter effects [5], and magnetic/MHD fluctuations [6]. The goal is not to claim new IR-T1 experiments or to recover original shots that are unavailable in the repository. Instead, the software provides inspectable computational procedures and a consistent way to document input provenance and limitations.

The contribution is the combination of diagnostic-specific algorithms, runnable examples, automated verification, and an evidence-provenance model. This model distinguishes source-reported values, table transcriptions, figure digitizations, reconstructed values, synthetic inputs, assumptions, and derived quantities. It also makes clear that a successful software test is not equivalent to independent physical validation.

## 2. Software description

### 2.1. Architecture and capabilities

The package provides reusable components for:

- **Optical spectroscopy:** wavelength calibration, line identification, Gaussian fitting, and Doppler-broadening calculations.
- **Magnetic diagnostics:** signal preprocessing, power spectral density (PSD), singular-value decomposition (SVD), wavelet-oriented analysis, and spatial Fourier-mode identification.
- **Electrostatic probes:** probe-oriented calculations and compound-probe flow/Mach-number analysis.
- **Hard-X-ray analysis:** event- and spectrum-oriented processing.
- **Turbulence and transport:** fluctuation statistics, electric-field and E×B-related quantities, Reynolds stress, turbulent-flux calculations, and parameter scans.
- **Cross-diagnostic analysis:** time alignment, correlation, and comparative summaries.
- **Reconstruction and provenance:** source manifests, field-level provenance, dataset loaders, audit records, and comparison utilities.

The repository contains reusable package modules, domain notebooks, six publication-reconstruction cases, a dedicated Dataset A P01 laboratory line-width notebook, tests, package metadata, and audit documentation. Notebooks demonstrate the workflows but are not the only implementation of the analysis.

### 2.2. Evidence classes and dataset boundaries

Three evidence classes are maintained separately.

**Dataset A — supplied laboratory and diagnostic-software records.** This set contains a limited collection of owner-supplied laboratory measurements and diagnostic-software outputs. Source records are retained without numerical alteration. Dataset A is not a complete archive of original IR-T1 discharge data. The owner identifies e06_mhd_signal.csv as a diagnostic-software export; its columns (x_pixel, y_pixel, frequency_kHz, and amplitude) do not establish that it is a raw time-domain waveform, so the software does not calculate a time-domain PSD from it without valid waveform and sampling metadata.

**Dataset B — publication-derived records.** This set contains values transcribed from tables or text, digitized from figures, or reconstructed from six IR-T1 publications [1–6]. Source manifests and column-level provenance distinguish exact reported values from approximate digitizations and reconstructed quantities. Dataset B is not Dataset A with noise added.

**Synthetic data — controlled computational inputs.** Synthetic signals exercise algorithms or encode selected constraints. Where the documented relative-noise convention is used, Gaussian noise standard deviation is 1.3% of the absolute nonzero reference value; exact zero references remain zero. This rule applies only to synthetic signals and does not alter Dataset A or Dataset B.

Several source boundaries are particularly important. For P01, the lead author supplied real laboratory measurements, and certain values in the publication were intentionally approximate or different to protect sensitive diagnostic know-how. The author-supplied laboratory record is therefore used as the experimental data basis and kept separate from the publication-derived record. The early synthetic CCD-like spectrum was a software-development scaffold, not the experimental dataset; comparisons between that scaffold and publication temperatures are withdrawn from scientific reporting and are not reported as experimental discrepancies. For P02, the Dataset A modal table and the Dataset B transcription of the published table coincide numerically; that overlap is preserved because the two records have different provenance roles, and it is not independent validation. For P04, Dataset A records +0.0010 for radial transport at 2.3 Torr under +200 V, while the source paper text reports −0.0011; both are retained with their provenance rather than silently adjusted. For P06, the digitized pressure-specific PSD peaks are approximate (about 42, 48, and 52 kHz) and carry a conservative combined peak-selection uncertainty of ±3.1 kHz. These comparisons do not justify treating a digitized curve as a raw time series or forcing agreement with a paper's broader frequency band.

### 2.3. Publication-grounded computational cases

The six cases illustrate different computational paths:

| Case | Domain and demonstration | Main limitation |
|---|---|---|
| P01 | Spectral-line fitting and Doppler-related calculations; separate laboratory-data analysis | Synthetic fitting is a software test, not the experimental spectrum |
| P02 | Hard-X-ray event-energy summaries, synthetic multichannel magnetic signals, and spatial Fourier modes | Original detector response and raw Mirnov time series are unavailable |
| P03 | Directional-current model and Mach-number sensitivity analysis | Original collector-current time series is unavailable |
| P04 | Potential-to-field and transport calculations under pressure and bias conditions | Some intermediate traces are synthetic; reconstructed values are labelled approximate |
| P05 | Parameterized limiter-position and bias scenarios | Scenarios are consistency demonstrations, not new measurements or independent causal inference |
| P06 | Synthetic multichannel fluctuations, PSD analysis, and selected figure digitization | Figure-derived values are approximate; source timing inconsistencies remain documented |

Synthetic traces are not described as recovered measurements. Agreement with a target used to construct a synthetic signal is a computational consistency check, not independent experimental validation. The software does not infer a physical poloidal mode number merely from an SVD component index.

## 3. Illustrative use

A typical workflow loads a dataset using provenance-aware functions, checks its source manifest and field-level records, applies reusable analysis functions, compares outputs only with relevant source constraints, and runs the corresponding tests or notebook.

For a spectroscopy example, a user can load a spectrum, apply wavelength calibration, identify and fit spectral lines, and calculate a Doppler-broadening estimate. The separate P01 laboratory notebook demonstrates the analysis of supplied measurements; the synthetic fitting path remains available for software testing without reporting a synthetic-versus-publication experimental discrepancy.

For magnetic/MHD examples, a synthetic multichannel Mirnov matrix can be projected onto spatial Fourier bases to identify the constructed poloidal components, followed by PSD and comparative analysis. For turbulence/transport examples, parameterized inputs demonstrate how electric-field and transport-related quantities are calculated while reported text values remain separate from approximate reconstructions. Intermediate steps are available for inspection, and source records remain traceable through manifests and provenance metadata.

## 4. Impact, verification, and limitations

The framework's practical value is the organization of reusable diagnostic-analysis methods and auditable input provenance in one software distribution. Researchers can reuse individual modules without adopting every workflow, inspect intermediate calculations, and rerun selected examples. The project does not claim external adoption, quantified time savings, or improved physical inference; those claims would require independent-user studies or validation against separately documented experimental datasets.

The cited software version is archived as v0.2.2 [7]. Continuous integration on the released source commit 5fa9b58b43b3461135404ef84db7bd434a31e5c4 passed on Python 3.11, 3.12, and 3.13. The Python 3.11 job executed the reconstruction notebooks; all three jobs completed tests, compilation, import checks, and installed-wheel checks. The corresponding CI run is [38174480297](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38174480297). The release-packaging workflow also passed, built the source distribution and wheel, created the source ZIP and checksum file, and attached the four assets to the GitHub release [run 38174480392](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38174480392).

These checks establish software execution, packaging, and selected computational consistency. They do not independently validate historical IR-T1 measurements, verify unavailable acquisition logs, recover missing raw shots, or convert synthetic constraints into new experimental findings. Dataset B values digitized from figures or reconstructed from incomplete publication information may be approximate; their precision and uncertainty are documented accordingly. Dataset A is a limited supplied record set rather than a full acquisition archive, and confidential client datasets are not distributed.

## 5. Conclusions

*Plasma Diagnostics Data Analysis* is a reusable Python framework for plasma-diagnostic signal processing and publication-grounded computational demonstrations. Its central design choice is to document the provenance and limitations of inputs alongside diagnostic-specific algorithms, executable examples, and automated tests. The software supports workflows across spectroscopy, hard-X-ray signals, magnetic fluctuations, electrostatic probes, turbulence and transport, and cross-diagnostic analysis. It preserves the distinction between supplied laboratory/device-software records, publication-derived data, and synthetic test inputs, and it does not claim recovery of unavailable IR-T1 raw shots or independent experimental validation of synthetic reconstructions.

## Software availability and metadata

| Code metadata | Description |
|---|---|
| Current code version | 0.2.2 |
| Permanent link to the code version | https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2 |
| Version-specific archive DOI | https://doi.org/10.5281/zenodo.23300661 |
| Repository | https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis |
| Legal code license | MIT |
| Versioning system | Git |
| Language and tools | Python; NumPy, SciPy, Matplotlib, pandas; pytest and Jupyter for development/testing |
| Requirements and environment | Python ≥ 3.11; CI on Python 3.11–3.13; notebook execution on Python 3.11 |
| Documentation | https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis |
| Support contact | alipour_r@ymail.com |

**Installation:** `python -m pip install "plasma-diagnostics-data-analysis @ https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/download/v0.2.2/plasma_diagnostics_data_analysis-0.2.2-py3-none-any.whl"`  
**Tests from a source checkout:** `python -m pip install -e ".[dev]" && python -m pytest`

## CRediT authorship contribution statement

Ramin Alipour: Conceptualization, Software, Methodology, Validation, Formal analysis, Data curation, Visualization, Writing – original draft, Writing – review and editing.

## Declaration of competing interest

The author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Funding

Funding information must be confirmed by the author before submission. No funding source is asserted in this draft.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this manuscript, the author used ChatGPT (OpenAI) to assist with drafting, organization, and language editing. The author must review and edit the text as needed and take full responsibility for the content of the submitted manuscript.

## Data availability

The software, source manifests, provenance records, and included datasets are available in the public repository and the version-specific Zenodo archive identified above. Dataset A contains a limited set of supplied laboratory and diagnostic-software records; Dataset B contains separately documented publication-derived values. Neither is presented as a complete archive of original IR-T1 raw shots. Confidential client datasets are not included.

## Acknowledgements

No acknowledgements are included in this draft.

## References

1. Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017). First investigation on plasma impurities of the IR-T1 Tokamak. *AIP Advances*, 7(11), 115303. https://doi.org/10.1063/1.4990869
2. Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017). Investigation on the Hard X-ray Radiations of the IR-T1 Tokamak Plasma: Electric and Magnetic Perspectives. *Brazilian Journal of Physics*, 47, 567–574. https://doi.org/10.1007/s13538-017-0536-6
3. Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017). Design and fabrication of a new compound probe for plasma flux measurement in IR-T1 tokamak. *Review of Scientific Instruments*, 88, 093516. https://doi.org/10.1063/1.4994037
4. Alipour, R., Meshkani, S., Elahi, A. S., & Ghoranneviss, M. (2017). Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma. *The European Physical Journal D*, 71, 60. https://doi.org/10.1140/epjd/e2017-70563-6
5. Alipour, R., Ghoranneviss, M., Elahi, A. S., & Meshkani, S. (2017). Effects of the location of a biased limiter on turbulent transport in the IR-T1 tokamak plasma. *The European Physical Journal D*, 71, 228. https://doi.org/10.1140/epjd/e2017-80215-6
6. Alipour, R., & Ghanbari, M. R. (2018). Magnetic evaluation of hydrogen pressure changes on MHD fluctuations in IR-T1 tokamak plasma. *The European Physical Journal D*, 72, 75. https://doi.org/10.1140/epjd/e2018-90033-y
7. Alipour, R. *Plasma Diagnostics Data Analysis*, version 0.2.2 [software]. Zenodo; 2026. https://doi.org/10.5281/zenodo.23300661

---

## Internal finalization checklist — remove from the submitted manuscript

- [x] Freeze the cited software version at v0.2.2; do not mutate its release assets during manuscript edits.
- [x] Separate Dataset A (supplied laboratory/device-software records), Dataset B (publication-derived records), and synthetic data.
- [x] Remove P01 synthetic-spectrum discrepancy reporting and avoid claims of independent physical validation.
- [x] Correct the archived release commit and current CI run references.
- [x] Abstract under 250 words; seven keywords; four separate highlights under 85 characters each.
- [x] Add SoftwareX-style code metadata table, CRediT statement, competing-interest declaration, and data-availability statement.
- [ ] Transfer the approved text into the current official SoftwareX Word or LaTeX template without changing its layout rules.
- [ ] Author confirmation before submission: verify funding/acknowledgements and the competing-interest statement.
- [ ] Final proofread of the formatted manuscript, references, line numbering, and all metadata fields.
