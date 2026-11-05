"""Mechanism-level regression and property tests for GAL 2.0 inheritance."""
import pytest

from gal2.agent import Agent
from gal2.adaptive_inheritance import (
    AdaptationPolicy, adapt_capability, adaptive_inherit, context_similarity,
)
from gal2.inheritance import inherit_capabilities, verify_inherited_capability
from gal2.models import Capability, MemoryKind, MemoryRecord, Task


def test_basic_inheritance_copies_only_verified_capabilities_and_resets_verification():
    parent = Agent("p", 0, 11)
    parent.capabilities["verified"] = Capability(
        "verified", 0.83, 0.72, context_tags=("lab",), verified=True, version=4,
        lineage=("ancestor",),
    )
    parent.capabilities["unverified"] = Capability("unverified", 0.99, verified=False)
    child = Agent("c", 1, 11)
    report = inherit_capabilities(parent, child)

    assert set(child.capabilities) == {"verified"}
    copied = child.capabilities["verified"]
    assert copied.proficiency == 0.83
    assert copied.confidence == 0.72
    assert copied.version == 4
    assert copied.verified is False
    assert copied.lineage == ("ancestor", "p")
    assert report.candidate_capabilities == ("verified",)


def test_basic_inheritance_copies_only_verified_memory_and_preserves_provenance():
    parent, child = Agent("p", 0, 11), Agent("c", 1, 11)
    verified = MemoryRecord(MemoryKind.SEMANTIC, {"claim": "x"}, "origin", 0,
                            ("tag",), True, lineage=("older",))
    unverified = MemoryRecord(MemoryKind.SEMANTIC, {"claim": "y"}, "p", 0,
                              ("tag",), False)
    parent.memory.add(verified)
    parent.memory.add(unverified)

    inherit_capabilities(parent, child)
    received = child.memory.get(MemoryKind.SEMANTIC)
    assert len(received) == 1
    assert received[0].content == {"claim": "x"}
    assert received[0].source_agent == "origin"
    assert received[0].custodian_agent == "c"
    assert received[0].verified is True
    assert received[0].lineage == ("older", "origin")


@pytest.mark.parametrize("prior", [0.0, 0.1, 0.5, 0.9, 1.0])
@pytest.mark.parametrize("strength", [0.0, 0.25, 0.5, 0.75, 1.0])
@pytest.mark.parametrize("similarity_case", [("a",), ("a", "b"), ("a", "b", "c")])
def test_adaptive_recalibration_stays_in_unit_interval(prior, strength, similarity_case):
    cap = Capability("skill", proficiency=0.91, context_tags=similarity_case, verified=True)
    policy = AdaptationPolicy(
        min_context_similarity=0.0,
        prior_proficiency=prior,
        recalibration_strength=strength,
    )
    child, decision = adapt_capability(cap, similarity_case, policy)
    assert child is not None and decision.accepted
    assert 0.0 <= child.proficiency <= 1.0
    assert child.verified is False
    assert child.evidence == []


def test_context_similarity_is_bounded_for_disjoint_and_identical_sets():
    cases = [
        ((), (), 0.0),
        (("a",), ("b",), 0.0),
        (("a", "b"), ("a", "b"), 1.0),
        (("a", "b"), ("b", "c"), 1.0 / 3.0),
    ]
    for left, right, expected in cases:
        value = context_similarity(left, right)
        assert 0.0 <= value <= 1.0
        assert value == pytest.approx(expected)


def test_adaptive_inheritance_rejects_unverified_parent_and_low_similarity():
    parent, child = Agent("p", 0, 5), Agent("c", 1, 5)
    parent.capabilities["unverified"] = Capability(
        "unverified", 0.9, context_tags=("lab",), verified=False
    )
    parent.capabilities["mismatch"] = Capability(
        "mismatch", 0.9, context_tags=("lab",), verified=True
    )
    report = adaptive_inherit(
        parent, child, ("field",),
        AdaptationPolicy(min_context_similarity=0.2),
    )
    assert all(not item.accepted for item in report.decisions)
    assert child.capabilities == {}


def test_child_verification_uses_held_out_tasks_and_records_outcome():
    child = Agent("c", 1, 5)
    child.capabilities["skill"] = Capability("skill", proficiency=0.98)
    tasks = [
        Task(f"heldout-{i}", "skill", "concept", 0.05, "new-context", "test")
        for i in range(200)
    ]
    # The threshold is intentionally low: this test checks the verification path,
    # not whether a particular random sample achieves a high performance threshold.
    result = verify_inherited_capability(
        child, "skill", tasks, min_trials=20, min_success_rate=0.01
    )
    report = child.last_evaluation["skill"]
    assert result is report.passed
    assert report.trials == 200
    assert len(set(report.task_ids)) == 200
    assert child.capabilities["skill"].verified is result


def test_training_and_evaluation_are_separate_state_channels():
    agent = Agent("agent", 0, 123)
    task = Task("t", "skill", "concept", 0.2, "context", "train")
    before = (dict(agent.capabilities), agent.memory.counts())
    agent.attempt(task)
    assert agent.memory.counts()["episodic"] == 1
    assert agent.capabilities["skill"].evidence

    holdout = [Task(f"v{i}", "skill", "concept", 0.2, "heldout", "validation")
               for i in range(20)]
    cap = agent.capabilities["skill"]
    state_before = (cap.proficiency, list(cap.evidence), agent.memory.counts())
    agent.evaluate("skill", holdout, min_trials=5, min_success_rate=0.0)
    state_after = (cap.proficiency, list(cap.evidence), agent.memory.counts())
    assert state_before == state_after
    assert before != (dict(agent.capabilities), agent.memory.counts())
