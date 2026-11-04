# GAL 2.0 Core (experimental)

GAL 2.0 is a parallel research implementation. It does not replace or modify the original symbolic GAL implementation under `gal/`.

## Implemented architecture

- Structured capability records with outcome-based proficiency, evidence provenance, confidence indicator, prerequisites, context tags, failure conditions, version and lineage.
- Separate episodic, semantic and procedural memory stores.
- Seeded task generation with train/validation/test labels (finite vocabulary).
- Evidence-gated basic inheritance.
- **Adaptive inheritance:** context compatibility scoring, conservative proficiency recalibration, explicit accept/reject reports and child-side revalidation.
- Evaluation is isolated from training updates and uses a Wilson lower-bound gate.

## Important limitations

This remains a synthetic research harness, not an actual learning agent. Its task executor is a probabilistic simulator; it does not use memory, prerequisites or procedures to solve tasks. Context similarity is a Jaccard heuristic over declared tags, not semantic understanding. No external benchmark, baseline comparison, resource accounting or independent replication has been run. Do not present synthetic scores as empirical AI capability results.

## Run tests

```bash
python -m pip install -e '.[test]'
python -m pytest
```

## Research integrity

Keep GAL 2.0 separate from original GAL 1.0 results. Preserve raw outputs, seeds, protocol and code revision. Unit tests validate software invariants, not scientific hypotheses.

See [Adaptive inheritance design](ADAPTIVE_INHERITANCE.md) and [validation protocol](PROTOCOL.md).
