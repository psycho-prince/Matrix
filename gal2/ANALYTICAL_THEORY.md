# GAL 2.0 — Analytical theory of knowledge inheritance

**Status:** formal model and proved propositions; no simulation or empirical claim is made here.

## 1. Knowledge state

Let the finite hypothesis space be \(\Theta=\{\theta_1,\ldots,\theta_m\}\).
An agent's epistemic state is a probability distribution \(\pi(\theta)\)
over hypotheses. Uncertainty is explicit: knowledge is not a Boolean flag.

An observation \(y\) has likelihood \(L(y\mid\theta)\). Bayesian acquisition is

\[
\pi'(\theta)=
\frac{L(y\mid\theta)\pi(\theta)}
{\sum_{\vartheta\in\Theta}L(y\mid\vartheta)\pi(\vartheta)}.
\]

Independent observations multiply likelihoods. Conflicting evidence changes
relative posterior mass; it is not silently overwritten.

## 2. Inheritance operator

Let \(\pi_0\) be the successor's base prior and \(\pi_p\) the parent's
posterior built from evidence eligible for transfer. Define

\[
\boxed{\pi_c=(1-r)\pi_0+r\pi_p,\quad r\in[0,1].}
\]

This linear opinion pool is normalized because it is a convex combination of
normalized distributions. \(r=0\) means no inheritance; \(r=1\) means full
transfer. Intermediate values retain partial parental information while
preserving base-prior support. This is an explicit modelling choice, not a
claim that biological inheritance literally follows this law.

## 3. Verification as a Bayes-factor requirement

For a claim \(H\), prior probability \(p\), and evidence Bayes factor
\(B=P(y\mid H)/P(y\mid\neg H)\), posterior odds satisfy

\[
\frac{P(H\mid y)}{P(\neg H\mid y)}
=B\frac{p}{1-p}.
\]

To require posterior confidence at least \(\tau\in(0,1)\), evidence must satisfy

\[
\boxed{B\geq\frac{\tau}{1-\tau}\frac{1-p}{p}.}
\]

This makes verification thresholds depend on prior odds and evidence strength,
rather than an arbitrary fixed score. Evidence with \(B=1\) adds no confidence.

## 4. Adaptation under environmental shift

Let \(P\) be the source environment's observation distribution and \(Q\)
the successor environment's distribution. Total variation distance is

\[
d_{TV}(P,Q)=\sup_A|P(A)-Q(A)|
=\frac12\sum_x|P(x)-Q(x)|
\]

on a finite space.

For any fixed decision rule \(f\) and loss \(\ell\in[0,1]\),

\[
|R_P(f)-R_Q(f)|\leq d_{TV}(P,Q).
\]

**Proof.** For bounded measurable \(g\in[0,1]\), the variational
characterization of total variation gives
\(|\mathbb E_Pg-\mathbb E_Qg|\leq d_{TV}(P,Q)\). Set
\(g(x)=\ell(f(x),x)\). \(\square\)

### Proposition: sufficient condition for inherited advantage to survive a shift

Suppose inherited rule \(f_I\) has source-domain risk advantage \(G\geq0\)
over baseline \(f_B\):

\[
R_P(f_B)-R_P(f_I)=G.
\]

Then in the successor environment,

\[
\boxed{R_Q(f_B)-R_Q(f_I)\geq G-2d_{TV}(P,Q).}
\]

**Proof.** Apply the bounded-loss inequality to each rule:
\(R_Q(f_B)\geq R_P(f_B)-d_{TV}\) and
\(R_Q(f_I)\leq R_P(f_I)+d_{TV}\). Subtract. \(\square\)

Thus if \(G>2d_{TV}(P,Q)\), the inherited rule is guaranteed to retain
a positive risk advantage. If the shift is larger, this bound is
uninformative; it does not prove inheritance is harmful.

## 5. What this establishes

The propositions establish Bayesian evidence accumulation, posterior-odds
verification, a normalized inheritance operator, and a distribution-shift
bound for bounded losses. They do not establish that a real agent can discover
a correct likelihood model, estimate environmental distributions, construct a
useful hypothesis space, or achieve positive source-domain gain \(G\).
Those remain empirical questions requiring a real learner and externally
grounded tasks.

## 6. Exact implementation

The analytical_theory.py module implements rational-probability updates,
inheritance, Bayes-factor thresholds, total variation, and the shift bound
using exact fractions. Tests are algebraic invariant checks, not sampled trials.
