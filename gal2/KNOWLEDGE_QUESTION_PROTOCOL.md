# GAL 2.1 — Knowledge Processing vs Question Creation

## Research question
Are knowledge processing and question creation opposites, equal, or complementary?

## Operational definitions
- **Question creation:** encode a stored fact as a question.
- **Knowledge processing:** resolve that question against a knowledge store.
- **Round-trip recovery:** reconstruct the original fact from the question key and returned answer.

These operations are treated as directional transformations. They are not assumed to be exact inverses: generation may omit information, and processing may fail because knowledge is missing or ambiguous.

## Protocol
- Eight fixed symbolic facts across geography, history, science and biology.
- Generate one question per fact using relation-specific templates.
- Resolve each generated question using exact subject, relation and context matching.
- Reconstruct each fact from the question key and answer.
- Include negative controls for unknown and ambiguous facts.
- Report generation validity, answer accuracy, exact round-trip recovery and negative-control rejection separately.

## Results
The deterministic report is produced by `python -m gal2.knowledge_questions` and uploaded as the `gal2-knowledge-question-benchmark` CI artifact.

## Interpretation
A perfect result demonstrates equivalence only within this finite template-and-retrieval benchmark. It does not establish natural-language understanding, open-ended question quality, semantic reasoning, or learned knowledge. A stronger follow-up must use paraphrases, distractor facts, incomplete context, multi-hop relations and held-out facts.
