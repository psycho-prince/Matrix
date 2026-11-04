"""Typed domain models for capabilities, memories, tasks and evidence."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MemoryKind(str, Enum):
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


@dataclass(frozen=True)
class Evidence:
    task_id: str
    context: str
    success: bool
    score: float
    generation: int
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.task_id or not self.context:
            raise ValueError("Evidence requires task_id and context")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Evidence score must be between 0 and 1")
        if self.generation < 0:
            raise ValueError("generation cannot be negative")


@dataclass
class Capability:
    name: str
    proficiency: float = 0.0
    confidence: float = 0.0
    evidence: list[Evidence] = field(default_factory=list)
    prerequisites: tuple[str, ...] = ()
    context_tags: tuple[str, ...] = ()
    failure_conditions: tuple[str, ...] = ()
    verified: bool = False
    version: int = 1

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Capability name cannot be empty")
        self._validate_scores()

    def _validate_scores(self) -> None:
        if not 0.0 <= self.proficiency <= 1.0:
            raise ValueError("proficiency must be between 0 and 1")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def record(self, item: Evidence) -> None:
        self.evidence.append(item)
        self.proficiency = sum(e.score for e in self.evidence) / len(self.evidence)
        self.confidence = min(1.0, len(self.evidence) / 10.0)
        self._validate_scores()


@dataclass(frozen=True)
class MemoryRecord:
    kind: MemoryKind
    content: dict[str, Any]
    source_agent: str
    generation: int
    tags: tuple[str, ...] = ()
    verified: bool = False

    def __post_init__(self) -> None:
        if not self.source_agent:
            raise ValueError("Memory source_agent cannot be empty")
        if self.generation < 0:
            raise ValueError("generation cannot be negative")
        if not isinstance(self.content, dict):
            raise TypeError("Memory content must be a dictionary")


@dataclass(frozen=True)
class Task:
    task_id: str
    capability: str
    concept: str
    difficulty: float
    context: str
    split: str = "train"
    description: str = ""

    def __post_init__(self) -> None:
        if not self.task_id or not self.capability or not self.concept or not self.context:
            raise ValueError("Task identifiers, capability, concept and context are required")
        if not 0.0 < self.difficulty <= 1.0:
            raise ValueError("difficulty must be in (0, 1]")
        if self.split not in {"train", "validation", "test"}:
            raise ValueError("split must be train, validation or test")
