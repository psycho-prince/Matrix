"""Agent state and evidence-producing task interaction for GAL 2.0."""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from .memory import MemoryStore
from .models import Capability, Evidence, MemoryKind, MemoryRecord, Task


@dataclass
class Agent:
    agent_id: str
    generation: int
    seed: int
    capabilities: dict[str, Capability] = field(default_factory=dict)
    memory: MemoryStore = field(default_factory=MemoryStore)

    def __post_init__(self) -> None:
        if not self.agent_id or self.generation < 0:
            raise ValueError("agent_id is required and generation cannot be negative")
        self._rng = random.Random(f"{self.seed}:{self.agent_id}:{self.generation}")

    def attempt(self, task: Task) -> Evidence:
        capability = self.capabilities.get(task.capability)
        proficiency = capability.proficiency if capability else 0.0
        # Baseline probabilistic task model; replaceable by real task adapters later.
        probability = max(0.02, min(0.98, proficiency - 0.45 * task.difficulty + 0.25))
        success = self._rng.random() < probability
        score = min(1.0, max(0.0, probability if success else probability * 0.25))
        evidence = Evidence(task.task_id, task.context, success, score, self.generation)
        if capability is None:
            capability = Capability(task.capability)
            self.capabilities[task.capability] = capability
        capability.record(evidence)
        self.memory.add(MemoryRecord(
            kind=MemoryKind.EPISODIC,
            content={"task_id": task.task_id, "success": success, "score": score, "context": task.context},
            source_agent=self.agent_id,
            generation=self.generation,
            tags=(task.capability, task.concept, task.context),
            verified=False,
        ))
        if success:
            self.memory.add(MemoryRecord(
                kind=MemoryKind.SEMANTIC,
                content={"concept": task.concept, "supported_by": task.task_id},
                source_agent=self.agent_id,
                generation=self.generation,
                tags=(task.concept, task.capability),
                verified=False,
            ))
            self.memory.add(MemoryRecord(
                kind=MemoryKind.PROCEDURAL,
                content={"procedure": f"solve:{task.capability}", "task_id": task.task_id},
                source_agent=self.agent_id,
                generation=self.generation,
                tags=(task.capability,),
                verified=False,
            ))
        return evidence

    def verify_capability(self, name: str, evaluation_tasks: list[Task], min_trials: int = 5,
                          min_success_rate: float = 0.7) -> bool:
        if min_trials < 1 or not 0.0 <= min_success_rate <= 1.0:
            raise ValueError("invalid verification threshold")
        relevant = [t for t in evaluation_tasks if t.capability == name and t.split in {"validation", "test"}]
        if len(relevant) < min_trials:
            return False
        results = [self.attempt(t) for t in relevant]
        rate = sum(e.success for e in results) / len(results)
        capability = self.capabilities.get(name)
        if capability is None:
            return False
        capability.verified = rate >= min_success_rate
        return capability.verified

    def inherit_from(self, parent: "Agent") -> int:
        """Import candidate capabilities, never their verified status."""
        copied = 0
        for name, parent_capability in parent.capabilities.items():
            if not parent_capability.verified:
                continue
            candidate = Capability(
                name=name,
                proficiency=parent_capability.proficiency,
                confidence=parent_capability.confidence,
                evidence=list(parent_capability.evidence),
                prerequisites=parent_capability.prerequisites,
                context_tags=parent_capability.context_tags,
                failure_conditions=parent_capability.failure_conditions,
                verified=False,
                version=parent_capability.version,
            )
            self.capabilities[name] = candidate
            copied += 1
        self.memory.inherit_verified(
            tuple(record for kind in MemoryKind for record in parent.memory.get(kind)),
            self.agent_id,
            self.generation,
        )
        return copied
