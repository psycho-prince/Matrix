# Foundational GAL validation protocol (pre-registration draft)

**Status:** Design specification; not yet executed.
**Scope:** Original symbolic/population GAL model in `gal/agents/agent.py` and `gal/environment/world.py`.
**Not in scope:** Neural GAL-CL, EWC, replay, tool-calling agents, or replacement inheritance algorithms.

## 1. Foundational question

Does transferring acquired capabilities and/or semantic concepts from parents to successors cause cumulative improvement in population task performance across generations, beyond what equally exposed independent learners achieve?

The experiment tests a causal effect of generational inheritance in the current GAL model. It does not test consciousness, biological evolution, or general intelligence.

## 2. Existing model audited

- Individuals are instances of the repository's original `Agent`.
- Each individual has five scalar skills and a set of semantic concepts.
- The original `Environment` contains five tasks, each with a required skill, difficulty, and associated concept.
- Each generation develops, performs five independent-learning/work cycles, and attempts 50 tasks per individual.
- Each child currently receives one parent by index-matched pairing when population sizes are equal.
- Inheritance modes in the source: `A`, `B-copy`, `C-full`, `C-no-memory`, `C-low-effort`.
- Inheritance and lifetime RNG streams are separated. For identical seed, generation and identity, the lifetime stream is independent of inheritance mode; this supports paired stochastic comparisons, subject to tests.

## 3. Primary hypothesis and estimand

**H1:** At a fixed generation and equal individual learning/work exposure, inheritance conditions that transfer acquired state improve held-out task success relative to independent development (`A`).

Primary estimand:
`mean_seed(task_success_rate[mode, generation 10] - task_success_rate[A, generation 10])`.

Primary endpoint: generation-10 population mean task success rate, paired by universe seed.

Pre-specified contrasts:
1. B-copy vs A: effect of direct copying of skills and concepts.
2. C-full vs A: effect of teaching-style skill transfer plus concept transfer.
3. C-no-memory vs A: effect of teaching-style skill transfer without concept transfer.
4. C-low-effort vs A: lower-effort teaching plus concept transfer.
5. B-copy vs C-full: direct copying versus teaching-style transfer with the same concept inheritance.

The original mode A is the no-inheritance control. Do not relabel the neural GAL-CL proxy as this experiment.

## 4. Fixed protocol

- 100 paired universe seeds (0–99) for the confirmatory run.
- 100 agents per generation.
- 10 generations.
- Same initial population construction, generation sizes, task environment, individual learning cycles and task-attempt budget across modes.
- Run all five modes for every seed.
- Preserve raw per-seed and per-agent records, not only aggregate curves.
- Record code commit, Python/dependency versions, command line, configuration and artifact SHA-256.
- No hyperparameter tuning against confirmatory outcomes.

## 5. Required measurements

For every seed × mode × generation:
- Mean task success rate and uncertainty across agents.
- Success rate for each of the five tasks.
- Mean and distribution of each skill.
- Mean concept-set size and prevalence of each task-associated concept.
- Tasks attempted and succeeded.
- Parent identity and child identity for every transmission.
- Inherited state immediately before independent learning.
- State after each development/work cycle.

The primary outcome remains task success, not raw concept count. Concept count alone can reward irrelevant or non-useful concepts.

## 6. Required controls and validity checks

Before the confirmatory run:
- Verify identical lifetime random streams across modes for matched agent identity/seed/generation.
- Verify equal task-attempt and independent-learning exposure.
- Verify parent-child mapping is one-to-one for the equal-sized population.
- Verify mode A receives no parent skills or concepts.
- Verify B-copy transfers exactly the parent's skills and concept set.
- Verify C-full transfers concepts and performs the specified three correction iterations for positive parent skills.
- Verify C-no-memory transfers skills by teaching but does not transfer concepts.
- Verify C-low-effort transfers concepts and performs one lower-rate correction iteration.
- Verify all skill values remain within [0, 1].
- Verify task difficulty/concept semantics and task-success calculation independently.
- Validate raw-data completeness and seed pairing.

If a test exposes a mismatch between implementation and intended mechanism, stop and fix before running the confirmatory experiment. Document any protocol change and assign a new protocol version.

## 7. Statistical plan

- Paired seed-level contrasts; report mean paired difference, 95% paired bootstrap confidence interval, paired t-test and Wilcoxon signed-rank sensitivity analysis.
- Report standardized paired effect size.
- Use Holm correction across the five pre-specified contrasts.
- Plot full generation trajectories with seed-level uncertainty.
- Report per-task results and heterogeneity, not only pooled success.
- Publish raw seed-level data and analysis script.
- Treat p-values as supporting evidence, not as a substitute for effect magnitude or model validity.

## 8. Construct-validity risks and follow-up experiments

The current environment is handcrafted and stationary. Therefore even a successful result establishes only that the implemented inheritance mechanisms improve performance in this particular model/environment.

Follow-up experiments must separately test:
1. **Novel-task transfer:** tasks sharing underlying skills/concepts but not seen during parent learning.
2. **Environmental change:** controlled changes to task frequencies, task difficulty, or concept utility.
3. **Inheritance cost:** explicit cost for copying/teaching, matched against independent-learning time/energy.
4. **Population structure:** one-to-one lineage versus multiple parents or social transmission, as separate protocols.
5. **Replicability:** independent implementation or researcher-run replication.

Do not combine these changes into the first confirmatory run. Each changes the scientific question.

## 9. Decision criteria

Evidence consistent with H1 requires:
- positive pre-specified paired differences versus A,
- uncertainty intervals that exclude zero for the relevant primary contrasts after multiplicity correction,
- effects visible in task performance (not only internal knowledge metrics),
- successful implementation and exposure audits,
- robustness to per-task analysis.

A null or negative result is a valid outcome. Do not modify the hypothesis after inspecting results.

## 10. Immutable historical results

The 2026-11-02 Split Digits neural-proxy run is retained separately:
- Source commit: `12baf9446a6fa08b9beb1c4d33c3ffc2517e8ea8`
- Workflow: `41416824440`
- Artifact ID: `13127368635`
- Artifact SHA-256: `2f2a6c4f891122039fd37b837c29a8179e92fe7bac7733e448a087c29ee6bb32`
- Audit: `experiments/09_split_digits/RESULTS_AUDIT_2026-11-02.md`

Never overwrite that artifact or audit. Corrected experiments receive new run IDs, artifacts and dated audit files.
