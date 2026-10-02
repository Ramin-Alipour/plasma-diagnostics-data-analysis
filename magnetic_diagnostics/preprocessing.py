"""Magnetic preprocessing orchestration.

Common preprocessing operations are implemented in ``plasma_core.signal_processing``;
this module intentionally re-exports them rather than duplicating code.
"""
from plasma_core.signal_processing import apply_filter, detrend_signal, normalize_signal, remove_offset

__all__ = ["apply_filter", "detrend_signal", "normalize_signal", "remove_offset"]
