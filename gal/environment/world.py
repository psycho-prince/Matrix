import random

class Task:
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

class Environment:
    def __init__(self, random_seed: int = None):
        # We no longer set global random.seed() here
        self.tasks = [
            Task("resource_gathering", "foraging", 0.3),
            Task("shelter_building", "construction", 0.5),
            Task("tool_making", "crafting", 0.6),
            Task("navigation", "exploration", 0.4),
            Task("problem_solving", "logic", 0.7)
        ]
        
    def get_random_task(self, rng: random.Random) -> Task:
        return rng.choice(self.tasks)
