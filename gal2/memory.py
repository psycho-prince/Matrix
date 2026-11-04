"""Separated memory stores with source provenance and immutable transfer lineage."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import replace
from .models import MemoryKind, MemoryRecord
class MemoryStore:
    def __init__(self): self._records:dict[MemoryKind,list[MemoryRecord]]=defaultdict(list)
    def add(self,record): self._records[record.kind].append(record)
    def get(self,kind): return tuple(self._records[kind])
    def search(self,kind,tag): return tuple(r for r in self._records[kind] if tag in r.tags)
    def verify_related(self,capability):
        """Legacy tag-based helper; this is not independent semantic verification."""
        changed=0
        for kind in (MemoryKind.SEMANTIC,MemoryKind.PROCEDURAL):
            updated=[]
            for record in self._records[kind]:
                if capability in record.tags and not record.verified:
                    record=replace(record,verified=True); changed+=1
                updated.append(record)
            self._records[kind]=updated
        return changed
    def inherit_verified(self,records,child_id,generation):
        copied=0
        for record in records:
            if record.verified:
                self.add(MemoryRecord(record.kind,dict(record.content),record.source_agent,
                    record.generation,record.tags,True,child_id,record.lineage+(record.source_agent,)))
                copied+=1
        return copied
    def counts(self): return {kind.value:len(self._records[kind]) for kind in MemoryKind}
