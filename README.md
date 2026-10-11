# Plasma Diagnostics Data Analysis

> **Reproducible, publication-grounded workflows for experimental plasma diagnostics — from diagnostic signals and spectra to quantitative observables, uncertainty, consistency checks, and scientific provenance.**

> **Concept DOI:** [10.5281/zenodo.23298821](https://doi.org/10.5281/zenodo.23298821) — resolves to the latest archived version. The [v0.2.1 release](https://doi.org/10.5281/zenodo.23300345) has its own version-specific DOI.

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

The repository does **not** claim new IR-T1 experiments after 2018 or recovered IR-T1 raw shots.

## What is actually demonstrated

The public artifacts distinguish explicitly between:

- published experimental evidence
- directly extracted quantities
- reconstructed quantities
- synthetic measurements
- assumptions
- derived observables
- quantities not independently validated

This distinction is intentional. Synthetic demonstrations are **not presented as original IR-T1 measurements**.

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
4. **Notebooks** — [notebooks/](notebooks/) — executable domain demonstrations plus dedicated P01–P06 reconstruction notebooks.
5. **Figures** — [figures/](figures/) — four flagship outputs selected from the reconstruction layer.
6. **Tests** — [tests/](tests/) — automated tests covering the diagnostic and reconstruction modules.

This repository should be read as an **experimental plasma-diagnostics research portfolio with a reproducible computational layer**, not as a generic software project and not as a claim of new IR-T1 experiments after 2018.

### Evidence boundary

The repository deliberately separates historical experimental evidence from current computational evidence. Dataset A contains the laboratory/device/software-origin CSVs supplied for this project, including the owner-confirmed E06 diagnostic-software output; these files are preserved as supplied. They should not be confused with a complete archive of original IR-T1 raw tokamak shots, which is not available in this repository. Confidential client datasets are also not distributed. Dataset B is reconstructed from published papers and remains separate from Dataset A. Synthetic or reconstructed quantities are labelled as such and are not presented as recovered measurements.

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

The published **v0.2.0** release was checked by GitHub Actions on release commit `b3dbd1a145684b314c4d1017cfad19a173e2df9a`:

- CI passed on Python 3.11, 3.12, and 3.13
- all eight publication-reconstruction notebooks executed successfully on Python 3.11
- Python compilation and import smoke tests passed
- the package wheel was built, installed, and tested outside the source checkout
- the release-packaging workflow subsequently generated the source ZIP, wheel, source distribution, and `SHA256SUMS.txt`; the workflow and CI both passed on main commit `940000cdab1ff931d3fddbc973988f566fc173fd`

See the [release-commit CI run](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38143258358), [latest main CI run](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38144540547), and [release-packaging workflow](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38144540661).

These checks establish software execution and packaging, not independent experimental validation of publication reconstructions.

## Data policy

Complete original IR-T1 raw-shot archives are **not distributed**. Dataset A is a separate set of supplied laboratory measurements and diagnostic hardware/software outputs; its files are retained as supplied and are not reclassified based on numerical similarity to Dataset B. Confidential client/project-specific datasets are also not included.

Dataset B uses publication-grounded constraints and selected digitized publication figures. Separate synthetic workflows use explicit assumptions and computational consistency checks. Publication reconstructions and synthetic demonstrations are not independent experimental validation. Both dataset source manifests include Git blob fingerprints, and CI checks the exact bytes of every listed source file to detect undocumented changes.

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

v0.2.2 aligns the package version and citation metadata, clarifies the concept DOI versus version-specific DOIs, and preserves the distinction between Dataset A laboratory/device-software-origin records, Dataset B publication-derived reconstructions, and synthetic software-test data. The metadata update does not change source-data values or claim independent experimental validation.

- **GitHub Release:** [v0.2.2 — Metadata Alignment and Reproducibility](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2)
- **Zenodo version DOI (v0.2.2):** [10.5281/zenodo.23300661](https://doi.org/10.5281/zenodo.23300661)
- **Previous release:** [v0.2.1 — Integrity and Reproducibility Improvements](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.1) — [version DOI](https://doi.org/10.5281/zenodo.23300345)
- **Concept DOI:** [10.5281/zenodo.23298821](https://doi.org/10.5281/zenodo.23298821) — identifies the project across versions and resolves to the latest archived version.

## Citation

For published software, cite the exact archived version used. For v0.2.2:

> Alipour, R. (2026). *Plasma Diagnostics Data Analysis* (Version v0.2.2) [Computer software]. Ramin Alipour. https://doi.org/10.5281/zenodo.23300661

- **Version DOI (v0.2.2):** https://doi.org/10.5281/zenodo.23300661
- **Concept DOI:** https://doi.org/10.5281/zenodo.23298821
- **GitHub Release:** https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2
- **Previous version DOI (v0.2.1):** https://doi.org/10.5281/zenodo.23300345
- **Earlier version DOI (v0.2.0):** https://doi.org/10.5281/zenodo.23298822
- **Citation metadata:** [CITATION.cff](CITATION.cff)

The version DOI identifies a specific archived release; the concept DOI identifies the project across versions.

## License

MIT License — see [LICENSE](LICENSE).
