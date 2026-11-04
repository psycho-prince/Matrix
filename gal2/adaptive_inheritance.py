"""Adaptive inheritance policy with explicit context matching and audit records."""
from __future__ import annotations
from dataclasses import dataclass
from .agent import Agent
from .models import Capability,MemoryKind

@dataclass(frozen=True)
class AdaptationPolicy:
    min_context_similarity:float=.25
    prior_proficiency:float=.5
    recalibration_strength:float=.5
    def __post_init__(self):
        if not 0<=self.min_context_similarity<=1:raise ValueError("min_context_similarity must be in [0,1]")
        if not 0<=self.prior_proficiency<=1:raise ValueError("prior_proficiency must be in [0,1]")
        if not 0<=self.recalibration_strength<=1:raise ValueError("recalibration_strength must be in [0,1]")
@dataclass(frozen=True)
class AdaptationDecision:
    capability:str; accepted:bool; context_similarity:float; source_proficiency:float
    adapted_proficiency:float|None; reason:str
@dataclass(frozen=True)
class AdaptiveInheritanceReport:
    parent_id:str; child_id:str; decisions:tuple[AdaptationDecision,...]
def context_similarity(source:tuple[str,...],target:tuple[str,...])->float:
    """Jaccard similarity of declared context labels, not semantic similarity."""
    a,b=set(source),set(target)
    return len(a&b)/len(a|b) if a and b else 0.0
def adapt_capability(parent_cap:Capability,child_context:tuple[str,...],
                     policy:AdaptationPolicy=AdaptationPolicy()):
    if not parent_cap.verified:
        return None,AdaptationDecision(parent_cap.name,False,0.0,parent_cap.proficiency,None,"parent capability is not verified")
    similarity=context_similarity(parent_cap.context_tags,child_context)
    if similarity<policy.min_context_similarity:
        return None,AdaptationDecision(parent_cap.name,False,similarity,parent_cap.proficiency,None,"context similarity below transfer threshold")
    weight=similarity*(1.0-policy.recalibration_strength)
    adapted=policy.prior_proficiency+weight*(parent_cap.proficiency-policy.prior_proficiency)
    child=Capability(parent_cap.name,adapted,0.0,[],parent_cap.prerequisites,child_context,
        parent_cap.failure_conditions,False,parent_cap.version+1,parent_cap.lineage)
    return child,AdaptationDecision(parent_cap.name,True,similarity,parent_cap.proficiency,adapted,
        "accepted; recalibrated to target context; child must independently validate")
def adaptive_inherit(parent:Agent,child:Agent,child_context:tuple[str,...],
                     policy:AdaptationPolicy=AdaptationPolicy())->AdaptiveInheritanceReport:
    if child.generation<=parent.generation:raise ValueError("child generation must be greater than parent generation")
    decisions=[]
    for name in sorted(parent.capabilities):
        adapted,decision=adapt_capability(parent.capabilities[name],child_context,policy)
        decisions.append(decision)
        if adapted is not None:
            adapted.lineage=parent.capabilities[name].lineage+(parent.agent_id,)
            child.capabilities[name]=adapted
    child.memory.inherit_verified(tuple(r for kind in MemoryKind for r in parent.memory.get(kind)),
                                  child.agent_id,child.generation)
    return AdaptiveInheritanceReport(parent.agent_id,child.agent_id,tuple(decisions))
