#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "=== Reproducing Paper 4 (Neural Continual Learning) ==="
echo "[1/3] Running multi-seed neural MLP parameter sweep across shift frequencies..."
python3 "$REPO_ROOT/experiments/05_neural_continual_learning/run_multi_seed_neural.py"

echo "[2/3] Running Permuted-MNIST benchmark validation..."
python3 "$REPO_ROOT/experiments/05_neural_continual_learning/permuted_mnist_continual.py"

echo "[3/3] Compiling Paper 4 LaTeX manuscript to PDF..."
cd "$DIR"
pdflatex -interaction=nonstopmode paper4.tex > /dev/null
pdflatex -interaction=nonstopmode paper4.tex > /dev/null

echo "Paper 4 successfully reproduced! Output: $DIR/paper4.pdf"
