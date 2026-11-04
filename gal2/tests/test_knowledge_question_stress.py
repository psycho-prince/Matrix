from gal2.knowledge_question_stress import (
    Fact, answer_question, answer_multi_hop, detect_contradictions,
    parse_question, run_five_tests,
)


def test_all_five_stress_tests_pass():
    report = run_five_tests()
    assert report["passed_tests"] == 5
    assert report["total_tests"] == 5
    assert report["overall_pass"] is True


def test_paraphrase_parser_handles_unseen_surface_forms():
    parsed = parse_question("Name the capital city of France")
    assert parsed is not None
    assert parsed.subject == "france"
    assert parsed.relation == "capital_of"


def test_unanswerable_question_is_not_guessed():
    result = answer_question(
        "What is the capital of Atlantis?",
        [Fact("France", "capital_of", "Paris")],
    )
    assert result.status == "unknown"
    assert result.answer is None


def test_multi_hop_requires_both_edges():
    facts = [
        Fact("France", "capital_of", "Paris"),
        Fact("Paris", "located_in", "Europe"),
    ]
    assert answer_multi_hop(
        "Which region contains the capital of France?", facts
    ).answer == "Europe"
    assert answer_multi_hop(
        "Which region contains the capital of France?",
        [Fact("France", "capital_of", "Paris")],
    ).status == "unknown"


def test_contradictions_are_detected_and_block_answers():
    facts = [
        Fact("France", "capital_of", "Paris"),
        Fact("France", "capital_of", "Lyon"),
    ]
    assert len(detect_contradictions(facts)) == 1
    assert answer_question("What is the capital of France?", facts).status == "contradictory"


def test_contexts_do_not_conflict_when_distinct():
    facts = [
        Fact("Mercury", "located_in", "Solar System", "astronomy"),
        Fact("Mercury", "located_in", "Thermometer", "chemistry"),
    ]
    assert detect_contradictions(facts) == []
