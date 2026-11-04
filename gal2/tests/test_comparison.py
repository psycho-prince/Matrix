from gal2.comparison import ARMS, run_experiment


def test_comparison_is_paired_and_reproducible():
    first = run_experiment(seed_start=42, seeds=3, test_trials=40)
    second = run_experiment(seed_start=42, seeds=3, test_trials=40)
    assert first == second
    assert len(first["raw_results"]) == 3 * len(ARMS)
    assert first["diagnostics"]["shared_memory_equals_no_transfer"]
    assert first["diagnostics"]["memory_is_consumed_by_task_executor"] is False
    assert set(first["summary"]) == set(ARMS)


def test_all_parent_capabilities_verified_but_children_are_not():
    result = run_experiment(seed_start=7, seeds=2, test_trials=20)
    for row in result["raw_results"]:
        assert row["capability_verified_at_start"] is False
