"""Paired analysis and prospective power planning for canonical Split-MNIST runs."""
import json
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "mnist" / "canonical_split_mnist_results.json"
OUT = ROOT / "data" / "mnist" / "canonical_split_mnist_statistics.json"
METHODS = ("GAL", "EWC", "SI", "GEM", "ER", "DER++")


def required_n(dz, power, alpha=0.05, maximum=10000):
    if abs(dz) < 1e-12:
        return None
    for n in range(3, maximum + 1):
        df = n - 1
        crit = stats.t.ppf(1 - alpha / 2, df)
        ncp = abs(dz) * np.sqrt(n)
        achieved = stats.nct.cdf(-crit, df, ncp) + stats.nct.sf(crit, df, ncp)
        if achieved >= power:
            return n
    return None


def main():
    data = json.loads(SOURCE.read_text())
    rows = data["per_seed"]
    by_method = {m: {r["seed"]: r["final_accuracy"] for r in rows if r["method"] == m} for m in METHODS}
    seeds = sorted(set.intersection(*(set(v) for v in by_method.values())))
    if len(seeds) != data["seeds"]:
        raise ValueError("Incomplete or unpaired seed results")
    comparisons = {}
    for baseline in METHODS:
        if baseline == "GAL":
            continue
        d = np.asarray([by_method["GAL"][s] - by_method[baseline][s] for s in seeds])
        test = stats.ttest_rel([by_method["GAL"][s] for s in seeds],
                               [by_method[baseline][s] for s in seeds])
        dz = float(d.mean() / d.std(ddof=1))
        comparisons[f"GAL_vs_{baseline}"] = {
            "mean_paired_difference": float(d.mean()),
            "sd_paired_difference": float(d.std(ddof=1)),
            "cohens_dz": dz,
            "paired_t": float(test.statistic),
            "p_uncorrected": float(test.pvalue),
            "n_for_80_percent_power": required_n(dz, 0.80),
            "n_for_90_percent_power": required_n(dz, 0.90)
        }
    pvals = [v["p_uncorrected"] for v in comparisons.values()]
    order = np.argsort(pvals)
    adjusted = [None] * len(pvals)
    running = 0.0
    m = len(pvals)
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m-rank) * pvals[idx]))
        adjusted[idx] = running
    for key, p_adj in zip(comparisons, adjusted):
        comparisons[key]["p_holm"] = float(p_adj)
    result = {"n_paired_seeds": len(seeds), "alpha": 0.05,
              "multiple_comparison_correction": "Holm across five GAL-vs-baseline comparisons",
              "comparisons": comparisons,
              "sample_size_note": "The initial 20-seed run is a pilot. Final N must be selected from blinded pilot variance or a pre-registered minimum effect, not by chasing significance."}
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
