#!/bin/bash
set -e

# Create main directories
mkdir -p manuscripts/paper1 manuscripts/paper2 manuscripts/paper3 manuscripts/preprints
mkdir -p scripts analysis data

# Move manuscripts
mv paper.* manuscripts/paper1/ || true
mv paper2.* manuscripts/paper2/ || true
mv LITERATURE_REVIEW.md PREPRINT_RELEASE.md manuscripts/preprints/ || true

# Copy Paper 3 from artifact directory
cp /home/kali/.gemini/antigravity-cli/brain/588f8bff-460d-4f43-9fcf-c2ab5ff8edae/paper3_memory_economics.md manuscripts/paper3/paper.md

# Move reproduction and analysis scripts
mv reproduce.sh manuscripts/paper1/ || true
mv reproduce_paper2.sh manuscripts/paper2/ || true
mv validate_phase_boundary.py independent_validation.py analysis/ || true
mv test_stats.py test_llm.py list_models.py scripts/ || true

# Move results into data/
mv test_run test_run_fixed test_results_final gal_simulation_results results data/ || true

# Organize experiments
cd experiments
mkdir -p 01_llm_prototypes 02_capacity_trap 03_golden_ratio 04_memory_economics

# 01_llm_prototypes
mv exp00* 01_llm_prototypes/ || true

# 02_capacity_trap
mv exp_capacity_shift.py exp_parameter_sweep.py exp_hypothesis_test.py runner.py 02_capacity_trap/ || true

# 03_golden_ratio
mv exp_golden_ratio.py exp_pure_math.py exp_pi_volatility.py exp_fibonacci_volatility.py exp_ultimate_law.py exp_ultimate_pure_math.py exp_optimal_f_vs_frequency.py exp_constants_battle.py exp_evolutionary_discovery.py 03_golden_ratio/ || true

# 04_memory_economics
mv exp_coevolution_learning_retention.py exp_lr_vs_retention_boundary.py exp_cost_of_learning.py exp_evolve_capacity.py exp_information_tracking.py exp_joint_evolution_env_rates.py 04_memory_economics/ || true

cd ..

# Make a clean commit
git add .
git commit -m "Refactor: structure repository into manuscripts, experiments, analysis, and data"

