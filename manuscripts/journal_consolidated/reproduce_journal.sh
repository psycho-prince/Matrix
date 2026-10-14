#!/bin/bash
set -e

echo "=== Reproducing Consolidated Journal Manuscript ==="
echo "[1/3] Running Cryptographic Audit across 90 independent seeds..."
python3 ../../analysis/verify_scientific_validity.py

echo "[2/3] Generating Figure 3 (Memory Economics Phase Diagram)..."
python3 ../../scripts/generate_paper3_figures.py
cp ../paper3/figure3_phase_diagram.png ./

echo "[3/3] Compiling Consolidated LaTeX Manuscript to PDF..."
pdflatex -interaction=nonstopmode journal_paper.tex > /dev/null
pdflatex -interaction=nonstopmode journal_paper.tex > /dev/null

echo "Consolidated Journal Paper successfully reproduced! Output: manuscripts/journal_consolidated/journal_paper.pdf"
EOF
chmod +x manuscripts/journal_consolidated/reproduce_journal.sh
