from __future__ import annotations

import csv
from pathlib import Path

from scripts.generate_reference_noise import perturb_csv


def _read(path: Path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_relative_noise_is_reproducible_and_labels_synthetic_data(tmp_path):
    source = tmp_path / "reference.csv"
    source.write_text("paper_id,signal,source\nP99,100,Table X\nP99,200,Table X\n",
                      encoding="utf-8")
    out_a = tmp_path / "a.csv"
    out_b = tmp_path / "b.csv"
    perturb_csv(source, out_a, ["signal"], seed=130026)
    perturb_csv(source, out_b, ["signal"], seed=130026)
    assert out_a.read_bytes() == out_b.read_bytes()
    rows = _read(out_a)
    assert [r["data_provenance"] for r in rows] == [
        "synthetic_noise_perturbation_of_published_constraint"
    ] * 2
    assert all(r["noise_relative_sigma"] == "0.013" for r in rows)
    assert [float(r["signal"]) for r in rows] != [100.0, 200.0]


def test_exact_zero_is_preserved_and_counted(tmp_path):
    source = tmp_path / "reference.csv"
    source.write_text("paper_id,signal,source\nP99,0,Table X\nP99,100,Table X\n",
                      encoding="utf-8")
    output = tmp_path / "synthetic.csv"
    audit = perturb_csv(source, output, ["signal"], seed=1)
    rows = _read(output)
    assert float(rows[0]["signal"]) == 0.0
    assert audit["exact_zeros_preserved"] == 1
    assert audit["changed_cells"] == 1


def test_only_selected_numeric_columns_are_perturbed(tmp_path):
    source = tmp_path / "reference.csv"
    source.write_text("time_ms,signal,label\n1,10,original\n2,20,original\n",
                      encoding="utf-8")
    output = tmp_path / "synthetic.csv"
    perturb_csv(source, output, ["signal"], seed=5)
    rows = _read(output)
    assert [r["time_ms"] for r in rows] == ["1", "2"]
    assert [r["label"] for r in rows] == ["original", "original"]
