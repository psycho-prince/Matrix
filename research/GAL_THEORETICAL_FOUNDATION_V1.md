# GAL Theoretical Foundation v1.0
**Status:** Consolidated research specification; not a claim of a unified validated theory  
**Prepared:** 25 November 2026  
**Baseline:** `research/gal-2.1-memory-grounded-learning`  
**Purpose:** Reconcile the existing GAL 1.0, GAL 2.0, information-theory, inheritance-channel, and cross-programme documents without conflating their mechanisms or evidence.

---

## 1. Executive statement

Generational Artificial Life (GAL) is currently a **research programme about generational transfer, learning, memory, and adaptation**, implemented through two related but non-equivalent computational programmes.

The repository supports several narrow results about specified transfer operators in synthetic environments. It does not yet establish a general theory of artificial life, a universal law of memory economics, open-ended evolution, biological inheritance, general intelligence, or consciousness.

The most defensible shared scientific question is:

> **Under what conditions does transferring information from one generation to the next improve a successor's decisions, once evidence reliability, dependence between inherited observations, environmental change, finite memory, and verification cost are taken into account?**

This question is broad enough to connect the existing work, but it is not itself novel. Cultural evolution, iterated learning, Bayesian transmission, optimal forgetting, continual learning, and information theory already study important parts of it. Any GAL contribution must be a more precise mechanism, theorem, measurement, or experimentally validated prediction.

This document consolidates existing foundations. It does not merge the GAL 1.0 and GAL 2.0 implementations, alter historical results, or introduce a new empirical claim.

## 2. Scope and programme separation

### 2.1 GAL 1.0: generational agents and transfer operators

GAL 1.0 represents agents with operational skill values and concept identifiers. Agents interact with task environments, and different inheritance conditions transmit different parts of the parent's state.

The current native implementation and foundational experiments are a useful testbed for:
- no inheritance versus inheritance;
- exact copying versus specified stochastic teaching/correction operators;
- concept transmission and skill-state transfer;
- population and generation-level outcomes.

The present foundational task world is a finite, handcrafted symbolic environment. Its skill and concept variables are simulation state, not validated measures of semantic knowledge or biological cognition.

### 2.2 GAL 2.0: evidence, provenance, and successor verification

GAL 2.0 represents capabilities, evidence, memory types, provenance, verification state, and lineage. It is a richer epistemic data model.

Its current synthetic executor uses capability proficiency and task difficulty to generate success probabilities. It does not yet retrieve episodic, semantic, or procedural memory to select actions or solve tasks. Therefore the existence and transfer of memory records must not be described as demonstrated memory-grounded learning.

### 2.3 Non-equivalence rule

GAL 1.0 and GAL 2.0 must remain separate empirical programmes until a bridge study establishes measurement equivalence.

The following quantities are not interchangeable without a validated measurement model:
- GAL 1.0 concept count and Shannon information;
- skill values and calibrated beliefs;
- GAL 2.0 confidence heuristics and posterior probabilities;
- verified flags and real-world truth;
- memory-record count and useful retained knowledge;
- task success and general intelligence.

A shared vocabulary is useful for theory comparison; it does not make the implementations mathematically or empirically equivalent.

## 3. Common generational-system description

For generation (g), use the comparison tuple

$
\mathcal{G}_g=(\mathcal{A}_g,\mathcal{E}_g,\mathcal{T}_g,\mathcal{K}_g,\mathcal{I}_g,\mathcal{C}_g),
$

where:
- (\mathcal{A}_g): agents or learning entities;
- (\mathcal{E}_g): environmental state and its distribution;
- (\mathcal{T}_g): task distribution and evaluation protocol;
- (\mathcal{K}_g): programme-specific internal state;
- (\mathcal{I}_g): inheritance or transmission mechanism;
- (\mathcal{C}_g): resource limits and costs.

An abstract successor transition can be written as

$
X_{g+1}=\Phi(X_g,O_{g+1},U_{g+1};\eta),
$

where (X_g) is the programme-specific state, (O_{g+1}) is new observation or experience, (U_{g+1}) is inherited input, and (\eta) collects fixed design choices.

This is a bookkeeping formalism, not a claim that every current implementation explicitly models every term. Each experiment must specify the actual transition function and the causal path from inherited state to successor decisions.

## 4. Shared outcome and transfer estimands

For a fixed evaluation distribution (Q_g), decision rule (f), and bounded loss (\ell\in[0,1]), define

$
R_{Q_g}(f)=\mathbb{E}_{z\sim Q_g}[\ell(f,z)].
$

For a higher-is-better score, define utility (V_{Q_g}(f)=-R_{Q_g}(f)).

For a transfer intervention (a) and a matched no-transfer condition (0), define the paired effect

$
\Delta_g(a)=\mathbb{E}_s[V_g(a,s)-V_g(0,s)],
$

where (s) indexes independent paired runs or matched initial conditions. The experimental unit must be declared; agents sharing a population and environment are not automatically independent replicates.

If resource costs are measured, report them separately. A composite objective may be defined as

$
J_g(a)=V_g(a)-\lambda C_g(a),
$

but (C_g) must be operationally measured and (\lambda) specified before outcomes are inspected. Do not call a chosen numerical fitness penalty a measured metabolic or physical energy cost.

For a source distribution (P) and successor distribution (Q), on a finite state space,

$
d_{TV}(P,Q)=\frac12\sum_x|P(x)-Q(x)|.
$

Always report actual successor-distribution performance as well as any theoretical shift bound.

## 5. Evidence and inheritance: the central conceptual distinction

The consolidated research question requires separating at least five properties:

1. **Transmission:** Was a state or record copied to the successor?
2. **Correctness:** Does the inherited claim correspond to the environment's ground truth?
3. **Evidence quality:** How reliable are the observations supporting it?
4. **Evidence dependence:** Are multiple records genuinely independent, or do they descend from the same source observation?
5. **Successor relevance:** Does the inherited information remain useful under the successor's environment and task distribution?

These properties must not be collapsed into a single confidence or verification flag.

A record with multiple descendants is not necessarily supported by multiple independent observations. Repeatedly copying one source claim does not create new evidence. Likewise, an inherited claim can be correct in the source environment and become stale after a distribution shift.

GAL 2.0's provenance and lineage fields provide useful implementation scaffolding for this question. They do not yet establish statistical dependence correction or calibrated reliability.

## 6. Existing mathematical foundations and their limits

### 6.1 Bayesian evidence updating

For a finite hypothesis space (\Theta), prior distribution (\pi), and observation (y) with a specified likelihood (L(y\mid\theta)), Bayesian updating is

$
\pi'(	heta)=
\frac{L(y\mid\theta)\pi(\theta)}
{\sum_{\vartheta\in\Theta}L(y\mid\vartheta)\pi(\vartheta)}.
$

This is an established mathematical rule under the assumed prior and likelihood. It does not show that an agent can correctly specify its hypothesis space or likelihood model. Multiplication of likelihoods is justified for conditionally independent observations; duplicated or correlated evidence requires a joint likelihood or dependence model.

### 6.2 GAL 2.0 linear opinion-pool inheritance

The existing analytical document proposes

$
\pi_c=(1-r)\pi_0+r\pi_p,\qquad r\in[0,1],
$

where (\pi_0) is a successor base prior and (\pi_p) is a parent distribution. This is a normalized convex mixture. It is a modelling choice, not Bayesian updating in general and not a biological inheritance law. The current GAL 2.0 implementation does not implement this analytical Bayesian model.

### 6.3 Verification threshold

For claim (H), prior probability (p), and Bayes factor (B), posterior odds are

$
\frac{P(H\mid y)}{P(\neg H\mid y)}
=B\frac{p}{1-p}.
$

To require posterior probability at least (\tau\), the evidence must satisfy

$
B\geq\frac{\tau}{1-\tau}\frac{1-p}{p}.
$

This is an algebraic consequence of Bayes' rule. It only has an empirical interpretation if the likelihood ratio is valid and the evidence dependence is handled correctly.

### 6.4 Distribution-shift bound

For bounded loss and a fixed decision rule,

$
|R_P(f)-R_Q(f)|\leq d_{TV}(P,Q).
$

If an inherited rule (f_I) has source-domain risk advantage (G\geq0) over baseline (f_B),

$
R_P(f_B)-R_P(f_I)=G,
$

then

$
R_Q(f_B)-R_Q(f_I)\geq G-2d_{TV}(P,Q).
$

This is a sufficient bound. It does not establish that (G>0), that the bound is tight, or that inheritance remains useful after every shift.

### 6.5 Information theory and thermodynamics

The data-processing inequality and Landauer's principle are established results imported by the existing GAL information-theory notes. They are useful constraints on information processing and physical computation.

They do not by themselves imply that:
- a concept set is a measured number of bits;
- copying memory is physically free or costly in a particular implementation;
- a simulation's fitness penalty is metabolic energy;
- information loss is automatically adaptive;
- a new thermodynamic law has been discovered.

A GAL-specific contribution would require an explicitly defined stochastic channel, state distribution, resource model, and a correctly derived result beyond merely restating an established theorem.

### 6.6 Exact inheritance channels

The existing exact-channel notes derive or propose properties for specified copying, erasure, and teaching operators. Those derivations should remain mechanism-specific. A channel identity for a binary erasure toy model is not a measured information rate for native continuous skill transfer or GAL 2.0's evidence-dependent verification.

## 7. Shared candidate hypotheses

These hypotheses consolidate the existing H1–H5 programme. They remain candidates and must be operationalised separately in each implementation.

- **H1 — Conditional transfer benefit:** There are specified environments and evidence regimes in which transfer improves successor utility relative to a matched no-transfer condition.
- **H2 — Shift sensitivity:** The transfer effect changes as a function of a measured source-to-successor environmental shift.
- **H3 — Evidence-quality dependence:** Reliable, genuinely independent inherited evidence improves successor decisions more than equally sized unreliable or duplicated evidence.
- **H4 — Capacity trade-off:** Under finite memory or representation capacity, full retention is not uniformly optimal across all successor environments.
- **H5 — Generational accumulation:** Task-relevant, independently supported information can accumulate across generations without unbounded growth in raw stored state.

Each hypothesis needs:
- an operational definition;
- a primary outcome and smallest effect of practical interest;
- a held-out evaluation distribution;
- a preregistered manipulation and control;
- falsification criteria;
- an explicit mapping to implementation variables.

A null or negative result must be retained. An increase in stored records, concepts, or proficiency alone does not establish useful knowledge accumulation.

## 8. Candidate unifying research model

The most promising next model is **lineage-aware evidence transmission under environmental drift**.

Each successor receives a finite budget for:
- storing inherited claims;
- acquiring new observations;
- checking claims against evidence;
- resolving conflicts;
- adapting to changed environmental conditions.

Each claim should carry, where applicable:
- content or hypothesis identity;
- source observation identifiers;
- source agent and generation;
- evidence quality or a calibrated reliability estimate;
- dependence/ancestry information;
- time or environmental context;
- verification procedure and outcome;
- storage and verification cost.

The successor must choose whether to retain, discount, re-test, revise, or discard the claim. The action should affect its downstream decisions; otherwise the memory model is not causally connected to performance.

**Candidate hypothesis (not a novelty claim):**

> Under finite memory and verification budgets, a successor policy that accounts for evidence reliability, shared ancestry, and source-to-successor environmental mismatch can reduce held-out decision loss relative to no transfer, full copying, and fixed-rate forgetting.

The model should explicitly include counterexamples:
- highly reliable information that remains useful, where full retention should win;
- stale information after a large environmental shift, where transfer should harm;
- duplicated evidence that falsely inflates confidence;
- noisy evidence that should be rejected;
- verification that costs more than the expected benefit;
- small or absent shifts where selective verification is wasteful.

If the proposed policy cannot outperform simple baselines in a regime where its assumptions should help, the model must be revised or rejected.

## 9. Required experiment sequence

### Stage A — analytical specification (no new simulation yet)

1. Define the latent environment and transition process.
2. Define the observation model and ground truth.
3. Define source identity and dependence between observations.
4. Define the memory and verification budgets.
5. Define the successor decision and bounded loss.
6. Derive the policy or decision rule under explicit assumptions.
7. Identify counterexamples and limiting cases.
8. State predictions that distinguish it from existing models.

### Stage B — benchmark design

At minimum, compare:
1. no inheritance;
2. full inheritance;
3. fixed fractional retention;
4. selective retention without lineage/dependence correction;
5. selective retention with dependence-aware evidence handling;
6. successor verification under a limited budget;
7. independent learning with matched observations and compute;
8. oracle upper bound, reported only as an upper bound.

Primary outcome: held-out successor decision loss after a controlled environmental shift.

Secondary outcomes: false-accept rate, claim accuracy, calibration (only for calibrated probabilities), recovery time, retained useful information, memory use, compute, transfer, and verification costs.

Use multiple environment families, paired independent seeds, a preregistered primary endpoint, immutable per-run records, and an independent analysis script. Training and evaluation data must be separated. Do not use an oracle's hidden truth labels as if the agent independently discovered them.

### Stage C — within-programme tests and bridge study

First audit and test GAL 1.0 and GAL 2.0 independently. Only then design a bridge study with a common task family and validated measurement mapping. If a faithful common task cannot be built, report a conceptual comparison, not a direct empirical comparison.

## 10. Implementation-to-theory map

| Theoretical component | GAL 1.0 | GAL 2.0 | Current status |
|---|---|---|---|
| Agent state | Skills and concepts | Capabilities, evidence, memory stores | Explicit but non-equivalent |
| Environment | Fixed symbolic task world in foundational runner | Synthetic task records | Explicit, limited |
| Inheritance | Copying and stochastic teaching variants | Evidence-gated capability/memory transfer | Implemented mechanisms |
| Evidence provenance | Partial runner-level lineage | Source and custodian metadata | Richer in 2.0 |
| Evidence dependence | Not represented at claim level | Lineage fields exist; statistical correction absent | Open |
| Environmental drift | Separate capacity/volatility experiments | Context labels; executor shift is not causally grounded | Incomplete |
| Memory affects action | Skills/concepts affect task success | Stored episodic/semantic/procedural memories do not drive solver | Different causal pathways |
| Resource costs | Simplified fitness penalties in selected experiments | Not fully operationalised | Incomplete |
| Held-out successor utility | Not consistently present in foundational studies | Validation/test task labels exist, but memory causal path is absent | Needs redesign |
| Cross-programme measurement | No validated mapping | No validated mapping | Not established |

## 11. Prior-art boundary

The broad question of how memory, forgetting, social transmission, and environmental change affect adaptation is already studied. The following areas must be included in a full literature review before novelty is claimed:

- cumulative cultural evolution and cultural transmission fidelity;
- Bayesian iterated learning and social learning;
- optimal forgetting, memory allocation, and rate-distortion theory;
- dual-inheritance and gene-culture coevolution models;
- Lamarckian and Baldwinian evolutionary computation;
- continual learning and stability–plasticity methods;
- open-ended evolution and its measurement criteria;
- information theory and thermodynamics of computation.

The current repository literature review is a starting outline, not a completed systematic or exhaustive review. A paper-by-paper comparison matrix is still required. The candidate novelty, if any, must be narrower than the general claim that inherited information can become stale or that forgetting can help adaptation.

## 12. Theorem and claim discipline

Every theorem must include:
- exact definitions and domains;
- all assumptions, including independence and stationarity assumptions;
- a complete proof;
- boundary cases;
- counterexamples when assumptions are relaxed;
- a clear mapping to any implementation claimed to instantiate it.

A simulation is not a proof. A test suite verifies programmed invariants, not a scientific theory. A small p-value does not repair construct validity or a mismatched baseline.

The following existing claims require continued scrutiny and must not be presented as established:
- universal or general critical-volatility phase transition;
- exact variance/energy conservation under the current noisy inheritance implementation;
- a universal Golden Ratio retention law or attractor;
- biological metabolic interpretation of arbitrary fitness penalties;
- open-ended evolution from fixed task or state spaces;
- superiority over established continual-learning baselines;
- consciousness or subjective experience from LLM narratives.

## 13. Governance and versioning

- Keep GAL 1.0 and GAL 2.0 implementations, raw outputs, and protocols separate.
- Treat this document as the shared theoretical specification, not a new implementation.
- Preserve historical manuscripts and results; correct claims through versioned revisions rather than silently rewriting history.
- Record source commit, protocol version, dependencies, seeds, raw outcomes, exclusions, and analysis code for every confirmatory study.
- A green CI run establishes software execution only.
- Do not call a manuscript peer-reviewed without a verifiable publication record.
- Do not call a study independent unless the analysis and replication are genuinely independent of the original result.

## 14. Existing source documents consolidated here

This specification is intended to serve as the canonical entry point to, not a replacement for, the following documents:

- `research/GAL_RESEARCH_FOUNDATIONS.md` on branch `research/gal-shared-theory`;
- `research/GAL_CROSS_PROGRAMME_PROTOCOL.md` on branch `research/gal-shared-theory`;
- `GAL_RESEARCH_PROGRAMME_FRAMEWORK.md`;
- `GAL_IMPLEMENTATION_THEORY_AUDIT.md`;
- `GAL_EXACT_INHERITANCE_CHANNELS.md`;
- `GAL_INFORMATION_THERMODYNAMICS.md`;
- `GAL_BINARY_INFORMATION_BENCHMARK.md`;
- `gal2/ANALYTICAL_THEORY.md`;
- `gal2/SCIENTIFIC_VALIDATION_GAP_AUDIT.md).

The shared-theory branch documents remain valuable historical and programme-specific sources. This file does not delete or supersede their implementation-specific conclusions.

---

## Final position

GAL's strongest path is to investigate **when generational information transfer is beneficial, harmful, or wasteful because of evidence quality, dependence, environmental change, and finite verification resources**.

The current repository supplies useful models, mechanisms, and mathematical tools. It has not yet established that this combined account is novel or empirically superior to existing explanations.

The next scientific deliverable should be a completed literature comparison and a fully specified analytical model. Only after those steps should a new confirmatory simulation be implemented.
