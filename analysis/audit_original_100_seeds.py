"""Recompute the original 100-seed B-copy vs C-full result from tracked raw files.

The paired seed is the experimental unit. This script never trusts manuscript summary
numbers: it loads each seed JSON, verifies pairing, recomputes descriptive statistics,
Welch and paired tests, a two-sided sign-flip Monte Carlo test, bootstrap CI, and
power-based sample-size estimates for a future independent paired replication.
"""
import json
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "results" / "raw"
OUT = ROOT / "data" / "results" / "original_100_seed_audit.json"
N_PERM = 200_000
N_BOOT = 50_000


def load_condition(mode):
    files = sorted(RAW.glob(f"mode_{mode}_seed_*.json"))
    expected = [f"{i:03d}" for i in range(100)]
    ids = [p.stem.rsplit("seed_", 1)[1] for p in files]
    if ids != expected:
        raise ValueError(f"{mode}: expected exactly seed IDs 000..099; got {len(ids)} files")
    rows = []
    for path in files:
        obj = json.loads(path.read_text())
        if obj.get("mode") != mode or obj.get("seed") != int(path.stem.rsplit("_", 1)[1]):
            raise ValueError(f"Metadata mismatch in {path}")
        scores = obj.get("task_success_rates")
        if not isinstance(scores, list) or len(scores) != 10:
            raise ValueError(f"Expected 10 generation scores in {path}")
        if not np.all(np.isfinite(scores)):
            raise ValueError(f"Non-finite scores in {path}")
        rows.append(scores)
    return np.asarray(rows, dtype=float)


def mc_sign_flip(d, n=N_PERM, seed=20261102):
    rng = np.random.default_rng(seed)
    observed = abs(float(np.mean(d)))
    extreme = 0
    done = 0
    while done < n:
        size = min(5000, n - done)
        signs = rng.choice((-1.0, 1.0), size=(size, len(d)))
        extreme += int(np.sum(np.abs(np.mean(signs * d, axis=1)) >= observed))
        done += size
    return (extreme + 1) / (n + 1), extreme


def bootstrap_ci(d, n=N_BOOT, seed=20261103):
    rng = np.random.default_rng(seed)
    means = np.empty(n)
    for start in range(0, n, 1000):
        size = min(1000, n - start)
        idx = rng.integers(0, len(d), size=(size, len(d)))
        means[start:start + size] = np.mean(d[idx], axis=1)
    return np.quantile(means, [0.025, 0.975]).tolist()


def paired_power_n(dz, power=0.80, alpha=0.05, max_n=10000):
    # Two-sided paired t-test power using noncentral t distribution.
    if not np.isfinite(dz) or abs(dz) < 1e-12:
        return None
    for n in range(3, max_n + 1):
        df = n - 1
        critical = stats.t.ppf(1 - alpha / 2, df)
        ncp = abs(dz) * np.sqrt(n)
        achieved = stats.nct.cdf(-critical, df, ncp) + stats.nct.sf(critical, df, ncp)
        if achieved >= power:
            return n
    return None


def main():
    b = load_condition("B-copy")
    c = load_condition("C-full")
    d = b[:, -1] - c[:, -1]
    t_pair = stats.ttest_rel(b[:, -1], c[:, -1])
    t_welch = stats.ttest_ind(b[:, -1], c[:, -1], equal_var=False)
    wilcoxon = stats.wilcoxon(d, alternative="two-sided", zero_method="wilcox")
    p_flip, extreme = mc_sign_flip(d)
    dz = float(np.mean(d) / np.std(d, ddof=1))
    report = {
        "dataset": "original GAL scalar-agent experiment",
        "experimental_unit": "paired universe seed",
        "n_paired_seeds": int(len(d)),
        "generation": 10,
        "B_copy": {"mean": float(np.mean(b[:, -1])), "sd": float(np.std(b[:, -1], ddof=1))},
        "C_full": {"mean": float(np.mean(c[:, -1])), "sd": float(np.std(c[:, -1], ddof=1))},
        "difference_B_minus_C": {
            "mean": float(np.mean(d)), "sd": float(np.std(d, ddof=1)),
            "median": float(np.median(d)), "positive_pairs": int(np.sum(d > 0)),
            "negative_pairs": int(np.sum(d < 0)), "ties": int(np.sum(d == 0)),
            "bootstrap_95_percentile_ci": bootstrap_ci(d),
            "cohens_dz": dz
        },
        "tests_two_sided": {
            "paired_t": {"statistic": float(t_pair.statistic), "p": float(t_pair.pvalue)},
            "welch_t": {"statistic": float(t_welch.statistic), "p": float(t_welch.pvalue)},
            "wilcoxon": {"statistic": float(wilcoxon.statistic), "p": float(wilcoxon.pvalue)},
            "sign_flip_mc": {"permutations": N_PERM, "extreme": extreme, "p_plus_one": p_flip}
        },
        "future_paired_replication_power": {
            "effect_assumption": "observed paired Cohen dz from this historical dataset; optimistic if effect is inflated",
            "alpha_two_sided": 0.05,
            "n_for_80_percent_power": paired_power_n(dz, 0.80),
            "n_for_90_percent_power": paired_power_n(dz, 0.90)
        },
        "interpretation": "This tests the specific simulated B-copy vs C-full contrast, not a universal inheritance law or neural catastrophic-forgetting claim."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
