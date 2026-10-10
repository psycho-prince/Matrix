# Matrix: Generational Artificial Life (GAL)

This repository contains the codebase and scientific findings for the **Generational Artificial Life (GAL)** research project.

## Project Structure

* **`manuscripts/`**: Contains the draft papers and preprints synthesizing our findings.
  * `paper1/`: The foundational Capacity-Saturation Trap.
  * `paper2/`: The discovery of the Golden Ratio attractor under chaotic volatility.
  * `paper3/`: "Memory Economics" - Co-evolution of learning rate, retention, and capacity.
  * `preprints/`: Literature reviews and release logs.
* **`experiments/`**: Contains the reproducible evolutionary scripts categorized by research phase.
  * `01_llm_prototypes/`: Early generative AI and cultural evolution prototypes.
  * `02_capacity_trap/`: Scripts establishing the bounds of memory capacity.
  * `03_golden_ratio/`: Scripts documenting the mathematical emergence of the ~$0.618$ attractor.
  * `04_memory_economics/`: Scripts for the joint-evolution phase diagrams and cost-of-learning metrics.
* **`analysis/`**: Validation scripts and statistical analyzers.
* **`scripts/`**: Utility scripts for testing LLM models and running helper functions.
* **`data/`**: Output data from major simulation runs.
* **`gal/`**: The core simulation engine module.

## Reproduction
Each manuscript directory contains its respective reproducibility script (e.g. `reproduce.sh`). 
