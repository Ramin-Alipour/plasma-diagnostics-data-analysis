from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any
import json
from pathlib import Path

@dataclass
class ProvenanceRecord:
    record_id: str
    source_paper: str
    source_locator: str
    source_type: str
    quantity: str
    reported_value: Any
    unit: str | None
    extraction_method: str
    reconstruction_method: str | None = None
    assumptions: list[str] = field(default_factory=list)
    model_assumptions: list[str] = field(default_factory=list)
    reconstructed_value: Any = None
    uncertainty: Any = None
    relative_error_pct: Any = None
    limitation: str = ""

    def to_dict(self): return asdict(self)

def save_records(records: list[ProvenanceRecord], path: str | Path) -> None:
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps([r.to_dict() for r in records], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load_records(path: str | Path) -> list[ProvenanceRecord]:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    return [ProvenanceRecord(**x) for x in data]
