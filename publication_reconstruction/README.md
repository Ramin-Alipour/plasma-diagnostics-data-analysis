# Publication-grounded reconstruction

This directory contains deterministic synthetic/model-constrained reconstructions grounded in six peer-reviewed IR-T1 publications.

**Important:** these are not recovered original raw measurements. Each dataset is tagged by provenance and by the strength of the constraint:

- `exact_table`: directly reported numerical table values.
- `exact_reported`: directly reported numerical result/range.
- `model_from_paper`: equation/model structure reported by the paper.
- `qualitative`: reported direction/trend without a numerical value.
- `synthetic_assumption`: an explicit assumption needed because raw data are absent.
- `digitized_from_published_figure`: quantitative information extracted from a calibrated published figure rendering, with explicit uncertainty.

## RC4.2 deep reconstruction

The initial generators remain available in `reconstruct.py`. `advanced.py` adds deeper measurement-to-observable chains:

- P01: synthetic CCD-like spectrum → Gaussian fit → instrumental correction → Doppler temperature → Monte-Carlo uncertainty.
- P02: 12-channel spatial Fourier mode identification + HXR mean/count-constrained spectrum + non-causal cross-diagnostic summary.
- P03: synthetic compound-probe currents → Mach number + bootstrap uncertainty.
- P04: synthetic potential → E-field → E×B velocity → turbulent particle flux. The absolute P04 transport entries in Dataset B are approximate reconstructions, not exact table transcriptions. The basic synthetic generator uses them as amplitude-scale constraints; the advanced physics chain instead uses the separately documented text-level transport targets.
- P05: limiter position/bias → field-amplitude parameterization → transport/Reynolds-stress effects.
- P06: 12-channel Mirnov → PSD plus separately calibrated Figure 2 digitization. The synthetic signals use the text-level approximately 44 kHz activity; pressure-specific frequency entries in the constraint CSV are approximate figure/text reconstructions, not exact table values. Canonical Dataset B peak estimates and the retained legacy processing snapshot intentionally remain distinct.

The intended evidence chain is:

`published result → extracted constraints → reconstructed synthetic measurement → repository workflow → reconstructed observable → uncertainty → publication comparison`

The reconstruction functions deliberately do **not** claim recovery of the original experimental data.


## Relative-noise model

The core synthetic measurement arrays from `reconstruct_paper1` through
`reconstruct_paper6` use the shared relative Gaussian-noise model by default:
for nonzero reference values, `sigma = 0.013 * abs(reference)`; zero-valued
references remain zero. The `relative_noise_std` parameter allows a caller to
change or disable this model. Dataset A and Dataset B are never modified by
these generators. P02 HXR event-energy sampling and the P05 parameterized
target-effect summary retain their separately documented model roles.

## P01 data basis and reporting boundary

P01 experimental interpretation is based on the real laboratory measurements supplied by the lead author. Publication-derived values remain separate because some were intentionally reported approximately/differently to protect sensitive diagnostic know-how. The legacy synthetic CCD-like spectrum is a software test scaffold only; its comparison with publication values is withdrawn from scientific reporting and is not a reportable experimental discrepancy. Synthetic reconstruction functions may remain available for regression tests, but their outputs must not be presented as P01 experimental results.
