from gal2.memory_grounded_benchmark import run


def test_capability_only_is_a_real_metadata_control_without_rule_memory():
    report = run(seed_start=91000, seeds=2, tasks_per_seed=5)
    rows = [
        row for row in report["raw_results"]
        if row["arm"] == "capability_only"
    ]

    assert len(rows) == 2
    for row in rows:
        assert row["capability_metadata"] == {
            "name": "symbolic_rule_application",
            "proficiency": 1.0,
            "confidence": 1.0,
            "verified": True,
        }
        assert row["memory_counts"] == {
            "episodic": 0,
            "semantic": 0,
            "procedural": 0,
        }
        assert row["accuracy"] == 0.0
        assert row["abstentions"] == 5


def test_corrupted_memory_arm_uses_a_separate_store_and_exposes_errors():
    report = run(seed_start=91000, seeds=4, tasks_per_seed=30)
    rows = [
        row for row in report["raw_results"]
        if row["arm"] == "corrupted_memory"
    ]

    assert len(rows) == 4
    assert sum(row["incorrect"] for row in rows) > 0
    assert all(row["semantic_records_retrieved"] == 1 for row in rows)
    assert all(row["incorrect"] + row["correct"] + row["abstentions"] == 30 for row in rows)


def test_memory_transfer_arms_retrieve_only_their_declared_record_types():
    report = run(seed_start=91000, seeds=2, tasks_per_seed=5)
    rows = {
        (row["seed"], row["arm"]): row
        for row in report["raw_results"]
    }

    for seed in (91000, 91001):
        assert rows[(seed, "episodic_only")]["memory_counts"] == {
            "episodic": 1,
            "semantic": 0,
            "procedural": 0,
        }
        assert rows[(seed, "semantic_procedural")]["memory_counts"] == {
            "episodic": 0,
            "semantic": 1,
            "procedural": 1,
        }
        assert rows[(seed, "combined")]["memory_counts"] == {
            "episodic": 1,
            "semantic": 1,
            "procedural": 1,
        }
