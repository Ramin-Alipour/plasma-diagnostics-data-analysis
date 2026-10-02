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
- P04: synthetic potential → E-field → E×B velocity → turbulent particle flux.
- P05: limiter position/bias → field-amplitude parameterization → transport/Reynolds-stress effects.
- P06: 12-channel Mirnov → PSD plus separately calibrated Figure 2 digitization.

The intended evidence chain is:

`published result → extracted constraints → reconstructed synthetic measurement → repository workflow → reconstructed observable → uncertainty → publication comparison`

The reconstruction functions deliberately do **not** claim recovery of the original experimental data.
