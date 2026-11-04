"""Evidence-gated capability inheritance and successor verification."""
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
    copied = child.inherit_from(parent)
    names = tuple(sorted(name for name, cap in child.capabilities.items() if not cap.verified))
    return InheritanceReport(parent.agent_id, child.agent_id, names, ())


def verify_inherited_capability(child: Agent, name: str, held_out_tasks: list[Task],
                                min_trials: int = 5, min_success_rate: float = 0.7) -> bool:
    """A child must independently pass held-out tasks before verification."""
    capability = child.capabilities.get(name)
    if capability is None or capability.verified:
        return bool(capability and capability.verified)
    return child.verify_capability(name, held_out_tasks, min_trials, min_success_rate)
