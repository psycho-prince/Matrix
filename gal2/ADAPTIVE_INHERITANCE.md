# Adaptive inheritance design (GAL 2.0)

## Implemented in this milestone
- **Eligibility gate:** only parent capabilities explicitly marked verified are candidates.
- **Context compatibility:** Jaccard similarity over declared context tags; empty context sets do not transfer.
- **Proficiency recalibration:** inherited proficiency is discounted toward a configurable prior as context overlap decreases.
- **No inherited validation:** child capabilities start unverified, with empty child evidence and an incremented version.
- **Lineage:** parent agent identity is appended to capability lineage; inherited memory retains its original source and records the current custodian.
- **Auditable decisions:** each capability yields accepted/rejected status, similarity, source/adapted proficiency and reason.
- **Holdout separation:** evaluation uses a separate random stream and does not update skill statistics or memory. Verification requires both the observed rate and Wilson lower bound to meet the threshold.

## Explicit limitations
Context tags are metadata, not semantic understanding. Jaccard overlap is a baseline heuristic. The synthetic executor does not consume memory, prerequisites, or procedures when solving tasks. No mutation, recombination, multi-parent arbitration, forgetting, or real environment adaptation is implemented yet. These features require separate experiments and baselines.

## Recommended next tests
1. Ablate context filtering and recalibration independently.
2. Compare inheritance against no-transfer, copy-only and shared-memory baselines.
3. Evaluate on preregistered context shifts and unseen task templates.
4. Report transfer acceptance, held-out success, calibration, retention, compute and memory costs.
