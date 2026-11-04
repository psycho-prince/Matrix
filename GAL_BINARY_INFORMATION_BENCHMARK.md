# GAL Binary Information-Channel Benchmark

**Classification:** analytical toy benchmark with explicit assumptions. It is not a measurement of either GAL implementation, not a foundation-model performance result, and not evidence that semantic knowledge is conserved.

## Purpose

Test the information-accounting logic with the smallest transparent probabilistic model before attempting continuous skill-channel information estimates.

## Model

- Latent binary target: \(X\in\{0,1\}\), with \(P(X=1)=\pi\).
- Parent memory: \(M=X\oplus N\), where \(N\sim\operatorname{Bernoulli}(\epsilon)\) independently of \(X\). Thus the parent memory may already contain source/encoding error.
- Inheritance gate: \(G\sim\operatorname{Bernoulli}(q)\), assumed independent of \((X,M)\) for this benchmark.
- Child memory: \(Y=M\) if \(G=1\), and \(Y=\bot\) if \(G=0\). The missing symbol \(\bot\) is observable.

The assumption that \(G\) is independent is deliberate. GAL 2.0 verification is based on evidence and may be correlated with capability correctness; therefore \(q\) is a sensitivity parameter here, not an empirically estimated verification probability.

## Exact result

Because the transfer gate is independent and its outcome is observable,

\[
I(X;Y)=qI(X;M).
\]

For a uniform source, \(\pi=1/2\), the parent memory is a binary symmetric channel and

\[
I(X;M)=1-h_2(\epsilon),
\]

where

\[
h_2(\epsilon)=-\epsilon\log_2\epsilon-(1-\epsilon)\log_2(1-\epsilon).
\]

Hence

\[
\boxed{I(X;Y)=q[1-h_2(\epsilon)]}.
\]

This is an exact calculation under the benchmark assumptions. It is consistent with DPI: \(0\le q\le1\) implies \(I(X;Y)\le I(X;M)\).

## Sensitivity results

For \(\pi=0.5\), the following values are exact to the displayed precision.

| Source error \(\epsilon\) | Parent \(I(X;M)\) bits | Child, \(q=0.5\) bits | Child, \(q=0.25\) bits |
|---:|---:|---:|---:|
| 0.00 | 1.000000 | 0.500000 | 0.250000 |
| 0.05 | 0.713603 | 0.356802 | 0.178401 |
| 0.10 | 0.531004 | 0.265502 | 0.132751 |
| 0.20 | 0.278072 | 0.139036 | 0.069518 |
| 0.30 | 0.118709 | 0.059355 | 0.029677 |
| 0.40 | 0.029049 | 0.014525 | 0.007262 |
| 0.50 | 0.000000 | 0.000000 | 0.000000 |

## Interpretation and mapping limits

- **GAL 1.0 B-copy / exact concept-set copy:** analogous to identity transfer of the *stored representation*. This benchmark additionally models possible source-to-parent encoding error; that error is not estimated from GAL 1.0 code.
- **GAL 1.0 C-no-memory:** the concept-transfer component resembles an erasure channel for the concept set. The continuous skill teaching channel is not represented by this binary benchmark.
- **GAL 2.0 basic verified capability transfer:** resembles gated payload copying, but the independence assumption for \(G\) is not established by the implementation. A realistic model must estimate \(P(G\mid X,M,\text{evidence})\), not substitute an arbitrary constant.
- **GAL 2.0 adaptive inheritance:** deterministic recalibration is not automatically an erasure or noisy channel. If its map is one-to-one over the relevant state support, it preserves information in the ideal mathematical model; if thresholding or quantization collapses states, it may lose information. This requires an explicit source distribution.

The benchmark does **not** rank the five GAL 1.0 modes or claim GAL 2.0 verification is effective. It tests a narrow mathematical identity and provides executable regression checks.

## Reproducibility

Run:

```bash
python analysis/information_channel_benchmark.py --self-test
python analysis/information_channel_benchmark.py --prior 0.5 --source-error 0.1 --transfer-probability 0.5
```

The script uses only the Python standard library. It computes mutual information from the joint distribution directly rather than hardcoding the uniform-source formula.

## Independent model review

The derivation was checked as a mathematical consistency review by GPT-6. This is not an independent external-model replication, and no claim is made that a second foundation model was queried. The executable assertions check boundary cases, the binary-entropy symmetry, the exact erasure identity, and DPI over a declared parameter grid.

## Next test required

To test the real GAL 1.0 continuous teaching kernels, estimate or derive the output distributions conditional on a declared latent source and compute mutual information by validated numerical integration. For GAL 2.0, model verification as evidence-dependent selection and include false-positive/false-negative rates. Neither analysis should be called an implementation result until the source-to-target likelihoods are specified and independently checked.
