import random
import numpy as np

class UltimateAgent:
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

    def work(self, active_skill: str, difficulty: float, max_time: int):
        # Time cost for learning faster (moderate penalty, factor=50)
        time_cost = int(self.trait_lr * 50)
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
        if self.tasks_attempted == 0: return 0.0
        
        # Base efficiency
        efficiency = self.tasks_succeeded / self.tasks_attempted
        
        # Absolute productivity (max possible tasks = max_time)
        productivity = self.tasks_succeeded / 30.0 
        
        raw_fitness = (efficiency * 0.5) + (productivity * 0.5)
        
        # Metabolic cost to maintaining large capacity brain
        metabolic_cost = self.capacity * 0.05
        
        return max(0.0, raw_fitness - metabolic_cost)


def generate_periodic_shifts(frequency, max_gen):
    shifts = set()
    for i in range(frequency, max_gen, frequency):
        shifts.add(i)
    return shifts

def generate_chaotic_shifts(max_gen):
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    shifts = set()
    current_gen = 0
    while current_gen < max_gen:
        for i in (fib + pi_dig):
            current_gen += i
            if current_gen < max_gen:
                shifts.add(current_gen)
    return shifts

def run_joint_experiment(shift_mode, frequency=None, population_size=100, generations=500):
    if shift_mode == "periodic":
        shifts = generate_periodic_shifts(frequency, generations)
    else:
        shifts = generate_chaotic_shifts(generations)
        
    rng = random.Random(42 + (frequency if frequency else 0))
    
    population = []
    for _ in range(population_size):
        # Initial traits: f=random, lr=random(low), cap=1.0
        population.append((rng.random(), rng.uniform(0.01, 0.10), rng.uniform(0.5, 2.0), {"A": 0.0, "B": 0.0}))
        
    current_skill = "A"
    
    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"
            
        evaluated = []
        for trait_f, trait_lr, trait_cap, parent_skills in population:
            agent = UltimateAgent(rng, trait_cap, trait_f, trait_lr)
            agent.skills = {k: v * trait_f for k, v in parent_skills.items()}
            
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, max_time=30)
            
            evaluated.append(agent)
            
        evaluated.sort(key=lambda a: a.fitness, reverse=True)
        parents = evaluated[:population_size // 2]
        
        next_pop = []
        while len(next_pop) < population_size:
            parent = rng.choice(parents)
            
            # Mutate traits
            child_f = max(0.0, min(1.0, parent.trait_f + rng.gauss(0, 0.05)))
            child_lr = max(0.001, min(0.25, parent.trait_lr + rng.gauss(0, 0.01)))
            child_cap = max(0.1, min(5.0, parent.capacity + rng.gauss(0, 0.1)))
            
            next_pop.append((child_f, child_lr, child_cap, parent.skills.copy()))
            
        population = next_pop
        
    # Average over last 50 generations to smooth out volatility
    # We will just return the final population means for simplicity,
    # as the population size provides some averaging.
    mean_f = np.mean([p[0] for p in population])
    mean_lr = np.mean([p[1] for p in population])
    mean_cap = np.mean([p[2] for p in population])
    
    return mean_f, mean_lr, mean_cap

if __name__ == "__main__":
    print("=== Joint Evolution Under Varying Environmental Volatility ===")
    print("Agents co-evolve Retention (f), Learning Rate (lr), and Capacity (cap)")
    print("with a moderate cost applied to both high learning and large capacity.")
    print("-" * 80)
    print("Environment          | Shift Freq  | Retention (f) | Learn Rate (lr) | Capacity")
    print("-" * 80)
    
    scenarios = [
        ("Hyper-Volatile", "periodic", 2),
        ("Highly Volatile", "periodic", 5),
        ("Chaotic (Fib/Pi)", "chaotic", None),
        ("Moderately Volatile", "periodic", 20),
        ("Stable", "periodic", 50),
        ("Hyper-Stable", "periodic", 200)
    ]
    
    for name, mode, freq in scenarios:
        f, lr, cap = run_joint_experiment(mode, freq, generations=800)
        freq_str = str(freq) if freq else "Mixed"
        print(f"{name:<20} | {freq_str:<11} | {f:<13.4f} | {lr:<15.4f} | {cap:.4f}")

