# Extended Split Digits study

## Pre-registered execution plan

- 10 tuning seeds (0-9), used only for EWC hyperparameter selection.
- 20 held-out evaluation seeds (1000-1019); increase to 30 with workflow input.
- Per-seed stratified 60/20/20 train/validation/test split.
- Five class-incremental tasks: (0,1), (2,3), (4,5), (6,7), (8,9).
- EWC strength grid: 1, 10, 100, 1000; select highest mean validation accuracy.
- Replay budgets: 5, 10, 20, 50 exemplars per class.
- Report final accuracy, 95% normal-approximation CIs, task-wise forgetting, and per-class accuracy.

## GAL-CL operationalization

GAL-CL is not native symbolic GAL. It is a testable neural operationalization of generational selective inheritance:

1. The model after task t is the parent generation.
2. Estimate diagonal Fisher importance on the current task's training data.
3. Rank all scalar parameters globally by Fisher importance.
4. The child inherits the top 70% scalar weights exactly.
5. Remaining 30% are reinitialized (Xavier for matrices, zero for biases).
6. The child is trained on the next task, with no replay memory.
7. Recompute and accumulate Fisher importance for the next generation.

This deliberately tests selective inheritance without replay. It is compared against FT, tuned EWC and replay methods. The 70% retention fraction is fixed before held-out evaluation; it must not be tuned on test results.

## Important caveats

- The dataset is small; conclusions do not establish performance on Fashion-MNIST or large-scale continual learning.
- The CI is a descriptive normal approximation; paired seed-level comparisons and bootstrap CIs should be added before publication.
- EWC tuning uses a disjoint tuning seed set, not the held-out evaluation set.
- The GAL-CL rule is an explicit new mapping, not evidence that the original symbolic GAL implementation itself learns neural tasks.
