"""Typed domain models for GAL 2.0. Evidence is immutable and provenance-aware."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
class MemoryKind(str, Enum):
    EPISODIC="episodic"; SEMANTIC="semantic"; PROCEDURAL="procedural"
@dataclass(frozen=True)
class Evidence:
    task_id:str; context:str; success:bool; score:float; generation:int
    notes:str=""; agent_id:str="unknown"; inherited_from:str|None=None
    def __post_init__(self):
        if not self.task_id or not self.context or not self.agent_id: raise ValueError("Evidence requires task_id, context and agent_id")
        if not 0<=self.score<=1: raise ValueError("Evidence score must be between 0 and 1")
        if self.generation<0: raise ValueError("generation cannot be negative")
@dataclass
class Capability:
    name:str; proficiency:float=0.0; confidence:float=0.0; evidence:list[Evidence]=field(default_factory=list)
    prerequisites:tuple[str,...]=(); context_tags:tuple[str,...]=(); failure_conditions:tuple[str,...]=()
    verified:bool=False; version:int=1; lineage:tuple[str,...]=()
    def __post_init__(self):
        if not self.name.strip(): raise ValueError("Capability name cannot be empty")
        self._validate_scores()
    def _validate_scores(self):
        if not 0<=self.proficiency<=1 or not 0<=self.confidence<=1: raise ValueError("proficiency and confidence must be between 0 and 1")
    def record(self,item:Evidence):
        self.evidence.append(item)
        self.proficiency=sum(float(e.success) for e in self.evidence)/len(self.evidence)
        self.confidence=len(self.evidence)/(len(self.evidence)+10.0)
        self._validate_scores()
@dataclass(frozen=True)
class MemoryRecord:
    kind:MemoryKind; content:dict[str,Any]; source_agent:str; generation:int
    tags:tuple[str,...]=(); verified:bool=False; custodian_agent:str|None=None; lineage:tuple[str,...]=()
    def __post_init__(self):
        if not self.source_agent: raise ValueError("Memory source_agent cannot be empty")
        if self.generation<0: raise ValueError("generation cannot be negative")
        if not isinstance(self.content,dict): raise TypeError("Memory content must be a dictionary")
@dataclass(frozen=True)
class Task:
    task_id:str; capability:str; concept:str; difficulty:float; context:str
    split:str="train"; description:str=""
    def __post_init__(self):
        if not self.task_id or not self.capability or not self.concept or not self.context: raise ValueError("Task identifiers, capability, concept and context are required")
        if not 0<self.difficulty<=1: raise ValueError("difficulty must be in (0, 1]")
        if self.split not in {"train","validation","test"}: raise ValueError("split must be train, validation or test")
@dataclass(frozen=True)
class EvaluationReport:
    agent_id:str; capability:str; task_ids:tuple[str,...]; successes:int; trials:int
    success_rate:float; wilson_lower_bound:float; contexts:tuple[str,...]; passed:bool
