#!/bin/bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO_ROOT="$DIR/../.."

echo "=== Reproducing Consolidated Journal Manuscript ==="
echo "[1/3] Running Cryptographic Audit across 90 independent seeds..."
python3 "$REPO_ROOT/analysis/verify_scientific_validity.py"

echo "[2/3] Generating Figure 3 (Memory Economics Phase Diagram)..."
python3 "$REPO_ROOT/scripts/generate_paper3_figures.py"
cp "$REPO_ROOT/manuscripts/paper3/figure3_phase_diagram.png" "$DIR/"

echo "[3/3] Compiling Consolidated LaTeX Manuscript to PDF..."
cd "$DIR"
pdflatex -interaction=nonstopmode journal_paper.tex > /dev/null
pdflatex -interaction=nonstopmode journal_paper.tex > /dev/null

echo "Consolidated Journal Paper successfully reproduced! Output: $DIR/journal_paper.pdf"
