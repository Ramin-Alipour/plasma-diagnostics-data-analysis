# Paired publication-reference and synthetic datasets

This utility creates two linked tables from `plasma_provenance/records.json`.

- **Dataset A — publication-reference values:** numeric values recorded in the provenance register, with paper ID, table/figure locator, quantity, units, and extraction method. The 0.1% value is an extraction-precision target, not a guaranteed measurement uncertainty.
- **Dataset B — synthetic 1.3% Gaussian perturbations:** one paired row per numeric Dataset A row. For non-zero reference value \(x_i\), the generator uses \(x_i^{(B)}=x_i(1+\epsilon_i)\), where \(\epsilon_i\sim\mathcal{N}(0,0.013^2)\). Exact zero references remain zero because relative noise is undefined at zero; this exception is marked in each row.
- The random seed is stored so the synthetic values can be regenerated.

## Run

```bash
python -m publication_reconstruction.dataset_pair \
  --provenance plasma_provenance/records.json \
  --output-dir data/paired_publication_reconstruction \
  --seed 20261011
```

Outputs:

- `dataset_A_publication_reference_values.csv`
- `dataset_B_synthetic_1p3pct.csv`
- `dataset_pair_metadata.json`

## Interpretation boundary

Dataset A is a traceable publication-derived reference table. Digitizing a published graph to 0.1% numerical resolution does not establish 0.1% accuracy relative to the underlying measurement. Publication-derived values also do not, by themselves, verify original instrument-recorded files. Dataset B is synthetic by construction and must not be described as an independent experimental measurement. The pair supports software testing, sensitivity analysis, and reproducibility checks; it does not independently validate the original experiments.
