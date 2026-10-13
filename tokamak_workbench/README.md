# Tokamak Workbench — new analysis layer

This package is added alongside the existing Plasma Diagnostics Data Analysis software. The legacy modules and six IR-T1 publication-reconstruction workflows are preserved, not overwritten.

## Run the desktop shell

After installing the project in a Python 3.11+ environment, launch the new interface with `tokamak-workbench` or `python -m tokamak_workbench.app`. Tkinter must be available in the Python installation.

## Initial implementation

- Structured catalog based on the uploaded 24-page Persian tokamak.pdf and the existing six IR-T1 publication workflows.
- Catalog entries distinguish measured signals, derived observables and model-inferred quantities; each includes methods, formula/principle, required inputs and limitations.
- CSV, TSV, TXT and Excel import plus missing-value/duplicate/numeric summaries.
- Executable routines for Doppler ion temperature, Doppler line-of-sight velocity, electric-field gradients, E×B drift, beta, energy confinement time, Debye length, electron plasma frequency, Greenwald density, Welch PSD, normalized cross-correlation and SVD.

## Scientific safeguards

A catalog entry does not mean every tokamak has that diagnostic, nor that every listed method is implemented. Correct calibration, units, detector response, geometry, timing, atomic data and model assumptions remain necessary. Interferometry measures line-integrated density; absolute impurity density requires calibrated emissivity and atomic data; surface heat flux usually requires an inverse thermal model; and tau_E requires a consistently defined net loss power.

This is the first code layer, not a claim that every diagnostic algorithm in the literature is already implemented or validated. Existing software and six-paper provenance records remain intact.
