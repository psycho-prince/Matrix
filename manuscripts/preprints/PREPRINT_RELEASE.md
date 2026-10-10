# GAL Simulation: Matrix-Main Preprint Release Notes

## Release Commit
**Commit Hash:** `v1.0-preprint`
**Environment:** Linux (Python 3.x), detailed in `requirements.txt`

## 1. Verified Scientific Claim
Based on internal reproducibility and statistical checks, this repository advances the following strictly bounded claim:
> Under the tested simulation conditions, exact-copy inheritance achieved a higher mean final task-success score than the specified stochastic iterative error-correction inheritance method across 100 paired seeds.

This simulation **does not** assert universal superiority of copying over teaching, it **does not** generalize beyond these specific algorithmic constraints, and it **does not** claim discovery of novel thermodynamic or cosmological laws.

## 2. Internal Validation Summary
Prior to external review, the following internal consistency checks were passed:
* **Deterministic Reproducibility:** Two independent clean checkouts produced bit-for-bit identical raw outputs across all active modes.
* **Paired Comparison Integrity:** Exactly 100 unique seeds per condition, fully matched in pairwise arrays. Baseline fairness is enforced via a dual-RNG architecture separating lifetime events from inheritance mechanisms.
* **Statistical Robustness:** A paired sign-flip permutation test (100,000 permutations) on the final generation task-success differences yielded zero extreme exceedances. Utilizing the plus-one estimator, the empirical probability is reported as $p_{\mathrm{MC}} = 1/100001 \approx 10^{-5}$.
* **Publication Artifacts:** The manuscript (`paper.pdf`) successfully recompiles directly from `paper.tex` during the pipeline execution, preserving complete alignment between the written report and the digital experiment.

## 3. External Review Instructions
External researchers are encouraged to independently validate these findings. 
1. Clone the repository at the specified commit hash.
2. Execute `./reproduce.sh` to autonomously recreate the 100-seed data set, recalculate the exact paired t-statistics, and regenerate the manuscript.
3. Compare the generated `/results/` directory against the archived baseline.
