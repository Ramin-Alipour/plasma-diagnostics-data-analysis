# Evidence Map

| Capability | Experimental / professional evidence | Computational evidence | Repository evidence | Boundary |
|---|---|---|---|---|
| Doppler spectroscopy | IR-T1 experimental spectroscopy | spectral synthesis, fitting, Doppler correction | `P01`; `spectroscopy/` | synthetic reconstruction, not raw recovery |
| Hard X-ray diagnostics | IR-T1 HXR measurements | count/energy and spectrum analysis | `P02`; `hard_xray/` | detector response not reconstructed |
| Mirnov/MHD | IR-T1 magnetic diagnostics | PSD, SVD, spatial mode projection, wavelet | `P02/P06`; `magnetic_diagnostics/` | synthetic multichannel signals |
| Electrostatic probes | IR-T1 Langmuir/compound probes | I-V, E-field, Mach/flow, uncertainty | `P03`; `electrostatic_diagnostics/` | probe transfer function not recovered |
| Turbulence/transport | IR-T1 transport publications | E×B, Reynolds stress, turbulent flux | `P04/P05`; `turbulence_transport/` | model-constrained synthetic inputs |
| Signal processing | experimental + independent analysis practice | filtering, PSD, SVD, wavelets, correlation | `plasma_core/signal_processing/`; `tests/` | client data not public |
| Quantitative analysis | scientific/technical work | Python/MATLAB-oriented workflows | multiple packages | proprietary artifacts excluded |
| Reproducible research | current computational work | tests, notebooks, provenance, audit | `tests/`, `notebooks/`, `plasma_provenance/`, `audit/` | applies to public/reconstructed data |
