import random

class Task:
    def __init__(self, name: str, required_skill: str, difficulty: float):
        self.name = name
        self.required_skill = required_skill
        self.difficulty = difficulty

    def attempt(self, agent_skill_level: float) -> bool:
        """
        Attempt the task. Probability of success depends on skill level vs difficulty.
        """
        if agent_skill_level >= self.difficulty:
            # High chance of success if skill meets/exceeds difficulty
            return random.random() < 0.9
        else:
            # Lower chance of success based on ratio
            ratio = agent_skill_level / max(0.01, self.difficulty)
            return random.random() < (ratio * 0.5)

class Environment:
    """
    Represents the world in which agents exist, providing specific tasks to accomplish.
    """
    def __init__(self, random_seed: int = None):
        if random_seed is not None:
            random.seed(random_seed)
            
        self.tasks = [
            Task("resource_gathering", "foraging", 0.3),
            Task("shelter_building", "construction", 0.5),
            Task("tool_making", "crafting", 0.6),
            Task("navigation", "exploration", 0.4),
            Task("problem_solving", "logic", 0.7)
        ]
        
    def get_random_task(self) -> Task:
        return random.choice(self.tasks)
