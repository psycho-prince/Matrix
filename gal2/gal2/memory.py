"""Small in-memory stores with explicit separation of memory types."""
from __future__ import annotations

from collections import defaultdict
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

    def inherit_verified(self, records: tuple[MemoryRecord, ...], child_id: str, generation: int) -> int:
        """Copy only verified memory; preserve provenance and mark new owner."""
        copied = 0
        for record in records:
            if record.verified:
                self.add(MemoryRecord(
                    kind=record.kind,
                    content=dict(record.content),
                    source_agent=child_id,
                    generation=generation,
                    tags=record.tags,
                    verified=True,
                ))
                copied += 1
        return copied

    def counts(self) -> dict[str, int]:
        return {kind.value: len(self._records[kind]) for kind in MemoryKind}
