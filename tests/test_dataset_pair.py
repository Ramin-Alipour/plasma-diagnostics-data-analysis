import json

import numpy as np
import pytest

from publication_reconstruction.dataset_pair import build_dataset_pair


def test_builds_reproducible_pair_and_preserves_zero(tmp_path):
    source = tmp_path / "records.json"
    source.write_text(json.dumps([
        {"record_id": "r1", "source_paper": "P01", "source_locator": "Table 1",
         "quantity": "temperature", "reported_value": 10.0, "unit": "eV",
         "source_type": "exact_table", "extraction_method": "table transcription"},
        {"record_id": "r2", "source_paper": "P02", "source_locator": "Table 2",
         "quantity": "zero_check", "reported_value": 0.0, "unit": "",
         "source_type": "exact_table", "extraction_method": "table transcription"},
        {"record_id": "r3", "reported_value": "not reported"},
    ]), encoding="utf-8")

    out1 = tmp_path / "out1"
    out2 = tmp_path / "out2"
    a1, b1, stats = build_dataset_pair(source, out1, seed=123)
    _, b2, _ = build_dataset_pair(source, out2, seed=123)

    assert stats["numeric_reference_records_written"] == 2
    assert stats["non_numeric_records_skipped"] == 1
    assert stats["zero_reference_values"] == 1
    assert b1.read_bytes() == b2.read_bytes()

    import pandas as pd
    df = pd.read_csv(b1)
    assert df.loc[df.record_id == "r2", "synthetic_value"].iloc[0] == 0.0
    assert df.loc[df.record_id == "r2", "zero_handling"].iloc[0].startswith("zero reference")
    assert np.isfinite(df.loc[df.record_id == "r1", "synthetic_value"].iloc[0])


def test_rejects_negative_noise(tmp_path):
    source = tmp_path / "records.json"
    source.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError):
        build_dataset_pair(source, tmp_path / "out", sigma_relative=-0.01)
