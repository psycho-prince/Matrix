# Matrix: Generational Artificial Life (GAL)

This repository contains the codebase, empirical simulations, and peer-reviewed manuscripts for the **Generational Artificial Life (GAL)** research framework.

**Author:** Prince T Philip (`princephilip514@gmail.com`)  
**Date:** October 2026

---

## 🌟 Interactive Web Dashboard (Option 4)
Run the browser simulator to interactively explore memory economics and phase boundaries:
```bash
python3 web_dashboard/serve.py
```
Then navigate to `http://localhost:8080` in your web browser. Features live parameter sliders for shift frequencies, metabolic costs, and real-time generation plots.

---

## 🔬 Manuscripts & Preprints
* **`manuscripts/paper1/`**: *The Capacity-Saturation Trap* (foundational limits of Lamarckian weight copying).
* **`manuscripts/paper2/`**: *Lossy Transmission as a Mathematical Regularizer* (Golden Ratio attractor discovery under chaotic volatility).
* **`manuscripts/paper3/`**: *Memory Economics: Environmental Volatility Selects Between Lamarckian Inheritance and Agile Amnesia* (Joint co-evolution of retention, learning rate, and capacity). Includes full LaTeX source and compiled PDF.

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
