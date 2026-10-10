import random
import numpy as np
from scipy import stats

class ConstrainedAgent:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.skills = {"A": 0.0, "B": 0.0}
        self.capacity = 1.0 
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def get_total_skill(self):
        return sum(self.skills.values())

    def enforce_capacity(self):
        total = self.get_total_skill()
        if total > self.capacity:
            for k in self.skills:
                self.skills[k] = self.skills[k] * (self.capacity / total)

    def learn(self, active_skill: str, steps: int):
        for _ in range(steps):
            if self.get_total_skill() < self.capacity:
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

def run_environment(seeds=100, generations=20, switch_freq=5):
    # Modes: 
    # 'Exact': inherit all
    # 'Lossy': inherit 50% of all
    # 'Selective': inherit 100% of active, 0% of inactive
    # 'Baseline': inherit 0%
    modes = ['Exact', 'Lossy', 'Selective', 'Baseline']
    results = {m: [] for m in modes}
    
    for seed in range(seeds):
        rngs = {m: random.Random(seed) for m in modes}
        parent_skills = {m: {"A": 0.0, "B": 0.0} for m in modes}
        
        for g in range(generations):
            active_skill = "A" if (g // switch_freq) % 2 == 0 else "B"
            difficulty = 0.4
            record = (g == generations - 1)
            
            for m in modes:
                agent = ConstrainedAgent(rngs[m])
                
                if m == 'Exact':
                    agent.skills = parent_skills[m].copy()
                elif m == 'Lossy':
                    agent.skills = {k: v * 0.5 for k, v in parent_skills[m].items()}
                elif m == 'Selective':
                    agent.skills = {k: (v if k == active_skill else 0.0) for k, v in parent_skills[m].items()}
                elif m == 'Baseline':
                    agent.skills = {"A": 0.0, "B": 0.0}
                    
                agent.enforce_capacity()
                agent.learn(active_skill, 10)
                agent.work(active_skill, difficulty, num_tasks=20, record=record)
                
                parent_skills[m] = agent.skills.copy()
                
                if record:
                    results[m].append(agent.success_rate)
                    
    return {m: np.array(scores) for m, scores in results.items()}

if __name__ == "__main__":
    print("Testing Inheritance Mechanisms under Capacity Constraints & Shifting Environments\n")
    
    switch_frequencies = [2, 5, 10]
    
    for freq in switch_frequencies:
        print(f"=== Environment shifts every {freq} generations ===")
        res = run_environment(seeds=100, generations=20, switch_freq=freq)
        
        exact = res['Exact']
        for mode in ['Exact', 'Lossy', 'Selective', 'Baseline']:
            mean = np.mean(res[mode])
            ci = 1.96 * np.std(res[mode], ddof=1) / np.sqrt(len(exact))
            print(f"{mode:10s} Mean: {mean:.4f}  (95% CI: +/- {ci:.4f})")
            
            if mode != 'Exact':
                diff = np.mean(res[mode] - exact)
                t_stat, p_val = stats.ttest_rel(res[mode], exact)
                print(f"           vs Exact -> Diff: {diff:+.4f}, p: {p_val:.2e}")
        print()
