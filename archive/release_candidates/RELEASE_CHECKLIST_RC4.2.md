# RC4.2 Release Checklist

## Scientific audit
- [x] P01–P06 evidence classes documented.
- [x] Published/directly extracted values separated from reconstructed and synthetic quantities.
- [x] P04 identical-pressure intermediate-trace issue corrected.
- [x] P06 timing inconsistency retained explicitly rather than silently corrected.
- [x] No causal HXR↔MHD claim introduced by the reconstruction layer.

## Scientific continuity
- [x] 2006–2013 foundation documented as historical/professional context.
- [x] 2013–2017 IR-T1 experimental period explicitly mapped to diagnostics.
- [x] 2017–2018 independent-research period explicitly separated.
- [x] 2018–2026 scientific/technical continuity documented without inventing public client artifacts.
- [x] 2026 publication-grounded computational layer linked to executable artifacts.

## Reproducibility
- [x] 14/14 unique notebooks execute.
- [x] Notebook imports work without manually setting `PYTHONPATH`.
- [x] No notebook execution errors.
- [x] 96 automated tests pass.
- [x] Python compilation/import checks pass.
- [x] Provenance count verified at 55 records.
- [x] Master audit is deterministic across repeated runs.
- [x] Archive is checked for duplicate/absolute paths and generated cache artifacts.

## Release metadata
- [x] `CITATION.cff` version = `0.1.0-rc4.2`.
- [x] `CHANGELOG.md` contains RC4.2 entry.
- [x] RC4.2 release notes included.
- [x] Scientific audit matrix included.
- [x] Final archive checksum generated after all edits and cleanup.
