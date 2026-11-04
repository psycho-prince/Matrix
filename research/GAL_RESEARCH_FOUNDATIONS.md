# Shared theoretical foundations for Generational Artificial Life (GAL)

**Document status:** research framework / theory specification  
**Scope:** GAL 1.0 and GAL 2.0 as distinct research programmes  
**Implementation branch:** `research/gal-shared-theory`  
**Source programmes:** `research/gal-native-reproduction` and `research/gal-2.0-core`

## 1. Purpose and boundary

This document establishes a common mathematical language for comparing the two GAL programmes. It does **not** merge their implementations, assert that their mechanisms are equivalent, or claim that either programme has established a general theory of artificial life.

- **GAL 1.0** studies generational adaptation through population-level agents, environmental task performance, skill development, concept transmission, and alternative inheritance/teaching regimes.
- **GAL 2.0** studies explicit knowledge states, evidence provenance, memory classes, capability verification, and controlled transfer to successor agents. Its current task executor is a synthetic probabilistic harness, not an externally grounded learning system.

The shared framework is an analytical comparison layer. Each programme retains its own ontology, mechanisms, protocols, raw data, and claims. A result in one programme is not automatically evidence for the other.

## 2. A minimal generational-system formalism

Let a research system be indexed by generation (g\in\mathbb N_0). Define

\[
\mathcal G_g=(\mathcal A_g,\mathcal E_g,\mathcal T_g,\mathcal K_g,\mathcal I_g,\mathcal C_g),
\]

where:

- \(\mathcal A_g\): agents or learning entities present in generation (g);
- \(\mathcal E_g\): environmental state and its distribution;
- \(\mathcal T_g\): task distribution and evaluation protocol;
- \(\mathcal K_g\): the programme-specific knowledge state;
- \(\mathcal I_g\): inheritance or transmission operator;
- \(\mathcal C_g\): resource constraints and costs.

This is a comparison schema, not a claim that every implementation currently represents every component explicitly.

A successor state is generated abstractly by

\[
X_{g+1}=\Phi(X_g, O_{g+1}, U_{g+1};\eta),
\]

where (X_g) is the complete programme-specific state, (O_{g+1}) is new experience or observation, (U_{g+1}) is inherited input, and \(\eta\) collects fixed design choices. The decomposition of \(\Phi\) into learning, selection, inheritance, development, and environmental interaction must be specified separately for each experiment.

## 3. Knowledge is not a single interchangeable variable

The programmes currently encode knowledge differently. The comparison must preserve that difference.

### 3.1 GAL 1.0 representation

The inspected native agent implementation contains a skill vector

\[
s_{i,g}\in[0,1]^d
\]

and a concept set

\[
C_{i,g}\subseteq\mathcal V,
\]

where \(\mathcal V\) is the implementation's concept vocabulary. Task success depends on required skill, task difficulty, and whether the associated concept is present. Inheritance modes differ in whether skills are copied, taught, or left uninherited, and whether concepts are transmitted.

These are operational state variables in the current model. They should not be relabelled as calibrated beliefs or verified propositions without additional semantics and evidence.

### 3.2 GAL 2.0 representation

GAL 2.0 uses structured capability records and evidence objects. A capability includes proficiency, confidence indicator, evidence, prerequisites, context tags, failure conditions, verification state, version, and lineage. Memory is typed as episodic, semantic, or procedural, with source and custodian provenance.

These fields are richer bookkeeping than a scalar skill, but the current executor does not use stored memories, prerequisites, or procedures to solve tasks. Its success probability is a specified function of proficiency and task difficulty. Consequently, the present architecture does not yet demonstrate memory-grounded reasoning or open-ended knowledge acquisition.

### 3.3 Non-equivalence rule

No direct numerical comparison between GAL 1.0 skill/concept scores and GAL 2.0 proficiency/confidence/memory counts is valid unless a measurement model establishes what common construct is measured and validates the mapping. In particular:

- a concept-set size is not an information-theoretic knowledge quantity;
- a confidence field is not automatically a calibrated probability;
- a verified flag is not proof of truth outside its stated evaluation distribution;
- a task success rate is not a general intelligence measure.

## 4. Common outcome quantities

For a fixed evaluation distribution \(Q_g\), policy or agent \(f\), and bounded loss \(\ell\in[0,1]\), define risk

\[
R_{Q_g}(f)=\mathbb E_{z\sim Q_g}[\ell(f,z)].
\]

For higher-is-better scores, define expected utility \(V_{Q_g}(f)=-R_{Q_g}(f)\). Every reported performance quantity must name its task distribution, evaluation split, generation, unit of analysis, and aggregation rule.

For an inheritance intervention \(a\) and a matched no-transfer baseline \(0\), the generation-specific transfer effect is

\[
\Delta_g(a)=\mathbb E_s\left[V_g(a,s)-V_g(0,s)\right],
\]

where \(s\) indexes paired experimental seeds or matched initial conditions. The estimand is meaningful only if treatment arms share the same exogenous conditions and the pairing is implemented correctly.

Where costs are measured, define net utility

\[
J_g(a)=V_g(a)-\lambda C_g(a),
\]

with \(C_g\) a predeclared resource measure and \(\lambda\geq0\) a declared exchange rate. Do not choose \(\lambda\) after seeing outcomes. Report performance and cost separately as well as any composite.

For environmental change from source distribution \(P\) to successor distribution \(Q\), record the shift measure and its estimation uncertainty. On finite spaces, total variation is

\[
d_{TV}(P,Q)=\frac12\sum_x|P(x)-Q(x)|.
\]

A shift metric is not a substitute for evaluating on the actual successor distribution.

## 5. Shared research questions

The following questions can be investigated by both programmes while retaining separate operational definitions.

1. **Transfer benefit:** Under what conditions does inherited state improve successor performance over a matched no-transfer baseline?
2. **Transfer harm:** Under what conditions does inherited state reduce successor performance, increase false confidence, or impose excessive costs?
3. **Retention versus adaptation:** How does persistence of inherited state interact with environmental change?
4. **Evidence quality:** How does the reliability, independence, and provenance of inherited information affect successor outcomes?
5. **Capacity:** Under bounded representational or memory capacity, which information should be retained, compressed, revised, or discarded?
6. **Accumulation:** When does a sequence of generations produce a persistent increase in useful, independently validated information rather than merely increasing stored state?
7. **Robustness:** Do conclusions survive changes in task composition, evaluation distribution, population size, and implementation details?

## 6. Candidate hypotheses and falsification criteria

These are hypotheses to test, not conclusions.

- **H1 — Conditional transfer advantage:** There exist environments and evidence regimes for which inheritance yields positive successor utility relative to no transfer. Falsified for a specified domain if adequately powered, preregistered replications consistently bound the effect at or below a prespecified practically meaningful threshold.
- **H2 — Shift sensitivity:** Transfer effects depend on source-to-successor environmental change. Falsified within a specified domain if well-powered experiments show no practically meaningful interaction across a validated range of shifts.
- **H3 — Evidence-quality dependence:** More reliable and independent inherited evidence yields better calibrated successor decisions than equally sized low-quality or duplicated evidence. Falsified if the prespecified quality manipulation has no predicted effect under verified manipulation checks.
- **H4 — Capacity trade-off:** Under finite capacity, retaining all inherited state is not uniformly optimal across environments. Falsified if a preregistered set of environments shows a single retention policy dominates all alternatives under the stated utility and cost model.
- **H5 — Generational accumulation:** Useful information can increase across generations without unbounded growth in raw stored state. This requires an operational measure of useful information and a capacity constraint; growth in concept count, memory records, or skill scores alone does not establish it.

Null results, negative effects, and failed replications must be retained and reported.

## 7. Mathematical results: what is established and what remains open

GAL 2.0 currently contains a finite-hypothesis Bayesian update, a convex linear opinion-pool inheritance operator, a Bayes-factor verification threshold, and a total-variation risk bound. These are valid results under their stated mathematical assumptions. They are not yet a unified theorem about GAL 1.0 and GAL 2.0.

For bounded loss \(\ell\in[0,1]\), the total-variation inequality gives

\[
|R_P(f)-R_Q(f)|\leq d_{TV}(P,Q).
\]

If an inherited policy has source-domain advantage \(G=R_P(f_B)-R_P(f_I)\), then

\[
R_Q(f_B)-R_Q(f_I)\geq G-2d_{TV}(P,Q).
\]

This is a sufficient lower bound. It does not show that an inherited policy actually has positive source-domain advantage, nor that the bound is tight.

### Open theorem programme

The following are research targets, not proved claims:

1. **Evidence accumulation with dependence:** characterize when sequential and inherited evidence can be combined without double-counting correlated observations.
2. **Optimal inheritance under drift:** derive an optimal transfer weight from source posterior quality, successor prior, environmental drift, and transfer cost.
3. **Capacity-constrained retention:** characterize optimal retention or compression under finite memory and nonstationary task distributions.
4. **Multi-parent recombination:** derive aggregation operators with explicit dependence correction and conditions for calibration.
5. **Generational stability:** identify conditions under which errors contract, persist, or amplify through repeated transmission.
6. **Useful-information accumulation:** define and bound the increase in task-relevant information across generations under fixed resource constraints.

Every theorem must state its assumptions, quantify over its variables, provide a complete proof, and include boundary cases or counterexamples. A numerical illustration is not a proof.

## 8. Cross-programme measurement discipline

A cross-programme claim requires a bridge study. Before pooling or comparing results:

1. Define a common task family and a common held-out evaluation distribution.
2. Define a construct-level mapping from each programme's state to the measured outcome.
3. Verify that the mapping is invariant across generations and treatment arms.
4. Match exposure, compute, data, population size, and random streams where relevant.
5. Separate within-programme replication from cross-programme replication.
6. Report effect sizes, uncertainty intervals, raw data, exclusions, and all deviations.
7. Do not pool incompatible metrics or treat independent implementations as interchangeable replications.

The first cross-programme bridge should compare observable successor utility under carefully matched transfer/no-transfer conditions. It should not attempt to compare internal state counts as if they were the same quantity.

## 9. Research integrity and versioning

- GAL 1.0 and GAL 2.0 retain separate source branches and experiment protocols.
- Do not rewrite historical outputs, failed runs, or audit records.
- A green CI workflow establishes execution of the checked code, not the truth of a scientific hypothesis.
- Unit tests establish only the software invariants they exercise.
- Synthetic tasks and simulators must be labelled as such.
- Empirical claims require raw-data access, a frozen protocol, independent analysis, and reproducibility from a recorded commit.
- The shared framework may be revised, but every revision must preserve a dated change record and identify affected claims.

## 10. Source implementation anchors

The framework was grounded in source inspection of:

- GAL 1.0: `gal/agents/agent.py`, `gal/environment/world.py`, `gal/metrics/knowledge.py` on `research/gal-native-reproduction`.
- GAL 2.0: `gal2/models.py`, `gal2/agent.py`, `gal2/inheritance.py`, `gal2/ANALYTICAL_THEORY.md` on `research/gal-2.0-core`.

This document is a comparative research specification. It does not modify either programme's implementation or retroactively alter their results.
