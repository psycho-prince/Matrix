from gal2.memory import MemoryStore
from gal2.models import MemoryKind,MemoryRecord
def test_memory_types_are_isolated():
    store=MemoryStore(); store.add(MemoryRecord(MemoryKind.EPISODIC,{"event":"x"},"a1",0,("debugging",)))
    assert len(store.get(MemoryKind.EPISODIC))==1 and store.get(MemoryKind.SEMANTIC)==()
def test_only_verified_records_are_inherited_with_provenance():
    parent=MemoryStore()
    parent.add(MemoryRecord(MemoryKind.PROCEDURAL,{"procedure":"p"},"p1",0,verified=True))
    parent.add(MemoryRecord(MemoryKind.PROCEDURAL,{"procedure":"q"},"p1",0,verified=False))
    child=MemoryStore(); assert child.inherit_verified(parent.get(MemoryKind.PROCEDURAL),"c1",1)==1
    record=child.get(MemoryKind.PROCEDURAL)[0]
    assert record.source_agent=="p1" and record.custodian_agent=="c1" and record.lineage==("p1",)
