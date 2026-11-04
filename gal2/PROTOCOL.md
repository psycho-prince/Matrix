# GAL 2.0 Core — implementation and validation protocol v0.2

## Research question
Can evidence-backed capabilities and typed memory be inherited, adapted to a successor's context, and independently revalidated on held-out tasks?

## Scope
This milestone implements data structures and a synthetic probabilistic harness only. It does not test AGI, general intelligence, biological evolution, or practical task performance.

## Mechanisms
1. Structured capability records retain observed proficiency, a sample-size confidence indicator, evidence, prerequisites, context tags, failure conditions, version and lineage.
2. Episodic, semantic and procedural memory are stored separately. Transfer preserves original source provenance and records the current custodian.
3. Seeded task generation labels train, validation and test tasks. Its vocabulary is finite.
4. Basic inheritance transfers only parent-verified capabilities, with child verification reset.
5. Adaptive inheritance applies a context-tag Jaccard threshold and discounts source proficiency toward a configurable prior. Child evidence is empty and the child must validate independently.
6. Evaluation uses a separate random stream and does not update proficiency, evidence or memory. A capability passes only if observed success rate and Wilson lower confidence bound meet the configured threshold.

## Required invariants
- Invalid scores, task difficulty, task split, or missing provenance are rejected.
- Same seed/split/offset produces the same tasks.
- Train and test task identifiers are disjoint.
- Memory types remain isolated; inherited memory retains source and custodian lineage.
- Unverified parent capabilities are not inherited.
- Parent verification is not automatically propagated to children.
- Adaptive transfer rejects unverified capabilities and incompatible contexts.
- Evaluation does not mutate training state.
- Too few held-out trials fails closed.
- A child must belong to a later generation than its parent.

## Threats to validity
- The task executor is a synthetic Bernoulli simulator, not an actual problem-solving agent.
- Context similarity is Jaccard overlap over manually declared tags, not semantic context understanding.
- The generator draws from finite predefined vocabularies.
- The executor does not yet use memory, prerequisites or procedures to solve tasks.
- Unit tests validate software invariants, not scientific hypotheses.
- No baseline comparison, resource accounting, independent replication, or external benchmark has been run.

## Next milestones
1. Add persistent content-addressed provenance and tamper-evident experiment records.
2. Implement real task adapters and blinded held-out evaluation.
3. Add conflict resolution, forgetting/revocation, multi-parent inheritance and recombination as separate modules.
4. Compare no-transfer, copy-only, adaptive-transfer and shared-memory baselines under preregistered environment shifts.
5. Integrate a foundation model only after the non-LLM mechanism is validated.
