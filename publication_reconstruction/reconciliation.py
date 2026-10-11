"""Traceable P01 source correspondence without overwriting either dataset.

Dataset A contains laboratory/device-side records. Dataset B contains
publication-derived records. Matching field values are not proof that rows
share raw-data provenance and do not authorize a numerical correction.
"""
from __future__ import annotations

from pathlib import Path
import sysconfig
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SHARE_DATASETS = Path(sysconfig.get_path("data")) / "share" / "plasma-diagnostics-data-analysis" / "datasets"


def _dataset_path(relative: str) -> Path:
    source_path = ROOT / "datasets" / relative
    if source_path.is_file():
        return source_path
    installed_path = SHARE_DATASETS / relative
    if installed_path.is_file():
        return installed_path
    return source_path


DATASET_A = _dataset_path("dataset_a/laboratory_measurements/exp1_spectroscopy.csv")
DATASET_B = _dataset_path("dataset_b/publication_reconstruction/paper1_spectroscopy.csv")
LEDGER = _dataset_path("dataset_audit/p01_reconciliation.csv")
KEY_COLUMNS = ("ion", "wavelength_nm", "measured_fwhm_nm")


def _normalized_key(row):
    return (str(row["ion"]).strip(),
            round(float(row["wavelength_nm"]), 6),
            round(float(row["measured_fwhm_nm"]), 6))


def build_p01_reconciliation(dataset_a: pd.DataFrame | None = None,
                             dataset_b: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return a value-based correspondence ledger; never calculate a corrected value."""
    a = pd.read_csv(DATASET_A) if dataset_a is None else dataset_a.copy(deep=True)
    b = pd.read_csv(DATASET_B) if dataset_b is None else dataset_b.copy(deep=True)
    for label, frame in (("Dataset A", a), ("Dataset B", b)):
        missing = set(KEY_COLUMNS) - set(frame.columns)
        if missing:
            raise ValueError(f"{label} lacks required key columns: {sorted(missing)}")
    bkeys = {}
    for idx, row in b.iterrows():
        key = _normalized_key(row)
        if key in bkeys:
            raise ValueError(f"Ambiguous duplicate key in Dataset B: {key}")
        bkeys[key] = (idx, row)
    records = []
    for a_idx, row_a in a.iterrows():
        key = _normalized_key(row_a)
        hit = bkeys.get(key)
        if hit is None:
            records.append({
                "dataset_a_row_1based": int(a_idx) + 2,
                "dataset_a_experiment_id": row_a.get("experiment_id", ""),
                "ion": row_a["ion"], "wavelength_nm": row_a["wavelength_nm"],
                "dataset_a_measured_fwhm_nm": row_a["measured_fwhm_nm"],
                "dataset_b_row_1based": "", "dataset_b_measured_fwhm_nm": "",
                "dataset_b_resolution_fwhm_nm": "", "dataset_b_reported_temperature_eV": "",
                "dataset_b_calculated_temperature_eV": "",
                "reconciliation_status": "NO_MATCH",
                "reconciled_value": "",
                "rationale": "Exact normalized key match not found; no inferred reconciliation.",
            })
            continue
        b_idx, row_b = hit
        records.append({
            "dataset_a_row_1based": int(a_idx) + 2,
            "dataset_a_experiment_id": row_a.get("experiment_id", ""),
            "ion": row_a["ion"], "wavelength_nm": row_a["wavelength_nm"],
            "dataset_a_measured_fwhm_nm": row_a["measured_fwhm_nm"],
            "dataset_b_row_1based": int(b_idx) + 2,
            "dataset_b_measured_fwhm_nm": row_b["measured_fwhm_nm"],
            "dataset_b_resolution_fwhm_nm": row_b.get("resolution_fwhm_nm", ""),
            "dataset_b_reported_temperature_eV": row_b.get("reported_temperature_eV", ""),
            "dataset_b_calculated_temperature_eV": row_b.get("calculated_temperature_eV", ""),
            "reconciliation_status": "KEY_FIELDS_MATCH_ONLY",
            "reconciled_value": "",
            "rationale": ("Matching ion/wavelength/measured-FWHM values identify a value-based "
                          "correspondence only; they do not establish shared raw-data provenance. "
                          "No correction is inferred and neither source is altered."),
        })
    return pd.DataFrame(records)


def validate_p01_reconciliation(ledger: pd.DataFrame | None = None) -> dict:
    """Validate ledger safety properties and summarize match counts."""
    frame = pd.read_csv(LEDGER, keep_default_na=False) if ledger is None else ledger.copy(deep=True)
    required = {"reconciliation_status", "reconciled_value", "rationale"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Ledger lacks columns: {sorted(required - set(frame.columns))}")
    if frame["reconciled_value"].astype(str).str.strip().ne("").any():
        raise ValueError("Reconciled values must remain blank until a traceable method is authorized.")
    if not frame["reconciliation_status"].isin(["KEY_FIELDS_MATCH_ONLY", "NO_MATCH"]).all():
        raise ValueError("Unknown reconciliation status.")
    if frame["rationale"].astype(str).str.strip().eq("").any():
        raise ValueError("Every ledger row requires an explicit rationale.")
    return {
        "rows": int(len(frame)),
        "key_fields_match_only": int((frame["reconciliation_status"] == "KEY_FIELDS_MATCH_ONLY").sum()),
        "no_match": int((frame["reconciliation_status"] == "NO_MATCH").sum()),
        "numeric_corrections_applied": 0,
    }


if __name__ == "__main__":
    ledger = build_p01_reconciliation()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    ledger.to_csv(LEDGER, index=False)
    print(validate_p01_reconciliation(ledger))
