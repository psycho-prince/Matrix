import random
import numpy as np
import os

class EvolvableAgent:
    def __init__(self, rng: random.Random, capacity: float, trait_f: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = capacity 
        self.trait_f = trait_f  # Genetic trait: inheritance factor
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
        return self.tasks_succeeded / self.tasks_attempted

def generate_mixed_shifts():
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    shifts = set()
    current_gen = 0
    # Create a long enough sequence
    for i in (fib + pi_dig) * 5:
        current_gen += i
        shifts.add(current_gen)
    return shifts

def run_evolution(population_size=100, generations=200):
    shifts = generate_mixed_shifts()
    
    # Initialize population with random f traits uniformly from 0.0 to 1.0
    rng = random.Random(42)
    population = []
    
    # Each member is a tuple: (trait_f, skills_dict)
    for _ in range(population_size):
        population.append((rng.random(), {"A": 0.0, "B": 0.0}))
        
    capacity = 1.0
    current_skill = "A"
    
    history_f = []
    
    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"
            
        evaluated_agents = []
        
        # Evaluate current population
        for trait_f, parent_skills in population:
            # Create agent instance
            agent = EvolvableAgent(rng, capacity, trait_f)
            # Inherit skills using their specific genetic trait
            agent.skills = {k: v * trait_f for k, v in parent_skills.items()}
            
            # Live their life
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, num_tasks=20)
            
            evaluated_agents.append(agent)
            
        # Selection: Sort by fitness (success rate)
        evaluated_agents.sort(key=lambda a: a.fitness, reverse=True)
        
        # Keep top 50% as parents
        parents = evaluated_agents[:population_size // 2]
        
        next_population = []
        
        # Reproduction with mutation
        while len(next_population) < population_size:
            # Pick a random parent from the top 50%
            parent = rng.choice(parents)
            
            # Mutate the f trait slightly (Gaussian noise, std=0.05)
            child_f = parent.trait_f + rng.gauss(0, 0.05)
            child_f = max(0.0, min(1.0, child_f)) # clamp between 0 and 1
            
            next_population.append((child_f, parent.skills.copy()))
            
        population = next_population
        
        # Record stats
        mean_f = np.mean([p[0] for p in population])
        history_f.append(mean_f)
        
        if g % 20 == 0 or g == generations - 1:
            print(f"Generation {g:3d} | Mean Population 'f' trait: {mean_f:.4f}")
            
    return history_f

if __name__ == "__main__":
    print("=== Evolutionary Discovery of the Golden Ratio ===")
    print("Population: 100 agents.")
    print("Initialization: Random 'f' traits between 0.0 and 1.0.")
    print("Selection: Top 50% most successful agents reproduce.")
    print("Mutation: Offspring mutate their parent's 'f' trait slightly.\n")
    
    run_evolution(population_size=100, generations=300)
    
    print("\nEvolution complete.")
    print("Mathematical Golden Ratio (1/phi) = 0.6180")
