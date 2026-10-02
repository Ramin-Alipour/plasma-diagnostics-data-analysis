# RC4 Release Checklist

## Scientific

- [x] Six publication constraint datasets retained
- [x] P01 full spectral reconstruction
- [x] P02 explicit 12-channel spatial mode identification
- [x] P02 HXR synthetic spectrum and cross-diagnostic summary
- [x] P03 uncertainty/sensitivity
- [x] P04 potential → E → E×B → turbulent-flux chain
- [x] P05 limiter/bias → field → transport parameterization
- [x] P06 pressure-dependent PSD reconstruction
- [x] Selective real figure digitization with calibration/uncertainty
- [x] Provenance schema and records
- [x] Six-paper master audit

## Reproducibility

- [x] Automated tests
- [x] Python compilation
- [x] Import smoke test
- [x] All 14 notebooks executed successfully
- [x] Notebook outputs checked for execution errors
- [x] Cache/temp cleanup before release archive
- [x] Archive extraction test
- [x] SHA-256 checksum
- [x] Isolated virtual-environment test using the audited dependency set

## Boundary checks

- [x] Synthetic data never described as recovered raw data
- [x] Figure-derived values labelled as digitized
- [x] Post-2018 confidential/client datasets not fabricated or included
- [x] P06 timing inconsistency preserved and documented
- [x] No physical mode is inferred from SVD component number alone
- [x] Cross-diagnostic comparisons explicitly avoid causal claims
