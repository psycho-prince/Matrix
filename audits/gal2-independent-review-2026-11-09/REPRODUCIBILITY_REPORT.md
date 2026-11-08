# GAL 2.0 Reproducibility Report

**Reviewed commit:** `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`  
**Observed workflow:** [42035297592](https://github.com/psycho-prince/Matrix/actions/runs/42035297592)

## Reproduction status

The repository provides a dedicated GAL 2.0 package, a `pyproject.toml`, tests, deterministic experiment entry points, GitHub Actions workflows, and artifact uploads. The latest configured workflow passed across Python 3.10–3.12.

This is evidence of CI reproducibility for the configured commands. The reviewer did not perform a second independent clean checkout or execute the experiments locally. Raw-artifact independent reproduction is therefore not claimed.

## Reproduction commands from a clean checkout

```bash
git clone https://github.com/psycho-prince/Matrix.git
cd Matrix
git checkout research/gal-2.0-core

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './gal2[test]'

python -m pytest -q gal2/tests
python -m compileall -q gal2
python -c "import gal2; from gal2.validation import run_validation; print('imports: OK')"

python -m gal2.validation --seed 20261104 --output /tmp/gal2-validation.json
python -m gal2.comparison --seed-start 1000 --seeds 100 --test-trials 250 --output /tmp/gal2-comparison.json
python -m gal2.knowledge_lifecycle > /tmp/gal2-knowledge-lifecycle.json
python -m gal2.knowledge_questions > /tmp/gal2-knowledge-questions.json
python -m gal2.knowledge_question_stress > /tmp/gal2-knowledge-question-stress.json
python -m unittest gal2.tests.test_analytical_theory -v
```

## Environment and dependency observations

- GAL 2.0 declares Python `>=3.10`.
- The test extra declares `pytest>=8.0`; it is not pinned to an exact version.
- The core package declares no runtime dependencies.
- The repository root `requirements.txt` contains unpinned `numpy`, `matplotlib`, `scipy`, and `google-genai`.
- The core CI workflow uses `actions/checkout@v4` and `actions/setup-python@v5`, and tests three Python minor versions.
- The CI workflow uploads experiment reports as artifacts.

## Reproducibility gaps

1. No lockfile or fully pinned dependency set for the full repository is present in the reviewed paths.
2. CI uses dependency ranges, so future clean installs can resolve different pytest/build-tool versions.
3. The CI unit-test job runs the GAL 2.0 package tests, not the root legacy test suite.
4. No clean-checkout independent rerun was performed for this audit.
5. Artifact presence and job success do not independently establish artifact integrity or metric correctness.
6. Some experiments use deterministic seeds, but the exact task manifest and environment should be exported alongside every result.
7. LLM prototype experiments require model/provider/version/prompt/configuration logging and may not be deterministic even when a seed is set.
8. For full scientific reproducibility, archive the source commit, environment manifest, task manifest, raw trace, analysis script, and output hashes together.

## Required artifact manifest

Each confirmatory run should publish:
- source commit SHA;
- Python version and OS/runner image;
- dependency lockfile and package hashes;
- complete configuration;
- seed list;
- task/world manifest hash;
- raw trace archive and SHA-256;
- analysis code commit;
- generated summary and figure hashes;
- exclusions and failed-run log.

## Verdict

**CI reproducibility: demonstrated for the configured GAL 2.0 workflow on the reviewed commit. Independent clean-checkout reproduction: pending. Full repository reproducibility: partial.**
