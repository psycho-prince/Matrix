import random
import hashlib
from typing import Dict, List, Optional
from gal.environment.world import Environment, Task

def get_deterministic_rng(seed_string: str) -> random.Random:
    # Create a deterministic integer seed from a string
    hash_obj = hashlib.sha256(seed_string.encode('utf-8'))
    seed_int = int(hash_obj.hexdigest(), 16)
    return random.Random(seed_int)

class Agent:
    def __init__(self, identity: str, generation: int, universe_seed: int):
        self.identity = identity
        self.generation = generation
        self.universe_seed = universe_seed
        
        # VERSION 0.3: Dual isolated RNG streams
        self.inheritance_rng = get_deterministic_rng(f"{universe_seed}_{generation}_{identity}_inherit")
        self.lifetime_rng = get_deterministic_rng(f"{universe_seed}_{generation}_{identity}_lifetime")
            
        self.age = 0
        self.development_stage = "infant"
        
        # Capabilities (0.0 to 1.0)
        self.skills: Dict[str, float] = {
            "foraging": 0.0,
            "construction": 0.0,
            "crafting": 0.0,
            "exploration": 0.0,
            "logic": 0.0
        }
        
        self.knowledge_concepts = set()
        self.parents: List[str] = []
        self.successor: Optional[str] = None
        
        self.tasks_attempted = 0
        self.tasks_succeeded = 0

    def develop(self):
        self.age = 18
        self.development_stage = "adult"

    def learn_independently(self, environment: Environment):
        if self.development_stage in ["child", "adult"]:
            num_new_concepts = self.lifetime_rng.randint(5, 20)
            for _ in range(num_new_concepts):
                self.knowledge_concepts.add(f"concept_{self.lifetime_rng.randint(1, 1000)}")
            
            skill_to_improve = self.lifetime_rng.choice(list(self.skills.keys()))
            self.skills[skill_to_improve] = min(1.0, self.skills[skill_to_improve] + self.lifetime_rng.uniform(0.01, 0.1))
            self.age += 1

    def work(self, environment: Environment, num_tasks: int = 5):
        # Using lifetime_rng ensures identical task sequences across all experimental conditions
        for _ in range(num_tasks):
            task = environment.get_random_task(self.lifetime_rng)
            self.tasks_attempted += 1
            
            skill_level = self.skills.get(task.required_skill, 0.0)
            # TRUE SEMANTIC MEMORY: Task checks if agent has the required abstract concept
            if task.attempt(skill_level, self.knowledge_concepts, self.lifetime_rng):
                self.tasks_succeeded += 1
                self.skills[task.required_skill] = min(1.0, self.skills[task.required_skill] + 0.02)
        self.age += 5

    def inherit(self, parent_agent, mode: str):
        """
        Version 0.3 Inheritance. Strictly utilizes inheritance_rng.
        """
        if mode == 'A':
            pass 
            
        elif mode == 'B-copy':
            self.knowledge_concepts = set(parent_agent.knowledge_concepts)
            for skill, level in parent_agent.skills.items():
                self.skills[skill] = level * 0.9
                
        elif mode == 'C-full':
            # TRUE TEACHING MECHANISM
            self.knowledge_concepts.update(parent_agent.knowledge_concepts)
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    child_initial = self.inheritance_rng.uniform(0, 0.2)
                    learning_iterations = 3
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.inheritance_rng.uniform(0.3, 0.7)
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))
                    
        elif mode == 'C-no-memory':
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    child_initial = self.inheritance_rng.uniform(0, 0.2)
                    learning_iterations = 3
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.inheritance_rng.uniform(0.3, 0.7)
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))
                    
        elif mode == 'C-low-effort':
            self.knowledge_concepts.update(parent_agent.knowledge_concepts)
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    child_initial = self.inheritance_rng.uniform(0, 0.2)
                    learning_iterations = 1 # Low effort teaching
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.inheritance_rng.uniform(0.1, 0.4)
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))

    @property
    def task_success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted
