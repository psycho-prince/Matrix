import pytest
from gal2.agent import Agent
from gal2.inheritance import inherit_capabilities, verify_inherited_capability
from gal2.models import Capability, Task


def test_unverified_parent_capability_is_not_inherited():
    parent = Agent("p", 0, 7)
    parent.capabilities["debugging"] = Capability("debugging", proficiency=0.9, verified=False)
    child = Agent("c", 1, 7)
    report = inherit_capabilities(parent, child)
    assert report.candidate_capabilities == ()
    assert "debugging" not in child.capabilities


def test_verified_parent_capability_becomes_unverified_candidate():
    parent = Agent("p", 0, 7)
    parent.capabilities["debugging"] = Capability("debugging", proficiency=0.9, confidence=0.9, verified=True)
    child = Agent("c", 1, 7)
    report = inherit_capabilities(parent, child)
    assert report.candidate_capabilities == ("debugging",)
    assert child.capabilities["debugging"].verified is False


def test_child_must_pass_held_out_verification():
    child = Agent("c", 1, 7)
    child.capabilities["debugging"] = Capability("debugging", proficiency=1.0)
    tasks = [Task(f"t{i}", "debugging", "causal_analysis", 0.15, "shifted", "test") for i in range(8)]
    result = verify_inherited_capability(child, "debugging", tasks, min_trials=5, min_success_rate=0.0)
    assert result is True
    assert child.capabilities["debugging"].verified is True


def test_child_generation_must_be_later():
    parent = Agent("p", 2, 1)
    child = Agent("c", 2, 1)
    with pytest.raises(ValueError):
        inherit_capabilities(parent, child)


def test_insufficient_held_out_tasks_fail_closed():
    child = Agent("c", 1, 1)
    child.capabilities["debugging"] = Capability("debugging", proficiency=1.0)
    tasks = [Task("t1", "debugging", "causal", 0.2, "shifted", "test")]
    assert verify_inherited_capability(child, "debugging", tasks, min_trials=5) is False
    assert child.capabilities["debugging"].verified is False
