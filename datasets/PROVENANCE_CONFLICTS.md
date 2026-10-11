# Dataset A / Dataset B provenance and quality-control note

**Status: source categories are distinct; some values can legitimately coincide.**

Dataset A contains the owner's supplied laboratory/device/software records. Dataset B contains values transcribed or reconstructed from the six cited IR-T1 publications. Dataset B is **not a synthetic-noise version** of Dataset A.

## E02 / P02 modal table

The 20 rows in `datasets/dataset_a/laboratory_measurements/exp2_modes.csv` coincide numerically with the values printed in Table 2 of P02, which are transcribed in `datasets/dataset_b/publication_reconstruction/paper2_modes.csv`. This overlap is consistent with the possibility that Dataset A contains the original values underlying the publication and Dataset B transcribes those same published values. It is **not evidence that either file is synthetic**, and the values must not be altered to manufacture a difference.

The two files have different provenance roles:
- Dataset A: owner-supplied laboratory/device/software record.
- Dataset B: publication transcription from P02, Table 2.
- Because the numerical content overlaps, this pair is not an independent validation dataset or an independent comparison.

The P02 table values are printed to three decimal places in the source. Preserve the published precision and values; do not round them to 0.01 or normalize modal percentages.

## E06 / P06 figure comparison

The owner has reported that `datasets/dataset_a/laboratory_signal_analysis/e06_mhd_signal.csv` came from the diagnostic's software. The file has 423 rows and columns including `x_pixel`, `y_pixel`, `frequency_kHz`, and `amplitude`; that structure does not establish that it is a raw time-domain waveform. A possible acquisition/export/processing issue is a hypothesis to investigate, not a verified explanation. Its values remain unchanged until the original export, acquisition metadata, or other traceable evidence can resolve the issue.

The separate P06 Figure 2 dataset is publication digitization. Numerical similarity alone does not prove that E06 was digitized from the paper, and the owner's source declaration alone does not provide independent acquisition-log verification. Keep this uncertainty explicit; do not calculate a time-domain PSD from E06 as currently structured.

## Required extraction and reporting rules

- Re-extract Dataset B from the cited papers and preserve the precision printed in tables.
- For figure-derived values, document the figure, axes calibration, digitization method, and uncertainty. A displayed value with two decimal places is not automatically accurate to ±0.01; only claim that accuracy where the source resolution and calibration support it.
- Current P04 absolute E-field/transport entries and P06 pressure-specific frequency/timing entries are labelled approximate in the data files. They are not verified to 0.01 accuracy and must not be described as exact extractions until re-digitized and checked.
- Do not add synthetic noise to Dataset B, alter source values to force agreement, or treat overlapping Dataset A/B values as independent experimental validation.
- This note records the owner's source declaration and the present file-level audit; it does not claim independent access to the diagnostic software or acquisition logs.
