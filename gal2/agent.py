"""Synthetic agent harness. Evaluation is separated from learning."""
from __future__ import annotations
from dataclasses import dataclass,field
import math,random
from .memory import MemoryStore
from .models import Capability,Evidence,EvaluationReport,MemoryKind,MemoryRecord,Task
def wilson_lower_bound(successes,trials,z=1.96):
    if trials<=0:return 0.0
    p=successes/trials; z2=z*z; denom=1+z2/trials
    centre=p+z2/(2*trials); margin=z*math.sqrt((p*(1-p)+z2/(4*trials))/trials)
    return max(0.0,(centre-margin)/denom)
@dataclass
class Agent:
    agent_id:str; generation:int; seed:int
    capabilities:dict[str,Capability]=field(default_factory=dict)
    memory:MemoryStore=field(default_factory=MemoryStore)
    def __post_init__(self):
        if not self.agent_id or self.generation<0: raise ValueError("agent_id is required and generation cannot be negative")
        self._rng=random.Random(f"{self.seed}:{self.agent_id}:{self.generation}:train")
        self._eval_rng=random.Random(f"{self.seed}:{self.agent_id}:{self.generation}:evaluation")
        self.last_evaluation={}
    def _success_probability(self,task):
        cap=self.capabilities.get(task.capability); proficiency=cap.proficiency if cap else 0.0
        return max(.02,min(.98,proficiency-.45*task.difficulty+.25))
    def attempt(self,task):
        """Training interaction: updates skill statistics and creates memories."""
        success=self._rng.random()<self._success_probability(task); score=float(success)
        evidence=Evidence(task.task_id,task.context,success,score,self.generation,agent_id=self.agent_id)
        cap=self.capabilities.setdefault(task.capability,Capability(task.capability)); cap.record(evidence)
        self.memory.add(MemoryRecord(MemoryKind.EPISODIC,{"task_id":task.task_id,"success":success,"context":task.context},
            self.agent_id,self.generation,(task.capability,task.concept,task.context),False))
        if success:
            self.memory.add(MemoryRecord(MemoryKind.SEMANTIC,{"concept":task.concept,"supported_by":task.task_id},
                self.agent_id,self.generation,(task.concept,task.capability),False))
            self.memory.add(MemoryRecord(MemoryKind.PROCEDURAL,{"procedure":f"solve:{task.capability}","task_id":task.task_id},
                self.agent_id,self.generation,(task.capability,),False))
        return evidence
    def evaluate(self,name,tasks,min_trials=5,min_success_rate=.7,confidence_z=1.96):
        """Holdout scoring; never mutates proficiency, evidence, or memory."""
        if min_trials<1 or not 0<=min_success_rate<=1: raise ValueError("invalid verification threshold")
        relevant=[t for t in tasks if t.capability==name and t.split in {"validation","test"}]
        if len(relevant)<min_trials:return None
        if len({t.task_id for t in relevant})!=len(relevant):raise ValueError("evaluation task IDs must be unique")
        successes=sum(self._eval_rng.random()<self._success_probability(t) for t in relevant)
        rate=successes/len(relevant); lower=wilson_lower_bound(successes,len(relevant),confidence_z)
        passed=rate>=min_success_rate and lower>=min_success_rate
        report=EvaluationReport(self.agent_id,name,tuple(t.task_id for t in relevant),successes,len(relevant),
            rate,lower,tuple(sorted({t.context for t in relevant})),passed)
        self.last_evaluation[name]=report
        return report
    def verify_capability(self,name,evaluation_tasks,min_trials=5,min_success_rate=.7):
        report=self.evaluate(name,evaluation_tasks,min_trials,min_success_rate)
        if report is None or name not in self.capabilities:return False
        self.capabilities[name].verified=report.passed
        return report.passed
    def inherit_from(self,parent):
        copied=0
        for name,pc in parent.capabilities.items():
            if not pc.verified:continue
            self.capabilities[name]=Capability(name,pc.proficiency,pc.confidence,list(pc.evidence),
                pc.prerequisites,pc.context_tags,pc.failure_conditions,False,pc.version,pc.lineage+(parent.agent_id,))
            copied+=1
        self.memory.inherit_verified(tuple(r for kind in MemoryKind for r in parent.memory.get(kind)),self.agent_id,self.generation)
        return copied
