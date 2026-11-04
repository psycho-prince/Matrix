# GAL Information Thermodynamics: Conservation, Data Processing, and Erasure

**Status:** formal theoretical framework; propositions are mathematical consequences of established information theory under stated assumptions. No claim is made that semantic knowledge is a conserved physical substance.
**Applies to:** GAL 1.0 and GAL 2.0 as a shared theoretical layer. Their implementations and empirical protocols remain separate.

## Abstract

This document develops a defensible connection between generational knowledge transmission and established results in information theory and the thermodynamics of computation. The central tools are (i) the data-processing inequality, (ii) the chain rule for mutual information, and (iii) Landauer's bound for logically irreversible erasure. Together they yield a precise statement: repeated processing or transmission cannot increase information about a fixed source through a Markov chain without access to additional information; new observations can add information; and physically resetting a memory has a thermodynamic cost under the assumptions of Landauer's principle.

This is **not** a theorem that semantic knowledge can never be destroyed. A local memory can be erased, corrupted, or made inaccessible. The rigorous claim is narrower: information about a specified source cannot increase through source-independent post-processing alone, and logically irreversible reset has a lower-bounded physical cost. Whether information remains recoverable in a larger physical environment is a separate question.

## 1. Physical and information-theoretic foundations

### 1.1 Data-processing inequality (DPI)

For random variables forming a Markov chain

\[
X\rightarrow M\rightarrow Y,
\]

the data-processing inequality states

\[
\boxed{I(X;Y)\leq I(X;M).}
\]

Here \(X\) is a source variable, \(M\) is an intermediate memory/state, \(Y\) is the result of processing or transmitting that state, and \(I\) is mutual information. The Markov condition means that conditioned on \(M\), the output \(Y\) contains no additional information about \(X\).

The inequality applies to any measurable stochastic processing channel under the usual conditions for mutual information. It does not require a thermodynamic model.

**Interpretation for GAL:** copying, encoding, compressing, filtering, teaching from, or transforming a parent state cannot increase information about a fixed source variable merely by processing that state. A transfer mechanism may preserve information, discard information, or make it less accessible. It cannot create source information from nothing.

### 1.2 Chain rule: new observations are a distinct information source

For random variables \(X,M,E\),

\[
\boxed{I(X;M,E)=I(X;M)+I(X;E\mid M).}
\]

The conditional mutual information term \(I(X;E\mid M)\) is the additional information about \(X\) carried by observation \(E\) beyond what is already in \(M\).

**Interpretation for GAL:** a successor can end up with more information about a target than its parent had only if it receives genuinely additional information (new observations, an external data source, or side information) or if the source variable being evaluated changes. Repeatedly copying a fixed parent record is not information acquisition.

Do not assume that information contributions from parent and child evidence add independently. The conditional term explicitly accounts for redundancy and dependence.

### 1.3 Landauer's principle

For an ideal memory in contact with a thermal reservoir at temperature \(T\), resetting a memory with Shannon entropy \(H(M)\) bits to a fixed standard state has the ideal lower bound

\[
\boxed{W_{\mathrm{erase}}\geq k_B T\ln 2\;H(M),}
\]

under the standard degenerate-memory, isothermal-reset assumptions. For a uniformly random single bit, \(H(M)=1\), giving \(k_BT\ln2\).

More general initial distributions, non-degenerate memory states, finite-time protocols, and side information require the corresponding generalised free-energy treatment; the simple expression must not be applied outside its assumptions.

Landauer's principle is a bound on the physical cost of logically irreversible erasure/reset. It does **not** say that information cannot be erased, that all forgetting costs exactly this amount, or that a semantic proposition is indestructible. Information may be dissipated locally while correlations with an environment or other degrees of freedom remain. Recoverability is not guaranteed.

## 2. A generational information model

Let \(X\) denote a fixed target/source variable whose information is to be tracked. Let \(M_g\) denote the memory/state available at generation \(g\). A pure inheritance-only lineage is modelled as

\[
X\rightarrow M_0\rightarrow M_1\rightarrow\cdots\rightarrow M_g,
\]

where each transition is a stochastic channel \(K_j(m_j\mid m_{j-1})\) and no generation receives new observations or side information about \(X\).

This is an explicit modelling assumption. Real GAL agents can interact with environments and obtain new observations, so the inheritance-only chain is a limiting case used to isolate transmission.

## 3. Theorem 1 — No amplification under inheritance-only processing

**Statement.** If \(X,M_0,\ldots,M_g\) form the Markov chain above, then for every generation \(g\geq 1\),

\[
\boxed{I(X;M_g)\leq I(X;M_{g-1})\leq\cdots\leq I(X;M_0).}
\]

**Proof.** For each transition, the Markov condition gives \(X\rightarrow M_{g-1}\rightarrow M_g\). Applying the data-processing inequality yields \(I(X;M_g)\leq I(X;M_{g-1})\). Repeating this argument for each earlier transition proves the chain of inequalities. \(\square\)

**Equality condition.** Equality at a transition holds precisely when the processing output is a sufficient statistic of the input for \(X\), equivalently when \(I(X;M_{g-1}\mid M_g)=0\) under the Markov structure. Lossless copying is one special case; it is not the only possible sufficient transformation.

**Meaning.** In an inheritance-only lineage, information about the fixed source cannot be amplified by copying or processing alone. It can be preserved or degraded.

This theorem concerns mutual information about a specified random variable. It does not establish monotonicity of task performance, semantic correctness, usefulness, or an agent's total knowledge about a changing world.

## 4. Theorem 2 — Additional observations are the only new information term in the model

Let a successor state be generated from inherited memory \(M_g\) and a new observation \(E_{g+1}\), so that \(M_{g+1}=\phi(M_g,E_{g+1},N)\), where \(N\) is processing noise. Then

\[
I(X;M_g,E_{g+1})=I(X;M_g)+I(X;E_{g+1}\mid M_g).
\]

If \(M_{g+1}\) is a function or stochastic post-processing of \((M_g,E_{g+1})\), DPI gives

\[
\boxed{I(X;M_{g+1})\leq I(X;M_g)+I(X;E_{g+1}\mid M_g).}
\]

**Proof.** Apply the mutual-information chain rule to \((M_g,E_{g+1})\), then apply DPI to the processing channel from \((M_g,E_{g+1})\) to \(M_{g+1}\). \(\square\)

The new-information term is conditional. It can be zero if the observation is redundant, and positive if it contains additional information about \(X\). It is not necessarily equal to the raw information content \(H(E_{g+1})\).

## 5. Corollary — An exact accounting identity, not a conservation law

For a fixed target \(X\), define the information gap after generation \(g\) as

\[
D_g=I(X;M_0)-I(X;M_g).
\]

Under inheritance-only processing, Theorem 1 implies \(D_g\geq0\). The quantity \(D_g\) is the information about \(X\) no longer present in the current memory, relative to the initial memory.

This is not necessarily destroyed information in the universe. It may remain in a parent, an archive, a communication channel, or environmental degrees of freedom. Conversely, if all correlated records are erased or become physically inaccessible, recovery may be impossible in practice.

The expression

\[
I_{\mathrm{retained}}+I_{\mathrm{discarded}}=I_{\mathrm{initial}}
\]

is **not** generally valid as a universal decomposition: mutual information is not an additive conserved substance, and overlapping or synergistic information makes naive bookkeeping invalid. The rigorous accounting quantities are the chain rule and conditional mutual information.

## 6. Theorem 3 — Thermodynamic lower bound for reset

**Statement.** For a memory register with initial Shannon entropy \(H(M)\) bits, reset to a fixed standard state in an isothermal process at temperature \(T\), with degenerate logical states and an ideal thermal reservoir, the average work cost obeys

\[
W_{\mathrm{erase}}\geq k_BT\ln2\,H(M).
\]

For one equiprobable bit this reduces to \(W_{\mathrm{erase}}\geq k_BT\ln2\).

**Scope.** This is Landauer's principle, not a GAL-specific theorem. Its assumptions must be checked before numerical use. A memory that is merely overwritten, abandoned, or allowed to decohere is not automatically the same physical protocol as controlled reset to a standard state.

**Implication for GAL:** a physical implementation that repeatedly resets finite memory has a nonzero ideal thermodynamic lower bound determined by the entropy of the reset register. The actual energy cost will generally depend on architecture and operating conditions and may greatly exceed the bound. This does not imply that every software deletion in an abstract simulator incurs a measurable Landauer cost in the simulator's accounting.

## 7. What can and cannot be claimed

| Claim | Status |
|---|---|
| Processing in a Markov chain cannot increase mutual information about its fixed source | Theorem from DPI |
| New observations can contribute additional conditional information | Chain rule; contribution may be zero |
| Resetting a physical memory has a thermodynamic lower bound under Landauer assumptions | Established physical principle |
| Semantic knowledge is a conserved physical substance | Not established; do not claim |
| Knowledge can never be destroyed | False as a general claim |
| A successor must be at least as capable as its parent | Not implied |
| More retained bits means more useful knowledge | Not implied |
| GAL 1.0 or GAL 2.0 currently implements these theorems | Not established by the current code audit |

## 8. Research propositions for GAL

These are research questions, not established theorems.

### P1 — Reliability-aware transmission

Define a source variable \(X\) representing a task-relevant fact, and a memory channel with measurable error. Characterise which transmission channels preserve sufficient statistics for predicting \(X\), and which channels degrade them.

### P2 — Evidence renewal under environmental drift

Let the target itself depend on generation, \(X_g\). Derive conditions under which fresh observations compensate for loss of information about an older target, and distinguish genuine adaptation from simply tracking a changed target.

### P3 — Cost-aware memory policy

Combine expected decision loss with storage, communication, verification, and physical reset costs. Derive an optimal policy only after specifying the utility function, resource constraints, and physical implementation. Landauer's lower bound is one term, not the whole cost model.

### P4 — Redundant lineage archives

Study when preserving multiple correlated ancestral records improves recoverability, and quantify the marginal information gain using conditional mutual information rather than counting copies or bytes.

## 9. Operational bridge to the two GAL programmes

### GAL 1.0

Potential mapping:
- source \(X\): task-relevant environmental state or latent task rule;
- memory \(M_g\): skill vector and concept set;
- channel: the selected inheritance mode (A, B-copy, C-full, C-no-memory, C-low-effort);
- new observation \(E_g\): task feedback and independently acquired experience.

The current fixed symbolic task environment is not a physical memory device and has no temperature, energy register, or controlled erasure protocol. Landauer's energy bound therefore cannot be numerically applied to its in-memory Python data structures. The DPI framework can be applied only after a probabilistic source variable and channel distributions are explicitly defined.

### GAL 2.0

Potential mapping:
- source \(X\): a proposition, task rule, or latent capability-relevant state;
- memory \(M_g\): evidence and memory records, including provenance;
- channel: verified capability and memory inheritance, or adaptive recalibration;
- new observation \(E_g\): successor task evidence.

The current task executor is synthetic and does not consume memory records when solving tasks. Before estimating mutual information, GAL 2.0 needs an explicit data-generating model for ground truth, observations, memory encoding, and task decisions. Its current confidence heuristic is not an information measure.

## 10. Required next mathematical work

1. Specify finite source and memory alphabets for a minimal theorem model.
2. Derive exact transition matrices for each native GAL 1.0 inheritance mode under a declared simplified task model.
3. Derive the GAL 2.0 evidence-transfer channel, including source lineage and correlated evidence.
4. Calculate mutual information and conditional mutual information exactly for those channels.
5. Construct counterexamples: perfect copying with zero new information; lossy copying; misleading inherited evidence; fresh evidence restoring information; and redundant multi-parent transfer.
6. Only then decide whether a common quantitative result applies to both systems.

No simulation is needed to establish Theorems 1–3. If later numerical examples are used, they must be labelled as analytic calculations or experiments and must not replace the proofs.

## 11. References

1. R. Landauer, “Irreversibility and Heat Generation in the Computing Process,” *IBM Journal of Research and Development* 5, 183–191 (1961), DOI: [10.1147/rd.53.0183](https://doi.org/10.1147/rd.53.0183).
2. C. H. Bennett, “The Thermodynamics of Computation—A Review,” *International Journal of Theoretical Physics* 21, 905–940 (1982), DOI: [10.1007/BF02084158](https://doi.org/10.1007/BF02084158).
3. J. M. R. Parrondo, J. M. Horowitz, and T. Sagawa, “Thermodynamics of information,” *Nature Physics* 11, 131–139 (2015), DOI: [10.1038/nphys3230](https://doi.org/10.1038/nphys3230).
4. T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley (2006), chapters 2 and 7 (entropy, mutual information, data processing).
5. I. Georgescu, “60 years of Landauer’s principle,” *Nature Reviews Physics* 3, 770 (2021), DOI: [10.1038/s42254-021-00400-8](https://doi.org/10.1038/s42254-021-00400-8).

## 12. Research integrity statement

This framework imports established theorems; it does not claim to have discovered the data-processing inequality or Landauer's principle. Any novel GAL contribution must be a new, correctly proved result about a specified generational channel, a new bound under explicit assumptions, or a validated operational consequence. The physical law is not being extended by analogy alone.
