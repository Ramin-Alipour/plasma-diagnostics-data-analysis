# 1.3% Relative-Noise Benchmark

Run from the repository root:

```bash
python scripts/generate_reference_noise.py
```

The default output directory is `data/synthetic_noise_1p3/`. A fixed seed makes
the generated files repeatable. Override the seed or output path with
`--seed` and `--output-dir`.

For each selected nonzero reference value \(x\), the generator applies

\[
x_{\mathrm{syn}} = x + \epsilon, \qquad
\epsilon \sim \mathcal{N}(0, (0.013|x|)^2).
\]

Thus 1.3% is the **relative noise standard deviation**, not a guaranteed
pointwise error bound and not a claim about the uncertainty of the original
measurements. Exact zeros are preserved because this relative model gives zero
standard deviation at zero. If a zero represents a measurement floor or a
physical null with nonzero uncertainty, a separate absolute-noise model must be
specified and justified before perturbing it.

The generator only perturbs explicitly listed observable/outcome columns. It
does not perturb identifiers, time boundaries, or setup parameters. Each output
contains provenance fields and `noise_manifest.csv` records counts and seeds.
The files are synthetic perturbations of published numerical constraints, not
original IR-T1 raw diagnostic arrays and not independent physical validation.

## Coverage limitation

P01, P02, P03, P04, and P06 have selected numeric fields that can be perturbed
from their current constraint tables. P03 is restricted to reported outcome
quantities; geometry and model parameters are not perturbed. P05's current
constraint table encodes mostly qualitative directional effects rather than
numeric point values, so the script deliberately does not invent a numerical
reference dataset for P05. P05 needs a separate controlled synthetic signal
generator based on documented qualitative effects; it must be labelled as
model-generated synthetic data, not as 1.3%-perturbed published data.
