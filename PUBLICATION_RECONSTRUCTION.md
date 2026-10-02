# Publication-Grounded Reconstruction Study

## Purpose

This study turns the six selected IR-T1 publications into a reproducible, quantitatively testable synthetic-reconstruction benchmark. It is **not** a recovery of the original raw experimental data and must not be presented as such.

The evidence chain is:

`published experimental result -> extracted numerical constraints -> reconstructed synthetic/raw-like measurement -> repository analysis workflow -> reconstructed observable -> comparison with the publication`

## Six-paper coverage

| Paper | Reconstructed dataset | Direct numerical constraints | Main workflow exercised | Status |
|---|---|---|---|---|
| P01 spectroscopy/impurities | synthetic Gaussian spectral lines | Table VI measured/resolution/Doppler widths; Table VII ion temperatures | calibration → Doppler broadening → ion temperature | quantitative validation |
| P02 HXR + MHD | HXR event energies + 12-channel Mirnov matrix | Table 1 HXR counts/energy; Table 2 mode-energy fractions/q | HXR spectrum + SVD + PSD + cross-diagnostic basis | quantitative validation |
| P03 compound probe | synthetic up/down saturation currents | probe geometry, k=1.7, Ti/Te=0.2, h=0.5 mm, Te≈14 eV, Ip≈16 kA | saturation-current ratio → Mach number | model-constrained validation |
| P04 pressure/turbulence | pressure-dependent synthetic E-field/transport traces | 1.9/2.3/2.7 Torr, current/steady-state values, reported transport ranges | E-field → E×B proxy → transport/Reynolds workflow | range-constrained reconstruction |
| P05 limiter/bias | synthetic limiter-position/bias transport traces | ±200 V, 0/5/10 mm, reported percentage/range effects | electrostatic + turbulence/transport | effect-constrained reconstruction |
| P06 pressure/MHD | 12-channel Mirnov matrices for 1.9/2.5/2.9 Torr | pressure, steady-state times, 44 kHz dominant activity, Fig. 5 windows | SVD + PSD + wavelet-ready multichannel data | frequency-constrained reconstruction |

## Provenance classes

Every constraint file distinguishes what is actually known:

- `exact_table`: copied from a numerical table in the paper.
- `exact_reported`: numerical value/range stated in the text.
- `model_from_paper`: equation/model structure stated in the paper.
- `qualitative`: a direction/trend reported without a numerical value.
- `synthetic_assumption`: an explicit modelling choice required because the raw measurement is absent.

## Important scientific limitations

1. The six PDFs do not provide the original raw diagnostic arrays.
2. Where a raw signal is absent, the reconstruction is non-unique.
3. Noise, sampling, channel response, calibration details and hidden preprocessing cannot generally be recovered exactly from a publication figure.
4. A successful numerical match to a reported quantity demonstrates that the published constraints can be encoded into a reproducible workflow; it does **not** demonstrate recovery of the original shot.
5. P06 contains an internal timing inconsistency: the paper reports discharge time <35 ms while Fig. 5 includes a 45–46 ms analysis window. The reconstruction preserves both reported facts rather than silently resolving the discrepancy.

## Figure digitization policy

The first reconstruction pass prioritizes tables and explicitly reported numbers because they provide auditable numerical constraints. Figure-only quantities are used as qualitative or model constraints unless they can be calibrated and digitized independently. A figure-derived value is never promoted to an exact experimental value without a documented pixel-to-axis calibration and uncertainty estimate.

## Relationship to the 12-section repository

The repository as a whole now provides the full chain from data model/preprocessing through signal processing, magnetic diagnostics, spectroscopy, electrostatic diagnostics, turbulence/transport, HXR, cross-diagnostic analysis, validation notebooks, tests, and release/traceability documentation. Each publication notebook exercises the diagnostic workflows relevant to that paper; the repository-level test and audit layers provide the shared validation/reproducibility layer.

## What this demonstrates

The resulting artifact is stronger than a generic synthetic-data demonstration because the synthetic measurements are constrained by the user's own peer-reviewed experimental publications. It demonstrates the ability to translate published diagnostic methodology and reported quantitative constraints into reproducible computational workflows, while keeping the distinction between historical experimental evidence and newly generated synthetic data explicit.

## RC4.2 deep reconstruction layer

RC4 adds a second layer above the initial constraint generators:

- **P01:** synthetic CCD-like spectra with explicit background/noise, Gaussian fitting, instrumental-broadening correction, Doppler-temperature recovery, and Monte-Carlo uncertainty.
- **P02:** explicit 12-channel spatial Fourier mode identification; SVD component number is not used as a proxy for physical mode number. HXR count/mean/total-energy constraints are converted into a mean-constrained synthetic spectrum, and an HXR↔m=3 magnetic summary is reported without causal interpretation.
- **P03:** collector-current ratio → Mach reconstruction with bootstrap sensitivity.
- **P04:** synthetic potential → E-field → E×B velocity → turbulent particle-flux chain, with pressure-dependent transport values retained as explicit calibration constraints.
- **P05:** limiter position and bias alter synthetic field amplitudes; reported numerical percentage effects are reproduced as transparent calibration targets rather than presented as newly discovered experimental effects.
- **P06:** reconstructed 12-channel Mirnov PSD validation plus real pixel-to-axis digitization of Figure 2, with explicit uncertainty and provenance.

## Master audit

`notebooks/publication_reconstruction/00_six_paper_reconstruction_audit.ipynb` and `audit/RC4_MASTER_AUDIT.md` provide the central paper-by-paper audit. The audit reports numerical comparisons where they are scientifically meaningful and states limitations where a comparison would otherwise imply false precision.
