from gal2.memory import MemoryStore
from gal2.models import MemoryKind, MemoryRecord


def make_record(content=None, **kwargs):
    return MemoryRecord(
        kind=MemoryKind.SEMANTIC,
        content=content or {"rule": {"operation": "add", "amount": 2}},
        source_agent=kwargs.get("source_agent", "parent-A"),
        generation=kwargs.get("generation", 0),
        tags=("symbolic-rulebook",),
        verified=kwargs.get("verified", True),
        custodian_agent=kwargs.get("custodian_agent"),
        lineage=kwargs.get("lineage", ()),
    )


def test_memory_types_are_isolated():
    store = MemoryStore()
    store.add(
        MemoryRecord(
            MemoryKind.EPISODIC,
            {"event": "x"},
            "a1",
            0,
            ("debugging",),
        )
    )
    assert len(store.get(MemoryKind.EPISODIC)) == 1
    assert store.get(MemoryKind.SEMANTIC) == ()


def test_only_verified_records_are_inherited_with_provenance():
    parent = MemoryStore()
    parent.add(
        MemoryRecord(
            MemoryKind.PROCEDURAL,
            {"procedure": "p"},
            "p1",
            0,
            verified=True,
        )
    )
    parent.add(
        MemoryRecord(
            MemoryKind.PROCEDURAL,
            {"procedure": "q"},
            "p1",
            0,
            verified=False,
        )
    )
    child = MemoryStore()
    assert child.inherit_verified(
        parent.get(MemoryKind.PROCEDURAL), "c1", 1
    ) == 1
    record = child.get(MemoryKind.PROCEDURAL)[0]
    assert record.source_agent == "p1"
    assert record.custodian_agent == "c1"
    assert record.lineage == ("p1",)


def test_nested_mutation_of_input_record_cannot_change_store():
    original_content = {"rule": {"operation": "add", "amount": 2}}
    store = MemoryStore()
    store.add(make_record(original_content))

    original_content["rule"]["amount"] = 999
    stored = store.get(MemoryKind.SEMANTIC)[0]
    assert stored.content["rule"]["amount"] == 2


def test_nested_mutation_of_read_result_cannot_change_store():
    store = MemoryStore()
    store.add(make_record())

    returned = store.get(MemoryKind.SEMANTIC)[0]
    returned.content["rule"]["amount"] = 999

    searched = store.search(MemoryKind.SEMANTIC, "symbolic-rulebook")[0]
    assert searched.content["rule"]["amount"] == 2


def test_child_memory_mutation_cannot_change_parent():
    parent = MemoryStore()
    parent.add(make_record())
    child = MemoryStore()
    child.inherit_verified(parent.get(MemoryKind.SEMANTIC), "child-B", 1)

    child_record = child.get(MemoryKind.SEMANTIC)[0]
    child_record.content["rule"]["amount"] = 777

    assert parent.get(MemoryKind.SEMANTIC)[0].content["rule"]["amount"] == 2


def test_lineage_tracks_each_immediate_donor_across_generations():
    parent = MemoryStore()
    parent.add(make_record())

    child = MemoryStore()
    child.inherit_verified(parent.get(MemoryKind.SEMANTIC), "child-B", 1)

    grandchild = MemoryStore()
    grandchild.inherit_verified(
        child.get(MemoryKind.SEMANTIC), "grandchild-C", 2
    )

    record = grandchild.get(MemoryKind.SEMANTIC)[0]
    assert record.source_agent == "parent-A"
    assert record.custodian_agent == "grandchild-C"
    assert record.lineage == ("parent-A", "child-B")


def test_unverified_records_are_not_copied():
    parent = MemoryStore()
    parent.add(make_record(verified=False))
    child = MemoryStore()

    assert child.inherit_verified(
        parent.get(MemoryKind.SEMANTIC), "child-B", 1
    ) == 0
    assert child.counts()["semantic"] == 0
