"""GAL memory bridge with evidence-based successor verification."""

from dataclasses import dataclass, replace
from hashlib import sha256
import json
import math


@dataclass(frozen=True)
class VerificationReport:
    candidate_id: str
    evaluator_id: str
    task_ids: tuple
    successes: int
    trials: int
    success_rate: float
    wilson_lower_bound: float
    passed: bool

    def __post_init__(self):
        if not self.candidate_id or not self.evaluator_id:
            raise ValueError("Candidate and evaluator IDs are required")

        if self.trials < 1 or not 0 <= self.successes <= self.trials:
            raise ValueError("Invalid trial counts")

        if len(self.task_ids) != self.trials:
            raise ValueError("Every trial must have a task ID")

        if len(set(self.task_ids)) != len(self.task_ids):
            raise ValueError("Task IDs must be unique")

        if not 0 <= self.success_rate <= 1:
            raise ValueError("Invalid success rate")

        if not 0 <= self.wilson_lower_bound <= 1:
            raise ValueError("Invalid confidence bound")

        expected = self.successes / self.trials
        if not math.isclose(self.success_rate, expected, abs_tol=1e-9):
            raise ValueError("Success rate does not match trial counts")


@dataclass(frozen=True)
class MemoryCandidate:
    candidate_id: str
    kind: str
    content_json: str
    source_agent: str
    source_generation: int
    custodian_agent: str
    custodian_generation: int
    tags: tuple
    lineage: tuple
    parent_verified: bool
    status: str = "pending"
    verification_evidence_ids: tuple = ()
    evaluator_id: str | None = None

    @property
    def content(self):
        return json.loads(self.content_json)

    @property
    def verified(self):
        return self.status == "verified"


def wilson_lower_bound(successes, trials, z=1.96):
    if trials <= 0:
        return 0.0

    p = successes / trials
    z2 = z * z
    denominator = 1 + z2 / trials
    centre = p + z2 / (2 * trials)
    margin = z * math.sqrt(
        (p * (1 - p) + z2 / (4 * trials)) / trials
    )

    return max(0.0, (centre - margin) / denominator)


class GALMemoryAdapter:
    def inherit(self, record, child_id, child_generation):
        if not record.verified:
            return None

        if child_generation <= record.generation:
            raise ValueError("Child generation must exceed source generation")

        content_json = json.dumps(
            record.content,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

        identity = {
            "kind": record.kind.value,
            "content": content_json,
            "source": record.source_agent,
            "source_generation": record.generation,
            "child": child_id,
            "child_generation": child_generation,
            "tags": list(record.tags),
            "lineage": list(record.lineage),
        }

        candidate_id = sha256(
            json.dumps(identity, sort_keys=True).encode("utf-8")
        ).hexdigest()

        return MemoryCandidate(
            candidate_id=candidate_id,
            kind=record.kind.value,
            content_json=content_json,
            source_agent=record.source_agent,
            source_generation=record.generation,
            custodian_agent=child_id,
            custodian_generation=child_generation,
            tags=tuple(record.tags),
            lineage=tuple(record.lineage) + (record.source_agent,),
            parent_verified=True,
        )

    def verify(self, candidate, report, min_trials=30,
               min_success_rate=0.70):
        """Accept only a passing, candidate-specific held-out report."""

        if candidate.status != "pending":
            raise ValueError("Only pending candidates can be verified")

        if not isinstance(report, VerificationReport):
            raise TypeError("A VerificationReport is required")

        if report.candidate_id != candidate.candidate_id:
            raise ValueError("Report belongs to a different candidate")

        if report.trials < min_trials:
            raise ValueError("Insufficient independent evaluation trials")

        if report.success_rate < min_success_rate:
            raise ValueError("Success rate below verification threshold")

        if report.wilson_lower_bound < min_success_rate:
            raise ValueError("Confidence bound below verification threshold")

        if not report.passed:
            raise ValueError("Independent evaluator did not approve candidate")

        return replace(
            candidate,
            status="verified",
            verification_evidence_ids=report.task_ids,
            evaluator_id=report.evaluator_id,
        )

    def prompt_context(self, candidates):
        lines = []

        for item in candidates:
            label = (
                "VERIFIED"
                if item.verified
                else "UNVERIFIED CANDIDATE — DO NOT ASSUME TRUE"
            )

            lines.append(
                f"[{label}] Kind: {item.kind}; "
                f"Source: {item.source_agent}; "
                f"Generation: {item.source_generation}; "
                f"Content: {item.content_json}"
            )

        return "\n".join(lines)
