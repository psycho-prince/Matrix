"""Bidirectional knowledge/question transformation benchmark.

This is a deterministic symbolic benchmark, not a natural-language model.
It tests whether question generation and question processing preserve facts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Iterable


@dataclass(frozen=True)
class Fact:
    subject: str
    relation: str
    object: str
    context: str

    def key(self) -> tuple[str, str, str, str]:
        return (self.subject, self.relation, self.object, self.context)


@dataclass(frozen=True)
class Question:
    text: str
    subject: str
    relation: str
    context: str
    expected_object: str


def question_from_fact(fact: Fact) -> Question:
    """Encode a fact as a direct question while retaining its query key."""
    prompts = {
        "capital_of": f"What is the capital of {fact.subject}?",
        "invented": f"Who invented {fact.subject}?",
        "located_in": f"Where is {fact.subject} located?",
        "used_for": f"What is {fact.subject} used for?",
    }
    if fact.relation not in prompts:
        raise ValueError(f"Unsupported relation: {fact.relation}")
    return Question(prompts[fact.relation], fact.subject, fact.relation,
                    fact.context, fact.object)


def process_question(question: Question, knowledge: Iterable[Fact]) -> str | None:
    """Resolve a question against stored facts; refuse missing/ambiguous matches."""
    matches = {
        fact.object for fact in knowledge
        if fact.subject == question.subject
        and fact.relation == question.relation
        and fact.context == question.context
    }
    if len(matches) != 1:
        return None
    return next(iter(matches))


def recover_fact(question: Question, answer: str) -> Fact:
    """Reconstruct the original fact from a question key and its answer."""
    return Fact(question.subject, question.relation, answer, question.context)


def benchmark() -> dict:
    facts = [
        Fact("France", "capital_of", "Paris", "geography"),
        Fact("Japan", "capital_of", "Tokyo", "geography"),
        Fact("Ada Lovelace", "invented", "analytical engine algorithm", "history"),
        Fact("Alexander Fleming", "invented", "penicillin discovery", "science"),
        Fact("Mount Everest", "located_in", "Himalayas", "geography"),
        Fact("Photosynthesis", "used_for", "converting light into chemical energy", "biology"),
        Fact("Mitochondria", "used_for", "cellular energy production", "biology"),
        Fact("Kerala", "capital_of", "Thiruvananthapuram", "geography"),
    ]
    generated = [question_from_fact(fact) for fact in facts]
    answers = [process_question(q, facts) for q in generated]
    recovered = [
        recover_fact(q, answer) if answer is not None else None
        for q, answer in zip(generated, answers)
    ]
    generation_valid = sum(bool(q.text.strip().endswith("?")) for q in generated)
    processing_correct = sum(
        answer == fact.object for answer, fact in zip(answers, facts)
    )
    roundtrip_exact = sum(
        item is not None and item.key() == original.key()
        for item, original in zip(recovered, facts)
    )

    # Negative controls: absent facts and ambiguous matching keys must be rejected.
    absent = Question("What is the capital of Atlantis?", "Atlantis",
                      "capital_of", "geography", "unknown")
    ambiguous_store = facts + [Fact("France", "capital_of", "Lyon", "geography")]
    ambiguous = Question("What is the capital of France?", "France",
                         "capital_of", "geography", "Paris")
    absent_rejected = process_question(absent, facts) is None
    ambiguous_rejected = process_question(ambiguous, ambiguous_store) is None

    report = {
        "schema_version": 1,
        "experiment": "gal2_bidirectional_knowledge_question_benchmark",
        "fact_count": len(facts),
        "question_generation": {
            "valid_questions": generation_valid,
            "total": len(facts),
            "rate": generation_valid / len(facts),
        },
        "question_processing": {
            "correct_answers": processing_correct,
            "total": len(facts),
            "rate": processing_correct / len(facts),
        },
        "round_trip": {
            "exact_fact_recoveries": roundtrip_exact,
            "total": len(facts),
            "rate": roundtrip_exact / len(facts),
        },
        "negative_controls": {
            "unknown_fact_rejected": absent_rejected,
            "ambiguous_fact_rejected": ambiguous_rejected,
        },
        "classification": (
            "complementary_inverse_like_operations"
            if generation_valid == len(facts)
            and processing_correct == len(facts)
            and roundtrip_exact == len(facts)
            and absent_rejected and ambiguous_rejected
            else "not_equivalent_under_this_benchmark"
        ),
        "raw_results": [
            {
                "fact": asdict(fact),
                "question": asdict(question),
                "answer": answer,
                "recovered_fact": asdict(rebuilt) if rebuilt else None,
            }
            for fact, question, answer, rebuilt
            in zip(facts, generated, answers, recovered)
        ],
        "scope_warning": (
            "Deterministic symbolic templates and exact-key retrieval only. "
            "This does not test open-ended language generation, semantic "
            "understanding, reasoning, or learned knowledge."
        ),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["results_sha256"] = hashlib.sha256(canonical).hexdigest()
    return report


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
