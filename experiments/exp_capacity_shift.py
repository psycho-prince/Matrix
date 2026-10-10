import random
import numpy as np

class ShiftingAgent:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.skills = {"logic": 0.0, "foraging": 0.0}
        self.capacity = 1.0 # Total maximum skill capacity
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def get_total_skill(self):
        return sum(self.skills.values())

    def enforce_capacity(self):
        total = self.get_total_skill()
        if total > self.capacity:
            # Scale down all skills to fit capacity
            for k in self.skills:
                self.skills[k] = self.skills[k] * (self.capacity / total)

    def learn(self, active_skill: str, steps: int):
        for _ in range(steps):
            if self.get_total_skill() < self.capacity:
                self.skills[active_skill] += self.rng.uniform(0.01, 0.05)
                self.enforce_capacity()

    def work(self, active_skill: str, difficulty: float, num_tasks: int = 20):
        for _ in range(num_tasks):
            self.tasks_attempted += 1
            skill_level = self.skills[active_skill]
            
            # Attempt task
            if skill_level >= difficulty:
                success = self.rng.random() < 0.9
            else:
                success = self.rng.random() < ((skill_level / max(0.01, difficulty)) * 0.5)
                
            if success:
                self.tasks_succeeded += 1
                self.skills[active_skill] += 0.01
                self.enforce_capacity()

    @property
    def success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted

def run_shifting_environment(seeds=100, generations=20):
    b_scores = []
    c_scores = []
    
    for seed in range(seeds):
        rng_b = random.Random(seed)
        rng_c = random.Random(seed)
        
        b_parent_skills = {"logic": 0.0, "foraging": 0.0}
        c_parent_skills = {"logic": 0.0, "foraging": 0.0}
        
        for g in range(generations):
            # Environment shifts every 5 generations
            active_skill = "logic" if (g // 5) % 2 == 0 else "foraging"
            difficulty = 0.4
            
            # --- B-copy Agent ---
            b_agent = ShiftingAgent(rng_b)
            # Exact copy fills capacity with potentially obsolete skills
            b_agent.skills = b_parent_skills.copy() 
            
            # --- C-full (Teaching) Agent ---
            c_agent = ShiftingAgent(rng_c)
            # Teaching only transfers the currently useful skill, allowing child to discard obsolete knowledge
            # (or it transfers with error, so child has more free capacity to learn new things)
            # Let's say teaching is "lossy", so child gets 50% of parent's skills, freeing capacity
            c_agent.skills = {k: v * 0.5 for k, v in c_parent_skills.items()}
            
            b_agent.learn(active_skill, 10)
            c_agent.learn(active_skill, 10)
            
            b_agent.work(active_skill, difficulty)
            c_agent.work(active_skill, difficulty)
            
            b_parent_skills = b_agent.skills
            c_parent_skills = c_agent.skills
            
            if g == generations - 1:
                b_scores.append(b_agent.success_rate)
                c_scores.append(c_agent.success_rate)
                
    return np.mean(b_scores), np.mean(c_scores)

if __name__ == "__main__":
    print("Testing Hypothesis: Cost of Copying in a Shifting Environment")
    b_mean, c_mean = run_shifting_environment()
    print(f"\nFinal Generation Mean Task Success (B-copy): {b_mean:.4f}")
    print(f"Final Generation Mean Task Success (Lossy Teaching): {c_mean:.4f}")
    if c_mean > b_mean:
        print("\nConclusion: When copying incurs a capacity penalty in a non-stationary environment, lossy teaching outperforms exact cloning by preventing obsolete memory saturation.")
