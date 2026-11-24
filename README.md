# Matrix: Generational Artificial Life (GAL)

[![Scientific Reproducibility & Audit CI](https://github.com/psycho-prince/Matrix/actions/workflows/reproduce.yml/badge.svg)](https://github.com/psycho-prince/Matrix/actions/workflows/reproduce.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This repository contains software, simulations, research notes, manuscripts, and preprints related to **Generational Artificial Life (GAL)**.

**Author:** Prince T Philip  
**Research status:** Active research; claims and results are at different stages of validation.

---

## Scientific status and scope

The repository is a research programme, not a single validated scientific theory. It contains exploratory prototypes, controlled synthetic simulations, mathematical proposals, and manuscripts at different levels of maturity. The presence of code, a passing software test, a reproducible run, or a small p-value does not by itself establish a scientific mechanism or its generality.

Unless a specific publication record is linked, manuscripts in this repository should be treated as **preprints or research drafts**, not as peer-reviewed publications.

Current evidence is conditional on the assumptions, task environments, transfer rules, resource constraints, and evaluation protocols implemented in each experiment. In particular:

- Results from fixed synthetic tasks do not establish general intelligence, biological equivalence, or open-ended evolution.
- The memory-economics and capacity-saturation experiments are simplified computational models. Their outcomes should not be generalized to biological metabolism, human culture, or neural memory without independent empirical bridges.
- The neural continual-learning experiments include exploratory proxies. The synthetic 8×8 digit-like benchmark is not canonical MNIST, and the current results do not establish that GAL outperforms established continual-learning methods.
- The Golden Ratio experiments are exploratory parameter searches under selected schedules. They do not establish a universal Golden Ratio law or attractor.
- The repository does not provide experimental evidence for machine consciousness or subjective experience.

See the relevant manuscript, experiment protocol, result audit, and limitations before interpreting any reported result.

---

## Interactive Web Dashboard

Play with the simulator in your browser:

[https://psycho-prince.github.io/Matrix/](https://psycho-prince.github.io/Matrix/)

Or run locally:

```bash
python3 web_dashboard/serve.py
```

Then navigate to `http://localhost:8080`. The dashboard exposes simulation parameters and generation plots; it is an exploration interface, not an independent scientific validation tool.

---

## Manuscripts and preprints

The following manuscripts are research outputs in the repository. Their publication and validation status should be checked individually; listing them here does not imply peer review.

- **`manuscripts/paper1/` — “Evaluating Parameter Copying vs. Iterative Teaching in Matrix Environments.”** A paired-seed comparison of exact parameter copying and a specified stochastic iterative-correction operator. The result is specific to that implementation; the correction procedure is not equivalent to a full empirical teacher–learner feedback process.
- **`manuscripts/paper2/` — “The Capacity-Saturation Trap: Why Lossy Transmission is Required for Cumulative Inheritance in Volatile Environments.”** A simplified model of bounded skill capacity, environmental switching, exact copying, and fixed fractional retention. Interpret “lossy transmission” as the specific retention operator implemented in this experiment.
- **`manuscripts/paper3/` — “Memory Economics: Environmental Volatility Selects Between Lamarckian Inheritance and Agile Amnesia.”** An exploratory model of retention, learning rate, capacity, and environmental schedules. Seed counts and configurations differ across the main experiment and supplementary audits; consult the protocol and raw results before interpreting effect sizes.
- **`manuscripts/paper4/` — “Continual Learning via Generational Parameter Transmission.”** An exploratory neural-network study. Its benchmark naming, result tables, random seeding, and baseline comparability require correction before its claims can be treated as confirmatory.
- **`manuscripts/journal_consolidated/` — consolidated research manuscript.** A synthesis of the memory-economics and continual-learning programme. Proposed analytical results and theorem statements remain subject to mathematical and implementation audits; do not treat them as established theorems unless a complete derivation and supporting validation are provided.

---

## Research and experiment areas

- **`experiments/02_capacity_trap/`**: controlled experiments on capacity limits and environmental switching.
- **`experiments/04_memory_economics/`**: exploratory multi-regime studies of retention, learning, capacity, and resource penalties.
- **`experiments/05_neural_continual_learning/`**: neural-network prototypes under changing task distributions; these are not evidence of superiority over established continual-learning methods.
- **`experiments/06_spatial_lattice_gal/`**: a spatial-lattice prototype with local interactions and environmental waves.
- **`experiments/10_foundational_gal/`**: native GAL confirmatory protocol, results, and independent scientific audit.

GAL 2.0 is a parallel research implementation focused on structured capabilities, evidence provenance, memory stores, inheritance, and successor-side revalidation. Its current synthetic task executor does not yet establish that episodic, semantic, or procedural memory causally improves task solving. See `gal2/SCIENTIFIC_VALIDATION_GAP_AUDIT.md`.

---

## Reproduction and auditing

Reproduction scripts are provided for selected manuscripts:

```bash
./manuscripts/paper1/reproduce.sh
./manuscripts/paper2/reproduce_paper2.sh
./manuscripts/paper3/reproduce_paper3.sh
./manuscripts/paper4/reproduce_paper4.sh
```

A script completing successfully means that the scripted workflow ran; it does not independently validate the scientific interpretation. Some scripts, manuscript tables, seed counts, and committed result files have known discrepancies documented in the relevant audits. Check those before relying on a reported number.

For the native GAL confirmatory study, begin with:

- `experiments/10_foundational_gal/FOUNDATIONAL_VALIDATION_PROTOCOL.md`
- `experiments/10_foundational_gal/INDEPENDENT_SCIENTIFIC_AUDIT.md`
- `experiments/10_foundational_gal/RESEARCH_LOG.md`

For GAL 2.0, begin with:

- `gal2/README.md`
- `gal2/SCIENTIFIC_VALIDATION_GAP_AUDIT.md`
- `gal2/ANALYTICAL_THEORY.md`

For contributions, distinguish implementation correctness, internal reproducibility, independent replication, and external scientific validity. These are separate standards.
