# GAL 2.0 Prioritized Research and Engineering Roadmap

This roadmap is based on the source-level audit of commit `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`. It is a proposed plan, not a record of implemented changes.

## P0 — Protect research integrity

1. Preserve current GAL 2.0 source, raw results, workflow artifacts, and historical claims unchanged.
2. Keep future implementation work on a new branch and versioned benchmark.
3. Add structured provenance to every verification event.
4. Deprecate tag-only memory verification from any trusted inheritance path.
5. Add immutable/deep-copied memory payloads and enforce generation ordering in low-level transfer APIs.

**Exit criteria:** no memory can become trusted through tag matching alone; no mutable payload can silently cross generation boundaries; invalid temporal transfer is rejected.

## P1 — Make memory causally relevant

1. Define a versioned memory-using task policy.
2. Require task execution to retrieve relevant records and expose retrieval/action traces.
3. Separate episodic recall, semantic rule use, and procedural policy execution.
4. Add ablations where each memory channel is disabled independently.
5. Keep the current Bernoulli executor as a named synthetic control, not as the new policy.

**Exit criteria:** intervention on inherited memory changes policy behaviour in a traceable way, and memory-enabled agents outperform matched controls on pre-specified held-out tasks.

## P2 — Build a defensible benchmark

1. Create an explicit finite world with ground-truth rules.
2. Generate training and test tasks from disjoint compositions/surface forms.
3. Include distribution shift and contradictory/corrupted inherited information.
4. Compare no transfer, capability-only, each memory channel, combined transfer, independent learning, and oracle upper bound.
5. Match data, compute, model access, and interaction budgets.
6. Pre-register primary endpoint, hypotheses, stopping rules, and exclusion rules.

**Exit criteria:** paired-seed held-out performance and uncertainty estimates can be independently recomputed from raw traces.

## P3 — Measurement and statistical quality

1. Replace the confidence count heuristic with calibrated probability estimates or rename it as evidence volume.
2. Report Brier score, log loss, reliability diagrams, false-discovery rate, precision/recall, and calibration by generation.
3. Report effect sizes and confidence intervals, not only p-values.
4. Use hierarchical/paired analysis appropriate to tasks nested within agents, seeds, and generations.
5. Correct for multiple comparisons and report every planned contrast.
6. Separate transmission, retention, correctness, task utility, and cost metrics.

**Exit criteria:** results are robust to pre-specified alternative analyses and an independent auditor can reproduce them.

## P4 — Reproducibility and CI

1. Add a pinned lockfile for the GAL 2.0 package and a separate environment for legacy/root experiments.
2. Add CI for the root test suite or explicitly document why it is excluded.
3. Archive task manifests, configurations, dependency manifests, raw traces, and SHA-256 checksums.
4. Add a clean-checkout reproduction workflow.
5. Add CI checks for memory immutability, provenance, generation monotonicity, context filtering, and leakage.
6. Keep LLM prototype evaluation separate and record model/provider/version, prompts, decoding parameters, and response traces.

**Exit criteria:** an independent clean environment can reproduce the same report schema and metrics within declared tolerances.

## P5 — External validation and claims discipline

1. Invite an independent researcher to review the protocol before confirmatory runs.
2. Publish code, preregistration, task manifests, raw outputs, and analysis scripts.
3. Replicate with a second agent implementation or model family.
4. Keep all claims bounded to the operational benchmark.
5. Do not claim AGI, consciousness, biological evolution, or physical conservation without entirely separate evidence and operational definitions.

## Suggested release gates

| Release | Minimum requirement |
|---|---|
| GAL 2.0.x | Existing mechanism and software invariants stable |
| GAL 2.1 experimental | Memory-mediated action path and trace logging |
| GAL 2.2 benchmark | Matched-budget baselines and held-out rule tasks |
| GAL 2.3 confirmatory | Preregistered, multi-seed study with independent raw-data audit |
| Research release | Reproducible external replication and appropriately scoped claims |

## Immediate next action

Create `research/gal-2.1-memory-grounded-learning` from the reviewed GAL 2.0 commit only after the audit is accepted. Implement the memory-use policy there. Do not merge or rewrite the original branch's results.
