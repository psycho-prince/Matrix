# Memory Economics: Environmental Volatility Selects Between Lamarckian Inheritance and Agile Amnesia

**Author:** Prince T Philip  
**Email:** princephilip514@gmail.com  
**Date:** 10/10/2026  

## Abstract
In generational artificial life models, the optimal rate of knowledge inheritance is classically assumed to be bounded by the rate of environmental change. We show that when learning speed and memory capacity are allowed to co-evolve alongside retention rates under metabolic constraints, the evolutionary dynamics of memory become highly non-monotonic. We map the trade-off surface of retention ($f$), learning rate ($lr$), and capacity ($c$) across a spectrum of environmental shift frequencies. Extremely rapid environmental fluctuation (shifts every 2 generations) produces a "boomerang" strategy favoring larger brain capacity, minimal learning, and high retention ($>90\%$), as retaining old skills is metabolically cheaper than relearning them. Intermediate volatility flips the population into "agile amnesia," characterized by low retention ($\sim 19\%$), elevated learning rates, and smaller capacities. Long-term environmental stability favors "Lamarckian rentiers" exhibiting high retention and minimal learning. Furthermore, tracking information provenance reveals that in the agile amnesia regime, up to 85% of active memory consists of newly acquired data, relegating inherited knowledge to a short-lived bootstrap buffer. These findings reframe biological and artificial inheritance not as static physiological traits, but as fluid economic equilibria governed by environmental cadence and the metabolic costs of neuroplasticity.

---

## 1. Introduction
A fundamental challenge for adaptive systems in non-stationary environments is balancing the retention of ancestral knowledge with the acquisition of novel skills. Previous work in this domain established that under fixed, slow learning rates and chaotic environmental shifts, evolutionary algorithms discover an optimal fractional retention rate near the Golden Ratio conjugate ($1/\phi \approx 0.618$). 

However, biological agents operate under metabolic constraints where rapid learning and large memory capacities are energetically costly. This study investigates the conditional nature of the aforementioned attractor. We hypothesize that the optimal strategy for knowledge transmission is a function of "memory economics": the metabolic cost of learning, the upkeep cost of memory capacity, and the frequency of environmental change. By co-evolving retention, learning rate, and capacity, we map the full phase diagram of evolutionary strategies across multiple temporal scales of environmental volatility.

---

## 2. Model
We extend the Generational Artificial Life (GAL) framework to support the joint evolution of three continuous traits:
1. **Retention ($f \in [0, 1]$):** The fraction of the parent's accumulated skill level passed to the offspring.
2. **Learning Rate ($lr \in [0.001, 0.25]$):** The rate at which the agent acquires skill points during its active learning phase.
3. **Capacity ($c \in [0.1, 5.0]$):** The maximum total skill points an agent can hold simultaneously. If exceeded, existing skills are proportionally scaled down.

**Skill Accumulation & Work:** 
During their lifetime, agents dedicate time steps to learning the currently active environmental skill, followed by a work phase where they attempt tasks based on their skill level.

**Metabolic Costs:**
To accurately reflect biological trade-offs, we impose two critical costs:
* *Cost of Learning:* High learning rates incur a time penalty, proportionally reducing the number of tasks an agent can attempt during its work phase (simulating time spent learning rather than exploiting).
* *Cost of Capacity:* Agents pay a baseline fitness penalty for maintaining larger memory capacities ($0.05 \times c$), regardless of whether the capacity is actively utilized.

**Environmental Shifts & Selection:** 
The environment demands one of two distinct skills (A or B). The active skill shifts according to discrete generation schedules: Periodic (every $k$ generations) or Chaotic (intervals following Fibonacci and Pi digit sequences). Fitness is proportional to task success efficiency and absolute productivity, minus metabolic costs. The top 50% of the population reproduces with Gaussian mutation applied to all three traits.

---

## 3. Results

### 3.1 The Cost of Learning and Agile Amnesia
Baseline experiments allowing free (zero-cost) learning resulted in an immediate crash of retention ($f \approx 0.23$) and maximized learning rates ($lr \approx 0.20$). However, introducing a moderate time penalty on learning completely reversed this dynamic, collapsing the learning rate to near-zero ($lr \approx 0.01$) and restoring high retention ($f > 0.70$). This suggests that under our model's assumptions, the "fast-learning amnesiac" strategy is only viable when the cost of learning is negligible; under metabolic constraints, populations revert to strict Lamarckian copying.

### 3.2 Evolutionary Shrinkage of Brain Capacity
When brain capacity ($c$) was allowed to co-evolve alongside $f$ and $lr$ under chaotic environmental shifts, evolution actively selected for smaller brains. Mean capacity shrank from an initial $1.18$ to $0.57$. Because large memory is expensive to maintain and difficult to fill usefully before a chaotic shift renders it obsolete, evolutionary selection favored small, overwrite-friendly brains paired with high learning rates and low retention.

### 3.3 Information Provenance
By tracking the exact bits of information utilized by agents at the end of their lifetime, we quantified the actual utilization of parental memory. In populations that evolved the "agile amnesia" trait cluster, 85.6% of the final skill level consisted of information actively learned during the agent's lifetime. Inherited information (14.4%) served merely as a short-lived bootstrap buffer to survive early-life tasks before being overwritten by new learning.

### 3.4 Joint Evolution Phase Diagram
The most significant finding emerged from sweeping the joint evolution across various periodic environmental shift frequencies (Table 1).

**Table 1: Final Trait Values vs. Environmental Shift Frequency**

| Environment | Shift Freq | Retention ($f$) | Learn Rate | Capacity |
| :--- | :--- | :--- | :--- | :--- |
| Hyper-Volatile | 2 gens | 0.9070 | 0.0132 | 1.3705 |
| Highly Volatile | 5 gens | 0.1961 | 0.0525 | 0.7007 |
| Chaotic | Fib/Pi | 0.8249 | 0.0205 | 0.6728 |
| Moderately Volatile| 20 gens | 0.7177 | 0.0131 | 0.7730 |
| Stable | 50 gens | 0.7458 | 0.0156 | 0.7360 |
| Hyper-Stable | 200 gens | 0.8010 | 0.0127 | 0.6754 |

The evolutionary response is distinctly non-monotonic. 
* **The "Boomerang" Strategy:** At extreme volatility (shifts every 2 generations), the population evolves larger capacities ($c \approx 1.37$), minimal learning, and near-perfect retention. It is metabolically cheaper to build a brain large enough to store *both* skills than it is to repeatedly relearn them.
* **Agile Amnesia:** At intermediate volatility (shifts every 5 generations), the boomerang strategy is too expensive to maintain. The population crashes into low retention and high learning rates, actively wiping memory to acquire the current skill.
* **Lamarckian Rentiers:** During long stable periods ($\ge 20$ generations), populations converge on high retention and low learning rates, paying the learning cost only once per shift and surviving off inherited knowledge for the duration of the stable era.
* **Chaotic Hedging:** Interestingly, chaotic environments push the population closer to the stable/rentier regime ($f \approx 0.82$), favoring robust retention to survive unpredictable shocks over the fragile agility of the 5-generation amnesia strategy.

---

## 4. Discussion
This study provides a unified framework for understanding the economics of memory inheritance. The original observation of a fixed $\approx 0.618$ attractor is now understood as a conditional state—one that requires slow learning, sufficient capacity, and intermediate volatility. 

When agents are subject to metabolic trade-offs, inheritance strategies bifurcate. High retention is heavily favored in environments that are either highly stable (allowing skill reuse across many generations) or hyper-volatile (where skills return to relevance faster than the decay rate of memory). Agile amnesia dominates the intermediate zone where skills shift just slowly enough to make dual-storage inefficient, but fast enough to mandate constant updating.

**Limitations:** 
It is crucial to emphasize that these results are derived from a highly stylized, abstract simulation. The model relies on several simplifying assumptions: agents have only two explicit skill slots (A and B); memory capacity is treated as a simple scalar boundary; learning occurs via a linear additive update rule without explicit interference between skills (other than capacity overflow); and fitness is calculated via a hand-crafted heuristic equation rather than emerging from spatial competition or complex ecology. Furthermore, the simulation lacks spatial structure, overlapping generations, and sexual recombination. The exact numerical values (such as the ~0.618 Golden Ratio attractor) should be viewed as illustrative artifacts of these specific mathematical choices, not universal biological constants. 

**Implications:** These findings have compelling analogies for both biology and artificial intelligence. In biology, it suggests that epigenetic inheritance mechanisms should be most prominent in environments matching the "rentier" or "boomerang" timescales. In AI, these results suggest that for continual learning systems operating under capacity constraints, the optimal rate of weight decay (analogous to $1 - f$) should be dynamically tuned to the spectral frequency of the incoming data distribution, rather than kept as a static hyperparameter.

---

## 5. Suggested Figures

1. **Figure 1:** Time series showing the divergence of mean $f$, $lr$, and $c$ under the chaotic shift schedule over 800 generations, demonstrating the active shrinking of brain capacity.
2. **Figure 2:** Heat-map of final retention ($f$) as a function of the metabolic penalty multiplier applied to learning rates.
3. **Figure 3:** The Phase Diagram (Bar Chart/Scatter): Final trait values plotted against the log-scale of environmental shift frequency, clearly illustrating the non-monotonic "U-shape" of retention and capacity.
4. **Figure 4:** Area plot showing the ratio of inherited vs. learned information within the active memory buffer over time in the agile amnesia regime.
