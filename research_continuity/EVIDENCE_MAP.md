# Evidence Map

| Capability | Experimental / professional evidence | Computational evidence | Repository evidence | Boundary |
|---|---|---|---|---|
| **Data provenance (repository-wide)** | **Dataset A: real supplied raw laboratory measurements and diagnostic device/software outputs, including E06** | Dataset B: publication-extracted/reconstructed data; separate, explicitly labelled synthetic inputs for selected demonstrations | Dataset A / Dataset B manifests, P01, notebooks and audit records | The absence of a complete IR-T1 shot archive does not mean Dataset A is absent or synthetic |
|---|---|---|---|---|
| Doppler spectroscopy | Historical IR-T1 work plus real supplied laboratory/device-software measurements in Dataset A | Dataset A line-width analysis; separate synthetic fitting tests; Dataset B publication-derived values where identified | `P01`; `spectroscopy/` | Dataset A is real supplied measurement/output data; synthetic tests do not recover original IR-T1 shot arrays |
| Hard X-ray diagnostics | IR-T1 HXR measurements | count/energy and spectrum analysis | `P02`; `hard_xray/` | detector response not reconstructed |
| Mirnov/MHD | Historical IR-T1 magnetic-diagnostic publications | PSD, SVD, spatial mode projection, wavelet on labelled synthetic demonstration signals and publication constraints | `P02/P06`; `magnetic_diagnostics/` | Synthetic multichannel examples are distinct from Dataset A; complete original IR-T1 shot arrays are not included |
| Electrostatic probes | IR-T1 Langmuir/compound probes | I-V, E-field, Mach/flow, uncertainty | `P03`; `electrostatic_diagnostics/` | probe transfer function not recovered |
| Turbulence/transport | IR-T1 transport publications | E×B, Reynolds stress, turbulent flux workflows using labelled model-constrained synthetic inputs and separately identified Dataset B values | `P04/P05`; `turbulence_transport/` | Computational examples do not replace Dataset A or claim to recover original probe traces |
| Signal processing | experimental + independent analysis practice | filtering, PSD, SVD, wavelets, correlation | `plasma_core/signal_processing/`; `tests/` | client data not public |
| Quantitative analysis | scientific/technical work | Python/MATLAB-oriented workflows | multiple packages | proprietary artifacts excluded |
| Reproducible research | current computational work | tests, notebooks, provenance, audit | `tests/`, `notebooks/`, `plasma_provenance/`, `audit/` | applies to public/reconstructed data |
