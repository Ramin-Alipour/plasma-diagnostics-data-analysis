"""Experimental-condition metadata kept separate from signal arrays."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ExperimentalCondition:
    """Describe the experimental condition associated with an analysis result."""
    values: dict[str, Any] = field(default_factory=dict)
    label: str = ""


def compare_with_conditions(results, conditions):
    """Pair arbitrary analysis-result objects with explicit condition metadata.

    No numerical aggregation or ordering is imposed; this helper preserves the
    association between a result and its experimental condition.
    """
    if len(results) != len(conditions):
        raise ValueError("results and conditions must have equal length")
    return [{"result": r, "condition": c} for r, c in zip(results, conditions)]
