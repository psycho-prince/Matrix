"""Independent paired-seed validation for the committed B-copy/C-full results."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "results" / "raw"


def _seed_id(path):
    return path.stem.split("seed_", 1)[1]


def verify_seeds(b_files, c_files):
    b_seeds = sorted(_seed_id(Path(p)) for p in b_files)
    c_seeds = sorted(_seed_id(Path(p)) for p in c_files)

    if len(b_seeds) != 100 or len(set(b_seeds)) != 100:
        raise ValueError(f"Expected 100 unique B-copy seeds, found {len(b_seeds)}")
    if len(c_seeds) != 100 or len(set(c_seeds)) != 100:
        raise ValueError(f"Expected 100 unique C-full seeds, found {len(c_seeds)}")
    if b_seeds != c_seeds:
        raise ValueError("Seed IDs do not match across paired comparisons")
    return b_seeds


def paired_sign_flip_test(b_values, c_values, n_permutations=100_000, seed=42):
    """One-sided Monte Carlo sign-flip test for B-copy > C-full."""
    differences = np.asarray(b_values, dtype=float) - np.asarray(c_values, dtype=float)
    if differences.ndim != 1 or differences.size < 2:
        raise ValueError("At least two paired observations are required")

    observed = float(np.mean(differences))
    rng = np.random.default_rng(seed)
    extreme = 0
    # Batch the simulation to avoid allocating an unbounded permutation matrix.
    batch_size = 2_000
    remaining = n_permutations
    while remaining:
        batch = min(batch_size, remaining)
        signs = rng.choice((-1.0, 1.0), size=(batch, differences.size))
        permuted_means = np.mean(signs * differences, axis=1)
        extreme += int(np.count_nonzero(permuted_means >= observed))
        remaining -= batch

    p_value = (extreme + 1) / (n_permutations + 1)
    return observed, p_value, extreme


def load_generation_10(files):
    values = []
    for path in files:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        if len(data.get("task_success_rates", [])) != 10:
            raise ValueError(f"Expected 10 generation scores in {path}")
        values.append(float(data["task_success_rates"][-1]))
    return np.asarray(values)


def main():
    b_files = sorted(RAW_DIR.glob("mode_B-copy_seed_*.json"))
    c_files = sorted(RAW_DIR.glob("mode_C-full_seed_*.json"))
    verify_seeds(b_files, c_files)

    b_values = load_generation_10(b_files)
    c_values = load_generation_10(c_files)
    observed, p_value, extreme = paired_sign_flip_test(b_values, c_values)

    print("Paired-seed validation: B-copy vs C-full")
    print(f"Seeds: {len(b_values)}")
    print(f"B-copy mean: {np.mean(b_values):.4f}")
    print(f"C-full mean: {np.mean(c_values):.4f}")
    print(f"Mean paired difference (B-copy - C-full): {observed:+.4f}")
    print(f"One-sided sign-flip Monte Carlo p-value: {p_value:.6e}")
    print(f"Extreme permutations: {extreme}/{100_000}")


if __name__ == "__main__":
    main()
