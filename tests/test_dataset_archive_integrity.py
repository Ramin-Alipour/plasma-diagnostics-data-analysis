from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "datasets" / "dataset_a"
B = ROOT / "datasets" / "dataset_b"


def test_dataset_a_and_b_have_separate_manifests():
    assert (A / "source_manifest.csv").is_file()
    assert (B / "source_manifest.csv").is_file()
    assert (B / "column_provenance.csv").is_file()
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


def test_modal_percentages_are_not_silently_normalized():
    df = pd.read_csv(B / "publication_reconstruction" / "paper2_modes.csv")
    cols = [f"m{i}_pct" for i in range(1, 7)]
    sums = df[cols].sum(axis=1)
    # Published rounded values need not sum exactly to 100%; preserve them as transcribed.
    assert len(df) == 19
    assert ((sums - 100).abs() > 0).any()


def test_p04_values_remain_explicitly_approximate():
    df = pd.read_csv(B / "publication_reconstruction" / "paper4_pressure_transport.csv")
    assert df["confidence"].str.contains("approximate_reconstruction").all()
    assert df["source"].str.contains("not exact table transcriptions").all()


def test_large_source_arrays_are_explicitly_tracked_as_pending():
    # Do not allow a partial data upload to be mistaken for a complete data release.
    assert not (A / "laboratory_signal_analysis" / "e06_mhd_signal.csv").exists()
    assert not (B / "publication_digitization" / "p06_figure2_digitized.csv").exists()
