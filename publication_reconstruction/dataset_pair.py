"""Create paired publication-reference and synthetic-noise CSV datasets.

Dataset A stores numeric values transcribed from the project's publication-provenance
records. Dataset B applies independent Gaussian relative noise (sigma = 1.3%) to
non-zero numeric values. Exact zero references remain zero and are explicitly flagged.

Important: this utility cannot recover or certify original instrument files. Values
transcribed from papers must not be represented as verified instrument-recorded raw
measurements unless independently supported by the original acquisition records.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

NOISE_SIGMA_RELATIVE = 0.013
EXTRACTION_PRECISION_TARGET_PCT = 0.1


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("records", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    raise ValueError("Expected a JSON list of provenance records.")


def _numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and np.isfinite(value)


def build_dataset_pair(
    provenance_json: str | Path,
    output_dir: str | Path,
    *,
    seed: int = 20261011,
    sigma_relative: float = NOISE_SIGMA_RELATIVE,
) -> tuple[Path, Path, dict[str, int]]:
    """Write Dataset A and its paired Dataset B, returning paths and row counts."""
    if not np.isfinite(sigma_relative) or sigma_relative < 0:
        raise ValueError("sigma_relative must be a finite non-negative number.")

    source_path = Path(provenance_json)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    rows = _records(payload)
    rng = np.random.default_rng(seed)

    dataset_a: list[dict[str, Any]] = []
    dataset_b: list[dict[str, Any]] = []
    skipped_non_numeric = 0
    zero_count = 0

    for row in rows:
        value = row.get("reported_value")
        if not _numeric(value):
            skipped_non_numeric += 1
            continue

        record_id = str(row.get("record_id", f"record-{len(dataset_a) + 1:04d}"))
        base = {
            "record_id": record_id,
            "source_paper": row.get("source_paper", ""),
            "source_locator": row.get("source_locator", ""),
            "quantity": row.get("quantity", ""),
            "reference_value": float(value),
            "unit": row.get("unit", "") or "",
            "source_type": row.get("source_type", ""),
            "extraction_method": row.get("extraction_method", ""),
            "reconstruction_method": row.get("reconstruction_method", ""),
            "extraction_precision_target_pct": EXTRACTION_PRECISION_TARGET_PCT,
            "provenance_class": "publication-derived reference value",
        }
        dataset_a.append(base.copy())

        if float(value) == 0.0:
            synthetic_value = 0.0
            noise_value = 0.0
            handling = "zero reference preserved; no relative noise applied"
            zero_count += 1
        else:
            noise_value = float(rng.normal(loc=0.0, scale=sigma_relative))
            synthetic_value = float(value) * (1.0 + noise_value)
            handling = "multiplicative Gaussian relative noise"

        dataset_b.append({
            **base,
            "reference_value": float(value),
            "synthetic_value": synthetic_value,
            "relative_noise_realization": noise_value,
            "relative_noise_sigma": sigma_relative,
            "relative_noise_sigma_pct": 100.0 * sigma_relative,
            "zero_handling": handling,
            "provenance_class": "synthetic perturbation of publication-derived reference value",
            "random_seed": seed,
        })

    a_path = out / "dataset_A_publication_reference_values.csv"
    b_path = out / "dataset_B_synthetic_1p3pct.csv"
    _write_csv(a_path, dataset_a)
    _write_csv(b_path, dataset_b)

    metadata = {
        "input_provenance_records": len(rows),
        "numeric_reference_records_written": len(dataset_a),
        "non_numeric_records_skipped": skipped_non_numeric,
        "zero_reference_values": zero_count,
        "synthetic_records_written": len(dataset_b),
        "random_seed": seed,
    }
    (out / "dataset_pair_metadata.json").write_text(
        json.dumps({
            **metadata,
            "dataset_A": a_path.name,
            "dataset_B": b_path.name,
            "relative_noise_distribution": "Gaussian",
            "relative_noise_sigma": sigma_relative,
            "relative_noise_sigma_pct": 100.0 * sigma_relative,
            "extraction_precision_target_pct": EXTRACTION_PRECISION_TARGET_PCT,
            "note": (
                "Dataset A contains publication-derived numeric reference values; it is not "
                "automatically equivalent to original instrument-recorded raw data. Dataset B "
                "is synthetic and is generated by perturbing Dataset A."
            ),
        }, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return a_path, b_path, metadata


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provenance", default="plasma_provenance/records.json")
    parser.add_argument("--output-dir", default="data/paired_publication_reconstruction")
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--sigma-relative", type=float, default=NOISE_SIGMA_RELATIVE)
    args = parser.parse_args()
    a_path, b_path, counts = build_dataset_pair(
        args.provenance, args.output_dir, seed=args.seed, sigma_relative=args.sigma_relative
    )
    print(f"Dataset A: {a_path}")
    print(f"Dataset B: {b_path}")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
