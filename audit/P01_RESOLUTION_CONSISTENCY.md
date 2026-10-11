# P01 resolution analysis and data-protection provenance

## Author-confirmed data basis

The lead author confirms that the P01 laboratory measurements supplied for this project are real experimental data obtained from the author, not simulated measurements. Because the diagnostic method and measurement technique are sensitive intellectual work, some numerical values in the publication were intentionally reported approximately or differently to reduce straightforward copying. The author's supplied laboratory data are therefore the relevant experimental basis; publication-derived values are retained as a separate documentary record.

The synthetic CCD-like spectrum used during early software development was a test scaffold only. It is not a substitute for the author-supplied experimental data and must not be compared against the publication table as if it were a reconstruction of the experiment. Consequently, the prior synthetic-spectrum/equation comparison is withdrawn from scientific reporting. Its numerical difference is **not a reportable experimental discrepancy**, and must not appear as a result in the manuscript, summary tables, or conclusions.

## Handling rules

- Preserve Dataset A laboratory/device-side values byte-for-byte.
- Preserve Dataset B publication-derived values as a separate record; do not treat approximate publication values as the authoritative raw measurements.
- Use author-supplied laboratory measurements for the P01 experimental analysis.
- Synthetic spectra may be used only for clearly labelled software tests and must not be used to claim experimental agreement or disagreement.
- Do not report a discrepancy obtained by comparing synthetic test output with author-supplied experimental measurements or intentionally approximate publication values.
- Do not overwrite source data or infer undocumented numerical corrections.
- P04/P05/P06 results remain consistency checks, not independent validation.
- The 1.3% relative-noise convention applies only to explicitly synthetic datasets.

The software may retain separate `tabulated` and `equation` modes for diagnostic testing, but synthetic-mode outputs are not evidence about the actual P01 experiment and are excluded from scientific conclusions.
