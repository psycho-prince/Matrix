# Split Digits class-incremental benchmark (independent fallback)

This experiment avoids the unavailable CLDD raw tensor file. It uses scikit-learn's bundled Optical Recognition of Handwritten Digits dataset (8x8 grayscale, 10 classes) and a deterministic five-task class-incremental split: (0,1), (2,3), (4,5), (6,7), (8,9).

This is an **independent benchmark**, not a reproduction of CLDD and not a result for native GAL.

## Methods
- FT: sequential fine-tuning.
- EWC: diagonal Fisher regularization after each task.
- ER: reservoir-like fixed memory, here balanced exemplars per class, replayed during subsequent task training.

All methods use the same MLP, task order, train/test split, epoch count, and seeds. Final evaluation is over all ten classes (class-incremental; no task ID at inference).

## Run
```bash
python -m pip install torch scikit-learn numpy
python experiments/09_split_digits/run_benchmark.py --seeds 3 --epochs 8
```

The default is deliberately small for a smoke benchmark. Increase seeds and epochs only after checking the run logs and deterministic protocol.

## Limitations
- Digits is small and 8x8; it is a pipeline-validation benchmark, not a substitute for Fashion-MNIST-scale evaluation.
- EWC uses a diagonal Fisher approximation.
- ER memory is balanced by class and fixed at 20 exemplars per class.
- No GAL-CL result is included. GAL-CL must be a separately specified learner, not a relabelled FT/ER/EWC implementation.
