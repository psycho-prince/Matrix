# GAL 2.1 memory-grounded benchmark

## Purpose

This benchmark tests whether a successor can solve held-out symbolic tasks by retrieving inherited records from GAL 2.0's actual `MemoryStore` implementation. It is a targeted mechanism test, not an AGI evaluation.

## Implementation

The executable harness is `gal2/memory_grounded_benchmark.py`. It imports `MemoryStore`, `MemoryRecord`, and `MemoryKind` from the GAL 2.0 package. It creates a parent memory store, transfers verified records through `inherit_verified`, retrieves records through `search`, and supplies retrieved semantic/procedural content to a deterministic solver.

Seven paired conditions are included:

1. `no_transfer`: empty child memory.
2. `capability_only`: capability metadata without symbol-to-operation semantics.
3. `episodic_only`: experience record, no rule mapping or procedure.
4. `semantic_procedural`: inherited rule mapping and execution procedure.
5. `combined`: episodic, semantic, and procedural records.
6. `corrupted_memory`: semantic rule altered after transfer while retaining its verified flag, simulating an undetected integrity failure.
7. `oracle`: direct access to the task-generating rulebook; upper-bound control, not an inheritance condition.

Each seed generates a distinct opaque-symbol arithmetic rulebook and task set. Every arm receives the same tasks for a given seed. The default run uses 100 paired seeds and 30 tasks per seed per arm (3,000 task instances per arm).

## Run

From the repository root:

```bash
python -m gal2.memory_grounded_benchmark --seeds 100 --tasks-per-seed 30
```

The command writes `gal2_memory_grounded_results.json` and prints a summary, paired contrasts against no-transfer, and a SHA-256 fingerprint. A smaller smoke run can be requested with `--seeds 2 --tasks-per-seed 5`.

## Metrics

- Exact task accuracy.
- Incorrect answer count.
- Abstention rate.
- Mean and standard deviation of accuracy across paired seeds.
- Per-seed paired accuracy differences versus no-transfer.
- Counts of inherited and retrievable memory records by type.

## Expected interpretation

The semantic/procedural and combined arms are expected to solve tasks when records are correctly retrieved. Episodic-only and capability-only do not contain the operation mapping and should abstain. The corrupted arm tests whether the solver can detect a semantically incorrect but still `verified` record; this implementation does not yet provide an independent verifier, so wrong answers are an expected possible outcome. The oracle arm validates task/evaluator consistency.

These are design expectations, not reported outcomes. No benchmark execution result is claimed in this document.

## Limitations

- The solver is deterministic reference code, not a language model call.
- The benchmark uses arithmetic symbol-composition tasks, not broad reasoning or external tasks.
- It exercises GAL's memory data path but not `Agent.evaluate`, which remains a probabilistic simulator and does not consume memory.
- The benchmark's generated task labels and scoring are controlled by code; independent blinded evaluation is still needed.
- The corrupted-memory arm deliberately retains `verified=True`; this tests the consequence of a false verification state, not ordinary transfer behavior.
- No statistical significance or causal claim should be made from expected values. Use the emitted raw results and paired contrasts after an actual run.

## Research integrity

This file and the harness are isolated on `research/gal-2.1-memory-grounded-learning`. GAL 1.0, the GAL 2.0 research branch, existing datasets, and previous reports are not modified. Results should be reviewed before any claims or changes are propagated.
