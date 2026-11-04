import pytest
from gal2.agent import Agent
from gal2.adaptive_inheritance import AdaptationPolicy,adapt_capability,adaptive_inherit,context_similarity
from gal2.models import Capability,Task

def test_context_similarity_jaccard():
    assert context_similarity(("lab","noisy"),("lab","remote"))==pytest.approx(1/3)
    assert context_similarity((),("lab",))==0
def test_unverified_capability_rejected():
    cap=Capability("debugging",.9,context_tags=("lab",))
    assert adapt_capability(cap,("lab",))[0] is None
def test_context_mismatch_rejected():
    cap=Capability("debugging",.9,context_tags=("lab",),verified=True)
    adapted,decision=adapt_capability(cap,("field",),AdaptationPolicy(min_context_similarity=.2))
    assert adapted is None and not decision.accepted
def test_compatible_capability_recalibrated_and_unverified():
    cap=Capability("debugging",.9,.9,context_tags=("lab","noisy"),verified=True)
    adapted,decision=adapt_capability(cap,("lab","remote"))
    assert adapted and adapted.proficiency<cap.proficiency
    assert not adapted.verified and adapted.evidence==[] and decision.accepted
def test_adaptive_inheritance_requires_later_generation():
    parent,child=Agent("p",0,1),Agent("c",1,1)
    parent.capabilities["debugging"]=Capability("debugging",.9,context_tags=("lab",),verified=True)
    report=adaptive_inherit(parent,child,("lab",))
    assert report.decisions[0].accepted and not child.capabilities["debugging"].verified
    with pytest.raises(ValueError):adaptive_inherit(child,Agent("same",1,2),("lab",))
def test_evaluation_does_not_mutate_learning_state():
    agent=Agent("child",1,4); agent.capabilities["debugging"]=Capability("debugging",.95)
    before=(agent.capabilities["debugging"].proficiency,list(agent.capabilities["debugging"].evidence),agent.memory.counts())
    tasks=[Task(f"test-{i}","debugging","causal",.1,"shifted","test") for i in range(100)]
    report=agent.evaluate("debugging",tasks,min_trials=20,min_success_rate=.1)
    after=(agent.capabilities["debugging"].proficiency,list(agent.capabilities["debugging"].evidence),agent.memory.counts())
    assert report is not None and before==after
