# P01 reconciliation

The CSV ledger records value-based correspondence between Dataset A laboratory/device-side spectroscopy rows and Dataset B publication-derived rows.

- All 15 rows match on normalized ion, wavelength, and measured FWHM fields.
- A field match does not establish shared raw-data provenance.
- The reconciled-value field remains blank; no numeric correction or hidden transformation is applied.
- Dataset A and Dataset B remain separate and unchanged.
- The 158.09% quadrature-model result remains a conditional sensitivity result. It is not hidden and is not automatically classified as an experimental error.
- Any future numeric mapping must document its method, source, and rationale.
