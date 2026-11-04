from gal2.knowledge_questions import (
    Fact, Question, benchmark, process_question, question_from_fact, recover_fact,
)


def test_bidirectional_round_trip_preserves_facts():
    report = benchmark()
    assert report["question_generation"]["rate"] == 1.0
    assert report["question_processing"]["rate"] == 1.0
    assert report["round_trip"]["rate"] == 1.0
    assert report["classification"] == "complementary_inverse_like_operations"


def test_unknown_and_ambiguous_questions_are_rejected():
    facts = [Fact("France", "capital_of", "Paris", "geography")]
    unknown = Question("What is the capital of Atlantis?", "Atlantis",
                       "capital_of", "geography", "unknown")
    ambiguous = Question("What is the capital of France?", "France",
                         "capital_of", "geography", "Paris")
    assert process_question(unknown, facts) is None
    assert process_question(
        ambiguous, facts + [Fact("France", "capital_of", "Lyon", "geography")]
    ) is None


def test_recovered_fact_uses_question_key_and_answer():
    fact = Fact("Japan", "capital_of", "Tokyo", "geography")
    question = question_from_fact(fact)
    assert recover_fact(question, "Tokyo") == fact


def test_benchmark_is_deterministic():
    assert benchmark() == benchmark()
