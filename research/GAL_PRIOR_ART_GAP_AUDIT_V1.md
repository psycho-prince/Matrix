# GAL Prior-Art and Research-Gap Audit v1

**Status:** Preliminary literature-to-GAL comparison; not a novelty certification  
**Prepared:** 25 November 2026  
**Branch:** `research/gal-prior-art-gap-audit-v1`  
**Base:** `research/gal-2.1-memory-grounded-learning`  
**Scope:** Compare the existing GAL manuscript programme and candidate shared model against established work in cultural evolution, iterated learning, adaptive memory, continual learning, and artificial life.

---

## 1. Executive finding

The current GAL programme is **not yet demonstrably novel at the level of its broad central ideas**.

The following propositions are already well represented in prior work:

- Generational transmission can preserve or transform acquired information.
- Transmission fidelity, reconstruction, and population-level biases affect cumulative culture.
- Environmental instability creates a trade-off between retaining useful knowledge and adapting to changed conditions.
- Adaptive forgetting and memory selection can improve Bayesian learning in non-stationary environments.
- Continual learning already studies stability–plasticity, replay, regularization, and memory constraints.
- Open-ended evolution requires stronger evidence than continued generational change or growth in a chosen metric.

This does not make GAL worthless. It means the research contribution cannot be “inheritance helps,” “forgetting can be adaptive,” “lossy transfer is useful,” or “generations accumulate knowledge.” Those are too broad and overlap established theory.

**Most promising candidate gap (still unproven):** a formal and experimentally testable account of how *lineage-correlated evidence* should be retained, discounted, independently re-verified, or forgotten across generations when (i) the environment drifts or revisits earlier regimes, (ii) memory is bounded, and (iii) verification and acquisition have explicit costs.

The potential differentiator is not forgetting alone. It is the joint treatment of evidence provenance/dependence, successor-environment relevance, verification allocation, and finite generational budgets in one causal model. A systematic search of adjacent Bayesian, cultural-evolution, and adaptive-filtering literature is still required before making a novelty claim.

## 2. Prior-art map

| Research area | Established result / mechanism | Direct relevance to GAL | What GAL cannot claim from this overlap |
|---|---|---|---|
| Cumulative cultural evolution | Cultural traits can accumulate through intergenerational transmission; fidelity, modification, combination, and population processes affect ratcheting | GAL 1.0 inheritance and teaching operators; generational skill/concept state | That generational transfer or cumulative state is itself new |
| Iterated learning | Learners acquire behaviour from prior learners; Bayesian learner assumptions and transmission bottlenecks shape cultural distributions | Parent-to-successor learning and reconstruction | That learning through generations, or Bayesian transmission, is a new mechanism |
| Fidelity under instability | Copying fidelity and environmental variability interact; trial-and-error can sometimes be more robust than precise imitation | Exact copying versus stochastic teaching/correction; capacity and environmental shifts | That exact copying is always optimal or that lossy transfer is generally superior |
| Adaptive Bayesian memory | In non-stationary environments, naive accumulation of all past data can become stale; adaptive memory/forgetting can select or downweight observations | GAL memory economics and environmental volatility | That adaptive forgetting or memory selection is a new idea |
| Continual learning | Replay, EWC, synaptic consolidation, and other approaches manage stability–plasticity and catastrophic forgetting | GAL neural continual-learning side experiments and parameter inheritance | That generational parameter transfer solves continual learning or beats established baselines |
| Concept drift / filtering | State estimation under changing distributions uses filtering, change detection, discounting, and switching models | Volatile and recurrent environments | That environmental drift or forgetting under drift is a new problem |
| Open-ended evolution | OEE requires sustained novelty and/or complexity growth, with no settled consensus on definitions and measurement | GAL's artificial-life framing | That a multi-generation simulation is open-ended evolution |

### Core sources

1. Lewis et al. (2012), *Transmission fidelity is the key to the build-up of cumulative culture*: https://pmc.ncbi.nlm.nih.gov/articles/PMC3385684/
2. Griffiths & Kalish (2007), *Language Evolution by Iterated Learning With Bayesian Agents*: https://doi.org/10.1080/15326900701326576
3. Kirby, Griffiths & Smith (2014), *Iterated learning and the evolution of language*: https://doi.org/10.1016/j.conb.2014.07.014
4. *Cultural transmission in an ever-changing world: trial-and-error copying may be more robust than precise imitation* (2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC5812963/
5. *The experimental evolution of human culture: flexibility, fidelity and environmental instability* (2022): https://pmc.ncbi.nlm.nih.gov/articles/PMC9627710/
6. Nassar et al., *BAM: Bayes with Adaptive Memory* (2022 preprint): https://arxiv.org/abs/2202.02405
7. *Learning and forgetting using reinforced Bayesian change detection* (2019): https://pmc.ncbi.nlm.nih.gov/articles/PMC6488101/
8. Kirkpatrick et al. (2017), *Overcoming catastrophic forgetting in neural networks* (EWC): https://doi.org/10.1073/PNAS.1611835114
9. Rolnick et al. (2019), *Experience Replay for Continual Learning*: https://proceedings.neurips.cc/paper/2019/hash/fa7cdfad1a5aaf8370ebeda47a1ff1c3-Abstract.html
10. Taylor et al. (2016), *Open-Ended Evolution: Perspectives from the OEE Workshop in York*: https://doi.org/10.1162/ARTL_A_00210
11. *Cultural evolution: A review of theoretical challenges* (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC10955367/
12. *Evolving Machine Learning in Non-Stationary Environments: A Unified Survey of Drift, Forgetting, and Adaptation* (2026): https://doi.org/10.1080/08839514.2026.2707047

The 2026 survey is recent and useful for taxonomy, but a survey is not a substitute for comparing primary algorithms and their assumptions. The BAM work is a preprint, not evidence of peer-reviewed publication.

---

## 3. Manuscript-by-manuscript comparison

**Important audit limitation:** this first pass uses the manuscript descriptions, existing repository audits, and the research specifications available in the programme history. It is not yet a line-by-line reproduction of every manuscript equation, appendix, and code path. Therefore each overlap judgement is provisional. Before submission or a novelty statement, the exact manuscript versions and their equations must be checked against the cited primary papers.

### 3.1 Paper 1 — Parameter copying versus iterative teaching

**Known question/mechanism:** compare exact parameter/skill copying with a stochastic teaching or correction operator in a handcrafted Matrix environment. The historical scope is a narrow paired-seed comparison; it is not a full model of teacher–learner feedback or an empirically grounded human cultural-transmission process.

| Dimension | GAL paper's current framing | Closest prior art | Audit judgement / required change |
|---|---|---|---|
| Question | Does exact copying or iterative teaching better preserve/improve inherited state? | Cultural transmission fidelity; iterated learning; social learning under noise | The high-level question is established |
| Mechanism | Exact state copy versus stochastic correction/teaching | Bayesian iterated learning; trial-and-error copying; cultural transmission models | Need define the operator mathematically and compare transition kernels |
| Assumptions | Finite symbolic task world; specified synthetic skill dynamics | Prior work varies learner biases, fidelity, population structure, and environmental variability | State clearly which assumptions are deliberately simplified |
| Environment | Handcrafted Matrix tasks | Laboratory transmission chains and agent-based cultural evolution models | No ecological or human generalisation follows |
| Baselines | Copying and teaching conditions, plus controls described in the manuscript audit | No transmission, individual learning, high/low fidelity, reconstruction, and population-level correction are relevant comparators | Add only baselines required by the precise hypothesis; do not inflate the experiment |
| Metrics | Task performance and generational state/skill measures | Cultural trait persistence, task success, cumulative performance | A skill/concept count is not information or cultural complexity |
| Evidence level | Synthetic simulation, paired seeds | Formal models plus human/animal experiments in parts of the literature | A narrow simulation result, not a general transmission law |
| Potential distinct contribution | A precisely specified operator comparison under a controlled task and noise schedule | Mechanisms are not novel at broad level | Could be a useful replication/benchmark study if the operator effect is robust and carefully isolated |

**Must be tested/falsified:** Does iterative teaching outperform exact copying only when observation noise or task variation lies in a defined range? Does the result survive independent environments, matched information budgets, and a baseline with successor individual learning? If it does not, the paper should report the boundary or null result rather than a universal preference.

**Primary comparison:** Lewis et al. (2012); Griffiths & Kalish (2007); Kirby et al. (2014); trial-and-error copying under environmental variability (2018).

### 3.2 Paper 2 — Capacity saturation and lossy transmission

**Known question/mechanism:** a bounded skill-capacity model with environmental switching compares exact copying and fixed fractional retention/loss. The paper argues that lossy transmission can prevent saturation and support adaptation under volatility.

| Dimension | GAL paper's current framing | Closest prior art | Audit judgement / required change |
|---|---|---|---|
| Question | Can lossy inheritance outperform exact copying under finite capacity and environmental switching? | Cumulative culture under fidelity constraints; adaptive forgetting; information bottlenecks; continual learning | Capacity limits and forgetting are established; exact combined boundary may be worth testing |
| Mechanism | Bounded skill capacity; exact copy versus fixed fractional retention | Memory decay/discounting, Bayesian adaptive memory, replay-buffer limits, rate-distortion and compression ideas | Fixed fractional loss is not equivalent to optimal or evidence-aware forgetting |
| Assumptions | Stylised bounded state, switching regimes, fixed retention parameter | Prior models distinguish environmental dynamics, learner bias, fidelity, and memory policy | Make capacity, switching process, and retention law explicit |
| Mathematics | Retention/capacity transition and performance comparison | Cultural transmission models and adaptive-filtering equations | Need derive the threshold rather than infer a universal law from phase plots |
| Baselines | Exact copying and lossy retention | No memory, random deletion, age decay, adaptive discounting, reconstruction, and acquisition-only controls | Fixed-fraction loss is an incomplete baseline set |
| Metrics | Performance, retention, saturation, generation trends | Prediction risk, information retained, task utility, adaptation lag | Do not equate reduced state size with useful information |
| Evidence level | Synthetic simulation and analytical simplification | Formal models plus empirical cultural and ML studies | Results remain model-dependent |
| Potential distinct contribution | A closed-form or validated phase boundary for when a specific lossy channel beats exact copying under explicit capacity and drift assumptions | The general idea is already present in memory economics and cultural transmission | Novelty can only reside in a nontrivial derivation or predictive boundary not already implied by known models |

**Must be tested/falsified:** Is the alleged benefit caused by actual reduction of stale information, by a lower effective learning rate, by random regularisation, or by an implementation-specific cap? Compare fixed retention against adaptive memory, age-based discounting, and change detection. Test recurrent environments: a policy that discards knowledge after one shift may fail when an earlier regime returns.

**Critical conceptual warning:** a fixed fractional deletion rule is not evidence that “loss is required for cumulative inheritance.” It is one intervention. High-fidelity transmission can support cumulative culture, while adaptive forgetting can help under non-stationarity. Which mechanism wins depends on the environment and learning process.

**Primary comparison:** Lewis et al. (2012); *Cultural transmission in an ever-changing world* (2018); Nassar et al. (BAM, 2022); *Learning and forgetting using reinforced Bayesian change detection* (2019); *The experimental evolution of human culture* (2022).

### 3.3 Paper 3 — Memory economics and agile amnesia

**Known question/mechanism:** joint schedules for retention, learning, capacity, and environmental volatility; exploratory phase diagrams examine when retaining inherited state or forgetting/adapting is beneficial. Existing audit notes identify differences between main and supplementary seed configurations.

| Dimension | GAL paper's current framing | Closest prior art | Audit judgement / required change |
|---|---|---|---|
| Question | How does environmental volatility affect retention versus forgetting? | Adaptive memory, Bayesian forgetting, concept drift, change detection, switching state-space models | The broad question is already studied |
| Mechanism | Co-varying retention, learning rate, capacity, and environment schedule | BAM selects memories; Bayesian change detection adapts forgetting; filters discount stale observations | Need distinguish a policy search from a principled decision rule |
| Assumptions | Synthetic volatility schedules and exploratory parameter sweeps | Prior work models gradual drift, abrupt change, and recurring latent regimes | Add explicit drift process and recurrence structure |
| Baselines | Retention/learning/capacity schedules | Fixed memory, exponential discounting, change-point detection, BAM-like adaptive selection, no transfer | Include strong adaptive-memory comparators |
| Metrics | Task performance and parameter/retention outcomes | Predictive log loss, calibration, adaptation delay, false change detections, memory and compute cost | Include regret or risk over the full time series, not only terminal score |
| Evidence level | Exploratory simulation; seed-configuration differences documented | Formal Bayesian and filtering models plus simulations | Exploratory plots do not establish a general law |
| Potential distinct contribution | A jointly constrained, lineage-aware memory policy that optimises retention, verification, and new acquisition across generations | Adaptive memory already handles selection/forgetting; exact novelty is unclear | The most promising avenue is explicit lineage dependence plus verification-cost allocation under recurrent drift |

**Must be tested/falsified:** Does the proposed policy beat BAM-style adaptive memory and conventional change-detection baselines when all receive the same observations, memory capacity, and compute budget? Does it still win when the environment revisits previous regimes? Is the result robust to misspecified drift models?

**Primary comparison:** BAM (2022); reinforced Bayesian change detection (2019); concept-drift filtering literature; experimental cultural learning under instability (2022).

### 3.4 Paper 4 — Continual learning via generational parameter transmission

**Known question/mechanism:** an exploratory MLP study on Circle and XOR task distributions transfers or retains network parameters across generations. The prior audit records benchmark naming, random seeding, result-table, and baseline-comparability concerns.

| Dimension | GAL paper's current framing | Closest prior art | Audit judgement / required change |
|---|---|---|---|
| Question | Can generational parameter transfer preserve/adapt neural task competence? | Continual learning, neuroevolution, Lamarckian inheritance, weight inheritance, transfer learning | Parameter inheritance is a long-established mechanism |
| Mechanism | MLP weights are transmitted or partially retained across task/generation transitions | EWC, replay, synaptic intelligence, parameter inheritance in evolutionary algorithms | Must distinguish biological analogy from actual update rule |
| Tasks | Circle versus XOR toy distributions | Standard class-incremental/task-incremental benchmarks | Toy tasks can test a mechanism but not support broad CL claims |
| Baselines | Existing exploratory arms | Fine-tuning, EWC, SI, experience replay, joint training, random reinitialisation, weight inheritance controls | Match task exposure, compute, parameter count, and replay budget |
| Metrics | Task accuracy/retention | Average accuracy, backward transfer, forward transfer, forgetting, calibration, compute and memory | Report full task-by-generation matrix and confidence intervals |
| Evidence level | Exploratory neural simulation; not validated as a state-of-the-art CL method | Large CL literature and benchmark suites | No claim of solving catastrophic forgetting |
| Potential distinct contribution | A controlled study of generational parameter transmission as a distinct operator with explicit lineage and resource budgets | Weight inheritance and CL are established | Novelty requires a mechanism or boundary not equivalent to existing transfer/regularisation/replay |

**Must be tested/falsified:** Reproduce the established baselines first; then compare parameter inheritance under equal data and compute budgets. Use canonical sequential-learning benchmarks and task-order replications. A proxy using Fisher-weighted retention must not be described as native GAL or as EWC unless it implements the actual method.

**Primary comparison:** Kirkpatrick et al. (2017) EWC; Rolnick et al. (2019) replay; Zenke et al. (2017) synaptic intelligence; neuroevolutionary inheritance literature (systematic search still required).

### 3.5 Consolidated journal manuscript

The consolidated manuscript is a synthesis of the preceding claims, the multi-regime memory-economics experiments, and neural continual-learning material. It is not a separate independent empirical contribution merely because it combines them.

| Dimension | Current state | Required action |
|---|---|---|
| Central claim | Memory economics under environmental volatility | Narrow to one falsifiable claim with one primary estimand |
| Evidence synthesis | Multiple experimental programmes with differing assumptions and evidence maturity | Keep each programme's data, seeds, and controls separate |
| Statistical headline | Prior repository copy advertised a very small p-value | Audit the exact test, unit of analysis, multiplicity, effect size, and reproducible raw data before reuse |
| Theory | Several established equations and mechanism-specific derivations | Separate imported theorems, model assumptions, and GAL-derived results |
| Submission readiness | Existing audit flags reproducibility and comparability issues | Do not treat the consolidated manuscript as ready until those are resolved |

---

## 4. Equation-level comparison: what is and is not new

The following equations are present in the consolidated GAL theoretical foundation or existing analytical programme. Their mathematical forms are established; they are not new discoveries by GAL.

### 4.1 Bayesian updating

For hypothesis \(\theta\) and evidence \(y\):

\[
p(\theta\mid y)=\frac{p(y\mid\theta)p(\theta)}{p(y)}
\]

This is Bayes' rule. Repeated multiplication of likelihoods assumes the relevant conditional independence structure. Descendant records copied from one ancestral observation cannot be counted as independent evidence merely because there are multiple records.

### 4.2 Linear opinion pool

\[
\pi_c=(1-r)\pi_0+r\pi_p,\quad r\in[0,1]
\]

This is a convex mixture of distributions. It is not Bayesian updating in general. A specific model must explain why the mixture is appropriate, how \(r\) is chosen, and how it differs from discounting evidence or mixing priors.

### 4.3 Bayes-factor verification threshold

\[
B\geq\frac{\tau}{1-\tau}\frac{1-p}{p}
\]

This follows from posterior odds and Bayes' rule. A GAL-specific contribution would need to model the cost and allocation of verification, dependence among evidence items, and decision consequences—not simply restate the threshold.

### 4.4 Total-variation shift bound

For loss in [0,1]:

\[
|R_P(f)-R_Q(f)|\leq d_{TV}(P,Q)
\]

This is a standard distribution-shift inequality. It supplies a conservative bound for a fixed decision rule, not a GAL-specific law and not a complete solution to adaptation.

### 4.5 Candidate lineage-aware decision problem

A useful next mathematical object is a finite memory-selection problem. Let each inherited item be

\[
m_j=(h_j,y_j,q_j,a_j,\mathcal{L}_j,c_j),
\]

where \(h_j\) is a claim/hypothesis, \(y_j\) its observation, \(q_j\) a reliability model, \(a_j\) its age or timestamp, \(\mathcal{L}_j\) its lineage/provenance, and \(c_j\) its storage or verification cost.

Let \(S\) be the set retained by a successor, with memory budget \(B\). A candidate policy objective is

\[
\max_{S:\sum_{j\in S}c_j\leq B}
\mathbb{E}_{E_{g+1}}[U(S,E_{g+1})]
-\lambda_v C_v(S)-\lambda_a C_a(S).
\]

This is a **problem formulation, not a novel theorem**. Its scientific value depends on specifying:
- the joint likelihood for correlated/duplicated evidence using lineage;
- a generative model for environmental drift and recurrence;
- how verification changes the posterior or reliability state;
- a measurable successor utility;
- storage, verification, and acquisition costs;
- a tractable policy and a proof or empirical comparison against existing adaptive-memory policies.

A simple age-decay score or a hand-coded lineage penalty would not be enough to establish novelty.

---

## 5. Candidate research gap and novelty test

### 5.1 Narrow research question

> Given a fixed memory and verification budget, when should a successor preserve an inherited claim, discount it, independently re-verify it, or forget it, if evidence records share ancestry and the environment may drift or revisit previous regimes?

### 5.2 Candidate contribution

Develop a **lineage-aware evidence management model** with four explicit operations:

1. **Preserve** — retain a claim when its evidence remains relevant and reliable.
2. **Discount** — reduce evidential weight when observations are stale or correlated.
3. **Verify** — spend limited resources to obtain new, independent evidence.
4. **Forget** — remove claims whose expected future utility is lower than their storage/opportunity cost.

The candidate distinction is the joint optimisation of lineage dependence, environmental relevance, verification, and finite resources across generations. This remains a hypothesis about novelty, not a claim that no prior paper has done it.

### 5.3 Minimum novelty test

Before coding the new model, perform a targeted systematic search for combinations of:
- cultural transmission with correlated or genealogically dependent evidence;
- Bayesian filtering with ancestry/provenance-aware data dependence;
- adaptive memory selection with verification-cost constraints;
- memory allocation under recurrent concept drift;
- evolutionary/continual learning with explicit evidence lineage rather than only parameter or sample replay.

For every closest paper, extract its exact state variables, transition equation, objective, assumptions, baselines, and theorem/empirical result. If a prior model already solves the same constrained optimisation problem, GAL should reproduce, extend, or abandon the candidate rather than rename it.

---

## 6. Proposed confirmatory experiment — only after theory is specified

Do not start this experiment until the equation-level prior-art comparison is complete and the policy is mathematically specified.

### Environment factors

- **Drift:** stationary, gradual, abrupt, and recurrent regimes.
- **Evidence quality:** calibrated high/low reliability.
- **Evidence dependence:** independent observations versus multiple descendants of one source observation.
- **Capacity:** small, medium, and large fixed memory budgets.
- **Verification:** zero, low, and high verification budgets.
- **Acquisition:** explicit cost for new observations or learning.

### Minimum comparison arms

1. No inheritance / learn from current observations only.
2. Exact copying of inherited records.
3. Random deletion at matched memory capacity.
4. Fixed age-based decay.
5. Fixed fractional retention (historical GAL mechanism).
6. Bayesian discounting or a suitable adaptive-filter baseline.
7. Change-detection baseline.
8. BAM-style adaptive memory baseline, with implementation and data budget documented.
9. Proposed lineage-aware preserve/discount/verify/forget policy.

All arms must receive the same observation stream and matched memory, verification, and compute budgets wherever the comparison permits. Include a joint-information or unrestricted-memory reference only as an explicitly labelled upper bound.

### Primary outcomes

- Successor predictive log loss or Brier score on held-out observations.
- Decision utility on held-out tasks.
- Calibration of confidence/reliability estimates.
- False retention of stale claims and false deletion of reusable claims.
- Adaptation delay after a shift and recovery after a regime returns.
- Memory consumed, verification actions, acquisition cost, and compute.
- Generational performance trajectory, not just final-generation score.

### Design and analysis controls

- Preregister the primary outcome, effect size of interest, exclusions, and statistical model.
- Use independent master seeds for environmental trajectories and agent initialisation.
- Pair arms on the same environment trajectories.
- Treat environment trajectory / independent run as the experimental unit; agents within one shared population are not automatically independent.
- Report effect sizes and confidence intervals, not only p-values.
- Correct for planned multiple comparisons.
- Publish raw run-level data and exact reproduction commands.
- Include negative results and all tested parameter schedules.

---

## 7. Stop/go criteria

**GO** only if all are satisfied:

- A close-reading matrix covers the closest primary papers, not just reviews.
- The proposed state, transition, likelihood, and objective are mathematically explicit.
- The model differs from BAM/adaptive filtering and cultural-transmission models in a precise, testable way.
- A nontrivial prediction or theorem is derived before large-scale simulation.
- A fair confirmatory design can falsify the claimed advantage.

**NO-GO / pivot** if:

- The candidate mechanism reduces to an existing adaptive-memory or change-detection algorithm with renamed variables.
- The apparent effect disappears under matched memory/compute/observation budgets.
- The result depends on counting copied descendants as independent evidence.
- The only evidence is a hand-designed score or a terminal performance chart.
- No distinct prediction can be made relative to existing baselines.

A no-go result is useful: it prevents more code from being built around a non-contribution.

---

## 8. Work still required for a full paper-by-paper audit

This document is a preliminary gap audit. The following are deliberately not marked complete:

1. Extract exact equations and assumptions from the final submitted version of each GAL manuscript.
2. Match every GAL equation to its nearest original source, not merely a broad topic.
3. Read primary methods and appendices for BAM, adaptive filtering, cultural transmission, and neuroevolutionary inheritance.
4. Search citation networks and conference proceedings for lineage-aware Bayesian memory and verification-cost allocation.
5. Audit every manuscript result against the corresponding source code, seeds, raw data, and reproduction command.
6. Reconcile inconsistent paper numbering/titles between the historical README and manuscript directories.
7. Produce a claim-by-claim novelty table with status: established prior art / GAL replication / implementation-specific result / plausible extension / unsupported.

Until those steps are complete, the project should use the phrase **“candidate research gap”**, not “novel theory” or “first framework.”

## 9. Bottom line

GAL has a coherent research direction, but its current broad claims overlap substantial existing science. The strongest next move is not another simulation. It is to determine whether lineage-aware evidence dependence and verification allocation under bounded memory and recurrent environmental drift yield a genuinely distinct model.

If the literature already contains that model, cite it and build on it. If it does not, derive the mechanism and a falsifiable prediction first. Either outcome is scientific progress.
