"""Deterministic acceptance tests for the GAL Protocol 2.1 data contract."""
import copy
import random

import pytest

from gal_qwen.datasets.generator_v2 import generate_full_dataset_pipeline
from gal_qwen.datasets.leakage_auditor import detect_leakage, has_critical_leakage
from gal_qwen.datasets.schema import evaluation_tasks
from gal_qwen.datasets.validation import ContractError, validate_dataset


def test_generated_dataset_passes_contract():
    dataset = generate_full_dataset_pipeline(7300)
    report = validate_dataset(dataset)
    assert report["valid"] is True
    assert report["n_evaluation"] == 3


def test_answer_is_absent_from_model_facing_tasks():
    dataset = generate_full_dataset_pipeline(7300)
    tasks = evaluation_tasks(dataset["evaluation"])
    assert len(tasks) == len(dataset["evaluation"]["ground_truth"])
    assert all("answer" not in task for task in tasks)
    assert [t["question_id"] for t in tasks] == [
        g["question_id"] for g in dataset["evaluation"]["ground_truth"]
    ]


def test_question_id_mapping_is_unique_and_bijective():
    dataset = generate_full_dataset_pipeline(7300)
    gt = dataset["evaluation"]["ground_truth"]
    assert len({item["question_id"] for item in gt}) == len(gt)
    assert len({item["question_id"]: item["answer"] for item in gt}) == len(gt)


def test_duplicate_question_id_fails_hard():
    dataset = generate_full_dataset_pipeline(7300)
    dataset["evaluation"]["ground_truth"].append(
        copy.deepcopy(dataset["evaluation"]["ground_truth"][0])
    )
    with pytest.raises(ContractError, match="question_id must be unique"):
        validate_dataset(dataset)


def test_unknown_evidence_path_fails_hard():
    dataset = generate_full_dataset_pipeline(7300)
    dataset["evaluation"]["ground_truth"][0]["evidence_path"] = ["NO-SUCH-FACT"]
    with pytest.raises(ContractError, match="unknown evidence IDs"):
        validate_dataset(dataset)


def test_global_random_state_is_not_mutated():
    random.seed(123)
    before = random.getstate()
    generate_full_dataset_pipeline(7300)
    assert random.getstate() == before


def test_generic_answer_word_overlap_is_not_leakage():
    dataset = generate_full_dataset_pipeline(7300)
    # Add an unrelated fact containing the answer word but not the target tuple.
    answer = dataset["evaluation"]["ground_truth"][0]["answer"]
    dataset["acquisition"]["facts"].append({
        "fact_id": "D1-UNRELATED", "entity_id": "entity-unrelated",
        "group_id": "group-unrelated", "relation": "describes",
        "property": answer, "source": "generated", "verified": True,
        "acquisition_round": 1,
    })
    findings = detect_leakage(dataset["acquisition"], dataset["verification"],
                              dataset["evaluation"])
    assert not has_critical_leakage(findings)


def test_direct_answer_fact_exposure_is_detected():
    dataset = generate_full_dataset_pipeline(7300)
    item = dataset["evaluation"]["ground_truth"][0]
    dataset["acquisition"]["facts"].append({
        "fact_id": "D1-DIRECT", "entity_id": item["target_entity_id"],
        "group_id": item["target_group_id"], "relation": "has_property",
        "property": item["answer"], "source": "generated", "verified": True,
        "acquisition_round": 1,
    })
    findings = detect_leakage(dataset["acquisition"], dataset["verification"],
                              dataset["evaluation"])
    assert any(f["classification"] == "direct_answer_fact_exposure"
               for f in findings)
    assert has_critical_leakage(findings)
