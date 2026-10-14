#!/bin/bash
set -e

echo "=== Reproducing Paper 4 (Neural Continual Learning) ==="
echo "[1/2] Running multi-seed neural MLP parameter sweep across shift frequencies..."
python3 ../../experiments/05_neural_continual_learning/run_multi_seed_neural.py

echo "[2/2] Compiling Paper 4 LaTeX manuscript to PDF..."
pdflatex -interaction=nonstopmode paper4.tex > /dev/null
pdflatex -interaction=nonstopmode paper4.tex > /dev/null

echo "Paper 4 successfully reproduced! Output: manuscripts/paper4/paper4.pdf"
EOF
chmod +x manuscripts/paper4/reproduce_paper4.sh
