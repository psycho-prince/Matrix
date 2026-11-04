# GAL Research Programme: Shared Theoretical Framework

**Status:** research architecture and formal problem statement  
**Scope:** GAL 1.0 and GAL 2.0 remain independent research programmes. This document defines a common mathematical vocabulary and comparison interface; it does not merge their implementations or claim that either programme has established the general theory.

## 1. Research programme structure

GAL 1.0 and GAL 2.0 investigate related but non-identical questions.

- **GAL 1.0:** generational adaptation, inheritance mechanisms, memory economics, capacity constraints, environmental volatility, and artificial-life dynamics.
- **GAL 2.0:** explicit knowledge states, evidence provenance, verification, memory organisation, and reliable transfer between agents or generations.

The shared question is:

> Under what assumptions, and by what mechanisms, can information acquired by one generation improve the expected performance or epistemic state of later generations without making them systematically less adapted to their environments?

This question is deliberately conditional. It does not presume inheritance is beneficial.

## 2. Common mathematical objects

Let generations be indexed by (g\in\mathbb{N}_0), and let agent (i) in generation (g) have:

- an internal state (Z_{g,i}\in\mathcal Z);
- an environment (E_g\in\mathcal E);
- an observation history (H_{g,i}\in\mathcal H);
- an action or decision rule (f_{g,i}\in\mathcal F);
- a measurable loss (L(f_{g,i},E_g)\in[0,1]), where lower is better.

A general generational transition is a stochastic kernel

\[
K_g(dz'\mid z,h,e,\eta),
\]

where (z) is the source state, (h) is the evidence/history available for transmission, (e) is the receiving environment, and \(\eta\) represents an explicitly specified transmission mechanism (copying, teaching, filtering, recombination, compression, or no transfer).

This kernel is a common abstraction, not a claim that the two implementations currently instantiate the same process.

## 3. Separate the quantities that must not be conflated

The following are distinct and must be measured separately:

1. **Information retained:** what state or evidence is transmitted.
2. **Information reliability:** whether transmitted claims remain supported by valid evidence.
3. **Information utility:** whether transmission reduces expected loss in the receiving environment.
4. **Adaptation:** whether the recipient performs better under its actual environment and resource constraints.
5. **Population-level effects:** whether the distribution of agent states changes across generations.
6. **Cost:** resources consumed to acquire, preserve, transmit, verify, and use information.

A larger memory, higher confidence score, or greater parent-child similarity is not by itself evidence of greater knowledge or adaptation.

## 4. Core estimand: causal value of inheritance

For a specified receiving environment distribution (Q_g), define the expected loss of a recipient under inheritance mechanism \(\eta\) as

\[
R_g(\eta)=\mathbb E_{E\sim Q_g,\,\omega}[L(f_{g+1}^{(\eta)},E)],
\]

where \(\omega\) includes the declared randomness in learning, sampling, and transmission.

Against a predeclared baseline \(\eta_0\), define the inheritance value

\[
\Delta_g(\eta;\eta_0)=R_g(\eta_0)-R_g(\eta).
\]

Positive \(\Delta_g\) means lower expected loss under the specified conditions. The estimand is only meaningful when both arms have comparable initial conditions, task exposure, resource budgets, evaluation data, and randomisation or pairing.

For a cost-aware comparison, define

\[
\Delta_g^{(c)}=\Delta_g-\lambda(C_g(\eta)-C_g(\eta_0)),
\]

where cost \(C_g\) is measured in declared physical or computational units and \(\lambda\) is a pre-specified exchange rate. Results must also report the unadjusted performance and cost separately; the scalarised quantity must not conceal trade-offs.

## 5. Three hypotheses to investigate, not assume

### H1 — Conditional inheritance benefit

There exist nontrivial conditions under which an inheritance mechanism yields \(\Delta_g>0\) relative to no inheritance, under matched exposure and resources.

A valid result must identify those conditions and report regions where the effect is zero or negative.

### H2 — Reliability- and shift-dependent transfer

The value of inherited information depends jointly on its evidential reliability and the difference between source and receiving environments.

A useful theory must define reliability and environmental shift operationally, derive a bound or decision rule, and state when the bound is tight or vacuous.

### H3 — Resource-constrained memory allocation

Under finite acquisition, storage, transmission, and verification budgets, selective retention can outperform indiscriminate retention in some environments.

This is not a presumption that forgetting is beneficial. The claim requires an explicit cost model and a comparison against matched-capacity alternatives.

## 6. Theoretical obligations

Any theorem used to support a GAL claim must include:

- a precise statement of all spaces, random variables, distributions, and assumptions;
- a complete proof or a clearly labelled proof sketch;
- a counterexample search for weakened assumptions;
- boundary cases, including zero information, perfect information, no shift, maximal shift, and dependent evidence;
- a statement of what the theorem does **not** establish;
- a mapping from each mathematical object to an implemented or measurable quantity, or an explicit statement that it is not yet operationalised.

The Bayesian model in gal2/ANALYTICAL_THEORY.md is one candidate formalisation for epistemic state and evidence. It is not automatically the mathematical model of GAL 1.0's native agent dynamics. A bridge must be derived, not asserted.

## 7. Evidence hierarchy

Claims must be labelled according to their actual support:

- **Formal result:** follows from stated assumptions and a valid proof.
- **Software invariant:** established by tests for specified code paths.
- **Mechanism validation:** confirms that an implementation executes its intended mechanism.
- **Pilot observation:** exploratory result used to validate mechanics or estimate variability.
- **Confirmatory result:** result from a pre-specified design with adequate analysis and preserved raw data.
- **Independent replication:** reproduced by an independent implementation or team.

A passing CI workflow is not a scientific finding. A theorem about an abstract model is not evidence that a particular implementation satisfies that model. A synthetic benchmark is not evidence of real-world agent capability.

## 8. Cross-programme comparison contract

When comparing GAL 1.0 and GAL 2.0, use a common reporting schema:

| Dimension | Required report |
|---|---|
| Unit of analysis | Agent, lineage, generation, or population |
| Environment | Stationary/non-stationary specification and sampling process |
| Information | Exact state/evidence available to each agent |
| Transfer | Mechanism, timing, filtering, and provenance |
| Verification | Rule, calibration, and false-accept/false-reject rates |
| Resources | Acquisition, storage, compute, transmission, evaluation |
| Outcome | Predeclared loss and secondary measures |
| Baselines | No transfer, naive transfer, and relevant domain baselines |
| Uncertainty | Seed/cluster structure, intervals, effect sizes, multiplicity |
| Reproducibility | Commit, protocol, raw artifact, hash, audit, environment |

Do not compare raw scores across different task spaces as if they shared a scale. Cross-programme comparisons require a common task or a justified normalisation.

## 9. Immediate research sequence

1. **Model audit:** map each GAL 1.0 and GAL 2.0 implementation variable to the common objects above; mark unmapped quantities.
2. **Assumption audit:** identify where evidence independence, stationarity, bounded loss, finite hypothesis spaces, or known likelihoods are assumed.
3. **Bridge theorem:** derive a result connecting an explicit inheritance mechanism to a measurable change in expected recipient loss. Do not reuse a theorem whose assumptions are not met.
4. **Counterexamples:** construct analytical cases where inheritance harms recipients, including stale knowledge, correlated evidence, false verification, and resource displacement.
5. **Operationalisation:** only after the model and counterexamples are stable, specify experiments that can distinguish the hypotheses.
6. **Independent review:** seek external review of definitions, proofs, protocols, and analysis before making broad claims.

## 10. Non-goals and integrity constraints

- This document does not merge GAL 1.0 and GAL 2.0.
- It does not change either implementation or any historical result.
- It does not assert that generational inheritance is universally beneficial.
- It does not establish biological equivalence, consciousness, general intelligence, or open-ended learning.
- It does not authorise replacing analytical work with toy simulations.
- Any future empirical study must be separately protocolled and must preserve failures and raw outputs.

## 11. Programme-level research question

The central question for both programmes is not whether a successor can copy a predecessor. It is:

> When does transmitting acquired structure produce a net, reliable, and reproducible improvement in the successor's ability to act under its own environment, after accounting for uncertainty, environmental change, and the full cost of transmission?

That question is the shared research target. The two programmes may answer different parts of it, and either may produce evidence against a general inheritance advantage.
