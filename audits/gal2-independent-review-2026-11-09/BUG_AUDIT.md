# GAL 2.0 Bug and Risk Audit

**Reviewed commit:** `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`  
**Scope:** Source-level findings. Findings below are not claims that a runtime failure was reproduced unless explicitly stated.

## Findings

### B-01 — Tag matching can mark memory verified without independent evidence
**Severity:** High  
**Location:** `gal2/memory.py`, `MemoryStore.verify_related()`

The helper changes semantic and procedural records to `verified=True` solely when a capability name occurs in the record's tags. The method's own docstring correctly says this is not independent semantic verification, but the API still mutates the same verification flag used by inheritance.

**Risk:** A downstream caller may treat a tag association as truth validation and propagate unsupported claims.

**Recommendation:** Deprecate or remove this helper from production inheritance paths. Replace the boolean with explicit verification metadata: verifier identity/type, evidence reference, protocol version, timestamp, and outcome. Require an independent verifier or a declared oracle in tests.

### B-02 — Adaptive inheritance does not adapt/filter memory by context
**Severity:** High  
**Location:** `gal2/adaptive_inheritance.py`, `adaptive_inherit()`

Capabilities are filtered and recalibrated by context similarity. Verified memory records are then copied wholesale through `inherit_verified()`, regardless of tags, source context, or child context.

**Risk:** The adaptive policy can reject a capability as context-incompatible while still transferring associated knowledge/procedures from the same context.

**Recommendation:** Add explicit memory-context metadata and a separately specified memory-transfer policy. Record accepted/rejected memory decisions. Do not assume capability context tags are sufficient to infer memory applicability.

### B-03 — MemoryRecord is only shallowly immutable
**Severity:** Medium  
**Location:** `gal2/models.py`, `MemoryRecord.content`; `gal2/memory.py`, `inherit_verified()`

The dataclass is frozen, but `content` is a mutable dictionary. Inheritance creates a shallow `dict()` copy, so nested dictionaries/lists remain shared references.

**Risk:** A nested mutation can change a supposedly immutable record or leak across generations, undermining provenance and reproducibility.

**Recommendation:** Deep-freeze or deep-copy payloads at construction and transfer. Add tests with nested mutable payloads and mutation attempts.

### B-04 — Generation-order invariant is enforced only by wrapper functions
**Severity:** Medium  
**Location:** `gal2/agent.py`, `Agent.inherit_from()`; `gal2/memory.py`, `inherit_verified()`

The public low-level transfer methods do not independently enforce that the receiving generation is later than every source record/capability generation. The higher-level inheritance wrappers do check agent generation ordering.

**Risk:** Direct API use can bypass a core lineage invariant and produce temporally invalid transfer records.

**Recommendation:** Enforce generation ordering in the lowest-level transfer API and validate source record generation and custodian lineage.

### B-05 — Capability confidence is not calibrated
**Severity:** Medium  
**Location:** `gal2/models.py`, `Capability.record()`

Confidence is set to `n / (n + 10)`. This increases with evidence count irrespective of task difficulty, evidence quality, calibration error, or correctness distribution.

**Risk:** The field may be misinterpreted as a probability that the capability is correct.

**Recommendation:** Rename it to an evidence-volume indicator or replace it with a calibrated estimate evaluated using Brier score, log loss, and reliability diagrams.

### B-06 — Evidence score is not used to update proficiency
**Severity:** Medium  
**Location:** `gal2/models.py`, `Capability.record()`

Proficiency is computed as the mean of boolean success flags; the `Evidence.score` field is retained but ignored by the update rule.

**Risk:** Partial-credit or graded evidence is silently discarded.

**Recommendation:** Either remove/define the score field or specify and test how it contributes to proficiency. Keep the binary and graded outcomes distinct if both are needed.

### B-07 — Evaluation verification is probabilistic and task IDs do not establish task novelty
**Severity:** Medium  
**Location:** `gal2/agent.py`, `evaluate()`; `gal2/tasks.py`

Evaluation samples Bernoulli outcomes from the same scalar success formula. Unique IDs are checked within one evaluation call, but unique IDs do not prove that held-out tasks are novel or semantically disjoint from training tasks.

**Risk:** A capability can pass a synthetic threshold without demonstrating learned competence on independently specified tasks.

**Recommendation:** Use executable task environments, explicit train/validation/test manifests, content-level deduplication, and separate evaluation policies. Document that the current check is simulator verification only.

### B-08 — Verification provenance is not attached to MemoryRecord
**Severity:** Medium  
**Location:** `gal2/models.py`, `MemoryRecord`; `gal2/memory.py`

Memory records carry a boolean `verified` flag but no verifier identity, evidence object, verification protocol, or verification timestamp.

**Risk:** The system cannot audit why a memory is trusted or whether the verification was appropriate for the child context.

**Recommendation:** Add a structured verification event with verifier, method, oracle/source, evidence references, scope, version, and result.

### B-09 — Adaptive transfer's unverified-parent decision reports similarity as zero
**Severity:** Low  
**Location:** `gal2/adaptive_inheritance.py`, `adapt_capability()`

For unverified parent capabilities the method returns a rejection with `context_similarity=0.0` without computing actual similarity.

**Risk:** Audit output conflates “not evaluated because parent unverified” with “measured zero compatibility.”

**Recommendation:** Compute similarity independently or use an explicit null/not-evaluated value.

### B-10 — The root test suite and GAL 2.0 test suite have different coverage boundaries
**Severity:** Medium  
**Location:** `tests/test_gal_core.py`; `gal2/tests/`; `.github/workflows/gal2-core.yml`

The observed GAL 2.0 workflow runs `gal2/tests` and GAL 2.0 experiments. It does not run the repository-root legacy test suite. The root test suite also checks manuscript PDFs and legacy dataset/statistics artifacts, which is a different scope.

**Risk:** A green GAL 2.0 workflow may be mistaken for a green full-repository test suite.

**Recommendation:** Label CI status by scope and add a separate root/legacy CI job with pinned dependencies, or document why that suite is intentionally excluded.

## Positive controls observed

- Child capability verification is reset on inheritance.
- Evaluation is designed not to mutate training state.
- The latest CI run completed all configured GAL 2.0 jobs successfully.
- The scientific validation gap audit explicitly discloses the memory-to-action limitation.

## Triage

Fix B-01 and B-02 before using inherited memory as a scientific mechanism. Fix B-03 and B-04 before relying on lineage as an integrity guarantee. Reframe B-05/B-06 before interpreting confidence or graded evidence.
