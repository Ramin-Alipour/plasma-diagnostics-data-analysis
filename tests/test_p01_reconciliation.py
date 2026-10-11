from pathlib import Path
import pandas as pd
import pytest

from publication_reconstruction.reconciliation import (
    DATASET_A, DATASET_B, LEDGER, build_p01_reconciliation,
    validate_p01_reconciliation,
)


def test_p01_reconciliation_is_separate_and_does_not_invent_corrected_values():
    a_before = DATASET_A.read_bytes()
    b_before = DATASET_B.read_bytes()
    ledger = build_p01_reconciliation()
    summary = validate_p01_reconciliation(ledger)
    assert summary["rows"] == 15
    assert summary["key_fields_match_only"] == 15
    assert summary["numeric_corrections_applied"] == 0
    assert ledger["reconciled_value"].fillna("").eq("").all()
    assert set(ledger["reconciliation_status"]) == {"KEY_FIELDS_MATCH_ONLY"}
    assert DATASET_A.read_bytes() == a_before
    assert DATASET_B.read_bytes() == b_before


def test_p01_ledger_is_checked_in_and_matches_rebuilt_correspondence():
    stored = pd.read_csv(LEDGER, keep_default_na=False)
    rebuilt = build_p01_reconciliation()
    assert len(stored) == len(rebuilt) == 15
    assert stored["reconciliation_status"].tolist() == rebuilt["reconciliation_status"].tolist()
    assert stored["reconciled_value"].eq("").all()
    assert validate_p01_reconciliation(stored)["numeric_corrections_applied"] == 0


def test_p01_reconciliation_rejects_ambiguous_dataset_b_keys():
    a = pd.read_csv(DATASET_A)
    b = pd.read_csv(DATASET_B)
    b = pd.concat([b, b.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="Ambiguous duplicate key"):
        build_p01_reconciliation(a, b)


def test_p01_reconciliation_refuses_untracked_numeric_corrections():
    ledger = build_p01_reconciliation()
    ledger.loc[0, "reconciled_value"] = "123"
    with pytest.raises(ValueError, match="must remain blank"):
        validate_p01_reconciliation(ledger)
