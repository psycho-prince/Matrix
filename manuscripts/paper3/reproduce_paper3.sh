#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "=== Reproducing Paper 3 (Memory Economics) ==="
echo "[1/3] Running multi-seed joint evolution phase diagram experiment..."
python3 "$REPO_ROOT/experiments/04_memory_economics/exp_joint_evolution_env_rates.py"

echo "[2/3] Generating Figure 3 (phase diagram)..."
python3 "$REPO_ROOT/scripts/generate_paper3_figures.py"

echo "[3/3] Compiling LaTeX manuscript to PDF..."
cd "$DIR"
pdflatex -interaction=nonstopmode paper3.tex > /dev/null
pdflatex -interaction=nonstopmode paper3.tex > /dev/null

echo "Paper 3 successfully reproduced! Output: $DIR/paper3.pdf"
