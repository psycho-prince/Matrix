import argparse
import sys
import json
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import csv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from gal.agents.agent import Agent
from gal.environment.world import Environment

def run_single_simulation(mode: str, num_agents: int, generations: int, seed: int):
    random.seed(seed)
    np.random.seed(seed)
    
    world = Environment()
    previous_generation = []
    success_rates = []
    
    for gen in range(1, generations + 1):
        current_generation = [Agent(identity=f"GAL-GEN{gen}-{i:03d}", generation=gen, universe_seed=seed) for i in range(num_agents)]
        
        if previous_generation:
            for i, child in enumerate(current_generation):
                parent = previous_generation[i % len(previous_generation)]
                child.parents.append(parent.identity)
                parent.successor = child.identity
                child.inherit(parent, mode)
        
        for agent in current_generation:
            agent.develop()
            for _ in range(5): 
                agent.learn_independently(world)
                agent.work(world, num_tasks=10)
                
        gen_success = np.mean([a.task_success_rate for a in current_generation])
        success_rates.append(gen_success)
        previous_generation = current_generation
        
    return success_rates

def run_experiment(mode: str, num_agents: int, generations: int, num_seeds: int, output_dir: Path):
    print(f"Running Experiment - Mode: {mode}")
    all_results = []
    
    raw_dir = output_dir.parent / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    for seed in range(num_seeds):
        res = run_single_simulation(mode, num_agents, generations, seed)
        all_results.append(res)
        
        # Save raw seed data
        with open(raw_dir / f"mode_{mode}_seed_{seed:03d}.json", "w") as f:
            json.dump({
                "mode": mode,
                "seed": seed,
                "num_agents": num_agents,
                "generations": generations,
                "task_success_rates": res
            }, f, indent=2)
        
    all_results = np.array(all_results)
    mean_results = np.mean(all_results, axis=0)
    se = stats.sem(all_results, axis=0)
    ci = se * stats.t.ppf((1 + 0.95) / 2., num_seeds-1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    np.save(output_dir / f"mode_{mode}_results.npy", all_results)
    
    return all_results, mean_results, ci

def save_summary_csv(results_summary, generations, output_dir):
    csv_path = output_dir / "summary.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["Mode"] + [f"Gen_{i}" for i in range(1, generations + 1)]
        writer.writerow(header)
        for mode, data in results_summary.items():
            mean = data['mean']
            writer.writerow([mode] + [f"{m:.4f}" for m in mean])

def plot_results(results_summary, generations, figures_dir):
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(12, 7))
    x = np.arange(1, generations + 1)
    colors = {'A': 'red', 'B-copy': 'blue', 'C-full': 'green', 'C-no-memory': 'orange', 'C-low-effort': 'purple'}
    
    for mode, data in results_summary.items():
        mean, ci = data['mean'], data['ci']
        plt.plot(x, mean, label=mode, color=colors[mode], linewidth=2)
        plt.fill_between(x, mean - ci, mean + ci, color=colors[mode], alpha=0.2)
        
    plt.title('Generational Task Performance Across Populations (95% CI)')
    plt.xlabel('Generation')
    plt.ylabel('Average Task Success Rate')
    plt.ylim(0, 1.0)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(figures_dir / "generation_trajectory.png")
    
    # Final generation comparison bar chart
    plt.figure(figsize=(10, 6))
    modes = list(results_summary.keys())
    means = [results_summary[m]['mean'][-1] for m in modes]
    cis = [results_summary[m]['ci'][-1] for m in modes]
    plt.bar(modes, means, yerr=cis, color=[colors[m] for m in modes], capsize=5)
    plt.title('Final Generation (Gen 10) Task Success Rate Comparison')
    plt.ylabel('Task Success Rate')
    plt.tight_layout()
    plt.savefig(figures_dir / "final_generation_comparison.png")

def run_stats(results_summary, stats_dir):
    stats_dir.mkdir(parents=True, exist_ok=True)
    
    c_full = results_summary['C-full']['raw'][:, -1]
    b_copy = results_summary['B-copy']['raw'][:, -1]
    
    # Paired t-test
    t_stat, p_val = stats.ttest_rel(b_copy, c_full)
    
    # Paired effect size (d_z)
    differences = b_copy - c_full
    mean_diff = np.mean(differences)
    sd_diff = np.std(differences, ddof=1)
    cohens_d_z = mean_diff / sd_diff if sd_diff > 0 else float('inf')
    
    mean_c = np.mean(c_full)
    mean_b = np.mean(b_copy)
    
    report = {
        "comparison": "B-copy vs C-full",
        "test": "Paired t-test",
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "cohens_d_z": float(cohens_d_z),
        "significant_at_05": bool(p_val < 0.05),
        "mean_b_copy": float(mean_b),
        "mean_c_full": float(mean_c)
    }
    
    with open(stats_dir / "statistical_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Paired t-test B-copy vs C-full: t={t_stat:.4f}, p={p_val:.2e}, d_z={cohens_d_z:.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agents", type=int, default=100)
    parser.add_argument("--generations", type=int, default=10)
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--outdir", type=str, default="results")
    args = parser.parse_args()
    
    base_out = Path(args.outdir)
    processed_out = base_out / "processed"
    
    results_summary = {}
    modes = ['A', 'B-copy', 'C-full', 'C-no-memory', 'C-low-effort']
    
    for mode in modes:
        raw, mean, ci = run_experiment(mode, args.agents, args.generations, args.seeds, processed_out)
        results_summary[mode] = {'raw': raw, 'mean': mean, 'ci': ci}
        
    save_summary_csv(results_summary, args.generations, processed_out)
    plot_results(results_summary, args.generations, base_out / "figures")
    run_stats(results_summary, base_out / "statistics")
    
    print("\nExperiment complete. Archive generated.")
