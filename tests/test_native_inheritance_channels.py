"""Mechanism-level regression tests for GAL 1.0 native inheritance.

These tests exercise the implementation, not the abstract binary-channel model.
"""
import pytest

from gal.agents.agent import Agent
from gal.environment.world import Environment


def _parent(seed=17, generation=0):
    parent = Agent("parent", generation, seed)
    parent.skills.update({
        "foraging": 0.8,
        "construction": 0.6,
        "crafting": 0.4,
        "exploration": 0.9,
        "logic": 0.7,
    })
    parent.knowledge_concepts = {"concept_42", "concept_108", "concept_314"}
    return parent


def _child(seed=17, identity="child"):
    return Agent(identity, 1, seed)


def test_mode_a_does_not_transfer_skills_or_concepts():
    parent = _parent()
    child = _child()
    before = (dict(child.skills), set(child.knowledge_concepts))
    child.inherit(parent, "A")
    assert (child.skills, child.knowledge_concepts) == before


def test_b_copy_transfers_exact_skill_values_and_concepts():
    parent, child = _parent(), _child()
    child.inherit(parent, "B-copy")
    assert child.skills == parent.skills
    assert child.knowledge_concepts == parent.knowledge_concepts


def test_c_full_and_c_no_memory_have_identical_skill_channel_but_different_memory_channel():
    parent = _parent()
    full, no_memory = _child(), _child()
    full.inherit(parent, "C-full")
    no_memory.inherit(parent, "C-no-memory")
    # Same child RNG identity/seed and same teaching draws; only concept transfer differs.
    assert full.skills == no_memory.skills
    assert full.knowledge_concepts == parent.knowledge_concepts
    assert no_memory.knowledge_concepts == set()


def test_c_low_effort_transfers_concepts_and_moves_positive_skills_toward_parent():
    parent, child = _parent(), _child()
    child.inherit(parent, "C-low-effort")
    assert child.knowledge_concepts == parent.knowledge_concepts
    for name, parent_value in parent.skills.items():
        assert 0.0 <= child.skills[name] <= parent_value


@pytest.mark.parametrize("mode", ["A", "B-copy", "C-full", "C-no-memory", "C-low-effort"])
def test_inheritance_does_not_advance_lifetime_rng(mode):
    parent, child = _parent(), _child()
    before = child.lifetime_rng.getstate()
    child.inherit(parent, mode)
    assert child.lifetime_rng.getstate() == before


@pytest.mark.parametrize("mode", ["B-copy", "C-full", "C-no-memory", "C-low-effort"])
def test_inheritance_does_not_mutate_parent(mode):
    parent, child = _parent(), _child()
    skills_before = dict(parent.skills)
    concepts_before = set(parent.knowledge_concepts)
    child.inherit(parent, mode)
    assert parent.skills == skills_before
    assert parent.knowledge_concepts == concepts_before


def test_unknown_mode_is_currently_a_no_op():
    # Characterizes current behavior; it is not an endorsement of silent fallback.
    parent, child = _parent(), _child()
    before = (dict(child.skills), set(child.knowledge_concepts))
    child.inherit(parent, "not-a-mode")
    assert (child.skills, child.knowledge_concepts) == before
