# GAL 2.1 — Five knowledge/question stress tests

## Scope
This benchmark extends the first exact-key round-trip benchmark with five separate tests. It is a controlled symbolic software test, not a test of a foundation model or open-ended natural-language understanding.

## Tests
1. **Incomplete knowledge:** create questions only from known facts and flag a missing object slot rather than inventing an answer.
2. **Held-out paraphrases:** answer two surface forms not used by the canonical question generator using explicit grammar patterns.
3. **Unanswerable questions:** return an unknown status when the queried fact is absent; do not guess.
4. **Multi-hop relations:** answer a question by following two graph edges (country → capital → region), retaining both evidence edges.
5. **Contradiction detection:** identify incompatible objects for the same subject/relation/context and block a definitive answer.

## Success criteria
Each test has a distinct pass condition. Overall success requires all five conditions. Raw structured output and a SHA-256 digest are emitted by `python -m gal2.knowledge_question_stress`.

## Limitations
Paraphrase handling is a finite hand-authored pattern set, not semantic language understanding. Multi-hop is a fixed two-edge relation path, not general planning. Incomplete knowledge is represented as a missing slot. Contradiction detection uses exact symbolic keys and context labels. Passing demonstrates implementation correctness under this protocol only.


## Implementation note
The parser accepts only the explicit question forms listed in the benchmark source; it does not infer arbitrary paraphrases. The current CI suite validates these forms and rejects unsupported ones.
