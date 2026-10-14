# Matrix: Generational Artificial Life (GAL)

[![Scientific Reproducibility & Audit CI](https://github.com/psycho-prince/Matrix/actions/workflows/reproduce.yml/badge.svg)](https://github.com/psycho-prince/Matrix/actions/workflows/reproduce.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Verified Data Hash](https://img.shields.io/badge/SHA--256-Audit_Verified-success)](data/cryptographic_validation_audit.json)

This repository contains the codebase, empirical simulations, and peer-reviewed manuscripts for the **Generational Artificial Life (GAL)** research framework.

**Author:** Prince T Philip (`princephilip514@gmail.com`)  
**Date:** October 2026

---

## 🌟 Interactive Web Dashboard (Live on GitHub Pages)
Play with the live simulator directly in your browser:
👉 **[https://psycho-prince.github.io/Matrix/](https://psycho-prince.github.io/Matrix/)**

Or run locally via Python:
```bash
python3 web_dashboard/serve.py
```
Navigate to `http://localhost:8080`. Features live parameter sliders for shift frequencies, metabolic costs, and real-time generation plots.

---

## 🔬 Manuscripts & Preprints
* **`manuscripts/journal_consolidated/`**: **Flagship Consolidated Treatise** (*Memory Economics in Generational Artificial Life: How Environmental Volatility Dictates the Phase Boundary Between Lamarckian Inheritance and Agile Amnesia*). Synthesizes the Capacity Trap, the 90-seed multi-regime statistical audit ($p = 2.86 \times 10^{-32}$), and Neural Continual Learning into a unified submission targeting **ALIFE / GECCO / CoLLAs / Artificial Life (MIT Press)**. Includes LaTeX source and compiled PDF.
* **`manuscripts/paper1/`**: *The Capacity-Saturation Trap* (foundational limits of Lamarckian weight copying).
* **`manuscripts/paper2/`**: *Lossy Transmission as a Mathematical Regularizer* (Golden Ratio attractor discovery under chaotic volatility).
* **`manuscripts/paper3/`**: *Memory Economics: Environmental Volatility Selects Between Lamarckian Inheritance and Agile Amnesia* (Joint co-evolution of retention, learning rate, and capacity).
* **`manuscripts/paper4/`**: *Continual Learning via Generational Parameter Transmission* (Weight retention dynamics in Multi-Layer Perceptrons on nonlinear Circle vs. XOR task distributions).

---

## 🚀 Advanced Research Phases
* **`experiments/04_memory_economics/`**: Multi-seed joint evolution phase diagrams across environmental timescales.
* **`experiments/05_neural_continual_learning/`**: Neural network agents (MLP parameters) learning non-stationary task distributions under bounded parameter capacity.
* **`experiments/06_spatial_lattice_gal/`**: 2D toroidal spatial lattice simulation featuring traveling environmental waves and localized cultural competition.

---

## Quick Reproduction
To reproduce any manuscript's results and compile its PDF:
```bash
./manuscripts/paper1/reproduce.sh
./manuscripts/paper2/reproduce_paper2.sh
./manuscripts/paper3/reproduce_paper3.sh
```
