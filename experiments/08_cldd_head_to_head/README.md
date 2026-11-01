# CLDD continual-learning benchmark integration

Status: protocol and published-baseline audit only. No GAL-on-Fashion-MNIST result is claimed here.

## Benchmark source

- Dataset/repository: https://github.com/tachyonicClock/cldd
- Dataset DOI: https://doi.org/10.5281/zenodo.21232615
- Official task stream: RotatedFashionMNISTPT, using the archived `rotated_fashion_mnist_data.pt`
- Official learner implementations: FT, EWC, SI in the CLDD repository (CapyMOA 0.15.1)
- Model: FashionCNN
- Drift conditions: abrupt, gradual, slow
- CLDD-A: 3 boundaries x 6 strategies x 1 oracle detector x 20 seeds = 360 configurations.
- Published `data/evaluate/data_frame.csv`: 10 evaluation seeds per strategy/boundary; the CLDD workflow defines separate 10-seed tuning and evaluation sets.

## Critical compatibility decision

The original GAL agent is a symbolic agent with five scalar skills and a set of semantic concept IDs. It is not a neural network learner and does not currently consume image tensors or class labels. Therefore, directly comparing its native task-success score with CLDD classification accuracy would be invalid.

The head-to-head must have two clearly separated tracks:

1. **Benchmark reproduction:** run the official CLDD implementation for FT, EWC and SI using its original FashionCNN, task streams, optimizer, task schedule and evaluation loop. Confirm the published CSV values within expected seed/run variability.
2. **GAL-CL research implementation:** explicitly define and document a neural representation of GAL inheritance. It must preserve GAL's inheritance logic as far as possible, be named GAL-CL (not native GAL), and be evaluated on the same task streams, architecture, exposure and compute budget. Any neural mapping is a new operationalization and requires ablations.

Do not label neural weight noise/perturbation as native GAL.

## Metrics

Primary:
- final accuracy (`ocl.accuracy_final`)
- average accuracy on seen tasks (`ocl.accuracy_seen_avg`)
- backward transfer (`ocl.backward_transfer`)

Secondary:
- test-then-train stream accuracy (`ttt.accuracy`)
- forgetting derived from the per-task accuracy matrix
- peak and persistent memory use
- training examples, optimizer steps and wall-clock time

## Statistical protocol

- Pair methods by identical evaluation seed and drift condition.
- Keep tuning seeds separate from held-out evaluation seeds.
- Report mean, standard deviation, 95% confidence intervals and paired effect sizes.
- Correct multiple comparisons (Holm) for planned pairwise tests.
- Report failed runs and missing seeds; never silently drop them.
- Compare only methods using the same task stream and evaluation metric.

## Immediate next steps

1. Reproduce official FT, EWC and SI with CLDD's own code and pinned dependencies.
2. Verify the data archive and exact seed split against the workflow and datasheet.
3. Only after reproduction passes, implement GAL-CL as a separate learner and run a small smoke test.
4. Run paired held-out experiments across all three drift conditions.

## Current result status

Published CSV analysis is available separately. No fresh local CLDD training run and no GAL-CL evaluation have been completed as part of this integration yet.
