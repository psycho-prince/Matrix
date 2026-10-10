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
