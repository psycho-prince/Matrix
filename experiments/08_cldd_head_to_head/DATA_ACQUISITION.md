# CLDD raw training-data acquisition: blocker report

Date: 2026-11-02

## What was verified

The public CLDD download linked by the upstream README is:

`https://pub-69d9a50abcb04461bc0b8f04d7a47656.r2.dev/cldd_dataset.zip`

The GitHub Actions run downloaded the archive, passed ZIP CRC validation, identified the published CLDD Parquet dataset, and uploaded the archive plus a manifest.

Successful run:
https://github.com/psycho-prince/Matrix/actions/runs/41344109685

This archive is the published drift-detection dataset. Its documented schema contains error_stream, trues, preds, boundary, strategy, detector and seed fields. It is not the raw image training data.

## What the upstream training code requires

In upstream `tachyonicClock/cldd`, `src/scenario.py` implements `RotatedFashionMNISTPT` by loading:

`data/rotated_fashion_mnist_data.pt`

The loader expects a PyTorch object with `dataset["train"]` and `dataset["test"]`, each containing task-wise (x, y) tensor pairs.

If the file is absent, the code raises FileNotFoundError. The public repository tree inspected for this audit does not contain this tensor file or an obvious generator script. The upstream README's public ZIP link points to the CLDD benchmark archive, not to the tensor file.

## Reproduction status

- Published CLDD Parquet archive: acquired and integrity-checked.
- Raw rotated Fashion-MNIST tensor file: not located in the upstream repository or linked download.
- Fresh FT/EWC/SI training: not run.
- GAL-CL training: not run.

Do not substitute the published error_stream values for image data. They are learner outputs, not training examples. Do not substitute CapyMOA's built-in RotatedFashionMNIST without labelling it as a modified reproduction: the upstream configuration specifically selects RotatedFashionMNISTPT.

## Required next action

Locate the exact `rotated_fashion_mnist_data.pt` file from the authors' supplementary materials or obtain confirmation from the dataset authors of the generation procedure and preprocessing. Verify SHA-256 and tensor shapes before use. If unavailable, request the artifact from the authors or create a clearly labelled independent reproduction using a documented public Fashion-MNIST source and deterministic rotation pipeline; do not claim exact reproduction of the published benchmark.
