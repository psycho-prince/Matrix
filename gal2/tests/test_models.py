import pytest
from gal2.models import Capability, Evidence, MemoryKind, MemoryRecord, Task


def test_capability_rejects_invalid_scores():
    with pytest.raises(ValueError):
        Capability("debugging", proficiency=1.2)


def test_evidence_updates_capability_metrics():
    cap = Capability("debugging")
    cap.record(Evidence("t1", "routine", True, 0.8, 0))
    cap.record(Evidence("t2", "noisy", False, 0.4, 0))
    assert cap.proficiency == pytest.approx(0.6)
    assert cap.confidence == pytest.approx(0.2)


def test_task_rejects_invalid_split_and_difficulty():
    with pytest.raises(ValueError):
        Task("x", "debugging", "causal", 0, "routine")
    with pytest.raises(ValueError):
        Task("x", "debugging", "causal", 0.5, "routine", "leak")


def test_memory_record_requires_source():
    with pytest.raises(ValueError):
        MemoryRecord(MemoryKind.EPISODIC, {}, "", 0)
