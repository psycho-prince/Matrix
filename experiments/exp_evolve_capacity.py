import random
import numpy as np

class VariableCapacityAgent:
    def __init__(self, rng: random.Random, trait_cap: float, trait_f: float, trait_lr: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = trait_cap 
        self.trait_f = trait_f    
        self.trait_lr = trait_lr  
        
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

    def work(self, active_skill: str, difficulty: float, num_tasks: int):
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
        if self.tasks_attempted == 0: return 0.0
        base_fitness = self.tasks_succeeded / self.tasks_attempted
        # Small metabolic cost to maintaining large capacity brain
        metabolic_cost = self.capacity * 0.05
        return max(0.0, base_fitness - metabolic_cost)

def generate_mixed_shifts():
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    shifts = set()
    current_gen = 0
    for i in (fib + pi_dig) * 5:
        current_gen += i
        shifts.add(current_gen)
    return shifts

def run_capacity_experiment(population_size=100, generations=300):
    shifts = generate_mixed_shifts()
    rng = random.Random(42)
    
    population = []
    for _ in range(population_size):
        # f, lr, cap, skills
        population.append((rng.random(), rng.uniform(0.01, 0.10), rng.uniform(0.5, 2.0), {"A": 0.0, "B": 0.0}))
        
    current_skill = "A"
    
    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"
            
        evaluated = []
        for trait_f, trait_lr, trait_cap, parent_skills in population:
            agent = VariableCapacityAgent(rng, trait_cap, trait_f, trait_lr)
            agent.skills = {k: v * trait_f for k, v in parent_skills.items()}
            
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, num_tasks=20)
            
            evaluated.append(agent)
            
        evaluated.sort(key=lambda a: a.fitness, reverse=True)
        parents = evaluated[:population_size // 2]
        
        next_pop = []
        while len(next_pop) < population_size:
            parent = rng.choice(parents)
            child_f = max(0.0, min(1.0, parent.trait_f + rng.gauss(0, 0.05)))
            child_lr = max(0.001, min(0.25, parent.trait_lr + rng.gauss(0, 0.01)))
            child_cap = max(0.1, min(5.0, parent.capacity + rng.gauss(0, 0.1)))
            next_pop.append((child_f, child_lr, child_cap, parent.skills.copy()))
            
        population = next_pop
        
        if g % 50 == 0 or g == generations - 1:
            mean_f = np.mean([p[0] for p in population])
            mean_lr = np.mean([p[1] for p in population])
            mean_cap = np.mean([p[2] for p in population])
            print(f"Gen {g:3d} | Mean f: {mean_f:.4f} | Mean lr: {mean_lr:.4f} | Mean cap: {mean_cap:.4f}")
            
if __name__ == "__main__":
    print("=== Co-Evolution of Capacity, Retention, and Learning Rate ===")
    run_capacity_experiment()
