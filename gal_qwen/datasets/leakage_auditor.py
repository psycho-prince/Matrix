"""Task-specific leakage audit for GAL Protocol 2.1.

The auditor compares canonical fact tuples and explicit evidence paths. It does
not infer leakage from generic answer-word overlap.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Set, Tuple


def canonical_fact(fact: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """Canonical semantic identity; IDs/provenance do not affect equivalence."""
    norm = lambda value: re.sub(r"\s+", " ", str(value or "").strip().casefold())
    return (norm(fact.get("entity_id")), norm(fact.get("group_id")),
            norm(fact.get("relation", "has_property")), norm(fact.get("property")))


def detect_leakage(acquisition: Dict[str, Any], verification: Dict[str, Any],
                   evaluation: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Inspect terminal answer facts and each question's explicit evidence path.

    A terminal fact is an exact semantic fact that directly states the answer
    for the evaluated entity/group. Intermediate evidence-path facts are
    reported as structural support, not automatically treated as answer leakage.
    """
    training = acquisition["facts"] + verification["facts"]
    by_id = {fact["fact_id"]: fact for fact in training}
    canonical_training = {canonical_fact(f): f for f in training}
    findings: List[Dict[str, Any]] = []

    for task in evaluation["ground_truth"]:
        qid = task["question_id"]
        path_ids = task["evidence_path"]
        missing = [fid for fid in path_ids if fid not in by_id]
        if missing:
            findings.append({
                "question_id": qid, "classification": "invalid_evidence_path",
                "severity": "high", "evidence_ids": missing,
            })
            continue

        # Only a fact matching the target entity/group AND the answer property
        # is direct answer disclosure. Generic word overlap is deliberately ignored.
        answer = re.sub(r"\s+", " ", str(task["answer"]).strip().casefold())
        direct_matches = [
            fact for fact in training
            if re.sub(r"\s+", " ", str(fact.get("property", "")).strip().casefold()) == answer
            and (fact.get("entity_id") == task.get("target_entity_id")
                 or fact.get("group_id") == task.get("target_group_id"))
        ]
        path_facts = [by_id[fid] for fid in path_ids]
        path_canonical = {canonical_fact(f) for f in path_facts}
        canonical_path_matches = [
            fact for fact in training if canonical_fact(fact) in path_canonical
        ]

        if direct_matches:
            findings.append({
                "question_id": qid, "classification": "direct_answer_fact_exposure",
                "severity": "high",
                "fact_ids": sorted({fact["fact_id"] for fact in direct_matches}),
            })
        else:
            findings.append({
                "question_id": qid, "classification": "no_direct_answer_fact_exposure",
                "severity": "pass",
            })

        findings.append({
            "question_id": qid, "classification": "evidence_path_inspected",
            "severity": "info", "evidence_ids": path_ids,
            "canonical_path_facts": len(canonical_path_matches),
        })

    return findings


def has_critical_leakage(findings: Iterable[Dict[str, Any]]) -> bool:
    return any(item.get("severity") == "high" for item in findings)
