# Experiment record — 2026-11-02

## Run identity
- Repository: psycho-prince/Matrix
- Branch: research/gal-native-reproduction
- Source commit: 12baf9446a6fa08b9beb1c4d33c3ffc2517e8ea8
- Workflow run: 41416824440
- Workflow URL: https://github.com/psycho-prince/Matrix/actions/runs/41416824440
- Job: 125182601058 (extended; success)
- Artifact: split-digits-extended-results
- Artifact ID: 13127368635
- Artifact SHA-256: 2f2a6c4f891122039fd37b837c29a8179e92fe7bac7733e448a087c29ee6bb32
- Artifact URL: https://github.com/psycho-prince/Matrix/actions/runs/41416824440/artifacts/13127368635

## Protocol actually executed
- Dataset: scikit-learn Optical Recognition of Handwritten Digits (8x8), not MNIST.
- Five class-incremental tasks: (0,1), (2,3), (4,5), (6,7), (8,9).
- 10 EWC tuning seeds (0–9); 20 held-out evaluation seeds (1000–1019).
- Per-seed stratified 60/20/20 train/validation/test split.
- 8 epochs per task; batch size 64.
- Methods: FT, EWC, ER-5/10/20/50, GAL-CL.
- EWC grid: 1, 10, 100, 1000; selected 1000 from tuning validation accuracy.
- GAL-CL is a neural proxy: global Fisher top-70% scalar weight retention; remaining weights reset; no replay. It is NOT the original symbolic GAL system.

## Observed results
Final all-class test accuracy and mean forgetting (20 seeds):

| Method | Final accuracy | SD | 95% normal CI | Mean forgetting |
|---|---:|---:|---:|---:|
| FT | 14.18% | 5.22 pp | 11.89–16.47% | 55.26% |
| EWC | 18.07% | 7.35 pp | 14.85–21.29% | 48.02% |
| ER-5 | 45.06% | 11.58 pp | 39.98–50.13% | 28.75% |
| ER-10 | 45.47% | 11.57 pp | 40.40–50.54% | 27.45% |
| ER-20 | 44.99% | 10.47 pp | 40.40–49.57% | 28.73% |
| ER-50 | 45.65% | 12.67 pp | 40.10–51.20% | 29.01% |
| GAL-CL proxy | 17.99% | 1.04 pp | 17.53–18.44% | 74.90% |

These are descriptive results from this particular small benchmark and implementation. No paired significance tests or bootstrap intervals were included. Do not interpret overlapping or non-overlapping normal CIs as formal pairwise tests.

## Audit findings and limitations
1. The workflow completed and uploaded its JSON artifact successfully.
2. This experiment does not validate the original GAL theory or original symbolic Agent/Environment implementation.
3. The dataset is the small 8x8 sklearn digits dataset, not MNIST, Fashion-MNIST, or a large-scale benchmark.
4. GAL-CL is a newly defined neural proxy and performs poorly here; report the negative result transparently.
5. Code audit found the EWC implementation accumulates Fisher diagonals across tasks but overwrites the reference means with the latest task's parameters. This is not the usual per-task EWC formulation and needs correction or a clearly specified online-EWC derivation before treating EWC as a sound baseline.
6. ER and non-replay methods use equal optimizer-step counts and batch sizes, but ER allocates half of each batch to replay and therefore has different current-task sample exposure. Report this distinction.
7. Confidence intervals are normal approximations; add paired seed-level comparisons, bootstrap intervals, and multiple-comparison handling before publication.
8. The script's GAL-CL helper accepts a seed argument that is unused; remove it or use it for a documented stochastic operation.
9. Do not use this benchmark as evidence for or against the foundational GAL hypothesis. It is an exploratory neural continual-learning side experiment only.

## Next actions
- Correct and unit-test EWC using a defensible canonical or explicitly specified online formulation.
- Add unit tests for task masks, inheritance fraction, exact inherited-value preservation, reset-value behavior, memory budgets, and forgetting calculation.
- Add paired seed-level statistics and bootstrap confidence intervals.
- Keep neural proxy experiments separate from the original GAL Artificial Life experiments.
- Return to the core GAL population/environment/inheritance mechanisms for foundational validation.

## Integrity rule
Never overwrite this record with improved results. Add a new dated record for each new run, and retain failed runs and protocol deviations.
