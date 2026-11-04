"""Exact finite-probability mathematics for GAL knowledge inheritance.
No simulation or Monte Carlo; all probability arithmetic is rational and exact.
"""
from __future__ import annotations
from fractions import Fraction
from typing import Mapping

Distribution = Mapping[str, Fraction]

def _validate_distribution(p: Distribution) -> None:
    if not p or any(v < 0 for v in p.values()) or sum(p.values(), Fraction(0)) != 1:
        raise ValueError("distribution must be non-empty, non-negative, and sum exactly to one")

def normalize(weights: Mapping[str, Fraction]) -> dict[str, Fraction]:
    if not weights or any(v < 0 for v in weights.values()):
        raise ValueError("weights must be non-empty and non-negative")
    total = sum(weights.values(), Fraction(0))
    if total == 0: raise ValueError("cannot normalize zero total weight")
    return {k:v/total for k,v in weights.items()}

def bayes_update(prior: Distribution, likelihood: Mapping[str, Fraction]) -> dict[str, Fraction]:
    _validate_distribution(prior)
    if set(prior) != set(likelihood): raise ValueError("prior and likelihood supports differ")
    if any(v < 0 or v > 1 for v in likelihood.values()): raise ValueError("likelihoods must lie in [0,1]")
    return normalize({h:prior[h]*likelihood[h] for h in prior})

def inherit_distribution(parent: Distribution, base: Distribution, retention: Fraction) -> dict[str,Fraction]:
    _validate_distribution(parent); _validate_distribution(base)
    if set(parent) != set(base): raise ValueError("parent and base supports differ")
    if not 0 <= retention <= 1: raise ValueError("retention must lie in [0,1]")
    return {h:(1-retention)*base[h]+retention*parent[h] for h in base}

def posterior_odds(prior_probability: Fraction, bayes_factor: Fraction) -> Fraction:
    if not 0 < prior_probability < 1 or bayes_factor < 0: raise ValueError("invalid prior or Bayes factor")
    return prior_probability/(1-prior_probability)*bayes_factor

def bayes_factor_for_confidence(prior_probability: Fraction, target_probability: Fraction) -> Fraction:
    if not 0 < prior_probability < 1 or not 0 < target_probability < 1: raise ValueError("probabilities must lie in (0,1)")
    return (target_probability/(1-target_probability))/(prior_probability/(1-prior_probability))

def total_variation(p: Distribution, q: Distribution) -> Fraction:
    _validate_distribution(p); _validate_distribution(q)
    if set(p) != set(q): raise ValueError("distributions must share support")
    return sum((abs(p[k]-q[k]) for k in p),Fraction(0))/2

def bounded_loss_shift_bound(source_risk_gain: Fraction, environment_tv: Fraction) -> Fraction:
    """For losses in [0,1], lower bound shifted-domain gain = G - 2 TV."""
    if source_risk_gain < 0 or not 0 <= environment_tv <= 1: raise ValueError("invalid gain or TV")
    return source_risk_gain-2*environment_tv

def verification_threshold(prior_probability: Fraction, target_probability: Fraction) -> Fraction:
    return bayes_factor_for_confidence(prior_probability,target_probability)
