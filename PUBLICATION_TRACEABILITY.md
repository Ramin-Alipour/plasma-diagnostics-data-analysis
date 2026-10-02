# Publication-to-Project Traceability

## Purpose

This document records the scientific relationship between the six IR-T1 publications that form the project's initial scientific reference set and the implemented research-software workflows in `plasma-diagnostics-data-analysis`.

The purpose is traceability, not a claim of exact paper reproduction. Original IR-T1 raw experimental datasets are not distributed with this repository. The implemented demonstrations therefore use synthetic or controlled computational data, and the distinction between published experimental evidence and new computational capability is maintained throughout.

The relationship represented here is:

```text
Published IR-T1 experiment
        ↓
Diagnostic / analysis method
        ↓
Generalized repository workflow
        ↓
Synthetic or controlled computational demonstration
        ↓
Tests / scientific validation
```

## Six-paper reference set

The six papers below are the fixed initial scientific reference set for the project.

### 1. Optical/CCD spectroscopy and plasma impurities

**Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017).** First investigation on plasma impurities of the IR-T1 Tokamak. *AIP Advances, 7*(11), 115303. DOI: `10.1063/1.4990869`.

**Experimental / scientific basis**
- Optical/CCD spectroscopic measurement of IR-T1 plasma emission.
- Spectral-line identification and wavelength calibration.
- Doppler-broadening analysis for plasma-temperature information.
- Impurity-related spectral analysis.

**Repository traceability**
- Section 7 — `spectroscopy/`
- `spectroscopy/calibration/`
- `spectroscopy/line_identification/`
- `spectroscopy/spectral_fitting/`
- `spectroscopy/doppler_broadening/`
- `spectroscopy/synthetic.py`
- `notebooks/publication_reconstruction/P01_IRT1_spectroscopy_reconstruction.ipynb`
- `notebooks/publication_reconstruction/P01_full_spectroscopy_showcase.ipynb`
- `notebooks/spectroscopy/01_doppler_broadening.ipynb`
- `tests/test_spectroscopy.py`

**What the repository demonstrates**
A generalized, synthetic spectroscopy workflow from wavelength calibration and line identification through Gaussian fitting, FWHM/Doppler broadening, and temperature recovery from controlled synthetic spectra.

**Reproducibility status**
Methodological/synthetic demonstration. It does **not** reproduce the original IR-T1 measurements or published numerical results because the original experimental data are not distributed.

**Transferable research capability represented**
Spectral-data analysis, quantitative Doppler-broadening analysis, calibration-aware interpretation, and conversion of spectroscopic measurements into physically interpretable plasma quantities.

---

### 2. Hard X-ray, magnetic, and electrostatic diagnostics

**Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017).** Investigation on the Hard X-ray Radiations of the IR-T1 Tokamak Plasma: Electric and Magnetic Perspectives. *Brazilian Journal of Physics, 47*, 567–574. DOI: `10.1007/s13538-017-0536-6`.

**Experimental / scientific basis**
- NaI-scintillator hard-X-ray detection and MCA spectrum acquisition.
- 12-channel Mirnov magnetic measurements.
- Rake and poloidal Langmuir-probe measurements.
- Plasma current and loop-voltage measurements.
- SVD, wavelet, PSD/frequency analysis, and relationships between diagnostic signals.

**Repository traceability**
- Section 6 — `magnetic_diagnostics/`
- Section 8 — `electrostatic_diagnostics/`
- Section 10 — `hard_xray/`
- Section 11 — `cross_diagnostic/`
- `core/signal_processing/`
- `notebooks/publication_reconstruction/P02_IRT1_hxr_mirnov_reconstruction.ipynb`
- `notebooks/magnetic_diagnostics/01_mirnov_svd_wavelet.ipynb`
- `notebooks/hard_xray/01_xray_mhd_correlation.ipynb`
- `notebooks/cross_diagnostic/01_cross_diagnostic_analysis.ipynb`
- `tests/test_magnetic_diagnostics.py`
- `tests/test_hard_xray.py`
- `tests/test_electrostatic_diagnostics.py`
- `tests/test_cross_diagnostic.py`

**What the repository demonstrates**
A generalized multi-diagnostic analysis architecture covering magnetic fluctuations, hard-X-ray signals, electrostatic measurements, and explicit cross-diagnostic alignment/correlation.

**Important limitation**
The repository does not claim to reproduce the reported IR-T1 hard-X-ray spectrum, runaway-electron energy, or experimental correlations. Those published observations remain experimental evidence from the paper; the repository demonstrates related analysis methods on controlled synthetic data.

**Transferable research capability represented**
Multichannel diagnostic analysis, signal processing, SVD/wavelet analysis, hard-X-ray signal/spectrum analysis, and integration of complementary diagnostic measurements.

---

### 3. Compound probe and plasma-flow measurement

**Alipour, R., Ghoranneviss, M., & Elahi, A. S. (2017).** Design and fabrication of a new compound probe for plasma flux measurement in IR-T1 tokamak. *Review of Scientific Instruments, 88*, 093516. DOI: `10.1063/1.4994037`.

**Experimental / scientific basis**
- Diagnostic design and fabrication of a compound probe.
- Experimental implementation and plasma-flux measurement.
- Extraction of plasma-flow and Mach-number quantities from directional measurements.

**Repository traceability**
- Section 8 — `electrostatic_diagnostics/compound_probe/`
- `electrostatic_diagnostics/compound_probe/flow.py`
- `electrostatic_diagnostics/compound_probe/synthetic.py`
- `notebooks/publication_reconstruction/P03_IRT1_compound_probe_reconstruction.ipynb`
- `tests/test_electrostatic_diagnostics.py`

**What the repository demonstrates**
A computational analysis layer for directional electrostatic measurements, including synthetic velocity recovery and Mach-number consistency checks.

**Important limitation**
The repository does not reproduce the mechanical design, fabrication, installation, or original IR-T1 measurements of the published probe. Those are documented experimental contributions of the publication. The repository represents the corresponding quantitative analysis concepts.

**Transferable research capability represented**
Connecting diagnostic measurement concepts to derived plasma-flow quantities and maintaining a clear distinction between measured and derived parameters.

---

### 4. Turbulent transport versus hydrogen pressure

**Alipour, R., Meshkani, S., Elahi, A. S., & Ghoranneviss, M. (2017).** Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma. *The European Physical Journal D, 71*, 60. DOI: `10.1140/epjd/e2017-70563-6`.

**Experimental / scientific basis**
- Variation of hydrogen pressure and limiter biasing conditions.
- Fluctuating electrostatic measurements.
- Electric-field-related quantities.
- Reynolds-stress and turbulent-transport analysis.

**Repository traceability**
- Section 9 — `turbulence_transport/`
- `turbulence_transport/fluctuations/`
- `turbulence_transport/reynolds_stress/`
- `turbulence_transport/transport_analysis/`
- `notebooks/publication_reconstruction/P04_IRT1_pressure_transport_reconstruction.ipynb`
- `notebooks/turbulence_transport/01_reynolds_stress.ipynb`
- `tests/test_turbulence_transport.py`

**What the repository demonstrates**
A generalized synthetic workflow for separating fluctuations, computing correlations/Reynolds stress, deriving electric-field-related quantities, and evaluating turbulent flux/transport quantities.

**Reproducibility status**
Methodological/synthetic demonstration. The repository does not reproduce the pressure-dependent published transport values without the original experimental datasets.

**Transferable research capability represented**
Quantitative plasma-fluctuation analysis, Reynolds-stress methods, turbulent-transport calculations, and interpretation of transport in relation to experimental conditions.

---

### 5. Turbulent transport versus biased-limiter position

**Alipour, R., Ghoranneviss, M., Elahi, A. S., & Meshkani, S. (2017).** Effects of the location of a biased limiter on turbulent transport in the IR-T1 tokamak plasma. *The European Physical Journal D, 71*, 228. DOI: `10.1140/epjd/e2017-80215-6`.

**Experimental / scientific basis**
- Variation of biased-limiter position and bias conditions.
- Plasma fluctuations and electric-field-related quantities.
- Reynolds-stress and turbulent-transport response to experimental configuration.

**Repository traceability**
- Section 9 — `turbulence_transport/`
- `turbulence_transport/transport_analysis/parameter_scans.py`
- `turbulence_transport/reynolds_stress/`
- `notebooks/publication_reconstruction/P05_IRT1_limiter_transport_reconstruction.ipynb`
- `notebooks/turbulence_transport/01_reynolds_stress.ipynb`
- `tests/test_turbulence_transport.py`

**What the repository demonstrates**
A generalized parameter-scan architecture in which an explicitly synthetic experimental/control parameter can be varied and related to diagnostic or transport quantities.

**Important limitation**
The parameter-scan implementation is explicitly synthetic. It must not be interpreted as a reproduction of the published limiter-position measurements or their reported percentage changes.

**Transferable research capability represented**
Parameter-dependent experimental analysis, transport-response organization, correlation-based interpretation, and separation of experimental control variables from measured/derived quantities.

---

### 6. Magnetic MHD fluctuations versus hydrogen pressure

**Alipour, R., & Ghanbari, M. R. (2018).** Magnetic evaluation of hydrogen pressure changes on MHD fluctuations in IR-T1 tokamak plasma. *The European Physical Journal D, 72*, 75. DOI: `10.1140/epjd/e2018-90033-y`.

**Experimental / scientific basis**
- 12-channel Mirnov-coil measurements.
- Hydrogen-pressure variation.
- SVD and wavelet analysis.
- PSD and analysis of temporal/spatial MHD structures and poloidal-mode energy.

**Repository traceability**
- Section 6 — `magnetic_diagnostics/`
- `synthetic_data/magnetic/mirnov.py`
- `magnetic_diagnostics/preprocessing.py`
- `magnetic_diagnostics/fft_psd.py`
- `magnetic_diagnostics/wavelet.py`
- `magnetic_diagnostics/svd.py`
- `magnetic_diagnostics/mode_analysis.py`
- `notebooks/publication_reconstruction/P06_IRT1_pressure_mhd_reconstruction.ipynb`
- `notebooks/magnetic_diagnostics/01_mirnov_svd_wavelet.ipynb`
- `tests/test_synthetic_mirnov.py`
- `tests/test_magnetic_diagnostics.py`

**What the repository demonstrates**
A controlled multichannel Mirnov-like synthetic workflow with explicit sampling information, known frequency content, controlled channel relationships, PSD, wavelet analysis, SVD, and spatial/channel-structure analysis.

**Important limitation**
SVD outputs are mathematical decompositions and are not automatically identified with physical MHD modes. The repository does not reproduce the pressure-dependent IR-T1 experimental results.

**Transferable research capability represented**
Multichannel magnetic-diagnostic analysis, time/frequency/time-localized analysis, matrix decomposition, spatial/temporal structure extraction, and scientifically cautious interpretation of MHD-related signals.

---

## Dedicated reconstruction notebooks

Each paper now has a directly linked publication-reconstruction notebook in addition to the relevant domain-analysis notebook(s):

| Paper | Dedicated reconstruction notebook |
|---|---|
| P01 | [P01 spectroscopy reconstruction](notebooks/publication_reconstruction/P01_IRT1_spectroscopy_reconstruction.ipynb) · [P01 full spectroscopy showcase](notebooks/publication_reconstruction/P01_full_spectroscopy_showcase.ipynb) |
| P02 | [P02 HXR + Mirnov reconstruction](notebooks/publication_reconstruction/P02_IRT1_hxr_mirnov_reconstruction.ipynb) |
| P03 | [P03 compound-probe reconstruction](notebooks/publication_reconstruction/P03_IRT1_compound_probe_reconstruction.ipynb) |
| P04 | [P04 pressure/transport reconstruction](notebooks/publication_reconstruction/P04_IRT1_pressure_transport_reconstruction.ipynb) |
| P05 | [P05 limiter/transport reconstruction](notebooks/publication_reconstruction/P05_IRT1_limiter_transport_reconstruction.ipynb) |
| P06 | [P06 pressure/MHD reconstruction](notebooks/publication_reconstruction/P06_IRT1_pressure_mhd_reconstruction.ipynb) |

The central audit notebook is [00_six_paper_reconstruction_audit.ipynb](notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb).

## Cross-paper capability map

The six papers collectively motivate the project's main diagnostic-analysis capabilities:

| Scientific capability | Primary paper(s) | Repository implementation | Demonstration layer |
|---|---|---|---|
| Optical spectroscopy / Doppler analysis | Paper 1 | `spectroscopy/` | spectroscopy notebook + tests |
| Hard-X-ray signal/spectrum analysis | Paper 2 | `hard_xray/` | HXR notebook + tests |
| Multichannel magnetic fluctuation analysis | Papers 2, 6 | `magnetic_diagnostics/` | magnetic notebook + tests |
| Electrostatic probe analysis | Papers 2, 3 | `electrostatic_diagnostics/` | Langmuir notebook + tests |
| Plasma-flow / Mach-number analysis | Paper 3 | `electrostatic_diagnostics/compound_probe/` | synthetic validation + tests |
| Turbulence / Reynolds-stress analysis | Papers 2, 4, 5 | `turbulence_transport/` | turbulence notebook + tests |
| Parameter-dependent transport analysis | Papers 4, 5, 6 | `turbulence_transport/transport_analysis/` | synthetic parameter scans + tests |
| Cross-diagnostic analysis | Paper 2, with methods generalized across the project | `cross_diagnostic/` | cross-diagnostic notebook + tests |

## What this traceability establishes

This mapping provides a defensible bridge between the earlier IR-T1 experimental research and the current research-software project:

```text
IR-T1 experimental publications
        ↓
Established diagnostic experience and analysis methods
        ↓
Generalized computational architecture
        ↓
Reusable Python implementations
        ↓
Controlled synthetic demonstrations
        ↓
Numerical/scientific validation tests
        ↓
Current reproducible research-software artifact
```

It does **not** establish that the repository reproduces the six publications. It establishes that the repository is methodologically grounded in the diagnostic and quantitative-analysis problems represented by those publications, while explicitly separating published experimental evidence from newly implemented computational demonstrations.

## Relationship to the development Sections

The scientific traceability layer primarily connects the publication set to the implemented diagnostic and integration Sections:

- **Sections 1–5:** project foundation, common data/analysis infrastructure, and supporting architecture.
- **Section 6:** magnetic diagnostics; directly connected to Papers 2 and 6.
- **Section 7:** spectroscopy; directly connected to Paper 1.
- **Section 8:** electrostatic diagnostics and compound-probe analysis; directly connected to Papers 2 and 3.
- **Section 9:** turbulence and transport; directly connected to Papers 4 and 5 and methodologically related to Paper 2.
- **Section 10:** hard-X-ray diagnostics; directly connected to Paper 2.
- **Section 11:** unified cross-diagnostic analysis; directly connected to the multi-diagnostic character of Paper 2 and generalized beyond that single experiment.
- **Section 12:** release, reproducibility, audit, and documentation; this traceability document is part of that release/audit layer rather than a new scientific-analysis capability.

## Career-continuity interpretation

This repository should be presented as a **current research-software and scientific-data-analysis activity grounded in the user's earlier experimental plasma research**, not as a replacement for missing experimental employment or as evidence that new experiments were performed during the intervening period.

The defensible continuity is:

```text
Experimental IR-T1 plasma diagnostics
        ↓
Peer-reviewed research and quantitative analysis
        ↓
Transferable Python/MATLAB scientific-data-analysis practice
        ↓
Current reproducible plasma-diagnostics research software
```

This distinction is important for CVs, research statements, and job applications: the project can provide current evidence of active technical/research engagement, while the employment history and publications should continue to state the underlying dates and roles accurately.


## Publication-Grounded Reconstruction

See `PUBLICATION_RECONSTRUCTION.md` for the six-paper reconstruction study, provenance classes, limitations, and validation scope.
