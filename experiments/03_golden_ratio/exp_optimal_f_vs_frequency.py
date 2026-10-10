import random
import numpy as np

class ConstrainedAgent:
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

def find_optimal_f_for_frequency(switch_freq, capacity=1.0, seeds=30, generations=40):
    factors = np.arange(0.10, 0.99, 0.02) # Sweep from 0.10 to 0.98 in steps of 0.02
    best_f = 0
    best_score = -1
    
    for f in factors:
        seed_means = []
        for seed in range(seeds):
            rng = random.Random(seed)
            parent_skills = {"A": 0.0, "B": 0.0}
            
            gen_scores = []
            
            for g in range(generations):
                active_skill = "A" if (g // switch_freq) % 2 == 0 else "B"
                
                agent = ConstrainedAgent(rng, capacity)
                agent.skills = {k: v * f for k, v in parent_skills.items()}
                
                agent.enforce_capacity()
                agent.learn(active_skill, 10)
                agent.work(active_skill, 0.4, num_tasks=20, record=True)
                
                parent_skills = agent.skills.copy()
                if g >= 10: # Post burn-in
                    gen_scores.append(agent.success_rate)
                
            seed_means.append(np.mean(gen_scores))
            
        mean_score = np.mean(seed_means)
        if mean_score > best_score:
            best_score = mean_score
            best_f = f
            
    return best_f, best_score

if __name__ == "__main__":
    frequencies = [1, 2, 3, 5, 8, 13, 20]
    
    print("=== Testing Optimal Inheritance Factor vs. Environmental Volatility ===")
    print("Does the Golden Ratio hold universally, or does the optimal 'forgetting' factor")
    print("depend on the exact length of the stability era?\n")
    
    print("Stability Era (Gens) | Optimal Retention Factor (f) | Max Success Rate")
    print("-" * 65)
    
    for freq in frequencies:
        opt_f, max_score = find_optimal_f_for_frequency(freq)
        print(f"       {freq:2d}            |            {opt_f:.2f}            |      {max_score:.4f}")

