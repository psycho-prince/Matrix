# GAL 2.0 Model-Assisted Memory Transfer Pilot

**Date:** 2026-11-09  
**Repository:** `psycho-prince/Matrix`  
**Reference implementation:** `research/gal-2.0-core` at `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`  
**Audit branch:** `audit/gal2-independent-review-2026-11-09`  
**Status:** Exploratory pilot; not a confirmatory scientific study.

## Question

Can an agent use information stored in an inherited memory record to solve held-out tasks that require composing previously learned operations?

This directly probes the gap identified in the independent review: GAL 2.0 implements memory storage and transfer, but its current task executor does not establish that retrieved memory causally improves task solving.

## Experimental design

A small synthetic protocol was created specifically for this pilot. A parent agent is assumed to have learned and stored this rulebook:

- A: add 2
- B: multiply by 3
- C: subtract 1

Each held-out task supplies an integer seed and an ordered sequence of symbols. The solver must retrieve the rulebook and apply operations in order. The exact answer is calculated by a deterministic evaluator.

Two information conditions are defined:

1. **Memory available:** the solver receives the inherited rulebook and the task.
2. **Memory unavailable:** the solver receives only the task; the symbol meanings are withheld. Correctly abstaining is preferable to inventing a mapping.

Twelve fixed task instances were evaluated in the memory-available condition by this model using the stated rulebook. The memory-unavailable condition is an information-control condition: without the mapping, the correct numeric answer is underdetermined. It is not represented as a separately sampled model call.

## Results

| Task | Seed | Sequence | Exact answer |
|---:|---:|---|---:|
| 1 | 4 | A → B | 18 |
| 2 | 7 | C → A → B | 24 |
| 3 | 3 | B → C | 8 |
| 4 | 9 | A → A → C | 12 |
| 5 | 2 | B → A → C | 7 |
| 6 | 5 | C → B → A | 14 |
| 7 | 8 | A → B → C → A | 31 |
| 8 | 6 | C → C → B | 12 |
| 9 | 1 | B → A → A | 7 |
| 10 | 10 | A → C → B → C | 32 |
| 11 | 12 | C → A → C → B | 36 |
| 12 | 11 | B → C → A → A | 36 |

**Memory-available exact accuracy:** 12/12 (100%) on this fixed pilot set.  
**Memory-unavailable identifiability:** 0/12 tasks have a uniquely derivable numeric answer from the task prompt alone, because the symbol-to-operation mapping is omitted. A responsible solver should abstain rather than guess.

## Interpretation

The pilot confirms a narrow, expected capability: this model can apply a supplied symbolic rulebook compositionally to new seeds and unseen operation sequences. It illustrates why retrieval of inherited information can be useful.

It does **not** establish that GAL 2.0 itself caused the improvement. The rulebook was supplied directly in the model context; this pilot did not execute GAL 2.0's MemoryStore, inheritance pipeline, or task executor. It also does not demonstrate autonomous knowledge acquisition, independent verification, long-term retention, robust transfer under distribution shift, or general intelligence.

The 100% score is descriptive for 12 hand-specified cases, not a population estimate. There was no randomized task sampling, multi-run replication, blinded scoring, independent evaluator, or statistical hypothesis test. The memory-unavailable condition is an information-theoretic control, not a measured baseline score.

## What this experiment says about GAL 2.0

- **Supported:** rule-guided compositional task solving is feasible when the relevant rules are present in context.
- **Not yet supported:** GAL's own inherited memory records are retrieved and used by the agent to improve performance.
- **Not yet supported:** inherited memory outperforms capability-only, no-transfer, or matched-information baselines in a controlled experiment.

## Required next experiment

Implement a benchmark harness in a separate experimental branch. The task-solving policy must retrieve memory records through the actual GAL API and expose the retrieved record IDs in an auditable action trace. Compare, under identical task budgets and paired seeds:

1. no inheritance;
2. capability-only inheritance;
3. episodic-memory inheritance;
4. semantic/procedural-memory inheritance;
5. combined inheritance;
6. corrupted-memory control;
7. oracle-memory upper bound.

Use randomly generated rulebooks and held-out compositional sequences, preregister scoring, repeat across multiple seeds, and report exact accuracy, abstention, false-memory use, calibration, and token/cost budget. Do not use this pilot's 12 examples as confirmatory test data.

## Reproducibility note

The task list and rulebook are fully specified above, and the answers can be recomputed with the simple sequential evaluator:

`x = seed`; for each symbol in order, apply its mapped operation to `x`.

This was a model-assisted reasoning pilot, not a run of the repository's GAL 2.0 code, not a GitHub Actions test, and not an independent clean-environment reproduction.
