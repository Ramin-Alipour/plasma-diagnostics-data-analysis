# Provenance and synthetic-noise protocol

## Dataset classes

1. **Published numerical values**: values transcribed from article tables/text; not raw diagnostic arrays.
2. **Digitized-from-figure values**: estimates extracted from calibrated pixels; retain figure/page, axis calibration and uncertainty.
3. **Reconstructed/model-derived values**: calculations from published constraints and explicit assumptions.
4. **Synthetic test values**: generated computationally for robustness tests; not IR-T1 observations.

Do not relabel categories 1–3 as original raw measurements. Raw data require actual original measurement files and acquisition provenance.

## Relative Gaussian noise

`publication_reconstruction.noise_model.add_relative_gaussian_noise` generates a separate synthetic array. For nonzero reference x, noise standard deviation is sigma_noise(x) = 0.013 * abs(x).

Thus 1.3% is the relative standard deviation, not a bound on each sample and not a claim about the source data measurement uncertainty.

- Default `zero_policy="preserve"` keeps exact zero entries unchanged.
- `zero_policy="scale"` requires a positive `zero_scale` in the same physical units. Noise standard deviation at zero is 1.3% of that declared scale; document the scale and rationale.
- Use a fixed seed for reproducibility, but do not treat one realization as statistical validation.

## The proposed 0.1% target

A 0.1% extraction target is not automatic for values transcribed from papers. Assess source resolution, axis calibration, line thickness, rounding and significant figures. Record estimated uncertainty per digitized quantity. If the evidence cannot support 0.1%, report the limitation rather than adding digits or describing synthetic values as raw.

## Suggested manuscript wording

> Reference datasets comprise numerical constraints transcribed from published tables and text, selected values digitized from published figures, and explicitly identified model-derived quantities. Separate synthetic datasets are generated for software robustness tests using Gaussian perturbations with a relative standard deviation of 1.3% for nonzero reference values. These synthetic datasets are not original IR-T1 measurements. Software tests assess computational behavior and reproducibility; they do not independently validate the underlying experimental results.

For every generated dataset, record source paper, table/figure, transformation, units, assumptions, seed and zero policy.
