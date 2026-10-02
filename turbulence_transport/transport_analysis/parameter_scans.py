"""Controlled synthetic parameter-scan models for turbulence demonstrations."""
from __future__ import annotations
import numpy as np


def parameter_scan(parameter_values, parameter_name, *, baseline_response=1.0, sensitivity=0.15, reference_value=None):
    """Generate a transparent synthetic response to one control parameter.

    The response is an illustrative linear sensitivity model. It is not a fit
    to the numerical results of an IR-T1 publication.
    """
    values = np.asarray(parameter_values, dtype=float)
    if values.ndim != 1 or values.size < 2 or np.any(~np.isfinite(values)):
        raise ValueError("parameter_values must be a finite one-dimensional array with at least two values")
    if not np.isfinite(baseline_response) or baseline_response <= 0:
        raise ValueError("baseline_response must be positive and finite")
    if not np.isfinite(sensitivity):
        raise ValueError("sensitivity must be finite")
    ref = float(values[0] if reference_value is None else reference_value)
    if not np.isfinite(ref):
        raise ValueError("reference_value must be finite")
    response = baseline_response * (1.0 + sensitivity * (values - ref) / max(abs(ref), np.finfo(float).eps))
    return {
        "parameter_name": str(parameter_name),
        "parameter_values": values,
        "response": response,
        "reference_value": ref,
        "baseline_response": float(baseline_response),
        "sensitivity": float(sensitivity),
        "data_type": "synthetic",
        "model": "linear_sensitivity",
    }
