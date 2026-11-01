"""Reproducible native-GAL experiment using the repository's actual Agent and Environment."""
import argparse
import json
import random
from pathlib import Path
import sys

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from gal.agents.agent import Agent
from gal.environment.world import Environment

MODES = ("A", "B-copy", "C-full", "C-no-memory", "C-low-effort")


def run_one(mode, seed, agents=100, generations=10):
    world = Environment()
    previous = []
    history = []
    for gen in range(1, generations + 1):
        current = [
            Agent(identity=f"GAL-GEN{gen}-{i:03d}", generation=gen, universe_seed=seed)
            for i in range(agents)
        ]
        if previous:
            for i, child in enumerate(current):
                parent = previous[i % len(previous)]
                child.parents.append(parent.identity)
                parent.successor = child.identity
                child.inherit(parent, mode)
        for agent in current:
            agent.develop()
            for _ in range(5):
                agent.learn_independently(world)
                agent.work(world, num_tasks=10)
        history.append(float(np.mean([a.task_success_rate for a in current])))
        previous = current
    return history


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--agents", type=int, default=100)
    ap.add_argument("--generations", type=int, default=10)
    ap.add_argument("--out", default="artifacts/native_gal")
    args = ap.parse_args()
    out = Path(args.out)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    arrays = {}
    for mode in MODES:
        rows = []
        for seed in range(args.seeds):
            # Agent owns deterministic, isolated RNG streams; these seed the
            # world-independent global libraries used by surrounding code.
            random.seed(seed)
            np.random.seed(seed)
            scores = run_one(mode, seed, args.agents, args.generations)
            rows.append(scores)
            (raw_dir / f"mode_{mode}_seed_{seed:03d}.json").write_text(
                json.dumps({"mode": mode, "seed": seed, "agents": args.agents,
                            "generations": args.generations, "task_success_rates": scores}, indent=2)
            )
        arrays[mode] = np.asarray(rows, dtype=float)

    report = {
        "model": "gal.agents.agent.Agent + gal.environment.world.Environment",
        "n_seeds": args.seeds,
        "agents_per_generation": args.agents,
        "generations": args.generations,
        "modes": {},
        "paired_comparisons_vs_B_copy": {}
    }
    for mode, values in arrays.items():
        report["modes"][mode] = {
            "generation_10_mean": float(values[:, -1].mean()),
            "generation_10_sd": float(values[:, -1].std(ddof=1)),
            "generation_trajectory_mean": values.mean(axis=0).tolist(),
        }
    for mode in MODES:
        if mode == "B-copy":
            continue
        d = arrays["B-copy"][:, -1] - arrays[mode][:, -1]
        test = stats.ttest_rel(arrays["B-copy"][:, -1], arrays[mode][:, -1])
        report["paired_comparisons_vs_B_copy"][mode] = {
            "mean_difference_B_minus_mode": float(d.mean()),
            "paired_t": float(test.statistic),
            "p_uncorrected": float(test.pvalue),
            "cohens_dz": float(d.mean() / d.std(ddof=1)) if d.std(ddof=1) else None,
            "B_copy_wins": int((d > 0).sum()),
            "mode_wins": int((d < 0).sum()),
            "ties": int((d == 0).sum())
        }
    (out / "native_gal_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
