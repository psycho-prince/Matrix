# GAL 2.0 Core — implementation and validation protocol v0.1

## Research question
Can evidence-backed capabilities and typed memory be transferred to successor agents, then independently revalidated on held-out tasks?

## Scope
This milestone implements the data model and deterministic synthetic harness only. It does not test AGI, general intelligence, biological evolution, or practical task performance.

## Mechanisms
1. Capability records retain proficiency, confidence, evidence, prerequisites, context tags and failure conditions.
2. Episodic, semantic and procedural memory are stored separately.
3. Dynamic tasks are generated from a seeded task generator and explicitly labelled train, validation or test.
4. Only verified parent capabilities are eligible for transfer. Transferred capabilities lose their verified status in the child.
5. Child verification uses held-out tasks and minimum trial/success thresholds.

## Required invariants
- Invalid scores, task difficulty, task split, or missing provenance are rejected.
- Same seed/split/offset produces the same tasks.
- Train and test task identifiers are disjoint.
- Memory types remain isolated.
- Unverified parent capabilities are not inherited.
- Parent verification is not automatically propagated to children.
- Too few held-out trials fails closed.
- A child must belong to a later generation than its parent.

## Known threats to validity
- The task executor uses a simple probabilistic formula and is not an actual problem-solving agent.
- The task generator draws from finite predefined capability/concept/context vocabularies.
- The initial tests validate software invariants, not scientific claims.
- No baseline comparison, resource accounting, independent replication, or external benchmark has been run.

## Next milestones
1. Add persistence and content-addressed provenance for memory/evidence.
2. Implement real task adapters and blinded held-out evaluation.
3. Add fitness-based multi-objective selection and controlled mutation as separately testable modules.
4. Add environment-shift experiments and matched shared-memory/skill-library baselines.
5. Integrate a foundation model only after the non-LLM mechanism is validated.
