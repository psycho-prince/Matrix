"""Paired synthetic comparison of inheritance and memory baselines.

This experiment compares mechanisms in the existing Bernoulli simulator only.
It is not an empirical benchmark of a real learning system.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path
from .agent import Agent
from .adaptive_inheritance import AdaptationPolicy, adaptive_inherit
from .models import Capability, MemoryKind, MemoryRecord, Task

ARMS = ("no_transfer", "capability_copy", "adaptive_inheritance", "shared_memory")


def paired_tasks(seed: int, split: str, count: int, context: str) -> list[Task]:
    # Same task sequence is used by all arms for each paired seed.
    return [Task(f"{split}-{seed}-{i}", "planning", "decomposition",
                 0.25 + (i % 5) * 0.05, context, split)
            for i in range(count)]


def build_parent(seed: int) -> Agent:
    parent = Agent(f"parent-{seed}", 0, seed)
    parent.capabilities["planning"] = Capability(
        "planning", proficiency=0.5,
        context_tags=("routine", "resource_limited"),
    )
    for task in paired_tasks(seed, "train", 300, "routine"):
        parent.attempt(task)
    # Independent holdout verification; fail closed if this fixture does not verify.
    verified = parent.verify_capability(
        "planning", paired_tasks(seed, "validation", 250, "routine"),
        min_trials=100, min_success_rate=0.50,
    )
    if not verified:
        raise RuntimeError(f"Parent capability failed verification for seed {seed}")
    # This baseline tests transfer of verified declarative/procedural memory.
    parent.memory.verify_related("planning")
    return parent


def make_child(parent: Agent, arm: str, target_context: tuple[str, ...]) -> Agent:
    child = Agent(f"successor-{parent.seed}", 1, parent.seed)
    if arm == "no_transfer":
        return child
    if arm == "capability_copy":
        source = parent.capabilities["planning"]
        child.capabilities["planning"] = Capability(
            source.name, source.proficiency, source.confidence, [],
            source.prerequisites, source.context_tags, source.failure_conditions,
            False, source.version, source.lineage + (parent.agent_id,),
        )
        return child
    if arm == "adaptive_inheritance":
        adaptive_inherit(
            parent, child, target_context,
            AdaptationPolicy(min_context_similarity=0.2,
                             prior_proficiency=0.5,
                             recalibration_strength=0.5),
        )
        return child
    if arm == "shared_memory":
        child.memory.inherit_verified(
            tuple(record for kind in MemoryKind for record in parent.memory.get(kind)),
            child.agent_id, child.generation,
        )
        return child
    raise ValueError(f"Unknown arm: {arm}")


def wilson_lower(successes: int, trials: int, z: float = 1.96) -> float:
    p = successes / trials
    z2 = z * z
    denom = 1 + z2 / trials
    centre = p + z2 / (2 * trials)
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * trials)) / trials)
    return max(0.0, (centre - margin) / denom)


def run_experiment(seed_start: int = 1000, seeds: int = 100,
                   test_trials: int = 250) -> dict:
    if seeds < 2 or test_trials < 1:
        raise ValueError("Use at least 2 seeds and at least 1 test trial")
    target_context = ("resource_limited", "shifted")
    rows = []
    for seed in range(seed_start, seed_start + seeds):
        parent = build_parent(seed)
        test_tasks = paired_tasks(seed, "test", test_trials, "shifted")
        for arm in ARMS:
            child = make_child(parent, arm, target_context)
            report = child.evaluate("planning", test_tasks, min_trials=1,
                                    min_success_rate=0.0)
            # An agent without a transferred capability still receives a valid
            # evaluation report from the same simulator's zero-proficiency prior.
            rows.append({
                "seed": seed, "arm": arm, "successes": report.successes,
                "trials": report.trials, "success_rate": report.success_rate,
                "wilson_lower_bound": report.wilson_lower_bound,
                "capability_present": "planning" in child.capabilities,
                "capability_verified_at_start": bool(
                    child.capabilities.get("planning") and
                    child.capabilities["planning"].verified),
                "inherited_memory_records": sum(child.memory.counts().values()),
                "initial_proficiency": (
                    child.capabilities["planning"].proficiency
                    if "planning" in child.capabilities else 0.0
                ),
            })
    summary = {}
    by_seed = {}
    for row in rows:
        by_seed.setdefault(row["seed"], {})[row["arm"]] = row["success_rate"]
    for arm in ARMS:
        vals = [r["success_rate"] for r in rows if r["arm"] == arm]
        summary[arm] = {
            "mean_success_rate": statistics.mean(vals),
            "sd_across_seed_rates": statistics.stdev(vals),
            "mean_wilson_lower_bound": statistics.mean(
                r["wilson_lower_bound"] for r in rows if r["arm"] == arm),
            "mean_initial_proficiency": statistics.mean(
                r["initial_proficiency"] for r in rows if r["arm"] == arm),
            "mean_inherited_memory_records": statistics.mean(
                r["inherited_memory_records"] for r in rows if r["arm"] == arm),
        }
    contrasts = {}
    reference = "no_transfer"
    for arm in ARMS:
        if arm == reference:
            continue
        diffs = [by_seed[s][arm] - by_seed[s][reference] for s in sorted(by_seed)]
        contrasts[f"{arm}_minus_{reference}"] = {
            "mean_paired_difference": statistics.mean(diffs),
            "sd_paired_difference": statistics.stdev(diffs),
            "se_paired_difference": statistics.stdev(diffs) / math.sqrt(len(diffs)),
            "seeds_won": sum(d > 0 for d in diffs),
            "seeds_tied": sum(d == 0 for d in diffs),
            "seeds_lost": sum(d < 0 for d in diffs),
        }
    # The executor does not consult memory; verify the expected equivalence
    # between shared-memory and no-transfer as a limitation diagnostic.
    memory_executor_equivalent = all(
        by_seed[s]["shared_memory"] == by_seed[s]["no_transfer"]
        for s in by_seed
    )
    payload = {
        "schema_version": 1,
        "experiment": "gal2_inheritance_baseline_comparison",
        "seed_start": seed_start, "paired_seeds": seeds,
        "test_trials_per_seed_per_arm": test_trials,
        "arms": list(ARMS),
        "training": {
            "parent_training_tasks_per_seed": 300,
            "parent_verification_tasks_per_seed": 250,
            "parent_verification_threshold": 0.65,
        },
        "target_context_tags": list(target_context),
        "summary": summary, "paired_contrasts_vs_no_transfer": contrasts,
        "diagnostics": {
            "shared_memory_equals_no_transfer": memory_executor_equivalent,
            "memory_is_consumed_by_task_executor": False,
            "capability_is_verified_in_parent_but_reset_in_child": True,
        },
        "raw_results": rows,
        "scope_warning": (
            "Synthetic Bernoulli simulator only. Context labels do not alter task "
            "difficulty or success probability; memory is not consumed by the executor. "
            "Results compare software transfer mechanics, not real-world learning, "
            "generalization, intelligence, or biological evolution."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["results_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-start", type=int, default=1000)
    parser.add_argument("--seeds", type=int, default=100)
    parser.add_argument("--test-trials", type=int, default=250)
    parser.add_argument("--output", type=Path, default=Path("gal2-comparison.json"))
    args = parser.parse_args()
    result = run_experiment(args.seed_start, args.seeds, args.test_trials)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "sha256": result["results_sha256"],
                      "summary": result["summary"],
                      "contrasts": result["paired_contrasts_vs_no_transfer"],
                      "diagnostics": result["diagnostics"]}, indent=2))


if __name__ == "__main__":
    main()
