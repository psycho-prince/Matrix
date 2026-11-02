# GAL research activity log

This log is append-only by convention. Do not replace earlier entries; append a dated entry for every code change, execution, failure, correction, or protocol deviation.

## 2026-11-02 — EWC correction, invariant tests, foundational GAL protocol

### Historical run preserved
- Historical neural proxy run: GitHub Actions run `41416824440`.
- Historical source commit: `12baf9446a6fa08b9beb1c4d33c3ffc2517e8ea8`.
- Artifact ID: `13127368635`.
- Artifact SHA-256: `2f2a6c4f891122039fd37b837c29a8179e92fe7bac7733e448a087c29ee6bb32`.
- Immutable audit: `experiments/09_split_digits/RESULTS_AUDIT_2026-11-02.md`.
- The source, results and audit for this run have not been rewritten. Later code changes are new commits and new experiments.

### EWC implementation correction
- Updated `experiments/09_split_digits/run_extended.py`.
- EWC now stores a distinct diagonal Fisher estimate and matching parameter reference for every completed task.
- Future-task loss uses the sum of task-specific quadratic penalties:
  `L = L_current + (lambda/2) * sum_t sum_i F[t,i] * (theta[i] - theta_star[t,i])^2`.
- Fisher is estimated from per-example squared gradients on the corresponding task's training partition.
- This is task-wise diagonal EWC, not online EWC.
- Commit: `e01183f11fe628de7777b0ab85db992dd78488ab`.

### Automated invariant tests
- Added `experiments/09_split_digits/tests/test_research_invariants.py`.
- Covers task-specific EWC reference means, zero-Fisher penalty, parameter schema validation, replay memory budget and determinism, task masks, task-wise evaluation, forgetting calculation, exact-copy inheritance, teaching modes, and independent mode.
- Added the test step before benchmark execution in `.github/workflows/split-digits-extended.yml`.
- Test suite commit: `e8ffb3ca9f8f5f2b0166f82f2d7649bb32e5f922`.
- Floating-point assertion hardening commit: `eec8eee2dcdc8649000646200ffec8e99b1f6b03`.
- CI triggered from this branch commit. At log creation, check runs were still in progress:
  - Invariant-test + extended study: run `41427149216`.
  - Existing deterministic benchmark workflow: run `41427149177`.
- Do not call the tests passed until the check run reports success and the test step is completed.

### Foundational GAL protocol
- Added `experiments/10_foundational_gal/FOUNDATIONAL_VALIDATION_PROTOCOL.md`.
- It specifies the original symbolic `Agent` and `Environment`, five original inheritance modes, paired universe seeds, equal population/exposure, task-level measurements, mechanism checks, paired statistics, and staged novelty/volatility follow-ups.
- It is a pre-registration draft, not a completed experiment.
- Commit: `d1800614c3330cfaa15f3b4244922b9a546a1201`.

### Protocol clarification
- Added task-wise EWC specification to `experiments/09_split_digits/EXTENDED_PROTOCOL.md`.
- Commit: `bf3825b8d8d34fe9d1c6cf8fd363531cc44b7a77`.

### Current state / next gates
1. Await CI for invariant tests. Fix failures before interpreting any new neural benchmark.
2. After successful CI, run a new corrected EWC study with a new workflow run ID and artifact. Do not modify the historical 2026-11-02 results.
3. Review native GAL tests against every inheritance mode and environment semantics.
4. Review the foundational protocol with an implementation audit, then run a pilot (small seed count) only to verify mechanics and data capture.
5. Run the 100-seed confirmatory native GAL experiment only after the pilot and all validity checks pass.
6. Keep the neural continual-learning proxy and native Artificial Life results in separate experiment families.

## Research integrity requirements

- A workflow green check means the code executed; it does not itself establish the hypothesis.
- A passing unit test establishes only the tested invariant.
- A pilot is not a confirmatory experiment.
- Never overwrite raw artifacts or dated audit reports.
- Preserve failed runs and explain why they failed.
- No result is scientific evidence for foundational GAL unless it comes from the original GAL population/environment mechanisms and the pre-specified protocol.


### CI failure and correction — 2026-11-02
- First automated test attempt failed before tests ran because the EWC refactor introduced an indentation error in the GAL-CL branch of `run_extended.py`.
- Failed CI run: `41427149216`; job `125216400859`.
- Exact failure: `IndentationError: unexpected indent` at the `if method == "GAL-CL"` branch.
- The separate pre-existing deterministic benchmark workflow completed successfully: run `41427149177`. This did not validate the new EWC/test changes.
- Corrected indentation in commit `098edbc3f4bfa8c0bf70e303a922b0b17cad51e9`.
- New CI checks triggered for the correction:
  - invariant-test + extended study: run `41427307866`, queued at time of this entry.
  - deterministic benchmark: run `41427307788`, queued at time of this entry.
- This failure is retained in the record. Do not report the invariant suite as passing until run `41427307866` completes successfully.
