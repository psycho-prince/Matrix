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

def generate_ultimate_shifts():
    # Mix Fibonacci, Pi, and Primes
    fib = [1, 1, 2, 3, 5, 8, 13]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    primes = [2, 3, 5, 7, 11, 13, 17]
    
    intervals = fib + pi_dig + primes
    
    shifts = set()
    current_gen = 0
    for i in intervals:
        current_gen += i
        shifts.add(current_gen)
        
    return shifts, current_gen

def adaptive_retention(era_length):
    # Based on our previous discovery: 1 gen -> ~0.78, 20 gens -> ~0.44
    # We fit a simple linear bound: f = 0.80 - 0.018 * era_length
    f = 0.80 - (0.018 * era_length)
    return max(0.30, min(0.95, f))

def run_ultimate_simulation(capacity=1.0, seeds=100):
    shifts, max_generations = generate_ultimate_shifts()
    
    modes = ['Exact', 'Lossy_50', 'Golden_Ratio', 'Rational_3_5', 'Adaptive_Law']
    history = {m: [] for m in modes}
    
    for seed in range(seeds):
        rngs = {m: random.Random(seed) for m in modes}
        parent_skills = {m: {"A": 0.0, "B": 0.0} for m in modes}
        
        current_skill = "A"
        era_length = 0
        
        gen_scores = {m: [] for m in modes}
        
        for g in range(max_generations):
            if g in shifts:
                current_skill = "B" if current_skill == "A" else "A"
                # Shift occurred, calculate how long the era was for the Adaptive agent
                era_length_for_shift = era_length
                era_length = 0 # reset for the new era
            else:
                era_length_for_shift = era_length
                era_length += 1
                
            for m in modes:
                agent = ConstrainedAgent(rngs[m], capacity)
                
                # Determine inheritance factor
                if m == 'Exact':
                    f = 1.0
                elif m == 'Lossy_50':
                    f = 0.5
                elif m == 'Golden_Ratio':
                    f = 0.618
                elif m == 'Rational_3_5':
                    f = 0.600
                elif m == 'Adaptive_Law':
                    # The adaptive law only drops memory drastically when a shift actually occurs.
                    # If it's a stable generation, it retains 100% to keep performing well.
                    if g in shifts:
                        f = adaptive_retention(era_length_for_shift)
                    else:
                        f = 1.0
                
                # Apply inheritance
                agent.skills = {k: v * f for k, v in parent_skills[m].items()}
                
                agent.enforce_capacity()
                agent.learn(current_skill, 10)
                agent.work(current_skill, 0.4, num_tasks=20, record=True)
                
                parent_skills[m] = agent.skills.copy()
                gen_scores[m].append(agent.success_rate)
                
        for m in modes:
            history[m].append(np.mean(gen_scores[m]))
            
    return {m: np.mean(history[m]) for m in modes}

if __name__ == "__main__":
    print("=== The Ultimate Law Simulation ===")
    print("Volatility Sequence: Fibonacci -> Pi -> Primes (Hyper-chaotic mixed sequence)")
    print("Agent Strategies Racing:")
    print("1. Exact Copying (100% Retention)")
    print("2. Standard Lossy (50% Fixed Retention)")
    print("3. Rational 3/5 (60.0% Fixed Retention)")
    print("4. Golden Ratio (61.8% Fixed Retention)")
    print("5. Adaptive Law (Retention scales inversely with stability era length)\n")
    
    results = run_ultimate_simulation(capacity=1.0, seeds=100)
    
    sorted_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("Strategy             | Mean Lifetime Success (150+ Generations)")
    print("-" * 65)
    for m, score in sorted_res:
        print(f"{m:20s} | {score:.4f}")
