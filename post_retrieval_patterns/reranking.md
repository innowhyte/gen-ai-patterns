# Reranking

## Problem

Initial retrieval results are often "good enough" but not ordered for answer generation. Relevant chunks can appear below weak or noisy chunks, which wastes context budget and increases the chance that the generator relies on lower-quality evidence.

## Condition

Use this pattern when:

- Retrieval returns more candidate chunks than can be sent to generation.
- Top-k retrieval quality varies across query types (exact-match queries vs semantic queries).
- You observe answer quality improving when you manually reorder chunks.

Do not use this pattern when:

- Your retriever already produces consistently high precision in the top positions for your target tasks.
- Added reranking latency would violate strict real-time response constraints.

## Solution

1. Retrieve a broader candidate set from the first-stage retriever (for example top 30-100 chunks).
2. Score each candidate against the user query with a reranker:
   - Rule-based scorer (BM25/MMR/feature-weighted heuristics), or
   - Model-based scorer (cross-encoder or LLM judge).
3. Sort candidates by reranker score and apply diversity constraints to avoid near-duplicate chunks.
4. Keep the top-ranked subset that fits generation budget.
5. Pass ranked chunks plus score and source metadata to the generation step.
6. Monitor reranker impact with offline metrics and end-to-end answer quality tests.

## Example

Example use cases:

1. **Legal Document Analysis**: After retrieving multiple case law references, reranking ensures the most on-point precedents appear first.
2. **Customer Support Knowledge Base**: A chatbot can retrieve numerous articles; reranking helps highlight the most relevant troubleshooting steps.
3. **News Summarization**: From a large corpus of articles, reranking surfaces the most significant pieces of information first.

An internal policy assistant retrieves 50 chunks for the query "Can contractors approve spend above $10k?".

Without reranking, top chunks include generic procurement summaries. After reranking:

1. Chunks that explicitly mention `contractors`, `approval authority`, and `$10k` move to the top.
2. Near-duplicate policy excerpts are collapsed.
3. Only the top 8 chunks are sent to generation.

The final context contains the approval matrix and exceptions section instead of broad policy text.

## Tradeoffs

- Gain: better use of limited context window through stronger ordering.
- Gain: reduced noise in the final generation input.
- Cost: extra inference or scoring latency.
- Cost: more evaluation and maintenance work for scoring logic.

## Failure Modes

- Reranker overfits keyword overlap and suppresses semantically relevant chunks.
- Aggressive diversity filters remove necessary corroborating evidence.
