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

def generate_pi_shifts():
    # First 50 digits of Pi
    pi_digits = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9, 5, 0, 2, 8, 8, 4, 1, 9, 7, 1, 6, 9, 3, 9, 9, 3, 7, 5, 1]
    
    shifts = set()
    current_gen = 0
    for d in pi_digits:
        if d == 0:
            continue
        current_gen += d
        shifts.add(current_gen)
        
    return shifts, current_gen

def test_inheritance_factor(factor, shift_gens, max_gen, capacity=1.0, seeds=50):
    seed_means = []
    
    for seed in range(seeds):
        rng = random.Random(seed)
        parent_skills = {"A": 0.0, "B": 0.0}
        current_skill = "A"
        
        gen_scores = []
        
        for g in range(max_gen):
            if g in shift_gens:
                current_skill = "B" if current_skill == "A" else "A"
                
            agent = ConstrainedAgent(rng, capacity)
            agent.skills = {k: v * factor for k, v in parent_skills.items()}
            
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, num_tasks=20, record=True)
            
            parent_skills = agent.skills.copy()
            gen_scores.append(agent.success_rate)
            
        seed_means.append(np.mean(gen_scores))
        
    return np.mean(seed_means)

if __name__ == "__main__":
    shifts, max_gen = generate_pi_shifts()
    
    PHI = 1.6180339887
    INV_PHI = 1.0 / PHI
    INV_PI = 1.0 / np.pi
    
    factors_to_test = [0.0, 0.1, 0.2, 0.3, INV_PI, 0.4, 0.5, 0.6, INV_PHI, 0.7, 0.8, 0.9, 1.0]
    
    print("=== Testing Optimal Inheritance Factor in a Pi-Volatility Environment ===")
    print("The environment shifts at intervals matching the digits of Pi:")
    print("3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5...")
    print(f"Sweeping factors, including 1/phi ({INV_PHI:.3f}) and 1/pi ({INV_PI:.3f})\n")
    
    results = {}
    for f in factors_to_test:
        score = test_inheritance_factor(f, shifts, max_gen)
        results[f] = score
        
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("Inheritance Factor | Mean Lifetime Success")
    print("-" * 55)
    for f, score in sorted_results:
        label = ""
        if abs(f - INV_PHI) < 0.001:
            label = " <-- Golden Ratio (1/phi)"
        elif abs(f - INV_PI) < 0.001:
            label = " <-- Inverse Pi (1/pi)"
        elif f == 0.5:
            label = " <-- Standard Lossy (50%)"
        elif f == 1.0:
            label = " <-- Exact Copying (100%)"
            
        print(f"      {f:.3f}        |        {score:.4f} {label}")
