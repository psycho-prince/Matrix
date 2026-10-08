import random
from typing import Dict, List, Optional
from gal.environment.world import Environment, Task

class Agent:
    def __init__(self, identity: str, generation: int, random_seed: int = None):
        # ISOLATED RNG INSTANCE to prevent cross-condition confounding
        self.rng = random.Random(random_seed) if random_seed is not None else random.Random()
            
        self.identity = identity
        self.generation = generation
        
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
            num_new_concepts = self.rng.randint(5, 20)
            for _ in range(num_new_concepts):
                self.knowledge_concepts.add(f"concept_{self.rng.randint(1, 10000)}")
            
            skill_to_improve = self.rng.choice(list(self.skills.keys()))
            self.skills[skill_to_improve] = min(1.0, self.skills[skill_to_improve] + self.rng.uniform(0.01, 0.1))
            self.age += 1

    def work(self, environment: Environment, num_tasks: int = 5):
        # We must also ensure the environment's task selection uses this agent's isolated RNG
        # to ensure perfect synchronization across ablation conditions.
        for _ in range(num_tasks):
            task = environment.get_random_task(self.rng)
            self.tasks_attempted += 1
            
            skill_level = self.skills.get(task.required_skill, 0.0)
            if task.attempt(skill_level, self.rng):
                self.tasks_succeeded += 1
                self.skills[task.required_skill] = min(1.0, self.skills[task.required_skill] + 0.02)
        self.age += 5

    def inherit(self, parent_agent, mode: str):
        """
        Fixed inheritance mechanism.
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
                    child_initial = self.rng.uniform(0, 0.2)
                    concept_bonus = 0.1 if len(parent_agent.knowledge_concepts) > 0 else 0.0
                    learning_iterations = 3
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.rng.uniform(0.3, 0.7) + concept_bonus
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))
                    
        elif mode == 'C-no-memory':
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    child_initial = self.rng.uniform(0, 0.2)
                    concept_bonus = 0.0 # No concepts transferred
                    learning_iterations = 3
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.rng.uniform(0.3, 0.7) + concept_bonus
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))
                    
        elif mode == 'C-low-effort':
            self.knowledge_concepts.update(parent_agent.knowledge_concepts)
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    child_initial = self.rng.uniform(0, 0.2)
                    concept_bonus = 0.05
                    learning_iterations = 1 # Low effort teaching
                    current_level = child_initial
                    for _ in range(learning_iterations):
                        error = parent_level - current_level
                        correction = error * self.rng.uniform(0.1, 0.4) + concept_bonus
                        current_level += correction
                    self.skills[skill] = min(1.0, max(self.skills[skill], current_level))

    @property
    def task_success_rate(self) -> float:
        if self.tasks_attempted == 0: return 0.0
        return self.tasks_succeeded / self.tasks_attempted
