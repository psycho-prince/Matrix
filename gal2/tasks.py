"""Seeded dynamic task generation with explicit data splits."""
from __future__ import annotations
import random
from .models import Task

class DynamicTaskGenerator:
    CAPABILITIES = ("debugging", "planning", "classification", "reasoning", "navigation")
    CONCEPTS = ("causal_analysis", "constraint_tracking", "pattern_detection", "decomposition", "spatial_mapping")
    CONTEXTS = ("routine", "noisy", "resource_limited", "time_limited", "shifted")
    def __init__(self, seed: int) -> None:
        self.seed = seed
    def generate(self, count: int, split: str = "train", offset: int = 0) -> list[Task]:
        if count < 1 or offset < 0:
            raise ValueError("count must be positive and offset non-negative")
        if split not in {"train", "validation", "test"}:
            raise ValueError("invalid split")
        rng = random.Random(f"{self.seed}:{split}:{offset}")
        tasks = []
        for index in range(offset, offset + count):
            capability = rng.choice(self.CAPABILITIES)
            concept = rng.choice(self.CONCEPTS)
            context = rng.choice(self.CONTEXTS)
            difficulty = round(rng.uniform(0.15, 0.95), 3)
            tasks.append(Task(f"{split}-{self.seed}-{index}", capability, concept, difficulty, context, split,
                              f"{capability} task requiring {concept} under {context} conditions"))
        return tasks
