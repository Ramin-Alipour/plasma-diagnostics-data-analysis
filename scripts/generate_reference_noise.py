"""Create reproducible 1.3%-relative-sigma perturbations of published constraints.

Outputs are synthetic perturbation benchmarks, not original IR-T1 raw data.
Only explicitly configured observable columns are perturbed. Exact zeros are
preserved because a relative-noise model has zero standard deviation at zero.
P05 contains only qualitative effects in its constraint CSV and is recorded as
not eligible for numerical perturbation; its synthetic signal needs a separate,
explicitly documented generator.
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIGMA_RELATIVE = 0.013
SEED = 130026

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
    # Only measured/derived outcomes, not probe geometry or model coefficients.
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
P03_ALLOWED_QUANTITIES = {
    "edge_electron_temperature", "plasma_current_max",
    "equal_saturation_current_location",
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
        rows = list(reader)

    for name in ("data_provenance", "noise_model", "noise_relative_sigma",
                 "noise_seed", "reference_file"):
        if name not in fieldnames:
            fieldnames.append(name)

    changed_cells = exact_zeros = non_numeric_or_blank = filtered_cells = 0
    for row in rows:
        for column in columns:
            if (source.name == "paper3_compound_probe.csv"
                    and row.get("quantity") not in P03_ALLOWED_QUANTITIES):
                filtered_cells += 1
                continue
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
        row["reference_file"] = source.relative_to(ROOT).as_posix()

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return {
        "paper_id": source.stem.replace("paper", "P").split("_")[0],
        "reference_file": source.relative_to(ROOT).as_posix(),
        "synthetic_file": destination.relative_to(ROOT).as_posix()
            if destination.is_relative_to(ROOT) else destination.as_posix(),
        "columns_perturbed": ";".join(columns),
        "rows": len(rows),
        "changed_cells": changed_cells,
        "exact_zeros_preserved": exact_zeros,
        "filtered_cells": filtered_cells,
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
        manifest.append(perturb_csv(source, output_dir / filename, columns, seed + offset))

    # P05 reports directional/qualitative effects, not numeric point values.
    # Do not invent numeric values merely to force a 1.3% perturbation.
    manifest.append({
        "paper_id": "P05",
        "reference_file": "data/publication_reconstruction/paper5_limiter_transport.csv",
        "synthetic_file": "",
        "columns_perturbed": "",
        "rows": 0,
        "changed_cells": 0,
        "exact_zeros_preserved": 0,
        "filtered_cells": 0,
        "blank_or_non_numeric_cells_skipped": 0,
        "relative_sigma": SIGMA_RELATIVE,
        "seed": seed + len(COLUMNS_BY_FILE),
        "status": "not_generated_qualitative_constraints_only",
    })
    manifest_path = output_dir / "noise_manifest.csv"
    output_dir.mkdir(parents=True, exist_ok=True)
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
        print(f"{result['paper_id']}: {result['status']}; "
              f"{result['changed_cells']} cells perturbed; "
              f"{result['exact_zeros_preserved']} exact zeros preserved")
    print(f"Manifest: {args.output_dir / 'noise_manifest.csv'}")


if __name__ == "__main__":
    main()
