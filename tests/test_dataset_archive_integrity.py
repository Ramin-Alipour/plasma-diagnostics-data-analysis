from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "datasets" / "dataset_a"
B = ROOT / "datasets" / "dataset_b"


def test_dataset_a_and_b_have_separate_manifests():
    assert (A / "source_manifest.csv").is_file()
    assert (B / "source_manifest.csv").is_file()
    assert (B / "column_provenance.csv").is_file()
    assert (ROOT / "datasets" / "PROVENANCE_CONFLICTS.md").is_file()
    a = pd.read_csv(A / "source_manifest.csv")
    b = pd.read_csv(B / "source_manifest.csv")
    assert not a.empty and not b.empty
    assert set(a["experiment_id"]) == {"E01", "E02", "E03", "E04", "E05", "E06"}
    assert set(b["paper_id"]) >= {"P01", "P02", "P03", "P04", "P05", "P06"}


def test_publication_hxr_mean_energy_is_arithmetically_consistent():
    df = pd.read_csv(B / "publication_reconstruction" / "paper2_hxr.csv")
    expected = df["total_energy_keV"] / df["total_counts"]
    assert (df["total_counts"] > 0).all()
    assert ((df["mean_energy_keV"] - expected).abs() < 1e-4).all()


def test_modal_percentages_are_preserved_without_normalization():
    df = pd.read_csv(B / "publication_reconstruction" / "paper2_modes.csv")
    cols = [f"m{i}_pct" for i in range(1, 7)]
    sums = df[cols].sum(axis=1)
    assert len(df) == 20
    assert ((sums - 100).abs() > 0).any()


def test_p04_values_remain_explicitly_approximate():
    df = pd.read_csv(B / "publication_reconstruction" / "paper4_pressure_transport.csv")
    assert df["confidence"].str.contains("approximate_reconstruction").all()
    assert df["source"].str.contains("not exact table transcriptions").all()


def test_p06_digitization_is_complete_and_numeric():
    df = pd.read_csv(B / "publication_digitization" / "p06_figure2_digitized.csv")
    assert len(df) == 423
    assert {"x_pixel", "y_pixel", "frequency_kHz", "amplitude"}.issubset(df.columns)
    assert df[["frequency_kHz", "amplitude"]].notna().all().all()


def test_e06_is_retained_as_owner_confirmed_diagnostic_software_output():
    a = pd.read_csv(A / "laboratory_signal_analysis" / "e06_mhd_signal.csv")
    manifest = pd.read_csv(A / "source_manifest.csv")
    row = manifest.loc[manifest["file"] == "e06_mhd_signal.csv"]
    assert len(a) == 423
    assert len(row) == 1
    assert "diagnostic software" in row.iloc[0]["basis"].lower()
    assert "owner-confirmed" in row.iloc[0]["basis"].lower()
    # Do not compare against Dataset B to infer/reject provenance: owner-confirmed source wins.

def test_inventory_and_manifest_paths_resolve_to_repository_files():
    inventory = pd.read_csv(ROOT / "datasets" / "dataset_inventory.csv")
    for relative_path in inventory["project_relative_path"]:
        assert (ROOT / relative_path).is_file(), relative_path

    for dataset_name, dataset_root in [("A", A), ("B", B)]:
        manifest = pd.read_csv(dataset_root / "source_manifest.csv")
        for relative_path in manifest["project_relative_path"]:
            assert (ROOT / relative_path).is_file(), f"{dataset_name}: {relative_path}"

    digitization_manifest = pd.read_csv(
        B / "publication_digitization" / "manifest.csv"
    )
    for outputs in digitization_manifest["output"].dropna():
        for relative_path in str(outputs).split(";"):
            assert (ROOT / relative_path).is_file(), relative_path

    # The historical top-level decision log is retained for compatibility,
    # but all of its outputs must resolve to the canonical Dataset B archive.
    legacy_manifest = pd.read_csv(
        ROOT / "data" / "publication_digitization" / "manifest.csv"
    )
    for outputs in legacy_manifest["output"].dropna():
        for relative_path in str(outputs).split(";"):
            assert (ROOT / relative_path).is_file(), relative_path

    # The legacy P06 tables are retained as a historical workflow snapshot.
    # They are not byte-for-byte/numerically identical to the canonical Dataset B
    # tables because the peak-picking outputs differ; do not silently overwrite
    # either version or infer that they are independent experiments.
    for filename in ["p06_figure2_digitized.csv", "p06_figure2_peak_summary.csv"]:
        canonical = pd.read_csv(B / "publication_digitization" / filename)
        legacy = pd.read_csv(ROOT / "data" / "publication_digitization" / filename)
        assert list(canonical.columns) == list(legacy.columns), filename
        assert len(canonical) == len(legacy), filename
    canonical_peaks = pd.read_csv(B / "publication_digitization" / "p06_figure2_peak_summary.csv")
    legacy_peaks = pd.read_csv(ROOT / "data" / "publication_digitization" / "p06_figure2_peak_summary.csv")
    keys = ["paper_id", "figure", "panel", "pressure_Torr"]
    pd.testing.assert_frame_equal(canonical_peaks[keys], legacy_peaks[keys])

    # Dataset A's signal-analysis manifest uses paths relative to the Dataset A
    # directory (unlike project_relative_path in the source manifests).
    signal_manifest = pd.read_csv(
        A / "laboratory_signal_analysis" / "manifest.csv"
    )
    assert len(signal_manifest) == 9
    for relative_path in signal_manifest["output"].dropna():
        assert (A / relative_path).is_file(), relative_path


def test_p06_provenance_records_match_canonical_dataset_b_peak_summary():
    import json

    peaks = pd.read_csv(B / "publication_digitization" / "p06_figure2_peak_summary.csv")
    records = json.loads((ROOT / "plasma_provenance" / "records.json").read_text(encoding="utf-8"))
    peak_records = {
        row["record_id"]: row
        for row in records
        if row.get("record_id") in {"P06-F2-a", "P06-F2-b", "P06-F2-c"}
    }
    assert set(peak_records) == {"P06-F2-a", "P06-F2-b", "P06-F2-c"}
    for panel_row in peaks.itertuples(index=False):
        record_id = f"P06-F2-{panel_row.panel}"
        record = peak_records[record_id]
        assert record["source_type"] == "digitized_from_published_figure"
        assert record["reported_value"] == pytest.approx(panel_row.peak_frequency_kHz)
        assert record["reconstructed_value"] == pytest.approx(panel_row.peak_frequency_kHz)
        assert "legacy workflow snapshot" in record["limitation"]


def test_repository_loader_reads_both_separated_archives_and_blocks_traversal():
    from plasma_provenance.dataset_archive import load_dataset_table, dataset_manifest

    a = load_dataset_table("A", "laboratory_measurements/exp1_spectroscopy.csv")
    b = load_dataset_table("B", "publication_reconstruction/paper1_spectroscopy.csv")
    assert len(a) == len(b) == 15
    assert not dataset_manifest("A").empty
    assert not dataset_manifest("B").empty
    p06_peaks = load_dataset_table("B", "publication_digitization/p06_figure2_peak_summary.csv")
    assert len(p06_peaks) == 3
    try:
        load_dataset_table("B", "../../pyproject.toml")
    except ValueError:
        pass
    else:
        raise AssertionError("path traversal should be rejected")
