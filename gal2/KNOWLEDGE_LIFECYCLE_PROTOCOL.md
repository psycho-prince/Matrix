# GAL 2.0 — Generational knowledge lifecycle experiment

## Question
Does verified-only knowledge inheritance improve reliable knowledge availability
across generations compared with no transfer and unfiltered memory transfer?

## Design
Four arms: no transfer, verified-only, all-memory, and noisy-transfer. Default:
40 deterministic seeds, four generations, 12 symbolic facts. Generation zero
receives eight observations, including two deliberately corrupted claims.
Successors can add two new facts from fresh observations. These are explicitly
new acquisitions, not inherited knowledge. A separate held-out truth map verifies
claims but is never exposed to the answer function. Verification resets at transfer.
Every claim retains source agent, source generation, evidence ID, and lineage.

## Metrics
Exact-answer accuracy and coverage over all world facts and generations,
conflict rate, and raw per-seed/per-arm/per-generation results with SHA-256.

## Interpretation constraints
This is a deterministic symbolic software test, not a cognition or foundation
model test. The noisy-transfer arm deterministically corrupts every third transferred
claim. Each successor re-verifies inherited claims against held-out truth
before use; corrupted claims are rejected and remain in the audit trail. The finite world and oracle do not test open-ended
discovery, semantic reasoning, or general intelligence.
