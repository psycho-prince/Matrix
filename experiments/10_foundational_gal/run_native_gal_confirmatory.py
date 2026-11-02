"""Pre-registered confirmatory run of the original symbolic GAL model.

This runner preserves the original Agent and Environment mechanisms. Raw records
are gzip-compressed JSONL; summary statistics are computed from paired seeds.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import platform
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from gal.agents.agent import Agent
from gal.environment.world import Environment

MODES = ("A", "B-copy", "C-full", "C-no-memory", "C-low-effort")
TASKS = ("resource_gathering", "shelter_building", "tool_making", "navigation", "problem_solving")
CONTRASTS = (("B-copy", "A"), ("C-full", "A"), ("C-no-memory", "A"),
             ("C-low-effort", "A"), ("B-copy", "C-full"))


def state(agent):
    return {"identity": agent.identity, "generation": agent.generation,
            "skills": dict(agent.skills), "concepts": sorted(agent.knowledge_concepts),
            "tasks_attempted": agent.tasks_attempted, "tasks_succeeded": agent.tasks_succeeded,
            "success_rate": agent.task_success_rate}


class TaskObserver:
    def __init__(self, task, callback):
        self.task, self.callback = task, callback
        for name in ("name", "required_skill", "difficulty", "associated_concept"):
            setattr(self, name, getattr(task, name))

    def attempt(self, skill, concepts, rng):
        success = self.task.attempt(skill, concepts, rng)
        self.callback(self.name, success)
        return success


class WorldObserver:
    def __init__(self, world, callback):
        self.world, self.callback = world, callback

    def get_random_task(self, rng):
        return TaskObserver(self.world.get_random_task(rng), self.callback)


def run_condition(mode: str, seed: int, agents_n: int, generations: int, raw_handle):
    world = Environment()
    previous = []
    seed_generation = []
    for gen in range(1, generations + 1):
        current = [Agent(identity=f"CONFIRM-S{seed}-G{gen}-A{i:03d}",
                         generation=gen, universe_seed=seed) for i in range(agents_n)]
        inheritance_events = []
        if previous:
            for i, child in enumerate(current):
                parent = previous[i]
                before = state(child)
                child.parents.append(parent.identity)
                parent.successor = child.identity
                child.inherit(parent, mode)
                after = state(child)
                inheritance_events.append({
                    "child": child.identity, "parent": parent.identity,
                    "parent_index": i, "child_before": {
                        "skills": before["skills"], "concepts": before["concepts"]},
                    "child_after_inherit": {
                        "skills": after["skills"], "concepts": after["concepts"]},
                })

        task_counts = {name: {"attempted": 0, "succeeded": 0} for name in TASKS}
        agent_task_counts = {}
        active = {"id": None}

        def record(name, success):
            item = task_counts[name]
            item["attempted"] += 1
            item["succeeded"] += int(success)
            a = agent_task_counts[active["id"]][name]
            a["attempted"] += 1
            a["succeeded"] += int(success)

        observed_world = WorldObserver(world, record)
        generation_agents = []
        for agent in current:
            agent.develop()
            agent_task_counts[agent.identity] = {
                name: {"attempted": 0, "succeeded": 0} for name in TASKS}
            cycle_states = []
            for cycle in range(5):
                agent.learn_independently(observed_world)
                active["id"] = agent.identity
                agent.work(observed_world, num_tasks=10)
                cycle_states.append({
                    "cycle": cycle + 1, "skills": dict(agent.skills),
                    "concept_count": len(agent.knowledge_concepts),
                    "tasks_attempted": agent.tasks_attempted,
                    "tasks_succeeded": agent.tasks_succeeded,
                })
            record_agent = state(agent)
            record_agent["cycle_states"] = cycle_states
            record_agent["task_counts"] = agent_task_counts[agent.identity]
            generation_agents.append(record_agent)

        success = float(np.mean([a["success_rate"] for a in generation_agents]))
        task_rates = {
            name: (v["succeeded"] / v["attempted"] if v["attempted"] else 0.0)
            for name, v in task_counts.items()}
        record = {
            "seed": seed, "mode": mode, "generation": gen,
            "population_mean_success": success,
            "task_counts": task_counts, "task_success_rates": task_rates,
            "population": generation_agents, "inheritance_events": inheritance_events,
            "mean_skills": {
                key: float(np.mean([a["skills"][key] for a in generation_agents]))
                for key in generation_agents[0]["skills"]},
            "mean_concept_count": float(np.mean([
                len(a["concepts"]) for a in generation_agents])),
            "task_concept_prevalence": {
                concept: float(np.mean([concept in a["concepts"] for a in generation_agents]))
                for concept in ("concept_42", "concept_108", "concept_7", "concept_99", "concept_314")},
        }
        raw_handle.write((json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n").encode())
        seed_generation.append(record)
        previous = current
    return seed_generation


def bootstrap_ci(values, rng, n=20000):
    values = np.asarray(values, dtype=float)
    draws = rng.choice(values, size=(n, len(values)), replace=True).mean(axis=1)
    return [float(np.quantile(draws, .025)), float(np.quantile(draws, .975))]


def holm_adjust(p_values):
    order = np.argsort(p_values)
    adjusted = np.empty(len(p_values), dtype=float)
    running = 0.0
    m = len(p_values)
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * float(p_values[idx]))
        adjusted[idx] = min(1.0, running)
    return adjusted.tolist()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=100)
    parser.add_argument("--agents", type=int, default=100)
    parser.add_argument("--generations", type=int, default=10)
    parser.add_argument("--out", default="artifacts/native_gal_confirmatory")
    args = parser.parse_args()
    if (args.seeds, args.agents, args.generations) != (100, 100, 10):
        raise SystemExit("Confirmatory protocol is fixed at 100 seeds x 100 agents x 10 generations")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    raw_path = out / "raw_records.jsonl.gz"
    results = {mode: [] for mode in MODES}
    with gzip.open(raw_path, "wb", compresslevel=6) as raw:
        for mode in MODES:
            for seed in range(args.seeds):
                generations = run_condition(mode, seed, args.agents, args.generations, raw)
                results[mode].append(generations)

    # Fail-closed completeness, exposure, and inheritance-mechanism checks.
    audit = {"expected_seed_mode_runs": 500, "observed_seed_mode_runs": sum(map(len, results.values())),
             "expected_generations": 5000, "observed_generations": sum(len(x) for v in results.values() for x in v),
             "errors": [], "mechanisms": {}}
    for mode, runs in results.items():
        events = [e for run in runs for g in run[1:] for e in g["inheritance_events"]]
        expected_events = args.seeds * (args.generations - 1) * args.agents
        if len(events) != expected_events:
            audit["errors"].append(f"{mode}: expected {expected_events} inheritance events, got {len(events)}")
        exact_skills = exact_concepts = unchanged = parent_concepts_retained = 0
        for e in events:
            p = next((a for a in []), None)  # Parent state is available in the preceding generation record.
            # Child-side mechanism invariants can be checked directly here.
            if e["child_after_inherit"]["skills"] == e["child_before"]["skills"] and e["child_after_inherit"]["concepts"] == e["child_before"]["concepts"]:
                unchanged += 1
            if mode == "B-copy":
                # Parent snapshot is resolved by identity from the previous generation below.
                pass
        for run in runs:
            for gi in range(1, len(run)):
                parent_by_id = {a["identity"]: a for a in run[gi-1]["population"]}
                for e in run[gi]["inheritance_events"]:
                    parent = parent_by_id[e["parent"]]
                    child = e["child_after_inherit"]
                    exact_skills += child["skills"] == parent["skills"]
                    exact_concepts += child["concepts"] == parent["concepts"]
                    parent_concepts_retained += set(parent["concepts"]).issubset(set(child["concepts"]))
                    if e["parent_index"] >= args.agents:
                        audit["errors"].append(f"{mode}: invalid parent index")
        if mode == "A" and unchanged != expected_events:
            audit["errors"].append("Mode A inheritance changed child state")
        if mode == "B-copy" and (exact_skills != expected_events or exact_concepts != expected_events):
            audit["errors"].append("B-copy exact state transfer failed")
        if mode == "C-no-memory" and parent_concepts_retained != 0:
            audit["errors"].append("C-no-memory transferred parent concepts")
        audit["mechanisms"][mode] = {
            "inheritance_events": len(events), "exact_skill_copy_events": int(exact_skills),
            "exact_concept_copy_events": int(exact_concepts),
            "unchanged_child_state_events": int(unchanged),
            "parent_concepts_retained_events": int(parent_concepts_retained)}
        for run in runs:
            for g in run:
                if len(g["population"]) != args.agents:
                    audit["errors"].append(f"{mode}/seed {g['seed']}/gen {g['generation']}: population size mismatch")
                if any(a["tasks_attempted"] != 50 for a in g["population"]):
                    audit["errors"].append(f"{mode}/seed {g['seed']}/gen {g['generation']}: task exposure mismatch")
                if sum(v["attempted"] for v in g["task_counts"].values()) != args.agents * 50:
                    audit["errors"].append(f"{mode}/seed {g['seed']}/gen {g['generation']}: task total mismatch")
                if set(g["task_counts"]) != set(TASKS):
                    audit["errors"].append(f"{mode}/seed {g['seed']}/gen {g['generation']}: missing task")
                if any(not 0 <= value <= 1 for a in g["population"] for value in a["skills"].values()):
                    audit["errors"].append(f"{mode}: skill outside [0,1]")
    if audit["errors"]:
        (out / "validity_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
        raise RuntimeError("Confirmatory validity audit failed; see validity_audit.json")

    trajectories = {
        mode: np.asarray([[g["population_mean_success"] for g in run] for run in runs])
        for mode, runs in results.items()}
    rng = np.random.default_rng(20261102)
    contrasts = []
    raw_ps = []
    for treatment, control in CONTRASTS:
        diff = trajectories[treatment][:, -1] - trajectories[control][:, -1]
        t_stat, p_t = stats.ttest_1samp(diff, popmean=0.0)
        try:
            w_stat, p_w = stats.wilcoxon(diff, zero_method="wilcox", alternative="two-sided")
        except ValueError:
            w_stat, p_w = float("nan"), 1.0
        sd = float(np.std(diff, ddof=1))
        contrasts.append({
            "treatment": treatment, "control": control,
            "mean_paired_difference": float(np.mean(diff)),
            "sd_paired_difference": sd,
            "cohens_dz": float(np.mean(diff) / sd) if sd else None,
            "paired_t": float(t_stat), "p_t": float(p_t),
            "wilcoxon_statistic": float(w_stat), "p_wilcoxon": float(p_w),
            "bootstrap_95_ci": bootstrap_ci(diff, rng),
            "treatment_wins": int(np.sum(diff > 0)),
            "ties": int(np.sum(diff == 0)),
        })
        raw_ps.append(float(p_t))
    adjusted = holm_adjust(raw_ps)
    for item, p_adj in zip(contrasts, adjusted):
        item["p_t_holm"] = p_adj
        item["significant_holm_05"] = bool(p_adj < .05)

    mode_summary = {}
    for mode, trajectory in trajectories.items():
        mode_summary[mode] = {
            "generation_mean": trajectory.mean(axis=0).tolist(),
            "generation_sd_across_seeds": trajectory.std(axis=0, ddof=1).tolist(),
            "generation_95_ci": [
                [float(m - stats.t.ppf(.975, args.seeds-1)*s/np.sqrt(args.seeds)),
                 float(m + stats.t.ppf(.975, args.seeds-1)*s/np.sqrt(args.seeds))]
                for m, s in zip(trajectory.mean(axis=0), trajectory.std(axis=0, ddof=1))],
        }
    summary = {
        "study": "Foundational native GAL confirmatory experiment",
        "protocol": "v1.0", "confirmatory": True,
        "model": "original gal.agents.agent.Agent + gal.environment.world.Environment",
        "configuration": {"seeds": args.seeds, "agents_per_generation": args.agents,
                          "generations": args.generations, "modes": list(MODES),
                          "independent_learning_cycles": 5, "tasks_per_cycle": 10},
        "python": platform.python_version(), "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "generation_summary": mode_summary, "pre_registered_contrasts": contrasts,
        "validity_audit": audit,
        "interpretation_limit": "Results apply to this handcrafted stationary GAL model/environment only.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (out / "generation_summary.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mode", "generation", "mean_success", "sd_across_seeds", "ci95_low", "ci95_high"])
        for mode, row in mode_summary.items():
            for i, mean in enumerate(row["generation_mean"]):
                writer.writerow([mode, i+1, mean, row["generation_sd_across_seeds"][i],
                                 *row["generation_95_ci"][i]])
    (out / "validity_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    digest = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    (out / "RAW_SHA256.txt").write_text(f"{digest}  {raw_path.name}\n")
    print(json.dumps({"raw_sha256": digest, "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
