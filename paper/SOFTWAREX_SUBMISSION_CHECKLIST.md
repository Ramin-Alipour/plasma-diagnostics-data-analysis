# SoftwareX submission checklist — v0.2.2

## Fixed software reference

- [x] GitHub release: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/releases/tag/v0.2.2
- [x] Version-specific Zenodo DOI: https://doi.org/10.5281/zenodo.23300661
- [x] Release source commit: 5fa9b58b43b3461135404ef84db7bd434a31e5c4
- [x] CI on the release commit: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38174480297
- [x] Release packaging workflow: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38174480392
- [x] GitHub and Zenodo release assets manually checked by the author; keep v0.2.2 immutable during manuscript edits.

## Dataset and claims audit

- [x] Dataset A is described as supplied laboratory/device-software records; source values are not described as paper transcriptions by default.
- [x] Dataset B is described as values transcribed, digitized, or reconstructed from six publications.
- [x] Synthetic data are a third category; the 1.3% relative-noise convention applies only to the synthetic layer.
- [x] P01 synthetic CCD-like spectrum is identified as a software-test scaffold, not the experimental dataset.
- [x] P02 numerical overlap between the two modal tables is preserved and not presented as independent validation.
- [x] P04 Dataset A/B radial-transport discrepancy is reported with both source values, without modifying Dataset A.
- [x] E06 is not treated as a time-domain waveform; no PSD claim is made without sampling metadata.
- [x] P06 figure digitization is labelled approximate and carries documented uncertainty.
- [x] No claim of independent experimental validation, recovered raw shots, post-2018 IR-T1 experiments, external adoption, or measured time savings.

## Manuscript and required submission materials

- [x] Manuscript has five numbered main sections and a SoftwareX-style code metadata table.
- [x] Abstract is below 250 words.
- [x] Seven keywords or fewer.
- [x] Separate highlights file contains four bullets, each no longer than 85 characters.
- [x] References [1]–[6] are cited in the text.
- [x] CRediT, competing-interest, and data-availability statements are included.
- [x] Funding and generative-AI disclosure sections are present as drafts; funding and final declaration text still require author confirmation.
- [ ] Move final content into the current official SoftwareX original-software-publication Word or LaTeX template; preserve its layout and add line numbers.
- [ ] Generate and inspect the final editable DOCX or LaTeX/PDF package from that official template.
- [ ] Author must confirm the funding statement, acknowledgements, and competing-interest declaration before submission.
- [ ] Final reference/DOI proofread and submission-system metadata check.

## Do not do

- Do not rewrite or force-update the v0.2.2 tag while preparing the paper.
- Do not change Dataset A or Dataset B merely to eliminate a numerical difference.
- Do not report synthetic-vs-publication agreement as independent experimental validation.
- Do not use the concept DOI as a substitute for the version-specific DOI when citing v0.2.2.
