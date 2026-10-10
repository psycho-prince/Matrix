import random
import numpy as np

# A simplified, uncapped environment to test the "Saturated World" and "Long-Lived" hypotheses
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
            # Uncapped learning
            self.skills["logic"] += self.rng.uniform(0.01, 0.1)
            
    def work(self, difficulty: float, num_tasks: int = 10):
        task = UncappedTask("solve", "logic", difficulty)
        for _ in range(num_tasks):
            self.tasks_attempted += 1
            if task.attempt(self.skills["logic"], self.rng):
                self.tasks_succeeded += 1
                self.skills["logic"] += 0.02 # Learn by doing

    @property
    def success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted

def run_generational(seeds, generations, learn_steps_per_gen):
    successes = []
    for seed in range(seeds):
        rng = random.Random(seed)
        difficulty = 0.5
        current_skill = 0.0
        
        for g in range(generations):
            agent = UncappedAgent(rng)
            # B-copy inheritance
            agent.skills["logic"] = current_skill 
            
            agent.learn(learn_steps_per_gen)
            difficulty += 0.1 # World gets harder over time, won't saturate
            agent.work(difficulty, num_tasks=50)
            current_skill = agent.skills["logic"]
            
        successes.append(agent.success_rate)
    return np.mean(successes)

def run_single_long_lived(seeds, generations, learn_steps_per_gen):
    successes = []
    for seed in range(seeds):
        rng = random.Random(seed)
        difficulty = 0.5
        
        agent = UncappedAgent(rng)
        
        for g in range(generations):
            # Same lifetime learning events as the generational agents
            agent.learn(learn_steps_per_gen)
            difficulty += 0.1 # World gets harder over time
            agent.work(difficulty, num_tasks=50)
            
        # We only measure the final epoch's success rate for fairness
        # by resetting the task counters before the last work phase, or just looking at overall
        # Let's reset counters to measure just the final generation's capability
        agent.tasks_attempted = 0
        agent.tasks_succeeded = 0
        agent.work(difficulty, num_tasks=50)
        
        successes.append(agent.success_rate)
    return np.mean(successes)

if __name__ == "__main__":
    seeds = 100
    generations = 10
    learn_steps = 15
    
    print("Testing Hypothesis: Generations act as a longer life in an uncapped world.")
    gen_score = run_generational(seeds, generations, learn_steps)
    immortal_score = run_single_long_lived(seeds, generations, learn_steps)
    
    print(f"\n10 Generations of B-copy agents (Final Gen Success Rate): {gen_score:.4f}")
    print(f"1 Single Long-Lived agent (Final Epoch Success Rate): {immortal_score:.4f}")
    
    if immortal_score >= gen_score:
        print("\nConclusion: The single agent matches or beats the copied generations.")
        print("This confirms the critique: Without a transmission cost or capacity penalty, B-copy is trivially equivalent to a single continuous lifespan.")
