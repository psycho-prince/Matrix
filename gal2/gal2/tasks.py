"""Deterministic dynamic task generation with explicit data splits."""
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
        if count < 1:
            raise ValueError("count must be positive")
        if split not in {"train", "validation", "test"}:
            raise ValueError("invalid split")
        rng = random.Random(f"{self.seed}:{split}:{offset}")
        tasks: list[Task] = []
        for index in range(offset, offset + count):
            capability = self.CAPABILITIES[rng.randrange(len(self.CAPABILITIES))]
            concept = self.CONCEPTS[rng.randrange(len(self.CONCEPTS))]
            context = self.CONTEXTS[rng.randrange(len(self.CONTEXTS))]
            difficulty = round(rng.uniform(0.15, 0.95), 3)
            tasks.append(Task(
                task_id=f"{split}-{self.seed}-{index}",
                capability=capability,
                concept=concept,
                difficulty=difficulty,
                context=context,
                split=split,
                description=f"{capability} task requiring {concept} under {context} conditions",
            ))
        return tasks
