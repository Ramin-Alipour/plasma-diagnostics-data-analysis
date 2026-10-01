# Plasma Diagnostics Data Analysis

> **Reproducible, publication-grounded workflows for experimental plasma diagnostics — from diagnostic signals and spectra to quantitative observables, uncertainty, validation, and scientific provenance.**

## Why this repository exists

This repository documents a **reproducible computational continuation of experimental plasma-diagnostic work previously performed on the IR-T1 tokamak**.

It is designed as a research portfolio as well as a scientific software project. The central question is:

**Can an experimental plasma-diagnostic problem be taken from measurement or publication-grounded evidence through quantitative analysis, physical interpretation, uncertainty, validation, and a reproducible computational artifact?**

The repository demonstrates that workflow across:

- **Doppler spectroscopy** — calibration, line identification, Gaussian fitting, Doppler broadening, ion-temperature estimation
- **Hard X-ray diagnostics** — time/energy-domain analysis and energetic-feature extraction
- **Magnetic/MHD diagnostics** — multichannel preprocessing, PSD, SVD, wavelet and spatial/mode analysis
- **Electrostatic probes** — Langmuir analysis, electric-field reconstruction, flow/Mach-number analysis
- **Turbulence & transport** — fluctuations, E×B drift, Reynolds stress and turbulent particle flux
- **Cross-diagnostic analysis** — explicit time alignment, correlation, lag and spectral comparison
- **Publication-grounded reconstruction** — six IR-T1 publications used as quantitative constraints and validation cases

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
| **P01** | Spectroscopy | spectrum → calibration → line fit → broadening → ion temperature |
| **P02** | HXR + Mirnov/MHD | energy/time analysis → spatial/modal decomposition → validation |
| **P03** | Compound probe | directional currents → flow/Mach reconstruction → uncertainty |
| **P04** | Turbulence/transport | potential → E → E×B → fluctuations → transport observables |
| **P05** | Limiter/transport | parameterized boundary conditions → transport scenarios |
| **P06** | Magnetic/MHD | pressure → Mirnov fluctuations → PSD → dominant frequency |

## Evidence and reproducibility

Start here:

- [research_continuity/PORTFOLIO.md](research_continuity/PORTFOLIO.md) — what was done and what can be demonstrated now
- [research_continuity/EVIDENCE_MAP.md](research_continuity/EVIDENCE_MAP.md) — claim → experimental evidence → computational artifact
- [audit/SCIENTIFIC_AUDIT.md](audit/SCIENTIFIC_AUDIT.md) — evidence classification and scientific boundaries
- [audit/RC4_MASTER_AUDIT.md](audit/RC4_MASTER_AUDIT.md) — quantitative reconstruction audit
- [PUBLICATION_TRACEABILITY.md](PUBLICATION_TRACEABILITY.md) — publication-to-workflow mapping
- [provenance/records.json](provenance/records.json) — machine-readable provenance records
- [notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb](notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb) — central executable audit

## Reproducibility

The RC4.2 snapshot was independently checked before publication:

- **14/14** notebooks executed successfully
- **96** automated tests passed
- Python compilation passed
- notebook IDs, execution counts and error outputs were checked
- provenance contains **55** records
- release archive integrity and SHA-256 were verified
- scientific and software audits were repeated before release

The computational workflow is intended to be reusable and inspectable rather than dependent on a single notebook.

## Data policy

Original IR-T1 raw experimental data are **not distributed**. Confidential client/project-specific datasets are also not included.

Where raw measurements are unavailable, the repository uses publication-grounded constraints, digitized publication figures where appropriate, deterministic synthetic data, explicit assumptions, and validation checks.

## Repository structure

~~~text
core/                     Common data models and signal processing
spectroscopy/             Spectroscopic diagnostics
magnetic_diagnostics/     Mirnov/MHD analysis
electrostatic_diagnostics/Probe workflows
turbulence_transport/     Turbulence and transport
hard_xray/                Hard X-ray workflows
cross_diagnostic/         Multi-diagnostic alignment and comparison
publication_reconstruction/ Six publication-grounded cases
research_continuity/      Scientific continuity and evidence map
provenance/               Traceability records
audit/                    Scientific and release audits
notebooks/                Executable demonstrations
figures/                  Flagship outputs
tests/                    Automated validation
~~~

## Quick start

Python 3.11+ is recommended.

~~~bash
python -m pip install -r requirements.txt
pytest -q
~~~

The notebooks can then be opened directly in Jupyter.

## Release

**Current release candidate: v0.1.0-rc4.2**

The exact release archive and its SHA-256 checksum are preserved separately:

- plasma-diagnostics-data-analysis-v0.1.0-rc4.2.zip
- SHA-256: 79a5ed595674e66f017fb41551e4ed30841ccd0b076c4fdbbd831a4be182457e

## Citation

Citation metadata are provided in [CITATION.cff](CITATION.cff).

## License

MIT License — see [LICENSE](LICENSE).
