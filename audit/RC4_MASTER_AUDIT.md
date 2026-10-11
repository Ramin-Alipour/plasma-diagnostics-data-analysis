# RC4.3 Master Reconstruction Audit

P01 scientific reporting is based on the author-supplied laboratory measurements. The legacy synthetic-spectrum comparison is withdrawn and is not an experimental result. This audit does not rank the six papers or assign an overall score.

## Summary

| Paper | Input | Reconstruction | Observable | Reported | Reconstructed | Metric | Value | Status |
|---|---|---|---|---|---|---|---:|---|
| P01 | author-supplied laboratory measurements | author-supplied experimental-data workflow | ion temperature | author-supplied values | not replaced by synthetic output | reporting status | author-data basis | AUTHOR DATA BASIS |
| P02 | Tables 1-2 | 12-channel spatial Fourier modes + HXR spectrum + aligned summary | m=3 fraction / HXR energy | 89.10755 | 88.96495 | mean abs m=3 error percentage points | 0.14627 | PASS |
| P03 | probe geometry + reported constraints | synthetic collector currents → current ratio → Mach | Mach | not numerically reported | 0.454929 | bootstrap uncertainty | 0.002349 | PASS |
| P04 | text-level constraints + separate approximate Dataset B values | potential → E → E×B → transport statistics | radial/poloidal transport proxies | text constraints; see details | calibrated to text constraints | calibration consistency check | executed | CONSISTENCY CHECK |
| P05 | limiter position + bias | parameterized E-field → E×B → transport observables | reported percentage effects | -50/-35% radial; -15/-5% Reynolds stress | -50/-35% radial; -15/-5% Reynolds stress | maximum absolute difference from encoded target, percentage points | 1.42e-14 | CONSISTENCY CHECK |
| P06 | pressure + Table 1/Figs 4-5 | 12-channel Mirnov → PSD | dominant frequency | mean of approximate pressure-specific estimates: 44.307 kHz | 44.010 kHz | mean absolute difference from approximate estimates | 0.628 kHz | CONSISTENCY CHECK |

## P01: author-supplied experimental-data basis

The lead author confirms that P01 laboratory measurements supplied to this project are real experimental data. Some publication values were intentionally reported approximately or differently to protect sensitive diagnostic know-how. The legacy synthetic CCD-like spectrum was a software-development scaffold, not the experimental dataset. Its comparison against publication-derived values is withdrawn from scientific reporting; no synthetic-spectrum discrepancy is a reportable P01 result.



The experimental analysis is based on real laboratory measurements supplied by the lead author. Some publication values were intentionally reported approximately or differently to protect sensitive diagnostic know-how. The legacy synthetic-spectrum and publication-table comparisons are withdrawn from scientific reporting; they are not reportable experimental discrepancies. P01 scientific results must be based on the author-supplied laboratory measurements.

## Scientific boundaries

- Synthetic reconstructions are never represented as recovered raw IR-T1 measurements.
- P01's two modes answer different questions: table reproduction and application of the printed equation. The table mode is not independent validation.
- P02 uses explicit spatial Fourier construction; SVD component number is not a proxy for physical mode number.
- P03 Mach is model-constrained; original raw collector-current series unavailable.
- P04 text-level constraints are separate from approximate Dataset B values.
- P05 numerical effects are parameterization targets where explicitly reported.
- P06 synthetic Mirnov traces use text-level approximately 44 kHz activity; pressure-specific frequencies and figure digitization remain approximate.

## Release interpretation

RC4.3 remains a release candidate, not completed scientific validation. Dataset A, Dataset B, and synthetic data remain separate evidence classes.
