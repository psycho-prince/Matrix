import random
import numpy as np
from scipy import stats

class UncappedTask:
    def __init__(self, name: str, required_skill: str, difficulty: float):
        self.name = name
        self.required_skill = required_skill
        self.difficulty = difficulty

    def attempt(self, agent_skill_level: float, rng: random.Random) -> bool:
        if agent_skill_level >= self.difficulty:
            return rng.random() < 0.9
        else:
            ratio = agent_skill_level / max(0.01, self.difficulty)
            return rng.random() < (ratio * 0.5)

class UncappedAgent:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.skills = {"logic": 0.0}
        self.tasks_attempted = 0
        self.tasks_succeeded = 0
        
    def learn(self, steps: int):
        for _ in range(steps):
            self.skills["logic"] += self.rng.uniform(0.01, 0.1)
            
    def work(self, difficulty: float, num_tasks: int = 10, record: bool = True):
        task = UncappedTask("solve", "logic", difficulty)
        for _ in range(num_tasks):
            if record:
                self.tasks_attempted += 1
            success = task.attempt(self.skills["logic"], self.rng)
            if success:
                if record:
                    self.tasks_succeeded += 1
                self.skills["logic"] += 0.02 # Learn by doing

    @property
    def success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted

def run_paired_comparison(seeds=100, generations=10, learn_steps=15, work_tasks=50):
    gen_scores = []
    immortal_scores = []
    
    for seed in range(seeds):
        # 1. Generational Run
        rng_gen = random.Random(seed)
        diff_gen = 0.5
        current_skill = 0.0
        final_gen_score = 0.0
        
        for g in range(generations):
            agent_gen = UncappedAgent(rng_gen)
            agent_gen.skills["logic"] = current_skill
            agent_gen.learn(learn_steps)
            diff_gen += 0.1
            # Only record tasks on the final generation
            record = (g == generations - 1)
            agent_gen.work(diff_gen, num_tasks=work_tasks, record=record)
            current_skill = agent_gen.skills["logic"]
            if record:
                final_gen_score = agent_gen.success_rate
        gen_scores.append(final_gen_score)
        
        # 2. Immortal Run
        rng_imm = random.Random(seed)
        diff_imm = 0.5
        agent_imm = UncappedAgent(rng_imm)
        
        for g in range(generations):
            agent_imm.learn(learn_steps)
            diff_imm += 0.1
            # Only record tasks on the final generation equivalent
            record = (g == generations - 1)
            agent_imm.work(diff_imm, num_tasks=work_tasks, record=record)
            
        immortal_scores.append(agent_imm.success_rate)
        
    return np.array(gen_scores), np.array(immortal_scores)

if __name__ == "__main__":
    print("Testing Hypothesis: Exact Copying vs Immortal Agent (Fair Baseline)")
    gen_scores, imm_scores = run_paired_comparison()
    
    diff = imm_scores - gen_scores
    t_stat, p_val = stats.ttest_rel(imm_scores, gen_scores)
    
    print(f"10 Generations (Final Epoch Mean): {np.mean(gen_scores):.4f}")
    print(f"Single Long-Lived (Final Epoch Mean): {np.mean(imm_scores):.4f}")
    print(f"Paired Difference (Immortal - Gen): {np.mean(diff):.4f}")
    print(f"t-statistic: {t_stat:.4f}, p-value: {p_val:.4e}")
