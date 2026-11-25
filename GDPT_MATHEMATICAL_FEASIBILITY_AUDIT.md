# GDPT v1 — Mathematical Feasibility Audit

**Scope:** theory and prior art only. No code, experiment, or GAL state changes.

**Conclusion:** **Conditional candidate requiring a specific missing proof.**

Robust decisions under unknown evidence dependence, partial identification, and finite-action compression are established ideas. A fixed decision problem can be preserved by transmitting a compact summary of robust action values rather than a posterior or provenance graph. The unresolved question is whether such summaries can be constructed online, with bounded memory, and maintained across generations and recurring regimes with a non-vacuous uniform approximation guarantee under uncertain ancestry. If that construction reduces to standard robust aggregation plus an existing coreset or streaming summary, GDPT has no algorithmic novelty.

This document distinguishes established results, deductions for GDPT, and the missing conjectural result. Citations are to primary papers where available; claims about their scope are intentionally narrow.

## 1. Formal model

### 1.1 State, evidence, ancestry, and environment

Let generations be indexed by `g = 0,1,...`; within-generation time is `t`.

- `X_{q,t} ∈ X_q` is the latent truth of claim `q` at time `t`. A special value `⊥` represents withdrawal/no current value.
- `R_t ∈ {1,...,J}` is an environmental regime. A transition kernel `T_R(r'|r)` permits recurrence: a regime can return after an intervening regime.
- Evidence item `i` has observed content `Y_i`, claim/time index `(q_i,t_i)`, and an ancestry graph `G`. An edge `j → i` says `i` was copied or transformed from `j`; roots are acquired from a source. Each edge has a transformation/corruption kernel `K_i(y_i|y_j,X,R,η_i)`. Root reports have kernels `K_i(y_i|X_{q_i,t_i},R_{t_i},η_i)`.
- `η` collects source-reliability and transformation parameters. It is included because without constraints on it, ancestry alone need not identify truth.
- `H=(G,η,T_R,...)` is a complete generative history. The observed records need not identify `H`.
- `C_g` is the finite-memory state transmitted from generation `g` to `g+1`, with encoded storage at most `K` bits (or a specified number of machine words; the unit must be fixed in an implementation paper).
- `V_g` is the generation-`g` verification budget. A verification action consumes a known cost and produces a report through a stated verification channel. It is not treated as an oracle unless the channel is perfect by assumption.
- `A` is a finite action set, e.g. `{retain, revise(v), withdraw, abstain}`. Utility `u_g(a,X,R)` is bounded. Action-relevant regimes or future queries must be stated; otherwise a summary preserving one task need not preserve another.

Given a full history `h` and observations `y`, the likelihood factors according to the ancestry graph:

\[
p_h(y\mid x,r)=\prod_{i\in roots(G)}K_i(y_i\mid x_{q_i,t_i},r_{t_i},\eta_i)
\prod_{i\notin roots(G)}K_i(y_i\mid y_{pa_G(i)},x_{q_i,t_i},r_{t_i},\eta_i).
\]

This prevents a copied record from being silently counted as a fresh independent observation. If records share a source but their parent edge is unavailable, the model must either introduce a latent shared source/cluster or include multiple compatible graphs.

### 1.2 Uncertain histories and posterior sets

Let `H_g(c_g)` be the set of histories compatible with all observations and metadata received by generation `g`. For each history `h`, prior `π_h`, and known likelihood, define

\[
P_h^g(dx,dr\mid c_g)
\propto p_h(c_g\mid x,r)\,\pi_h(dx,dr).
\]

The set-valued posterior is

\[
\mathcal P_g(c_g)=\{P_h^g(\cdot\mid c_g):h\in H_g(c_g)\}.
\]

It is a singleton only under point-identification assumptions. Bayesian model averaging is a different object: it assigns probabilities over `h` and averages these posteriors. Robust Bayes leaves a set of posteriors/priors and optimizes against that set.

### 1.3 Generation channel, recurrence, and budgets

The parent computes memory state `C_g = φ_g(history_g)` under storage budget `K`. The next generation receives a possibly corrupted/compressed message

\[
M_{g+1}\sim Q_g(\cdot\mid C_g),\qquad |M_{g+1}|\le K,
\]

and receives local observations/verification results `O_{g+1}`. The successor forms `C_{g+1}=ψ_g(M_{g+1},O_{g+1})`. The hidden regime follows `T_R`; if the transition model is uncertain, its possible values belong in `H_g` as well. Verification actions are chosen subject to total cost `≤V_g` and update the history set through their outcomes. A verification result resolves ancestry only if the verification channel actually carries that information—for example, it authenticates source identity or gives independent truth evidence.

This is a model class, not a proposed implementation. It separates temporal recurrence from evidence ancestry: a change in regime does not imply that records are independent, and shared ancestry does not imply a stationary truth value.

## 2. Does uncertainty propagate monotonically?

There is no general monotonicity theorem without a definition of uncertainty and assumptions on observations/channels. Posterior sets at different generations may also be over different variables, so set inclusion can be ill-typed. For a fixed claim space, use set inclusion or diameter under a metric; for decisions, use the width of the action-value set.

### 2.1 Uncertainty can shrink

Suppose the prior set for binary `X` is `P_0={Bernoulli(0.2), Bernoulli(0.8)}`. A perfect independent verification reports `Z=X`. Conditional on `Z=1`, both priors update to the point mass at `X=1`; the posterior set collapses to `{δ_1}`. This assumes a perfect, truth-revealing verification channel. With imperfect verification the set will generally shrink less and need not collapse.

### 2.2 Uncertainty can expand

Suppose at generation 0 the source identity is observed, so the only possible relation is “two records share root `s`.” A transmission channel drops that identifier and the successor sees two identical records. Histories “one common source” and “two independent sources” are now both compatible. Relative to the successor’s observable information, the identified set can strictly enlarge. This is loss of metadata, not a failure of Bayesian updating.

### 2.3 Uncertainty can move without nesting

At generation 0 two histories may remain plausible: shared-source/truthful and shared-source/unrelated. At generation 1, an authenticated new independent observation can eliminate one; simultaneously, regime uncertainty can create new uncertainty about whether an older claim has recurred. The new posterior set may be narrower for current truth but wider over the joint variable `(truth, regime, ancestry)`. Thus neither “always increases” nor “always decreases” is correct.

**Established mathematics:** data processing cannot increase information about a fixed latent variable for a fixed probability model. It does not imply monotone diameter of a *set of models* when channels, model uncertainty, or the target state change.

## 3. Identification and impossibility

### 3.1 Observational equivalence example

Let `U ~ Bernoulli(1/2)`.

- History A: `X=U`, and two reports are copies: `Y_1=Y_2=U`.
- History B: `X~Bernoulli(1/2)` independently of `U`, and `Y_1=Y_2=U`.

Both generate exactly the same observable-data distribution:

\[
P(00)=P(11)=1/2,\qquad P(01)=P(10)=0.
\]

Yet after `Y_1=Y_2=1`, History A has `P(X=1|Y)=1` and History B has `P(X=1|Y)=1/2`. Under suitable assertion/abstention utility, their optimal actions differ.

### 3.2 Impossibility theorem

**Theorem 1 (no uniform identification from observationally equivalent histories).** Let two histories `h_A,h_B` induce the same distribution `P^Y` over every observable available to an algorithm, but induce distinct target posteriors `P_A(X|Y)` and `P_B(X|Y)` on an event `E` of positive probability. No estimator `\hat p(Y)` can equal both target posteriors almost surely. If the histories imply different unique optimal actions on `E`, no decision rule based only on `Y` can be optimal in both histories on `E`.

**Proof.** Since the observable distributions agree, any possibly randomized estimator or policy has the same conditional output distribution under `h_A` and `h_B` for each realized `Y`. On event `E`, the required posterior values differ, so that common output cannot equal both. If each history has a different unique optimal action, the common action distribution cannot put probability one on both distinct actions. Hence at least one history incurs positive decision loss on `E`. ∎

The theorem is an elementary consequence of non-identification. It is not a GDPT contribution by itself.

### 3.3 Finite-memory lower bound for unrestricted future queries

**Theorem 2 (pigeonhole lower bound).** Suppose a generation has `n` independent binary claims whose truth vector `x∈{0,1}^n` is perfectly known, and a successor may receive any index `j∈{1,...,n}` and must assert `x_j` with zero error. Any deterministic one-way memory representation preserving all such decisions for every `x` requires at least `n` bits.

**Proof.** If memory has fewer than `n` bits, it has fewer than `2^n` states. By pigeonhole, two distinct vectors `x,x'` map to the same memory state. They differ at some coordinate `j`. The same received query `j` then requires opposite decisions from identical transmitted states, impossible for the decoder. ∎

This is a worst-case information lower bound. Randomized schemes also have communication lower bounds for low error; zero-error deterministic form suffices to establish the limitation. It does **not** imply that finite memory cannot preserve one fixed decision: if the decision context and utility are fixed and the parent can compute the answer, transmitting the selected action takes only `ceil(log2 |A|)` bits. The hard part is preserving decisions for a family of future claims, utilities, regimes, or verification opportunities.

Unknown source reliability makes the identification example stronger: source labels alone need not identify `X`; a labeled source may be arbitrarily unreliable unless calibrated or constrained.

## 4. Decision policies and positive guarantees

For history `h`, define action value

\[
V_h(a;c_g)=\mathbb E_{P_h^g}[u_g(a,X,R)].
\]

### 4.1 Expected utility

With a specified posterior distribution over histories `w_g(h|c_g)`, use

\[
a_{EU}=\arg\max_a\sum_h w_g(h|c_g)V_h(a;c_g).
\]

This can be efficient and informative, but weights over histories are substantive assumptions. If they are unsupported, this rule may give false precision.

### 4.2 Maximin robust utility

Without defensible history probabilities, use

\[
a_{MM}=\arg\max_a \inf_{h\in H_g(c_g)}V_h(a;c_g).
\]

This protects worst-case utility, and can be conservative if the plausible-history set is broad.

### 4.3 Minimax regret

Define `r_h(a)=max_{a'}V_h(a')-V_h(a)`. Then

\[
a_{MR}=\arg\min_a\sup_{h\in H_g(c_g)}r_h(a).
\]

This controls loss relative to the decision that would be optimal if the true history were known. Expected utility, maximin utility, and minimax regret can select different actions; the choice is normative, not determined by the evidence model alone.

### 4.4 Decision-focused bounded summaries

For a fixed finite action set, the full provenance graph/posterior is not necessarily needed. Define its robust value vector

\[
v_g=(v_g(a):a\in A),\qquad v_g(a)=\inf_{h\in H_g}V_h(a).
\]

For maximin action selection, these `|A|` values are a sufficient decision summary. If the exact vector is already computed, it can be quantized. Suppose values lie in `[L,U]`, and each coordinate is quantized with absolute error at most `δ`. Then encoding all values requires `O(|A| log((U-L)/δ))` bits; selecting an action from the decoded vector has robust regret at most `2δ` relative to the full-history maximin action.

For minimax regret, preserve `V_h(a)` sufficiently to approximate `max_a V_h(a)-V_h(b)` uniformly in `(h,a,b)`, or preserve the corresponding worst-case regret vector. Preserving only the maximin value vector is generally insufficient for minimax regret.

**Proposition 1 (robust action stability).** Let `V(a)=inf_h V_h(a)` and a bounded summary produce `\tilde V(a)` such that `sup_a |V(a)-\tilde V(a)|≤δ`. Let `a*` be the unique maximizer of `V`, with margin `m=V(a*)-max_{a≠a*}V(a)`. If `m>2δ`, then `argmax_a \tilde V(a)=a*`. More generally, selecting `\tilde a=argmax_a \tilde V(a)` has robust regret `V(a*)-V(\tilde a)≤2δ`.

**Proof.** For any competitor `a`, `\tilde V(a*)≥V(a*)-δ` and `\tilde V(a)≤V(a)+δ`. If the margin exceeds `2δ`, then `\tilde V(a*)>\tilde V(a)`. For the regret result, optimality under the summary gives `\tilde V(\tilde a)≥\tilde V(a*)`; hence `V(a*)-V(\tilde a)≤(V(a*)-\tilde V(a*))+ (\tilde V(\tilde a)-V(\tilde a))≤2δ`. ∎

This is a candidate positive result, but it is a generic finite-action decision result. It does not show that a bounded streaming algorithm can compute `\tilde V` with small `δ` under latent ancestry.

## 5. Multi-generation approximation and regret

Let `e_g` be a metric error between the exact robust value vector (or relevant robust regret vector) and the one represented in memory at generation `g`. A generic stability recurrence is

\[
e_{g+1}\le L_g e_g+\delta_g,
\]

where `δ_g` is new compression/channel/inference error and `L_g` is the sensitivity of the next update to inherited error. Iterating,

\[
e_g\le \left(\prod_{i=0}^{g-1}L_i\right)e_0+
\sum_{j=0}^{g-1}\delta_j\prod_{i=j+1}^{g-1}L_i.
\]

If `L_g≤L` and `δ_g≤δ`, then for `L<1`, `e_g≤L^g e_0+δ(1-L^g)/(1-L)`; for `L=1`, `e_g≤e_0+gδ`; for `L>1`, error can grow geometrically. This is a conditional perturbation bound, not yet an algorithmic result. GDPT must establish an appropriate `L_g` for its set-valued update, channel, and regime recurrence. Bayesian conditioning can be highly sensitive near zero likelihoods, so a finite universal Lipschitz constant is not automatic.

A corresponding maximin decision-regret bound is at most `2e_g` by Proposition 1. It is non-vacuous only if `e_g` stays meaningfully below the utility scale and decision margin.

## 6. Counterexamples to monotonicity and guarantees

1. **Uncertainty shrinks:** perfect independent verification collapses a binary truth posterior set to a point.
2. **Uncertainty expands:** a transmission channel deletes source IDs, making previously excluded independent/shared-source graphs both plausible.
3. **Uncertainty is incomparable:** truth uncertainty shrinks after verification while regime uncertainty expands after a surprising observation.
4. **No utility guarantee from posterior compression alone:** a posterior perturbation arbitrarily close to a decision threshold can flip the action. Decision margin matters.
5. **No uniform guarantee under unrestricted future queries with `K<n` bits:** Theorem 2.
6. **No inference can cure observational equivalence:** Theorem 1. More computation does not recover metadata absent from the observation distribution.

## 7. Prior-art comparison

### de Oliveira, Ishii, and Lin (2023), *Robust Aggregation of Correlated Information*

The paper models a finite state space, prior, finite actions, utilities, and `m` Blackwell experiments. The decision maker knows each source in isolation but allows **any joint information structure whose marginals agree with the known source experiments**. The robust strategy maximizes expected payoff in the worst admissible joint structure. Their Theorem 1: with two states and two actions, robust value equals the value of the best single source. Their Theorem 2 decomposes a two-state multi-action problem into binary comparisons and needs at most `n−1` sources for `n` actions. Their Theorem 3 bounds required sources by the number of kinks in the interim value function for general finite states. The PDF is dated October 2023 and is available as a working paper; publication status was not established in this audit. [Primary paper, model and theorem statements](https://economics.princeton.edu/wp-content/uploads/2023/08/Robust-Aggregation-of-Correlated-Information-Lin.pdf)

**Exact overlap:** robust decisions with unknown correlations among reports, finite state/action spaces, worst-case expected payoff.

**Difference:** source marginal experiments are assumed known. The paper does not maintain a generational ancestry graph, unknown source reliability, a finite-memory message, or regime recurrence. GDPT would be reducible to this work if it only says “consider all dependence structures consistent with source marginals and choose a robust action.”

### Partial identification (Manski; Tamer and related work)

Partial identification defines the set of parameter values/distributions observationally compatible with data plus maintained assumptions, then derives bounds and decisions from that set. It covers the mathematical form of `H_g`/`P_g`, including the impossibility of point-identification under observational equivalence. It does not supply a particular online ancestry-compression algorithm. [Manski](https://doi.org/10.1016/j.ijar.2004.10.006) · [Tamer](https://doi.org/10.1146/annurev.economics.050708.143401)

### Robust Bayesian decision theory

Gamma-minimax, multiple-prior, and minimax-regret methods already specify decisions over sets of priors/posteriors. They provide the criteria in §4, not a method for learning/compressing lineage sets. [Berger](https://doi.org/10.1080/03610927908827780)

### Latent source clusters and unknown dependence

Latent-class and dependent diagnostic-test models add latent truth, source/test accuracy, and conditional covariance. Hui–Walter-type assumptions can identify some models using multiple populations; adding dependence parameters can remove identification. This is a direct warning that introducing latent source variables does not guarantee identifiability. [Global identifiability analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC7036323/) · [Conditional dependence model](https://pmc.ncbi.nlm.nih.gov/articles/PMC4493568/)

### Uncertain graphical structures

Bayesian structure learning represents posterior uncertainty over DAGs and parameters. It gives a model-based alternative to a set-valued graph class when a graph prior and likelihood are supplied. It does not guarantee robust decisions under graph-prior misspecification or bounded-memory generational transmission. [Joint Bayesian inference over graph structure and parameters](https://arxiv.org/abs/2305.19366)

### Bayesian coresets and decision-focused compression

Bayesian coresets approximate the posterior by approximating its likelihood, with guarantees under assumptions and known lower-bound limitations. A decision-focused representation can instead preserve action values; Proposition 1 gives the elementary margin condition. Existing coreset literature makes generic posterior compression non-novel. This audit did not find a primary paper that gives a uniform robust-action guarantee over a set of latent provenance graphs and repeated generational updates. That is an absence from this search, not proof of a gap. [Fast Bayesian Coresets](https://arxiv.org/abs/2203.09675) · [General bounds](https://arxiv.org/abs/2405.11780)

### BOCPD, BAM, and regime memory

BOCPD tracks a posterior over run length under a specified hazard and segment likelihood; BAM selects past observations to recall in nonstationary environments. They address changes and recurrence/memory, not unknown source ancestry. Adding a regime index to a robust ancestry model is straightforward composition unless a new stability result is proved. [BOCPD](https://arxiv.org/abs/0710.3742) · [BAM](https://openreview.net/pdf/570533db54609ccaa349705c913de9ad4439ee1d.pdf)

### Iterated learning / cultural transmission

Bayesian iterated learning models generations as learners receiving data from prior learners and producing new data. This supplies standard transmission-channel formalization. A generational setting alone does not make the inference problem new; a contribution would need a result about how robust uncertainty or decision regret evolves under lineage loss and recurrent regimes. [Griffiths and Kalish (2007)](https://doi.org/10.1080/15326900701326576)

## 8. Candidate bounded-memory mechanism (not yet a justified new algorithm)

For a **fixed finite decision problem**, maintain an approximation to the robust action-value vector, not the whole graph:

1. Maintain or receive an admissible set of histories/graphs `H_g` and compute `v_g(a)=inf_{h∈H_g} E_h[u(a,X,R)|records]` for each action.
2. Quantize each value to error at most `δ_g`; transmit the quantized vector, utility/action identifiers, regime scope, and a certified error bound.
3. On successor evidence, update the history set and recompute the robust vector. Verification budget is spent on observations whose possible outcome can change the robust action or narrow the worst-case value set; this is decision-focused VOI.
4. If exact recomputation is impossible, use a coreset/variational approximation and separately certify uniform action-value error over the maintained graph set.

**Memory:** `O(|A| log((U-L)/δ))` bits per fixed decision context, plus context/regime identifiers and certified error metadata. For `J` contexts/regimes, multiply by `J`; if future queries are unrestricted, this bound does not apply.

**Update cost:** dominated by robust optimization over histories. With `H` explicitly enumerated graphs and per-graph inference cost `I`, naive cost is `O(HI)` per update. Optimizing over all dependence structures can be a linear/convex program for special finite models, but general latent DAG inference is combinatorial/intractable. The compact transmitted value vector does not make its computation cheap.

**Failure conditions:** wrong admissible-history set; unknown utilities or future query family; unbounded or unstable likelihood ratios; verification that does not distinguish histories; too little memory for all future contexts; recurring regimes not identifiable; error certificates too loose to preserve decision margins.

This mechanism is a reduction to robust decision sufficient summaries and approximate optimization. Without a new way to construct/certify the summary efficiently, it is not an algorithmic contribution.

## 9. Strongest-baseline reproduction and decisive comparison

The strongest baseline composition is:

1. Set-valued partial identification over histories/graphs compatible with observed records and explicit assumptions.
2. De Oliveira–Ishii–Lin robust aggregation over all joint structures consistent with known report marginals when that model applies.
3. Maximin utility or minimax regret over the resulting posterior set.
4. Regime-aware state (HMM/BOCPD or BAM-style memory) for temporal recurrence.
5. Bayesian coreset/streaming approximation, evaluated in robust action-value error rather than only posterior KL.

GDPT must outperform this composition under matched metadata, compute, and memory. The decisive comparison is whether GDPT can provide a **non-vacuous uniform bound** on worst-case action regret after `g` handoffs, under uncertainty over source graph and regime, at a storage/update cost lower than the baseline. A positive result must state the admissible graph class, reliability assumptions, utility class, channel model, and constants in the bound.

### Abandonment criterion

Abandon the algorithmic novelty claim if any of the following holds:

- GDPT’s robust policy is simply maximin/minimax regret over a set of graph-induced posteriors;
- its uncertainty set is equivalent to arbitrary joint correlation structures with fixed source marginals, so the de Oliveira et al. baseline applies;
- its memory state is merely a coreset, sufficient statistic, or quantized robust-value vector without a new construction or bound;
- its generation/regime update is an ordinary state-space, BOCPD, BAM, or iterated-learning transition;
- the only guarantee is Proposition 1 or a generic perturbation recurrence, without proving useful constants under uncertain lineage.

## 10. Final assessment

**Required conclusion: Conditional candidate requiring a specific missing proof.**

The mathematical ingredients are established. A bounded action-value summary can preserve robust decisions, with regret controlled by its uniform approximation error; the proof is given above. But this does not yet establish a useful algorithm because the robust values may be expensive to compute and no non-vacuous error bound has been shown for their online approximation across latent lineage graphs and generations.

The exact missing proof is:

> Construct an online, `K`-bit summary and update rule for a stated class of uncertain ancestry graphs and recurring-regime models, and prove a uniform bound `sup_{g≤G} Regret_g ≤ ε(K,G,𝓡)` that is non-vacuous and strictly improves the computation/memory tradeoff of robust aggregation plus standard streaming/coreset methods.

Until that is proven, the defensible position is **no demonstrated algorithmic novelty**. The impossibility theorem establishes a limitation of the information, not a GDPT contribution. The fixed-decision compression proposition is a generic positive result, not a novel ancestry algorithm. If the missing proof reduces to an existing robust aggregation theorem plus generic quantization/coreset bounds, the final classification should be **no-go: reducible to established methods**.

## References

- de Oliveira, H., Ishii, Y., & Lin, X. *Robust Aggregation of Correlated Information*. Working paper dated 2023. [PDF](https://economics.princeton.edu/wp-content/uploads/2023/08/Robust-Aggregation-of-Correlated-Information-Lin.pdf)
- Manski, C. F. (2005). “Partial identification with missing data: concepts and findings.” [DOI](https://doi.org/10.1016/j.ijar.2004.10.006)
- Tamer, E. (2010). “Partial Identification in Econometrics.” [DOI](https://doi.org/10.1146/annurev.economics.050708.143401)
- Berger, R. L. (1979). “Gamma-minimax robustness of Bayes rules.” [DOI](https://doi.org/10.1080/03610927908827780)
- Nassar, J. et al. (2022). “BAM: Bayes with Adaptive Memory.” [OpenReview PDF](https://openreview.net/pdf?id=570533db54609ccaa349705c913de9ad4439ee1d.pdf)
- Adams, R. P. & MacKay, D. J. C. (2007). “Bayesian Online Changepoint Detection.” [arXiv](https://arxiv.org/abs/0710.3742)
- Naik, C., Rousseau, J., & Campbell, T. (2022). “Fast Bayesian Coresets via Subsampling and Quasi-Newton Refinement.” [arXiv](https://arxiv.org/abs/2203.09675)
- Campbell, T. (2024). “General bounds on the quality of Bayesian coresets.” [arXiv](https://arxiv.org/abs/2405.11780)
- “Global identifiability of latent class models with applications to diagnostic test accuracy studies: A Gröbner basis approach.” *Biometrics* 76(1), 98–108. [Published article](https://academic.oup.com/biometrics/article-pdf/76/1/98/54284747/biometrics_76_1_98.pdf)
- Hui–Walter conditional-dependence extension. [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4493568/)
- Griffiths, T. L. & Kalish, M. L. (2007). “Language Evolution by Iterated Learning With Bayesian Agents.” [DOI](https://doi.org/10.1080/15326900701326576)
