# Mechanism-Level Testing Sprint

## Scope

This sprint adds tests against the current native inheritance implementations. It does not treat the abstract binary-channel benchmark as a proxy for either implementation.

## GAL 1.0 acceptance criteria

- A is a no-transfer control.
- B-copy transfers skill values and concept set exactly.
- C-full and C-no-memory use identical teaching draws for matched child identity/seed; only the concept-memory transfer differs.
- C-low-effort transfers concepts and its positive parent skill values move toward the parent under the current one-step update rule.
- Inheritance uses the isolated inheritance RNG and does not advance the lifetime RNG.
- Child inheritance does not mutate parent state.
- Current unknown-mode behavior is characterized as a no-op; this is flagged as a potential fail-closed/API-hardening issue, not endorsed behavior.

## GAL 2.0 acceptance criteria

- Basic inheritance transfers only verified parent capabilities and resets child verification.
- Only verified memory records are transferred; provenance and custodian are checked.
- Adaptive inheritance rejects unverified capabilities and below-threshold context matches.
- Recalibrated proficiency remains in [0,1], and inherited capabilities require child-side verification.
- Held-out evaluation is checked for task uniqueness and its state-isolation property.
- Training is checked to update evidence and memory.

## Test design and limitations

The tests use finite parameter grids and deterministic fixtures. They are property-style regression tests using pytest, not Hypothesis-generated tests. This avoids adding a new runtime dependency before the repository's dependency and CI policy is reviewed. Hypothesis is a suitable later extension for generated input spaces.

The tests characterize current behavior. They do not prove semantic correctness, calibration, causal knowledge transfer, or thermodynamic conservation. GAL 2.0's verification is a synthetic task-performance gate; it is not an external truth oracle.

## Execution status

Source-level test files added. Runtime execution and CI status must be reported separately and only after an actual test runner or workflow completes.
