# GAL 2.0 scientific validation gap audit

**Status:** Source-level audit; no multi-generation confirmatory outcome is claimed.  
**Scope:** `gal2/agent.py`, `gal2/inheritance.py`, `gal2/tasks.py`, and the mechanism tests.

## 1. Current operational model

The current GAL 2.0 agent is a synthetic probabilistic task harness:
`p(success) = clamp(proficiency - 0.45 × difficulty + 0.25, 0.02, 0.98)`.

Training attempts update capability evidence and create episodic, semantic, and procedural memory records. Evaluation uses validation/test-labelled tasks and a separate evaluation RNG; it does not mutate training proficiency, evidence, or memory.

Basic inheritance:
- copies only parent capabilities marked verified;
- resets the child's verified flag, requiring child-side revalidation;
- copies verified memory records while preserving provenance/custodian lineage.

The task generator uses finite capability, concept, and context vocabularies and explicit train/validation/test split labels.

## 2. Critical causal-path limitation

The current `Agent.attempt(task)` computes success probability from the task's capability proficiency and difficulty. It does not retrieve episodic, semantic, or procedural memory to select an action, alter the solution, or change the success probability.

Therefore:
- inherited verified capability proficiency can affect the synthetic success probability;
- inherited memory is currently a stored/provenance-tracked object, but the task executor does not use it;
- a benchmark showing inherited memory records are present would establish transfer/storage, not that inherited memory improves problem solving.

This must be fixed or explicitly made the research target before claiming that GAL 2.0 demonstrates useful knowledge inheritance. Do not silently change the executor and then compare it as if it were the existing implementation; introduce a versioned, separately tested memory-using policy.

## 3. What current tests establish

The current tests establish implementation properties such as:
- verified-only capability and memory transfer;
- child re-verification;
- provenance preservation;
- bounded adaptive recalibration and context similarity;
- separation of training mutation from evaluation state.

They do not establish:
- multi-generation accumulation or retention;
- accuracy/truth of inherited memories;
- calibrated confidence;
- causal utility of inherited memory;
- generalisation to new tasks;
- robustness to distribution shift;
- superiority to equal-budget independent learning.

The current confidence heuristic and synthetic Bernoulli executor should not be described as calibrated epistemic confidence or a real reasoning system.

## 4. Required validation design

GAL 2.0 needs a distinct multi-generation experiment. Do not borrow the GAL 1.0 result as evidence for GAL 2.0.

The benchmark should define a finite synthetic world with explicit ground-truth rules and task solutions. Each agent should:
1. observe a controlled training sample;
2. form a claim/memory with explicit provenance and uncertainty;
3. transmit selected claims and capabilities to a successor;
4. let the successor decide whether to retain, reject, or update inherited claims using new evidence;
5. solve disjoint held-out tasks where correct solutions depend on the underlying rules.

Compare at least:
- no inheritance;
- capability-only inheritance;
- memory-only inheritance;
- combined capability and memory inheritance;
- independent learning with exactly matched observation and compute budgets.

For each generation, report separately:
- information transmitted and retained;
- claim correctness and false-discovery rate;
- confidence calibration (proper scoring rules, not just sample-count heuristics);
- held-out task accuracy;
- recovery after a pre-specified distribution shift;
- memory/compute/interaction costs.

Use paired seeds, a pre-registered primary endpoint, explicit stopping/exclusion rules, raw immutable outputs, and an auditor that is independent of the experiment runner.

## 5. Decision

**Current status:** GAL 2.0 has tested inheritance and provenance mechanisms, but it has not yet demonstrated that inherited memory improves task performance. The direct causal route from memory to action is absent in the current executor.

The next valid step is a versioned memory-using benchmark plus matched controls, not a chess demonstration and not another test that only checks whether memory objects were copied.
