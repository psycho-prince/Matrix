"""Deterministic smoke validation for GAL 2.0 inheritance policies.

This is a software/mechanism validation, not an empirical AI capability benchmark.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .agent import Agent
from .adaptive_inheritance import AdaptationPolicy, adaptive_inherit
from .models import Capability, Task


def run_validation(seed: int = 20261104) -> dict:
    parent = Agent("parent", 0, seed)
    parent.capabilities["planning"] = Capability(
        "planning", proficiency=0.9, confidence=0.8,
        context_tags=("lab", "resource_limited"), verified=True,
    )
    parent.capabilities["navigation"] = Capability(
        "navigation", proficiency=0.8, confidence=0.7,
        context_tags=("ocean",), verified=True,
    )
    parent.capabilities["unverified"] = Capability(
        "unverified", proficiency=0.99, context_tags=("lab",), verified=False,
    )
    child = Agent("child", 1, seed)
    report = adaptive_inherit(
        parent, child, ("lab", "time_limited"),
        AdaptationPolicy(min_context_similarity=0.2, prior_proficiency=0.5,
                         recalibration_strength=0.5),
    )
    decisions = {item.capability: item for item in report.decisions}
    assert decisions["planning"].accepted
    assert not decisions["navigation"].accepted
    assert not decisions["unverified"].accepted
    assert child.capabilities["planning"].verified is False
    assert child.capabilities["planning"].evidence == []
    assert child.capabilities["planning"].proficiency < parent.capabilities["planning"].proficiency

    tasks = [
        Task(f"holdout-{i}", "planning", "decomposition", 0.2,
             "time_limited", "test")
        for i in range(250)
    ]
    before = (child.capabilities["planning"].proficiency,
              tuple(child.capabilities["planning"].evidence),
              child.memory.counts().copy())
    evaluation = child.evaluate("planning", tasks, min_trials=100,
                                 min_success_rate=0.1)
    after = (child.capabilities["planning"].proficiency,
             tuple(child.capabilities["planning"].evidence),
             child.memory.counts().copy())
    assert evaluation is not None
    assert before == after, "evaluation mutated training state"
    assert len(evaluation.task_ids) == len(set(evaluation.task_ids))

    # Determinism check: same seed and setup must yield the same holdout result.
    child_again = Agent("child", 1, seed)
    adaptive_inherit(parent, child_again, ("lab", "time_limited"),
                     AdaptationPolicy(min_context_similarity=0.2))
    evaluation_again = child_again.evaluate("planning", tasks, min_trials=100,
                                             min_success_rate=0.1)
    assert evaluation_again == evaluation

    return {
        "schema_version": 1,
        "validation_type": "synthetic_mechanism_smoke_test",
        "seed": seed,
        "checks": {
            "compatible_context_accepted": decisions["planning"].accepted,
            "incompatible_context_rejected": not decisions["navigation"].accepted,
            "unverified_parent_rejected": not decisions["unverified"].accepted,
            "child_starts_unverified": not child.capabilities["planning"].verified,
            "child_evidence_starts_empty": not child.capabilities["planning"].evidence,
            "proficiency_recalibrated_downward": child.capabilities["planning"].proficiency
                < parent.capabilities["planning"].proficiency,
            "evaluation_is_non_mutating": before == after,
            "evaluation_is_deterministic": evaluation_again == evaluation,
        },
        "decisions": [
            {
                "capability": item.capability,
                "accepted": item.accepted,
                "context_similarity": round(item.context_similarity, 6),
                "source_proficiency": round(item.source_proficiency, 6),
                "adapted_proficiency": None if item.adapted_proficiency is None
                    else round(item.adapted_proficiency, 6),
                "reason": item.reason,
            }
            for item in report.decisions
        ],
        "evaluation": {
            "trials": evaluation.trials,
            "successes": evaluation.successes,
            "success_rate": round(evaluation.success_rate, 6),
            "wilson_lower_bound": round(evaluation.wilson_lower_bound, 6),
            "passed": evaluation.passed,
        },
        "scope_warning": (
            "Synthetic Bernoulli simulator only; this report does not establish "
            "real-world learning, generalization, or AI capability."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261104)
    parser.add_argument("--output", type=Path, default=Path("validation-report.json"))
    args = parser.parse_args()
    result = run_validation(args.seed)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    failed = [name for name, passed in result["checks"].items() if not passed]
    print(json.dumps({"output": str(args.output), "checks": result["checks"],
                      "failed": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
