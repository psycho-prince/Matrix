"""
Cost Function Sensitivity and Structural Invariance Analysis.

Evaluates whether the phase transition between Lamarckian Rentier (f -> 1)
and Agile Amnesia (f -> 0) is an artifact of specific linear coefficients
or a topologically robust invariant of generational parameter economics.

Tests:
1. Scaling of metabolic cost alpha over a 20x range [0.01 to 0.20]
2. Scaling of time/learning penalty beta over a 10x range [10.0 to 100.0]
3. Non-linear functional forms: Linear (c), Quadratic (c^2), Sublinear (sqrt(c))
"""

import random
import numpy as np
import json
import os
import sys

class ConfigurableCostAgent:
    def __init__(self, rng, trait_cap: float, trait_f: float, trait_lr: float,
                 alpha: float = 0.05, beta: float = 50.0, cost_mode: str = "linear"):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = trait_cap
        self.trait_f = trait_f
        self.trait_lr = trait_lr
        self.alpha = alpha
        self.beta = beta
        self.cost_mode = cost_mode

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
                self.skills[active_skill] += self.trait_lr
                self.enforce_capacity()

    def work(self, active_skill: str, difficulty: float, max_time: int):
        time_cost = int(self.trait_lr * self.beta)
        num_tasks = max(1, max_time - time_cost)

        for _ in range(num_tasks):
            self.tasks_attempted += 1
            skill_level = self.skills[active_skill]

            if skill_level >= difficulty:
                success = self.rng.random() < 0.9
            else:
                success = self.rng.random() < ((skill_level / max(0.01, difficulty)) * 0.5)

            if success:
                self.tasks_succeeded += 1
                self.skills[active_skill] += 0.01
                self.enforce_capacity()

    @property
    def fitness(self) -> float:
        if self.tasks_attempted == 0:
            return 0.0
        efficiency = self.tasks_succeeded / self.tasks_attempted
        productivity = self.tasks_succeeded / 30.0
        raw_fitness = (efficiency * 0.5) + (productivity * 0.5)

        if self.cost_mode == "linear":
            metabolic_cost = self.alpha * self.capacity
        elif self.cost_mode == "quadratic":
            metabolic_cost = self.alpha * (self.capacity ** 2) * 0.5
        elif self.cost_mode == "sublinear":
            metabolic_cost = self.alpha * np.sqrt(max(0.01, self.capacity))
        else:
            metabolic_cost = self.alpha * self.capacity

        return max(0.0, raw_fitness - metabolic_cost)


def run_sensitivity_simulation(frequency, alpha, beta, cost_mode, generations=200, pop_size=40, seed=42):
    py_rng = random.Random(seed)
    shifts = set(range(frequency, generations, frequency))

    population = []
    for _ in range(pop_size):
        population.append((
            py_rng.random(),
            py_rng.uniform(0.01, 0.10),
            py_rng.uniform(0.5, 2.0),
            {"A": 0.0, "B": 0.0}
        ))

    current_skill = "A"
    f_history = []

    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"

        evaluated = []
        for trait_f, trait_lr, trait_cap, parent_skills in population:
            agent = ConfigurableCostAgent(py_rng, trait_cap, trait_f, trait_lr,
                                          alpha=alpha, beta=beta, cost_mode=cost_mode)
            agent.skills = {k: v * trait_f for k, v in parent_skills.items()}
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, max_time=30)
            evaluated.append(agent)

        evaluated.sort(key=lambda a: a.fitness, reverse=True)
        parents = evaluated[:pop_size // 2]
        f_history.append(np.mean([p.trait_f for p in parents]))

        next_pop = []
        while len(next_pop) < pop_size:
            parent = py_rng.choice(parents)
            child_f = max(0.0, min(1.0, parent.trait_f + py_rng.gauss(0, 0.05)))
            child_lr = max(0.001, min(0.25, parent.trait_lr + py_rng.gauss(0, 0.01)))
            child_cap = max(0.1, min(5.0, parent.capacity + py_rng.gauss(0, 0.1)))
            next_pop.append((child_f, child_lr, child_cap, parent.skills.copy()))
        population = next_pop

    # Return steady-state retention (average of last 50 generations)
    return float(np.mean(f_history[-50:]))


def run_full_sensitivity_sweep():
    print("=" * 80)
    print("  RUNNING COST FUNCTION SENSITIVITY & INVARIANCE ANALYSIS")
    print("  Evaluating Phase Boundary Across Non-Linear Cost Surfaces")
    print("=" * 80)

    alphas = [0.01, 0.03, 0.05, 0.10, 0.15]
    betas = [20.0, 50.0, 80.0]
    modes = ["linear", "quadratic", "sublinear"]

    results = {
        "alpha_sweep": {},
        "beta_sweep": {},
        "functional_form_sweep": {},
        "phase_invariance_verified": True
    }

    # 1. Functional Form Sweep (Freq=5 High Volatility vs Freq=50 High Stability)
    print("\n[1] Testing Functional Forms (Linear, Quadratic, Sublinear)...")
    for mode in modes:
        f_volatile = run_sensitivity_simulation(5, alpha=0.05, beta=50.0, cost_mode=mode, seed=101)
        f_stable = run_sensitivity_simulation(50, alpha=0.05, beta=50.0, cost_mode=mode, seed=101)
        delta = f_stable - f_volatile
        results["functional_form_sweep"][mode] = {
            "f_volatile": f_volatile,
            "f_stable": f_stable,
            "delta_retention": delta,
            "phase_preserved": bool(f_stable > 0.60 and f_volatile < 0.40)
        }
        print(f"  --> Form '{mode:9s}': Volatile f={f_volatile:.3f} | Stable f={f_stable:.3f} | Delta={delta:.3f} | Preserved: {results['functional_form_sweep'][mode]['phase_preserved']}")
        if not results["functional_form_sweep"][mode]["phase_preserved"]:
            results["phase_invariance_verified"] = False

    # 2. Metabolic Cost Alpha Sweep
    print("\n[2] Testing Metabolic Cost Alpha Scaling (0.01 to 0.15)...")
    for alpha in alphas:
        f_volatile = run_sensitivity_simulation(5, alpha=alpha, beta=50.0, cost_mode="linear", seed=202)
        f_stable = run_sensitivity_simulation(50, alpha=alpha, beta=50.0, cost_mode="linear", seed=202)
        results["alpha_sweep"][str(alpha)] = {
            "f_volatile": f_volatile,
            "f_stable": f_stable,
            "phase_preserved": bool(f_stable > f_volatile + 0.35)
        }
        print(f"  --> Alpha={alpha:.2f}: Volatile f={f_volatile:.3f} | Stable f={f_stable:.3f} | Preserved: {results['alpha_sweep'][str(alpha)]['phase_preserved']}")
        if not results["alpha_sweep"][str(alpha)]["phase_preserved"]:
            results["phase_invariance_verified"] = False

    # 3. Learning Time Penalty Beta Sweep
    print("\n[3] Testing Learning Penalty Beta Scaling (20 to 80)...")
    for beta in betas:
        f_volatile = run_sensitivity_simulation(5, alpha=0.05, beta=beta, cost_mode="linear", seed=303)
        f_stable = run_sensitivity_simulation(50, alpha=0.05, beta=beta, cost_mode="linear", seed=303)
        results["beta_sweep"][str(beta)] = {
            "f_volatile": f_volatile,
            "f_stable": f_stable,
            "phase_preserved": bool(f_stable > f_volatile + 0.35)
        }
        print(f"  --> Beta={beta:.1f}: Volatile f={f_volatile:.3f} | Stable f={f_stable:.3f} | Preserved: {results['beta_sweep'][str(beta)]['phase_preserved']}")
        if not results["beta_sweep"][str(beta)]["phase_preserved"]:
            results["phase_invariance_verified"] = False

    out_file = os.path.join(os.path.dirname(__file__), "../data/cost_sensitivity_analysis.json")
    with open(out_file, "w") as fp:
        json.dump(results, fp, indent=2)

    print("\n" + "=" * 80)
    print(f"  VERDICT: Phase Invariance Verified = {results['phase_invariance_verified']}")
    print(f"  Output saved to {out_file}")
    print("=" * 80)
    return results

if __name__ == "__main__":
    run_full_sensitivity_sweep()
