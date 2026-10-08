import random
from typing import Dict, List, Optional
from gal.environment.world import Environment, Task

class Agent:
    def __init__(self, identity: str, generation: int, random_seed: int = None):
        if random_seed is not None:
            random.seed(random_seed)
            
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
            num_new_concepts = random.randint(5, 20)
            for _ in range(num_new_concepts):
                self.knowledge_concepts.add(f"concept_{random.randint(1, 10000)}")
            
            skill_to_improve = random.choice(list(self.skills.keys()))
            self.skills[skill_to_improve] = min(1.0, self.skills[skill_to_improve] + random.uniform(0.01, 0.1))
            self.age += 1

    def work(self, environment: Environment, num_tasks: int = 5):
        for _ in range(num_tasks):
            task = environment.get_random_task()
            self.tasks_attempted += 1
            
            skill_level = self.skills.get(task.required_skill, 0.0)
            if task.attempt(skill_level):
                self.tasks_succeeded += 1
                self.skills[task.required_skill] = min(1.0, self.skills[task.required_skill] + 0.02)
        self.age += 5

    def inherit(self, parent_agent, mode: str):
        """
        Handle inheritance based on the specific experimental ablation mode.
        Ensures strict time/resource equivalence across all modes.
        Modes:
        - A: No inheritance
        - B-copy: Direct memory dump
        - C-full: Active teaching (skills and concepts)
        - C-no-memory: Active teaching (skills only)
        - C-low-effort: Active teaching (low transfer rate)
        """
        if mode == 'A':
            pass # Independent learning only
            
        elif mode == 'B-copy':
            # Direct database dump
            self.knowledge_concepts = set(parent_agent.knowledge_concepts)
            for skill, level in parent_agent.skills.items():
                self.skills[skill] = level * 0.9
                
        elif mode == 'C-full':
            # Full active teaching
            taught_concepts = random.sample(
                list(parent_agent.knowledge_concepts), 
                k=int(len(parent_agent.knowledge_concepts) * random.uniform(0.5, 0.8))
            ) if parent_agent.knowledge_concepts else []
            self.knowledge_concepts.update(taught_concepts)
            
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    transfer_rate = random.uniform(0.6, 0.95)
                    self.skills[skill] = max(self.skills[skill], parent_level * transfer_rate)
                    
        elif mode == 'C-no-memory':
            # Teaching skills, but not abstract concepts
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    transfer_rate = random.uniform(0.6, 0.95)
                    self.skills[skill] = max(self.skills[skill], parent_level * transfer_rate)
                    
        elif mode == 'C-low-effort':
            # Teaching with low effort
            taught_concepts = random.sample(
                list(parent_agent.knowledge_concepts), 
                k=int(len(parent_agent.knowledge_concepts) * random.uniform(0.2, 0.4))
            ) if parent_agent.knowledge_concepts else []
            self.knowledge_concepts.update(taught_concepts)
            
            for skill, parent_level in parent_agent.skills.items():
                if parent_level > 0:
                    transfer_rate = random.uniform(0.2, 0.5) # Lower transfer rate
                    self.skills[skill] = max(self.skills[skill], parent_level * transfer_rate)

    @property
    def task_success_rate(self) -> float:
        if self.tasks_attempted == 0:
            return 0.0
        return self.tasks_succeeded / self.tasks_attempted
