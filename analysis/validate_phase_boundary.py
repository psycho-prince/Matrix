import random
import numpy as np
import sys

class ValidationAgent:
    def __init__(self, rng: random.Random, capacity: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = capacity 
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def enforce_capacity(self):
        total = sum(self.skills.values())
        if total > self.capacity:
            for k in self.skills:
                self.skills[k] = self.skills[k] * (self.capacity / total)

    def learn(self, active_skill: str, steps: int):
        for _ in range(steps):
            if sum(self.skills.values()) < self.capacity:
                self.skills[active_skill] += self.rng.uniform(0.01, 0.05)
                self.enforce_capacity()

    def work(self, active_skill: str, difficulty: float, num_tasks: int, record: bool):
        for _ in range(num_tasks):
            if record:
                self.tasks_attempted += 1
            skill_level = self.skills[active_skill]
            
            if skill_level >= difficulty:
                success = self.rng.random() < 0.9
            else:
                success = self.rng.random() < ((skill_level / max(0.01, difficulty)) * 0.5)
                
            if success:
                if record:
                    self.tasks_succeeded += 1
                self.skills[active_skill] += 0.01
                self.enforce_capacity()

    @property
    def success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted

def run_validation_scenario(capacity=1.0, switch_freq=10, seeds=100, generations=20):
    modes = ['Exact', 'Lossy']
    seed_means = {m: [] for m in modes}
    
    for seed in range(seeds):
        rngs = {m: random.Random(seed) for m in modes}
        parent_skills = {m: {"A": 0.0, "B": 0.0} for m in modes}
        gen_scores = {m: [] for m in modes}
        
        for g in range(generations):
            active_skill = "A" if (g // switch_freq) % 2 == 0 else "B"
            
            for m in modes:
                agent = ValidationAgent(rngs[m], capacity)
                
                if m == 'Exact':
                    agent.skills = parent_skills[m].copy()
                elif m == 'Lossy':
                    agent.skills = {k: v * 0.5 for k, v in parent_skills[m].items()}
                    
                agent.enforce_capacity()
                agent.learn(active_skill, 10)
                agent.work(active_skill, 0.4, num_tasks=20, record=True)
                
                parent_skills[m] = agent.skills.copy()
                
                if g >= 10:
                    gen_scores[m].append(agent.success_rate)
                    
        for m in modes:
            seed_means[m].append(np.mean(gen_scores[m]))
            
    return np.array(seed_means['Exact']), np.array(seed_means['Lossy'])

def permutation_test(exact_scores, lossy_scores, num_permutations=100000):
    diffs = lossy_scores - exact_scores
    observed_mean_diff = np.mean(diffs)
    
    extreme_count = 0
    rng = np.random.default_rng(42)
    
    for _ in range(num_permutations):
        signs = rng.choice([-1, 1], size=len(diffs))
        permuted_mean = np.mean(diffs * signs)
        if permuted_mean >= observed_mean_diff:
            extreme_count += 1
            
    p_mc = (extreme_count + 1) / (num_permutations + 1)
    return observed_mean_diff, p_mc, extreme_count

if __name__ == "__main__":
    print("=== Paper 2 Independent Validation ===")
    print("Scenario: Capacity=1.0, SwitchFreq=10 (The Phase Boundary Transition)")
    
    exact_scores, lossy_scores = run_validation_scenario(seeds=100)
    
    mean_exact = np.mean(exact_scores)
    mean_lossy = np.mean(lossy_scores)
    
    print(f"\n1. Reproducibility & Paired Outcomes")
    print(f"Mean Exact Copying: {mean_exact:.4f}")
    print(f"Mean Lossy Teaching: {mean_lossy:.4f}")
    
    obs_diff, p_val, extreme_count = permutation_test(exact_scores, lossy_scores)
    
    print(f"\n2. Statistical Robustness (Sign-Flip Permutation Test)")
    print(f"Observed Mean Difference (Lossy - Exact): +{obs_diff:.4f}")
    print(f"Extreme permutations (out of 100,000): {extreme_count}")
    print(f"Monte Carlo p-value (plus-one estimator): p_MC = {p_val:.1e}")
    
    if p_val < 0.01 and obs_diff > 0.5:
        print("\n[PASS] Validation successful: Lossy teaching strongly outperforms exact copying under these constraints.")
        sys.exit(0)
    else:
        print("\n[FAIL] Results are not statistically significant or effect size is too small.")
        sys.exit(1)
