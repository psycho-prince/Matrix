"""Memory-grounded inheritance benchmark for GAL 2.0.

Run from the repository root:
    python -m gal2.memory_grounded_benchmark --seeds 100 --tasks-per-seed 30

This benchmark uses the repository's real MemoryStore/MemoryRecord classes.
It is a deterministic symbolic solver adapter, not an LLM evaluation and not
a claim that GAL's native Agent.evaluate consumes memory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
from dataclasses import replace
from pathlib import Path
from typing import Any

from .memory import MemoryStore
from .models import MemoryKind, MemoryRecord

ARMS = (
    "no_transfer",
    "capability_only",
    "episodic_only",
    "semantic_procedural",
    "combined",
    "corrupted_memory",
    "oracle",
)


def make_rulebook(rng: random.Random) -> dict[str, dict[str, int | str]]:
    """Generate a per-seed mapping from opaque symbols to arithmetic rules."""
    symbols = ("K", "M", "Q")
    operations = ("add", "subtract", "multiply")
    rules: dict[str, dict[str, int | str]] = {}
    used: set[tuple[str, int]] = set()
    for symbol in symbols:
        while True:
            operation = rng.choice(operations)
            amount = rng.randint(2, 5)
            if operation == "multiply" and amount == 1:
                continue
            candidate = (operation, amount)
            if candidate not in used:
                used.add(candidate)
                rules[symbol] = {"operation": operation, "amount": amount}
                break
    return rules


def apply_rule(value: int, rule: dict[str, int | str]) -> int:
    operation = rule["operation"]
    amount = int(rule["amount"])
    if operation == "add":
        return value + amount
    if operation == "subtract":
        return value - amount
    if operation == "multiply":
        return value * amount
    raise ValueError(f"Unsupported operation: {operation}")


def make_tasks(rng: random.Random, count: int, rules: dict) -> list[dict[str, Any]]:
    tasks = []
    for index in range(count):
        seed_value = rng.randint(1, 12)
        sequence = [rng.choice(tuple(rules)) for _ in range(rng.randint(2, 5))]
        answer = seed_value
        for symbol in sequence:
            answer = apply_rule(answer, rules[symbol])
        tasks.append({
            "task_id": f"task-{index:04d}",
            "seed": seed_value,
            "sequence": sequence,
            "answer": answer,
        })
    return tasks


def make_parent_store(parent_id: str, generation: int, rules: dict) -> MemoryStore:
    store = MemoryStore()
    store.add(MemoryRecord(
        MemoryKind.EPISODIC,
        {"observation": "parent completed symbolic-operation practice",
         "practice_count": 20},
        parent_id, generation, ("practice", "experience"), True,
    ))
    store.add(MemoryRecord(
        MemoryKind.SEMANTIC,
        {"rulebook": rules},
        parent_id, generation, ("symbolic-rulebook", "operation-mapping"), True,
    ))
    store.add(MemoryRecord(
        MemoryKind.PROCEDURAL,
        {"procedure": "apply each symbol's operation to the running value from left to right"},
        parent_id, generation, ("left-to-right", "procedure"), True,
    ))
    return store


def inherit_arm(parent: MemoryStore, arm: str, child_id: str, generation: int) -> MemoryStore:
    child = MemoryStore()
    selected = []
    for kind in MemoryKind:
        records = parent.get(kind)
        if arm == "episodic_only" and kind == MemoryKind.EPISODIC:
            selected.extend(records)
        elif arm == "semantic_procedural" and kind in (MemoryKind.SEMANTIC, MemoryKind.PROCEDURAL):
            selected.extend(records)
        elif arm == "combined":
            selected.extend(records)
        elif arm == "corrupted_memory" and kind in (MemoryKind.SEMANTIC, MemoryKind.PROCEDURAL):
            selected.extend(records)
    child.inherit_verified(tuple(selected), child_id, generation)

    if arm == "corrupted_memory":
        # Deliberately simulate an undetected corruption after transfer:
        # the altered record remains marked verified. This is an adversarial
        # stress control, not a claim that the normal transfer path corrupts it.
        semantic = list(child.get(MemoryKind.SEMANTIC))
        if semantic:
            record = semantic[0]
            changed = dict(record.content)
            rules = dict(changed["rulebook"])
            first_symbol = sorted(rules)[0]
            original = dict(rules[first_symbol])
            original["amount"] = int(original["amount"]) + 1
            rules[first_symbol] = original
            changed["rulebook"] = rules
            records = list(child.get(MemoryKind.SEMANTIC))
            child._records[MemoryKind.SEMANTIC] = [
                replace(item, content=changed) if item is record else item
                for item in records
            ]
    return child


def solve_from_memory(task: dict, store: MemoryStore) -> tuple[int | None, str]:
    semantic = store.search(MemoryKind.SEMANTIC, "symbolic-rulebook")
    procedural = store.search(MemoryKind.PROCEDURAL, "left-to-right")
    if not semantic or not procedural:
        return None, "abstain_missing_required_memory"
    rules = semantic[0].content.get("rulebook")
    if not isinstance(rules, dict):
        return None, "abstain_invalid_rulebook"
    value = int(task["seed"])
    try:
        for symbol in task["sequence"]:
            value = apply_rule(value, rules[symbol])
    except (KeyError, TypeError, ValueError):
        return None, "abstain_invalid_rule"
    return value, "memory_solved"


def run(seed_start: int = 91000, seeds: int = 100, tasks_per_seed: int = 30) -> dict:
    if seeds < 2 or tasks_per_seed < 1:
        raise ValueError("Require at least 2 paired seeds and 1 task per seed")
    raw: list[dict[str, Any]] = []
    paired: dict[int, dict[str, dict[str, float]]] = {}

    for seed in range(seed_start, seed_start + seeds):
        rng = random.Random(seed)
        rules = make_rulebook(rng)
        tasks = make_tasks(rng, tasks_per_seed, rules)
        parent = make_parent_store(f"parent-{seed}", 0, rules)
        paired[seed] = {}

        for arm in ARMS:
            child = inherit_arm(parent, arm, f"child-{seed}-{arm}", 1)
            correct = 0
            abstentions = 0
            incorrect = 0
            for task in tasks:
                if arm == "oracle":
                    prediction = task["seed"]
                    for symbol in task["sequence"]:
                        prediction = apply_rule(prediction, rules[symbol])
                    status = "oracle_solved"
                elif arm == "capability_only":
                    # Capability metadata is deliberately not a rule mapping.
                    # It cannot identify the opaque symbol semantics.
                    prediction, status = None, "abstain_no_symbol_mapping"
                else:
                    prediction, status = solve_from_memory(task, child)

                if prediction is None:
                    abstentions += 1
                elif prediction == task["answer"]:
                    correct += 1
                else:
                    incorrect += 1

            accuracy = correct / tasks_per_seed
            abstention_rate = abstentions / tasks_per_seed
            paired[seed][arm] = {
                "accuracy": accuracy,
                "abstention_rate": abstention_rate,
            }
            raw.append({
                "seed": seed,
                "arm": arm,
                "tasks": tasks_per_seed,
                "correct": correct,
                "incorrect": incorrect,
                "abstentions": abstentions,
                "accuracy": accuracy,
                "abstention_rate": abstention_rate,
                "memory_counts": child.counts(),
                "semantic_records_retrieved": len(child.search(
                    MemoryKind.SEMANTIC, "symbolic-rulebook")),
                "procedural_records_retrieved": len(child.search(
                    MemoryKind.PROCEDURAL, "left-to-right")),
            })

    summary: dict[str, Any] = {}
    for arm in ARMS:
        rows = [row for row in raw if row["arm"] == arm]
        rates = [row["accuracy"] for row in rows]
        abstentions = [row["abstention_rate"] for row in rows]
        summary[arm] = {
            "mean_accuracy": statistics.mean(rates),
            "sd_accuracy_across_seeds": statistics.stdev(rates),
            "mean_abstention_rate": statistics.mean(abstentions),
            "total_correct": sum(row["correct"] for row in rows),
            "total_incorrect": sum(row["incorrect"] for row in rows),
            "total_abstentions": sum(row["abstentions"] for row in rows),
        }

    contrasts = {}
    for arm in ARMS:
        if arm == "no_transfer":
            continue
        differences = [
            paired[seed][arm]["accuracy"] - paired[seed]["no_transfer"]["accuracy"]
            for seed in sorted(paired)
        ]
        contrasts[f"{arm}_minus_no_transfer"] = {
            "mean_paired_accuracy_difference": statistics.mean(differences),
            "sd_paired_difference": statistics.stdev(differences),
            "seeds_won": sum(value > 0 for value in differences),
            "seeds_tied": sum(value == 0 for value in differences),
            "seeds_lost": sum(value < 0 for value in differences),
        }

    report = {
        "schema_version": 1,
        "experiment": "gal2_memory_grounded_inheritance_benchmark",
        "status": "generated_when_executed",
        "design": {
            "seed_start": seed_start,
            "paired_seeds": seeds,
            "tasks_per_seed_per_arm": tasks_per_seed,
            "total_task_instances_per_arm": seeds * tasks_per_seed,
            "arms": list(ARMS),
            "task_distribution": "per-seed random arithmetic rulebooks and opaque symbol sequences",
        },
        "summary": summary,
        "paired_contrasts_vs_no_transfer": contrasts,
        "interpretation_guardrails": [
            "This is a symbolic benchmark, not a general-intelligence or AGI test.",
            "The solver is deterministic reference code, not a foundation-model evaluation.",
            "The oracle arm is an upper-bound control and is not an inherited-memory condition.",
            "Capability-only receives no symbol mapping; it tests whether capability metadata alone is sufficient.",
            "Corrupted memory is deliberately altered after transfer while retaining verified=true.",
            "This benchmark exercises MemoryStore, not Agent.evaluate's task executor.",
        ],
        "raw_results": raw,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["results_sha256"] = hashlib.sha256(canonical).hexdigest()
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=91000)
    parser.add_argument("--seeds", type=int, default=100)
    parser.add_argument("--tasks-per-seed", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("gal2_memory_grounded_results.json"))
    args = parser.parse_args()
    report = run(args.seed_start, args.seeds, args.tasks_per_seed)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "results_sha256": report["results_sha256"],
        "summary": report["summary"],
        "paired_contrasts_vs_no_transfer": report["paired_contrasts_vs_no_transfer"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
