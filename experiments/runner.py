import argparse
import sys
import json
from pathlib import Path
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Add the project root to the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from gal.agents.agent import Agent
from gal.environment.world import Environment

def run_single_simulation(mode: str, num_agents: int, generations: int, seed: int):
    random.seed(seed)
    np.random.seed(seed)
    
    world = Environment(random_seed=seed)
    previous_generation = []
    success_rates = []
    
    for gen in range(1, generations + 1):
        current_generation = [Agent(identity=f"GAL-GEN{gen}-{i:03d}", generation=gen, random_seed=seed+i) for i in range(num_agents)]
        
        # Phase 1: Inheritance
        if previous_generation:
            for i, child in enumerate(current_generation):
                parent = previous_generation[i % len(previous_generation)]
                child.parents.append(parent.identity)
                parent.successor = child.identity
                
                child.inherit(parent, mode)
        
        # Phase 2: Lifecycle
        for agent in current_generation:
            agent.develop()
            for _ in range(5): 
                agent.learn_independently(world)
                agent.work(world, num_tasks=10)
                
        # Phase 3: Metrics
        gen_success = np.mean([a.task_success_rate for a in current_generation])
        success_rates.append(gen_success)
        
        previous_generation = current_generation
        
    return success_rates

def run_experiment(mode: str, num_agents: int, generations: int, num_seeds: int, output_dir: Path):
    print(f"Running Experiment - Mode: {mode}")
    all_results = []
    for seed in range(num_seeds):
        res = run_single_simulation(mode, num_agents, generations, seed)
        all_results.append(res)
        
    all_results = np.array(all_results) # Shape: (num_seeds, generations)
    mean_results = np.mean(all_results, axis=0)
    
    # 95% Confidence Intervals
    se = stats.sem(all_results, axis=0)
    ci = se * stats.t.ppf((1 + 0.95) / 2., num_seeds-1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    np.save(output_dir / f"mode_{mode}_results.npy", all_results)
    
    return all_results, mean_results, ci

def plot_results(results_summary, generations, output_file):
    plt.figure(figsize=(12, 7))
    x = np.arange(1, generations + 1)
    
    colors = {
        'A': 'red', 
        'B-copy': 'blue', 
        'C-full': 'green',
        'C-no-memory': 'orange',
        'C-low-effort': 'purple'
    }
    
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
    plt.savefig(output_file)
    print(f"Saved plot to {output_file}")

def run_stats(results_summary):
    print("\n--- Statistical Analysis (Gen 10) ---")
    c_full = results_summary['C-full']['raw'][:, -1]
    b_copy = results_summary['B-copy']['raw'][:, -1]
    
    # Welch's t-test
    t_stat, p_val = stats.ttest_ind(c_full, b_copy, equal_var=False)
    
    # Cohen's d effect size
    mean_c = np.mean(c_full)
    mean_b = np.mean(b_copy)
    pooled_std = np.sqrt((np.std(c_full, ddof=1)**2 + np.std(b_copy, ddof=1)**2) / 2)
    cohens_d = (mean_c - mean_b) / pooled_std
    
    print(f"C-full vs B-copy:")
    print(f"  Welch's t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_val:.4e}")
    print(f"  Cohen's d: {cohens_d:.4f}")
    
    if p_val < 0.05:
        print("  => Statistically Significant Difference at p < 0.05")
    else:
        print("  => NO Statistically Significant Difference at p < 0.05")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GAL v0.2 Experiments")
    parser.add_argument("--agents", type=int, default=100)
    parser.add_argument("--generations", type=int, default=10)
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--outdir", type=str, default="results/processed")
    args = parser.parse_args()
    
    out_path = Path(args.outdir)
    results_summary = {}
    
    modes = ['A', 'B-copy', 'C-full', 'C-no-memory', 'C-low-effort']
    
    for mode in modes:
        raw, mean, ci = run_experiment(mode, args.agents, args.generations, args.seeds, out_path)
        results_summary[mode] = {'raw': raw, 'mean': mean, 'ci': ci}
        
        print(f"  Final Gen {args.generations} Mean Success Rate: {mean[-1]:.2%} ± {ci[-1]:.2%} (95% CI)")
        
    plot_file = Path("results/figures/experiment_0.2_results.png")
    plot_file.parent.mkdir(parents=True, exist_ok=True)
    plot_results(results_summary, args.generations, plot_file)
    
    run_stats(results_summary)
