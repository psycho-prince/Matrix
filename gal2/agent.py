"""Synthetic agent harness; real-world task adapters are deliberately deferred."""
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
        cap = self.capabilities.get(task.capability)
        proficiency = cap.proficiency if cap else 0.0
        probability = max(0.02, min(0.98, proficiency - 0.45 * task.difficulty + 0.25))
        success = self._rng.random() < probability
        score = probability if success else probability * 0.25
        evidence = Evidence(task.task_id, task.context, success, score, self.generation)
        if cap is None:
            cap = Capability(task.capability)
            self.capabilities[task.capability] = cap
        cap.record(evidence)
        self.memory.add(MemoryRecord(MemoryKind.EPISODIC,
            {"task_id": task.task_id, "success": success, "score": score, "context": task.context},
            self.agent_id, self.generation, (task.capability, task.concept, task.context), False))
        if success:
            self.memory.add(MemoryRecord(MemoryKind.SEMANTIC, {"concept": task.concept, "supported_by": task.task_id},
                self.agent_id, self.generation, (task.concept, task.capability), False))
            self.memory.add(MemoryRecord(MemoryKind.PROCEDURAL, {"procedure": f"solve:{task.capability}", "task_id": task.task_id},
                self.agent_id, self.generation, (task.capability,), False))
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
        cap = self.capabilities.get(name)
        if cap is None:
            return False
        cap.verified = rate >= min_success_rate
        if cap.verified:
            self.memory.verify_related(name)
        return cap.verified
    def inherit_from(self, parent: "Agent") -> int:
        copied = 0
        for name, parent_cap in parent.capabilities.items():
            if not parent_cap.verified:
                continue
            self.capabilities[name] = Capability(name, parent_cap.proficiency, parent_cap.confidence,
                list(parent_cap.evidence), parent_cap.prerequisites, parent_cap.context_tags,
                parent_cap.failure_conditions, False, parent_cap.version)
            copied += 1
        self.memory.inherit_verified(tuple(r for kind in MemoryKind for r in parent.memory.get(kind)),
                                     self.agent_id, self.generation)
        return copied
