"""Separated episodic, semantic and procedural memory stores."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import replace
from .models import MemoryKind, MemoryRecord

class MemoryStore:
    def __init__(self) -> None:
        self._records: dict[MemoryKind, list[MemoryRecord]] = defaultdict(list)
    def add(self, record: MemoryRecord) -> None:
        self._records[record.kind].append(record)
    def get(self, kind: MemoryKind) -> tuple[MemoryRecord, ...]:
        return tuple(self._records[kind])
    def search(self, kind: MemoryKind, tag: str) -> tuple[MemoryRecord, ...]:
        return tuple(r for r in self._records[kind] if tag in r.tags)
    def verify_related(self, capability: str) -> int:
        changed = 0
        for kind in (MemoryKind.SEMANTIC, MemoryKind.PROCEDURAL):
            updated = []
            for record in self._records[kind]:
                if capability in record.tags and not record.verified:
                    record = replace(record, verified=True)
                    changed += 1
                updated.append(record)
            self._records[kind] = updated
        return changed
    def inherit_verified(self, records: tuple[MemoryRecord, ...], child_id: str, generation: int) -> int:
        copied = 0
        for record in records:
            if record.verified:
                self.add(MemoryRecord(record.kind, dict(record.content), child_id, generation, record.tags, True))
                copied += 1
        return copied
    def counts(self) -> dict[str, int]:
        return {kind.value: len(self._records[kind]) for kind in MemoryKind}
