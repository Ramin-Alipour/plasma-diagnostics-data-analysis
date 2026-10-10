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

The public v0.1.1 release had a path rooted at the repository root (`ROOT / "data" / "publication_reconstruction"`) and did not package reconstruction CSV files. The candidate patch fixes this source-tree-versus-wheel defect; the fix has now passed the clean installed-wheel full suite and the selected notebook-execution job, but remains unreleased.

The candidate patch addresses this by:
1. placing the seven reconstruction constraint CSVs under `publication_reconstruction/data/publication_reconstruction/`;
2. placing the P06 digitization summary under `publication_reconstruction/data/publication_digitization/`;
3. changing the reconstruction path to package-relative data;
4. declaring both CSV groups as package data in `pyproject.toml`;
5. adding tests that assert the package data files exist.

A Library checklist reports 98 passing tests and an earlier wheel build using `--no-build-isolation`. Separately, [GitHub Actions source-checkout CI for candidate commit `d182f97331dd04bc9acbfbb83467ab56ee31d613`](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38089376235) completed successfully on Python 3.11, 3.12, and 3.13, including tests, compilation, and import smoke tests. The earlier [packaging CI job](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38089994264) passed the build, clean installation, six reconstruction tests, and package-data checks. The updated [installed-wheel CI job](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38090406973) then built the source distribution and wheel with build isolation enabled, installed the wheel in a clean virtual environment outside the source checkout, and passed the complete test suite: **98 passed in 5.45 seconds**. It also confirmed that all seven reconstruction constraint tables were present and readable. The source-checkout CI matrix passed on Python 3.11, 3.12, and 3.13. After identifying legacy repository-root data paths in three reconstruction notebooks, those notebooks were updated to use package-relative data access. A new `notebook-smoke-test` CI job executed the six-paper audit notebook and the P01 and P06 reconstruction notebooks in a fresh Python 3.12 environment and passed (CI run [38090707281](https://github.com/Ramin-Alipour/plasma-diagnostics-data-analysis/actions/runs/38090707281)). All five jobs in that run passed: source-checkout tests on Python 3.11/3.12/3.13, installed-wheel test, and notebook execution.

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
5. **Citation audit:** verify all six source references, author order, page/article numbers, and DOI resolution before submission. The Springer publisher pages confirm the title, author order, volume/article number, and DOI for references [4] and [5]. The indexed PubMed record confirms reference [3]'s title, authors, journal, volume, article number, and DOI. Accessible indexed records also corroborate the title, authors, journal details, and DOI for [1] and [2], and the Springer publisher page confirms reference [6]. Before submission, complete a final DOI-resolution and publisher-metadata pass for all six entries; direct publisher records for [1]–[3] were not all retrievable during this check.
6. **Journal template:** the current Markdown draft is approximately 1,800 words when excluding title/author information, metadata table, and references; the abstract is approximately 171 words, with six keywords and two editable SVG figures. These are preliminary counts and must be checked again after transfer into the current official SoftwareX Original Software Publication template. Keep the main text within the official 3,000-word limit (including abstract and captions, excluding references and metadata tables) and no more than six figures.
7. **Required declarations:** confirm the current template fields for CRediT authorship contributions, competing interests, funding, and data availability.
8. **Figure sources:** verify that the final editable figures and captions are included in the manuscript package and that all content is original or appropriately attributed.

## Release checklist (do not mark complete until evidenced)

- [ ] Decide and publish a new version (proposed v0.1.2 only if that is the intended version).
- [ ] Ensure the tag and source archive contain the package-data fix.
- [x] Build wheel and source distribution in a clean environment with build isolation enabled (CI run 38089994264).
- [x] Install the wheel into a fresh virtual environment outside the source checkout (CI run 38089994264).
- [x] Run the full test suite against the installed artifact (98 passed; CI run 38090406973).
- [x] Confirm the clean-environment notebook CI job passes for the six-paper audit and P01/P06 reconstruction notebooks (Python 3.12; CI run 38090707281).
- [x] Check package-data access from the installed wheel; all seven reconstruction constraint tables were readable (CI run 38089994264).
- [ ] Create a version-specific Zenodo archive and verify its DOI resolves to the exact tagged artifact.
- [ ] Update `CITATION.cff`, README release metadata, and manuscript metadata only after publication.
- [ ] Complete the final DOI-resolution and publisher-metadata pass for all six references; references [4]–[6] have publisher/index confirmation, while direct publisher confirmation remains incomplete for [1]–[3].
- [ ] Confirm official SoftwareX template and word count.
- [ ] Finalize figures, cover letter, highlights, and declarations.
- [ ] Ask an independent researcher to install and run one example; record their feedback.

## Recommendation

Proceed with SoftwareX as the target, but treat the corrected software release and clean installed-artifact test as the first hard gate. Do not submit while the manuscript refers to a candidate version that is not public and permanently archived.
