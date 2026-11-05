#!/bin/bash
set -euo pipefail
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "=== Reproducing Paper 4: canonical Split-MNIST protocol ==="
python3 "$REPO_ROOT/analysis/audit_original_100_seeds.py"
python3 "$REPO_ROOT/experiments/05_neural_continual_learning/canonical_split_mnist.py" --seeds "${SEEDS:-20}" --device "${DEVICE:-cpu}"
python3 "$REPO_ROOT/analysis/analyze_canonical_split_mnist.py"

if ! command -v pdflatex >/dev/null 2>&1; then
  echo "pdflatex is required to compile paper4.tex" >&2
  exit 2
fi
cd "$DIR"
pdflatex -interaction=nonstopmode -halt-on-error paper4.tex
pdflatex -interaction=nonstopmode -halt-on-error paper4.tex
echo "Compiled: $DIR/paper4.pdf"
