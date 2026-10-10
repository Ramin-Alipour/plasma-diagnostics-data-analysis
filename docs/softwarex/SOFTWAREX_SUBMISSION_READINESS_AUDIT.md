# SoftwareX submission readiness audit — 11 October 2026

## Scope and evidence

This audit cross-checks the public GitHub repository files available through the GitHub connector and the files in the user's `/Github` Library folder. It is not a clean-room execution of the candidate ZIP and does not constitute a journal acceptance prediction.

## Current public release versus candidate

- Public repository: https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis
- Public default-branch `pyproject.toml` and `CITATION.cff` identify v0.1.1.
- Existing version DOI: https://doi.org/10.5281/zenodo.23101225 (v0.1.1).
- Library contains a proposed wheel-packaging patch and candidate ZIP; the candidate is not yet the public v0.1.2 release.
- Do not update the existing v0.1.1 DOI to point at modified source.

## Main technical finding

The current public `publication_reconstruction/reconstruct.py` uses a path rooted at the repository root (`ROOT / "data" / "publication_reconstruction"`). The public `pyproject.toml` declares package data only for `plasma_provenance`, not the reconstruction CSV files. This is a credible source-tree-versus-wheel packaging defect: data files needed by reconstruction functions may be absent from an installed wheel.

The candidate patch addresses this by:
1. placing the seven reconstruction constraint CSVs under `publication_reconstruction/data/publication_reconstruction/`;
2. placing the P06 digitization summary under `publication_reconstruction/data/publication_digitization/`;
3. changing the reconstruction path to package-relative data;
4. declaring both CSV groups as package data in `pyproject.toml`;
5. adding tests that assert the package data files exist.

A Library checklist reports 98 passing tests and an earlier wheel build using `--no-build-isolation`. Separately, [GitHub Actions source-checkout CI for candidate commit `d182f97331dd04bc9acbfbb83467ab56ee31d613`](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38089376235) completed successfully on Python 3.11, 3.12, and 3.13, including tests, compilation, and import smoke tests. The newer [packaging CI job](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38089994264) also completed successfully: it built the source distribution and wheel with build isolation enabled, installed the wheel into a clean virtual environment outside the checkout, passed all six publication-reconstruction tests, and confirmed that all seven constraint tables were present and readable. The full source-checkout CI matrix for this latest commit was still in progress at the time of this audit update, and the full test suite has not been run against the installed wheel.

## Scientific and editorial strengths

- Clear domain scope spanning spectroscopy, hard X-ray signals, magnetic fluctuations, electrostatic probes, and transport analysis.
- Six case studies linked to published IR-T1 studies.
- The documentation explicitly distinguishes published constraints, extracted values, reconstructed quantities, synthetic assumptions, and unvalidated quantities.
- MIT license, public source, citation metadata, notebooks, tests, provenance records, and two manuscript figures already exist.
- The draft avoids claiming recovery of unavailable raw IR-T1 shots or independent experimental validation.

## Major submission risks

1. **Novelty/impact evidence:** the paper must make the reusable software contribution concrete, not merely list standard algorithms. Demonstrate a real end-to-end workflow and explain what the shared provenance/reconstruction structure enables.
2. **Installed-package reproducibility:** the candidate fix must be released and tested from a clean environment. Source-tree tests alone are insufficient for this issue.
3. **Independent usability:** no independent-user installation/feedback is documented in the reviewed materials. It would materially strengthen evidence of usability.
4. **Validation framing:** results from synthetic signals and constraints encoded from the source paper are computational consistency checks, not independent validation. Avoid calling them experimental validation or exact reproduction.
5. **Citation audit:** verify all six source references, author order, page/article numbers, and DOI resolution before submission. The MHD paper [6] has now been checked against the Springer publisher page, which confirms the title, authors, volume 72, article 75 (2018), and DOI. The remaining five references still need a final publisher-record comparison before submission.
6. **Journal template:** the current Markdown draft is approximately 1,800 words when excluding title/author information, metadata table, and references; the abstract is approximately 171 words, with six keywords and two editable SVG figures. These are preliminary counts and must be checked again after transfer into the current official SoftwareX Original Software Publication template. Keep the main text within the official 3,000-word limit (including abstract and captions, excluding references and metadata tables) and no more than six figures.
7. **Required declarations:** confirm the current template fields for CRediT authorship contributions, competing interests, funding, and data availability.
8. **Figure sources:** verify that the final editable figures and captions are included in the manuscript package and that all content is original or appropriately attributed.

## Release checklist (do not mark complete until evidenced)

- [ ] Decide and publish a new version (proposed v0.1.2 only if that is the intended version).
- [ ] Ensure the tag and source archive contain the package-data fix.
- [x] Build wheel and source distribution in a clean environment with build isolation enabled (CI run 38089994264).
- [x] Install the wheel into a fresh virtual environment outside the source checkout (CI run 38089994264).
- [ ] Run package import smoke tests and the full test suite against the installed artifact.
- [ ] Execute the two flagship notebooks from a clean environment, and record environment versions.
- [x] Check package-data access from the installed wheel; all seven reconstruction constraint tables were readable (CI run 38089994264).
- [ ] Create a version-specific Zenodo archive and verify its DOI resolves to the exact tagged artifact.
- [ ] Update `CITATION.cff`, README release metadata, and manuscript metadata only after publication.
- [ ] Independently verify all six references.
- [ ] Confirm official SoftwareX template and word count.
- [ ] Finalize figures, cover letter, highlights, and declarations.
- [ ] Ask an independent researcher to install and run one example; record their feedback.

## Recommendation

Proceed with SoftwareX as the target, but treat the corrected software release and clean installed-artifact test as the first hard gate. Do not submit while the manuscript refers to a candidate version that is not public and permanently archived.
