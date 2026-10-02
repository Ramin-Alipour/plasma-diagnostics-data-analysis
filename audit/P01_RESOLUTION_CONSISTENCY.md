# P01 Resolution Consistency Note

## Issue

The P01 spectroscopy paper defines the total resolution broadening in quadrature. Equation (3) states that the resolution term is the quadrature sum of instrumental and diffraction broadening, and Eq. (11) gives the diffraction contribution as wavelength divided by the total ruling number. The paper also gives an instrumental broadening of 0.03704 nm for a 5 μm slit.

The repository previously carried the approximately 0.040 nm values from the paper table as the resolution term. Those tabulated values are not used as a linear sum in the reconstruction model.

## Correct implementation

For each selected P01 line:

- instrumental broadening: `Δλ_instrumental = 0.03704 nm`
- total ruling number: `N = 1.35 × 10^5`
- diffraction broadening: `Δλ_diffraction = λ / N`
- resolution: `Δλ_resolution = sqrt(Δλ_instrumental² + Δλ_diffraction²)`
- Doppler width: `Δλ_Doppler = sqrt(Δλ_measured² − Δλ_resolution²)`

The resulting resolution is approximately 0.0372 nm over the selected 410–537 nm lines.

## Scientific interpretation

Using the quadrature resolution materially increases the inferred Doppler contribution for lines whose measured FWHM is close to the instrumental width. Consequently, the reconstructed ion temperatures for several metal lines are substantially higher than the temperatures reported in Table VII. The repository does **not** alter the reported temperatures to force agreement. Instead, the difference is explicitly recorded as a consistency-check result.

The synthetic Gaussian generation remains a computational round trip: the synthetic spectrum is generated from the published measured FWHM, fitted back, and then corrected with the published resolution model. This is not independent experimental validation and does not recover the original CCD data.
