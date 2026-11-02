"""Regression tests for Split Digits helpers and native GAL inheritance.

Run from repository root:
    python -m unittest discover -s experiments/09_split_digits/tests -v
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
import sys

import torch
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

SCRIPT = REPO_ROOT / "experiments" / "09_split_digits" / "run_extended.py"
SPEC = importlib.util.spec_from_file_location("gal_split_digits_extended", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)

from gal.agents.agent import Agent


class EWCInvariantTests(unittest.TestCase):
    def test_each_task_constraint_uses_its_own_reference(self):
        model = nn.Linear(1, 1, bias=False)
        with torch.no_grad():
            model.weight.fill_(3.0)
        fisher = {"weight": torch.ones_like(model.weight)}
        reference_a = {"weight": torch.zeros_like(model.weight)}
        reference_b = {"weight": torch.full_like(model.weight, 2.0)}

        penalty = benchmark.ewc_penalty(
            model, [(fisher, reference_a), (fisher, reference_b)]
        )
        # (3 - 0)^2 + (3 - 2)^2 = 10
        self.assertAlmostEqual(float(penalty), 10.0, places=6)

    def test_zero_fisher_produces_zero_penalty(self):
        model = nn.Linear(2, 1)
        fisher = {name: torch.zeros_like(p) for name, p in model.named_parameters()}
        reference = {name: torch.ones_like(p) for name, p in model.named_parameters()}
        self.assertEqual(float(benchmark.ewc_penalty(model, [(fisher, reference)])), 0.0)

    def test_parameter_schema_mismatch_is_rejected(self):
        model = nn.Linear(2, 1)
        with self.assertRaises(ValueError):
            benchmark.ewc_penalty(model, [({"wrong": torch.ones(1)}, {})])


class MemoryInvariantTests(unittest.TestCase):
    def test_memory_respects_per_class_budget_and_labels(self):
        x = torch.arange(100 * 64, dtype=torch.float32).reshape(100, 64)
        y = torch.tensor([0] * 40 + [1] * 35 + [2] * 25)
        mx, my = benchmark.make_memory(x, y, per_class=5, seed=19)
        counts = torch.bincount(my, minlength=10)
        self.assertLessEqual(int(counts.max()), 5)
        self.assertEqual(int(counts.sum()), 15)
        self.assertTrue(set(my.tolist()).issubset({0, 1, 2}))
        self.assertEqual(len(mx), len(my))

    def test_memory_sampling_is_seed_reproducible(self):
        x = torch.arange(30 * 64, dtype=torch.float32).reshape(30, 64)
        y = torch.tensor([0] * 10 + [1] * 10 + [2] * 10)
        a = benchmark.make_memory(x, y, per_class=3, seed=7)
        b = benchmark.make_memory(x, y, per_class=3, seed=7)
        self.assertTrue(torch.equal(a[0], b[0]))
        self.assertTrue(torch.equal(a[1], b[1]))


class TaskEvaluationTests(unittest.TestCase):
    def test_task_mask_selects_exact_classes(self):
        labels = torch.tensor([0, 1, 2, 3, 4, 5])
        mask = benchmark.task_mask(labels, (2, 5))
        self.assertEqual(labels[mask].tolist(), [2, 5])

    def test_task_matrix_returns_one_score_per_task(self):
        class ConstantModel(nn.Module):
            def forward(self, x):
                logits = torch.zeros((len(x), 10))
                logits[:, 0] = 1.0
                return logits

        x = torch.zeros((10, 64))
        y = torch.arange(10)
        scores = benchmark.evaluate_task_matrix(
            ConstantModel(), x, y, tasks=((0,), (1,), (2,), (3,), (4,))
        )
        self.assertEqual(len(scores), 5)
        self.assertAlmostEqual(scores[0], 1.0)
        self.assertTrue(all(score == 0.0 for score in scores[1:]))


class ForgettingMetricTests(unittest.TestCase):
    def test_forgetting_uses_best_accuracy_after_initial_learning(self):
        matrix = [
            [0.80, 0.00, 0.00],
            [0.60, 0.70, 0.00],
            [0.50, 0.65, 0.90],
        ]
        self.assertEqual(
            benchmark.calculate_forgetting(matrix),
            [0.30, 0.05, 0.0],
        )

    def test_invalid_task_matrix_is_rejected(self):
        with self.assertRaises(ValueError):
            benchmark.calculate_forgetting([[0.5, 0.2], [0.3]])


class NeuralInheritanceTests(unittest.TestCase):
    def test_exact_inherited_fraction_is_preserved(self):
        model = nn.Linear(4, 2)
        parent = {name: p.detach().clone() for name, p in model.named_parameters()}
        fisher = {name: torch.arange(1, p.numel() + 1, dtype=p.dtype).reshape_as(p)
                  for name, p in model.named_parameters()}
        benchmark.apply_gal_inheritance(model, fisher, keep=0.70)
        # The helper ranks globally, so the number retained is exact.
        total = sum(p.numel() for p in model.parameters())
        expected = max(1, int(0.70 * total))
        retained = 0
        for name, parameter in model.named_parameters():
            retained += int(torch.isclose(parameter, parent[name]).sum())
        self.assertGreaterEqual(retained, expected)
        self.assertLessEqual(retained, expected + 1)


class NativeGALInheritanceTests(unittest.TestCase):
    def _agents(self):
        parent = Agent("parent", generation=1, universe_seed=123)
        parent.skills = {
            "foraging": 0.8, "construction": 0.6, "crafting": 0.4,
            "exploration": 0.2, "logic": 0.9,
        }
        parent.knowledge_concepts = {"concept_42", "concept_108"}
        child = Agent("child", generation=2, universe_seed=123)
        return parent, child

    def test_copy_mode_transfers_skills_and_concepts_exactly(self):
        parent, child = self._agents()
        child.inherit(parent, "B-copy")
        self.assertEqual(child.skills, parent.skills)
        self.assertEqual(child.knowledge_concepts, parent.knowledge_concepts)

    def test_no_memory_mode_teaches_skills_without_concept_transfer(self):
        parent, child = self._agents()
        child.inherit(parent, "C-no-memory")
        self.assertEqual(child.knowledge_concepts, set())
        self.assertTrue(all(0.0 <= value <= 1.0 for value in child.skills.values()))
        self.assertGreater(child.skills["foraging"], 0.0)

    def test_full_teaching_transfers_concepts_and_develops_skills(self):
        parent, child = self._agents()
        child.inherit(parent, "C-full")
        self.assertEqual(child.knowledge_concepts, parent.knowledge_concepts)
        self.assertTrue(all(0.0 <= value <= 1.0 for value in child.skills.values()))
        self.assertGreater(child.skills["foraging"], 0.0)

    def test_independent_mode_does_not_inherit_parent_state(self):
        parent, child = self._agents()
        before_skills = dict(child.skills)
        child.inherit(parent, "A")
        self.assertEqual(child.skills, before_skills)
        self.assertEqual(child.knowledge_concepts, set())


if __name__ == "__main__":
    unittest.main()
