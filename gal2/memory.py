"""Separated memory stores with source provenance and isolated transfer lineage."""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import replace

from .models import MemoryKind, MemoryRecord


class MemoryStore:
    """A memory store that does not expose mutable internal record contents.

    MemoryRecord is frozen, but its content field is a dictionary. Therefore
    copying only the dataclass is insufficient: nested dictionaries and lists
    must also be copied at every store boundary.
    """

    def __init__(self):
        self._records: dict[MemoryKind, list[MemoryRecord]] = defaultdict(list)

    def add(self, record: MemoryRecord) -> None:
        """Store an isolated snapshot of a record."""
        self._records[record.kind].append(
            replace(record, content=deepcopy(record.content))
        )

    def get(self, kind: MemoryKind) -> tuple[MemoryRecord, ...]:
        """Return detached snapshots; callers cannot mutate stored state."""
        return tuple(deepcopy(self._records[kind]))

    def search(self, kind: MemoryKind, tag: str) -> tuple[MemoryRecord, ...]:
        """Search by tag and return detached snapshots."""
        matches = (record for record in self._records[kind] if tag in record.tags)
        return tuple(deepcopy(tuple(matches)))

    def verify_related(self, capability: str) -> int:
        """Legacy tag-based helper; this is not independent semantic verification."""
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

    def inherit_verified(
        self,
        records: tuple[MemoryRecord, ...] | list[MemoryRecord],
        child_id: str,
        generation: int,
    ) -> int:
        """Copy verified records and append the immediate donor to lineage.

        source_agent remains the original creator. custodian_agent identifies
        the current holder. lineage records each successive donor, so a
        parent -> child -> grandchild transfer becomes
        (parent_id, child_id), not (parent_id, parent_id).
        """
        copied = 0
        for record in records:
            if not record.verified:
                continue
            donor_id = record.custodian_agent or record.source_agent
            self.add(
                MemoryRecord(
                    kind=record.kind,
                    content=deepcopy(record.content),
                    source_agent=record.source_agent,
                    generation=record.generation,
                    tags=record.tags,
                    verified=True,
                    custodian_agent=child_id,
                    lineage=record.lineage + (donor_id,),
                )
            )
            copied += 1
        return copied

    def counts(self) -> dict[str, int]:
        return {kind.value: len(self._records[kind]) for kind in MemoryKind}
