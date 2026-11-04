# GAL cross-programme comparative protocol

**Status:** protocol draft; not preregistered and no experiment authorized by this document has been run.  
**Applies to:** GAL 1.0 and GAL 2.0 independently, followed by a bridge study.

## 1. Objective

Test whether generational transfer improves successor performance relative to a matched no-transfer condition, and identify how the effect depends on environmental change, evidence quality, and transfer cost.

The objective is deliberately narrower than demonstrating artificial life, intelligence, or open-ended evolution.

## 2. Stage 0 — construct and mechanism audit

Complete separately for each programme before collecting confirmatory outcomes.

### GAL 1.0 audit

- Enumerate all inheritance modes and document the exact state transferred by each.
- Trace task generation, task success, skill updates, concept acquisition, and random-number streams.
- Verify paired seeds produce matched exogenous task sequences across treatment arms.
- Confirm each treatment differs only in its declared mechanism.
- Distinguish native symbolic GAL outcomes from neural continual-learning proxy outcomes.

### GAL 2.0 audit

- Document the exact synthetic success function and all state updates.
- Determine whether memory, prerequisites, procedures, context tags, and evidence provenance causally affect task solving; do not assume they do because they are stored.
- Audit inheritance eligibility, child revalidation, duplicated evidence, and confidence semantics.
- Keep exact mathematical tests separate from task-performance experiments.
- Do not describe the current probabilistic executor as an external learner.

A failed audit blocks confirmatory interpretation.

## 3. Stage 1 — within-programme replication

Each programme runs its own frozen protocol. Minimum arms:

1. no transfer;
2. programme's primary transfer mechanism;
3. a mechanism-matched control that preserves exposure and resource use but removes the hypothesized information transfer.

Additional arms are allowed only if specified before outcome inspection. GAL 1.0's existing inheritance modes and GAL 2.0's existing evidence-gated transfer can be evaluated in their own studies; they are not assumed to be equivalent treatments.

Use paired seeds or matched initial conditions. The experimental unit must be declared in advance (e.g., universe, population, or independent run). Agents within one shared environment are not automatically independent replicates.

## 4. Stage 2 — environmental change

Specify source and successor task distributions before execution. Include:

- stationary control;
- moderate, quantified distribution shift;
- severe, quantified distribution shift.

The shift metric, sampling method, and uncertainty must be specified. Report performance on the actual successor test distribution in addition to any theoretical distance bound.

## 5. Stage 3 — evidence quality and dependence

Where the implementation supports it, manipulate evidence quality independently of quantity:

- reliable observations;
- controlled noisy observations;
- duplicated or correlated observations;
- contradictory observations.

Check that the manipulation changes the intended property and no unintended property. For GAL 2.0, provenance labels alone do not make observations statistically independent. For GAL 1.0, concept transmission alone does not establish truth or evidence quality.

## 6. Primary and secondary outcomes

**Primary outcome:** successor performance on a held-out successor-distribution test set, measured using a prespecified loss or score.

**Secondary outcomes:**

- source-domain performance;
- transfer effect relative to no-transfer;
- performance degradation under shift;
- retention of useful state, using a separately validated measure;
- false-positive or unsupported-claim rate where applicable;
- resource cost (training, evaluation, storage, compute, and transfer);
- calibration, only where the system outputs probabilities with a defensible calibration interpretation.

Do not use memory-record count, concept count, confidence fields, or raw skill summaries as substitutes for the primary outcome.

## 7. Statistical analysis

For paired runs, calculate per-seed differences

\[
D_s=Y_s(\text{transfer})-Y_s(\text{control}).
\]

Report the mean paired effect, standard deviation, confidence interval, full distribution, and a robust paired analysis. Specify the primary estimator and interval procedure before running the experiment. Correct for multiple comparisons when making confirmatory claims across multiple arms or outcomes.

Power and sample size must be determined from a declared smallest effect of practical interest and a defensible variance estimate. Pilot data may inform variance and mechanics, but must not be silently reused as confirmatory evidence.

## 8. Data and reproducibility requirements

Every run must record:

- immutable source commit and environment/dependency versions;
- protocol version and deviations;
- all seeds and treatment assignments;
- raw per-task and per-agent outcomes;
- generation-level summaries;
- resource measurements;
- exclusion reasons;
- artifact checksum and audit report.

Preserve failed runs. Do not silently rerun until a desired result appears. Independent audit should be possible from raw records without trusting summary metrics.

## 9. Cross-programme bridge study

Only after both within-programme audits pass:

1. Select a task family that can be represented in both systems without changing the construct being measured.
2. Define the common input/output contract and held-out evaluation distribution.
3. Match the information available to parent and successor, task exposure, and evaluation budget.
4. Compare each system's transfer effect against its own matched control.
5. Compare effect estimates and uncertainty; do not pool raw scores unless measurement equivalence is established.
6. Publish implementation-specific deviations and negative results.

If a faithful common task cannot be implemented, report a conceptual comparison rather than claiming a direct empirical comparison.

## 10. Stop conditions

Stop or redesign before confirmatory analysis if:

- treatment arms differ in unintended ways;
- paired random streams are not actually paired;
- the primary outcome leaks into training or verification;
- memory/provenance is claimed to affect behavior but does not enter the causal execution path;
- raw records cannot reconstruct reported summaries;
- the test distribution is not held out;
- resource use is materially unequal and unmeasured.

No result from this protocol, by itself, establishes consciousness, biological life, general intelligence, or open-ended evolution.
