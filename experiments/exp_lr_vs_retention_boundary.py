import random
import numpy as np

class EvolvableAgent:
    def __init__(self, rng: random.Random, capacity: float, trait_f: float, fixed_lr: float):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = capacity 
        self.trait_f = trait_f  
        self.fixed_lr = fixed_lr  
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
                self.skills[active_skill] += self.fixed_lr
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
    for i in (fib + pi_dig) * 10: # extended for longer runs
        current_gen += i
        shifts.add(current_gen)
    return shifts

def run_evolution_for_lr(fixed_lr, population_size=100, generations=300, seeds=5):
    shifts = generate_mixed_shifts()
    final_f_means = []
    
    for seed in range(seeds):
        rng = random.Random(seed)
        population = [(rng.random(), {"A": 0.0, "B": 0.0}) for _ in range(population_size)]
        capacity = 1.0
        current_skill = "A"
        
        for g in range(generations):
            if g in shifts:
                current_skill = "B" if current_skill == "A" else "A"
                
            evaluated = []
            for trait_f, parent_skills in population:
                agent = EvolvableAgent(rng, capacity, trait_f, fixed_lr)
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
                next_pop.append((child_f, parent.skills.copy()))
                
            population = next_pop
            
        # Average the last 20 generations to smooth out the final-generation volatility shock
        # Actually, let's just take the mean of the final generation for this seed
        final_f_means.append(np.mean([p[0] for p in population]))
        
    return np.mean(final_f_means), np.std(final_f_means)

if __name__ == "__main__":
    print("=== Mapping the Disappearance of the Golden Ratio Attractor ===")
    print("Sweeping fixed learning rates to find where parental memory becomes a liability.")
    print("Each LR is tested over 5 independent seeds, 300 generations each.\n")
    
    learning_rates = [0.01, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20]
    
    print("Fixed LR | Potential Skill/Gen | Evolved Retention (f) | Std Dev")
    print("-" * 70)
    
    for lr in learning_rates:
        # 10 steps of learning
        potential_skill = lr * 10
        mean_f, std_f = run_evolution_for_lr(lr, seeds=5, generations=300)
        
        marker = ""
        if abs(mean_f - 0.618) < 0.05:
            marker = "  <-- Golden Ratio Basin"
            
        print(f"  {lr:.2f}   |        {potential_skill:.1f}        |       {mean_f:.4f}        |  {std_f:.4f} {marker}")
