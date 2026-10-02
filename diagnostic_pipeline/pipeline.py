from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, Any

@dataclass
class PipelineStage:
    name: str
    purpose: str
    status: str = "defined"

PIPELINE_STAGES = [
    PipelineStage("measurement_input", "raw, reconstructed, or synthetic diagnostic measurement"),
    PipelineStage("preprocessing", "validation, detrending, filtering and conditioning"),
    PipelineStage("calibration", "mapping instrument/sample coordinates to physical coordinates where applicable"),
    PipelineStage("noise_handling", "explicit noise/background treatment"),
    PipelineStage("feature_extraction", "lines, peaks, counts, modes, fluctuations or other observables"),
    PipelineStage("time_frequency_analysis", "PSD, FFT, wavelet or time-domain statistics"),
    PipelineStage("spatial_modal_analysis", "multichannel spatial decomposition or diagnostic geometry"),
    PipelineStage("physical_observable", "temperature, flow/Mach, transport, mode energy, HXR energy metric, etc."),
    PipelineStage("uncertainty", "uncertainty propagation, bootstrap or sensitivity analysis"),
    PipelineStage("validation", "comparison against known/reported constraints"),
    PipelineStage("publication_comparison", "traceable comparison to publication values or trends"),
]

def run_pipeline(data: Any, stages: list[Callable[[Any], Any]]) -> Any:
    out=data
    for stage in stages: out=stage(out)
    return out

def stage_manifest(): return [asdict(x) for x in PIPELINE_STAGES]
