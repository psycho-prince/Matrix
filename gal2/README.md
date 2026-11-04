# GAL 2.0 Core (experimental)

GAL 2.0 is a parallel research implementation. It does not replace or modify the original symbolic GAL implementation under `gal/`.

## Initial scope

- Structured capability records with evidence, confidence, prerequisites and context metadata.
- Separate episodic, semantic and procedural memory stores.
- Deterministic dynamic task generation with train/validation/test labels.
- Evidence-gated inheritance: only parent-verified capabilities are candidates, and a child receives them as **unverified** until it independently passes held-out evaluation.

## Important limitations

The current task executor is a synthetic probabilistic simulator, not an LLM, robot or real-world task adapter. Its scores are software-test fixtures and must not be presented as empirical AI capability results. The initial generator is deterministic and uses a finite vocabulary; it is not yet an open-ended task generator. Memory is in-memory only. Selection, mutation, recombination, population adaptation, persistence, safety policies and foundation-model integration are not implemented in this milestone.

## Run tests

```bash
python -m pip install -e '.[test]'
pytest
```

## Research integrity

Do not compare GAL 2.0 synthetic scores to the original GAL experiment as if they were the same benchmark. Preserve raw experiment outputs, seeds, code revision and protocol for all future studies.
