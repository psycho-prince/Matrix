import random
import numpy as np
import pandas as pd
import os

class ConstrainedAgent:
    def __init__(self, rng: random.Random, capacity: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = capacity 
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def get_total_skill(self):
        return sum(self.skills.values())

    def enforce_capacity(self):
        total = self.get_total_skill()
        if total > self.capacity:
            for k in self.skills:
                self.skills[k] = self.skills[k] * (self.capacity / total)

    def learn(self, active_skill: str, steps: int):
        for _ in range(steps):
            if self.get_total_skill() < self.capacity:
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

def evaluate_condition(capacity, switch_freq, seeds=50, generations=20):
    modes = ['Exact', 'Lossy']
    
    # Store the average success rate of generations 10-19 for each seed
    seed_means = {m: [] for m in modes}
    
    for seed in range(seeds):
        rngs = {m: random.Random(seed) for m in modes}
        parent_skills = {m: {"A": 0.0, "B": 0.0} for m in modes}
        
        gen_scores = {m: [] for m in modes}
        
        for g in range(generations):
            active_skill = "A" if (g // switch_freq) % 2 == 0 else "B"
            difficulty = 0.4
            # Always record to compute the moving average
            record = True
            
            for m in modes:
                agent = ConstrainedAgent(rngs[m], capacity)
                
                if m == 'Exact':
                    agent.skills = parent_skills[m].copy()
                elif m == 'Lossy':
                    agent.skills = {k: v * 0.5 for k, v in parent_skills[m].items()}
                    
                agent.enforce_capacity()
                agent.learn(active_skill, 10)
                agent.work(active_skill, difficulty, num_tasks=20, record=record)
                
                parent_skills[m] = agent.skills.copy()
                
                if g >= 10: # Only average the last 10 generations (burn-in period)
                    gen_scores[m].append(agent.success_rate)
                    
        for m in modes:
            seed_means[m].append(np.mean(gen_scores[m]))
                    
    mean_exact = np.mean(seed_means['Exact'])
    mean_lossy = np.mean(seed_means['Lossy'])
    
    return mean_exact, mean_lossy

if __name__ == "__main__":
    capacities = [0.2, 0.5, 0.8, 1.0, 1.5, 2.0]
    switch_freqs = [1, 2, 3, 5, 10, 20] # 20 means no switch
    
    records = []
    
    print("Running parameter sweep... (this may take a few seconds)")
    
    for cap in capacities:
        for freq in switch_freqs:
            exact_val, lossy_val = evaluate_condition(cap, freq, seeds=50, generations=20)
            advantage_lossy = lossy_val - exact_val
            records.append({
                "Capacity": cap,
                "SwitchFreq": freq,
                "Exact_Mean": exact_val,
                "Lossy_Mean": lossy_val,
                "Lossy_Advantage": advantage_lossy
            })
            
    df = pd.DataFrame(records)
    
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/parameter_sweep.csv", index=False)
    
    pivot = df.pivot(index="Capacity", columns="SwitchFreq", values="Lossy_Advantage")
    print("\nPhase Boundary: Lossy Advantage over Exact Copying")
    print("(Positive values mean Lossy is better, Negative means Exact is better)")
    print("-" * 70)
    print(pivot.round(3))
    print("-" * 70)
    print("\nSweep complete. Raw data saved to results/parameter_sweep.csv.")
