# Independent scientific audit — foundational GAL confirmatory study

**Audit status:** Source/protocol audit completed; raw-artifact independent reproduction pending.  
**Study:** Native symbolic GAL confirmatory experiment, workflow run `41497968447`.  
**Source commit:** `947ef554e69a3ae8e04b6912b1910dae7b188f02`.  
**Artifact:** `native-gal-confirmatory-41497968447`, artifact ID `13168006474`.  
**Artifact ZIP SHA-256 (recorded):** `2586d5128f98b67084d6be19d51061cdfff68fd8d8a0fd777c6b46d93ede0828`.

This report is an audit of the available protocol, source code, and recorded run summary. It is **not** an independent re-analysis of the 413.9 MB raw artifact. The original research log explicitly leaves that independent parse and embedded raw-file hash verification pending.

## 1. What the experiment actually tested

The runner imports the original `gal.agents.agent.Agent` and `gal.environment.world.Environment`. It compares five inheritance modes across 100 paired universe seeds, 100 agents per generation, and 10 generations. Each agent receives five independent-learning cycles and 50 task attempts per generation.

The five tasks are the fixed tasks in the original environment:
- resource gathering / foraging / `concept_42`
- shelter building / construction / `concept_108`
- tool making / crafting / `concept_7`
- navigation / exploration / `concept_99`
- problem solving / logic / `concept_314`

The environment is stationary. The runner trains and measures success through the same `Environment` task set.

## 2. Important protocol-to-code mismatch

The pre-registration draft describes the primary endpoint as **held-out task success**. The confirmatory runner does not implement a held-out evaluation set.

It creates one `Environment()` per run, wraps that environment with an observer, and calls `agent.work(observed_world, num_tasks=10)` during each of five learning cycles. The resulting `population_mean_success` is computed from each agent's accumulated `task_success_rate` over those same 50 training/work attempts.

There is no separate validation/test task set, no independent evaluation RNG, and no evaluation phase that leaves agent state unchanged.

**Required correction:** describe the existing endpoint as *generation-level in-environment task success under repeated exposure to the fixed task distribution*. Do not call it held-out performance, novel-task transfer, or generalisation.

This does not erase the measured result. It narrows the claim to the outcome actually implemented.

## 3. Results recorded in the research log

The research log reports these generation-10 means:
- A: 0.041434
- B-copy: 0.884194
- C-full: 0.846732
- C-no-memory: 0.815040
- C-low-effort: 0.365926

It reports paired seed-level contrasts against A, plus B-copy versus C-full:
- B-copy − A: +0.842760; paired bootstrap 95% CI [0.841444, 0.844062]; Holm-adjusted p = 2.51e-209.
- C-full − A: +0.805298; CI [0.803582, 0.807000]; Holm p = 4.12e-196.
- C-no-memory − A: +0.773606; CI [0.771770, 0.775474]; Holm p = 2.35e-190.
- C-low-effort − A: +0.324492; CI [0.322002, 0.327030]; Holm p = 2.91e-140.
- B-copy − C-full: +0.037462; CI [0.036366, 0.038566]; Holm p = 1.31e-83.

These values are **reported results**, not yet independently reproduced from the raw archive. Their extreme significance does not repair a construct-validity limitation.

## 4. What is supported, conditional on raw-data audit

If the raw records reproduce the logged summaries and pass independent integrity checks, the study supports this scoped statement:

> In the implemented handcrafted, stationary five-task symbolic environment, the tested inheritance modes produced higher generation-10 in-environment task success than the no-inheritance control under the specified paired-seed and exposure protocol.

The mechanism audit recorded in the log reports 90,000 inheritance events per mode:
- A: child state unchanged by inheritance in all recorded events.
- B-copy: exact skill and concept transfer in all recorded events.
- C-full: concept transfer, with teaching-style skill updates.
- C-no-memory: no parent concept transfer.
- C-low-effort: concept transfer with one lower-effort skill teaching iteration.

These are implementation-mechanism checks. They do not establish that inherited concepts are semantically true, that information is conserved, or that knowledge transfers to unseen tasks.

## 5. Unresolved audit requirements

Before treating the confirmatory result as independently validated, an auditor must parse the original raw JSONL archive without importing the study runner and verify:

1. Archive ZIP SHA-256 and embedded `RAW_SHA256.txt` against the extracted `raw_records.jsonl.gz`.
2. Exactly 5,000 generation records: 100 seeds × 5 modes × 10 generations.
3. Unique and complete seed/mode/generation keys.
4. Exactly 100 agents per generation and 50 task attempts per agent.
5. Task-attempt denominators and success counts reconcile at agent, task, generation, seed, and mode levels.
6. Every generation after the first has 100 valid parent-child links; parent IDs resolve to the immediately preceding generation.
7. The observed inherited child state matches the parent's recorded state for B-copy; A remains unchanged; C-no-memory does not copy parent concepts.
8. Matched seed/mode/agent/generation identities have identical per-task attempt counts, as expected from the isolated lifetime RNG design.
9. Recomputed generation means, seed-level contrasts, confidence intervals, and multiplicity-adjusted tests reproduce the logged summary within stated numerical tolerances.
10. Failed or malformed records are reported, never silently dropped.

The audit must be implemented independently of `run_native_gal_confirmatory.py`; otherwise it risks repeating the same assumptions and errors.

## 6. Next experiment required for stronger scientific validation

Do not rerun the same stationary benchmark at larger scale. The next experiment should test **generalisation under controlled distribution shift**.

A separate, versioned benchmark should:
- define a finite set of task-relevant ground-truth facts or rules;
- expose generations to a training task distribution;
- evaluate them on disjoint tasks that require the same underlying rules but use unseen surface forms or combinations;
- introduce a pre-specified shift in task frequencies or rule relevance;
- compare no inheritance, skill-only inheritance, knowledge-only inheritance, and combined inheritance;
- keep training and evaluation RNG streams separate;
- measure separately: exact information retained, correctness of inherited information, held-out task utility, and recovery after shift;
- use paired seeds, equal training budgets, fixed pre-registered hypotheses, and an independent raw-data auditor.

The current random concept vocabulary and fixed exact-match concept bonuses are not a sufficient semantic ground-truth model for a general knowledge-retention claim. A controlled synthetic rule benchmark must explicitly define what counts as true information and how new tasks depend on it. Label that benchmark as a new operationalisation, not as a property already demonstrated by the original environment.

## 7. Research claims that remain out of scope

This study does not establish:
- physical energy or information conservation;
- biological evolution or inheritance;
- consciousness, general intelligence, or AGI;
- universal benefit from inheritance;
- semantic truth or reliability of inherited knowledge;
- transfer to novel tasks or changing environments.

## 8. Audit decision

**Decision: conditional support for a narrow in-environment performance effect; no independent raw-data validation yet; no evidence yet for generalisation or information conservation.**

Preserve the original run, artifact, and historical audit unchanged. Any correction to the protocol or new benchmark must receive a new protocol version, source commit, workflow run, artifact, and dated audit record.
