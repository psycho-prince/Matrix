#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "==========================================================="
echo "  GAL Research: Phase Boundary Reproduction (Paper 2)      "
echo "==========================================================="

echo -e "\n1. Running Capacity/Volatility Parameter Sweep (100 lineages per grid point)..."
python3 "$REPO_ROOT/experiments/02_capacity_trap/exp_parameter_sweep.py"

echo -e "\n2. Running Independent Statistical Validation (Sign-flip Permutation)..."
python3 "$REPO_ROOT/analysis/validate_phase_boundary.py"

echo -e "\n3. Compiling Paper 2 LaTeX manuscript to PDF..."
cd "$DIR"
pdflatex -interaction=nonstopmode paper2.tex > /dev/null
pdflatex -interaction=nonstopmode paper2.tex > /dev/null

echo "==========================================================="
echo "  Paper 2 successfully reproduced! Output: $DIR/paper2.pdf"
echo "==========================================================="
