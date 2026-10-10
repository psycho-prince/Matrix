#!/bin/bash
set -e
echo "Running GAL Simulation (100 agents, 10 generations, 100 seeds)..."
python3 experiments/runner.py --agents 100 --generations 10 --seeds 100 --outdir results
echo "Calculating exact paired statistics..."
python3 test_stats.py
echo "Compiling paper..."
pdflatex paper.tex > /dev/null
pdflatex paper.tex > /dev/null
echo "Reproducibility script complete."
