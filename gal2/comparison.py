"""Paired synthetic comparison of inheritance and memory baselines.

This experiment compares mechanisms in the existing Bernoulli simulator only.
It is not an empirical benchmark of a real learning system.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path
from .agent import Agent
from .adaptive_inheritance import AdaptationPolicy, adaptive_inherit
from .models import Capability, MemoryKind, MemoryRecord, Task

ARMS = ("no_transfer", "capability_copy", "adaptive_inheritance", "shared_memory")


def paired_tasks(seed: int, split: str, count: int, context: str) -> list[Task]:
    # Same task sequence is used by all arms for each paired seed.
    return [Task(f"{split}-{seed}-{i}", "planning", "decomposition",
                 0.25 + (i % 5) * 0.05, context, split)
            for i in range(count)]


def build_parent(seed: int) -> Agent:
    """Create a deterministic, already-verified synthetic parent fixture.

    This isolates transfer policies from the current simulator's unstable
    training dynamics; it is not evidence that the parent learned the skill.
    """
    parent = Agent(f"parent-{seed}", 0, seed)
    parent.capabilities["planning"] = Capability(
        "planning", proficiency=0.9, confidence=0.9,
        context_tags=("routine", "resource_limited"),
        verified=True,
    )
    parent.memory.add(MemoryRecord(
        MemoryKind.SEMANTIC,
        {"concept": "decomposition", "supported_by": "fixture"},
        parent.agent_id, 0, ("decomposition", "planning"), True,
    ))
    parent.memory.add(MemoryRecord(
        MemoryKind.PROCEDURAL,
        {"procedure": "solve:planning", "source": "fixture"},
        parent.agent_id, 0, ("planning",), True,
    ))
    return parent

