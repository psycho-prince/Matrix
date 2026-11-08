# GAL 2.0 Architecture Review

**Review date:** 2026-11-09  
**Repository:** https://github.com/psycho-prince/Matrix  
**Target ref reviewed:** `research/gal-2.0-core`  
**Reviewed commit:** `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`  
**Review type:** Source-level architecture review plus inspection of recorded GitHub Actions execution. No local checkout or independent Python execution was performed by the reviewer.

## Executive assessment

GAL 2.0 is a modular, experimental Python research harness for capability and symbolic-memory inheritance. It contains meaningful engineering boundaries: typed records, separate memory kinds, seeded task generation, training/evaluation RNG separation, evidence-gated capability inheritance, adaptive context heuristics, and explicit validation scripts.

It is not currently an end-to-end generational learning agent in the strong sense. The core task executor computes success from a scalar capability proficiency and task difficulty. It does not retrieve episodic, semantic, or procedural memories to select or improve actions. Thus, the code demonstrates storage and transfer mechanisms, plus a synthetic capability-proficiency effect; it does not demonstrate causal utility of inherited memory for problem solving.

## Component map

| Component | Main responsibility | Review notes |
|---|---|---|
| `gal2/models.py` | Evidence, Capability, MemoryRecord, Task, EvaluationReport | Typed data model; some nested payloads remain mutable |
| `gal2/memory.py` | Episodic/semantic/procedural record storage, lookup, verification helper, inheritance | Exact-tag lookup only; legacy verification helper is not independent |
| `gal2/tasks.py` | Seeded finite-vocabulary task generation | Task labels are synthetic descriptors, not executable task semantics |
| `gal2/agent.py` | Training attempts, probabilistic task outcomes, memory creation, evaluation, basic inheritance | Main causal path bypasses memory |
| `gal2/inheritance.py` | Basic verified capability transfer and child revalidation | Generation guard exists in wrapper |
| `gal2/adaptive_inheritance.py` | Jaccard context similarity and proficiency recalibration | Heuristic label overlap; memory transfer remains unfiltered |
| `gal2/validation.py` | Deterministic mechanism smoke test | Validates software invariants, not real-world learning |
| `gal2/comparison.py` | Paired-seed synthetic baseline comparison | Explicitly acknowledges memory is not consumed by executor |
| `gal2/knowledge_lifecycle.py` | Symbolic claims, oracle verification, generation transfer experiment | Useful controlled oracle experiment; not autonomous truth discovery |
| `gal2/knowledge_questions.py`, `knowledge_question_stress.py` | Knowledge processing/question-generation benchmarks | Separate symbolic benchmark family; inspect outputs and task semantics before making learning claims |
| `gal2/analytical_theory.py` | Exact analytical calculations | Exact math tests are distinct from empirical validation |
| `gal2/tests/` | Unit and mechanism tests | Tests cover several invariants, not the full causal hypothesis |
| `.github/workflows/gal2-core.yml` | CI matrix, validation, experiments, artifact upload | Latest observed run completed successfully |

## Data flow

### Training path

1. A `Task` enters `Agent.attempt()`.
2. `Agent._success_probability()` reads the task capability's scalar proficiency and task difficulty.
3. A seeded training RNG samples success/failure.
4. The agent records an `Evidence` object and updates capability proficiency/confidence.
5. Episodic memory is added for each attempt.
6. Successful attempts additionally create semantic and procedural memory records.

The task result does not depend on memory retrieval, memory content, prerequisite satisfaction, or procedure execution.

### Evaluation path

1. `Agent.evaluate()` filters to validation/test tasks for the requested capability.
2. A separate evaluation RNG samples outcomes using the same proficiency/difficulty probability formula.
3. The method calculates success rate and Wilson lower confidence bound.
4. The report is stored in `last_evaluation`; evaluation does not update proficiency, evidence, or memory.
5. `verify_capability()` uses the report's pass flag to update the capability's verified status.

The split label is enforced by filtering, but the generator itself uses finite vocabularies and independently seeded split streams. The code does not prove that task instances are semantically disjoint or that task templates cannot overlap.

### Basic inheritance path

1. `inherit_capabilities()` checks that the child's generation is later.
2. `Agent.inherit_from()` copies only parent capabilities marked verified.
3. The copied capability is reset to unverified.
4. Verified memory records are copied with source/custodian and lineage metadata.
5. Child verification is a separate operation using held-out-labelled tasks.

### Adaptive inheritance path

1. Each verified parent capability is compared with child context tags using Jaccard similarity.
2. Low-similarity or unverified capabilities are rejected.
3. Accepted proficiency is recalibrated toward a prior according to similarity and recalibration strength.
4. Child verification is reset.
5. Verified memory records are inherited without applying an equivalent context-compatibility policy.

## Architectural strengths

- Explicit typed objects and separation of training from evaluation.
- Deterministic seed design for core synthetic mechanisms.
- Child-side verification rather than blindly preserving a parent's verified flag.
- Provenance/custodian fields and lineage tracking.
- A documented distinction between mechanism tests and scientific evidence.
- Dedicated GAL 2.0 package and CI jobs separate from the original `gal/` implementation.

## Architectural limitations

- Memory is not in the task-solving causal path.
- The capability executor is a Bernoulli-style simulator, not an adaptive reasoning policy.
- Memory search is exact tag membership, not semantic retrieval.
- Context compatibility is Jaccard overlap over manually assigned labels.
- The confidence field is a sample-count heuristic, not a calibrated epistemic confidence estimate.
- The symbolic knowledge lifecycle experiment has access to a ground-truth oracle.
- The top-level repository includes older GAL experiments, neural prototypes, LLM prototypes, papers, and datasets; those are not automatically evidence for GAL 2.0.

## Decision

**Architecture status: coherent experimental software foundation; not yet a demonstrated generational learning system with memory-mediated task improvement.**

The next architecture milestone should introduce a versioned memory-using task policy and preserve the existing simulator as a control arm. Do not silently change the current executor and retrospectively attribute new results to the existing implementation.
