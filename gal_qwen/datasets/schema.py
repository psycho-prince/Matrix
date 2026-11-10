"""Canonical GAL Protocol 2.1 data-contract constants and constructors.

The scorer-only answer is stored in evaluation.ground_truth. Model-facing tasks
are generated separately by evaluation_tasks(), which never includes answers.
"""
from __future__ import annotations

from typing import Any, Dict, List

PROTOCOL_VERSION = "2.1"
REQUIRED_FACT_FIELDS = {
    "fact_id", "entity_id", "group_id", "property", "source",
    "verified", "acquisition_round",
}
REQUIRED_QUESTION_FIELDS = {
    "question_id", "question_text", "evidence_path", "answer",
    "answer_withheld",
}


def make_fact(*, fact_id: str, entity_id: str, group_id: str | None,
              property: str, verified: bool, acquisition_round: int,
              relation: str = "has_property") -> Dict[str, Any]:
    """Create a normalized provenance-bearing fact record."""
    return {
        "fact_id": fact_id,
        "entity_id": entity_id,
        "group_id": group_id,
        "relation": relation,
        "property": property,
        "source": "generated",
        "verified": bool(verified),
        "acquisition_round": int(acquisition_round),
    }


def evaluation_tasks(evaluation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return model-facing task objects with scorer-only answers removed."""
    tasks = []
    for item in evaluation["ground_truth"]:
        tasks.append({
            "question_id": item["question_id"],
            "question_text": item["question_text"],
            "permitted_evidence": list(item["evidence_path"]),
            "answer_withheld": True,
        })
    return tasks
