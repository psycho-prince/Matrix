import hashlib
import json
import os

import numpy as np
from scipy import stats


ROOT = os.path.dirname(os.path.dirname(__file__))


def _load_json(relative_path):
    with open(os.path.join(ROOT, relative_path), encoding="utf-8") as handle:
        return json.load(handle)


def test_statistical_audit_digest_and_raw_summary_are_consistent():
    audit = _load_json("data/cryptographic_validation_audit.json")
    recorded_digest = audit.pop("sha256_verification_hash")
    canonical = json.dumps(audit, sort_keys=True).encode("utf-8")
    assert hashlib.sha256(canonical).hexdigest() == recorded_digest

    results = audit["results"]
    assert audit["sample_size_per_condition"] == 30
    assert audit["total_independent_runs"] == 90
    for condition in results.values():
        raw = np.asarray(condition["raw_f"], dtype=float)
        assert raw.shape == (30,)
        assert np.isclose(raw.mean(), condition["f_mean"])
        assert np.isclose(raw.std(ddof=1), condition["f_std"])

    rentier = np.asarray(results["Lamarckian Rentier (Freq=50)"]["raw_f"])
    amnesia = np.asarray(results["Agile Amnesia (Freq=5)"]["raw_f"])
    t_stat, p_value = stats.ttest_ind(rentier, amnesia, equal_var=False)
    recorded = audit["statistical_tests"]["Rentier_vs_Amnesia"]
    assert np.isclose(t_stat, recorded["t_statistic"], rtol=1e-10)
    assert np.isclose(p_value, recorded["p_value_welch"], rtol=1e-10)


def test_committed_neural_results_do_not_claim_method_superiority():
    results = _load_json("data/mnist/permuted_mnist_results.json")
    standard = results["standard_regime"]
    proposed = standard["Variance-Preserving Reset (Ours)"]["mean_continual_acc"]

    for baseline in (
        "Elastic Weight Consolidation (EWC)",
        "Experience Replay (ER)",
        "Naive Sequential Cloning (f=1.0)",
    ):
        assert proposed < standard[baseline]["mean_continual_acc"]

    bottleneck = results["bottleneck_plasticity_regime"]
    assert np.isclose(bottleneck["plasticity_advantage_percent"], -6.25)
    assert bottleneck["lossy_task5_acc"] < bottleneck["cloning_task5_acc"]


def test_digit_benchmark_generator_is_deterministic_and_synthetic():
    import importlib.util

    path = os.path.join(ROOT, "data/mnist/mnist_benchmark.py")
    spec = importlib.util.spec_from_file_location("mnist_benchmark_under_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    X1, y1 = module.generate_mnist_benchmarks(n_samples_per_digit=3, seed=123)
    X2, y2 = module.generate_mnist_benchmarks(n_samples_per_digit=3, seed=123)
    assert X1.shape == (30, 64)
    assert y1.shape == (30,)
    assert np.array_equal(X1, X2)
    assert np.array_equal(y1, y2)
    assert set(np.unique(y1)) == set(range(10))


def test_gka_metric_matches_its_documented_endpoint_formula():
    from gal.metrics.knowledge import GenerationalKnowledgeAccumulation

    assert GenerationalKnowledgeAccumulation([1.0]).calculate() == 0.0
    assert np.isclose(
        GenerationalKnowledgeAccumulation([1.0, 2.0, 4.0]).calculate(),
        (4.0 - 1.0) / 2.0,
    )
