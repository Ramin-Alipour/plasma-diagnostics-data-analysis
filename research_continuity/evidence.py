from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class EvidenceItem:
    capability: str
    experimental_evidence: str
    computational_evidence: str
    repository_evidence: str
    evidence_type: str
    limitation: str

def default_evidence_map() -> list[EvidenceItem]:
    return [
        EvidenceItem("Doppler spectroscopy","IR-T1 spectroscopy work","Python/MATLAB spectral analysis","P01; spectroscopy/","documented experimental + computational","P01 is publication-grounded reconstruction; no raw IR-T1 data are distributed."),
        EvidenceItem("Hard X-ray diagnostics","IR-T1 HXR measurements","count/energy analysis; spectrum features","P02; hard_xray/","documented experimental + computational","Synthetic spectrum is mean/count constrained, not detector-response reconstruction."),
        EvidenceItem("Mirnov/MHD diagnostics","IR-T1 magnetic-fluctuation measurements","PSD, SVD, spatial Fourier mode analysis, wavelet tools","P02/P06; magnetic_diagnostics/","documented experimental + computational","Reconstructed signals are synthetic; mode identification is performed on the synthetic multichannel data."),
        EvidenceItem("Electrostatic probes","IR-T1 Langmuir/compound-probe work","I-V, E-field, flow/Mach, fluctuation analysis","P03/P04; electrostatic_diagnostics/","documented experimental + computational","Synthetic transfer model is not a recovered probe calibration."),
        EvidenceItem("Turbulent transport","IR-T1 transport publications","E×B, Reynolds stress, turbulent flux workflows","P04/P05; turbulence_transport/","documented publication-grounded computational work","Synthetic inputs are constrained by reported values/effects."),
        EvidenceItem("Signal processing","Experimental diagnostics + independent technical analysis","filtering, FFT/PSD, SVD, wavelet, correlation, time-series analysis","plasma_core/signal_processing/; tests/","methodological + computational","Client-specific datasets are not public."),
        EvidenceItem("Quantitative scientific analysis","Experimental plasma research + independent scientific/technical work","Python/MATLAB-oriented workflows and validation","multiple packages; tests/","professional-history + computational evidence","Post-2018 project-specific datasets are not included."),
        EvidenceItem("Reproducible analysis","Current computational work","tests, notebooks, provenance, deterministic seeds, audit","tests/; notebooks/; plasma_provenance/; audit/","computational evidence","Reproducibility applies to the supplied/reconstructed datasets and documented assumptions."),
    ]
