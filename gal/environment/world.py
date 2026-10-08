import random

class Task:
    def __init__(self, name: str, required_skill: str, difficulty: float, associated_concept: str):
        self.name = name
        self.required_skill = required_skill
        self.difficulty = difficulty
        self.associated_concept = associated_concept

    def attempt(self, agent_skill_level: float, agent_concepts: set, rng: random.Random) -> bool:
        # VERSION 0.3: True Semantic Memory
        # Having the abstract concept related to the task effectively lowers its difficulty
        effective_difficulty = self.difficulty
        if self.associated_concept in agent_concepts:
            effective_difficulty *= 0.5 # Conceptual understanding makes the task 50% easier
            
        if agent_skill_level >= effective_difficulty:
            return rng.random() < 0.9
        else:
            ratio = agent_skill_level / max(0.01, effective_difficulty)
            return rng.random() < (ratio * 0.5)

class Environment:
    def __init__(self):
        # The abstract concepts required to gain the semantic memory bonus
        self.tasks = [
            Task("resource_gathering", "foraging", 0.3, "concept_42"),
            Task("shelter_building", "construction", 0.5, "concept_108"),
            Task("tool_making", "crafting", 0.6, "concept_7"),
            Task("navigation", "exploration", 0.4, "concept_99"),
            Task("problem_solving", "logic", 0.7, "concept_314")
        ]
        
    def get_random_task(self, rng: random.Random) -> Task:
        return rng.choice(self.tasks)
