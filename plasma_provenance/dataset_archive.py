"""Load explicitly separated Dataset A/B tables from a repository checkout.

These helpers preserve the distinction between laboratory-archive files and
publication-derived tables. They do not assert that archived values are
independently validated experimental measurements.
"""
from pathlib import Path
import pandas as pd

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_DATASETS_ROOT = _REPOSITORY_ROOT / "datasets"
_DATASET_DIRS = {
    "A": _DATASETS_ROOT / "dataset_a",
    "B": _DATASETS_ROOT / "dataset_b",
}


def load_dataset_table(dataset: str, relative_path: str) -> pd.DataFrame:
    """Load one CSV from Dataset A or B, rejecting paths outside its directory."""
    key = dataset.upper()
    if key not in _DATASET_DIRS:
        raise ValueError("dataset must be 'A' or 'B'")
    root = _DATASET_DIRS[key].resolve()
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root):
        raise ValueError("relative_path must remain inside the selected dataset")
    if path.suffix.lower() != ".csv":
        raise ValueError("only CSV tables are supported")
    if not path.is_file():
        raise FileNotFoundError(f"Dataset {key} CSV not found: {relative_path}")
    return pd.read_csv(path)


def dataset_manifest(dataset: str) -> pd.DataFrame:
    """Return the file-level source manifest for Dataset A or Dataset B."""
    return load_dataset_table(dataset, "source_manifest.csv")
