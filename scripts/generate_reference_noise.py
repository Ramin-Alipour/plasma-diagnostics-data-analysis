"""Create reproducible 1.3%-relative-sigma synthetic perturbations of published constraints.

These outputs are synthetic perturbation benchmarks, not original IR-T1 raw data.
Only explicitly configured observable columns are perturbed. Exact zeros are kept
at zero because a relative-noise model has zero standard deviation at zero; the
manifest records how many exact zeros were encountered.
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGMA_RELATIVE = 0.013
SEED = 130026

# Only outcome/observable columns are listed. Coordinates, time-window boundaries,
# setup parameters, identifiers, and qualitative text are deliberately not perturbed.
COLUMNS_BY_FILE = {
    "paper1_spectroscopy.csv": [
        "measured_fwhm_nm", "instrumental_broadening_fwhm_nm",
        "diffraction_broadening_fwhm_nm", "resolution_fwhm_nm",
        "doppler_fwhm_nm", "reported_temperature_eV",
    ],
    "paper2_hxr.csv": ["total_counts", "total_energy_keV", "mean_energy_keV"],
    "paper2_modes.csv": [
        "m1_pct", "m2_pct", "m3_pct", "m4_pct", "m5_pct", "m6_pct",
        "edge_safety_factor",
    ],
    "paper3_compound_probe.csv": ["value"],
    "paper4_pressure_transport.csv": [
        "avg_Er_reported", "avg_Etheta_reported",
        "radial_transport_no_bias", "radial_transport_plus200",
        "radial_transport_minus200", "poloidal_transport_no_bias",
        "poloidal_transport_plus200", "poloidal_transport_minus200",
    ],
    "paper6_pressure_mhd.csv": [
        "steady_state_ms", "electron_density_min_1e13_cm3",
        "electron_density_max_1e13_cm3", "electron_temperature_min_eV",
        "electron_temperature_max_eV", "dominant_frequency_kHz",
    ],
}


def perturb_csv(source: Path, destination: Path, columns: list[str], seed: int) -> dict:
    """Write a labelled synthetic copy, perturbing selected numeric cells only."""
    rng = random.Random(seed)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"No CSV header: {source}")
        fieldnames = list(reader.fieldnames)
        missing = sorted(set(columns) - set(fieldnames))
        if missing:
            raise ValueError(f"{source.name}: configured columns missing: {missing}")
        for name in ("data_provenance", "noise_model", "noise_relative_sigma",
                     "noise_seed", "reference_file"):
            if name not in fieldnames:
                fieldnames.append(name)
        rows = list(reader)

    changed_cells = 0
    exact_zeros = 0
    non_numeric_or_blank = 0
    for row in rows:
        for column in columns:
            raw = row.get(column, "")
            if raw is None or raw.strip() == "":
                non_numeric_or_blank += 1
                continue
            try:
                value = float(raw)
            except ValueError:
                non_numeric_or_blank += 1
                continue
            if value == 0.0:
                # Relative sigma is zero at an exact zero. Preserve it and audit it.
                exact_zeros += 1
                row[column] = format(value, ".12g")
                continue
            noisy = value + rng.gauss(0.0, SIGMA_RELATIVE * abs(value))
            row[column] = format(noisy, ".12g")
            changed_cells += 1
        row["data_provenance"] = "synthetic_noise_perturbation_of_published_constraint"
        row["noise_model"] = "additive_gaussian_sigma_0.013_times_abs_reference"
        row["noise_relative_sigma"] = str(SIGMA_RELATIVE)
        row["noise_seed"] = str(seed)
        row["reference_file"] = source.as_posix()

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return {
        "reference_file": source.as_posix(),
        "synthetic_file": destination.as_posix(),
        "columns_perturbed": ";".join(columns),
        "rows": len(rows),
        "changed_cells": changed_cells,
        "exact_zeros_preserved": exact_zeros,
        "blank_or_non_numeric_cells_skipped": non_numeric_or_blank,
        "relative_sigma": SIGMA_RELATIVE,
        "seed": seed,
        "status": "generated_synthetic_not_raw_data",
    }


def generate_all(output_dir: Path, seed: int = SEED) -> list[dict]:
    source_dir = ROOT / "data" / "publication_reconstruction"
    manifest = []
    for offset, (filename, columns) in enumerate(COLUMNS_BY_FILE.items()):
        source = source_dir / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = output_dir / filename
        manifest.append(perturb_csv(source, destination, columns, seed + offset))
    manifest_path = output_dir / "noise_manifest.csv"
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "data" / "synthetic_noise_1p3")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    results = generate_all(args.output_dir, args.seed)
    for result in results:
        print(f"{result['reference_file']} -> {result['synthetic_file']}: "
              f"{result['changed_cells']} cells, "
              f"{result['exact_zeros_preserved']} exact zeros preserved")
    print(f"Manifest: {args.output_dir / 'noise_manifest.csv'}")
    print("NOTE: P05's constraint table is qualitative; it is not numerically "
          "perturbed here. P05 requires a separately labelled synthetic signal "
          "derived from the documented directional effects.")


if __name__ == "__main__":
    main()
