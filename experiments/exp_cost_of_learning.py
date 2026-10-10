import random
import numpy as np

class CostlyLearningAgent:
    def __init__(self, rng: random.Random, capacity: float, trait_f: float, trait_lr: float, penalty_factor: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = capacity 
        self.trait_f = trait_f    
        self.trait_lr = trait_lr  
        self.penalty_factor = penalty_factor
        
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
        # Time cost for learning faster: 
        # e.g., if penalty_factor=100 and lr=0.10, cost is 10 time units
        time_cost = int(self.trait_lr * self.penalty_factor)
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
        # Incorporate total tasks accomplished as part of fitness
        # so losing time to high LR hurts absolute productivity.
        efficiency = self.tasks_succeeded / self.tasks_attempted
        productivity = self.tasks_succeeded / 30.0 # max possible
        return efficiency * 0.5 + productivity * 0.5

def generate_mixed_shifts():
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    shifts = set()
    current_gen = 0
    for i in (fib + pi_dig) * 5:
        current_gen += i
        shifts.add(current_gen)
    return shifts

def run_cost_experiment(penalty_factor, population_size=100, generations=300):
    shifts = generate_mixed_shifts()
    rng = random.Random(42 + int(penalty_factor))
    
    population = []
    for _ in range(population_size):
        population.append((rng.random(), rng.uniform(0.01, 0.10), {"A": 0.0, "B": 0.0}))
        
    capacity = 1.0
    current_skill = "A"
    
    for g in range(generations):
        if g in shifts:
            current_skill = "B" if current_skill == "A" else "A"
            
        evaluated = []
        for trait_f, trait_lr, parent_skills in population:
            agent = CostlyLearningAgent(rng, capacity, trait_f, trait_lr, penalty_factor)
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
            child_f = max(0.0, min(1.0, parent.trait_f + rng.gauss(0, 0.05)))
            child_lr = max(0.001, min(0.25, parent.trait_lr + rng.gauss(0, 0.01)))
            next_pop.append((child_f, child_lr, parent.skills.copy()))
            
        population = next_pop
        
    mean_f = np.mean([p[0] for p in population])
    mean_lr = np.mean([p[1] for p in population])
    return mean_f, mean_lr

if __name__ == "__main__":
    print("=== Evolving Retention with a Cost on Learning Rate ===")
    print("Penalty Multiplier | Final Retention (f) | Final Learning Rate (lr)")
    print("-" * 70)
    for penalty in [0, 50, 100, 150, 200]:
        f, lr = run_cost_experiment(penalty)
        print(f"       {penalty:<11} |        {f:.4f}         |        {lr:.4f}")
