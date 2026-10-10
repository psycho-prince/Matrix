# Matrix: Capacity-Shift Literature Review

## Abstract / Goal
To contextualize the Matrix "capacity-shift" hypothesis within existing academic research. The core hypothesis is: *Exact inheritance (cloning) excels in stable environments with unlimited capacity, but catastrophically fails in volatile environments with strict capacity constraints, where lossy or selective transmission (teaching) acts as a necessary regularizer.*

## 1. Continual Learning & Catastrophic Forgetting
*Core Question:* How does the machine learning literature handle agents that must learn new tasks without forgetting old ones, especially when neural capacity is fixed?
* **Relevant Concepts:** Elastic Weight Consolidation (EWC), replay buffers, catastrophic forgetting.
* **Matrix Connection:** Matrix's capacity limit enforces a form of forgetting. Does exact copying force the agent to retain obsolete weights, leading to catastrophic interference when the environment shifts?

## 2. Cultural Evolution & Cumulative Inheritance
*Core Question:* How do anthropologists and evolutionary biologists model the transmission of skills across generations?
* **Relevant Concepts:** Dual inheritance theory, the "ratchet effect," the role of transmission errors in innovation.
* **Matrix Connection:** In human cultural evolution, teaching is inherently lossy, yet this lossiness prevents overfitting to a single generation's idiosyncratic environment. Matrix's C-full model mathematically approximates this "lossy teaching" mechanism.

## 3. Evolutionary Computation & Lamarckian Transfer
*Core Question:* How have previous computational simulations modeled the transfer of acquired lifetime traits (weights) versus innate traits (architecture)?
* **Relevant Concepts:** Baldwin effect, Lamarckian evolution in Artificial Neural Networks (ANNs), Neuroevolution of Augmenting Topologies (NEAT).
* **Matrix Connection:** Matrix implements a direct Lamarckian transfer. We need to review studies that bounded the amount of Lamarckian transfer permitted and how it affected adaptation in dynamic fitness landscapes.

## 4. Gap Analysis
*Where does Matrix contribute new knowledge?*
* Most evolutionary computation models assume stable fitness landscapes or infinite capacity.
* Matrix aims to provide a minimalist, computationally tractable demonstration of a phase transition: the exact point where the environment's volatility outpaces the agent's memory capacity, turning exact inheritance from an advantage into a fatal flaw.

## References to Investigate
* (To be populated with specific papers and citations)

## Autonomous Research Findings (October 2026)

### 1. Continual Learning & The Stability-Plasticity Dilemma
* **The Core Conflict:** The tension between plasticity (learning new tasks) and stability (retaining old tasks).
* **Capacity Saturation:** Catastrophic forgetting is not purely a symptom of small model size; even massive models suffer from "capacity saturation" in sequential tasks as the optimization process overwrites previous task representations to minimize current errors.
* **Matrix Application:** Matrix tests this explicitly. When an agent's memory capacity is constrained, retaining obsolete weights (via exact copying) leads to capacity saturation, preventing the learning of new tasks when the environment shifts. 

### 2. Cultural Evolution: Transmission Error & Regularization
* **Cumulative Cultural Evolution (CCE):** Requires high-fidelity transmission, but *transmission error* is a constant factor that introduces variation.
* **Regularization as a Stabilizer:** Cognitive or social regularization processes filter out noise. However, the literature emphasizes a critical balance: if regularization is too weak, complex traits degrade; if it is too strong (like Matrix's exact copying), it stifles innovation.
* **Matrix Application:** Matrix's "teaching" mechanism (C-full) acts as a mathematical proxy for lossy cultural transmission. By enforcing a bounded number of error-correction steps, it effectively introduces a form of regularization that prevents overfitting to the immediate generation's environment.

### 3. Evolutionary Computation: Lamarckian Inheritance in Dynamic Environments
* **Performance in Nonstationary Environments:** Evolutionary Robotics (ER) research consistently shows Lamarckian systems (which pass acquired weights to offspring, akin to Matrix's B-copy) adapt much more rapidly to shifting environments than Darwinian systems.
* **The Overfitting Tradeoff:** The primary risk of Lamarckian transfer in these simulations is *premature convergence* to local optima. 
* **Matrix Application:** Matrix's findings complicate the standard Lamarckian narrative. Our initial experiments show that when *capacity is limited*, the rapid adaptation of Lamarckian transfer (exact copying) becomes a liability during an environmental shift, as obsolete traits cannot be unlearned fast enough.
