"""General cross-diagnostic comparison workflows."""
from .alignment import align_time_series, interpolate_to_time, resample_time_series
from .comparison import correlation_coefficient, cross_correlation, spectral_comparison
from .metadata import ExperimentalCondition, compare_with_conditions

__all__ = [
    "align_time_series", "interpolate_to_time", "resample_time_series",
    "correlation_coefficient", "cross_correlation", "spectral_comparison",
    "ExperimentalCondition", "compare_with_conditions",
]
