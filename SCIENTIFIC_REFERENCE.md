# Scientific Reference

## Project: `plasma-diagnostics-data-analysis`

**Status:** Internal scientific reference for repository development  
**Scientific basis:** Six IR-T1 tokamak experimental publications  
**Data policy:** Original IR-T1 raw experimental data are not distributed; computational demonstrations use synthetic data.

---

## 1. Purpose of This Document

This document is the internal scientific reference for the repository. It records the experimental diagnostics, measured quantities, derived quantities, analysis methods, operating variables, temporal characteristics, and limitations represented by the six selected IR-T1 publications.

The repository is broader than IR-T1. The six publications provide experimental motivation and methodological grounding for generalized, reusable computational workflows. The repository must not imply that its synthetic demonstrations reproduce the original experiments unless a specific workflow has been implemented, validated, and documented as such.

The scientific relationship is:

**Published Experimental Research → Scientific Analysis Methods → Generalized Computational Workflow → Synthetic Reproducible Demonstration**

---

# 2. Reference Set — Exactly Six Publications

Only the following six IR-T1 publications constitute the project's scientific reference set. A seventh publication is intentionally excluded.

## Reference 1 — Spectroscopic Diagnostics

**Alipour, R., Ghoranneviss, M., & Salar Elahi, A. (2017).**  
*First investigation on plasma impurities of the IR-T1 Tokamak.*  
*AIP Advances, 7*(11), 115303.  
DOI: `10.1063/1.4990869`  
Repository source file: `papers/1.4990869 (2).pdf`

### Diagnostic
- Optical/visible plasma-emission spectroscopy
- CCD spectrometer
- Spectral acquisition over approximately 400–550 nm

### Experimental measurement / observable
- Plasma emission spectrum
- Spectral-line positions and line profiles
- Plasma-current and loop-voltage evolution used as contextual plasma parameters

### Analysis methods
- Wavelength calibration
- Spectral-line identification
- Comparison with NIST atomic spectral data
- Assessment of spectral resolution
- Doppler-broadening analysis
- Interpretation of impurity-related spectral features

### Physical quantities / information
- Ion-temperature information from Doppler broadening
- Plasma-flow information associated with Doppler shifts/broadening where applicable
- Impurity species identification / characterization
- Spectral characteristics relevant to plasma conditions

### Reported impurity species
The paper discusses spectral features associated with species including N, O, Cr, C, Mo, Ar, Ni, Ti, Mn, W, and Fe.

### Relevant computational workflow

**Synthetic Spectrum → Wavelength Calibration → Line Identification → Baseline / Preprocessing → Spectral Fitting → FWHM → Doppler Broadening → Temperature Estimate**

### Important limitation
The repository must not claim to reproduce the published IR-T1 temperature or impurity measurement unless the original experimental data, relevant calibration information, and the required analysis procedure are actually available and validated.

---

## Reference 2 — Hard X-ray, Magnetic, and Electrostatic Diagnostics

**Alipour, R., Ghoranneviss, M., & Salar Elahi, A. (2017).**  
*Investigation on the Hard X-ray Radiations of the IR-T1 Tokamak Plasma: Electric and Magnetic Perspectives.*  
*Brazilian Journal of Physics, 47*, 567–574.  
DOI: `10.1007/s13538-017-0536-6`  
Repository source file: `papers/10.1007_s13538-017-0536-6.pdf`

### Diagnostics
- NaI scintillator hard-X-ray detector
- Multichannel analyzer (MCA)
- 12 Mirnov coils
- Rake Langmuir probe
- Poloidal Langmuir probe
- Plasma-current measurement
- Loop-voltage measurement

### Experimental measurement / observable
- Hard-X-ray photon counts / energy spectrum
- Mirnov magnetic-fluctuation signals
- Plasma current
- Loop voltage
- Floating potential
- Electrostatic information used to obtain radial and poloidal electric fields

### Analysis methods
- FFT / frequency-domain analysis and PSD of Mirnov signals
- SVD of the multichannel Mirnov dataset
- Wavelet analysis of dominant principal components
- Spatial-structure analysis
- Poloidal-mode energy analysis
- Cross-diagnostic temporal comparison

### Derived quantities / interpretations
- Edge safety factor from magnetic/plasma parameters
- Radial and poloidal electric fields
- Reynolds-stress-related quantity
- Dominant temporal structures
- Spatial structures / principal axes
- Poloidal-mode energy contribution
- Hard-X-ray spectral characteristics
- Runaway-electron-related energy information

### Reported temporal characteristics
- Dominant MHD activity reported approximately in the 38–46 kHz range.
- The paper analyzes time windows during a discharge extending to approximately 30 ms in the presented X-ray analysis.

### Important mathematical convention
The published paper constructs its SVD data matrix with time as rows and Mirnov channels as columns. The repository uses the project-wide convention **channels × time** for its internal data model. The published orientation and the repository orientation must therefore be treated as explicit representation choices rather than silently equated.

### Important interpretation limitation
SVD principal components and principal axes are mathematical decompositions of the measured multichannel data. They may reveal coherent temporal/spatial structures, but repository documentation must not automatically label every mathematical component as a physically identified MHD mode.

---

## Reference 3 — Compound Electrostatic Probe

**Alipour, R., Ghoranneviss, M., & Salar Elahi, A. (2017).**  
*Design and fabrication of a new compound probe for plasma flux measurement in IR-T1 tokamak.*  
*Review of Scientific Instruments, 88*(9), 093516.  
DOI: `10.1063/1.4994037`  
Repository source file: `papers/10.1063@1.4994037 (2).pdf`

### Diagnostic
A compound probe combining:
- Ball-pen probe
- Gundestrup probe

The paper describes diagnostic design, fabrication, installation, and operation on IR-T1.

### Experimental measurement / observable
- Plasma potential information from the ball-pen component
- Electron-temperature information from the ball-pen measurement/model
- Ion-saturation-current measurements from the Gundestrup collectors
- Direction-sensitive current information for flow analysis

### Derived quantities
- Electron temperature
- Plasma potential
- Parallel Mach number
- Perpendicular Mach number
- Parallel / directional plasma-flow information

### Representative reported values
- Edge electron temperature: approximately 14 eV
- Plasma potential: approximately 44 V
- Mean parallel Mach number: approximately 0.5
- Mean perpendicular Mach number: approximately 0
- Representative parallel flow velocity: approximately 17 km/s

These values are **published experimental results**, not default values for future synthetic datasets.

### Relevant computational workflow

**Probe Signals → Signal Quality / Preprocessing → Probe-Specific Relations → Plasma Parameters → Directional Flow → Mach Numbers**

### Important limitation
Probe-derived quantities depend on the probe geometry, calibration, sheath/collection model, operating conditions, and assumptions used by the diagnostic. A generalized software implementation must expose these assumptions rather than silently treating them as universal constants.

---

## Reference 4 — Turbulent Transport versus Pressure

**Alipour, R., Meshkani, S., Elahi, A. S., & Ghoranneviss, M. (2017).**  
*Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma.*  
*The European Physical Journal D, 71*, 60.  
DOI: `10.1140/epjd/e2017-70563-6`  
Repository source file: `papers/Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma (2).pdf`

### Experimental control variable
Hydrogen pressure, with representative conditions around:
- 1.9 Torr
- 2.3 Torr
- 2.7 Torr

### Diagnostic / measurement basis
- Langmuir-probe measurements
- Floating-potential signals
- Ion-saturation-current signals
- Plasma current
- Loop voltage

### Derived quantities / analysis
- Radial electric field
- Poloidal electric field
- Fluctuation characteristics
- Radial turbulent transport
- Poloidal turbulent transport
- Reynolds-stress-related quantity

### Relevant computational workflow

**Control Parameter → Diagnostic Signals → Mean / Fluctuating Components → Correlation → Electric-Field Quantities → Reynolds-Stress / Transport Quantity → Parameter Response**

### Scientific interpretation
The paper investigates how turbulent transport and related fluctuation/electric-field quantities respond to changes in plasma pressure and limiter bias conditions.

### Repository limitation
The repository may reproduce the **methodology** with controlled synthetic signals, but it must not present synthetic results as numerical reproduction of the published pressure scan unless the original experimental data and analysis conditions are available.

---

## Reference 5 — Turbulent Transport versus Biased-Limiter Position

**Alipour, R., Ghoranneviss, M., Elahi, A. S., & Meshkani, S. (2017).**  
*Effects of the location of a biased limiter on turbulent transport in the IR-T1 tokamak plasma.*  
*The European Physical Journal D, 71*, 228.  
DOI: `10.1140/epjd/e2017-80215-6`  
Repository source file: `papers/d170215 (2).pdf`

### Experimental control variables
- Limiter position
- Limiter bias voltage

Representative limiter locations discussed in the project reference:
- Plasma edge
- Approximately 5 mm inside the plasma
- Approximately 10 mm inside the plasma

Representative bias conditions include positive and negative values up to approximately ±200 V.

### Diagnostic / measurement basis
- Plasma current
- Loop voltage
- Electrostatic-probe measurements
- Radial electric field
- Poloidal electric field
- Fluctuation signals

### Derived quantities / analysis
- Radial turbulent transport
- Poloidal turbulent transport
- Reynolds stress
- Response of electric fields and fluctuation quantities to limiter position and bias

### Relevant computational workflow

**Limiter Position / Bias → Diagnostic Signals → Fluctuation Analysis → Electric Fields → Reynolds Stress → Turbulent Transport → Parameter Response**

### Repository limitation
The software should represent the parameter-scan methodology and relationships using controlled synthetic data. Published percentage changes must not be treated as validation targets unless the original data and the exact published analysis procedure are available.

---

## Reference 6 — Magnetic MHD Fluctuations versus Pressure

**Alipour, R., & Ghanbari, M. R. (2018).**  
*Magnetic evaluation of hydrogen pressures changes on MHD fluctuations in IR-T1 tokamak plasma.*  
*The European Physical Journal D, 72*, 75.  
DOI: `10.1140/epjd/e2018-90033-y`  
Repository source file: `papers/10.1140.pdf`

### Experimental control variable
Hydrogen pressure:
- 1.9 Torr
- 2.5 Torr
- 2.9 Torr

### Diagnostic
- 12 Mirnov coils
- Plasma current
- Loop voltage

### Analysis methods
- FFT / PSD
- SVD
- Wavelet analysis
- Principal components
- Principal axes / spatial structures
- Poloidal-mode energy analysis

### Temporal structure
The paper considers three discharge phases:
- Rising phase
- Stable phase
- Falling / ramp-down phase

### Reported spectral characteristic
- MHD activity is reported approximately around 44 kHz.
- The PSD discussion describes MHD activity in approximately the 40–50 kHz range.

### Derived / analyzed quantities
- Dominant temporal structures
- Dominant spatial structures
- Poloidal-mode energy percentages
- Frequency-domain fluctuation characteristics
- Pressure-dependent changes in MHD activity

### Repository relevance
This paper is the primary scientific basis for the first development vertical slice:

**Synthetic Mirnov Data → Preprocessing → PSD → SVD → Wavelet → Visualization → Notebook → Tests**

### Important interpretation limitation
The repository should use the paper to motivate analysis of coherent multichannel magnetic fluctuations. It must not assume that a synthetic component at ~44 kHz constitutes a measured IR-T1 mode or that an SVD component is automatically a physically identified mode.

---

# 3. Cross-Paper Scientific Inventory

## 3.1 Diagnostic Domains

| Domain | IR-T1 reference(s) | Main experimental basis |
|---|---|---|
| Spectroscopy | 1 | CCD visible emission spectroscopy |
| Magnetic diagnostics | 2, 6 | Mirnov-coil arrays |
| Electrostatic diagnostics | 2, 3, 4, 5 | Langmuir, rake, poloidal, ball-pen, Gundestrup/compound probes |
| Turbulence / transport | 4, 5 | Probe fluctuations, electric fields, Reynolds-stress / transport analysis |
| Hard X-ray | 2 | NaI scintillator + MCA |

## 3.2 Core Measured Signals / Observables

- Plasma emission spectra
- Spectral line position and profile
- Mirnov-coil magnetic signals
- Langmuir-probe signals
- Floating potential
- Ion saturation current
- Hard-X-ray counts / energy spectrum
- Plasma current
- Loop voltage
- Experimental operating parameters such as hydrogen pressure, limiter position, and limiter bias

## 3.3 Derived / Estimated Quantities

- Ion temperature from Doppler-broadening analysis
- Plasma flow information from Doppler shift and/or probe-based flow analysis
- Impurity characterization from spectral-line identification
- Plasma potential
- Electron temperature
- Mach numbers
- Electric fields
- Reynolds-stress-related quantities
- Turbulent transport quantities
- PSD / frequency-domain characteristics
- SVD singular values, principal components, and spatial structures
- Wavelet time-frequency representations
- Poloidal-mode energy quantities
- Edge safety factor where the required magnetic/plasma inputs are available

The software must preserve the distinction between a directly acquired signal and a quantity computed or inferred from that signal.

---

# 4. Analysis Methods Represented by the Reference Set

## 4.1 Spectral Analysis

- Wavelength calibration
- Spectral-line identification
- Spectral fitting
- FWHM estimation
- Doppler-broadening analysis
- FFT
- PSD

## 4.2 Time-Frequency Analysis

- Wavelet transform
- Time-localized spectral characterization
- Temporal evolution of dominant fluctuation components

## 4.3 Multichannel Decomposition

- SVD
- Singular-value analysis
- Principal components
- Spatial / channel structures
- Reconstruction from retained components

## 4.4 Statistical / Correlation Analysis

- Mean and fluctuation decomposition
- Correlation
- Cross-correlation
- Relationships between complementary diagnostics
- Parameter-response analysis

## 4.5 Diagnostic-Specific Physical Analysis

- Doppler temperature estimation
- Probe-based plasma-parameter extraction
- Electric-field estimation
- Reynolds-stress analysis
- Turbulent transport analysis
- Hard-X-ray spectral / temporal analysis

---

# 5. Experimental Variables and Parameter Scans

The six publications motivate several classes of experimental variables:

### Plasma operating parameters
- Hydrogen pressure
- Plasma current
- Loop voltage
- Magnetic-field conditions

### Edge / bias conditions
- Limiter position
- Limiter bias voltage

### Diagnostic / acquisition parameters
- Wavelength range
- Spectrometer resolution
- Entrance-slit width
- Integration time
- Detector response / calibration
- Sampling and acquisition conditions

The software architecture should treat experimental variables as explicit metadata rather than hidden constants.

---

# 6. Temporal and Frequency Characteristics

The reference set contains several experimentally relevant time scales and frequency-domain features.

### Magnetic fluctuations
- MHD activity around tens of kHz is repeatedly analyzed.
- One paper reports approximately 38–46 kHz.
- Another reports approximately 40–50 kHz and identifies activity around approximately 44 kHz.

### Discharge evolution
- IR-T1 discharge durations in the cited studies are on the order of tens of milliseconds.
- The magnetic-pressure study explicitly separates rising, stable, and falling phases.
- The hard-X-ray study analyzes multiple time windows across the discharge.

### Repository implication
Synthetic magnetic data should contain explicit, configurable characteristic frequencies and temporal evolution. A nominal frequency such as 44 kHz is a **synthetic design parameter informed by the literature**, not an assertion that the synthetic signal is an IR-T1 measurement.

---

# 7. Measured vs Derived vs Estimated vs Synthetic

This distinction is mandatory throughout the repository.

| Category | Meaning in this project | Examples |
|---|---|---|
| **Measured** | Directly acquired experimental observable | CCD intensity, Mirnov voltage/signal, probe current, floating-potential signal, X-ray counts |
| **Derived** | Calculated from measured quantities using an explicit relation | Electric field, Reynolds stress, PSD, SVD components, mode-energy quantity |
| **Estimated** | Physical quantity inferred through a model, fit, calibration, or diagnostic relation | Doppler temperature, electron temperature, flow velocity, Mach number |
| **Synthetic** | Computationally generated demonstration data | Synthetic Mirnov channels, synthetic spectra, synthetic probe I–V curves |
| **Assumed** | Parameter or model choice introduced by the software/workflow | Noise model, calibration constants in a synthetic case, wavelet settings |
| **Illustrative** | Example chosen to explain a method rather than represent an experiment | Demonstration parameter scan or example figure |

A synthetic value must never be described as a measured IR-T1 value.

---

# 8. Critical Scientific Constraints

## 8.1 Phase Space / Velocity Space

The six IR-T1 papers do **not** provide a basis for claiming that IR-T1 directly measured plasma phase-space or velocity-space distributions.

Supported concepts include:
- Doppler-broadening information
- Doppler-shift / flow information
- Probe-based plasma-flow measurements
- Mach-number measurements / estimates
- Magnetic fluctuations
- Electrostatic fluctuations
- Turbulent transport
- Hard-X-ray radiation

Future phase-space or velocity-space functionality must initially be labeled as synthetic, methodological, computational, or future experimental extension unless suitable experimental distribution-function data are available.

## 8.2 SVD and Physical Mode Identification

SVD is a mathematical decomposition. Singular values, principal components, and spatial/channel structures should be described as mathematical outputs first. Physical MHD-mode identification requires additional physical interpretation and appropriate diagnostic geometry, timing, and mode-analysis assumptions.

## 8.3 Synthetic Data

Synthetic data must be designed to reproduce relevant characteristics of the intended diagnostic problem, such as:
- characteristic frequencies
- multichannel structure
- phase relationships
- amplitude variation
- noise
- temporal evolution
- spectral peaks
- spatial/channel relationships

Purely arbitrary random signals are not an adequate substitute for scientifically meaningful synthetic demonstrations.

## 8.4 Published Numerical Results

Published numerical values are reference facts about the experiments. They are not automatically validation targets for synthetic software. A numerical reproduction claim requires access to appropriate data and a documented analysis procedure that can actually reproduce the stated quantity.

---

# 9. Methodological Mapping to Repository Architecture

| Scientific basis | Repository area |
|---|---|
| Doppler / emission spectroscopy | `spectroscopy/` |
| Mirnov fluctuation analysis | `magnetic_diagnostics/` |
| Langmuir / compound probe analysis | `electrostatic_diagnostics/` |
| Reynolds stress / turbulent transport | `turbulence_transport/` |
| Hard-X-ray analysis | `hard_xray/` |
| Synthetic diagnostic signals | `synthetic_data/` |
| Demonstration workflows | `notebooks/` |
| Scientific figures | `figures/` |
| Numerical and scientific tests | `tests/` |

Common operations such as preprocessing, FFT/PSD, filtering, normalization, correlation, and validation should be implemented as reusable infrastructure rather than copied into each diagnostic domain.

---

# 10. Relationship to the First Vertical Slice

The first implementation target is deliberately based on the magnetic-analysis papers because they provide a clear multichannel signal-processing workflow that can be demonstrated without distributing experimental data.

### Scientific basis
- 12-channel Mirnov measurements
- MHD fluctuation analysis
- Frequency-domain analysis
- SVD
- Wavelet analysis
- Temporal and spatial structures

### Computational implementation

**Synthetic Mirnov Dataset → Common Preprocessing → PSD → SVD → Wavelet → Visualization → Notebook → Tests**

### Validation strategy

A controlled synthetic case should contain known frequencies, known multichannel relationships, controlled noise, and reproducible parameters. The software should then verify recovery of those known properties.

The result is a **scientifically controlled computational demonstration**, not an experimental reproduction of the IR-T1 dataset.

---

# 11. Unified Cross-Diagnostic Computational Extension

Section 11 implements one reusable cross-diagnostic integration layer for controlled synthetic demonstrations. It is intentionally not a set of hard-coded diagnostic-pair scripts. The demonstrated pairings are:

1. Magnetic diagnostics ↔ hard X-ray signals
2. Electrostatic fluctuations ↔ turbulence/transport quantities

The common interface requires an explicit shared time base. `interpolate_to_time()` and `resample_time_series()` are separate operations, and `align_time_series()` does not silently resample signals when sampling frequencies differ. Alignment is restricted to the temporal overlap and records the selected alignment method in metadata.

Version-1 comparisons include zero-lag Pearson correlation, normalized cross-correlation with a temporal lag, and Welch PSD comparison. A lag is reported only as a temporal offset; the workflow does not infer causality. Existing SVD/PCA functionality is reused rather than duplicated.

Experimental conditions such as pressure, limiter position, and limiter bias are represented separately from numerical signal arrays through `ExperimentalCondition` metadata. All Section 11 demonstrations use synthetic data and therefore do not constitute reconstructions of original IR-T1 raw measurements.

# 12. Limitations of the Scientific Reference

1. The repository does not distribute the original IR-T1 raw datasets.
2. Published figures and numerical results cannot automatically be reproduced from the papers alone.
3. Some diagnostic-derived quantities depend on calibration constants, geometry, assumptions, and models that must be explicitly represented in software.
4. The published SVD matrix orientation is not identical to the repository's project-wide `channels × time` convention; the conversion must be explicit.
5. Physical mode identification requires more than a generic mathematical decomposition.
6. Synthetic demonstrations cannot be described as experimental measurements.
7. Velocity-sensitive measurements do not imply direct measurement of a full velocity-space distribution.
8. Future machine-learning, phase-space, uncertainty-quantification, and advanced cross-diagnostic capabilities are extensions, not evidence contained in the six reference papers.

---

# 13. Development Status of This Reference

This document covers the **scientific-reference layer** for the current repository architecture, including the implemented Sections 1–11.

It is an internal working reference and may be refined when an implementation exposes a genuine ambiguity or when a scientific assumption is explicitly documented. Such refinements must not silently change the six-paper reference set or the project's core scientific constraints.

---

# 14. Reference Files

The six source PDFs are maintained in the project Library under `/papers/`:

1. `1.4990869 (2).pdf`
2. `10.1007_s13538-017-0536-6.pdf`
3. `10.1063@1.4994037 (2).pdf`
4. `Investigation on the effect of pressure on turbulent transports of the IR-T1 Tokamak plasma (2).pdf`
5. `d170215 (2).pdf`
6. `10.1140.pdf`

These files are the authoritative source documents for the six-paper scientific reference set.

## Publication Traceability

The six-paper scientific reference set is mapped explicitly to repository modules, notebooks, tests, and synthetic validation in [`PUBLICATION_TRACEABILITY.md`](PUBLICATION_TRACEABILITY.md). This mapping is intended to make the methodological continuity between the published IR-T1 experimental work and the current research-software artifact auditable without claiming exact reproduction of the papers.



## Publication-Grounded Reconstruction

See `PUBLICATION_RECONSTRUCTION.md` for the six-paper reconstruction study, provenance classes, limitations, and validation scope.
