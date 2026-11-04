# GAL 2.0 — paired inheritance baseline comparison

## Status
Executed synthetic mechanism comparison. The JSON artifact from the associated
GitHub Actions run is the authoritative record.

## Question
Under matched task exposure and paired random seeds, how do four successor
initialization policies compare on a held-out shifted-context task set?

## Arms
1. **No transfer:** fresh successor with no capability or memory.
2. **Capability copy:** copy the parent's verified capability statistics and
   declared context tags; child evidence is empty and verification resets.
3. **Adaptive inheritance:** use the existing Jaccard context gate and
   proficiency recalibration; child evidence is empty and verification resets.
4. **Shared memory:** transfer verified parent memory only; do not transfer a
   capability.

## Paired design
- Seeds: 1000–1099 (100 paired seeds).
- Each seed uses a deterministic synthetic parent fixture with proficiency
  0.90, a verified planning capability, and two verified memory records.
- This parent fixture is deliberately pre-verified to isolate transfer
  policies; it is not produced by learning and is not evidence of training.
- Every arm receives the same 250 shifted-context test task IDs and difficulty
  sequence within a seed.
- Successor IDs and evaluation RNG seeds are held constant across arms to
  support common-random-number pairing.
- Primary outcome: test success rate.
- Secondary outcomes: Wilson lower bound, paired seed-level differences,
  initial proficiency, inherited memory count.
- Paired differences are descriptive; no confirmatory significance claim is
  made by this first comparison.

## Results
See the run artifact `gal2-inheritance-baseline-comparison` for all raw
seed-by-arm results and the SHA-256 digest. This protocol is not a substitute
for the raw data.

## Interpretation constraints
The task executor calculates success from capability proficiency and task
difficulty only. Context labels do not change the success function, and memory
is not read by the executor. Therefore:
- Shared-memory and no-transfer are expected to be identical. This is a
  diagnostic of a known architectural limitation, not evidence that memory
  has no value in general.
- Copy and adaptive inheritance differ in initial proficiency; they are not
  isolated tests of context adaptation in a context-sensitive environment.
- The synthetic Bernoulli simulator is not a real learning agent.
- Results cannot establish generalization, intelligence, AGI, consciousness,
  biological evolution, or practical task performance.

## Reproduction
```bash
python -m gal2.comparison --seed-start 1000 --seeds 100 --test-trials 250 --output gal2/gal2-comparison.json
```

The output includes raw seed/arm rows and a SHA-256 digest over the canonical
JSON payload (excluding the digest field itself). Record the source commit SHA
alongside the artifact when reporting results.
