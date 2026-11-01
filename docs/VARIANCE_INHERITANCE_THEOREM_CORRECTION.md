# Variance-preserving inheritance: corrected statement

The implementation in `permuted_mnist_continual.py` uses, for weight tensors,
`W_child = f W_parent + sqrt(1-f^2) Xi`, where `Xi` is independently sampled
Gaussian noise with a fixed He-style variance. Bias tensors are instead multiplied
by `f`, and the complete parameter vector is subsequently projected onto an
L2-norm ball of radius `capacity`.

## Proposition (unprojected weight-tensor second moment)

Let (W) be a fixed parent weight tensor, let (fin[0,1]), and let
(Xi) be independent of (W), with (E[Xi]=0) and
(E[|Xi|_F^2]=sigma_Xi^2). Define
[
W' = fW + sqrt{1-f^2},Xi.
]
Then
[
E[|W'|_F^2mid W]
=f^2|W|_F^2+(1-f^2)sigma_Xi^2.
]
**Proof.** Expand the squared Frobenius norm:
[
|W'|_F^2=f^2|W|_F^2
+2fsqrt{1-f^2}langle W,Xiangle
+(1-f^2)|Xi|_F^2.
]
Taking conditional expectation, independence and zero-mean noise make the cross
term zero, yielding the stated identity. (square)

A consequence is that the expected squared norm is preserved only when
(sigma_Xi^2=|W|_F^2), or at the endpoints where the noise coefficient
vanishes. This is a conditional expectation statement, not pathwise conservation.

## What the current code does not prove

1. The noise variance is initialized using fan-in/He scaling. It is not calibrated
   to the realized parent tensor's squared norm. Therefore the equality condition
   above is not generally guaranteed.
2. Biases are scaled by (f) with no replacement noise; their squared norms
   shrink by (f^2).
3. The post-inheritance capacity projection rescales all tensors whenever the
   joint parameter norm exceeds the capacity. This projection can only further
   alter the second moment and generally destroys any pre-projection equality.
4. Therefore the phrase "conserves total parameter energy" and "Theorem 2"
   are withdrawn for the current implementation.

## Correct claim

The code implements a **variance-inspired stochastic weight perturbation rule**
that combines parent weights with independent initialization-scale noise, followed
by a global norm projection. It may preserve or alter parameter scale depending
on the parent norm, fan-in, bias magnitude, retention coefficient, and capacity.
Any empirical claim about stability or plasticity must be measured; it does not
follow from the proposition.
