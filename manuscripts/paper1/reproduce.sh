#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "==========================================================="
echo "  Reproducing Paper 1 (Copying vs. Iterative Teaching)     "
echo "==========================================================="

echo -e "\n1. Running GAL Simulation (100 agents, 10 generations, 100 seeds)..."
python3 "$REPO_ROOT/experiments/02_capacity_trap/runner.py" --agents 100 --generations 10 --seeds 100 --outdir "$REPO_ROOT/data/results"

echo -e "\n2. Calculating exact paired statistics..."
python3 "$REPO_ROOT/scripts/test_stats.py" "$REPO_ROOT/data/results"

echo -e "\n3. Compiling Paper 1 LaTeX manuscript to PDF..."
cd "$DIR"
pdflatex -interaction=nonstopmode paper.tex > /dev/null
pdflatex -interaction=nonstopmode paper.tex > /dev/null

echo "Paper 1 successfully reproduced! Output: $DIR/paper.pdf"
