#!/usr/bin/env python3
"""Reproducible binary information-channel benchmark for GAL.

This is an explicitly parameterized analytical benchmark, not a simulation of
the full GAL agents and not an empirical estimate of semantic knowledge.
"""
from __future__ import annotations

import argparse
import json
import math


def binary_entropy(p: float) -> float:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must be in [0, 1]")
    if p in (0.0, 1.0):
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def mutual_information(joint: dict[tuple[int, object], float]) -> float:
    px: dict[int, float] = {}
    py: dict[object, float] = {}
    for (x, y), probability in joint.items():
        if probability < 0.0:
            raise ValueError("joint probabilities must be nonnegative")
        px[x] = px.get(x, 0.0) + probability
        py[y] = py.get(y, 0.0) + probability
    total = sum(joint.values())
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"joint distribution sums to {total}, not 1")
    result = 0.0
    for (x, y), probability in joint.items():
        if probability:
            result += probability * math.log2(probability / (px[x] * py[y]))
    return result


def benchmark(prior_one: float, source_error: float, transfer_probability: float) -> dict:
    """X -> noisy parent bit M -> child Y; Y is M with prob q, else None.

    The transfer gate is assumed independent of X and M. This is a declared
    benchmark assumption, not a claim about empirical verification behaviour.
    """
    if not 0.0 <= prior_one <= 1.0:
        raise ValueError("prior_one must be in [0, 1]")
    if not 0.0 <= source_error <= 1.0:
        raise ValueError("source_error must be in [0, 1]")
    if not 0.0 <= transfer_probability <= 1.0:
        raise ValueError("transfer_probability must be in [0, 1]")

    px = {0: 1.0 - prior_one, 1: prior_one}
    parent_joint: dict[tuple[int, object], float] = {}
    child_joint: dict[tuple[int, object], float] = {}

    for x in (0, 1):
        for m in (0, 1):
            p_m_given_x = (1.0 - source_error) if m == x else source_error
            p = px[x] * p_m_given_x
            parent_joint[(x, m)] = p
            child_joint[(x, m)] = p * transfer_probability
            child_joint[(x, None)] = child_joint.get((x, None), 0.0) + p * (1.0 - transfer_probability)

    parent_mi = mutual_information(parent_joint)
    child_mi = mutual_information(child_joint)
    return {
        "prior_one": prior_one,
        "source_error": source_error,
        "transfer_probability": transfer_probability,
        "source_entropy_bits": binary_entropy(prior_one),
        "parent_memory_mi_bits": parent_mi,
        "child_memory_mi_bits": child_mi,
        "expected_identity": transfer_probability * parent_mi,
        "dpi_gap_bits": parent_mi - child_mi,
    }


def self_test() -> list[str]:
    tests = []
    assert binary_entropy(0.0) == 0.0
    assert math.isclose(binary_entropy(0.5), 1.0, abs_tol=1e-12)
    assert math.isclose(binary_entropy(0.1), binary_entropy(0.9), abs_tol=1e-12)
    tests.append("binary entropy boundary and symmetry")

    perfect = benchmark(0.5, 0.0, 1.0)
    assert math.isclose(perfect["parent_memory_mi_bits"], 1.0, abs_tol=1e-12)
    assert math.isclose(perfect["child_memory_mi_bits"], 1.0, abs_tol=1e-12)
    tests.append("perfect source memory + identity transfer preserves one bit")

    erased = benchmark(0.5, 0.0, 0.0)
    assert math.isclose(erased["child_memory_mi_bits"], 0.0, abs_tol=1e-12)
    tests.append("complete erasure transfers zero information")

    random_source = benchmark(0.5, 0.5, 1.0)
    assert math.isclose(random_source["parent_memory_mi_bits"], 0.0, abs_tol=1e-12)
    assert math.isclose(random_source["child_memory_mi_bits"], 0.0, abs_tol=1e-12)
    tests.append("uninformative parent memory remains uninformative")

    for eps in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
        result = benchmark(0.5, eps, 0.37)
        assert result["child_memory_mi_bits"] <= result["parent_memory_mi_bits"] + 1e-12
        assert math.isclose(
            result["child_memory_mi_bits"],
            0.37 * result["parent_memory_mi_bits"],
            abs_tol=1e-12,
        )
    tests.append("DPI and independent visible-erasure identity over error grid")

    nonuniform = benchmark(0.2, 0.1, 0.6)
    assert nonuniform["child_memory_mi_bits"] <= nonuniform["parent_memory_mi_bits"] + 1e-12
    tests.append("nonuniform prior satisfies DPI")

    return tests


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prior", type=float, default=0.5)
    parser.add_argument("--source-error", type=float, default=0.1)
    parser.add_argument("--transfer-probability", type=float, default=0.5)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps({"status": "PASS", "tests": self_test()}, indent=2))
        return
    print(json.dumps(benchmark(args.prior, args.source_error, args.transfer_probability), indent=2))


if __name__ == "__main__":
    main()
