# Plasma Diagnostics Data Analysis

## New development track: Tokamak Workbench

A separate **Tokamak Workbench** analysis layer is being developed alongside the existing package, based on the comprehensive diagnostic catalog in the uploaded tokamak reference and the six IR-T1 publication workflows. It adds a structured parameter/method/formula catalog, explicit measured-versus-derived-versus-model-inferred status, tabular data import and quality checks, and reusable physics/signal-analysis routines. See [tokamak_workbench/README.md](tokamak_workbench/README.md).

The existing modules, Dataset A/B provenance records, and P01–P06 reconstruction cases are preserved. This development branch is not yet a release, and catalog coverage must not be confused with implementation or validation of every diagnostic algorithm.


> **Reproducible, publication-grounded workflows for experimental plasma diagnostics — from diagnostic signals and spectra to quantitative observables, uncertainty, consistency checks, and scientific provenance.**

> **Data reuse terms:** [DATA_TERMS.md](DATA_TERMS.md) describes the current source-tree reuse conditions for Dataset A and Dataset B. The MIT license applies to code, not automatically to datasets.

> **Concept DOI:** [10.5281/zenodo.23298821](https://doi.org/10.5281/zenodo.23298821) — resolves to the latest archived version. The [v0.2.2 release](https://doi.org/10.5281/zenodo.23300661) has its own version-specific DOI.

## Why this repository exists

This repository documents a **reproducible computational continuation of experimental plasma-diagnostic work previously performed on the IR-T1 tokamak**.

It is designed as a research portfolio as well as a scientific software project. The central question is:

**Can an experimental plasma-diagnostic problem be taken from measurement or publication-grounded evidence through quantitative analysis, physical interpretation, uncertainty, consistency checking, and a reproducible computational artifact?**

The repository demonstrates that workflow across:

- **Doppler spectroscopy** — calibration, line identification, Gaussian fitting, Doppler broadening, ion-temperature estimation
- **Hard X-ray diagnostics** — time/energy-domain analysis and energetic-feature extraction
- **Magnetic/MHD diagnostics** — multichannel preprocessing, PSD, SVD, wavelet and spatial/mode analysis
- **Electrostatic probes** — Langmuir analysis, electric-field reconstruction, flow/Mach-number analysis
- **Turbulence & transport** — fluctuations, E×B drift, Reynolds stress and turbulent particle flux
- **Cross-diagnostic analysis** — explicit time alignment, correlation, lag and spectral comparison
- **Publication-grounded reconstruction** — six IR-T1 publications used as quantitative constraints and computational consistency cases

## Scientific continuity

| Period | Scientific continuity |
|---|---|
| **2006–2013** | Physics and experimental foundation |
| **2013–2017** | IR-T1 experimental plasma research: spectroscopy, hard X-ray, electrostatic probes, magnetic fluctuations/MHD and transport-related analysis |
| **2017–2018** | Independent research |
| **2018–2026** | Independent scientific & technical work: quantitative data analysis, Python/MATLAB-oriented workflows, signal processing and scientific/technical R&D support |
| **2026** | Publication-grounded reproducible computational reconstruction |

The repository contains **Dataset A: real supplied raw laboratory measurements and diagnostic device/software outputs**, plus a separate Dataset B of publication-extracted/reconstructed data and explicitly labelled synthetic inputs for selected demonstrations. It does not claim new IR-T1 experiments after 2018 or recovery of a complete archive of original IR-T1 tokamak shots.

## What is actually demonstrated

The public artifacts distinguish explicitly between:

- published experimental evidence
- directly extracted quantities
- reconstructed quantities
- synthetic measurements
- assumptions
- derived observables
- quantities not independently validated

This distinction is intentional. **Dataset A is real, supplied raw laboratory measurement and diagnostic device/software-output data. Dataset B is a separate publication-derived/reconstructed dataset.** Synthetic inputs are used only in explicitly identified examples or tests; they do not describe Dataset A and are not presented as original IR-T1 measurements.

### Flagship reconstruction cases

| Case | Diagnostic focus | Main computational chain |
|---|---|---|
| **P01** | Spectroscopy | author-supplied laboratory measurements for experimental analysis; synthetic line-fitting path for software tests only |
| **P02** | HXR + Mirnov/MHD | energy/time analysis → spatial/modal decomposition → consistency check |
| **P03** | Compound probe | directional currents → flow/Mach reconstruction → uncertainty |
| **P04** | Turbulence/transport | potential → E → E×B → fluctuations → transport observables |
| **P05** | Limiter/transport | parameterized boundary conditions → transport scenarios |
| **P06** | Magnetic/MHD | pressure → Mirnov fluctuations → PSD → dominant frequency |

## Portfolio navigation

For a research or recruitment review, the intended reading path is:

1. **Scientific continuity** — [research_continuity/PORTFOLIO.md](research_continuity/PORTFOLIO.md) — what was done, what is demonstrated now, and what can be verified.
2. **Evidence map** — [research_continuity/EVIDENCE_MAP.md](research_continuity/EVIDENCE_MAP.md) — capability → evidence → computational artifact → boundary.
3. **Publications** — [PUBLICATION_TRACEABILITY.md](PUBLICATION_TRACEABILITY.md) and [PUBLICATION_RECONSTRUCTION.md](PUBLICATION_RECONSTRUCTION.md) — six IR-T1 papers mapped to reconstruction workflows and scientific limitations.
4. **Notebooks** — [notebooks/](notebooks/) — executable domain demonstrations, a dedicated Dataset A P01 laboratory line-width analysis, and P01–P06 reconstruction notebooks.
5. **Figures** — [figures/](figures/) — four flagship outputs selected from the reconstruction layer.
6. **Tests** — [tests/](tests/) — automated tests covering the diagnostic and reconstruction modules.

This repository should be read as an **experimental plasma-diagnostics research portfolio with a reproducible computational layer**, not as a generic software project and not as a claim of new IR-T1 experiments after 2018.

### Evidence boundary

The repository contains two distinct data groups. **Dataset A consists of real supplied raw laboratory measurements and diagnostic hardware/software outputs**, including the E06 output from the diagnostic software; these files are preserved as supplied and are not synthetic or reconstructed from publications. **Dataset B consists of data extracted from or reconstructed using published papers and selected digitized figures.** Any synthetic inputs used for specific demonstrations or tests are explicitly labelled and remain separate from both datasets. The repository does not include a complete archive of all original IR-T1 tokamak shots, and confidential client-specific datasets are not distributed. This archive limitation does not mean that Dataset A is absent, synthetic, or publication-derived.

## Evidence and reproducibility

Start here:

- [research_continuity/PORTFOLIO.md](research_continuity/PORTFOLIO.md) — what was done and what can be demonstrated now
- [research_continuity/EVIDENCE_MAP.md](research_continuity/EVIDENCE_MAP.md) — claim → experimental evidence → computational artifact
- [audit/SCIENTIFIC_AUDIT.md](audit/SCIENTIFIC_AUDIT.md) — evidence classification and scientific boundaries
- [audit/RC4_MASTER_AUDIT.md](audit/RC4_MASTER_AUDIT.md) — quantitative reconstruction audit
- [PUBLICATION_TRACEABILITY.md](PUBLICATION_TRACEABILITY.md) — publication-to-workflow mapping
- [plasma_provenance/records.json](plasma_provenance/records.json) — machine-readable provenance records
- [notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb](notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb) — central executable audit

## Reproducibility

The GitHub Actions workflow checks the project on Python 3.11, 3.12, and 3.13. It runs the automated test suite, executes all notebooks on Python 3.11, compiles the Python modules, checks imports, and builds/installs/tests the package wheel. The [Actions page](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions) shows the result for each commit. These checks establish software execution and packaging, not independent experimental validation of publication reconstructions.

The published **v0.2.2** release was also tested and packaged from its immutable tag. The release workflow ran the automated test suite, built the wheel and source distribution, created the source ZIP and `SHA256SUMS.txt`, and attached all four assets to the [v0.2.2 GitHub Release](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2). See the [successful release-packaging run](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38153362054).

The earlier `v0.2.0` archive passed CI on Python 3.11–3.13 and executed its eight publication-reconstruction notebooks on Python 3.11; see its [release-commit CI run](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38143258358).

These checks establish software execution and packaging, not independent experimental validation of publication reconstructions.

## Data policy

**Dataset A contains real supplied raw laboratory measurements and diagnostic hardware/software outputs, including the owner-confirmed E06 diagnostic-software output. These data are not synthetic and are not reconstructed from publications. Dataset B is separate and contains data extracted from or reconstructed using published papers and selected digitized figures.** Synthetic inputs used in selected examples or tests form a third, explicitly labelled category. The three categories are not silently substituted for one another.

The repository does not distribute a complete archive of all original IR-T1 tokamak shots or confidential client/project-specific datasets. This is a limitation on the completeness of the historical shot archive; it does **not** mean that real laboratory data are absent, synthetic, or publication-derived.

Synthetic inputs used in selected demonstrations or tests are explicitly labelled and are not described as original experimental measurements. Publication reconstructions and synthetic demonstrations are computational examples and do not, by themselves, constitute independent experimental validation. Both dataset source manifests include Git blob fingerprints, and CI checks the exact bytes of every listed source file to detect undocumented changes.

## Repository structure

~~~text
plasma_core/              Common data models and signal processing
spectroscopy/             Spectroscopic diagnostics
magnetic_diagnostics/     Mirnov/MHD analysis
electrostatic_diagnostics/Probe workflows
turbulence_transport/     Turbulence and transport
hard_xray/                Hard X-ray workflows
cross_diagnostic/         Multi-diagnostic alignment and comparison
publication_reconstruction/ Six publication-grounded cases
research_continuity/      Scientific continuity and evidence map
plasma_provenance/       Traceability records
audit/                    Scientific and release audits
notebooks/                Executable demonstrations
figures/                  Flagship outputs
tests/                    Automated validation
~~~

## Quick start

Python 3.11+ is recommended.

~~~bash
python -m pip install -e ".[dev]"
pytest -q
~~~

The notebooks can then be opened directly in Jupyter.

## Release

**Latest published release: v0.2.2**


v0.2.2 aligns the package version and citation metadata, preserves the Dataset A / Dataset B provenance distinction, and includes the release assets attached to GitHub.

- **GitHub Release:** [v0.2.2 — Metadata and Reproducibility Update](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2)
- **Zenodo version DOI (v0.2.2):** [v0.2.2 release](https://doi.org/10.5281/zenodo.23300661)
- **Concept DOI:** [10.5281/zenodo.23298821](https://doi.org/10.5281/zenodo.23298821) — identifies the project across versions and resolves to the latest archived version.
- **Previous release:** [v0.2.1](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.1), DOI [10.5281/zenodo.23300345](https://doi.org/10.5281/zenodo.23300345)

## Citation

For published software, cite the exact archived version used. For v0.2.2, use its version-specific DOI:

> Alipour, R. (2026). *Plasma Diagnostics Data Analysis* (Version v0.2.2) [Computer software]. Ramin Alipour. https://doi.org/10.5281/zenodo.23300661

- **Version DOI (v0.2.2):** https://doi.org/10.5281/zenodo.23300661
- **Concept DOI:** https://doi.org/10.5281/zenodo.23298821
- **GitHub Release:** https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2
- **Previous version DOI (v0.2.1):** https://doi.org/10.5281/zenodo.23300345
- **Citation metadata:** [CITATION.cff](CITATION.cff)

The version DOI identifies a specific archived release; the concept DOI identifies the project across versions.

## License

MIT License — see [LICENSE](LICENSE).
