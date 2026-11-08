# GAL 2.0 MemoryStore → Model-Mediated Task Pilot

**Date:** 2026-11-09  
**Repository:** `psycho-prince/Matrix`  
**Source branch:** `research/gal-2.0-core`  
**Source revision reviewed in the prior audit:** `141765b96697ba2eeb62395e6ae7dc8a0fdd12d0`  
**Audit branch:** `audit/gal2-independent-review-2026-11-09`  
**Status:** Exploratory integration pilot; not a confirmatory study.

## Research question

Can a model solve held-out compositional tasks when it receives verified parent knowledge through GAL 2.0's memory record format and inheritance/retrieval API?

## Source-grounded implementation facts

The source files `gal2/models.py` and `gal2/memory.py` define `MemoryKind`, immutable `MemoryRecord`, `MemoryStore.add/get/search/inherit_verified/counts`. The inheritance method copies verified records to the child custodian and appends the source agent to lineage.

The source file `gal2/agent.py` separately defines `Agent.evaluate`, which estimates success from capability proficiency and task difficulty. It does not retrieve or consume `MemoryStore` records. Consequently, this pilot uses a thin external model adapter; it does not claim that the repository's native `Agent.evaluate` is memory-grounded.

## Protocol

A parent store contains two verified records:

- Semantic: a symbolic rulebook, A = add 2, B = multiply by 3, C = subtract 1.
- Procedural: start from the supplied seed and apply symbols left-to-right.

The child store receives records only through the source-defined `inherit_verified` behavior. The adapter retrieves the semantic record by the `rulebook` tag and the procedural record by the `procedure` tag. The model then applies the retrieved mapping to 12 fixed tasks. Answers are checked against an explicit deterministic evaluator.

The implementation used a small isolated Python reproduction of the relevant `MemoryRecord` and `MemoryStore` definitions copied from the inspected source. It was not an import of a cloned checkout of the repository. No GAL source file was modified.

## Observed results

- Verified parent records inherited: **2**
- Semantic rulebook records retrieved: **1**
- Procedural instruction records retrieved: **1**
- Provenance check: source `parent-pilot`, custodian `child-pilot`, lineage contains `parent-pilot`, verified flag retained.
- Model-mediated task accuracy with retrieved rulebook: **12/12 (100%)**.
- Without the mapping, the task prompts do not identify a unique numeric answer; the appropriate response is abstention. No fabricated numeric baseline accuracy is reported.

Answers in task order: **18, 24, 8, 12, 7, 14, 31, 12, 7, 32, 36, 36**.

The executed result payload SHA-256 was:

`38df30d8e1c00fc3d21c3c3eb5d1bd26d5c47c643880921640f217809ec42d77`

## Interpretation

This pilot establishes a limited end-to-end demonstration that (1) verified memory records in the GAL 2.0 data format can be inherited with source/custodian lineage, (2) a child-side retrieval call can select those records, and (3) this model can use the retrieved rulebook to solve a small set of compositional tasks.

It does **not** establish that the native GAL 2.0 agent uses memory during task execution. The native `Agent.evaluate` path does not consume memory; this limitation is explicit in the source. It also does not establish a causal performance gain over a measured baseline: the no-memory condition lacks the rule mapping, so numeric answers are underdetermined and abstention is the only defensible response. The 12 tasks are fixed, small, and deterministic. No randomization, independent replication, confidence interval, multi-model comparison, or statistical test was performed.

## What is needed for a real controlled comparison

A follow-on implementation must add a distinct model-backed task adapter that calls the actual `MemoryStore` retrieval path and logs retrieved record IDs, content hashes, prompts, model identifier, decoding settings, token usage, and outputs. It should compare:
1. no transfer (model receives task only);
2. capability-only transfer;
3. semantic memory transfer;
4. procedural memory transfer;
5. combined memory transfer;
6. corrupted-memory control;
7. oracle-memory upper bound.

Use generated rulebooks, disjoint train/test operation compositions, randomized paired task sets, multiple seeds, blinded deterministic scoring, explicit abstention scoring, and raw traces. Run it from a clean checkout in a reproducible environment. Until that exists, do not interpret this pilot as evidence that GAL 2.0 has acquired memory-grounded learning.

## Reproducibility and limitations

The pilot's exact executed result object is documented in the ChatGPT execution record for this session; this Markdown report records the output summary and hash. The isolated reproduction mirrors the inspected source methods used here but is not a test of the installed package. No GitHub Actions run or repository-native test suite was launched for this pilot.
