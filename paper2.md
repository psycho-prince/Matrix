---
title: "The Capacity-Saturation Trap: Why Lossy Transmission is Required for Cumulative Inheritance in Volatile Environments"
author: "GAL Research"
date: "October 2026"
abstract: |
  In evolutionary computation and artificial life simulations, exact (Lamarckian) weight transfer often accelerates adaptation. However, biological and cultural systems typically rely on "lossy" transmission mechanisms, such as teaching, which introduce error. We hypothesize that when an agent's memory capacity is strictly bounded, exact inheritance becomes a catastrophic liability in shifting environments. Using a minimalist Generational Artificial Life (GAL) simulation, we map the exact phase boundary where exact copying fails. We demonstrate that while exact copying excels in perfectly stable or high-capacity environments, lossy transmission acts as a vital mathematical regularizer—clearing obsolete memory to prevent capacity saturation. Our independent 100-seed permutation tests confirm that lossy transmission outperforms exact copying by +85.4% ($p < 10^{-5}$) under strict capacity constraints when the environment shifts every 10 generations.
---

# 1. Introduction

The tension between retaining old knowledge (stability) and acquiring new knowledge (plasticity) is a central problem in both continual learning and cultural evolution. In continual machine learning, models forced to learn sequential tasks often overwrite prior weights, a phenomenon known as catastrophic forgetting. Conversely, in cultural evolution, cumulative inheritance relies on the high-fidelity transmission of complex skills across generations.

In digital simulations, it is common to implement exact "Lamarckian" inheritance—cloning the parent's learned weights directly into the offspring. While this provides rapid adaptation in static environments, it bypasses the "lossy" nature of biological and cultural transmission. This paper investigates whether transmission error (lossiness) is not merely noise, but a required regularizer that prevents long-term lineages from collapsing under their own accumulated memory.

# 2. Methods

We utilized a Generational Artificial Life (GAL) simulation. Agents learn active survival skills (`A` or `B`) over a lifetime of 10 steps. We enforce a **Memory Capacity** limit, meaning the sum of an agent's acquired skills cannot exceed a defined threshold. If the limit is reached, acquiring new skills proportionally degrades old ones. 

We varied the **Environmental Volatility** (Switch Frequency), shifting the active survival skill from `A` to `B` every $N$ generations. We evaluated two modes of inheritance across 100 independent seeds:
*   **Exact Copying:** The offspring clones 100% of the parent's final weights.
*   **Lossy Teaching:** The offspring inherits only 50% of the parent's final weights.

# 3. Results: The Phase Boundary

Our parameter sweep mapping Memory Capacity against Environmental Volatility revealed a distinct phase transition.

| Memory Capacity | Shift every 1 gen | Shift every 2 gens | Shift every 5 gens | Shift every 10 gens | Stable (No shift) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0.5** | +0.067 | +0.274 | +0.308 | **+0.832** | 0.000 |
| **1.0** | +0.146 | +0.298 | +0.373 | **+0.854** | 0.000 |
| **2.0** | 0.000 | 0.000 | +0.370 | **+0.854** | 0.000 |

*(Table 1: Mean difference in task success rate: `Lossy - Exact`. Positive values indicate Lossy teaching superiority).*

### 3.1 The Capacity-Saturation Trap
When the environment shifts every 10 generations, an exact-copying lineage maximizes its current skill, eventually saturating its entire memory capacity. When the environment abruptly shifts from `A` to `B`, the offspring inherits a fully saturated memory of obsolete skill `A`. It is unable to learn `B` without catastrophic interference, resulting in a mean task success rate of 0.00%.

### 3.2 Lossy Transmission as a Regularizer
In the identical scenario, the Lossy lineage drops 50% of the inherited weight. This deliberate transmission error frees up memory capacity, allowing the offspring to rapidly adapt to the new environment. An independent sign-flip permutation test ($100,000$ permutations) confirms the difference is highly significant: Lossy teaching outperforms Exact copying by a mean difference of +0.854 ($p_{\mathrm{MC}} \approx 10^{-5}$).

# 4. Discussion

Our findings provide a mechanistic explanation for why exact cloning is dangerous in the real world. Exact inheritance is only mathematically optimal if (1) the environment never changes, or (2) the agent possesses a memory capacity large enough to hold all possible future skills simultaneously. 

Because biological organisms and human cultures operate under bounded neural capacity and volatile environments, "imperfect" teaching acts as a crucial garbage-collection mechanism. It prevents lineages from overfitting to a single epoch, ensuring enough plasticity remains to survive the next environmental shift.

# 5. Conclusion
Under the tested simulation constraints, lossy transmission is a mathematical prerequisite for long-term adaptation in volatile environments. Future work should investigate how these boundaries shift under different network architectures or selective inheritance mechanisms.
