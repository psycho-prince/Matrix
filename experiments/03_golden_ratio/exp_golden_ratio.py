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

def generate_fibonacci_shifts(max_generations):
    shifts = []
    a, b = 1, 1
    current_gen = 0
    while current_gen < max_generations:
        current_gen += a
        if current_gen < max_generations:
            shifts.append(current_gen)
        a, b = b, a + b
    return shifts

def test_inheritance_factor(factor, shift_gens, capacity=1.0, seeds=100, generations=88):
    seed_means = []
    
    for seed in range(seeds):
        rng = random.Random(seed)
        parent_skills = {"A": 0.0, "B": 0.0}
        current_skill = "A"
        
        gen_scores = []
        
        for g in range(generations):
            if g in shift_gens:
                current_skill = "B" if current_skill == "A" else "A"
                
            agent = ConstrainedAgent(rng, capacity)
            # Apply the inheritance factor (0.0 to 1.0)
            agent.skills = {k: v * factor for k, v in parent_skills.items()}
            
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, num_tasks=20, record=True)
            
            parent_skills = agent.skills.copy()
            gen_scores.append(agent.success_rate)
            
        seed_means.append(np.mean(gen_scores))
        
    return np.mean(seed_means)

if __name__ == "__main__":
    generations = 88 # 1+1+2+3+5+8+13+21+34
    shifts = generate_fibonacci_shifts(generations)
    
    PHI = 1.6180339887
    INV_PHI = 1.0 / PHI # approx 0.618
    INV_PHI_SQ = 1.0 / (PHI * PHI) # approx 0.382
    
    factors_to_test = [0.0, 0.1, 0.2, 0.3, INV_PHI_SQ, 0.4, 0.5, 0.6, INV_PHI, 0.7, 0.8, 0.9, 1.0]
    
    print("=== Testing Optimal Inheritance Factor in a Fibonacci Environment ===")
    print("Sweeping inheritance factors from 0.0 (Blank Slate) to 1.0 (Exact Copy).")
    print(f"Including Golden Ratio conjugates: {INV_PHI_SQ:.3f} and {INV_PHI:.3f}\n")
    
    results = {}
    for f in factors_to_test:
        score = test_inheritance_factor(f, shifts, generations=generations)
        results[f] = score
        
    # Sort by performance
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("Inheritance Factor | Mean Lifetime Success (across 88 gens)")
    print("-" * 65)
    for f, score in sorted_results:
        label = ""
        if abs(f - INV_PHI) < 0.001:
            label = " <-- Golden Ratio (1/phi)"
        elif abs(f - INV_PHI_SQ) < 0.001:
            label = " <-- Golden Ratio (1/phi^2)"
        elif f == 0.5:
            label = " <-- Standard Lossy (50%)"
        elif f == 1.0:
            label = " <-- Exact Copying (100%)"
            
        print(f"      {f:.3f}        |        {score:.4f} {label}")
