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


def test_dataset_source_manifests_verify_exact_file_bytes():
    """Guard source files against silent edits using their Git blob fingerprints."""
    import hashlib

    for dataset_name, dataset_root in [("A", A), ("B", B)]:
        manifest = pd.read_csv(dataset_root / "source_manifest.csv", keep_default_na=False)
        assert "git_blob_sha1" in manifest.columns
        assert manifest["git_blob_sha1"].str.fullmatch(r"[0-9a-f]{40}").all()
        for row in manifest.itertuples(index=False):
            path = ROOT / row.project_relative_path
            assert path.is_file(), f"{dataset_name}: missing source file {row.project_relative_path}"
            raw = path.read_bytes()
            # Git blob object ID = SHA-1("blob " + byte_length + NUL + file_bytes).
            # This fingerprints exact repository bytes; it is not presented as a security signature.
            payload = b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
            actual = hashlib.sha1(payload).hexdigest()
            assert actual == row.git_blob_sha1, (
                f"{dataset_name}: source bytes changed for {row.project_relative_path}; "
                "review provenance and update the manifest only after explicit approval"
            )


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


def test_p04_summary_values_are_retranscribed_from_article_text():
    df = pd.read_csv(B / "publication_reconstruction" / "paper4_pressure_transport.csv")
    assert df["confidence"].eq("text_reported_approximate_values").all()
    assert df["source"].str.contains("P04 Results/Conclusion text").all()
    assert df["max_current_kA"].tolist() == [20, 22, 22]
    assert df["steady_state_ms"].tolist() == [12, 11, 10]
    # The article reports these values in Results text; they are not figure estimates.


def test_p06_digitization_is_complete_and_numeric():
    df = pd.read_csv(B / "publication_digitization" / "p06_figure2_digitized.csv")
    assert len(df) == 153
    assert df["panel"].value_counts().to_dict() == {"a": 51, "b": 51, "c": 51}
    assert {"x_pixel", "y_pixel", "frequency_kHz", "amplitude"}.issubset(df.columns)
    assert df[["frequency_kHz", "amplitude"]].notna().all().all()
    assert df["frequency_uncertainty_kHz"].eq(0.35).all()
    assert df["amplitude_uncertainty"].eq(0.02).all()
    peaks = pd.read_csv(B / "publication_digitization" / "p06_figure2_peak_summary.csv")
    assert peaks["peak_frequency_kHz"].tolist() == [42.0, 48.0, 52.0]
    assert peaks["peak_frequency_uncertainty_kHz"].eq(3.1).all()


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

    # The old top-level P06 tables remain historical snapshots; the canonical
    # digitization was rebuilt from the original PDF raster and therefore has
    # 153 points rather than the legacy 423. Keep the snapshot for traceability.
    canonical = pd.read_csv(B / "publication_digitization" / "p06_figure2_digitized.csv")
    legacy = pd.read_csv(ROOT / "data" / "publication_digitization" / "p06_figure2_digitized.csv")
    assert list(canonical.columns) == list(legacy.columns)
    assert len(canonical) == 153
    assert len(legacy) == 423
    canonical_peaks = pd.read_csv(B / "publication_digitization" / "p06_figure2_peak_summary.csv")
    legacy_peaks = pd.read_csv(ROOT / "data" / "publication_digitization" / "p06_figure2_peak_summary.csv")
    assert list(canonical_peaks.columns) == list(legacy_peaks.columns)
    assert len(canonical_peaks) == len(legacy_peaks) == 3
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


def test_publication_notebooks_use_canonical_dataset_b_paths():
    import json

    notebook_root = ROOT / "notebooks" / "publication_reconstruction"
    paths = list(notebook_root.glob("*.ipynb"))
    assert paths
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        source = "\\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
        )
        assert "data/publication_reconstruction/" not in source, path.name
        assert "data/publication_digitization/" not in source, path.name
    p01 = (notebook_root / "P01_full_spectroscopy_showcase.ipynb").read_text(encoding="utf-8")
    p06 = (notebook_root / "P06_IRT1_pressure_mhd_reconstruction.ipynb").read_text(encoding="utf-8")
    assert "datasets/dataset_b/publication_reconstruction/paper1_spectroscopy.csv" in p01
    assert "datasets/dataset_b/publication_digitization/p06_figure2_peak_summary.csv" in p06


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
        assert "peak-selection uncertainty" in record["limitation"]


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


def test_superseded_publication_tables_are_archived_not_exposed_as_current_data():
    """Prevent stale duplicate CSVs from being mistaken for canonical Dataset B."""
    root = Path(__file__).resolve().parents[1]
    legacy_active = root / "data" / "publication_reconstruction"
    archive = root / "archive" / "legacy_data_snapshot" / "publication_reconstruction"
    assert not legacy_active.exists()
    assert (archive / "README.md").is_file()
    note = (archive / "README.md").read_text(encoding="utf-8")
    assert "not the current Dataset B" in note

    canonical_p01 = pd.read_csv(
        root / "datasets" / "dataset_b" / "publication_reconstruction" / "paper1_spectroscopy.csv"
    )
    assert "calculated_temperature_eV" in canonical_p01.columns
    canonical_p04 = pd.read_csv(
        root / "datasets" / "dataset_b" / "publication_reconstruction" / "paper4_pressure_transport.csv"
    )
    row = canonical_p04.loc[canonical_p04["pressure_Torr"] == 2.3]
    assert len(row) == 1
    assert row.iloc[0]["radial_transport_plus200"] == pytest.approx(-0.0011)


def test_scientific_reference_matches_current_data_policy_and_available_sources():
    """Catch stale blanket claims and references to PDFs absent from the repository."""
    root = Path(__file__).resolve().parents[1]
    scientific_reference = (root / "SCIENTIFIC_REFERENCE.md").read_text(encoding="utf-8")
    assert "limited set of owner-supplied laboratory measurements" in scientific_reference
    assert "complete archive of original IR-T1 shot-level raw data" in scientific_reference
    assert "papers/" not in scientific_reference

    legacy_digitization_note = (
        root / "data" / "publication_digitization" / "README.md"
    ).read_text(encoding="utf-8")
    assert "42, 48 and 52 kHz" in legacy_digitization_note
    assert "44.31, 40.82 and 45.61 kHz" not in legacy_digitization_note

def test_test_modules_do_not_redefine_top_level_functions():
    """Prevent Python from silently replacing a test with a later same-named definition."""
    import ast

    tests_root = ROOT / "tests"
    for path in tests_root.rglob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        names = [
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        assert not duplicates, f"Duplicate top-level function definitions in {path}: {duplicates}"
