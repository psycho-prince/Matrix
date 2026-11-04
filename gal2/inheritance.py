"""Evidence-gated inheritance and successor verification."""
from __future__ import annotations
from dataclasses import dataclass
from .agent import Agent
from .models import Task

@dataclass(frozen=True)
class InheritanceReport:
    parent_id: str
    child_id: str
    candidate_capabilities: tuple[str, ...]
    initially_verified: tuple[str, ...]

def inherit_capabilities(parent: Agent, child: Agent) -> InheritanceReport:
    if child.generation <= parent.generation:
        raise ValueError("child generation must be greater than parent generation")
    child.inherit_from(parent)
    candidates = tuple(sorted(name for name, cap in child.capabilities.items() if not cap.verified))
    return InheritanceReport(parent.agent_id, child.agent_id, candidates, ())

def verify_inherited_capability(child: Agent, name: str, held_out_tasks: list[Task],
                                min_trials: int = 5, min_success_rate: float = 0.7) -> bool:
    cap = child.capabilities.get(name)
    if cap is None:
        return False
    if cap.verified:
        return True
    return child.verify_capability(name, held_out_tasks, min_trials, min_success_rate)
