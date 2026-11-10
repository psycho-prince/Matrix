from types import SimpleNamespace

import pytest

from gal_qwen.memory_adapter import (
    GALMemoryAdapter,
    VerificationReport,
    wilson_lower_bound,
)


def make_record(verified=True, generation=0):
    return SimpleNamespace(
        kind=SimpleNamespace(value="semantic"),
        content={"fact": "Zorvium is fictional"},
        source_agent="parent-1",
        generation=generation,
        tags=("zorvium",),
        lineage=("ancestor-0",),
        verified=verified,
    )


def make_report(candidate, successes=30, trials=30):
    ids = tuple(f"heldout-{i}" for i in range(trials))
    return VerificationReport(
        candidate_id=candidate.candidate_id,
        evaluator_id="independent-evaluator-1",
        task_ids=ids,
        successes=successes,
        trials=trials,
        success_rate=successes / trials,
        wilson_lower_bound=wilson_lower_bound(successes, trials),
        passed=successes / trials >= 0.70
        and wilson_lower_bound(successes, trials) >= 0.70,
    )


def test_unverified_parent_record_is_rejected():
    assert GALMemoryAdapter().inherit(
        make_record(False), "child-1", 1
    ) is None


def test_inherited_record_starts_pending():
    candidate = GALMemoryAdapter().inherit(
        make_record(), "child-1", 1
    )

    assert candidate.status == "pending"
    assert not candidate.verified
    assert candidate.source_agent == "parent-1"
    assert candidate.custodian_agent == "child-1"
    assert candidate.lineage == ("ancestor-0", "parent-1")


def test_child_generation_must_be_later():
    with pytest.raises(ValueError):
        GALMemoryAdapter().inherit(make_record(), "child-1", 0)


def test_prompt_marks_pending_memory_unverified():
    adapter = GALMemoryAdapter()
    candidate = adapter.inherit(make_record(), "child-1", 1)

    prompt = adapter.prompt_context([candidate])

    assert "UNVERIFIED CANDIDATE" in prompt
    assert "DO NOT ASSUME TRUE" in prompt


def test_verification_requires_independent_report():
    adapter = GALMemoryAdapter()
    candidate = adapter.inherit(make_record(), "child-1", 1)

    with pytest.raises(TypeError):
        adapter.verify(candidate, ["heldout-task-001"])


def test_insufficient_trials_are_rejected():
    adapter = GALMemoryAdapter()
    candidate = adapter.inherit(make_record(), "child-1", 1)
    report = make_report(candidate, successes=10, trials=10)

    with pytest.raises(ValueError):
        adapter.verify(candidate, report)


def test_successful_report_verifies_without_mutating_parent_candidate():
    adapter = GALMemoryAdapter()
    candidate = adapter.inherit(make_record(), "child-1", 1)

    verified = adapter.verify(candidate, make_report(candidate))

    assert verified.verified
    assert not candidate.verified
    assert len(verified.verification_evidence_ids) == 30
    assert verified.evaluator_id == "independent-evaluator-1"


def test_report_for_another_candidate_is_rejected():
    adapter = GALMemoryAdapter()
    first = adapter.inherit(make_record(), "child-1", 1)
    second = adapter.inherit(make_record(), "child-2", 1)

    with pytest.raises(ValueError):
        adapter.verify(first, make_report(second))
