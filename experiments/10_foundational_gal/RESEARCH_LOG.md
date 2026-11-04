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


### Native GAL mechanism pilot passed and raw-data audit — 2026-11-02
- Corrected pilot workflow run `41493595467` completed successfully on commit `e3bda5cf9a4ccffc9b401c5cd1a8f5c415dad696`.
- Job: `125442638737`; all steps passed, including the 14 automated invariant tests, pilot execution, and artifact upload.
- Artifact: `native-gal-mechanism-pilot-41493595467`, artifact ID `13165401702`, size 1,365,652 bytes, SHA-256 `b42669724acbc9edbb2b011f0ac88fd9e0f68bdd98654f0f8ea3db093b1c0299`.
- Configuration: 5 paired universe seeds × 20 agents/generation × 4 generations × 5 original modes. Raw archive contains 25 per-mode/per-seed JSON files, 100 generation records, 2,000 agent-generation snapshots, and 1,500 inheritance events.
- Structural audit passed: every generation has 20 agents; each agent has 50 work attempts; each generation has 1,000 task attempts; all five task types are represented; generation 1 has no inheritance events; later generations have exactly 20 parent-child events. No structural errors were found.
- Pairing correction verified in source: mode-independent agent identities ensure corresponding seed/generation/agent indices use identical deterministic lifetime RNG streams across modes. The Agent implementation uses a separate inheritance RNG stream, so teaching-mode random draws do not consume lifetime task/learning draws.
- Mechanism audit across 300 inheritance events per mode:
  - A: all 300 children unchanged by inheritance.
  - B-copy: exact skills and concepts in all 300 events.
  - C-full: concepts transferred in all 300; skills not exact copies, consistent with teaching updates.
  - C-no-memory: no parent concepts retained in all 300; skills updated through teaching.
  - C-low-effort: concepts transferred in all 300; skills updated through the one-iteration teaching path.
  - Skill bounds remained within [0, 1] in all modes.
- Pilot descriptive generation-4 mean success: A 0.0420; B-copy 0.4148; C-full 0.3886; C-no-memory 0.3266; C-low-effort 0.2634. Paired seed-level generation-4 differences vs A: B-copy +0.3728; C-full +0.3466; C-no-memory +0.2846; C-low-effort +0.2214.
- These are pilot-scale descriptive outcomes only (5 seeds, 20 agents, 4 generations); no confirmatory inference or hypothesis claim is made from them.
- Artifact structural audit command executed against downloaded ZIP; checks returned 25 files, 100 generation records, 2,000 agent snapshots, 1,500 inheritance events, and zero validation errors.
- Gate decision: pilot mechanism and data-capture checks passed. The pre-registered 100-seed × 100-agent × 10-generation confirmatory native GAL study may now proceed. The pilot artifact and prior failed runs remain immutable.


### Foundational native GAL confirmatory run completed — 2026-11-02
- Workflow run: `41497968447`; job `125457787981`; conclusion success.
- Source commit: `947ef554e69a3ae8e04b6912b1910dae7b188f02`.
- Configuration: 100 paired universe seeds (0–99), 100 agents/generation, 10 generations, five original inheritance modes. 500 seed×mode runs and 5,000 generation records.
- Artifact: `native-gal-confirmatory-41497968447`, artifact ID `13168006474`, 413,865,175 bytes; uploaded ZIP SHA-256 `2586d5128f98b67084d6be19d51061cdfff68fd8d8a0fd777c6b46d93ede0828`. Archive contains five output files, including compressed raw JSONL, summary, generation CSV, validity audit and raw-data checksum.
- Reported validity audit: 500/500 seed-mode runs; 5,000/5,000 generation records; 90,000 inheritance events per mode; no reported audit errors. Every mode recorded 100 agents/generation, 50 task attempts/agent/generation, all five task types and skill values within [0,1].
- Mechanism audit: A unchanged child state 90,000/90,000; B-copy exact skill and concept transfer 90,000/90,000; C-full concept transfer 90,000/90,000 with teaching-style non-exact skills; C-no-memory parent concept transfer 0/90,000; C-low-effort concept transfer 90,000/90,000.
- Generation-10 mean task success: A 0.041434; B-copy 0.884194; C-full 0.846732; C-no-memory 0.815040; C-low-effort 0.365926.
- Pre-registered paired seed contrasts (treatment minus control):
  - B-copy − A: +0.842760; 95% paired bootstrap CI [0.841444, 0.844062]; paired t=1261.44; p=5.01e-210; Holm p=2.51e-209; 100/100 wins.
  - C-full − A: +0.805298; CI [0.803582, 0.807000]; t=925.50; p=1.03e-196; Holm p=4.12e-196; 100/100 wins.
  - C-no-memory − A: +0.773606; CI [0.771770, 0.775474]; t=807.17; p=7.84e-191; Holm p=2.35e-190; 100/100 wins.
  - C-low-effort − A: +0.324492; CI [0.322002, 0.327030]; t=250.55; p=1.45e-140; Holm p=2.91e-140; 100/100 wins.
  - B-copy − C-full: +0.037462; CI [0.036366, 0.038566]; t=65.93; p=1.31e-83; Holm p=1.31e-83; 100/100 wins.
  - All five Holm-adjusted paired t-test contrasts are below 0.05; Wilcoxon sensitivity p-values are also reported in the workflow log.
- Interpretation: Strong evidence that inheritance as implemented in this specific handcrafted, stationary GAL environment improves task performance over mode A, with direct state copying outperforming teaching-style C-full. This does not establish biological evolution, general intelligence, consciousness, or transfer to external environments.
- Audit limitation: workflow validity audit is a program-generated check. A separate independent parse of the 413.9 MB artifact archive and verification of its embedded raw SHA-256 remains pending; do not label this an independently reproduced analysis until that check is completed.
- Preserve artifact and workflow logs immutably. Do not rerun or overwrite this confirmatory result; follow-up work must use a new protocol/run ID.


### Foundational native GAL confirmatory run completed — 2026-11-02
- Workflow run `41497968447` completed successfully; commit `947ef554e69a3ae8e04b6912b1910dae7b188f02`.
- Artifact: `native-gal-confirmatory-41497968447`, artifact ID `13168006474`, size 413,865,175 bytes, GitHub artifact ZIP SHA-256 `2586d5128f98b67084d6be19d51061cdfff68fd8d8a0fd777c6b46d93ede0828`.
- Configuration: 100 paired seeds × 100 agents/generation × 10 generations × 5 modes. 500 seed-mode runs, 5,000 generation records, 500,000 agent-generation records, and 90,000 inheritance events per mode (450,000 total). Validity audit observed 500/500 runs and 5,000/5,000 generations; errors list empty.
- Generation-10 mean task success: A 0.041434; B-copy 0.884194; C-full 0.846732; C-no-memory 0.815040; C-low-effort 0.365926.
- Pre-registered paired generation-10 contrasts (difference in success-rate units; all treatment wins 100/100; all Holm-adjusted paired t tests significant at .05):
  - B-copy − A: +0.842760; 95% paired bootstrap CI [0.841444, 0.844062]; t=1261.44; p=5.01e-210; Holm p=2.51e-209.
  - C-full − A: +0.805298; CI [0.803582, 0.807000]; t=925.50; p=1.03e-196; Holm p=4.12e-196.
  - C-no-memory − A: +0.773606; CI [0.771770, 0.775474]; t=807.17; p=7.84e-191; Holm p=2.35e-190.
  - C-low-effort − A: +0.324492; CI [0.322002, 0.327030]; t=250.55; p=1.45e-140; Holm p=2.91e-140.
  - B-copy − C-full: +0.037462; CI [0.036366, 0.038566]; t=65.93; p=1.31e-83; Holm p=1.31e-83.
- Mechanism audit: A unchanged child state 90,000/90,000; B-copy exact skill and concept copy 90,000/90,000; C-full exact concept transfer 90,000/90,000; C-no-memory parent concepts retained 0/90,000; C-low-effort concept transfer 90,000/90,000. No validity audit errors.
- Interpretation: strong evidence that the implemented inheritance mechanisms increase task success in this specific handcrafted, stationary symbolic GAL environment under matched exposure. B-copy is highest; teaching-style modes also exceed independent mode A. This does not establish biological evolution, consciousness, general intelligence, or performance in external/novel environments.
- Next required work: independent audit of the archived raw JSONL (including seed-level pairing and task-level denominators), inspect the actual Agent inheritance implementation and confirm all task-attempt attribution and cycle exposure semantics, then conduct a separately pre-registered novel-task/environment-shift test. The current runner's automatic validity audit is necessary but not sufficient scientific peer review.
