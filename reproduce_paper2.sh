#!/bin/bash
set -e

echo "==========================================================="
echo "  GAL Research: Phase Boundary Reproduction (Paper 2)      "
echo "==========================================================="

echo -e "\n1. Running Capacity/Volatility Parameter Sweep (100 lineages per grid point)..."
python experiments/exp_parameter_sweep.py

echo -e "\n2. Running Independent Statistical Validation (Sign-flip Permutation)..."
python validate_phase_boundary.py

echo -e "\n==========================================================="
echo "  REPRODUCTION COMPLETE. Raw data saved to results/        "
echo "==========================================================="
