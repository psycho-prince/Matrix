"""Small mechanism-audited pilot of the original population GAL model.

This runner deliberately calls the repository's original Agent.develop,
Agent.inherit, Agent.learn_independently and Agent.work methods. It adds
observation only; it does not replace the inheritance or learning mechanism.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from gal.agents.agent import Agent
from gal.environment.world import Environment

MODES = ("A", "B-copy", "C-full", "C-no-memory", "C-low-effort")


def snapshot(agent):
    return {
        "identity": agent.identity,
        "generation": agent.generation,
        "skills": dict(agent.skills),
        "concepts": sorted(agent.knowledge_concepts),
        "tasks_attempted": agent.tasks_attempted,
        "tasks_succeeded": agent.tasks_succeeded,
        "success_rate": agent.task_success_rate,
    }


class ObservedTask:
    def __init__(self, task, record):
        self._task = task
        self._record = record
        self.name = task.name
        self.required_skill = task.required_skill
        self.difficulty = task.difficulty
        self.associated_concept = task.associated_concept

    def attempt(self, skill, concepts, rng):
        success = self._task.attempt(skill, concepts, rng)
        self._record(self.name, success)
        return success


class ObservedEnvironment:
    def __init__(self, environment, record):
        self._environment = environment
        self._record = record

    def get_random_task(self, rng):
        return ObservedTask(self._environment.get_random_task(rng), self._record)


def run_seed(mode, seed, agents_n, generations):
    world = Environment()
    previous = []
    records = []
    generations_out = []

    for gen in range(1, generations + 1):
        current = [
            Agent(identity=f"PILOT-{mode}-S{seed}-G{gen}-A{i:03d}",
                  generation=gen, universe_seed=seed)
            for i in range(agents_n)
        ]
        inheritance_events = []

        if previous:
            for i, child in enumerate(current):
                parent = previous[i % len(previous)]
                parent_before = snapshot(parent)
                child_before = snapshot(child)
                child.parents.append(parent.identity)
                parent.successor = child.identity
                child.inherit(parent, mode)
                child_after_inherit = snapshot(child)
                inheritance_events.append({
                    "parent": parent_before,
                    "child_before": child_before,
                    "child_after_inherit": child_after_inherit,
                    "mode": mode,
                    "one_to_one_parent_index": i % len(previous),
                })

        task_counts = defaultdict(lambda: {"attempted": 0, "succeeded": 0})
        agent_task_counts = defaultdict(lambda: defaultdict(lambda: {"attempted": 0, "succeeded": 0}))
        active_agent = {"identity": None}

        def record_task(task_name, success):
            task_counts[task_name]["attempted"] += 1
            task_counts[task_name]["succeeded"] += int(success)
            item = agent_task_counts[active_agent["identity"]][task_name]
            item["attempted"] += 1
            item["succeeded"] += int(success)

        observed_world = ObservedEnvironment(world, record_task)

        for agent in current:
            agent.develop()
            for _ in range(5):
                agent.learn_independently(observed_world)
                active_agent["identity"] = agent.identity
                agent.work(observed_world, num_tasks=10)

        population = [snapshot(a) for a in current]
        gen_success = float(np.mean([a["success_rate"] for a in population]))
        task_rates = {
            name: (counts["succeeded"] / counts["attempted"] if counts["attempted"] else 0.0)
            for name, counts in task_counts.items()
        }
        gen_record = {
            "generation": gen,
            "population_mean_success": gen_success,
            "population": population,
            "task_counts": dict(task_counts),
            "task_success_rates": task_rates,
            "agent_task_counts": {
                agent_id: dict(counts) for agent_id, counts in agent_task_counts.items()
            },
            "inheritance_events": inheritance_events,
            "mean_skill_levels": {
                skill: float(np.mean([agent.skills[skill] for agent in current]))
                for skill in current[0].skills
            },
            "mean_concept_count": float(np.mean([len(a.knowledge_concepts) for a in current])),
        }
        generations_out.append(gen_record)
        previous = current

    return {
        "mode": mode,
        "seed": seed,
        "agents_per_generation": agents_n,
        "generations": generations,
        "generation_records": generations_out,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--agents", type=int, default=20)
    parser.add_argument("--generations", type=int, default=4)
    parser.add_argument("--out", default="artifacts/native_gal_pilot")
    args = parser.parse_args()
    if args.seeds < 2 or args.agents < 2 or args.generations < 2:
        raise SystemExit("Pilot requires at least 2 seeds, agents and generations")

    out = Path(args.out)
    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "study": "native GAL mechanism-audited pilot",
        "model": "original gal.agents.agent.Agent + gal.environment.world.Environment",
        "pilot_only": True,
        "confirmatory": False,
        "seeds": args.seeds,
        "agents_per_generation": args.agents,
        "generations": args.generations,
        "modes": {},
        "mechanism_audit": {},
    }

    results = {mode: [] for mode in MODES}
    for mode in MODES:
        for seed in range(args.seeds):
            result = run_seed(mode, seed, args.agents, args.generations)
            results[mode].append(result)
            (raw_dir / f"{mode}_seed_{seed:03d}.json").write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n"
            )

    for mode, runs in results.items():
        trajectories = np.asarray([
            [g["population_mean_success"] for g in r["generation_records"]]
            for r in runs
        ])
        report["modes"][mode] = {
            "generation_mean_success": trajectories.mean(axis=0).tolist(),
            "generation_sd_across_seeds": trajectories.std(axis=0, ddof=1).tolist(),
            "seed_level_generation_trajectories": trajectories.tolist(),
        }

    # Audit the actual transferred state before the child starts independent learning.
    for mode, runs in results.items():
        events = [
            event
            for run in runs
            for generation in run["generation_records"]
            for event in generation["inheritance_events"]
        ]
        skill_exact = 0
        concept_exact = 0
        no_parent_state = 0
        teaching_concept_transfer = 0
        skill_values_valid = True
        for event in events:
            parent = event["parent"]
            inherited = event["child_after_inherit"]
            if inherited["skills"] == parent["skills"]:
                skill_exact += 1
            if inherited["concepts"] == parent["concepts"]:
                concept_exact += 1
            if inherited["skills"] == event["child_before"]["skills"] and inherited["concepts"] == event["child_before"]["concepts"]:
                no_parent_state += 1
            if set(parent["concepts"]).issubset(set(inherited["concepts"])):
                teaching_concept_transfer += 1
            skill_values_valid &= all(0.0 <= v <= 1.0 for v in inherited["skills"].values())
        report["mechanism_audit"][mode] = {
            "inheritance_events": len(events),
            "exact_skill_copy_events": skill_exact,
            "exact_concept_copy_events": concept_exact,
            "unchanged_from_child_initialization_events": no_parent_state,
            "parent_concepts_retained_events": teaching_concept_transfer,
            "skill_bounds_valid": bool(skill_values_valid),
        }

    # Expected invariants for this implementation; fail closed on a mechanism mismatch.
    if report["mechanism_audit"]["A"]["unchanged_from_child_initialization_events"] != report["mechanism_audit"]["A"]["inheritance_events"]:
        raise AssertionError("Mode A unexpectedly inherited parent state")
    if report["mechanism_audit"]["B-copy"]["exact_skill_copy_events"] != report["mechanism_audit"]["B-copy"]["inheritance_events"]:
        raise AssertionError("B-copy failed exact skill transfer")
    if report["mechanism_audit"]["B-copy"]["exact_concept_copy_events"] != report["mechanism_audit"]["B-copy"]["inheritance_events"]:
        raise AssertionError("B-copy failed exact concept transfer")
    if report["mechanism_audit"]["C-no-memory"]["parent_concepts_retained_events"] != 0:
        raise AssertionError("C-no-memory unexpectedly transferred parent concepts")
    if not all(v["skill_bounds_valid"] for v in report["mechanism_audit"].values()):
        raise AssertionError("Skill value outside [0, 1]")

    (out / "pilot_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
