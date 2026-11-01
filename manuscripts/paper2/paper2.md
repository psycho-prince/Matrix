---
title: "The Capacity-Saturation Trap: A Reassessment of Lossy and Exact Inheritance"
author: "Prince T Philip"
date: "October 2026; reassessed November 2, 2026"
abstract: |
  This manuscript investigates whether lossy generational transmission can act as a regularizer under bounded memory and changing environments. A consistency audit of the committed repository artifacts found that the earlier claim that lossy transmission outperformed exact copying by +85.4% is not supported by the currently committed 100-seed raw results. The committed summary instead reports a Generation-10 task-success rate of 0.8842 for exact B-copy and 0.8473 for C-full iterative teaching. The earlier phase table and p-value claim should therefore not be treated as validated until the experiment is rerun from a clean checkout and the raw data, analysis, and manuscript are reconciled. The present evidence is model-specific and does not establish that lossy inheritance is generally superior.
---

# 1. Research question

The study asks how exact inheritance and iterative, lossy teaching compare when agents learn under a bounded memory model and environmental conditions can change. The hypothesis that lossiness is beneficial is a testable hypothesis, not an established result.

# 2. Methods represented in the repository

The core GAL implementation defines:
- **B-copy:** exact copying of the parent's skill values and semantic concepts.
- **C-full:** three stochastic correction steps toward the parent's skill value, with inherited semantic concepts.
- **A:** no inherited skills or concepts.

The correction procedure is a particular algorithmic treatment. It should not be described as a general model of biological or cultural teaching without additional evidence.

# 3. Committed result audit

The committed `data/results/processed/summary.csv` reports the following Generation-10 mean task-success rates:

| Condition | Generation-10 mean |
|---|---:|
| A | 0.0413 |
| B-copy | 0.8842 |
| C-full | 0.8473 |
| C-no-memory | 0.8160 |
| C-low-effort | 0.3660 |

For the committed summary, B-copy exceeds C-full by 0.0369 (3.69 percentage points). This directly contradicts the previous manuscript statement that lossy teaching outperformed exact copying by +85.4%.

The repository also contains 100 raw seed files per condition for B-copy and C-full. The analysis script must be run against those exact committed files, with seed pairing verified and the test direction stated explicitly, before a new inferential result is reported.

# 4. Interpretation and limitations

The current committed results do not support the claim that C-full outperforms B-copy under the represented run. They also do not establish that exact copying is universally better. The outcome is conditional on the implementation, fitness function, environment schedule, and selected parameters.

The earlier table claiming a +0.854 lossy advantage, the statement that exact copying yields zero success after a shift, and the associated one-sided permutation-test claim are withdrawn pending a traceable reproduction. Do not cite those claims as established findings.

This experiment is a stylized two-skill agent simulation. It is not evidence that the same mechanism solves catastrophic forgetting in modern neural networks.

# 5. Reproducibility requirements

Before publication:
1. Run the analysis from the repository root using the committed `data/results/raw/` files.
2. Verify the 100 paired seed identifiers and compute the effect direction from raw observations.
3. Re-run the simulation from a clean environment and compare generated outputs with the committed artifacts.
4. Publish exact configuration, code revision, raw outputs, and analysis.
5. Update the compiled PDF so it matches this corrected source.

