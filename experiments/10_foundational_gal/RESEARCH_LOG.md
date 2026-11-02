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


### Automated tests green — 2026-11-02
- Corrected EWC/invariant workflow run `41427307866` completed successfully.
- The `Run automated research invariant tests` step completed successfully, followed by the extended Split Digits study and artifact upload.
- The separate existing deterministic benchmark workflow `41427307788` also completed successfully.
- This establishes that the current automated test suite executes successfully; it does not establish the foundational GAL hypothesis.

### Native GAL pilot launched — 2026-11-02
- Added `experiments/10_foundational_gal/run_native_gal_pilot.py`.
- Added `.github/workflows/native-gal-pilot.yml`.
- Pilot configuration: 5 universe seeds × 20 agents per generation × 4 generations × all five original inheritance modes.
- The runner uses the original `Agent`, `Environment`, `inherit`, `develop`, `learn_independently`, and `work` methods. It adds observation around task attempts and records raw per-agent state, parent/child inheritance snapshots, task-level success, population skill summaries, concept counts, and generation performance.
- Built-in fail-closed mechanism checks cover mode A no-inheritance, exact B-copy transfer, C-no-memory concept exclusion, and skill bounds.
- Workflow run: `41427799864`; job `125218543631`.
- At the time of this entry the pilot workflow was still installing dependencies; no pilot outcome or raw-data audit is claimed yet.
- Confirmatory 100-seed run remains blocked until pilot completion and inspection.


### Native GAL pilot failure and code correction — 2026-11-02
- Pilot run `41429686327` completed with failure; job `125224855484`.
- Dependency installation and all 14 automated invariant tests succeeded.
- Pilot execution failed while building the generation-level mean-skill summary: the code indexed an `Agent` instance as if it were a dictionary (`a["skills"][skill]`), raising `TypeError: 'Agent' object is not subscriptable`.
- No pilot artifact was uploaded; this run produced no scientific result and is retained as a failed execution.
- Corrected the summary to read the actual `Agent.skills` attribute: `agent.skills[skill]`.
- Correction commit: `9a4075f55de67e01c248862b6706163766710798`.
- The correction triggers a new pilot workflow run. Confirmatory 100-seed execution remains blocked until the new pilot completes and its raw data/mechanism checks are audited.


### Native GAL pilot failure and correction — 2026-11-02 (continued)
- Pilot run `41429686327` completed with failure; job `125224855484`.
- The 14 automated invariant tests passed in that job. The pilot then failed while constructing the generation summary: the aggregation indexed live `Agent` objects as dictionaries (`a["skills"]`), raising `TypeError: 'Agent' object is not subscriptable`. The pilot did not upload raw data; no pilot outcome is available.
- Source review also found that the pilot identity included the inheritance mode. Since the original Agent derives its lifetime RNG seed from identity, this accidentally gave different random streams to each mode and violated the paired-seed design.
- Corrected the skill aggregation to read `Agent.skills` and removed the mode label from agent identity so matching seed/generation/agent indices receive the same deterministic lifetime RNG stream across modes.
- Corrective code commit: `e3bda5cf9a4ccffc9b401c5cd1a8f5c415dad696`.
- This is a code correction, not a successful pilot. Await the newly triggered workflow and audit its raw outputs before any confirmatory run.
