# Scientific claim audit (2026-11-02)

This audit was performed against the repository's tracked source, manuscript text, and committed result artifacts. It is a code-and-artifact consistency review, not an independent reproduction of every experiment.

## Findings

### 1. Statistical audit: report the design precisely
- `data/cryptographic_validation_audit.json` records 3 conditions, 30 seeds per condition, and 90 condition-runs in total.
- The reported Welch comparison is between the 30 "Lamarckian Rentier (Freq=50)" observations and 30 "Agile Amnesia (Freq=5)" observations. The stored p-value is approximately 2.8564e-32.
- This supports a difference in the simulated retention trait under those specified conditions. It does not establish a universal law, prove causality outside the model, or validate AI continual-learning performance.
- The script's printed p-value annotation says `p < 0.0000000001`; the exact stored p-value is much smaller. The audit JSON's SHA-256 field should be verified by recomputing the canonical JSON digest, not merely checking that a hash string exists.

### 2. Neural continual-learning results do not support superiority
The committed `data/mnist/permuted_mnist_results.json` reports:
- Variance-Preserving Reset: 54.58% mean continual accuracy.
- EWC: 83.54%; Experience Replay: 83.75%; naive sequential cloning: 83.12%.
- In the capacity-bottleneck experiment, the recorded plasticity advantage is -6.25 percentage points (lossy: 90.62%, cloning: 96.88%).

Therefore the current committed benchmark does not show the proposed method outperforming these baselines. The manuscript must present these negative results and avoid claiming a solution to catastrophic forgetting.

### 3. The so-called Permuted-MNIST dataset is synthetic
`data/mnist/mnist_benchmark.py` constructs 8x8 binary digit-like prototype templates and adds Gaussian noise. It does not load canonical MNIST or the scikit-learn 8x8 Digits dataset. Permuting these generated vectors is a synthetic permuted-prototype benchmark, not canonical Permuted-MNIST. Rename it in claims, tables, and abstracts unless the experiment is rerun on a documented public dataset.

### 4. Variance-preservation statement needs qualification
The inheritance implementation adds independent noise to W1 and W2, but scales biases by f without adding noise. It also applies a global capacity projection after inheritance. Thus the simple variance identity is, at most, an expectation under assumptions for the noisy weight matrices before projection; it is not strict conservation of total parameter energy for the implemented full parameter state.

### 5. Reproduction and test harness issues
- The previous pytest discovery included `scripts/test_stats.py`, a command-line script that exits when its expected generated data is absent. The quality workflow now explicitly runs `pytest tests/`, avoiding that unrelated script.
- `analysis/independent_validation.py` searches `results/raw/` relative to the current working directory, while committed raw results are under `data/results/raw/`. Its documented root-level invocation therefore needs a path correction before it can be treated as a reproducibility check.
- Existing tests check that some artifacts exist and that selected p-values are small; they do not independently recompute the statistical audit, verify the digest, or validate dataset provenance.

### 6. Publication status
The repository contains manuscript sources and compiled PDFs. Repository contents alone do not establish peer review or journal acceptance. Describe them as manuscripts/preprints unless a journal acceptance or publication record is linked.

## Safe claims at this stage
1. GAL is a research framework for studying generational inheritance, retention, learning, and environmental change in stylized agent simulations.
2. The committed scalar-agent audit reports different evolved retention values between selected simulated environmental regimes (30 seeds per condition).
3. The current synthetic neural benchmark is exploratory and reports worse continual accuracy for the proposed variance-preserving reset than EWC, replay, and naive sequential training in its standard regime.
4. The codebase now has a CI workflow that compiles Python modules and runs the tests under `tests/`. A passing CI run is a software check, not a scientific replication.

## Required research work before strong claims
- Rerun the neural comparison on canonical, versioned datasets with documented preprocessing and fixed train/test splits.
- Use multiple seeds and paired task permutations; seed every RNG (including replay sampling and model initialization).
- Match memory, parameter, compute, and data budgets across baselines; report all method-specific overhead.
- Correct the theoretical statement to distinguish expected variance of selected weight matrices from total parameter norm after capacity projection.
- Fix and execute the independent validation script from a clean checkout.
- Publish raw per-seed results, configuration, environment lockfile, and analysis scripts for every reported table.
