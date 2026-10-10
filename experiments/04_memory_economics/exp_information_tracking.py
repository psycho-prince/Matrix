import random
import numpy as np

class InfoTrackingAgent:
    def __init__(self, rng: random.Random, capacity: float, trait_f: float, trait_lr: float):
        self.rng = rng
        # Track inherited vs learned bits for each skill
        self.skills = {"A": {"inherited": 0.0, "learned": 0.0}, "B": {"inherited": 0.0, "learned": 0.0}}
        self.capacity = capacity 
        self.trait_f = trait_f    
        self.trait_lr = trait_lr  
        
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def enforce_capacity(self):
        total = sum(s["inherited"] + s["learned"] for s in self.skills.values())
        if total > self.capacity:
            scale = self.capacity / total
            for k in self.skills:
                self.skills[k]["inherited"] *= scale
                self.skills[k]["learned"] *= scale

    def learn(self, active_skill: str, steps: int):
        for _ in range(steps):
            if sum(s["inherited"] + s["learned"] for s in self.skills.values()) < self.capacity:
                self.skills[active_skill]["learned"] += self.trait_lr
                self.enforce_capacity()

    def work(self, active_skill: str, difficulty: float, num_tasks: int):
        for _ in range(num_tasks):
            self.tasks_attempted += 1
            skill_level = self.skills[active_skill]["inherited"] + self.skills[active_skill]["learned"]
            
            if skill_level >= difficulty:
                success = self.rng.random() < 0.9
            else:
                success = self.rng.random() < ((skill_level / max(0.01, difficulty)) * 0.5)
                
            if success:
                self.tasks_succeeded += 1
                self.skills[active_skill]["learned"] += 0.01
                self.enforce_capacity()

    @property
    def fitness(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted

    def get_total_skill(self, skill_name):
        return self.skills[skill_name]["inherited"] + self.skills[skill_name]["learned"]

def generate_mixed_shifts():
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    shifts = set()
    current_gen = 0
    for i in (fib + pi_dig) * 5:
        current_gen += i
        shifts.add(current_gen)
    return shifts

def run_tracking_experiment(population_size=100, generations=300):
    shifts = generate_mixed_shifts()
    rng = random.Random(42)
    
    # Population format: (trait_f, trait_lr, parent_skills)
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
            agent = InfoTrackingAgent(rng, capacity, trait_f, trait_lr)
            # Inherit
            agent.skills["A"]["inherited"] = parent_skills["A"] * trait_f
            agent.skills["B"]["inherited"] = parent_skills["B"] * trait_f
            
            agent.enforce_capacity()
            agent.learn(current_skill, 10)
            agent.work(current_skill, 0.4, num_tasks=20)
            
            evaluated.append(agent)
            
        evaluated.sort(key=lambda a: a.fitness, reverse=True)
        parents = evaluated[:population_size // 2]
        
        # Track stats for top half (the survivors)
        total_inherited = sum(sum(s["inherited"] for s in p.skills.values()) for p in parents)
        total_learned = sum(sum(s["learned"] for s in p.skills.values()) for p in parents)
        total_content = total_inherited + total_learned
        
        pct_inherited = (total_inherited / total_content) * 100 if total_content > 0 else 0
        pct_learned = (total_learned / total_content) * 100 if total_content > 0 else 0
        
        next_pop = []
        while len(next_pop) < population_size:
            parent = rng.choice(parents)
            child_f = max(0.0, min(1.0, parent.trait_f + rng.gauss(0, 0.05)))
            child_lr = max(0.001, min(0.15, parent.trait_lr + rng.gauss(0, 0.01)))
            
            parent_skills = {
                "A": parent.get_total_skill("A"),
                "B": parent.get_total_skill("B")
            }
            next_pop.append((child_f, child_lr, parent_skills))
            
        population = next_pop
        
        if g % 50 == 0 or g == generations - 1:
            mean_f = np.mean([p[0] for p in population])
            mean_lr = np.mean([p[1] for p in population])
            print(f"Gen {g:3d} | f: {mean_f:.4f} | lr: {mean_lr:.4f} | Information Source: {pct_inherited:.1f}% inherited, {pct_learned:.1f}% learned")

if __name__ == "__main__":
    print("=== Tracking the Source of Information in Agent Brains ===")
    run_tracking_experiment()
