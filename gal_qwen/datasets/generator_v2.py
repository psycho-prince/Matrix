"""Deterministic synthetic dataset generator conforming to GAL Protocol 2.1."""
from __future__ import annotations

import random
from typing import Any, Dict, List

from .schema import make_fact
from .validation import validate_dataset


def generate_full_dataset_pipeline(seed: int = 42) -> Dict[str, Any]:
    """Generate D1 acquisition, D2 verification and answer-isolated D3 evaluation."""
    rng = random.Random(seed)  # never mutates process-global random state

    entities = [
        ("entity-01", "group-01", "sector-01"),
        ("entity-02", "group-02", "sector-02"),
        ("entity-03", "group-01", "sector-02"),
    ]
    group_traits = {"group-01": "conductive", "group-02": "insulating"}
    sector_climates = {"sector-01": "cold", "sector-02": "warm"}

    d1: List[Dict[str, Any]] = []
    d2: List[Dict[str, Any]] = []
    for index, (entity_id, group_id, sector_id) in enumerate(entities, start=1):
        d1.append(make_fact(
            fact_id=f"D1-F{index:03d}", entity_id=entity_id, group_id=group_id,
            property=group_id, relation="belongs_to_group", verified=True,
            acquisition_round=1,
        ))
        d1.append(make_fact(
            fact_id=f"D1-S{index:03d}", entity_id=entity_id, group_id=None,
            property=sector_id, relation="originates_in_sector", verified=True,
            acquisition_round=1,
        ))

    for index, (group_id, trait) in enumerate(group_traits.items(), start=1):
        d2.append(make_fact(
            fact_id=f"D2-G{index:03d}", entity_id="", group_id=group_id,
            property=trait, relation="group_has_trait", verified=True,
            acquisition_round=2,
        ))
    for index, (sector_id, climate) in enumerate(sector_climates.items(), start=1):
        d2.append(make_fact(
            fact_id=f"D2-C{index:03d}", entity_id="", group_id=sector_id,
            property=climate, relation="sector_has_climate", verified=True,
            acquisition_round=2,
        ))

    # All tasks require multi-hop evidence. The answer is derived from a path,
    # not repeated as a direct entity->answer fact in D1/D2.
    selected = rng.sample(entities, k=len(entities))
    ground_truth = []
    for index, (entity_id, group_id, sector_id) in enumerate(selected, start=1):
        trait = group_traits[group_id]
        climate = sector_climates[sector_id]
        group_fact = next(f["fact_id"] for f in d1
                          if f["entity_id"] == entity_id and f["relation"] == "belongs_to_group")
        sector_fact = next(f["fact_id"] for f in d1
                           if f["entity_id"] == entity_id and f["relation"] == "originates_in_sector")
        trait_fact = next(f["fact_id"] for f in d2
                          if f["group_id"] == group_id and f["relation"] == "group_has_trait")
        climate_fact = next(f["fact_id"] for f in d2
                            if f["group_id"] == sector_id and f["relation"] == "sector_has_climate")
        if index % 2:
            question_id = f"Q{index:03d}"
            question_text = f"What group-level trait is inherited by {entity_id}?"
            answer = trait
            evidence_path = [group_fact, trait_fact]
            target_group_id = group_id
        else:
            question_id = f"Q{index:03d}"
            question_text = f"What climate applies to {entity_id} through its sector of origin?"
            answer = climate
            evidence_path = [sector_fact, climate_fact]
            target_group_id = sector_id
        ground_truth.append({
            "question_id": question_id,
            "question_text": question_text,
            "evidence_path": evidence_path,
            "answer": answer,  # scorer-only; removed by evaluation_tasks()
            "answer_withheld": True,
            "target_entity_id": entity_id,
            "target_group_id": target_group_id,
        })

    dataset = {
        "protocol_version": "2.1",
        "seed": seed,
        "acquisition": {"split_id": "D1", "facts": d1},
        "verification": {"split_id": "D2", "facts": d2},
        "evaluation": {"split_id": "D3", "ground_truth": ground_truth},
        "split_manifest": {
            "d1": [fact["fact_id"] for fact in d1],
            "d2": [fact["fact_id"] for fact in d2],
            "d3": [item["question_id"] for item in ground_truth],
            "seed": seed,
        },
    }
    validate_dataset(dataset)
    return dataset
