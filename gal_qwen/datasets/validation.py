"""Deterministic hard-gate validation for GAL Protocol 2.1 datasets."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Iterable, List

from .schema import REQUIRED_FACT_FIELDS, REQUIRED_QUESTION_FIELDS, evaluation_tasks


class ContractError(ValueError):
    """Raised when a dataset violates the Protocol 2.1 contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _validate_facts(records: Iterable[Dict[str, Any]], split: str) -> None:
    seen = set()
    for index, fact in enumerate(records):
        missing = REQUIRED_FACT_FIELDS - set(fact)
        _require(not missing, f"{split}[{index}] missing fields: {sorted(missing)}")
        _require(bool(fact["fact_id"]), f"{split}[{index}] has empty fact_id")
        _require(fact["fact_id"] not in seen, f"{split} duplicate fact_id: {fact['fact_id']}")
        seen.add(fact["fact_id"])
        _require(fact["source"] == "generated", f"{split} fact source must be 'generated'")
        _require(isinstance(fact["verified"], bool), f"{split} verified must be bool")
        _require(isinstance(fact["acquisition_round"], int) and fact["acquisition_round"] >= 0,
                 f"{split} acquisition_round must be a non-negative integer")
        _require(bool(fact["entity_id"]) or bool(fact["group_id"]),
                 f"{split} fact must identify an entity or group")
        _require(bool(fact["property"]), f"{split} property must be non-empty")


def validate_dataset(dataset: Dict[str, Any]) -> Dict[str, Any]:
    """Validate shape, IDs, split boundaries, answer bijection and oracle isolation."""
    _require(dataset.get("protocol_version") == "2.1", "protocol_version must be '2.1'")
    for key in ("acquisition", "verification", "evaluation", "split_manifest"):
        _require(key in dataset, f"missing top-level key: {key}")

    acquisition = dataset["acquisition"]
    verification = dataset["verification"]
    evaluation = dataset["evaluation"]
    _validate_facts(acquisition["facts"], "acquisition.facts")
    _validate_facts(verification["facts"], "verification.facts")

    gt = evaluation.get("ground_truth")
    _require(isinstance(gt, list) and gt, "evaluation.ground_truth must be a non-empty list")
    ids = [item.get("question_id") for item in gt]
    duplicates = [qid for qid, count in Counter(ids).items() if count != 1]
    _require(not duplicates and all(ids), f"question_id must be unique and non-empty: {duplicates}")
    for index, item in enumerate(gt):
        missing = REQUIRED_QUESTION_FIELDS - set(item)
        _require(not missing, f"ground_truth[{index}] missing fields: {sorted(missing)}")
        _require(bool(item["question_text"]), f"ground_truth[{index}] question_text is empty")
        _require(bool(item["answer"]), f"ground_truth[{index}] answer is empty")
        _require(item["answer_withheld"] is True, "answer_withheld must be true")
        _require(isinstance(item["evidence_path"], list) and item["evidence_path"],
                 f"ground_truth[{index}] evidence_path must be a non-empty list")

    # Bijection: every task ID occurs once and maps to exactly one scorer answer.
    ground_truth_map = {item["question_id"]: item["answer"] for item in gt}
    _require(len(ground_truth_map) == len(gt), "ground_truth_map is not bijective")
    tasks = evaluation_tasks(evaluation)
    task_ids = [task["question_id"] for task in tasks]
    _require(task_ids == ids, "model-facing tasks do not preserve ground-truth question order/IDs")
    _require(all("answer" not in task for task in tasks), "answer leaked into model-facing task")
    _require(all(task["answer_withheld"] is True for task in tasks),
             "model-facing task must mark answer_withheld=true")

    manifest = dataset["split_manifest"]
    _require(manifest.get("d1") == [f["fact_id"] for f in acquisition["facts"]],
             "split_manifest.d1 does not match acquisition IDs")
    _require(manifest.get("d2") == [f["fact_id"] for f in verification["facts"]],
             "split_manifest.d2 does not match verification IDs")
    _require(manifest.get("d3") == ids, "split_manifest.d3 does not match evaluation IDs")
    all_fact_ids = {f["fact_id"] for f in acquisition["facts"] + verification["facts"]}
    for item in gt:
        unknown = set(item["evidence_path"]) - all_fact_ids
        _require(not unknown, f"{item['question_id']} references unknown evidence IDs: {sorted(unknown)}")

    return {
        "valid": True,
        "protocol_version": "2.1",
        "n_acquisition": len(acquisition["facts"]),
        "n_verification": len(verification["facts"]),
        "n_evaluation": len(gt),
        "ground_truth_map": ground_truth_map,
    }
