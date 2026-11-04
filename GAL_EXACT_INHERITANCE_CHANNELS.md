# Exact Inheritance Channels: Source-Derived GAL 1.0 and GAL 2.0

**Status:** source-level mathematical specification. The transition rules below are derived from the inspected implementation. Mutual-information values are deliberately not reported because neither branch specifies the required probability distribution over source states or ground truth.
**Scope:** this document supplements `GAL_INFORMATION_THERMODYNAMICS.md`; it does not alter either research programme's code, protocols, or historical results.

## 1. Method and evidence boundary

The channel for an inheritance mechanism is a conditional distribution

\[
K(m'\mid m)=\Pr(M_{child}=m'\mid M_{parent}=m).
\]

A deterministic transfer is represented by a Dirac/deterministic kernel. A stochastic transfer is specified by the random variables and their distributions in the implementation.

To calculate mutual information \(I(X;M)\), a joint distribution for a source/target variable \(X\) and memory \(M\) is also required. The source code specifies transition randomness, but it does **not** specify a probability distribution over true semantic facts, source states, or parent skill values. Therefore this document derives conditional channels and exact conditional expectations, but does not fabricate Shannon information values.

The inheritance step is isolated from later learning/work. GAL 1.0's independent learning and task outcomes, and GAL 2.0's task-generation/training process, are separate information inputs.

---

## 2. GAL 1.0: native inheritance channels

### 2.1 State and assumptions

For one agent, let

\[
M=(S,C),\qquad S=(s_1,\ldots,s_5),\qquad C\subseteq\mathcal V,
\]

where the five skill coordinates correspond to foraging, construction, crafting, exploration, and logic; \(s_i\in[0,1]\); and \(C\) is the set of concept identifiers.

The following calculations assume the child is newly initialized, so its skill coordinates and concept set are zero/empty before the inheritance call. This matches the constructor defaults. They describe the `inherit` call alone, before `learn_independently` or `work`.

### 2.2 Modes A and B-copy

**A — no transfer**

\[
S_c=(0,0,0,0,0),\qquad C_c=\varnothing.
\]

For the inheritance operation, the child state is independent of the parent's state because the method performs no assignment from the parent. This statement is limited to the inheritance call; it does not describe later correlated task streams or other shared experimental inputs.

**B-copy — exact state copy**

\[
S_c=S_p,\qquad C_c=C_p.
\]

This is a deterministic identity channel on the represented skills and concept set. It introduces no transfer noise and preserves the parent state exactly at this step.

### 2.3 Modes C-full and C-no-memory: skill channel

For any parent skill \(p>0\), the implementation draws

\[
X_0\sim\operatorname{Uniform}(0,0.2),
\]

then performs three teaching updates

\[
X_j=X_{j-1}+U_j(p-X_{j-1}),\qquad
U_j\overset{iid}{\sim}\operatorname{Uniform}(0.3,0.7).
\]

Equivalently,

\[
\boxed{X_3=p+(X_0-p)\prod_{j=1}^{3}(1-U_j).}
\]

The implementation clamps the result to [0,1]. Under the stated ranges the expression already lies in [0,1], so the clamp does not change it.

The exact conditional kernel is therefore the distribution induced by the displayed independent uniform variables. More explicitly, for any measurable set \(A\subseteq[0,1]\),

\[
K_C(A\mid p)=
\frac{1}{0.2(0.4)^3}
\int_0^{0.2}\int_{0.3}^{0.7}\int_{0.3}^{0.7}\int_{0.3}^{0.7}
\mathbf 1\!\left[
p+(x-p)\prod_{j=1}^{3}(1-u_j)\in A
\right]
\,du_3\,du_2\,du_1\,dx.
\]

This is an exact kernel specification; it does not assume a Gaussian approximation.

Because \(E[X_0]=0.1\), and each \(E[1-U_j]=0.5\),

\[
\boxed{E[X_3\mid p]=p+(0.1-p)(0.5)^3
=\frac{7}{8}p+\frac{1}{80}.}
\]

For \(p=0\), the code skips teaching and leaves the child's coordinate at zero. Thus the full conditional expectation is piecewise:

\[
E[S_{c,i}\mid S_{p,i}=p]=
\begin{cases}
0,&p=0,\\
\frac78p+\frac1{80},&p>0.
\end{cases}
\]

**C-full** also copies the parent's concepts exactly by set update:

\[
C_c=C_p.
\]

**C-no-memory** does not copy concepts:

\[
C_c=\varnothing.
\]

Its skill channel is the same as C-full.

### 2.4 Mode C-low-effort

For any parent skill \(p>0\), the implementation draws \(X_0\sim\operatorname{Uniform}(0,0.2)\) and performs one update with \(U\sim\operatorname{Uniform}(0.1,0.4)\):

\[
X_1=p+(X_0-p)(1-U).
\]

For measurable \(A\subseteq[0,1]\), the exact conditional kernel is

\[
K_{low}(A\mid p)=
\frac{1}{0.2(0.3)}
\int_0^{0.2}\int_{0.1}^{0.4}
\mathbf 1\!\left[p+(x-p)(1-u)\in A\right]du\,dx.
\]

Since \(E[1-U]=0.75\),

\[
\boxed{E[X_1\mid p]=p+0.75(0.1-p)=\frac14p+\frac3{40}.}
\]

For \(p=0\), the code leaves the child coordinate at zero. The mode also copies concepts exactly:

\[
C_c=C_p.
\]

### 2.5 Summary of source-derived GAL 1.0 channels

| Mode | Skill inheritance | Concept inheritance |
|---|---|---|
| A | zero child skill | empty child set |
| B-copy | exact copy | exact copy |
| C-full | 3 stochastic teaching updates | exact copy |
| C-no-memory | same 3-update skill channel | no copy |
| C-low-effort | 1 stochastic teaching update | exact copy |

These are implementation facts for a fresh child at the inheritance step. They do not establish which mode carries more information about a latent truth or produces better future decisions.

### 2.6 Important GAL 1.0 distinction: concept identifiers are not ground-truth labels

The environment uses five rewarded concept identifiers: `concept_42`, `concept_108`, `concept_7`, `concept_99`, and `concept_314`. Independent learning samples identifiers from `concept_1` through `concept_1000`. The source does not define a probability distribution over semantic truth or a mapping from every concept identifier to a latent proposition.

Consequently, exact set copying proves identity of the stored identifiers at inheritance; it does not prove semantic correctness or quantify information about environmental truth.

---

## 3. GAL 2.0: inheritance channels

GAL 2.0 has two distinct mechanisms: evidence-gated capability inheritance and context-adaptive capability inheritance. Memory-record transfer is a shared additional operation.

### 3.1 Basic evidence-gated capability channel

For each parent capability \(c\):

- If \(c.verified=\text{False}\), the capability is not transferred.
- If \(c.verified=\text{True}\), the child receives a capability with the same name, proficiency, confidence, evidence list contents, prerequisites, context tags, failure conditions, and version.
- The child's `verified` flag is reset to false.
- The parent's lineage tuple is extended by the parent agent identifier.

For a transferred capability, write its non-lineage payload as

\[
Z=(p,q,E,R,T,F,v).
\]

The basic capability channel is a deterministic gated map:

\[
K_{basic}(z'\mid z)=
\begin{cases}
\delta_{T_{basic}(z)}(z'),&verified(z)=1,\\
\delta_{\bot}(z'),&verified(z)=0,
\end{cases}
\]

where \(\bot\) denotes absence of that capability in the child, and \(T_{basic}\) copies the payload while setting child verification to false and appending lineage metadata.

This is not a probabilistic belief update. It is a deterministic transfer conditioned on a Boolean verification gate.

### 3.2 Verified memory-record channel

The memory store transfers only records whose `verified` field is true. Each copied record preserves:

- kind;
- content dictionary (copied as a dictionary);
- source agent;
- original generation;
- tags;
- verified status.

It changes the custodian to the child agent and appends the source agent identifier to lineage.

For a record \(r\), the channel is therefore

\[
T_{mem}(r)=
( kind,content,source,generation,tags,verified,
custodian=child,lineage\mathbin{+!!+}(source)).
\]

Unverified records are omitted. The source code does not deduplicate records or calculate semantic equivalence. This is a deterministic filter-and-copy operation, not evidence that the memory's content is true.

### 3.3 Adaptive capability channel

The adaptive mechanism first rejects unverified parent capabilities. For verified capabilities, it calculates Jaccard similarity between the parent's context tags \(A\) and the child's requested context tags \(B\):

\[
J(A,B)=
\begin{cases}
\frac{|A\cap B|}{|A\cup B|},&A\cup B\ne\varnothing,\\
0,&\text{otherwise}.
\end{cases}
\]

The default policy has threshold \(\tau=0.25\), prior proficiency \(p_0=0.5\), and recalibration strength \(\lambda=0.5\).

If \(J(A,B)<\tau\), the capability is rejected. Otherwise:

\[
w=J(A,B)(1-\lambda)
\]

and

\[
\boxed{p'=p_0+w(p-p_0).}
\]

Under the default policy:

\[
p'=0.5+0.5J(A,B)(p-0.5).
\]

The child capability has confidence 0, empty evidence, child context tags, incremented version, and verification false. Prerequisites and failure conditions are copied. Lineage is extended with the parent identifier by the caller.

The operation is deterministic given the parent capability and child context. Jaccard similarity is a similarity of declared labels; the implementation explicitly does not establish semantic similarity.

### 3.4 GAL 2.0 training and evaluation are not inheritance

The agent's training attempt samples a Bernoulli outcome with

\[
\Pr(success\mid task,capability)
=\operatorname{clip}(p-0.45d+0.25,0.02,0.98).
\]

It appends evidence and creates episodic memory on every attempt, and semantic/procedural memory on success. Capability proficiency is recomputed as the empirical mean of the stored Boolean success outcomes. Confidence is set to \(n/(n+10)\).

This is a specified synthetic outcome generator, not a learned likelihood model of real-world task competence. Evaluation uses a separate RNG and does not mutate proficiency, evidence, or memory.

Therefore, a future information-theoretic analysis must distinguish:
1. the inheritance channel;
2. new training observations;
3. the synthetic success-generation model;
4. the verification decision based on holdout outcomes.

Combining these into one undifferentiated “knowledge transfer” channel would obscure the causal mechanism.

---

## 4. What exact information quantities are currently identifiable?

From source code alone, we can identify:

- deterministic equality/copy operations;
- stochastic skill-transfer kernels for GAL 1.0;
- exact conditional expectations for GAL 1.0 skill transfer;
- deterministic verification gates and context-recalibration maps in GAL 2.0;
- the synthetic Bernoulli success probability conditional on a given capability proficiency and task difficulty.

We cannot identify from source code alone:

- \(I(X;M)\) for semantic truth \(X\);
- the entropy of a population's inherited memory distribution;
- the mutual information between a capability record and real-world competence;
- whether stored concept labels are true, useful, or causally explanatory;
- the empirical reliability of the synthetic task model outside its own stipulated generator.

These require explicit random variables, source distributions, and a declared interpretation of ground truth.

### A safe exact result

For GAL 1.0 B-copy, if the source variable is defined to be the complete parent represented state \(X=M_p\), then the inheritance output is exactly \(M_c=X\). Thus

\[
I(X;M_c)=H(X).
\]

This is an identity-copy result under that particular source definition. It is not a claim about information concerning external truth. If the parent state is deterministic across the population, then \(H(X)=0\) and the mutual information is zero despite perfect copying.

Likewise, for GAL 2.0 basic inheritance, the payload of a transferred verified capability is copied exactly conditional on passing the verification gate. Mutual information cannot be evaluated without a distribution over capability states and verification status.

---

## 5. Exact next-step analysis plan

The next rigorous step is not to invent a distribution. It is to define a small, explicit finite source model as a **separate analytic benchmark**, then calculate each channel's mutual information under that declared model.

Recommended benchmark design:

1. Define a binary latent task-relevant fact \(X\in\{0,1\}\) with a declared prior \(P(X=1)=\pi\).
2. Define an explicit parent memory representation \(M_p\) and its likelihood \(P(M_p\mid X)\). Keep this likelihood separate from the implementation-derived transfer channel.
3. Apply the exact transfer kernel derived above to obtain \(P(M_c\mid M_p)\).
4. Calculate the induced joint distribution \(P(X,M_c)\), then \(I(X;M_p)\) and \(I(X;M_c)\) in bits.
5. For new child observations \(E\), define \(P(E\mid X,M_p)\) and calculate the conditional information contribution \(I(X;E\mid M_p)\).
6. Report sensitivity over explicit priors and likelihood parameters; do not select parameters because they produce a preferred result.
7. Keep the benchmark analytical and separate from the existing confirmatory experiments. Any later experiment must have a preregistered protocol and independent audit.

For GAL 1.0, a binary abstraction of one of the five task-associated concepts is a possible benchmark, but it must not be confused with the implementation's broad `concept_1..concept_1000` vocabulary.

For GAL 2.0, define the latent fact independently of `verified`; verification is a software status flag, not ground truth.

---

## 6. Falsifiable claims and non-claims

**Supported by source inspection and algebra**
- GAL 1.0 B-copy copies represented skill values and concept identifiers exactly at inheritance.
- GAL 1.0 C-full and C-no-memory use the same three-step skill teaching rule; they differ in concept transfer.
- GAL 1.0 C-low-effort uses one lower-rate teaching step and copies concepts.
- GAL 2.0 basic inheritance transfers only verified capabilities and resets child verification.
- GAL 2.0 adaptive transfer uses Jaccard similarity and the stated linear recalibration equation.
- GAL 2.0 memory inheritance filters for verified records.

**Not established**
- Any ranking of the modes by mutual information about truth.
- Any claim that a copied verified record is objectively true.
- Any claim that a higher proficiency score means more Shannon information.
- Any claim that the stochastic skill channel is an optimal or biologically realistic teaching process.
- Any claim that either implementation obeys a physical conservation law.

## 7. References

The data-processing inequality and its Markov-chain condition are standard results in information theory. See:

1. T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley (2006), Chapter 2; [Wiley chapter page](https://doi.org/10.1002/0471200611.ch2).
2. Cover and Thomas, Chapter 2 excerpt on the data-processing inequality: [PDF excerpt](https://sgfin.github.io/files/notes/Cover_and_Thomas_ch2_entropy.pdf).

The source-derived formulas in Sections 2 and 3 are algebraic consequences of the repository code, not claims taken from these references.
