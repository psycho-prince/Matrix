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
    # Generates a list of generations where a shift occurs
    shifts = []
    a, b = 1, 1
    current_gen = 0
    while current_gen < max_generations:
        current_gen += a
        if current_gen < max_generations:
            shifts.append(current_gen)
        a, b = b, a + b
    return shifts

def run_fibonacci_environment(capacity=1.0, seeds=100, generations=60):
    modes = ['Exact', 'Lossy']
    shift_gens = generate_fibonacci_shifts(generations)
    
    # Store history of success per generation
    history = {m: {g: [] for g in range(generations)} for m in modes}
    
    for seed in range(seeds):
        rngs = {m: random.Random(seed) for m in modes}
        parent_skills = {m: {"A": 0.0, "B": 0.0} for m in modes}
        
        current_skill = "A"
        
        for g in range(generations):
            if g in shift_gens:
                current_skill = "B" if current_skill == "A" else "A"
                
            difficulty = 0.4
            
            for m in modes:
                agent = ConstrainedAgent(rngs[m], capacity)
                
                if m == 'Exact':
                    agent.skills = parent_skills[m].copy()
                elif m == 'Lossy':
                    agent.skills = {k: v * 0.5 for k, v in parent_skills[m].items()}
                    
                agent.enforce_capacity()
                agent.learn(current_skill, 10)
                agent.work(current_skill, difficulty, num_tasks=20, record=True)
                
                parent_skills[m] = agent.skills.copy()
                history[m][g].append(agent.success_rate)
                
    return history, shift_gens

if __name__ == "__main__":
    generations = 60
    print("=== Testing Fibonacci Volatility ===")
    print("The environment shifts at Fibonacci intervals: 1, 1, 2, 3, 5, 8, 13, 21...")
    print("This models an environment that starts highly volatile and gradually stabilizes.")
    print("Capacity is bounded to 1.0\n")
    
    history, shifts = run_fibonacci_environment(capacity=1.0, seeds=100, generations=generations)
    
    print("Generation | Active | Exact Succ | Lossy Succ | Advantage (Lossy - Exact)")
    print("-" * 75)
    
    current_skill = "A"
    
    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"
            
        exact_mean = np.mean(history['Exact'][g])
        lossy_mean = np.mean(history['Lossy'][g])
        diff = lossy_mean - exact_mean
        
        # Only print some generations to avoid spamming the console
        # Print shifts, generations near shifts, and the end
        if g in shifts or (g-1) in shifts or g % 10 == 0 or g == generations - 1:
            marker = "*" if g in shifts else " "
            print(f"Gen {g:2d} {marker}  |   {current_skill}    |   {exact_mean:.4f}   |   {lossy_mean:.4f}   |   {diff:+.4f}")

