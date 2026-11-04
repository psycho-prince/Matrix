from gal2.tasks import DynamicTaskGenerator


def test_task_generation_is_deterministic():
    generator = DynamicTaskGenerator(42)
    assert generator.generate(10) == generator.generate(10)


def test_splits_have_distinct_ids_and_are_labelled():
    generator = DynamicTaskGenerator(42)
    train = generator.generate(10, "train")
    test = generator.generate(10, "test")
    assert {t.task_id for t in train}.isdisjoint({t.task_id for t in test})
    assert all(t.split == "test" for t in test)


def test_generator_rejects_invalid_count():
    import pytest
    with pytest.raises(ValueError):
        DynamicTaskGenerator(1).generate(0)
