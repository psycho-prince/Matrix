from gal2.memory import MemoryStore
from gal2.models import MemoryKind, MemoryRecord


def test_memory_types_are_isolated():
    store = MemoryStore()
    record = MemoryRecord(MemoryKind.EPISODIC, {"event": "x"}, "a1", 0, ("debugging",))
    store.add(record)
    assert len(store.get(MemoryKind.EPISODIC)) == 1
    assert store.get(MemoryKind.SEMANTIC) == ()


def test_only_verified_records_are_inherited():
    parent = MemoryStore()
    parent.add(MemoryRecord(MemoryKind.PROCEDURAL, {"procedure": "p"}, "p1", 0, verified=True))
    parent.add(MemoryRecord(MemoryKind.PROCEDURAL, {"procedure": "q"}, "p1", 0, verified=False))
    child = MemoryStore()
    count = child.inherit_verified(parent.get(MemoryKind.PROCEDURAL), "c1", 1)
    assert count == 1
    assert len(child.get(MemoryKind.PROCEDURAL)) == 1
    assert child.get(MemoryKind.PROCEDURAL)[0].source_agent == "c1"
